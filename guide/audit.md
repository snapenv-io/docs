# Audit log

Every pull, push, change, and team action is recorded in an append-only audit log. Rows are never updated or deleted.

## Viewing the audit log

- **Per-project** — open a project → **Audit** tab
- **Workspace-wide** — **Workspace → Audit**

## What's logged

| Action | Trigger |
|---|---|
| `var.create` | Variable created |
| `var.update` | Variable value or type changed |
| `var.delete` | Variable deleted |
| `var.restore` | Variable restored from history |
| `vars.bulk_upsert` | Bulk import or `snapenv push` |
| `vars.bulk_delete` | Multi-select delete |
| `vars.pull` | CLI or operator pull |
| `token.create` | Access token created |
| `token.revoke` | Access token revoked |
| `token.rotate` | Access token rotated |
| `member.invite` | User invited |
| `member.remove` | Member removed |
| `member.role_change` | Workspace role changed |
| `access.grant` | User added to project |
| `access.update` | Project role or env perms changed |
| `access.revoke` | User removed from project |

## Fields

Each log entry includes:

- **Action** — what happened
- **Actor** — user name (or token name for CLI actions)
- **Actor type** — `user` (web/JWT) or `token` (CLI/access token)
- **Target key / env** — which variable or environment was affected
- **Timestamp** — UTC

## API access

```bash
# Project audit
GET /v1/projects/:id/audit?limit=50&cursor=

# Workspace audit
GET /v1/workspace/audit?limit=50
```

Supports cursor-based pagination via the `nextCursor` field in the response.
