"""Restore selected old builder inputs without losing their archive copy.

Example: python _BUILD_SOURCE/restore_art_source_1006.py --pattern
         "assets/game/stage3_enemy_damage/**" --copy
Defaults to listing matches. Never overwrites a newer file.
"""
import argparse,json,hashlib,fnmatch,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'UNUSED_ASSETS/cleanup_2026-10-06'
p=argparse.ArgumentParser();p.add_argument('--pattern',required=True);p.add_argument('--copy',action='store_true');args=p.parse_args()
j=json.loads((A/'archive-manifest.json').read_text());rows=[r for r in j['files'] if fnmatch.fnmatchcase(r['path'],args.pattern)]
for r in rows:
 src=(A/r['path']).resolve();dst=(R/r['path']).resolve()
 assert src.is_relative_to(A.resolve()) and dst.is_relative_to((R/'assets').resolve())
 assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256']
 if dst.exists():
  assert hashlib.sha256(dst.read_bytes()).hexdigest()==r['sha256'],f'Newer file will not be overwritten: {dst}'
 elif args.copy:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 print(r['path'])
print(f'{len(rows)} matching archived source files; '+('copied missing inputs.' if args.copy else 'listing only; use --copy to restore.'))
