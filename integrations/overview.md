# Integrations overview

Every integration authenticates with an [access token](/guide/tokens). Create one in the dashboard under **Settings → Access tokens**.

## Available integrations

| Integration | Best for |
|---|---|
| [CLI](/guide/cli) | Servers, local dev, scripts |
| [Kubernetes Operator](/integrations/kubernetes) | Auto-sync into native K8s Secrets |
| [GitHub Actions](/integrations/github-actions) | CI/CD pipelines |
| [Docker / Compose](/integrations/docker) | Container startup |
| [Init containers](/integrations/init-container) | Kubernetes without the operator |
| [Vercel](/integrations/vercel) | Build-time secrets for serverless/static deploys |
| [Railway](/integrations/railway) | Long-running services, via `snapenv run` |
| [Render](/integrations/render) | Long-running services, via `snapenv run` |
| [Dokploy](/integrations/dokploy) | Self-hosted PaaS, via `snapenv run` |
| [Coolify](/integrations/coolify) | Self-hosted PaaS, via `snapenv run` |

## Common pattern

All integrations follow the same pattern:

1. Create an access token in the dashboard
2. Store the token as a secret in your target system (GitHub Secret, K8s Secret, etc.)
3. Use `snapenv pull` (CLI, Docker) or a native integration (K8s Operator) to fetch variables at runtime
