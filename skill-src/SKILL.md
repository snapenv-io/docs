---
name: snapenv
description: Manage encrypted environment variables and secrets with SnapEnv — CLI (pull/push/run/diff), the Kubernetes operator (SnapEnvSecret CRD), Helm chart integration, and the REST API. Use this skill whenever a task involves .env files, environment variable or secrets management, injecting credentials into a running command, syncing secrets into Kubernetes, or a repo that already uses the snapenv CLI, SNAPENV_* environment variables, or a snp_live_ access token.
---

# SnapEnv

SnapEnv is a secure environment-variable manager: encrypted storage per project/environment, a CLI, a Kubernetes operator, and a REST API. This skill covers driving all of them on a user's behalf.

## Quick reference

```bash
snapenv login --token snp_live_...        # one-time, or set SNAPENV_TOKEN
snapenv pull --env prod                   # write variables to ./.env
snapenv pull --env prod --stdout          # print instead of writing a file
snapenv push --env dev                    # upload a local .env (additive — never deletes remote keys)
snapenv diff --env prod                   # compare local .env to remote, exit 1 on drift
snapenv projects                          # list projects + their UUID (needed for --project)
snapenv run --env prod --only DATABASE_URL -- node server.js   # inject without touching disk
```

Non-interactive/CI mode: set `SNAPENV_TOKEN`, `SNAPENV_PROJECT`, `SNAPENV_ENV` and every command above runs without a config file or login step.

## Ground rules for this skill

- **Prefer `snapenv run` over `snapenv pull` whenever you're about to execute or test something.** `run` injects variables into the child process (or as `{{VAR}}` placeholders in its arguments) without ever writing them to a file or printing them — and it scrubs any exposed value from the command's own stdout/stderr as it streams. `pull` writes real plaintext to `.env`; only use it when the user's workflow genuinely needs a file on disk (e.g. a framework that only reads `.env` at boot).
- **Never echo, log, or repeat a secret value back to the user** unless they explicitly ask to see it decrypted. Pulling into `.env` or injecting via `run` is enough — don't `cat .env` afterward to "confirm" it worked.
- **`run` requires an explicit scope** (`--only KEY1,KEY2` or `--all`, optionally with `--except`). There's no default — pick the narrowest scope the task actually needs, not `--all` out of convenience.
- **Don't invent variable names.** If you reference a `{{KEY}}` placeholder or a key in `--only` that doesn't exist in the environment, `run` fails loudly before the command starts — that's intentional, treat it as a signal to run `snapenv diff` or check the dashboard rather than guessing.
- **`push` is additive, never destructive** — keys missing from the local file are left alone remotely. Deleting a key requires the dashboard or a direct `DELETE` API call; don't assume `push` can do it.
- A project UUID is required for most commands (`--project`, or `$SNAPENV_PROJECT`). Get it from `snapenv projects` or the dashboard URL (`dash.snapenv.io/projects/<uuid>`).

## When to reach for each reference file

Load these only as needed — don't read all of them up front.

- **CLI** — every command, flag, exit code, GitHub Actions and non-interactive/CI patterns → [reference/cli.md](reference/cli.md)
- **Kubernetes operator & Helm** — the `SnapEnvSecret` CRD, installing the operator, auto-restart-on-change, and wiring SnapEnv into a Helm chart's own `values.yaml`/templates → [reference/operator.md](reference/operator.md)
- **REST API** — direct HTTP access when there's no CLI/operator in the picture (custom tooling, another language) → [reference/api.md](reference/api.md)
- **Access & permissions** — access-token scopes, the workspace/project/environment role model, who can read/write which environment → [reference/permissions.md](reference/permissions.md)
- **Variables** — variable references (composing one variable from another), expiry, environments, how encryption works → [reference/variables.md](reference/variables.md)
- **Webhooks** — notifying Slack or an HTTP endpoint when variables change → [reference/webhooks.md](reference/webhooks.md)

## Typical tasks

**"Set up SnapEnv for this project"** — check for an existing `~/.config/snapenv/config.json` or `SNAPENV_*` env vars first; if absent, ask the user for an access token (dashboard → Settings → Access tokens) rather than generating or guessing one. Then `snapenv projects` to find/confirm the project UUID.

**"Run the tests/dev server with prod-like secrets"** — use `snapenv run --env <env> --only <the specific keys needed> -- <command>`, not `pull`. Ask the user which keys before defaulting to `--all`.

**"Deploy this to Kubernetes"** — see [reference/operator.md](reference/operator.md). If the target already uses a Helm chart, wire SnapEnv in as chart values/templates (documented there) rather than hand-applying a one-off `SnapEnvSecret` YAML outside the chart's lifecycle.

**"Why doesn't my local .env match prod"** — `snapenv diff --env <env>`, not a manual pull-and-compare.

**"Add a new required secret across all environments"** — this touches real, live secrets; confirm the exact key name and which environments with the user before writing anything, the same as any other irreversible/shared-state action.
