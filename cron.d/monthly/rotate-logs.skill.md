---
name: rotate-logs
schedule: "0 5 1 * *"
timeout: 300
retries: 1
idempotent: true
enabled: true
mode: script
---
# Rotate logs

Retain logs according to config and report the number removed.
