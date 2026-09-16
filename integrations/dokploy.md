# Dokploy

Dokploy deploys your service as a long-running Docker container, so the same [`snapenv run`](/guide/cli-run) pattern used for Railway and Render applies directly — set it as the container's command.

## Set the bootstrap variables

In your Dokploy application → **Environment**, add only these three:

```
SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
SNAPENV_PROJECT=4fac4b02-...
SNAPENV_ENV=prod
```

## Override the container command

If the image has `curl` available, set the command in the application's Docker settings to install and run in one step:

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
- Because Dokploy is self-hosted, `SNAPENV_TOKEN` is the only credential that needs to leave your infrastructure at all if you're also self-hosting the SnapEnv API.
- Redeploy (or restart) the application after rotating a secret in the dashboard — `snapenv run` resolves values once, at process start.
