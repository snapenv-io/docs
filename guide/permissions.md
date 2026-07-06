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
