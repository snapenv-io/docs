#!/usr/bin/env python3
"""Build docs-site/public/skill/ — an installable Claude Code / AI-agent skill
package covering the SnapEnv CLI, Kubernetes operator, Helm integration, and
API. Reference files are generated from the same docs-site markdown that
gen-llms.py concatenates, so they stay in sync with the real docs instead of
drifting as a hand-maintained duplicate. SKILL.md itself is hand-authored
(skill-src/SKILL.md) and copied as-is — the entry point should stay curated,
not auto-concatenated.

Run from docs-site/: python3 gen-skill.py
"""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "skill-src")
OUT = os.path.join(ROOT, "public", "skill")
BASE = "https://docs.snapenv.io"

# Each reference file is a concatenation of these source docs, in order.
REFERENCES = {
    "cli.md": [
        "guide/cli.md", "guide/cli-pull.md", "guide/cli-run.md",
        "guide/cli-push.md", "guide/cli-diff.md", "guide/cli-projects.md",
    ],
    "operator.md": [
        "integrations/kubernetes.md",
    ],
    "api.md": [
        "api/overview.md", "api/authentication.md", "api/projects.md",
        "api/variables.md", "api/tokens.md", "api/workspace.md", "api/audit.md",
    ],
    "permissions.md": [
        "guide/authentication.md", "guide/tokens.md",
        "guide/permissions.md", "guide/team.md",
    ],
    "variables.md": [
        "guide/variables.md", "guide/variable-references.md",
        "guide/environments.md", "guide/expiry.md", "guide/encryption.md",
    ],
    "webhooks.md": [
        "guide/webhooks.md", "api/webhooks.md",
    ],
}


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1:] if nl != -1 else ""
    return text


def url_for(rel):
    return BASE + "/" + rel[:-3]


def build_reference(rel_paths):
    parts = []
    for rel in rel_paths:
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            body = strip_frontmatter(fh.read()).strip()
        parts.append("\n\n" + "=" * 78)
        parts.append(f"# Source: {url_for(rel)}")
        parts.append("=" * 78 + "\n")
        parts.append(body)
    return "\n".join(parts).strip() + "\n"


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "reference"))

    skill_md_src = os.path.join(SRC, "SKILL.md")
    if not os.path.exists(skill_md_src):
        raise SystemExit(f"missing {skill_md_src} — SKILL.md is hand-authored, not generated")
    shutil.copyfile(skill_md_src, os.path.join(OUT, "SKILL.md"))

    total_bytes = os.path.getsize(skill_md_src)
    for name, sources in REFERENCES.items():
        out_path = os.path.join(OUT, "reference", name)
        content = build_reference(sources)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(content)
        total_bytes += len(content)
        print(f"  reference/{name:16s} {len(sources)} source doc(s), {len(content):,} bytes")

    print(f"skill/: {len(REFERENCES) + 1} files, {total_bytes:,} bytes total")


if __name__ == "__main__":
    main()
