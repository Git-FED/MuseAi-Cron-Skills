from datetime import datetime, timezone
from .loader import BUCKETS

def due(item, now=None):
    if not item.get('enabled', False): return False
    if item['bucket'] == 'runonce':
        try: return datetime.fromisoformat(item['run_at'].replace('Z','+00:00')) <= (now or datetime.now(timezone.utc))
        except ValueError: return False
    return True  # cron expression filtering is delegated to the host cron/install layer

def bucket_expression(config, bucket):
    defaults = config.get('buckets', {})
    return defaults.get(bucket)
