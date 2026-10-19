import os, time
from pathlib import Path

class SkillLock:
    def __init__(self, path): self.path=Path(path); self.fd=None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.fd=os.open(self.path, os.O_CREAT|os.O_EXCL|os.O_WRONLY, 0o600)
            os.write(self.fd, str(os.getpid()).encode()); return self
        except FileExistsError: raise RuntimeError('already running')
    def __exit__(self, *_):
        if self.fd is not None: os.close(self.fd)
        self.path.unlink(missing_ok=True)
