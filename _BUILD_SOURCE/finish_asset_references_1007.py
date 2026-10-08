from pathlib import Path
from collections import defaultdict
import json,re
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=R/'_shots/asset_layout_1007'
journal=json.loads((O/'journal.json').read_text(encoding='utf-8'));mapping={q['old']:q['new'] for q in journal['moves']};groups=defaultdict(list)
for q in journal['moves']:
 p=Path(q['old']).parent
 while p.as_posix()!='assets/game':groups[p.as_posix()].append(q);p=p.parent
aliases={}
for old,rows in groups.items():
 values=set()
 for q in rows:
  suffix=Path(q['old']).relative_to(old).as_posix()
  if not q['new'].endswith('/'+suffix):break
  values.add(q['new'][:-len(suffix)])
 else:
  if len(values)==1:aliases[old+'/']=values.pop()
(R/'assets/data/asset_locations.json').write_text(json.dumps({**mapping,**aliases},indent=2)+'\n',encoding='utf-8')
pattern=re.compile('|'.join(re.escape(x) for x in sorted(aliases,key=len,reverse=True)))
changes=[]
for base in ['assets','tools','_BUILD_SOURCE']:
 for p in (R/base).rglob('*'):
  if not p.is_file() or p.suffix.lower() not in ['.js','.cjs','.py','.json','.html','.css','.ps1','.bat']:continue
  if p.name in ['asset_paths_1007.js','asset_locations.json','organize_assets_1007.py','patch_asset_loading_1007.py','finish_asset_references_1007.py','asset_catalog.json']:continue
  b=p.read_bytes()
  try:s=b.decode('utf-8')
  except UnicodeDecodeError:continue
  def replace(m):
   prefix=s[max(0,m.start()-90):m.start()]
   if 'UNUSED_ASSETS/' in prefix and not re.search(r'[\s"\x27]',prefix.split('UNUSED_ASSETS/')[-1]):return m.group(0)
   return aliases[m.group(0)]
  out=pattern.sub(replace,s)
  if out!=s:
   backup=O/'prefix_before'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b)
   p.write_bytes(out.encode('utf-8'));changes.append(p.relative_to(R).as_posix())
(O/'prefix_changes.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print('Updated',len(changes),'files;',len(aliases),'uniform directory aliases, preserving archived paths.')
