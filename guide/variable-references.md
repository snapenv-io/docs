# Variable references

Reference one variable's value from another using `${VAR}` syntax, instead of duplicating the same value across multiple keys.

```
APP_URL=https://app.example.com
API_URL=${APP_URL}/api
```

`API_URL` always resolves to `https://app.example.com/api` — change `APP_URL` once and every variable that references it updates automatically, with no need to touch each one by hand.

## Fallback values

Use `${VAR:-fallback}` to substitute a default when the referenced variable is unset or empty:

```
LOG_LEVEL=${LOG_LEVEL:-info}
```

The fallback fires whenever the referenced variable is missing **or** empty — not just when it's undefined.

## Chained references

References can chain through multiple variables:

```
REGION=us-east-1
BUCKET=snapenv-${REGION}
BACKUP_URL=s3://${BUCKET}/backups
```

`BACKUP_URL` resolves through `BUCKET` and `REGION` to `s3://snapenv-us-east-1/backups`.

## Circular references

A reference chain that loops back on itself (`A` → `B` → `A`) can't resolve. Behavior differs by endpoint:

- **Pull** (CLI, Kubernetes operator) fails with `422 CIRCULAR_REFERENCE` rather than injecting broken config into a running service.
- **List and Export** resolve everything they can and flag only the affected variable, so you can still see and fix the rest of your variables.

## Where it applies

References are resolved dynamically, scoped to a single project + environment — a variable can only reference other variables in the same environment. Resolution happens server-side at read time; the stored value is always the literal `${VAR}` text, so editing a variable shows the reference, not the resolved result.

- **Dashboard**: the variable list shows a **resolved** badge on any value containing a reference — hover it to see what it resolves to, or a **cycle** badge if it's part of a circular reference.
- **CLI** (`pull`, `run`): receives already-resolved values — no changes needed on your end.
- **API**: see [List](/api/variables#get-v1-projects-id-envs-env-vars) and [Pull](/api/variables#get-v1-projects-id-envs-env-pull) for exact response shapes.
