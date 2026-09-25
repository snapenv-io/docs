# AI agents

SnapEnv ships an installable skill for Claude Code (and any other AI agent that reads a project's `.claude/skills/` directory) — the CLI, the Kubernetes operator, Helm chart integration, and the API, all in one package, so you don't have to paste docs into the chat every time.

## Install

Run this in your project — it installs the skill to `.claude/skills/snapenv/`:

```bash
curl -fsSL https://get.snapenv.io/skill.sh | sh
```

Or, if you're already talking to an agent, paste this instead and let it run the command for you:

> Install the SnapEnv skill by running `curl -fsSL https://get.snapenv.io/skill.sh | sh`, then use it whenever this task involves SnapEnv, environment variables, or secrets.

By default it installs into the current project (`.claude/skills/snapenv/`). To install it once for every project instead:

```bash
SNAPENV_SKILL_DIR=~/.claude/skills/snapenv curl -fsSL https://get.snapenv.io/skill.sh | sh
```

## What it covers

- **CLI** — `pull`, `push`, `run`, `diff`, `projects`, flags, exit codes, CI/GitHub Actions and non-interactive-mode patterns
- **Kubernetes operator** — the `SnapEnvSecret` CRD, install/upgrade, auto-restart on variable change
- **Helm** — wiring SnapEnv into your own chart's `values.yaml` and templates
- **API** — direct HTTP access for tooling that isn't the CLI or operator
- **Permissions** — access-token scopes, the workspace/project/environment role model
- **Variables & webhooks** — variable references, expiry, encryption, and change notifications

It's generated from this documentation site, so it stays in sync with what you're reading here — see [SKILL.md](https://docs.snapenv.io/skill/SKILL.md) directly if you want to see exactly what the agent gets. It links out to each reference file (`reference/cli.md`, `reference/operator.md`, etc.) in turn.

## Why `snapenv run` for agents specifically

If you're having an agent run or test something that needs secrets, point it at `snapenv run` rather than `snapenv pull` — the skill tells it this, but it's worth knowing yourself too. `run` injects variables into the child process (or as `{{VAR}}` placeholders in its own arguments) without ever writing them to disk or printing them, and scrubs any exposed value from the command's output as it streams. That means a secret an agent is using never actually passes through anything it wrote to a file, or through its own chat transcript. See [`snapenv run`](/guide/cli-run) for the full behavior.
