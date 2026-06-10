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
