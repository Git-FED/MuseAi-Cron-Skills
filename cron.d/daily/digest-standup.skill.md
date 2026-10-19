---
name: digest-standup
schedule: "30 8 * * 1-5"
timeout: 120
retries: 1
idempotent: true
enabled: true
mode: agent
max_tokens: 1200
---
# Standup digest

Produce a concise standup digest from the configured Muse sources.
