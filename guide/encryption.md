# Encryption

Your secrets are encrypted at rest and in transit. Security is built into SnapEnv by default — there's nothing to configure.

## Encryption at rest

- **AES-256-GCM** — every variable value is encrypted before it's written to the database.
- **A unique key per project** — projects are cryptographically isolated, so exposure of one project's data never affects another.
- **Server-side decryption only** — values are only decrypted when you explicitly read or pull them through an authenticated, authorized request.
- **No plaintext in the database** — the database stores ciphertext only. Even a full database dump contains no readable secrets and no keys.

## Credentials

- **Access tokens** and **passwords** are stored as one-way hashes, never in plaintext.
- An access token's plaintext value is shown **once** at creation and never again.

## Encryption in transit

All traffic to SnapEnv is served over **HTTPS (TLS 1.2+)**, including the dashboard, API, and CLI.

## Key handling

Encryption keys are managed entirely server-side. They are never returned by the API, never sent to the CLI or dashboard, and never written to logs.

## Additional protection

- **Two-factor authentication (2FA)** for accounts — see [Two-Factor Authentication](/guide/2fa).
- **Append-only audit log** of every access and change — see [Audit Log](/guide/audit).
- **Scoped, revocable access tokens** for machines and CI — see [Access Tokens](/guide/tokens).
