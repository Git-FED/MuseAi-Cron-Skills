---
name: archive-year
schedule: "0 6 1 1 *"
timeout: 900
retries: 1
idempotent: true
enabled: true
mode: agent
max_tokens: 3000
---
# Archive year

Prepare the annual archive summary and verify required records are present.
