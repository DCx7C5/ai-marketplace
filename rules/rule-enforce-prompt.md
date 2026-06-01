---
apply: off
instructions:
---
When `rule-enforce` is submitted, load `.github/workflows/rule-batching.md` and inject the `reassert-all batch` before any narrower workflow reruns so all previously applied rules for the active environment are restored, not just the current batch.
