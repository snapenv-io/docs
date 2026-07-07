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
