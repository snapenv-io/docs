==============================================================================
# Source: https://docs.snapenv.io/api/overview
==============================================================================

# API Overview

**Base URL:** `https://api.snapenv.io`  
All endpoints are under the `/v1/` prefix.

## Authentication

```
Authorization: Bearer <credential>
```

Two credential types:

| Type | Format | Use case |
|---|---|---|
| **JWT** | `eyJ…` | Dashboard sessions only |
| **Access token** | `snp_live_…` | CLI, CI/CD, server scripts, operator |

Variable endpoints (`/projects/*`) accept both. Account and workspace endpoints (`/me/*`, `/workspace/*`) require a JWT.

## Error format

All non-2xx responses:

```json
{
  "error": {
    "code": "SNAKE_CASE",
    "message": "Human readable description",
    "field": "fieldName"
  }
}
```

Common codes:

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `VALIDATION` | Missing or invalid field |
| 401 | `UNAUTHORIZED` | Missing, expired, or invalid credential |
| 403 | `FORBIDDEN` | Insufficient role or permission |
| 404 | `NOT_FOUND` | Resource does not exist |
| 409 | `CONFLICT` | Duplicate (e.g. email already registered) |
| 429 | `RATE_LIMIT` | Too many requests |
| 500 | `SERVER` | Internal error |

## Rate limits

| Endpoint | Limit |
|---|---|
| `POST /v1/auth/login` | 10 req/min per IP |
| `POST /v1/auth/resend-verification` | 1 req/min per user |
| All other endpoints | No hard limit |

## Sections

- [Authentication](/api/authentication) — login, signup, 2FA, session
- [Projects](/api/projects) — CRUD, environments, diff
- [Variables](/api/variables) — list, create, update, history, pull
- [Tokens](/api/tokens) — create, list, rotate, revoke
- [Workspace](/api/workspace) — settings, team, billing, webhooks
- [Webhooks](/api/webhooks) — create, list, payload format
- [Audit](/api/audit) — log endpoints


==============================================================================
# Source: https://docs.snapenv.io/api/authentication
==============================================================================

# Authentication API

## POST /v1/auth/signup

Create an account and workspace.

```json
// request
{ "name": "Dana Whitfield", "email": "dana@acme.com", "password": "s3cr3t" }

// response 201
{ "token": "<jwt>", "user": { "id": "uuid", "name": "Dana Whitfield", "email": "dana@acme.com" } }
```

## POST /v1/auth/login

```json
// request
{ "email": "dana@acme.com", "password": "s3cr3t" }

// response — 2FA not enabled
{ "token": "<jwt>", "user": { ... } }

// response — 2FA enabled
{ "mfaRequired": true, "mfaToken": "<short-lived-jwt>" }
```

When `mfaRequired: true`, prompt for TOTP code and call `POST /v1/auth/verify-mfa`. The `mfaToken` expires in 5 minutes.

## POST /v1/auth/verify-mfa

```json
// request
{ "mfaToken": "<mfa-jwt>", "code": "123456" }

// response 200
{ "token": "<full-jwt>", "user": { ... } }
```

Accepts ±1 TOTP window (90 seconds total) and single-use backup codes.

## GET /v1/auth/session

Validate the stored JWT and return the current user. Called on every page load.

```json
{
  "user": {
    "id": "uuid",
    "name": "Dana Whitfield",
    "email": "dana@acme.com",
    "workspaceId": "uuid",
    "workspaceName": "Acme Corp",
    "wsRole": "Owner",
    "emailVerifiedAt": "2025-01-01T00:00:00Z"
  }
}
```

Returns 401 if the token is invalid, expired, or MFA-pending.

## POST /v1/auth/accept-invite

Accept a workspace invite. `token` is from the invite link.

```json
// request
{ "token": "a3f9b2..." }

// response 200
{ "token": "<jwt>", "workspaceId": "uuid", "workspaceName": "Acme Corp", "wsRole": "Member" }
```

## POST /v1/auth/switch-workspace

Issue a new JWT scoped to a different workspace the caller belongs to.

```json
// request
{ "workspaceId": "uuid" }
// response 200
{ "token": "<jwt>", "workspaceId": "uuid", "workspaceName": "Acme Corp" }
```


==============================================================================
# Source: https://docs.snapenv.io/api/projects
==============================================================================

# Projects API

## GET /v1/projects

```json
{
  "projects": [
    { "id": "uuid", "name": "Backend API", "desc": "Core gateway", "color": "#3b82f6", "envs": ["dev","staging","prod"] }
  ]
}
```

