==============================================================================
# Source: https://docs.snapenv.io/guide/variables
==============================================================================

# Variables

Variables are the core resource in SnapEnv. Each variable belongs to a project + environment combination.

## Types

| Type | Description |
|---|---|
| `secret` | Value is masked in the UI by default. Shown only with explicit reveal. |
| `plain` | Value is always visible. Use for non-sensitive config like feature flags or region names. |

## Adding variables

In the dashboard, open a project → select an environment → click **Add variable**. You can also bulk-import by pasting a `.env` file directly.

## Editing

Click any variable row to edit. Changes are saved immediately. Every change creates a history entry.

## Bulk operations

Select multiple variables using the checkbox column to:
- **Delete** — permanently removes selected keys from the environment
- **Change type** — toggle between `secret` and `plain` in one action

## Variable history

Every write (create, update, delete) is recorded. Click a variable → **History** to see all versions with timestamps and actors. Click **Restore** on any entry to roll back to that value.

## Variable references

Use `${VAR}` syntax in a value to reference another variable in the same environment, instead of duplicating values across keys. Resolves dynamically at read time — change the referenced variable once and everything that points to it updates automatically.

See [Variable references](/guide/variable-references) for syntax, fallback values, and circular-reference behavior.

## Expiry dates

Set an expiry date on a variable to track when a credential needs rotating. SnapEnv sends an email reminder when a secret is within 7 days of expiry.

See [Variable expiry](/guide/expiry) for details.

## Masked values

By default, values are shown as `•••••••`. Click the eye icon to reveal. Your preference (always show / always mask) is saved per account in Settings.

## Copying across environments

Use the dashboard's copy feature to duplicate a variable's value from one environment to another, or use the API to read from one env and write to another.


==============================================================================
# Source: https://docs.snapenv.io/guide/variable-references
==============================================================================

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


==============================================================================
# Source: https://docs.snapenv.io/guide/environments
==============================================================================

# Environments

Each project has one or more environments. Variables are scoped per environment — `DATABASE_URL` in `prod` is completely independent from `DATABASE_URL` in `staging`.

## Default environments

New projects are created with `dev`, `staging`, and `prod` by default.

## Protected environments

Environments can be marked **protected** to keep production secrets out of reach of every
developer by default. `prod` and `production` are protected automatically; you can protect
any environment (e.g. a prod-like `live` or `eu-prod`) with the 🔒 **Protect env** button in
the project toolbar — Owners only.

On a protected environment, members with the **Developer** project role get **no default
access** (they can't read or write its secrets) unless an Owner or Admin grants them an
explicit per-environment permission. Admins, Read-only members, and Owners are unaffected.
See [Permissions → Protected environments](/guide/permissions#protected-environments).

## Adding environments

Project → **Settings → Environments → Add**. Enter a name (e.g. `canary`, `eu-prod`, `qa`).

## Deleting environments

Project → **Settings → Environments → Delete**. This permanently deletes all variables in that environment. This action cannot be undone.

## Using environments in the CLI

```bash
snapenv pull --env prod
snapenv pull --env staging
snapenv pull --env canary
```

## Environment colors

Each environment has an associated color used throughout the dashboard UI (`prod` = red, `staging` = yellow, `dev` = green by default). You can customize colors per project.


==============================================================================
# Source: https://docs.snapenv.io/guide/expiry
==============================================================================

# Variable expiry

Set an expiry date on any variable to track when a credential needs to be rotated.

## Setting an expiry

Open a variable in the dashboard → click the expiry field → pick a date. Or via the API:

```bash
curl -X PUT https://api.snapenv.io/v1/projects/PROJECT_ID/envs/prod/vars/API_KEY \
  -H "Authorization: Bearer snp_live_..." \
  -H "Content-Type: application/json" \
  -d '{"expiresAt": "2026-12-31T00:00:00Z"}'
```

## Email reminders

When any variable in your workspace expires within **7 days**, SnapEnv sends an email to workspace Owners. Reminders are sent at most once per 24 hours per workspace.

## Clearing an expiry

In the dashboard, open the variable and clear the expiry date. Via the API:

```json
{ "clearExpiry": true }
```

## Viewing expiring variables

In the dashboard, variables with approaching expiry dates are highlighted in the variable list. Filter by expiry using the expiry indicator in the variable row.


==============================================================================
# Source: https://docs.snapenv.io/guide/encryption
==============================================================================

# Encryption

Your secrets are encrypted at rest and in transit. Security is built into SnapEnv by default — there's nothing to configure.

## Encryption at rest

- **AES-256-GCM** — every variable value is encrypted before it's written to the database.
- **A unique key per project** — projects are cryptographically isolated, so exposure of one project's data never affects another.
- **Server-side decryption only** — values are only decrypted when you explicitly read or pull them through an authenticated, authorized request.
- **No plaintext in the database** — the database stores ciphertext only. Even a full database dump contains no readable secrets and no keys.

## Credentials

- **Access tokens** and **passwords** are stored as one-way hashes, never in plaintext.
- An access token's plaintext value is shown **once** at creation and never again.

## Encryption in transit

All traffic to SnapEnv is served over **HTTPS (TLS 1.2+)**, including the dashboard, API, and CLI.

## Key handling

Encryption keys are managed entirely server-side. They are never returned by the API, never sent to the CLI or dashboard, and never written to logs.

## Additional protection

- **Two-factor authentication (2FA)** for accounts — see [Two-Factor Authentication](/guide/2fa).
- **Append-only audit log** of every access and change — see [Audit Log](/guide/audit).
- **Scoped, revocable access tokens** for machines and CI — see [Access Tokens](/guide/tokens).
