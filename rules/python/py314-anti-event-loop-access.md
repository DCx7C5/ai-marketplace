---
priority: CRITICAL
name: "Avoid direct event loop access"
rule: "Do not call `asyncio.get_event_loop()` or manage loops manually in code that can use `asyncio.run()` or `TaskGroup`."
---
