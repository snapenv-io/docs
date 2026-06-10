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