## POST /v1/projects

```json
// request
{ "name": "Backend API", "desc": "optional", "color": "#3b82f6", "envs": ["staging","prod"] }
// response 201 — same shape as list item
```

## GET /v1/projects/:id

Same shape as a list item.

## PATCH /v1/projects/:id

```json
// request — all optional
{ "name": "New Name", "desc": "Updated", "color": "#8b5cf6" }
// response 200 — same shape
```

## DELETE /v1/projects/:id

Permanently deletes the project and all its variables, history, and audit logs. Owner only. Returns 204.

## POST /v1/projects/:id/envs

```json
// request
{ "name": "canary" }
// response 201 — updated project with new env in envs array
```

## DELETE /v1/projects/:id/envs/:env

Deletes the environment and all its variables. Returns 204.

## GET /v1/projects/:id/diff

Compare variables between two environments.

```
?env=prod&env=staging
```

```json
{
  "onlyInA": ["FEATURE_FLAG"],
  "onlyInB": ["LEGACY_KEY"],
  "different": ["DATABASE_URL", "REDIS_URL"]
}
```


==============================================================================
# Source: https://docs.snapenv.io/api/variables
==============================================================================

# Variables API

## GET /v1/projects/:id/envs/:env/vars

List variables. Values are masked by default.

```
?reveal=true   — return plaintext values (requires write permission)
```

```json
{
  "vars": [
    { "key": "DATABASE_URL", "value": "***", "type": "secret", "updatedAt": "...", "expiresAt": null },
    { "key": "API_URL", "value": "${APP_URL}/api", "type": "plain", "updatedAt": "...", "expiresAt": null,
      "resolvedValue": "https://app.com/api" }
  ]
}
```

`resolvedValue` is included only when a value contains a [variable reference](/guide/variable-references) (`${VAR}` syntax) — the raw `value` field always stays whatever was actually stored, so editing shows the literal reference, not the resolved result. A reference stuck in a circular chain adds a `resolveError` string instead of resolving.

## POST /v1/projects/:id/vars

Bulk upsert across one or more environments.

```json
// request
{
  "envs": ["production", "staging"],
  "items": [{ "key": "FOO", "value": "bar", "type": "secret" }]
}

// response 200
{ "created": ["FOO"], "updated": ["DATABASE_URL"] }
```

## PUT /v1/projects/:id/envs/:env/vars/:key

Update a single variable.

```json
// request — all fields optional
{ "value": "new-value", "type": "plain", "expiresAt": "2025-12-31T00:00:00Z", "clearExpiry": false }

// response 200
{ "key": "FOO", "value": "new-value", "type": "plain", "updatedAt": "...", "expiresAt": "..." }
```

Set `clearExpiry: true` to remove an existing expiry date.

## DELETE /v1/projects/:id/envs/:env/vars/:key

Returns 204.

## POST /v1/projects/:id/envs/:env/vars:bulkDelete

```json
// request
{ "keys": ["FOO", "BAR"] }
// response 200
{ "deleted": 2 }
```

## GET /v1/projects/:id/envs/:env/vars/:key/history

```json
{
  "history": [
    { "id": 42, "value": "***", "type": "secret", "action": "updated", "changedBy": "uuid", "changedAt": "..." }
  ]
}
```

Append `?reveal=true` for plaintext.

## POST /v1/projects/:id/envs/:env/vars/:key/restore

```json
// request
{ "versionId": 42 }
// response 200 — the restored variable
{ "key": "FOO", "value": "***", "type": "secret", "updatedAt": "..." }
```

## GET /v1/projects/:id/envs/:env/pull

The CLI and Kubernetes operator endpoint. Returns variables as dotenv text.

```
Authorization: Bearer snp_live_...
X-SnapEnv-Client: operator   (optional — used by k8s operator to track sync time)
```

Response: `text/plain` dotenv format.

The dotenv body also appends synthetic **context variables** —
`SNAPENV_PROJECT`, `SNAPENV_ENV`, `SNAPENV_PROJECT_NAME` — so consumers can
introspect their source. They are never stored, and a user-defined variable of
the same name wins. Values are static, so the response `ETag` (used by the k8s
operator for `304` conditional sync) stays stable. Suppress with
`?metadata=false`.

Multi-line values are emitted double-quoted with escaped newlines so they
survive standard dotenv parsing.

