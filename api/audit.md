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
