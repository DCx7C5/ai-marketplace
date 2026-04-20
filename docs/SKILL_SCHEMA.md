# Skill Schema Reference

Every `SKILL.md` file must follow this structure:

```yaml
---
name: domain-subdomain-action
description: "What this skill does and when to invoke it."
domain: cybersecurity
model: sonnet
maxTurns: 20
mitre_attack:
  - T1234
nist_csf:
  - DE.CM-01
capec: []
---

# Skill Title

Skill body...

## Actions

...

## Output

...
```

## Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Path-derived name (see below) |
| `description` | string | ✅ | What this skill does, when to use it |
| `domain` | string | ✅ | One of: `cybersecurity`, `development`, `analysis`, `infrastructure` |
| `model` | string | ✅ | One of: `sonnet`, `haiku`, `opus` |
| `maxTurns` | integer | ✅ | 1–50 |
| `mitre_attack` | list | recommended | MITRE ATT&CK technique IDs (e.g., `T1059`) |
| `nist_csf` | list | recommended | NIST CSF control IDs (e.g., `DE.CM-01`) |
| `capec` | list | optional | CAPEC IDs |

## Name Derivation Rule

- **Skip** the top-level domain directory
- **Join** remaining path segments with `-`

### Examples

| Path | Name |
|------|------|
| `skills/deception/honeypot/SKILL.md` | `honeypot` |
| `skills/deception/canarytoken/SKILL.md` | `canarytoken` |
| `skills/mobile/android/apk/static-analysis/SKILL.md` | `android-apk-static-analysis` |
| `skills/steganography/image/png/lsb/detect/SKILL.md` | `image-png-lsb-detect` |
| `skills/vulnerabilities/cve/lookup/SKILL.md` | `cve-lookup` |

## Directory Taxonomy

```
skills/
└── <domain>/                    ← Top-level domain (skipped in name)
    └── <subdomain>/             ← Included in name
        └── <system>/            ← Included in name
            └── <action>/        ← Included in name (typically a verb)
                └── SKILL.md
```

## MITRE ATT&CK Reference

Use technique IDs from https://attack.mitre.org/. Sub-techniques use dot notation: `T1059.001`.

## NIST CSF 2.0 Reference

Format: `<Function>.<Category>-<Subcategory>` — e.g., `DE.CM-01`, `RS.MA-01`, `ID.AM-02`.

