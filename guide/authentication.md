# Authentication

SnapEnv uses two credential types depending on the context.

## JWT (web sessions)

Issued by `POST /v1/auth/login`. Used by the dashboard only. Short-lived (7 days). Rejected by the variable pull endpoint — use an access token for automation.

## Access tokens (`snp_live_`)

Created in the dashboard under **Settings → Access tokens**. Used by the CLI, Kubernetes operator, GitHub Actions, and any server-side automation.

```
snp_live_xxxxxxxxxxxxxxxxxxxx
```

Tokens are stored as `bcrypt(sha256(plaintext))` — the plaintext is shown once at creation and never stored. If you lose it, rotate the token to get a new one.

### Token scopes

| Scope | Pull | Push | Notes |
|---|---|---|---|
| `read` | ✓ | — | Default. Use for most integrations. |
| `write` | ✓ | ✓ | Required for `snapenv push` and bulk import from CI. |
| `deploy` | ✓ | — | Same access as `read`. Signals a CI/deploy context. |

### Environment restriction

A token can be restricted to specific environments. A token scoped to `["production"]` will be rejected if used to pull `staging`.

### Project restriction

Optionally restrict a token to a single project. Workspace-wide by default (access to all projects).

### Expiry

Tokens can have an expiry date (30 days, 90 days, 1 year, or no expiry). Expired tokens return 401.

## Using the token

Pass it as a Bearer token:

```bash
curl https://api.snapenv.io/v1/projects/PROJECT_ID/envs/prod/pull \
  -H "Authorization: Bearer snp_live_xxxxxxxxxxxx"
```

Or set the environment variable for the CLI:

```bash
export SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
snapenv pull --env prod
```

## 2FA

Enable TOTP two-factor authentication under **Settings → Security**. Once enabled, login requires a 6-digit code from your authenticator app. Backup codes are provided at enrollment.
