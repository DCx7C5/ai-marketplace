---
moment: "userPromptSubmitted"
matcher: "^/resume-or-start-working$"
title: "Resume or start working prompt rule"
rule: "When `/resume-or-start-working` is submitted, load `.github/workflows/resume-or-start-working-chain.md` so the `resume-or-start-working batch` is injected before runtime lookup and the worker then checks for its own runtime entry or starts a new claim."
---
