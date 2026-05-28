---
title: "Workflow failure recovery"
event: "postToolUseFailure"
matcher: "^(sql|bash|task)$"
---
A workflow-critical step failed.

Recovery rules:
1. Keep todo in a consistent state (`in_progress` only if actively owned).
2. If blocked by dependency/environment, set todo `blocked` with explicit reason.
3. Re-run only the failed verification step first (ruff/basedpyright/sql gate), then continue.
4. Never skip PRE/POST checklist gates after a failure.
