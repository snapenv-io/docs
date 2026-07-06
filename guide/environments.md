# Environments

Each project has one or more environments. Variables are scoped per environment — `DATABASE_URL` in `prod` is completely independent from `DATABASE_URL` in `staging`.

## Default environments

New projects are created with `dev`, `staging`, and `prod` by default.

## Protected environments

Environments can be marked **protected** to keep production secrets out of reach of every
developer by default. `prod` and `production` are protected automatically; you can protect
any environment (e.g. a prod-like `live` or `eu-prod`) with the 🔒 **Protect env** button in
the project toolbar — Owners only.

On a protected environment, members with the **Developer** project role get **no default
access** (they can't read or write its secrets) unless an Owner or Admin grants them an
explicit per-environment permission. Admins, Read-only members, and Owners are unaffected.
See [Permissions → Protected environments](/guide/permissions#protected-environments).

## Adding environments

Project → **Settings → Environments → Add**. Enter a name (e.g. `canary`, `eu-prod`, `qa`).

## Deleting environments

Project → **Settings → Environments → Delete**. This permanently deletes all variables in that environment. This action cannot be undone.

## Using environments in the CLI

```bash
snapenv pull --env prod
snapenv pull --env staging
snapenv pull --env canary
```

## Environment colors

Each environment has an associated color used throughout the dashboard UI (`prod` = red, `staging` = yellow, `dev` = green by default). You can customize colors per project.
