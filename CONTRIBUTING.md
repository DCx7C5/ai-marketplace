# Contributing to AI Marketplace

Thank you for contributing! This marketplace grows through community contributions.

## Types of Contributions

### 1. New Agent

Add a Claude Code sub-agent to [`agents/`](agents/).

**File format** (`agents/your-agent-name.md`):

```markdown
name: your-agent-name
description: "One-line description for Claude Code's auto-routing. Include: capabilities, triggers, use cases."
model: sonnet
maxTurns: 20
tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Agent Title — Short Tagline

Detailed system prompt for the agent...

## Capabilities
...

## Output Format
...
```

**Rules:**
- `name` must match the filename (without `.md`)
- `description` must be < 200 chars (used for Claude Code routing)
- `model` must be one of: `sonnet`, `haiku`, `opus`
- `maxTurns` must be between 1–100
- System prompt must begin after `---` separator

### 2. New Skill

Add a CyberSecSuite skill to [`skills/`](skills/) following the hierarchical taxonomy.

**Path convention:** `skills/<domain>/<subdomain>/<...>/<action>/SKILL.md`

**File format** (`skills/domain/subdomain/action/SKILL.md`):

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

Detailed skill instructions...

## Actions
...

## Output
...
```

**Rules:**
- `name` must follow: skip the top-level domain dir, join remaining path segments with `-`
  - Example: `skills/deception/honeypot/SKILL.md` → `name: honeypot`
  - Example: `skills/mobile/android/apk/static-analysis/SKILL.md` → `name: android-apk-static-analysis`
- `domain` should be one of: `cybersecurity`, `development`, `analysis`, `infrastructure`
- MITRE ATT&CK IDs must be valid technique IDs (e.g., `T1059`, `T1059.001`)
- NIST CSF IDs must be valid (e.g., `DE.CM-01`, `RS.MA-01`)

## Validation

Before opening a PR, validate your contribution:

```bash
bash scripts/validate.sh
```

This checks:
- YAML frontmatter is valid
- Required fields are present
- `name` matches filename/path convention

## Pull Request Process

1. Fork the repository
2. Create a branch: `git checkout -b feat/add-your-agent-name`
3. Add your agent or skill file(s)
4. Run validation: `bash scripts/validate.sh`
5. Commit: `git commit -m "feat(agents): add your-agent-name"`
6. Push and open a PR against `main`

### PR Checklist

- [ ] File added to correct directory (`agents/` or `skills/`)
- [ ] YAML frontmatter is valid and complete
- [ ] `name` matches file/path convention
- [ ] `description` is clear and < 200 chars
- [ ] System prompt / skill body is meaningful (not a placeholder)
- [ ] `scripts/validate.sh` passes

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(agents): add steganography-analyst agent
feat(skills): add mobile/android/frida/hook skill
fix(agents): correct maxTurns in kernel-analyst
docs: update README agent table
```

## Code of Conduct

Be respectful. Security research content is welcome; weaponized exploits or malicious payloads are not.

