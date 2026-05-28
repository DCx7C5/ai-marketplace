---
title: "Todo workflow entrypoint"
event: "userPromptSubmitted"
matcher: "(?i).*(\\btodo\\b|workflow 1|pre-todo|post-todo).*"
---
Apply **WORKFLOW 1 (single TODO)** from `.plan/development-workflow.md` using strict PRE → ACTIVE → POST order.

Required checklist:
1. **PRE-TODO**: run SQL claim flow (including in-progress leftover check), then enter runtime lifecycle by setting `status='in_progress'` + `primary_assigned_model` + `session_id`.
2. **ACTIVE**: keep runtime heartbeat current, implement only touched scope, run ruff and basedpyright gates, then run dependency analyzer checks.
3. **POST-TODO**: update local planning markdown, refresh phase snapshot query, set todo `done`, verify runtime row cleanup, and commit atomically.

Do not skip any PRE/ACTIVE/POST gate. Use the dedicated `todo-pre`, `todo-active`, and `todo-post` hook rules for exact steps.
