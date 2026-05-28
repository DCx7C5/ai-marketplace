---
title: "Bash workflow guard"
event: "preToolUse"
matcher: "^bash$"
---
For todo/task/phase execution via bash:

1. Run dependency analyzer before and after meaningful code edits.
2. Run `ruff` on touched scope (`--fix` then clean pass).
3. Run `basedpyright` on touched files or smallest touched directory.
4. For phase completion, run tests before finalizing.

Keep command scope tight to touched paths unless phase-level checks are explicitly required.
