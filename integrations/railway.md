# Railway

Railway runs your service as a long-lived process, so you can skip the "write a .env file" step entirely and inject secrets straight into the running process with [`snapenv run`](/guide/cli-run) — they never touch disk or Railway's own Variables store.

## Set the bootstrap variables

In your Railway service → **Variables**, add only these three:

```
SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
SNAPENV_PROJECT=4fac4b02-...
SNAPENV_ENV=prod
```

## Wrap your start command

Set a **Custom Start Command** that installs the CLI once and runs your process through it:

```bash
curl -fsSL https://get.snapenv.io/install.sh | sh && export PATH="$HOME/.local/bin:$PATH" && snapenv run --all -- node dist/server.js
```

`snapenv run` pulls the current variable set for `SNAPENV_ENV`, injects it into the child process's real environment, and exits with the same code your app exits with — Railway's restart/crash detection works unchanged.

## Or bake it into the image

If you deploy via Dockerfile instead of Railway's buildpacks:

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
- `--all` scopes every variable in `SNAPENV_ENV` into the process; use `--only DATABASE_URL,STRIPE_KEY` to inject a narrower set.
- A rotation in the dashboard takes effect on the next deploy/restart — `snapenv run` resolves values at process start, not continuously.
