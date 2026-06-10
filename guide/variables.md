# Variables

Variables are the core resource in SnapEnv. Each variable belongs to a project + environment combination.

## Types

| Type | Description |
|---|---|
| `secret` | Value is masked in the UI by default. Shown only with explicit reveal. |
| `plain` | Value is always visible. Use for non-sensitive config like feature flags or region names. |

## Adding variables

In the dashboard, open a project → select an environment → click **Add variable**. You can also bulk-import by pasting a `.env` file directly.

## Editing

Click any variable row to edit. Changes are saved immediately. Every change creates a history entry.

## Bulk operations

Select multiple variables using the checkbox column to:
- **Delete** — permanently removes selected keys from the environment
- **Change type** — toggle between `secret` and `plain` in one action

## Variable history

Every write (create, update, delete) is recorded. Click a variable → **History** to see all versions with timestamps and actors. Click **Restore** on any entry to roll back to that value.

## Expiry dates

Set an expiry date on a variable to track when a credential needs rotating. SnapEnv sends an email reminder when a secret is within 7 days of expiry.

See [Variable expiry](/guide/expiry) for details.

## Masked values

By default, values are shown as `•••••••`. Click the eye icon to reveal. Your preference (always show / always mask) is saved per account in Settings.

## Copying across environments

Use the dashboard's copy feature to duplicate a variable's value from one environment to another, or use the API to read from one env and write to another.
