# Skills

This directory contains **1,117+ AI skills** organized as a recursive catalog tree.

## Structure

All skills are organized under `skills/`, with each directory exposing its own `index.json`:

```
skills/
├── linux-foo-bar/           # Example: Linux-related skill
│   └── SKILL.md
├── cloud-aws-iam/           # Example: Cloud security skill
│   └── SKILL.md
├── webapp-auth-oauth/       # Example: Web application security skill
│   └── SKILL.md
├── offensive-initial-access/
│   └── SKILL.md
└── ...
```

### Naming Convention

Each skill directory follows the pattern:

```
<category>-<name>/
└── SKILL.md
```

Common root prefixes include:
- `linux-`, `windows-`, `cloud-`, `webapp-`, `net-`
- `offensive-`, `vuln-`, `malware-`, `soc-`, `intel-`
- `browser-`, `email-`, `crypto-`, `compliance-`
- `identity-`, `ics-`, `db-`, `stego-`, and others

## Finding Skills

### Via index.json (recommended)

The canonical catalog starts at the root `index.json`, which points to `skills/index.json` and then to per-directory indexes:

```bash
# Inspect the top-level skill tree
jq '.skills[]' index.json

# Inspect a directory-local catalog
jq '.skills[]' skills/browser/index.json
```

### By directory listing

```bash
# List all top-level skill directories
ls skills/

# List all offensive skills
ls skills/offensive-*
```

## Skill Format

Each skill directory contains a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: cloud-aws-iam
description: ...
domain: cybersecurity
subdomain: ...
tags: [...]
model: sonnet
maxTurns: 20
---
```

## Contributing

When adding new skills, place them in the appropriate directory under `skills/` and ensure the directory has a valid `SKILL.md` and generated `index.json`.

After adding or modifying skills, run:

```bash
python3 scripts/generate_index.py
sha512sum index.json | cut -d' ' -f1 > index.json.sha512
./scripts/validate.sh
```

## Migration Note

This directory was migrated from a flat layout to a recursive tree in 2026 so each subdirectory can carry its own catalog index.
