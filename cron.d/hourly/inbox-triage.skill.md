---
name: inbox-triage
schedule: "5 * * * *"
timeout: 180
retries: 1
idempotent: true
enabled: true
mode: agent
model: default
max_tokens: 1500
script: fetch.sh
hooks: before
---
# Inbox triage

Summarize the fetched inbox into **act now**, **waiting**, and **ignore**. Use no full quotes. Empty inbox should output `nothing`.
