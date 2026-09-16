# snapenv run

Runs a command with variables injected — never written to a `.env` file, and never appearing in anything you (or an AI coding agent driving the CLI on your behalf) actually wrote.

## Usage

```bash
snapenv run --env prod --only DATABASE_URL -- node server.js
snapenv run --env prod --all -- npm start
snapenv run --env prod --only API_TOKEN -- curl -H "Authorization: Bearer {{API_TOKEN}}" https://api.example.com
snapenv run --env staging --all --except DATABASE_URL -- ./migrate.sh
```

The `--` separator is required — everything after it is the command to run, untouched by `snapenv run`'s own flag parsing.

## Flags

| Flag | Default | Description |
|---|---|---|
| `--env` | `$SNAPENV_ENV` | Environment to pull from |
| `--project` | `$SNAPENV_PROJECT` | Project UUID |
| `--only` | — | Comma-separated keys to expose (mutually exclusive with `--all`) |
| `--all` | — | Expose every variable in the environment |
| `--except` | — | Comma-separated keys to exclude — only valid with `--all` |

There's no default scope — running without `--only` or `--all` is a hard error. That's deliberate: a command that's supposed to see one database URL shouldn't silently gain access to every secret in the environment because a flag was forgotten.

## Two ways to receive a value

**As a real environment variable** in the child process — the common case. Any program that reads `process.env` / `os.Getenv` / etc. just works, no code changes:

```bash
snapenv run --env prod --only DATABASE_URL -- node server.js
# server.js reads process.env.DATABASE_URL normally
```

**As a `{{VAR_NAME}}` placeholder** inside the command's own arguments, resolved immediately before exec — for tools like `curl` where the value has to be a literal argument, not something read from the environment:

```bash
snapenv run --only API_TOKEN -- curl -H "Authorization: Bearer {{API_TOKEN}}" https://api.example.com
```

A placeholder referencing a key outside the current scope is an error, and the command never starts — this is what stops a typo (or an over-eager AI agent guessing at a variable name) from silently passing the literal string `{{FOO}}` through instead of failing loudly.

## Output scrubbing

Anything the command prints — stdout or stderr — is scanned as it streams, and any occurrence of an exposed value is replaced with `***` before you (or an agent watching the command's output) ever see it. This is what protects against a secret leaking back out through a side channel the command wasn't asked to use: a verbose `--debug` flag, an accidental `console.log`, a stack trace on crash.

Values shorter than 6 characters are never scrubbed — a `PORT` of `3000` or a `LOG_LEVEL` of `debug` would otherwise collide with completely unrelated output far more often than they'd ever protect anything.

Scrubbing works correctly even when a value is split across two separate writes to the command's output (e.g. a slow process flushing one byte at a time) — the buffering that makes this reliable trades a small amount of latency (at most one secret's length) for correctness, so still effectively real-time for normal output volumes.

## What this is not

`snapenv run` is not a sandbox. It reduces the chance of an honest mistake — a verbose log, a careless `echo $DATABASE_URL`, a crash that dumps the environment — not a guarantee against a program that's deliberately trying to exfiltrate its own environment. If you don't trust the command, `snapenv run` isn't what makes it trustworthy.

## Exit codes

The command's own exit code is passed straight through — `snapenv run` exits with whatever the process it ran exited with. A scope/validation error (bad flags, an out-of-scope placeholder, missing `--`) exits `1` before the command ever starts.
