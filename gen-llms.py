#!/usr/bin/env python3
"""Build docs-site/public/llms-full.txt by concatenating all docs markdown.
Also copies the site llms.txt to public/. Run from docs-site/: python3 gen-llms.py
"""
import os, glob, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(ROOT, "public")
os.makedirs(PUBLIC, exist_ok=True)

BASE = "https://docs.snapenv.io"

# Deterministic, reader-friendly order.
ORDER = [
    "index.md",
    "guide/introduction.md", "guide/quick-start.md", "guide/ai-agents.md",
    "guide/variables.md", "guide/environments.md", "guide/encryption.md",
    "guide/permissions.md", "guide/team.md", "guide/tokens.md",
    "guide/authentication.md", "guide/2fa.md", "guide/audit.md",
    "guide/expiry.md", "guide/webhooks.md",
    "guide/cli.md", "guide/cli-pull.md", "guide/cli-run.md", "guide/cli-push.md",
    "guide/cli-diff.md", "guide/cli-projects.md",
    "integrations/overview.md", "integrations/kubernetes.md",
    "integrations/github-actions.md", "integrations/docker.md",
    "integrations/init-container.md",
    "api/overview.md", "api/authentication.md", "api/projects.md",
    "api/variables.md", "api/tokens.md", "api/workspace.md",
    "api/audit.md", "api/webhooks.md",
]

def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1:] if nl != -1 else ""
    return text

def url_for(rel):
    if rel == "index.md":
        return BASE + "/"
    return BASE + "/" + rel[:-3]  # drop .md

# Include any md not in ORDER (future-proof) at the end.
all_md = sorted(p for p in glob.glob("**/*.md", recursive=True)
                if "node_modules" not in p and ".vitepress" not in p)
seen = set(ORDER)
files = [f for f in ORDER if os.path.exists(os.path.join(ROOT, f))]
files += [f for f in all_md if f not in seen]

parts = [
    "# SnapEnv — Full Documentation",
    "",
    "> Secure environment variable & secrets manager for dev teams, CI/CD, and "
    "Kubernetes. Full documentation concatenated for language models. "
    "Canonical index: https://snapenv.io/llms.txt",
    "",
]

for rel in files:
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        body = strip_frontmatter(fh.read()).strip()
    parts.append("\n\n" + "=" * 78)
    parts.append(f"# Source: {url_for(rel)}")
    parts.append("=" * 78 + "\n")
    parts.append(body)

out = "\n".join(parts) + "\n"
with open(os.path.join(PUBLIC, "llms-full.txt"), "w", encoding="utf-8") as fh:
    fh.write(out)

# Copy the canonical index from the marketing site if present.
site_llms = os.path.abspath(os.path.join(ROOT, "..", "site", "static", "llms.txt"))
if os.path.exists(site_llms):
    shutil.copyfile(site_llms, os.path.join(PUBLIC, "llms.txt"))

print(f"llms-full.txt: {len(files)} docs, {len(out):,} bytes")
print("llms.txt: copied" if os.path.exists(site_llms) else "llms.txt: site source missing")
