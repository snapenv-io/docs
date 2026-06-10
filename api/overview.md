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
