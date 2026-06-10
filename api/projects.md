# Projects API

## GET /v1/projects

```json
{
  "projects": [
    { "id": "uuid", "name": "Backend API", "desc": "Core gateway", "color": "#3b82f6", "envs": ["dev","staging","prod"] }
  ]
}
```

## POST /v1/projects

```json
// request
{ "name": "Backend API", "desc": "optional", "color": "#3b82f6", "envs": ["staging","prod"] }
// response 201 — same shape as list item
```

## GET /v1/projects/:id

Same shape as a list item.

## PATCH /v1/projects/:id

```json
// request — all optional
{ "name": "New Name", "desc": "Updated", "color": "#8b5cf6" }
// response 200 — same shape
```

## DELETE /v1/projects/:id

Permanently deletes the project and all its variables, history, and audit logs. Owner only. Returns 204.

## POST /v1/projects/:id/envs

```json
// request
{ "name": "canary" }
// response 201 — updated project with new env in envs array
```

## DELETE /v1/projects/:id/envs/:env

Deletes the environment and all its variables. Returns 204.

## GET /v1/projects/:id/diff

Compare variables between two environments.

```
?env=prod&env=staging
```

```json
{
  "onlyInA": ["FEATURE_FLAG"],
  "onlyInB": ["LEGACY_KEY"],
  "different": ["DATABASE_URL", "REDIS_URL"]
}
```
