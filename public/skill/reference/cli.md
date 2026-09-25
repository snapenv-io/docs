==============================================================================
# Source: https://docs.snapenv.io/guide/cli
==============================================================================

# CLI Installation

The `snapenv` binary is a single static executable. No runtime required.

## Supported platforms

| Platform | Architecture |
|---|---|
| macOS | amd64, arm64 (Apple Silicon) |
| Linux | amd64, arm64 |

## Install

```bash
curl -fsSL https://get.snapenv.io/install.sh | sh
```

The install script detects your platform and architecture, downloads the correct binary to `~/.local/bin/snapenv`, and makes it executable.

### Manual download

```bash
# Linux amd64
curl -fsSL https://get.snapenv.io/cli/latest/snapenv-linux-amd64 \
  -o /usr/local/bin/snapenv && chmod +x /usr/local/bin/snapenv

# Linux arm64
curl -fsSL https://get.snapenv.io/cli/latest/snapenv-linux-arm64 \
  -o /usr/local/bin/snapenv && chmod +x /usr/local/bin/snapenv
```

## Configuration

Config is stored at `~/.config/snapenv/config.json` (chmod 600) and written by `snapenv login`.

```json
{
  "apiUrl": "https://api.snapenv.io",
  "token": "snp_live_...",
  "project": "4fac4b02-...",
  "env": "staging"
}
```

### Environment variable overrides

Environment variables always override the config file. Flags override environment variables.

| Variable | Description |
|---|---|
| `SNAPENV_TOKEN` | Access token |
| `SNAPENV_PROJECT` | Project UUID |
| `SNAPENV_ENV` | Environment name |
| `SNAPENV_OUTPUT` | Output file path (pull) |
| `SNAPENV_API_URL` | API base URL |

## Self-update

```bash
snapenv upgrade           # install latest version
snapenv upgrade --check   # check without installing
```

## Commands

