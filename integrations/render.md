# Render

Like Railway, a Render web service is a long-running process — wrap its start command with [`snapenv run`](/guide/cli-run) instead of managing secrets through Render's own Environment tab.

## Set the bootstrap variables

In your Render service → **Environment**, add only these three:

```
SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
SNAPENV_PROJECT=4fac4b02-...
SNAPENV_ENV=prod
```

## Wrap your start command

Set the service's **Start Command** to:

```bash
curl -fsSL https://get.snapenv.io/install.sh | sh && export PATH="$HOME/.local/bin:$PATH" && snapenv run --all -- node dist/server.js
```

Render's build step still runs your normal build command (`npm run build`, etc.) — only the start command changes, so build-time behavior is untouched.

## Docker-based services

If your Render service deploys from a Dockerfile:

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
- Render restarts the service on deploy and on crash; `snapenv run` re-resolves variables each time the process starts, so a rotated secret is picked up on the next restart.
- Background workers and cron jobs on Render follow the same pattern — prefix whatever command Render would otherwise run with `snapenv run --all --`.
