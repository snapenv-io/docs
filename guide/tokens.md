# Access tokens

Access tokens authenticate the CLI, Kubernetes operator, GitHub Actions, and any server-side automation against the SnapEnv API.

## Create a token

Dashboard → **Settings → Access tokens → New token**.

### Options

**Name** — how you'll recognize it in the list (e.g. `CI · GitHub Actions`, `k8s · production`).

**Scope**

| Scope | Pull | Push |
|---|---|---|
| `read` | ✓ | — |
| `write` | ✓ | ✓ |
| `deploy` | ✓ | — |

**Environment access** — select which environments this token can read/write. Leave all selected for unrestricted access.

**Project access** — leave blank for workspace-wide access, or pin to a single project. A project-scoped token returns `403` for any other project.

**Expiry** — 30 days, 90 days, 1 year, or no expiry.

## Token format

```
snp_live_xxxxxxxxxxxxxxxxxxxx
```

The plaintext is shown **once** at creation. Store it immediately in your secret manager, CI environment, or Kubernetes Secret. If you lose it, rotate the token.

## Rotate

Click the rotate icon next to a token. A new token is issued with the same name, scope, and permissions. The old token is revoked immediately — update any services using it before rotating.

## Revoke

Click **Revoke** to permanently invalidate a token. Revocation is immediate.

## Usage

```bash
# CLI
snapenv login --token snp_live_xxxxxxxxxxxx

# Environment variable (no config file needed)
export SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
snapenv pull --env prod

# Direct API call
curl https://api.snapenv.io/v1/projects/PROJECT_ID/envs/prod/pull \
  -H "Authorization: Bearer snp_live_xxxxxxxxxxxx"
```
