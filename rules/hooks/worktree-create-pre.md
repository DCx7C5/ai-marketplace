---
title: "Worktree create pre-hook"
event: "preToolUse"
matcher: "(?is).*\\bgit\\b.*\\bworktree\\s+add\\b.*"
---
Before creating a worktree:
1. Use path `~/.copilot/session-state/<uuid>/wt<n>`.
2. Ensure `<n>` is the next free number for the active session UUID.
3. Prefer detached HEAD unless a branch is explicitly required.
