# Encryption

## Variable encryption

Every variable value is encrypted before any database write and decrypted server-side only.

```
key  = HKDF-SHA256(MASTER_KEY, salt=projectID, info="snapenv-variable-key")
data = AES-256-GCM(key, plaintext)  →  stores (ciphertext, iv)
```

- **`MASTER_KEY`** — 32-byte hex environment variable on the API server only. Never stored in the database, never sent to the CLI.
- **Per-project key derivation** — each project gets a unique encryption key derived from `MASTER_KEY`. A breach of one project's key (impossible without `MASTER_KEY`) exposes nothing from other projects.
- **Unique IV per write** — every variable write generates a fresh 12-byte random IV. AES-GCM provides both confidentiality and integrity.
- **Zero plaintext in DB** — the `variables` table stores `(value_enc BYTEA, iv BYTEA)`. No plaintext ever.

## What the database contains

If someone exfiltrated the entire PostgreSQL database they would get:

- AES-256-GCM ciphertext (useless without `MASTER_KEY`)
- Random IVs
- bcrypt hashes of access tokens (pre-hashed with SHA-256 before bcrypt)
- bcrypt hashes of passwords

No plaintext secrets. No decryption keys.

## Token storage

Access tokens are stored as `bcrypt(sha256(plaintext))`:

1. SHA-256 pre-hash — avoids bcrypt's 72-byte input truncation for long tokens
2. bcrypt (cost 12) — makes brute-force impractical

The plaintext is returned once at creation and never stored.

## In-transit encryption

All traffic is over HTTPS (TLS 1.2+). Caddy handles TLS termination with automatic Let's Encrypt certificates.

## Key management

`MASTER_KEY` lives only in `/etc/snapenv/api.env` (chmod 600) on the API server. It is never:
- Stored in the database
- Returned by any API endpoint
- Included in logs or error messages
- Accessible to the CLI or dashboard
