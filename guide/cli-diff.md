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
