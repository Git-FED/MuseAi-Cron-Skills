# Scheduling

| Bucket | Default expression | Notes |
|---|---|---|
| secondly | `* * * * * *` | disabled unless explicitly supported by host |
| minutely | `* * * * *` | lock-skips overlapping runs |
| hourly | `5 * * * *` | off-minute default |
| daily | `0 3 * * *` | UTC by default |
| weekly | `0 4 * * 1` | Monday |
| monthly | `0 5 1 * *` | first day |
| yearly | `0 6 1 1 *` | January 1 |
| runonce | — | driven by `run_at`, archives on success |

`muse-cron install` prints host crontab lines. It does not modify a user's crontab automatically.
