"""Rebuild accepted PixelLab Hammer frames from preserved local sources.
No generation, per-frame fitting, palette edits or network access.
"""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/hammer_finish_1019';D=R/'assets/game/levels/stage_05/boss/hammer_finish_1019'
D.mkdir(parents=True,exist_ok=True)
s=(R/'assets/boss_motion_art_1009.js').read_text(encoding='utf-8');death=json.loads(s[s.index('={')+1:s.rindex(';')])['hammer_death'][:5]
art={'canvas':[256,256],'banks':{}}
for bank in ['chaingun','recovery']:
 rows=[]
 for i in range(9 if bank=='chaingun' else 5):
  if bank=='chaingun':
   im=Image.open(S/f'chaingun_{i:02}.png').convert('RGBA');pivot=[128,112];source=(S/f'chaingun_{i:02}.png').relative_to(R).as_posix()
  else:
   a=death[i];raw=Image.open(R/a['path']).convert('RGBA');raw=raw.resize((round(raw.width*.5),round(raw.height*.5)),Image.Resampling.NEAREST)
   im=Image.new('RGBA',(256,256));pivot=[128,72];im.alpha_composite(raw,(128-round(a['pivot'][0]*.5),72-round(a['pivot'][1]*.5)));source=a['path']
  assert im.size==(256,256)
  box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256
  path=D/f'{bank}_{i:02}.png';im.save(path,optimize=True)
  rows.append(dict(key=f'hf19_{bank}_{i}',path=path.relative_to(R).as_posix(),w=256,h=256,pivot=pivot,bounds=list(box),sha256=hashlib.sha256(im.tobytes()).hexdigest(),source=source))
 art['banks'][bank]=rows
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(R/'assets/hammer_finish_art_1019.js').write_text('"use strict";\n// Owned by build_hammer_finish_1019.py.\nconst HMF19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
(S/'provenance.json').write_text(json.dumps({'service':'PixelLab animate_image','job':'3b415711-c8dd-4ec3-b019-92409a59a291','asset':'ac1d939f-0820-5c8c-b4b1-3b69c19b7523','frames':8,'canvas':[256,256],'seed':101919,'source':'chaingun_seed.png','recovery':'First five intact existing hammer_death frames; no rupture/fire cells.'},indent=2)+'\n',encoding='utf-8')
