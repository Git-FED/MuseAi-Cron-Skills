from pathlib import Path
from .frontmatter import parse, FrontmatterError
BUCKETS = ('secondly','minutely','hourly','daily','weekly','monthly','yearly','runonce')

def discover(root):
    root = Path(root); found=[]; errors=[]
    cron = root/'cron.d'
    for bucket in BUCKETS:
        directory = cron/bucket
        if not directory.exists(): continue
        for path in sorted(directory.glob('*.skill.md')):
            try:
                item = parse(path); validate(item, bucket); item['bucket']=bucket; found.append(item)
            except Exception as exc: errors.append((path, str(exc)))
    return found, errors

def validate(item, bucket):
    required = ['name','enabled','mode','timeout','retries']
    for key in required:
        if key not in item: raise ValueError(f'missing field: {key}')
    if item['mode'] not in ('agent','script'): raise ValueError('mode must be agent or script')
    if not isinstance(item['timeout'], int) or item['timeout'] <= 0: raise ValueError('timeout must be positive integer')
    if not isinstance(item['retries'], int) or item['retries'] < 0: raise ValueError('retries must be non-negative integer')
    if bucket == 'runonce' and not item.get('run_at'): raise ValueError('runonce requires run_at')
    if bucket != 'runonce' and not item.get('schedule'): raise ValueError('schedule is required outside runonce')
