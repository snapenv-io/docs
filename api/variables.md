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
