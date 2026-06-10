# Variables API

## GET /v1/projects/:id/envs/:env/vars

List variables. Values are masked by default.

```
?reveal=true   — return plaintext values (requires write permission)
```

```json
{
  "vars": [
    { "key": "DATABASE_URL", "value": "***", "type": "secret", "updatedAt": "...", "expiresAt": null }
  ]
}
```

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

## GET /v1/projects/:id/envs/:env/export

Download all variables as a file.

```
?format=dotenv   (default) or k8s
?reveal=true     include plaintext values (requires write perm)
```
