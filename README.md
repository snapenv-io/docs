# SnapEnv Docs

Source for [docs.snapenv.io](https://docs.snapenv.io) — documentation for **SnapEnv**, a secure, hosted environment-variable and secrets manager for dev teams. Encrypted storage per project and environment, delivered via CLI, Kubernetes operator, API, or CI integrations, with scoped access control and a complete audit log.

- Product: [snapenv.io](https://snapenv.io)
- Dashboard: [dash.snapenv.io](https://dash.snapenv.io)
- About: [snapenv.io/about](https://snapenv.io/about)
- Security: [snapenv.io/security](https://snapenv.io/security)
- AI agents: [snapenv.io/ai-agents](https://snapenv.io/ai-agents)

## What's in this repo

Built with [VitePress](https://vitepress.dev).

| Path | Contents |
|---|---|
| `guide/` | Getting started, CLI, permissions, variables, security, AI-agent skill guide |
| `api/` | REST API reference |
| `integrations/` | Kubernetes operator (incl. Helm), GitHub Actions, Docker, Vercel, Railway, Render, Dokploy, Coolify |
| `public/skill/` | Generated, installable AI-agent skill package (see `gen-skill.py`) |
| `public/llms.txt`, `public/llms-full.txt` | Machine-readable summaries of this documentation, for LLMs and AI crawlers |

## Development

```bash
npm install
npm run dev       # local dev server
npm run build     # static build
```

Two generator scripts keep machine-readable content in sync with the docs — run them after editing `guide/`, `api/`, or `integrations/` content, then commit the regenerated output:

```bash
python3 gen-llms.py    # rebuilds public/llms.txt and public/llms-full.txt
python3 gen-skill.py    # rebuilds public/skill/ (the AI-agent skill package)
```

## Contributing

Docs are plain Markdown under `guide/`, `api/`, and `integrations/`. Edit the relevant file and open a PR.

---

© SnapEnv
