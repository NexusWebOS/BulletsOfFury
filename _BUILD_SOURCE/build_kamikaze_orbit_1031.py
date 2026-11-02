"""Current AF21 kamikaze roll poses, earth-camo palette and baked headings.
FRAME FORMAT:128x128 RGBA cells, shared64,64 fuselage pivot, one source scale.
The whole16-pose authored roll is reused; no new hull or procedural sprite.
"""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'assets/game/levels/stage_01/enemies/kamikaze_orbit_1031';O.mkdir(parents=True,exist_ok=True);Q=R/'_shots/kamikaze_orbit_1031';Q.mkdir(exist_ok=True)
s=(R/'assets/air_refit_art_1021.js').read_text(encoding='utf-8');M=json.JSONDecoder().raw_decode(s.split('const AF21_ART=',1)[1])[0]['models']['s1jetdelta_b'];B=M['banks']['roll'];src=R/B['path'];im=Image.open(src).convert('RGBA');frames=[];mounts=[];removed=[]
for f,rect in enumerate(B['cells']):
 x,y,w,h=rect;t=im.crop((x,y,x+w,y+h));blue=set()
 for yy in range(8,58):
  for xx in range(34,94):
   r,g,b,a=t.getpixel((xx,yy))
   if a>80 and b>115 and b>r*1.45 and b>g*1.05:blue.add((xx,yy))
 groups=[]
 while blue:
  todo=[blue.pop()];group=[]
  while todo:
   p=todo.pop();group.append(p)
   for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]:
    n=(p[0]+dx,p[1]+dy)
    if n in blue:blue.remove(n);todo.append(n)
  if len(group)>2:groups.append(group)
 assert groups,('No actual tail flame found',f)
 sockets=[];cuts=[]
 for group in groups:
  bottom=max(p[1]for p in group);edge=[p[0]for p in group if p[1]>=bottom-1];sockets.append([sum(edge)/len(edge),bottom+1]);cut=[min(p[0]for p in group),min(p[1]for p in group),max(p[0]for p in group)+1,bottom+1];t.paste((0,0,0,0),cut);cuts.append(cut)
 mounts.append(sockets);removed.append(cuts)
 # Paint the existing material/camo clusters, retaining dark seams and bright
 # neutral highlights. All colour ratios are normalized to source luminance.
 for yy in range(128):
  for xx in range(128):
   r,g,b,a=t.getpixel((xx,yy));v=max(r,g,b);Y=.2126*r+.7152*g+.0722*b
   if not a or v<52:continue
   if g>r*1.18 and g>b*1.12:rgb=(.85,1.08,.44)
   elif max(r,g,b)-min(r,g,b)<65 and Y<224:rgb=(1.35,.94,.52)if Y<175 else(1.16,1,.76)
   else:continue
   k=Y/(.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]);t.putpixel((xx,yy),(*(min(255,round(k*c))for c in rgb),a))
 frames.append(t)
dirs=32;sheet=Image.new('RGBA',(128*dirs,128*len(frames)))
for f,t in enumerate(frames):
 pad=Image.new('RGBA',(384,384));pad.alpha_composite(t,(128,128))
 for d in range(dirs):sheet.alpha_composite(pad.rotate(-d*360/dirs,Image.Resampling.NEAREST,center=(192,192)).crop((128,128,256,256)),(d*128,f*128))
p=O/'earth_roll_heading.png';sheet.save(p,optimize=True)
A=dict(key='ko31_earth_roll_heading',path=p.relative_to(R).as_posix(),cell=128,pivot=[64,64],dirs=dirs,frames=len(frames),tailSockets=mounts,source=dict(path=B['path'],cells=B['cells'],sha256=hashlib.sha256(src.read_bytes()).hexdigest(),staticExhaustRemoved=removed),palette='luminance-preserving light tan/orange-brown/olive; outlines and neutral highlights retained',sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(O/'manifest.json').write_text(json.dumps(dict(owner='_BUILD_SOURCE/build_kamikaze_orbit_1031.py',roll=A),indent=2)+'\n',encoding='utf-8')
(R/'assets/kamikaze_orbit_art_1031.js').write_text('"use strict";\nconst KO31_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
out=Image.new('RGB',(1024,320),(12,25,34));d=ImageDraw.Draw(out)
for f,t in enumerate(frames):out.paste(t,((f%8)*128,(f//8)*160+20),t);d.text(((f%8)*128+5,(f//8)*160+3),str(f),fill='white')
out.save(Q/'earth-roll-contact.png');print('Built',len(frames)*dirs,'fixed roll/heading frames with per-pose exhaust sockets')
