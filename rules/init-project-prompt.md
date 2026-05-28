---
moment: "userPromptSubmitted"
matcher: "^/init-project$"
title: "Init project prompt rule"
rule: "When `/init-project` is submitted, load the dedicated prompt chain doc `.github/workflows/init-project-prompt-chain.md`; the hook injects the `init-project batch` before the claim/runtime/task steps and then loads the assigned init charts in order."
---
