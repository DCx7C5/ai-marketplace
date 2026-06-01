---
apply: off
instructions:
---
After creating a worktree:
1. Verify `git worktree list` includes the new path.
2. Verify path exists under `~/.copilot/session-state/<uuid>/wt<n>`.
3. Verify worktree HEAD is valid with `git -C <path> rev-parse --short HEAD`.
