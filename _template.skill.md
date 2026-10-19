---
name: example-skill
schedule: "0 3 * * *"
timeout: 300
retries: 2
idempotent: true
enabled: true
mode: agent
model: default
max_tokens: 2000
prompt: prompt.md
script: run.sh
hooks: none
on_success: archive
---
# Example skill

Describe the task and its expected output. Keep instructions deterministic and safe to retry.
