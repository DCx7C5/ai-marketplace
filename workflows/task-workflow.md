---
title: "Task workflow checklist"
event: "userPromptSubmitted"
matcher: "(?i).*(\\btask\\b|workflow 2|pre-task|post-task).*"
---
Apply **WORKFLOW 2 (finish TASK)** from `.plan/development-workflow.md`.

Required sequence:
1. **PRE-TASK**: verify all todos in `TASK_NAME` are `done` via SQL.
2. **ACTIVE**: deduplicate and verify touched dirs/files with ruff + basedpyright.
3. **POST-TASK**: update module markdown and `.plan/plan.md` task/phase snapshot; commit atomically.

If task completion also finishes the phase, immediately continue with phase workflow.
