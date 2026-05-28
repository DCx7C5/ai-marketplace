---
priority: CRITICAL
name: "Avoid time sleep in async"
rule: "Do not use `time.sleep()` inside async code; it blocks the event loop and breaks concurrency."
---
