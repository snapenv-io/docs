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
