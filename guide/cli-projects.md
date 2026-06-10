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
