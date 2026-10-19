---
name: backup-notes
schedule: "0 3 * * *"
timeout: 300
retries: 2
idempotent: true
enabled: true
mode: script
script: run.sh
hooks: none
---
# Backup notes

Run the backup script and report a one-line summary. Failure means a non-zero exit.
