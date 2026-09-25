==============================================================================
# Source: https://docs.snapenv.io/guide/authentication
==============================================================================

# Authentication

SnapEnv uses two credential types depending on the context.

## JWT (web sessions)

Issued by `POST /v1/auth/login`. Used by the dashboard only. Short-lived (7 days). Rejected by the variable pull endpoint — use an access token for automation.

## Access tokens (`snp_live_`)

Created in the dashboard under **Settings → Access tokens**. Used by the CLI, Kubernetes operator, GitHub Actions, and any server-side automation.

```
snp_live_xxxxxxxxxxxxxxxxxxxx
```

Tokens are stored as `bcrypt(sha256(plaintext))` — the plaintext is shown once at creation and never stored. If you lose it, rotate the token to get a new one.

### Token scopes

| Scope | Pull | Push | Notes |
|---|---|---|---|
| `read` | ✓ | — | Default. Use for most integrations. |
| `write` | ✓ | ✓ | Required for `snapenv push` and bulk import from CI. |
| `deploy` | ✓ | — | Same access as `read`. Signals a CI/deploy context. |

### Environment restriction

A token can be restricted to specific environments. A token scoped to `["production"]` will be rejected if used to pull `staging`.

### Project restriction

Optionally restrict a token to a single project. Workspace-wide by default (access to all projects).

### Expiry

Tokens can have an expiry date (30 days, 90 days, 1 year, or no expiry). Expired tokens return 401.

## Using the token

Pass it as a Bearer token:

```bash
curl https://api.snapenv.io/v1/projects/PROJECT_ID/envs/prod/pull \
  -H "Authorization: Bearer snp_live_xxxxxxxxxxxx"
```

Or set the environment variable for the CLI:

```bash
export SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
snapenv pull --env prod
```

## 2FA

Enable TOTP two-factor authentication under **Settings → Security**. Once enabled, login requires a 6-digit code from your authenticator app. Backup codes are provided at enrollment.


==============================================================================
# Source: https://docs.snapenv.io/guide/tokens
==============================================================================

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


==============================================================================
# Source: https://docs.snapenv.io/guide/permissions
==============================================================================

# Permissions

SnapEnv enforces three layers of access control on every request.

## Layer 1: Workspace role

| Role | Access |
|---|---|
| **Owner** | Full access to all projects, all environments, billing, and team management. Bypasses all project-level checks. |
| **Member** | Access is determined by project roles. |

## Layer 2: Project role

Assigned per user per project. The role sets **default** environment permissions,
which depend on whether an environment is [protected](#protected-environments):

| Role | Protected env (e.g. prod) | Unprotected env (e.g. dev/staging) |
|---|---|---|
| **Admin** | write | write |
| **Developer** | **none** | write |
| **Read-only** | read | read |

Developers get **no default access to protected environments** — least privilege,
so production secrets aren't exposed to every developer. An Admin or Owner can still
grant a specific developer `read` or `write` on a protected environment using a
per-environment override (Layer 3).

These are the defaults — individual environment permissions can always be overridden.

## Protected environments

Each environment carries a **`protected`** flag. `prod` and `production` are protected
by default; every other environment starts unprotected. Protection is what drives the
"Developer gets no default access" rule above — and it keys off the flag, **not** the
environment's name, so a production environment named `live` or `main` is fully covered
once you mark it protected.

Protecting an environment **only** changes the default for the **Developer** role. It does
**not** restrict Owners, Admins, or Read-only members, and it doesn't change how secrets
are stored (everything is AES-256 encrypted regardless).

Workspace Owners can toggle protection from the project toolbar (the 🔒 **Protect env**
button) or via the API:

```bash
# PATCH /v1/projects/:id/envs/:env
curl -X PATCH https://api.snapenv.io/v1/projects/$PROJECT/envs/prod \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"protected": true}'
```

## Layer 3: Per-environment permission

The finest level of control. Set per user per project per environment.

| Value | Description |
|---|---|
| `none` | No access — can't see or pull this environment |
| `read` | Can pull variables, can't modify |
| `write` | Full read + write access |

## Token permissions

Access tokens have their own permission layer:
- **Scope** (`read` / `write` / `deploy`) — controls pull vs push
- **Env restriction** — limits which environments the token can access
- **Project restriction** — optionally limits to a single project

A token's effective access is the intersection of its own scope and the user permissions of the token's creator — a token can never exceed the creator's own access.

## Enforcement

All permission checks are enforced server-side. The dashboard only shows UI elements the user has access to, but the API will reject unauthorized requests regardless.


==============================================================================
# Source: https://docs.snapenv.io/guide/team
==============================================================================

# Team & access

SnapEnv has three layers of access control, all enforced server-side.

## Workspace roles

| Role | Description |
|---|---|
| **Owner** | Full access to everything — all projects, all environments, billing, team management |
| **Member** | Access determined by project roles below |

Owners bypass all project-level checks. Members only see and access projects they've been explicitly added to.

## Project roles

| Role | Default prod | Default staging/dev |
|---|---|---|
| **Admin** | write | write |
| **Developer** | read | write |
| **Read-only** | read | read |

Assign a project role from the project's **Settings → Team** tab. You can also override per-environment permissions individually.

## Per-environment permissions

The finest level of control. Three values:

- `none` — no access (can't see the environment at all)
- `read` — can pull variables, can't modify
- `write` — full read + write access

## Inviting members

**Workspace → Team → Invite**. Enter an email address and choose a workspace role.

- If the email already has a SnapEnv account, they're added immediately and notified by email.
- If not, an invite link is sent. The link expires in 7 days.

After joining, add them to individual projects from each project's Settings tab.

## Removing members

**Workspace → Team → Remove**. Access is revoked immediately. Their project memberships are also removed.

## Audit log

Every team action is recorded: invites, role changes, additions, removals. See [Audit log](/guide/audit).
