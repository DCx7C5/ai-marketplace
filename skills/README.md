# Skills

This directory contains **1,117+ AI skills** in a flat structure at the root level.

## Structure

All skills are now organized flatly under `skills/`:

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

The canonical list of all skills is in the root `index.json`:

```bash
# Find all skills in a category
jq '.skills[] | select(.path | startswith("cloud-"))' index.json

# Search by name or description
jq '.skills[] | select(.name | ascii_downcase | contains("bloodhound"))' index.json
```

### By directory listing

```bash
# List all cloud skills
ls skills/cloud-*

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

When adding new skills, place them directly under `skills/` using the flat naming convention above, and ensure they have valid YAML frontmatter.

After adding or modifying skills, run:

```bash
python3 scripts/generate_index.py
sha512sum index.json | cut -d' ' -f1 > index.json.sha512
./scripts/validate.sh
```

## Migration Note

This directory was migrated from a deep hierarchical structure (`category/subcategory/action/SKILL.md`) to the current flat layout in 2026. The old structure has been largely cleaned up, with skills now accessible directly by their flat names.
