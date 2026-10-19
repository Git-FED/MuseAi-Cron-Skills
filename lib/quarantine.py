from pathlib import Path
from datetime import datetime, timezone
import shutil

def quarantine(root, path, reason):
    root=Path(root); target=root/'cron.d'/'_invalid'/Path(path).name
    target.parent.mkdir(parents=True,exist_ok=True); shutil.move(str(path), str(target))
    target.with_name(target.name+'.REASON.txt').write_text(reason+'\n')

def archive(root, path):
    root=Path(root); target=root/'cron.d'/'_archive'/(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%S-')+Path(path).name)
    target.parent.mkdir(parents=True,exist_ok=True); shutil.move(str(path), str(target)); return target
