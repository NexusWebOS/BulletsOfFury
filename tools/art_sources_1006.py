"""Resolve editable inputs through owned folders and the untouched unused archive.

Enumerate in the original logical order, so an asset move cannot renumber a reel.
Outputs use output_path; callers never need to restore old shipping folders.
"""
from pathlib import Path,PurePosixPath
import json
ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'UNUSED_ASSETS/cleanup_2026-10-06'
_TABLE=ROOT/'assets/data/asset_locations.json'
LOCATIONS=json.loads(_TABLE.read_text(encoding='utf-8')) if _TABLE.exists() else {}
REVERSE={v:k for k,v in LOCATIONS.items()}
PREFIXES=sorted((k for k in LOCATIONS if k.endswith('/')),key=len,reverse=True)
REVERSE_PREFIXES=sorted((k for k in REVERSE if k.endswith('/')),key=len,reverse=True)
_Base=type(Path())
def redirect(rel,table,prefixes):
 if rel in table:return table[rel]
 for prefix in prefixes:
  if rel+'/'==prefix:return table[prefix].rstrip('/')
  if rel.startswith(prefix):return table[prefix]+rel[len(prefix):]
 return rel
def logical(path):
 p=Path(path)
 try:return ROOT/p.relative_to(ARCHIVE)
 except ValueError:pass
 try:return ROOT/redirect(p.relative_to(ROOT).as_posix(),REVERSE,REVERSE_PREFIXES)
 except ValueError:return p
def output_path(path):
 p=logical(path)
 try:return ROOT/redirect(p.relative_to(ROOT).as_posix(),LOCATIONS,PREFIXES)
 except ValueError:return p
def alternate(path):
 p=logical(path)
 try:return ARCHIVE/p.relative_to(ROOT)
 except ValueError:return None
def source(path):
 p=logical(path);live=output_path(p)
 if live.exists():return live
 if p.exists():return p
 a=alternate(p)
 if a is not None and a.exists():return a
 raise FileNotFoundError(p)
def virtual_files(path):
 p=logical(path)
 try:pre=p.relative_to(ROOT).as_posix().rstrip('/')+'/'
 except ValueError:return []
 return [(k[len(pre):],ROOT/v) for k,v in LOCATIONS.items() if not k.endswith('/') and k.startswith(pre)]
class ArtSourcePath(_Base):
 def __lt__(self,other):return str(logical(self)).casefold()<str(logical(other)).casefold()
 def glob(self,pattern,**kwargs):
  p=logical(self);a=alternate(p);live=output_path(p);files={}
  for folder in [a,p,live]:
   if folder is None or not folder.exists():continue
   for item in Path(folder).glob(pattern,**kwargs):
    rel=logical(item).relative_to(p).as_posix();files[rel]=ArtSourcePath(item)
  for rel,item in virtual_files(p):
   if ('/' in pattern or '/' not in rel) and PurePosixPath(rel).match(pattern) and item.exists():files[rel]=ArtSourcePath(item)
  return iter(sorted(files.values()))
 def iterdir(self):
  p=logical(self);a=alternate(p);live=output_path(p);files={}
  for folder in [a,p,live]:
   if folder is None or not folder.exists():continue
   for item in Path(folder).iterdir():files[item.name]=ArtSourcePath(item)
  for rel,item in virtual_files(p):
   name=rel.split('/')[0]
   files[name]=ArtSourcePath(item if '/' not in rel else p/name)
  return iter(sorted(files.values()))
 def is_dir(self):
  p=logical(self);a=alternate(p)
  return Path(output_path(p)).is_dir() or (a is not None and a.is_dir()) or bool(virtual_files(p))
