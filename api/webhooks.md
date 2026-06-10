# Webhooks API

See [Webhooks guide](/guide/webhooks) for the payload format and signature verification.

## GET /v1/workspace/webhooks

```json
{
  "webhooks": [
    {
      "id": "uuid", "name": "Deploy trigger",
      "url": "https://hooks.example.com/deploy",
      "events": ["vars.bulk_upsert", "var.update"],
      "active": true, "lastFiredAt": "...", "lastStatus": 200, "createdAt": "..."
    }
  ]
}
```

## POST /v1/workspace/webhooks

Owner only.

```json
// request
{ "name": "Deploy trigger", "url": "https://hooks.example.com/deploy", "events": ["vars.bulk_upsert"] }

// response 201
{
  "id": "uuid", "name": "Deploy trigger",
  "url": "https://hooks.example.com/deploy",
  "events": ["vars.bulk_upsert"],
  "active": true,
  "secret": "whsec_..."
}
```

`secret` is shown once — use it to verify incoming payloads.

## PATCH /v1/workspace/webhooks/:id

Owner only. All fields optional.

```json
{ "name": "New name", "url": "https://...", "events": [...], "active": false }
```

## DELETE /v1/workspace/webhooks/:id

Owner only. Returns 204.