Values containing a [variable reference](/guide/variable-references) (`${VAR}` syntax)
are resolved before output — the dotenv body always carries final values, never
the raw `${...}` text. If a reference is part of a circular chain, Pull hard-fails
rather than shipping broken config:

```json
// response 422
{ "error": "CIRCULAR_REFERENCE", "message": "API_URL: circular reference detected", "key": "API_URL" }
```

## GET /v1/projects/:id/envs/:env/export

Download all variables as a file.

```
?format=dotenv   (default) or k8s
?reveal=true     include plaintext values (requires write perm)
?metadata=false  omit the injected SNAPENV_* context variables (default: on)
```

Variable references are resolved the same way as Pull, but a circular reference
here never blocks the download — the affected value is left unresolved rather
than failing the whole export.


==============================================================================
# Source: https://docs.snapenv.io/api/tokens
==============================================================================

# Tokens API

## GET /v1/tokens

```json
{
  "tokens": [
    {
      "id": "uuid", "name": "CI Deploy", "tokenPrefix": "snp_live_XX",
      "scope": "read", "envs": ["production"], "projectId": null,
      "lastUsedAt": null, "expiresAt": null, "createdAt": "..."
    }
  ]
}
```

## POST /v1/tokens

```json
// request
{
  "name": "CI Deploy",
  "scope": "read",
  "envs": ["production"],
  "projectId": null,
  "expiresIn": 90
}

// response 201
{
  "id": "uuid",
  "token": "snp_live_XXXXXXXXXXXX",
  "name": "CI Deploy", "scope": "read",
  "envs": ["production"], "projectId": null,
  "expiresAt": "2026-09-07T00:00:00Z"
}
```

`token` is the plaintext — shown once only. `projectId: null` means workspace-wide.

## POST /v1/tokens/:id/rotate

Revoke and reissue with the same settings. Returns the new plaintext token.

```json
// response 200
{ "id": "uuid", "token": "snp_live_YYYYYYYY", "name": "CI Deploy", "scope": "read", "envs": ["production"] }
```

## DELETE /v1/tokens/:id

Revoke immediately. Returns 204.


==============================================================================
# Source: https://docs.snapenv.io/api/workspace
==============================================================================

# Workspace API

## GET /v1/workspace

```json
{ "id": "uuid", "name": "Acme Corp", "slug": "acme-corp" }
```

## PATCH /v1/workspace

Rename. Owner only.

```json
{ "name": "Acme Corp Inc." }
```

## GET /v1/workspace/billing

```json
{
  "plan": "free",
  "limits": { "projects": 3, "members": 3, "envsPerProject": 3 },
  "usage":  { "projects": 2, "members": 1 }
}
```

`-1` in limits means unlimited.

## GET /v1/workspace/connections

Integration connection status.

```json
{
  "operator": {
    "connected": true,
    "lastSync": "2026-06-10T14:30:00Z"
  }
}
```

## GET /v1/workspace/stats

```json
{ "memberCount": 4, "projectCount": 3, "variableCount": 142, "tokenCount": 2 }
```

## GET /v1/workspace/members

```json
{
  "members": [
    { "id": "uuid", "name": "Dana Whitfield", "email": "dana@acme.com", "wsRole": "Owner", "joinedAt": "..." }
  ]
}
```

## POST /v1/workspace/invites

```json
// request
{ "email": "new@acme.com", "wsRole": "Member" }

// response 200 — existing user
{ "userId": "uuid", "name": "...", "wsRole": "Member" }

// response 202 — new user, invite sent
{ "invited": true, "email": "new@acme.com" }
```

## PATCH /v1/workspace/members/:userId

```json
{ "wsRole": "Owner" }
```

## DELETE /v1/workspace/members/:userId

Returns 204. Owners can't remove themselves.


==============================================================================
# Source: https://docs.snapenv.io/api/audit
==============================================================================

# Audit API

## GET /v1/projects/:id/audit

```
?limit=50&cursor=<nextCursor>
```

```json
{
  "logs": [
    {
      "id": 42, "action": "var.update",
      "targetKey": "DATABASE_URL", "targetEnv": "production",
      "actorId": "uuid", "actorType": "user",
      "detail": null, "createdAt": "..."
    }
  ],
  "nextCursor": "42"
}
```

## GET /v1/workspace/audit

```
?limit=50
```

Same shape as project audit. Spans all projects in the workspace.

## Actor types

| `actorType` | Meaning |
|---|---|
| `user` | Action taken via the dashboard (JWT) |
| `token` | Action taken via CLI or API with an access token |
