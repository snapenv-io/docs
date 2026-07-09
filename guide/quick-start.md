# Quick start

Get from zero to `snapenv pull` in under 5 minutes.

## 1. Create an account

Sign up at [dash.snapenv.io](https://dash.snapenv.io/signup). A workspace is created automatically.

## 2. Create a project

Click **New project** in the dashboard. Give it a name and choose which environments you need (`dev`, `staging`, `prod` are created by default).

## 3. Add variables

Open the project → select an environment → click **Add variable**. Or paste a `.env` file directly into the bulk import area.

## 4. Create an access token

Go to **Settings → Access tokens → New token**. Choose:
- **Scope** — `read` for pulling only, `write` for push too
- **Environments** — restrict which envs the token can access
- **Project** — leave blank for workspace-wide, or pin to one project

Copy the token — it's shown once.

## 5. Install the CLI

```bash
curl -fsSL https://get.snapenv.io/install.sh | sh
```

## 6. Authenticate

```bash
snapenv login --token snp_live_xxxxxxxxxxxx
```

## 7. Pull your secrets

```bash
snapenv pull --env prod
# ✓ 14 variables written to .env
```

That's it. Your `.env` file is populated and ready.

## What's next?

- Set up [GitHub Actions](/integrations/github-actions) to pull secrets in CI
- Deploy the [Kubernetes Operator](/integrations/kubernetes) for automatic sync
- Review the [permission model](/guide/permissions) for your team
