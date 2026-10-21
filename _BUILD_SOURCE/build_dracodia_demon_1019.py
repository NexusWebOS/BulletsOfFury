"""PixelLab raw banks -> fixed registered padded shipping frames and review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
import urllib.request,json,time,hashlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_demon_1019';O=R/'_shots/dracodia_demon_1019';D=R/'assets/game/levels/stage_08/effects/dracodia_demon_1019'
for p in [S,O,D]:p.mkdir(parents=True,exist_ok=True)
jobs=json.loads((S/'jobs.json').read_text())
for bank,j in jobs.items():
 if j.get('workbench'):
  folder=S/j.get('folder',bank);folder.mkdir(parents=True,exist_ok=True);sheet=folder/'frames.png'
  if not sheet.exists():sheet.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/pixel-tools/{j["workbench"]}/frames.png',timeout=90).read())
  im=Image.open(sheet);side=j.get('size',192);cols=im.width//side
  for i in range(j['frames']):im.crop((i%cols*side,i//cols*side,(i%cols+1)*side,(i//cols+1)*side)).save(folder/f'{i:02}.png')
def fetch(row):
 bank,index=row;p=S/jobs[bank].get('folder',bank)/f'{index:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  for attempt in range(4):
   try:
    data=urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{jobs[bank]["animation"]}/download?index={index}',timeout=90).read();p.write_bytes(data);break
   except Exception:
    if attempt==3:raise
    time.sleep(2)
 return p
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,[(k,i) for k,v in jobs.items() for i in range(v['frames'])]))
art={'banks':{}};audit={'jobs':jobs,'banks':{}};html=[]
for bank,j in jobs.items():
 rows=[];poses=[];bounds=[];edges=[];source=j.get('size',128 if bank.startswith(('jet','robot')) else 192);size=source+64;pad=32
 for i in range(j['frames']):
  if i in j.get('rejectFrames',[]):continue
  raw=Image.open(S/j.get('folder',bank)/f'{i:02}.png').convert('RGBA');assert raw.size==(source,source),(bank,i,raw.size)
  alpha=raw.getchannel('A');edges.append(sum(v>48 for box in [(0,0,source,1),(0,source-1,source,source),(0,0,1,source),(source-1,0,source,source)] for v in alpha.crop(box).getdata()))
  destination=R/'assets/game/shared/player_fx/context_deaths_1019' if bank in ['ice','erase'] else R/'assets/game/levels/stage_08/enemies/dracodia_legion_1019' if bank.startswith(('jet','robot')) else D
  destination.mkdir(parents=True,exist_ok=True)
  im=Image.new('RGBA',(size,size));im.alpha_composite(raw,(pad,pad));p=destination/f'{bank}_{i:02}.png';im.save(p,optimize=True);poses.append(im);bounds.append(im.getbbox())
  rows.append(dict(key=f'dr21_{bank}_{i}',path=p.relative_to(R).as_posix(),w=size,h=size,pivot=[size//2,size//2],bounds=im.getbbox(),sha256=hashlib.sha256(im.tobytes()).hexdigest()))
 for folder in {D,destination}:
  for old in folder.glob(bank+'_*.png'):
   if old.relative_to(R).as_posix() not in {a['path'] for a in rows}:
    assert old.resolve().parent==folder.resolve() and R.resolve() in old.resolve().parents;old.unlink()
 assert not any(edges),(bank,'clipped source edge pixels',edges)
 art['banks'][bank]=rows;audit['banks'][bank]={'canvas':[size,size],'pivot':[size//2,size//2],'frames':len(rows),'sourceBorderPixels':edges,'bounds':bounds,'scale':'identity; shared transparent padding only'}
 poses[0].save(O/f'{bank}.webp',save_all=True,append_images=poses[1:],duration=56,loop=0,lossless=True)
 sheet=Image.new('RGBA',(size*4,size*4),(8,9,18,255));draw=ImageDraw.Draw(sheet)
 for i,im in enumerate(poses):
  xy=(i%4*size,i//4*size);sheet.alpha_composite(im,xy);draw.text((xy[0]+4,xy[1]+4),str(i),fill='white')
 sheet.save(O/f'{bank}-sheet.png');html.append(f'<section><h2>{bank}</h2><img src="{bank}.webp"><details><summary>All frames</summary><img class="sheet" src="{bank}-sheet.png"></details></section>')
for old in D.glob('teleport_*.png'):
 if 'teleport' not in jobs:
  assert old.resolve().parent==D.resolve();old.unlink()
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n');(S/'provenance.json').write_text(json.dumps(audit,indent=2)+'\n')
(R/'assets/dracodia_demon_art_1019.js').write_text('"use strict";\n// Owned by build_dracodia_demon_1019.py\nconst DR21_ART='+json.dumps(art,separators=(',',':'))+';\n')
(O/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Dracodia — Demon in the machine</title><style>body{background:#090b14;color:#eee;font:18px monospace;margin:32px}h1,h2{color:#cd9bff}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}section{background:#131525;padding:16px;border:1px solid #644884}img{image-rendering:pixelated;max-width:100%}.sheet{width:100%}a{color:#efcfff}</style><h1>DRACODIA — DEMON IN THE MACHINE</h1><p>Live choreography and PixelLab animation banks. Purple / chromium gray / white.</p><p><a href="encounter.webp">Native encounter animation</a></p><main>'+''.join(html)+'</main>')
print(json.dumps({k:{'frames':v['frames'],'edgePixels':v['sourceBorderPixels']} for k,v in audit['banks'].items()}))
review=O/'review.html'
native='<h2>Native encounter</h2><section><img src="homing_encounter.webp" alt="Live homing shadow ball, late dodge and giant foreground approach"><p>No FOV warning. The ball homes until its final escape window, then rushes past the screen. The aircraft dodges with no invulnerability.</p></section><main>'+''.join('<section><h2>'+label+'</h2><img src="'+file+'"></section>' for label,file in [('Overhead cast / Fear THIS!','caption-cast.png'),('Ghost teleport','ghostTeleport-cast.png'),('Download ritual','downloadRitual-release.png'),('Absorbing code shield / hit flash','shield-hit.png'),('Laser death','death-laser.png'),('Ice death','death-ice.png')])+'</main><h2>Orbital mechanical symbiote</h2><main><section><img src="../../assets/game/shared/cinematics/dracodia_demon_1019/emergence.webp"></section><section><img src="../../assets/game/shared/cinematics/dracodia_demon_1019/contact.webp"></section></main><h2>PixelLab animation banks</h2><main>'
review.write_text(review.read_text().replace('<main>',native,1))
