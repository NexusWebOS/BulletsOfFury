from pathlib import Path
from PIL import Image
import json, hashlib
R=Path(__file__).resolve().parents[1]
W=R/'_shots/ngplus_1027';W.mkdir(parents=True,exist_ok=True)
s=(R/'assets/element_arsenal_art_1011.js').read_text(); banks=json.loads(s[s.index('{'):s.rindex('}')+1])['banks']
out=R/'assets/game/shared/combat/ngplus_1027';out.mkdir(parents=True,exist_ok=True)
manifest={}
for el in ['fire','ice','lightning','chrome','toxic','dark','water','wind','kinetic']:
 source=banks[('kinetic' if el=='wind' else el)+'_round'];image=Image.open(R/source['path']).convert('RGBA')
 sheet=Image.new('RGBA',(72*32,72*16))
 for frame,(x,y,w,h) in enumerate(source['frames'][:16]):
  cell=image.crop((x,y,x+w,y+h)).resize((48,48),Image.Resampling.NEAREST)
  if el=='wind':
   pix=cell.load()
   for yy in range(48):
    for xx in range(48):
     r,g,b,a=pix[xx,yy];l=max(r,g,b)
     if a and l>40 and max(r,g,b)-min(r,g,b)>20:
      luminance=.2126*r+.7152*g+.0722*b;v=min(255,luminance/(.2126*.55+.7152+.0722*.86))
      pix[xx,yy]=(round(v*.55),round(v),round(v*.86),a)
  base=Image.new('RGBA',(72,72));base.alpha_composite(cell,(36-round(source['pivot'][0]*.375),36-round(source['pivot'][1]*.375)))
  for direction in range(32):sheet.alpha_composite(base.rotate(-direction*360/32,resample=Image.Resampling.NEAREST),(direction*72,frame*72))
 path=out/(el+'.png');sheet.save(path,optimize=True)
 manifest[el]={'key':'ng27_'+el,'path':path.relative_to(R).as_posix(),'source':source['path'],'sourceSha256':hashlib.sha256((R/source['path']).read_bytes()).hexdigest(),'directions':32,'frames':16,'cell':72,'pivot':[36,36]}
 print(el,path.stat().st_size,flush=True)
(R/'assets/ngplus_art_1027.js').write_text('"use strict";\nconst NG27_ART='+json.dumps(manifest,separators=(',',':'))+';\n')
(W/'art-manifest.json').write_text(json.dumps(manifest,indent=2))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
