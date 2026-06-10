# Variable expiry

Set an expiry date on any variable to track when a credential needs to be rotated.

## Setting an expiry

Open a variable in the dashboard → click the expiry field → pick a date. Or via the API:

```bash
curl -X PUT https://api.snapenv.io/v1/projects/PROJECT_ID/envs/prod/vars/API_KEY \
  -H "Authorization: Bearer snp_live_..." \
  -H "Content-Type: application/json" \
  -d '{"expiresAt": "2026-12-31T00:00:00Z"}'
```

## Email reminders

When any variable in your workspace expires within **7 days**, SnapEnv sends an email to workspace Owners. Reminders are sent at most once per 24 hours per workspace.

## Clearing an expiry

In the dashboard, open the variable and clear the expiry date. Via the API:

```json
{ "clearExpiry": true }
```

## Viewing expiring variables

In the dashboard, variables with approaching expiry dates are highlighted in the variable list. Filter by expiry using the expiry indicator in the variable row.
