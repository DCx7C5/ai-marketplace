---
apply: off
instructions:
---
Apply **WORKFLOW 3 (finish PHASE)** from `.plan/development-workflow.md`.

Required sequence:
1. **PRE-PHASE**: SQL verification that all phase todos are done.
2. **ACTIVE**: run project impact/dependency checks, touched-scope ruff and basedpyright, run tests, run rubber-duck review pass.
3. **POST-PHASE**: update `.plan/plan.md`, `.plan/memory.md`, `.plan/checkpoints.md` and local owner docs; commit atomically.

Do not mark phase complete before all checklist items are finished.
