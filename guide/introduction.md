# Introduction

SnapEnv is a secure environment variable manager for dev teams and production servers. It stores your secrets encrypted, delivers them anywhere via CLI or native integrations, and keeps a full audit trail of every access.

## Why SnapEnv?

The typical workflow — `.env` files committed to git, shared over Slack, copy-pasted between servers — is a liability. SnapEnv replaces it with:

- **One source of truth** per environment (`dev`, `staging`, `prod`)
- **Encrypted storage** — AES-256-GCM, unique key per project, zero plaintext in the database
- **Scoped access** — developers can write to staging, read-only on production
- **Audit trail** — every pull, push, and change is recorded

## Architecture

```
dash.snapenv.io  (dashboard)
       │  JWT or snp_live_ token
       ▼
api.snapenv.io   (Go + Gin API)
       │  pgx connection pool
       ▼
PostgreSQL       (encrypted variable values)
```

The API is stateless. Web sessions use short-lived JWTs. CLI and CI authenticate with `snp_live_` access tokens that you create in the dashboard.

## Next steps

- [Quick start](/guide/quick-start) — create a project and pull your first secret
- [CLI installation](/guide/cli) — install the `snapenv` binary
- [Access tokens](/guide/tokens) — create scoped credentials for your tools
