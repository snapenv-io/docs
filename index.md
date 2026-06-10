---
layout: home

hero:
  name: SnapEnv
  text: Secure environment variables for dev teams
  tagline: Encrypted at rest, pulled anywhere — CLI, Kubernetes, GitHub Actions, Docker.
  actions:
    - theme: brand
      text: Get started
      link: /guide/quick-start
    - theme: alt
      text: CLI reference
      link: /guide/cli
    - theme: alt
      text: API reference
      link: /api/overview

features:
  - icon: 🔐
    title: AES-256-GCM encryption
    details: Every variable is encrypted before any database write. Each project has a unique derived key — a breach of one project exposes nothing else.
  - icon: 🚀
    title: Pull anywhere
    details: CLI, Kubernetes operator, GitHub Actions, Docker, init containers. One access token, every environment.
  - icon: 👥
    title: Team access control
    details: Workspace roles, project roles, and per-environment permissions. Every action is in the append-only audit log.
  - icon: 🔄
    title: Variable history
    details: Every change is versioned. View old values and restore any variable to a previous state in one click.
  - icon: 🔔
    title: Webhooks & expiry
    details: Trigger deploys when variables change. Set expiry dates on credentials so rotation never gets missed.
  - icon: ☸️
    title: Kubernetes native
    details: The SnapEnv operator auto-syncs variables into native Kubernetes Secrets — no init containers or custom scripts.
---
