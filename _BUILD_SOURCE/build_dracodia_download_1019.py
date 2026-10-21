"""Own the seven PixelLab wireframe sheets and their fixed-cell registry."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_download_1019';O=R/'_shots/dracodia_download_1019';D=R/'assets/game/levels/stage_08/boss/dracodia_download_1019'
for p in [S,O,D]:p.mkdir(parents=True,exist_ok=True)
jobs=json.loads((S/'jobs.json').read_text());art={'forms':{}};audit={}
def fetch(row):
 name,j=row;d=S/name/j.get('cacheTag','');d.mkdir(parents=True,exist_ok=True)
 for file,url in [('full.png',f'https://api.pixellab.ai/mcp/pixel-tools/{j["drawing"]}/assets/south/full.png'),('recipe.json',f'https://api.pixellab.ai/mcp/pixel-tools/{j["drawing"]}/recipe.json'),('wire.png',f'https://api.pixellab.ai/mcp/images/{j["edit"]}/download?index=0')]:
  p=d/file
  if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=90).read())
 return name
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,jobs.items()))
for name,j in jobs.items():
 im=Image.open(S/name/j.get('cacheTag','')/'full.png').convert('RGBA');assert im.size==(1024,1024),(name,im.size)
 poses=[im.crop((i%4*256,i//4*256,i%4*256+256,i//4*256+256)) for i in range(16)]
 assert len({hashlib.sha256(p.tobytes()).hexdigest() for p in poses})>=12,name
 edges=[]
 for pose in poses:
  a=pose.getchannel('A');edges.append(sum(v>0 for box in [(0,0,256,1),(0,255,256,256),(0,0,1,256),(255,0,256,256)] for v in a.crop(box).getdata()))
 assert not any(edges),(name,edges)
 p=D/(name+'.png');im.save(p,optimize=True)
 boxes=[p.getbbox() for p in poses];bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
 art['forms'][name]=dict(key='dr22_wire_'+name,path=p.relative_to(R).as_posix(),w=256,h=256,columns=4,frames=16,pivot=[128,128],bounds=bounds,captureScale=.5,captureSize=410)
 audit[name]=dict(source=j,canvas=[256,256],sheet=list(im.size),borderPixels=edges,bounds=[p.getbbox() for p in poses],bytes=p.stat().st_size,sha256=hashlib.sha256(im.tobytes()).hexdigest())
 poses[0].save(O/(name+'.webp'),save_all=True,append_images=poses[1:],duration=70,loop=0,lossless=True)
 sheet=Image.new('RGB',(1024,1088),'#131521');g=ImageDraw.Draw(sheet)
 for i,pose in enumerate(poses):
  x=i%4*256;y=i//4*272;sheet.paste(pose,(x,y),pose);g.text((x+8,y+256),'FRAME '+str(i+1),fill='white')
 sheet.save(O/(name+'-sheet.png'))
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n');(S/'provenance.json').write_text(json.dumps(audit,indent=2)+'\n')
(R/'assets/dracodia_download_art_1019.js').write_text('"use strict";\n// Owned by build_dracodia_download_1019.py; actual native forms -> PixelLab wireframes.\nconst DR22_ART='+json.dumps(art,separators=(',',':'))+';\n')
(O/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Dracodia downloads</title><style>body{background:#0b0c15;color:#eee;font:18px monospace;margin:28px}a{color:#d9afff}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}section{background:#19182a;padding:16px}img{max-width:100%;image-rendering:pixelated}h1,h2{color:#c5a6ff}</style><h1>DRACODIA â€” DOWNLOAD THE NEXT BODY</h1><p>Actual native forms, PixelLab hollow wireframes, moving scan highlights and progressive armor reconstruction.</p><p><a href="../dracodia_demon_1019/review.html">Demon-machine attacks</a></p><h2>Native game captures</h2><main><section><h2>Rotating shadow ball / late edge escape</h2><img src="rotating-ball.webp"></section><section><h2>All five Phase 3 form changes</h2><img src="form-downloads.webp"></section><section><h2>Phase 2 and 3 arrival</h2><img src="phase-downloads.webp"></section></main><h2>PixelLab banks â€” every frame</h2><main>'+''.join('<section><h2>'+name+'</h2><img src="'+name+'.webp"><details><summary>All 16 frames</summary><img src="'+name+'-sheet.png"></details></section>' for name in jobs)+'</main>')
print(json.dumps(dict(forms=len(jobs),frames=len(jobs)*16,bytes=sum(r['bytes'] for r in audit.values()),borderPixels=sum(sum(r['borderPixels']) for r in audit.values()))),flush=True)
