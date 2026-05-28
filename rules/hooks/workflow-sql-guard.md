---
title: "SQL workflow guard"
event: "preToolUse"
matcher: "^sql$"
---
When using SQL for todo/task/phase workflows, enforce these gates:

1. Before implementation: query ready todos and claim one by setting `status='in_progress'` plus `primary_assigned_model` and `session_id`.
2. During implementation: heartbeat runtime row for active todo.
3. Before task completion: verify no remaining non-done rows for the task.
4. Before phase completion: verify phase has zero remaining non-done todos.
5. On todo exit: set `status='done'` (or `blocked`) and verify runtime row cleanup.

Never use non-existent tracker tables/columns (`tasks`, `completed_at`).
