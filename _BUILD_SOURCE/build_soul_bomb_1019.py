"""Export reviewed PixelLab soul-bomb animations using fixed padded cells."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,time
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/soul_bomb_1019';D=R/'assets/game/levels/stage_08/effects/soul_bomb_1019';O=R/'_shots/soul_bomb_1019'
JOBS={'charge':'ff05f280-a594-4a00-9640-58bdb4160c0f','flight':'1c67adf2-41ba-4689-aae3-875b7d842b9d','burst':'b9233ea4-5524-4971-a194-d0575ecbeed8'}
for p in [S,D,O]:p.mkdir(parents=True,exist_ok=True)
def fetch(task):
 bank,i=task;p=S/('burst_clean' if bank=='burst' else bank)/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  try:
   with Image.open(p) as im:im.verify()
   return
  except Exception:pass
 for attempt in range(4):
  try:
   with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{JOBS[bank]}/download?index={i}',timeout=60) as response:data=response.read()
   from io import BytesIO
   with Image.open(BytesIO(data)) as im:im.verify()
   p.write_bytes(data);return
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt)

with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,[(b,i) for b in JOBS for i in range(9 if b=='burst' else 13)]))
art={'palette':'purple_gray_white','banks':{}};audit={'jobs':JOBS,'reference':'https://www.facebook.com/reel/1416381680660383','observed':'At 21.5–24.9s: gathered emerald orb, electrical buildup, giant skull inside hooked green flame, rushing comet and dispersal.','palette':{'name':'purple_gray_white','method':'PixelLab exact map_colors; alpha and geometry unchanged','jobs':{'charge':'f6e5ad8a-32f5-49f2-b643-978444cb1904','flight':'0cfdb0d6-b041-4d2e-8196-5e6502afd0fd','burst':'c713f42c-6f0b-4c23-a786-fe912b49dedd'}},'banks':{},'rejected':[{'bank':'flight','sourceFrames':[11,12],'reason':'Flame ring loses its detailed clustered shading at the loop seam.'},{'bank':'burst','job':'d7917e2e-fc62-4b53-be8a-1f958138c9a8','reason':'Early expanding flame frames touch the source border; regenerate with wider margins.'}]}
for bank in JOBS:
 size=160 if bank=='charge' else 256;original=128 if bank=='charge' else 256 if bank=='burst' else 192;pad=(size-original)//2
 rows=[];poses=[];border=[];sheet=Image.new('RGBA',(size*4,size*4),(6,13,23,255))
 for i in (range(1,11) if bank=='flight' else range(1,13) if bank=='charge' else range(9)):
  raw=Image.open(S/'purple'/bank/f'{i:02}.png').convert('RGBA');assert raw.size==(original,original),(bank,i,raw.size)
  edge=list(raw.getchannel('A').crop((0,0,original,1)).getdata())+list(raw.getchannel('A').crop((0,original-1,original,original)).getdata())+list(raw.getchannel('A').crop((0,0,1,original)).getdata())+list(raw.getchannel('A').crop((original-1,0,original,original)).getdata())
  border.append(sum(v>48 for v in edge))
  im=Image.new('RGBA',(size,size));im.alpha_composite(raw,(pad,pad));path=D/f'{bank}_{len(rows):02}.png';im.save(path,optimize=True)
  rows.append(dict(key=f'soul19_{bank}_{len(rows)}',path=path.relative_to(R).as_posix(),w=size,h=size,pivot=[size//2,size//2],bounds=list(im.getbbox()) if im.getbbox() else None,source=(S/'purple'/bank/f'{i:02}.png').relative_to(R).as_posix(),sha256=hashlib.sha256(im.tobytes()).hexdigest()))
  xy=(len(poses)%4*size,len(poses)//4*size);sheet.alpha_composite(im,xy);ImageDraw.Draw(sheet).text((xy[0]+4,xy[1]+4),str(i),fill='#ffffff');poses.append(im)
 for old in D.glob(bank+'_*.png'):
  if old.name not in {Path(a['path']).name for a in rows}:
   assert old.resolve().parent==D.resolve();old.unlink()
 art['banks'][bank]=rows;audit['banks'][bank]={'frames':len(rows),'canvas':[size,size],'pivot':[size//2,size//2],'sourceBorderOpaquePixels':border,'scale':'Identity scale; common transparent padding only.'}
 sheet.save(O/f'{bank}-sheet.png');poses[0].save(O/f'{bank}.webp',save_all=True,append_images=poses[1:],duration=50,loop=0,lossless=True)
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8');(S/'provenance.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
(R/'assets/soul_bomb_art_1019.js').write_text('"use strict";\n// Owned by build_soul_bomb_1019.py.\nconst SOUL19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps(audit['banks']))
