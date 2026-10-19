import json, time, subprocess
from pathlib import Path
from .lock import SkillLock
from .muse import run_agent

def execute(item, root):
    root=Path(root); lock=root/'run'/'locks'/(item['name']+'.lock')
    started=time.time(); attempts=item['retries']+1; output=''
    try:
        with SkillLock(lock):
            for attempt in range(attempts):
                try:
                    if item.get('mode') == 'script':
                        script=item.get('script')
                        if not script: output='script mode with no script; nothing to run'
                        else:
                            skill_file=Path(item['_path'])
                            sibling_dir=skill_file.parent/skill_file.name.removesuffix('.skill.md')
                            script_path=(sibling_dir/script) if (sibling_dir/script).exists() else (skill_file.parent/script)
                            r=subprocess.run([str(script_path)], cwd=script_path.parent, text=True, capture_output=True, timeout=item['timeout'])
                            if r.returncode: raise RuntimeError(r.stderr.strip() or f'script exited {r.returncode}')
                            output=r.stdout.strip() or 'script completed'
                    else: output=run_agent(item, root)
                    status='success'; break
                except Exception as exc:
                    status='failed'; output=str(exc)
                    if attempt+1 == attempts: raise
            return status, output, int((time.time()-started)*1000)
    except RuntimeError as exc:
        if str(exc) == 'already running': return 'skipped', str(exc), 0
        raise

def record(root, item, status, output, duration):
    root=Path(root); state=root/'state'/'last_run.json'; state.parent.mkdir(exist_ok=True)
    try: data=json.loads(state.read_text())
    except (FileNotFoundError, json.JSONDecodeError): data={}
    data[item['name']]={'ts':time.time(),'status':status,'duration_ms':duration,'output':output}
    state.write_text(json.dumps(data, indent=2)+'\n')
    log=root/'logs'/item['name']/(time.strftime('%Y-%m')+'.log'); log.parent.mkdir(parents=True,exist_ok=True)
    with log.open('a') as fh: fh.write(f'{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} {status} {duration}ms {output}\n')