| Command | Description |
|---|---|
| [`snapenv login`](/guide/cli#login) | Save credentials to config |
| [`snapenv pull`](/guide/cli-pull) | Pull variables to a file or stdout |
| [`snapenv run`](/guide/cli-run) | Run a command with variables injected — no `.env` file, scrubbed output |
| [`snapenv push`](/guide/cli-push) | Push a local `.env` file to SnapEnv |
| [`snapenv diff`](/guide/cli-diff) | Compare local file to remote |
| [`snapenv projects`](/guide/cli-projects) | List all projects in the workspace |
| `snapenv upgrade` | Self-update the binary |
| `snapenv version` | Print version |

## login

```bash
snapenv login --token snp_live_...
snapenv login --token snp_live_... --api-url https://api.yourcompany.com
```

Writes credentials to `~/.config/snapenv/config.json`.


==============================================================================
# Source: https://docs.snapenv.io/guide/cli-pull
==============================================================================

# snapenv pull

Fetches variables for a project + environment and writes them to a file.

## Usage

```bash
snapenv pull --env prod
snapenv pull --env prod --file /run/secrets/.env
snapenv pull --env prod --stdout
snapenv pull --env prod --format k8s | kubectl apply -f -
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--env` | `$SNAPENV_ENV` | Environment name |
| `--project` | `$SNAPENV_PROJECT` | Project UUID |
| `--file`, `--output` | `.env` | Output file path |
| `--stdout` | — | Print to stdout, skip file write |
| `--format` | `dotenv` | Output format: `dotenv` or `k8s` |
| `--no-metadata` | — | Suppress the injected `SNAPENV_*` context variables |

## Output formats

### dotenv (default)

```
DATABASE_URL=postgres://...
REDIS_URL=redis://...
JWT_SECRET=abc123
```

Written with mode `0600`. Existing file is overwritten.

### k8s

Outputs a Kubernetes `v1/Secret` YAML with base64-encoded `data`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: snapenv-myproject-prod
type: Opaque
data:
  DATABASE_URL: cG9zdGdyZXM6Ly8...
  REDIS_URL: cmVkaXM6Ly8...
```

Pipe directly to `kubectl apply`:

```bash
snapenv pull --env prod --format k8s | kubectl apply -f -
```

## Context variables

Every pull injects a small set of reserved variables so your app, logs, or
deploy scripts can introspect which project and environment they were pulled
from — similar to Doppler's `DOPPLER_*` vars:

```
SNAPENV_PROJECT="9f8c...uuid"
SNAPENV_ENV="prod"
SNAPENV_PROJECT_NAME="Core API"
```

These are **synthetic** — they are never stored as real variables, and a
variable you define yourself with the same name always takes precedence.

Multi-line values (e.g. PEM keys) are emitted double-quoted with escaped
newlines, so they survive standard dotenv parsing and load as a single value.

Disable the context variables per call with `--no-metadata`:

```bash
snapenv pull --env prod --no-metadata
```

`snapenv diff` suppresses them automatically so they never appear as
remote-only additions.

## GitHub Actions integration

When `GITHUB_ACTIONS=true`, `snapenv pull` automatically appends all variables to `$GITHUB_ENV`, making them available to subsequent steps:

```yaml
- name: Pull secrets
  env:
    SNAPENV_TOKEN: ${{ secrets.SNAPENV_TOKEN }}
    SNAPENV_PROJECT: ${{ vars.SNAPENV_PROJECT }}
  run: snapenv pull --env prod

- name: Use secrets
  run: echo $DATABASE_URL   # available from previous step
```

## Non-interactive / auto mode

When `SNAPENV_TOKEN`, `SNAPENV_PROJECT`, and `SNAPENV_ENV` are all set, `snapenv pull` runs non-interactively — no config file required. Useful in CI and init containers.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Any error (auth, network, missing flag) |


==============================================================================
# Source: https://docs.snapenv.io/guide/cli-run
==============================================================================

# snapenv run

Runs a command with variables injected — never written to a `.env` file, and never appearing in anything you (or an AI coding agent driving the CLI on your behalf) actually wrote.

## Usage

```bash
snapenv run --env prod --only DATABASE_URL -- node server.js
snapenv run --env prod --all -- npm start
snapenv run --env prod --only API_TOKEN -- curl -H "Authorization: Bearer {{API_TOKEN}}" https://api.example.com
snapenv run --env staging --all --except DATABASE_URL -- ./migrate.sh
```

The `--` separator is required — everything after it is the command to run, untouched by `snapenv run`'s own flag parsing.

## Flags

| Flag | Default | Description |
|---|---|---|
| `--env` | `$SNAPENV_ENV` | Environment to pull from |
| `--project` | `$SNAPENV_PROJECT` | Project UUID |
| `--only` | — | Comma-separated keys to expose (mutually exclusive with `--all`) |
| `--all` | — | Expose every variable in the environment |
| `--except` | — | Comma-separated keys to exclude — only valid with `--all` |

There's no default scope — running without `--only` or `--all` is a hard error. That's deliberate: a command that's supposed to see one database URL shouldn't silently gain access to every secret in the environment because a flag was forgotten.

## Two ways to receive a value

**As a real environment variable** in the child process — the common case. Any program that reads `process.env` / `os.Getenv` / etc. just works, no code changes:

```bash
snapenv run --env prod --only DATABASE_URL -- node server.js
# server.js reads process.env.DATABASE_URL normally
```

**As a `{{VAR_NAME}}` placeholder** inside the command's own arguments, resolved immediately before exec — for tools like `curl` where the value has to be a literal argument, not something read from the environment:

```bash
snapenv run --only API_TOKEN -- curl -H "Authorization: Bearer {{API_TOKEN}}" https://api.example.com
```

A placeholder referencing a key outside the current scope is an error, and the command never starts — this is what stops a typo (or an over-eager AI agent guessing at a variable name) from silently passing the literal string `{{FOO}}` through instead of failing loudly.

## Output scrubbing

Anything the command prints — stdout or stderr — is scanned as it streams, and any occurrence of an exposed value is replaced with `***` before you (or an agent watching the command's output) ever see it. This is what protects against a secret leaking back out through a side channel the command wasn't asked to use: a verbose `--debug` flag, an accidental `console.log`, a stack trace on crash.

Values shorter than 6 characters are never scrubbed — a `PORT` of `3000` or a `LOG_LEVEL` of `debug` would otherwise collide with completely unrelated output far more often than they'd ever protect anything.

Scrubbing works correctly even when a value is split across two separate writes to the command's output (e.g. a slow process flushing one byte at a time) — the buffering that makes this reliable trades a small amount of latency (at most one secret's length) for correctness, so still effectively real-time for normal output volumes.

## What this is not

`snapenv run` is not a sandbox. It reduces the chance of an honest mistake — a verbose log, a careless `echo $DATABASE_URL`, a crash that dumps the environment — not a guarantee against a program that's deliberately trying to exfiltrate its own environment. If you don't trust the command, `snapenv run` isn't what makes it trustworthy.

## Exit codes

The command's own exit code is passed straight through — `snapenv run` exits with whatever the process it ran exited with. A scope/validation error (bad flags, an out-of-scope placeholder, missing `--`) exits `1` before the command ever starts.


==============================================================================
# Source: https://docs.snapenv.io/guide/cli-push
==============================================================================

# snapenv push

Reads a local `.env` file and upserts variables to SnapEnv. Additive — keys absent from the file are left unchanged remotely.

## Usage

```bash
snapenv push --env dev
snapenv push --env staging --file .env.staging
snapenv push --env prod --dry-run
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--env` | `$SNAPENV_ENV` | Target environment |
| `--project` | `$SNAPENV_PROJECT` | Project UUID |
| `--file` | `.env` | Source file |
| `--dry-run` | — | Print keys that would be sent, no API call |

## Requires write scope

The access token must have `write` scope. A `read`-scoped token will be rejected with `FORBIDDEN`.

## Output

```
✓ 3 created, 2 updated
```

## Notes

- Keys not in the local file are **not** deleted remotely
- To delete a key, use the dashboard or `DELETE /v1/projects/:id/envs/:env/vars/:key`
- Values are encrypted server-side before storage — the CLI sends plaintext over HTTPS


==============================================================================
# Source: https://docs.snapenv.io/guide/cli-diff
==============================================================================

# snapenv diff

Compares a local `.env` file to remote variables. Useful as a CI gate or before pushing.

## Usage

```bash
snapenv diff --env prod
snapenv diff --env prod --file .env.prod
snapenv diff --env prod --keys DATABASE_URL,REDIS_URL
```

## Flags

| Flag | Default | Description |
|---|---|---|
| `--env` | `$SNAPENV_ENV` | Environment to compare against |
| `--project` | `$SNAPENV_PROJECT` | Project UUID |
| `--file` | `.env` | Local file to compare |
| `--keys` | — | Comma-separated key filter |

## Output

Color-coded diff:

```
~ DATABASE_URL   (value differs)
+ FEATURE_FLAG   (remote only — not in local file)
- LEGACY_KEY     (local only — not in remote)
```

| Symbol | Meaning |
|---|---|
| `~` yellow | Key exists in both, values differ |
| `+` green | Remote only (missing locally) |
| `-` red | Local only (missing remotely) |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | No differences |
| `1` | Differences found (or error) |

Exit code `1` on differences makes `snapenv diff` useful as a CI gate to detect config drift:

```yaml
- name: Check for config drift
  run: snapenv diff --env prod
  # Fails the step if local .env doesn't match remote
```


==============================================================================
# Source: https://docs.snapenv.io/guide/cli-projects
==============================================================================

# snapenv projects

Lists all projects in the authenticated workspace.

## Usage

```bash
snapenv projects
```

## Output

```
ID                                    NAME           ENVS
─────────────────────────────────────────────────────────────────
4fac4b02-...                          Northwind API  dev, staging, prod
a1b2c3d4-...                          Frontend       staging, prod
```

Use the `ID` column value as `$SNAPENV_PROJECT` or pass it with `--project` to other commands.
