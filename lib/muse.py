import os, subprocess

def run_agent(item, root):
    prompt = item['_body']
    command = os.environ.get('MUSE_AGENT_COMMAND')
    if not command: return 'dry-run: agent command not configured'
    command = command.format(model=item.get('model','default'), max_tokens=item.get('max_tokens',2000), skill=item['name'])
    result = subprocess.run(command, input=prompt, text=True, shell=True, cwd=root, capture_output=True, timeout=item['timeout'])
    if result.returncode: raise RuntimeError(result.stderr.strip() or f'agent exited {result.returncode}')
    return result.stdout.strip() or 'agent completed'
