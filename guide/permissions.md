# Permissions

SnapEnv enforces three layers of access control on every request.

## Layer 1: Workspace role

| Role | Access |
|---|---|
| **Owner** | Full access to all projects, all environments, billing, and team management. Bypasses all project-level checks. |
| **Member** | Access is determined by project roles. |

## Layer 2: Project role

Assigned per user per project.

| Role | Default prod | Default staging | Default dev |
|---|---|---|---|
| **Admin** | write | write | write |
| **Developer** | read | write | write |
| **Read-only** | read | read | read |

These are the defaults — individual environment permissions can be overridden.

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
