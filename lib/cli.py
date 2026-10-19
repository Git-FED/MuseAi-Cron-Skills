import argparse, json, shutil, sys
from pathlib import Path
from .loader import discover
from .executor import execute, record
from .scheduler import due
from .quarantine import archive

def config(root):
    data={'buckets':{}}
    p=Path(root)/'config.toml'
    if p.exists():
        for line in p.read_text().splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k,v=line.split('=',1); v=v.strip().strip('"');
                if k.strip() in ('timezone','default_model','mode'): data[k.strip()]=v
    return data

def main(argv=None):
    ap=argparse.ArgumentParser(prog='muse-cron'); ap.add_argument('--root', default=str(Path(__file__).resolve().parents[1])); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('validate'); sub.add_parser('list')
    run=sub.add_parser('run'); run.add_argument('--due',action='store_true'); run.add_argument('--name')
    ins=sub.add_parser('install'); ins.add_argument('--print',action='store_true')
    args=ap.parse_args(argv); root=Path(args.root); items, errors=discover(root)
    if args.cmd=='validate':
        for path,reason in errors: print(f'INVALID {path}: {reason}', file=sys.stderr)
        print(f'{len(items)} valid skill(s), {len(errors)} invalid skill(s)')
        return 1 if errors else 0
    if args.cmd=='list':
        for i in items: print(f"{i['bucket']:8} {i['name']:24} {i.get('schedule',i.get('run_at','-'))} [{i['mode']}] {'enabled' if i['enabled'] else 'disabled'}")
        return 0
    if args.cmd=='run':
        selected=[i for i in items if (not args.name or i['name']==args.name) and (not args.due or due(i))]
        for item in selected:
            try:
                status,out,dur=execute(item,root); record(root,item,status,out,dur); print(f"{item['name']}: {status} - {out}")
                if status=='success' and item['bucket']=='runonce' and item.get('on_success')=='archive': archive(root,item['_path'])
            except Exception as exc: print(f"{item['name']}: failed - {exc}",file=sys.stderr)
        return 0
    if args.cmd=='install':
        lines=[f"# muse-cron: {i['name']}\n{i.get('schedule')} cd {root} && ./bin/muse-cron run --name {i['name']}" for i in items if i['bucket']!='runonce']
        print('\n'.join(lines)); return 0
