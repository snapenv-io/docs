# CLI Installation

The `snapenv` binary is a single static executable. No runtime required.

## Supported platforms

| Platform | Architecture |
|---|---|
| macOS | amd64, arm64 (Apple Silicon) |
| Linux | amd64, arm64 |

## Install

```bash
curl -fsSL https://snapenv.io/install.sh | sh
```

The install script detects your platform and architecture, downloads the correct binary to `~/.local/bin/snapenv`, and makes it executable.

### Manual download

```bash
# Linux amd64
curl -fsSL https://get.snapenv.io/cli/latest/snapenv-linux-amd64 \
  -o /usr/local/bin/snapenv && chmod +x /usr/local/bin/snapenv

# Linux arm64
curl -fsSL https://get.snapenv.io/cli/latest/snapenv-linux-arm64 \
  -o /usr/local/bin/snapenv && chmod +x /usr/local/bin/snapenv
```

## Configuration

Config is stored at `~/.config/snapenv/config.json` (chmod 600) and written by `snapenv login`.

```json
{
  "apiUrl": "https://api.snapenv.io",
  "token": "snp_live_...",
  "project": "4fac4b02-...",
  "env": "staging"
}
```

### Environment variable overrides

Environment variables always override the config file. Flags override environment variables.

| Variable | Description |
|---|---|
| `SNAPENV_TOKEN` | Access token |
| `SNAPENV_PROJECT` | Project UUID |
| `SNAPENV_ENV` | Environment name |
| `SNAPENV_OUTPUT` | Output file path (pull) |
| `SNAPENV_API_URL` | API base URL |

## Self-update

```bash
snapenv upgrade           # install latest version
snapenv upgrade --check   # check without installing
```

## Commands

| Command | Description |
|---|---|
| [`snapenv login`](/guide/cli#login) | Save credentials to config |
| [`snapenv pull`](/guide/cli-pull) | Pull variables to a file or stdout |
| [`snapenv push`](/guide/cli-push) | Push a local `.env` file to SnapEnv |
| [`snapenv diff`](/guide/cli-diff) | Compare local file to remote |
| [`snapenv projects`](/guide/cli-projects) | List all projects in the workspace |
| `snapenv upgrade` | Self-update the binary |
| `snapenv version` | Print version |

## login

```bash
snapenv login --token snp_live_...
snapenv login --token snp_live_... --api-url https://api.yourcompany.com
```

Writes credentials to `~/.config/snapenv/config.json`.
