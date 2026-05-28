---
priority: CRITICAL
name: "Avoid create_task fanout"
rule: "Do not scatter `asyncio.create_task()` calls without structured ownership, cancellation, and joining."
---
