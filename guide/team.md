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
