# Webhooks

Fire HTTP POST requests to any URL when variables change. Use them to trigger deployments, notify Slack, or invalidate caches.

## Create a webhook

**Workspace → Settings → Webhooks → Add webhook**.

- **URL** — the endpoint to POST to
- **Events** — which events trigger this webhook
- **Secret** — auto-generated `whsec_…` signing secret (shown once)

## Events

| Event | When |
|---|---|
| `var.update` | Single variable updated |
| `var.delete` | Single variable deleted |
| `var.restore` | Variable restored from history |
| `vars.bulk_upsert` | Bulk save (dashboard or `snapenv push`) |
| `vars.bulk_delete` | Bulk delete |
| `vars.pull` | Variables pulled via CLI or operator |

## Payload

```json
{
  "event": "vars.bulk_upsert",
  "projectId": "uuid",
  "env": "production",
  "actor": "Dana Whitfield",
  "keys": ["DATABASE_URL", "REDIS_URL"],
  "created": ["REDIS_URL"],
  "updated": ["DATABASE_URL"],
  "timestamp": "2026-06-01T10:00:00Z"
}
```

## Verifying signatures

Every delivery includes an `X-SnapEnv-Signature` header:

```
X-SnapEnv-Signature: sha256=<hmac-hex>
```

Verify on receipt using `HMAC-SHA256(signingSecret, rawRequestBody)`:

```python
import hmac, hashlib

def verify(secret: str, body: bytes, header: str) -> bool:
    expected = "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, header)
```

```typescript
import { createHmac, timingSafeEqual } from 'crypto';

function verify(secret: string, body: string, header: string): boolean {
  const expected = 'sha256=' + createHmac('sha256', secret).update(body).digest('hex');
  return timingSafeEqual(Buffer.from(expected), Buffer.from(header));
}
```

## Delivery log

The dashboard shows the last delivery status (HTTP status code) and timestamp for each webhook. Deliveries are async with a 10-second timeout.
