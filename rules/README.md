# Copilot Rule Markdown

Markdown rule files in this directory are loaded by
`~/.copilot/scripts/load_hook_rules.py` and injected as `additionalContext`
on session start.

## Categories

- Files are flat in this directory.
- Nested subdirectories are allowed for grouped rule sets.
- Filenames use a short `prefix-slug.md` format.
- Prefixes encode the original category:
  - `env-` — session and workspace setup rules
  - `plan-` — tracker and plan ownership rules
  - `code-` — runtime and coding discipline rules
  - `arch-` — structural and architecture rules
  - `wf-` — workflow and memory/checkpoint rules
  - `sev-` — importance and severity tiers
- Grouped subdirs currently include:
  - `plan/` — plan and tracker timing rules
  - `workflow/` — workflow execution rules

## Frontmatter keys

| Key | Description |
|---|---|
| `priority` | Required importance marker such as `CRITICAL`. |
| `name` | Required human-readable rule name. |
| `rule` | Required one-line rule text stored in frontmatter. |

## Priority policy

| Priority | Meaning |
|---|---|
| `CRITICAL` | Hard stop. Never break it. |
| `HIGH` | Strong default. Follow it whenever relevant, but it can yield to a CRITICAL rule or a real execution constraint. |

## Notes

- Keep the rule text in the `rule` frontmatter key.
- Keep flat rules limited to `priority`, `name`, and `rule`.
- `sessionStart` prepends rule, tool, and MCP inventories.
- Update `~/.copilot/scripts/load_hook_rules.py` when adding new rule roots.
