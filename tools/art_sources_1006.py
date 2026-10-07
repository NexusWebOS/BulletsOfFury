"""Editable atlas sources may live outside the shipping assets tree.

Prefer live files over archived donors and keep their original logical sort order.
Only input enumeration is redirected; atlas outputs still write to assets/game.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'UNUSED_ASSETS/cleanup_2026-10-06'
_Base=type(Path())
def logical(path):
 p=Path(path)
 try:return ROOT/p.relative_to(ARCHIVE)
 except ValueError:return p
def alternate(path):
 p=logical(path)
 try:return ARCHIVE/p.relative_to(ROOT)
 except ValueError:return None
def source(path):
 p=logical(path)
 if p.exists():return p
 a=alternate(p)
 if a is not None and a.exists():return a
 raise FileNotFoundError(p)
class ArtSourcePath(_Base):
 def __lt__(self,other):return str(logical(self)).casefold()<str(logical(other)).casefold()
 def glob(self,pattern,**kwargs):
  p=logical(self);a=alternate(p);files={}
  for folder in [a,p]:
   if folder is None or not folder.exists():continue
   for item in Path(folder).glob(pattern,**kwargs):files[item.relative_to(folder).as_posix()]=ArtSourcePath(item)
  return iter(sorted(files.values()))
 def iterdir(self):
  p=logical(self);a=alternate(p);files={}
  for folder in [a,p]:
   if folder is None or not folder.exists():continue
   for item in Path(folder).iterdir():files[item.name]=ArtSourcePath(item)
  return iter(sorted(files.values()))
