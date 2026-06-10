# Two-factor authentication (2FA)

SnapEnv supports TOTP-based 2FA (RFC 6238) compatible with any standard authenticator app.

## Enable 2FA

1. Go to **Settings → Security → Two-factor authentication**
2. Scan the QR code with your authenticator app (Google Authenticator, Authy, 1Password, etc.)
3. Enter the 6-digit code to confirm enrollment
4. Save the **backup codes** — you'll need them if you lose your authenticator

## Login flow with 2FA

1. Enter email + password as usual
2. Enter the 6-digit TOTP code from your authenticator
3. Accepted within ±1 TOTP window (±30 seconds)

## Backup codes

8 single-use backup codes are generated at enrollment. Each can only be used once. Store them somewhere safe (password manager, printed, etc.).

If you've used all backup codes and lost your authenticator device, contact support.

## Disable 2FA

**Settings → Security → Disable 2FA**. This requires your current TOTP code to confirm.
