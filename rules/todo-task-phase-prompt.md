---
moment: "userPromptSubmitted"
matcher: "(?s).*todo-task-phase.*"
title: "Todo task phase prompt rule"
rule: "When `todo-task-phase` is submitted, load `.github/workflows/todo-task-phase-chain.md` so the `todo-task-phase batch` is injected before lifecycle state changes and the full todo -> task -> phase workflow from `.plan/development-workflow.md` is applied automatically."
---
