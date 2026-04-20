---
name: New Agent
about: Submit a new Claude Code sub-agent
title: "[Agent] your-agent-name"
labels: ["agent", "new-content"]
assignees: []
---

## Agent Name

<!-- Must match the filename: `agents/your-agent-name.md` -->

## Description

<!-- One-line description (< 200 chars) used for Claude Code auto-routing -->

## Model

- [ ] `sonnet`
- [ ] `haiku`
- [ ] `opus`

## Domain / Category

<!-- e.g., Security & Forensics, Development, Network, UI/Infrastructure -->

## Checklist

- [ ] Frontmatter is valid YAML (`name`, `description`, `model`, `maxTurns`, `tools`)
- [ ] `name` matches filename (without `.md`)
- [ ] System prompt body is meaningful (not a placeholder)
- [ ] `scripts/validate.sh` passes locally
- [ ] PR includes the `.md` file in `agents/`

