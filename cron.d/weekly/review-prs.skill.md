---
name: review-prs
schedule: "0 4 * * 1"
timeout: 600
retries: 1
idempotent: true
enabled: true
mode: agent
max_tokens: 2500
---
# Review pull requests

Summarize open pull requests, highlighting blockers and requested reviews.
