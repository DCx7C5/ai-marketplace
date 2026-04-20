# Agent Schema Reference

Every file in `agents/` must follow this structure:

```
name: agent-name
description: "Short routing description < 200 chars"
model: sonnet
maxTurns: 20
tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Agent Title — Tagline

System prompt body...
```

## Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Must match filename (without `.md`) |
| `description` | string | ✅ | Claude Code uses this for auto-routing. Keep under 200 chars. |
| `model` | string | ✅ | One of: `sonnet`, `haiku`, `opus` |
| `maxTurns` | integer | ✅ | 1–100. How many turns before the agent stops. |
| `tools` | list | ✅ | Claude Code tool names the agent may use |

## Available Tools

```
Read, Write, Edit, MultiEdit, Bash, Glob, Grep, LS,
WebFetch, WebSearch, TodoRead, TodoWrite, Task
```

## Naming Convention

- File: `agents/kebab-case-name.md`
- `name:` field must exactly match filename

## Description Tips

The `description` field is used by Claude Code to decide **when** to invoke the agent. Write it to answer:
- What does this agent specialize in?
- What are concrete trigger examples?

**Good:** `"CVE lookup, IOC analysis, MITRE ATT&CK mapping. Triggers: CVE-YYYY-NNNNN, IOC discovery."`

**Bad:** `"A helpful security agent."`

