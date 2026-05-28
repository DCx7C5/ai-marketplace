# Hook-Specific Rules

Markdown rule files in this directory are loaded by the hook-rule loader and
injected as `additionalContext` only when their frontmatter matches the
current hook event.

## Frontmatter keys

| Key | Description |
|---|---|
| `event` | Required hook event name such as `sessionStart` or `subagentStart`. |
| `matcher` | Optional regex matched against event payload fields for that hook. |
| `title` | Optional display title for the injected rule block. |

## Current files

- `session-start.md`
- `css-plan-start.md`
- `todo-workflow-prompt.md`
- `task-workflow-prompt.md`
- `phase-workflow-prompt.md`
- `workflow-sql-guard.md`
- `workflow-bash-guard.md`
- `workflow-failure-recovery.md`

## Notes

- Keep the body as the actual rule text.
- Use these files for hook-only behavior, not for file-path instructions.
- Rule loading is handled by `scripts/load_hook_rules.py` via `hooks/hooks.json`.
- Stateful workflow automation is handled by `scripts/workflow_automation.py`
  and persisted in `~/.copilot/workflow-state.json`.
