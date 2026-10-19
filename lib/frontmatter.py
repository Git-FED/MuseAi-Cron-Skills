from pathlib import Path

class FrontmatterError(ValueError): pass

def _value(raw):
    raw = raw.strip()
    if not raw: return ""
    if raw.startswith(('"', "'")) and raw[-1:] == raw[0]: return raw[1:-1]
    if raw.lower() in ('true','false'): return raw.lower() == 'true'
    try: return int(raw)
    except ValueError: return raw

def parse(path):
    text = Path(path).read_text()
    if not text.startswith('---\n'): raise FrontmatterError('missing frontmatter opener')
    parts = text.split('\n---\n', 1)
    if len(parts) != 2: raise FrontmatterError('missing frontmatter closer')
    data = {}
    for line in parts[0][4:].splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        if ':' not in line: raise FrontmatterError(f'invalid frontmatter line: {line}')
        key, raw = line.split(':', 1)
        key = key.strip()
        if not key.replace('_','').isalnum(): raise FrontmatterError(f'invalid key: {key}')
        data[key] = _value(raw.split('#',1)[0])
    data['_body'] = parts[1].strip() + '\n'
    data['_path'] = str(path)
    return data
