# Authentication API

## POST /v1/auth/signup

Create an account and workspace.

```json
// request
{ "name": "Dana Whitfield", "email": "dana@acme.com", "password": "s3cr3t" }

// response 201
{ "token": "<jwt>", "user": { "id": "uuid", "name": "Dana Whitfield", "email": "dana@acme.com" } }
```

## POST /v1/auth/login

```json
// request
{ "email": "dana@acme.com", "password": "s3cr3t" }

// response — 2FA not enabled
{ "token": "<jwt>", "user": { ... } }

// response — 2FA enabled
{ "mfaRequired": true, "mfaToken": "<short-lived-jwt>" }
```

When `mfaRequired: true`, prompt for TOTP code and call `POST /v1/auth/verify-mfa`. The `mfaToken` expires in 5 minutes.

## POST /v1/auth/verify-mfa

```json
// request
{ "mfaToken": "<mfa-jwt>", "code": "123456" }

// response 200
{ "token": "<full-jwt>", "user": { ... } }
```

Accepts ±1 TOTP window (90 seconds total) and single-use backup codes.

## GET /v1/auth/session

Validate the stored JWT and return the current user. Called on every page load.

```json
{
  "user": {
    "id": "uuid",
    "name": "Dana Whitfield",
    "email": "dana@acme.com",
    "workspaceId": "uuid",
    "workspaceName": "Acme Corp",
    "wsRole": "Owner",
    "emailVerifiedAt": "2025-01-01T00:00:00Z"
  }
}
```

Returns 401 if the token is invalid, expired, or MFA-pending.

## POST /v1/auth/accept-invite

Accept a workspace invite. `token` is from the invite link.

```json
// request
{ "token": "a3f9b2..." }

// response 200
{ "token": "<jwt>", "workspaceId": "uuid", "workspaceName": "Acme Corp", "wsRole": "Member" }
```

## POST /v1/auth/switch-workspace

Issue a new JWT scoped to a different workspace the caller belongs to.

```json
// request
{ "workspaceId": "uuid" }
// response 200
{ "token": "<jwt>", "workspaceId": "uuid", "workspaceName": "Acme Corp" }
```
