---
name: heartbeat
schedule: "* * * * *"
timeout: 30
retries: 0
idempotent: true
enabled: true
mode: script
script: check.sh
hooks: none
---
# Heartbeat

Perform a lightweight health check and print one line.
