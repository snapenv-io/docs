# Docker / Compose

Resolve secrets at container start — not at build time. Secrets never get baked into your image layers.

## Multi-stage Dockerfile

Copy the `snapenv` binary from the official image and pull at runtime:

```dockerfile
FROM ghcr.io/snapenv-io/cli:latest AS snapenv

FROM node:20-alpine
COPY --from=snapenv /usr/local/bin/snapenv /usr/local/bin/snapenv
WORKDIR /app
COPY . .
RUN npm ci

# Pull secrets at container start, then launch the app
CMD snapenv pull --env prod && node dist/server.js
```

Set `SNAPENV_TOKEN` and `SNAPENV_PROJECT` as environment variables when running the container:

```bash
docker run \
  -e SNAPENV_TOKEN=snp_live_... \
  -e SNAPENV_PROJECT=4fac4b02-... \
  my-app:latest
```

## Docker Compose with env_file

Generate `.env` before `compose up`:

```yaml
# compose.yml
services:
  app:
    build: .
    env_file: .env
```

```bash
# deploy script
snapenv pull --env prod && docker compose up -d
```

## Notes

- Never pass secrets as build arguments (`ARG`) — they appear in `docker history`
- Use `--stdout` to pipe directly without writing a file: `snapenv pull --env prod --stdout > .env`
- For Kubernetes, prefer the [operator](/integrations/kubernetes) over Docker-style patterns
