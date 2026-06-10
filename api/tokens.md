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
