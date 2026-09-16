# GitHub Actions

Inject SnapEnv secrets into any CI workflow step — no third-party action required.

## Setup

**1. Store your token as a GitHub secret:**

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**. Name it `SNAPENV_TOKEN`.

Optionally store your project ID as a variable: **Variables → New variable**, name it `SNAPENV_PROJECT`.

**2. Add workflow steps:**

```yaml
- name: Install snapenv
  run: |
    curl -fsSL https://get.snapenv.io/install.sh | sh
    echo "$HOME/.local/bin" >> "$GITHUB_PATH"

- name: Pull secrets
  env:
    SNAPENV_TOKEN: ${{ secrets.SNAPENV_TOKEN }}
    SNAPENV_PROJECT: ${{ vars.SNAPENV_PROJECT }}
    SNAPENV_ENV: prod
  run: snapenv pull --env prod
  # Variables are now in .env
```

The install script puts the binary in `~/.local/bin`, which isn't on `PATH` yet in the same step that installed it. Appending to `$GITHUB_PATH` — not a plain `export PATH=...` — is what makes it available to every later step in the job, since each `run:` step is a fresh shell.

## Export to GITHUB_ENV

When `GITHUB_ACTIONS=true`, `snapenv pull` automatically appends all variables to `$GITHUB_ENV` — making them available to all subsequent steps without sourcing a file. This assumes the **Install snapenv** step above already ran earlier in the job:

```yaml
- name: Pull secrets to environment
  env:
    SNAPENV_TOKEN: ${{ secrets.SNAPENV_TOKEN }}
    SNAPENV_PROJECT: ${{ vars.SNAPENV_PROJECT }}
    SNAPENV_ENV: prod
  run: snapenv pull --env prod

- name: Build
  run: |
    echo $DATABASE_URL   # available — SnapEnv wrote it to GITHUB_ENV
    npm run build
```

## Cache the CLI binary

To avoid downloading the CLI on every run, cache it:

```yaml
- name: Cache snapenv
  uses: actions/cache@v4
  with:
    path: ~/.local/bin/snapenv
    key: snapenv-${{ runner.os }}

- name: Install snapenv
  run: |
    if [ ! -x "$HOME/.local/bin/snapenv" ]; then
      curl -fsSL https://get.snapenv.io/install.sh | sh
    fi
    echo "$HOME/.local/bin" >> "$GITHUB_PATH"
```

`$GITHUB_PATH` still needs to be set every run, cache hit or not — only the download is skipped on a hit.

## Use a project-scoped token

Create an access token restricted to your specific project and the `production` environment only — this limits blast radius if the secret is ever exposed.
