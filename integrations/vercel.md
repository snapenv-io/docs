# Vercel

Pull secrets into the build — the only thing that ever touches Vercel's own environment variable store is your SnapEnv token.

Vercel builds are ephemeral and mostly framework-driven, so the integration point is the build step, not a long-running process: `snapenv pull` writes a local `.env` file just before your framework's build command reads it.

## Set the bootstrap variables

In your Vercel project → **Settings → Environment Variables**, add only these three — everything else stays in SnapEnv:

```
SNAPENV_TOKEN=snp_live_xxxxxxxxxxxx
SNAPENV_PROJECT=4fac4b02-...
SNAPENV_ENV=prod
```

Scope `SNAPENV_ENV` per Vercel environment (`prod` for Production, `staging` for Preview) so a preview deploy never pulls production secrets.

## Wire it into the build

Add a `vercel-build` script — Vercel runs this instead of `build` automatically if it exists:

```json
{
  "scripts": {
    "vercel-build": "curl -fsSL https://get.snapenv.io/install.sh | sh && snapenv pull --env $SNAPENV_ENV --output .env.production.local && next build"
  }
}
```

Next.js, Vite, and most frameworks auto-load `.env.production.local` (or `.env.local`) at build time — swap the filename for your framework's convention. `.env*.local` is gitignored by every standard framework starter, so nothing written here risks a commit.

## Override the build command instead

If you'd rather not touch `package.json`, set a custom **Build Command** in Vercel project settings:

```bash
curl -fsSL https://get.snapenv.io/install.sh | sh && snapenv pull --env prod --output .env.production.local && next build
```

## Notes

- Vercel Serverless/Edge Functions read `process.env` at request time from whatever Vercel baked in at build — there's no long-running process to wrap with `snapenv run` the way there is on Railway or Render.
- Rotate `SNAPENV_TOKEN` in the dashboard any time without touching Vercel — only that one token, not your actual secrets, lives in Vercel's project settings.
