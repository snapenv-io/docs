# Coolify

Coolify deploys applications as long-running Docker containers, so it takes the same [`snapenv run`](/guide/cli-run) pattern as Railway, Render, and Dokploy — wrap the process instead of managing a secrets list in Coolify's own UI.

## Set the bootstrap variables

In your Coolify application → **Environment Variables**, add only these three:

```
SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
SNAPENV_PROJECT=4fac4b02-...
SNAPENV_ENV=prod
```

## Override the start command

If the image has `curl` available, set the start command in the application's general settings to install and run in one step:

```bash
curl -fsSL https://get.snapenv.io/install.sh | sh && export PATH="$HOME/.local/bin:$PATH" && snapenv run --all -- node dist/server.js
```

## Or install the CLI in your Dockerfile

```dockerfile
FROM ghcr.io/snapenv-io/cli:latest AS snapenv
FROM node:20-alpine
COPY --from=snapenv /usr/local/bin/snapenv /usr/local/bin/snapenv
WORKDIR /app
COPY . .
RUN npm ci
CMD ["snapenv", "run", "--all", "--", "node", "dist/server.js"]
```

## Notes

- The install script puts the binary in `~/.local/bin`, which isn't on `PATH` yet inside that same command — the `export PATH=...` between install and `snapenv run` is required, or you'll hit `snapenv: command not found`.
- Coolify is commonly self-hosted alongside SnapEnv itself — in that setup, secrets never leave infrastructure you control at any point in the pipeline.
- Redeploy after rotating a secret in the dashboard — `snapenv run` resolves values once, at process start, not continuously.
