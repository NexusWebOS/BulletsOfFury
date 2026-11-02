"""Fixed even-cell source art for physical twin weapons and black camo.
No atlas edits. All aiming directions are baked; source/crop/hash registered.
"""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'assets/game/levels/stage_01/enemies/physical_1031';O.mkdir(parents=True,exist_ok=True);A={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p,n):return json.JSONDecoder().raw_decode((R/p).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def gray(im,armor=False):
 im=im.copy()
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=im.getpixel((x,y));v=round(.2126*r+.7152*g+.0722*b)
   if a and(not armor or g>r*1.03 and g>b*1.1):
    v=round(v*.72)if armor else min(255,round(v*1.15));im.putpixel((x,y),(v,v,min(255,v+3),a))
 return im
def bank(name,frames,cell,dirs=1,refs=None):
 out=Image.new('RGBA',(cell*dirs,cell*len(frames)))
 for f,im in enumerate(frames):
  assert im.size==(cell,cell)
  pad=Image.new('RGBA',(cell*3,cell*3));pad.alpha_composite(im,(cell,cell))
  for d in range(dirs):out.alpha_composite(pad.rotate(-d*360/dirs,Image.Resampling.NEAREST,center=(cell*1.5,cell*1.5)).crop((cell,cell,cell*2,cell*2)),(d*cell,f*cell))
 p=O/(name+'.png');out.save(p,optimize=True);A[name]=dict(key='s1b_'+name,path=p.relative_to(R).as_posix(),cell=cell,pivot=[cell//2]*2,dirs=dirs,frames=len(frames),sources=refs,sha256=sha(p))
S=data('assets/stage1_motion_art_1009.js','S1M_ART')
for name,source,selection in [('gray_hull','hull',range(8)),('gray_turret','turret',[3])]:
 refs=[dict(path=S[source][i]['path'],sha256=sha(R/S[source][i]['path']))for i in selection]
 bank(name,[gray(Image.open(R/a['path']).convert('RGBA'),True).resize((192,192),Image.Resampling.NEAREST)for a in refs],192,64 if source=='turret'else 1,refs)
s=data('assets/stage1_amplify_art_1031.js','S1A_ART')['slug'];im=Image.open(R/s['path']).convert('RGBA')
bank('gray_slug',[gray(im.crop((0,f*64,64,(f+1)*64)))for f in range(4)],64,32,[dict(path=s['path'],sha256=sha(R/s['path']))])
for w in ['mg','missile']:
 p=R/('assets/game/shared/combat/enemy_overhaul_0925/sprites/ground_head_'+w+'.png');im=Image.open(p).convert('RGBA');bank('head_'+w,[im],256,64,[dict(path=p.relative_to(R).as_posix(),sha256=sha(p))])
# The red/white rocket is the actual loaded centre rocket of the current truck.
# Restrict its material mask to red paint, neutral metal and dark outlines;
# olive rack pixels are excluded. Exhaust comes from the authored S1M reel.
p=R/'assets/game/levels/stage_01/enemies/missile_truck_1018/mt18_launcher_olive_00.png';rect=[80,38,112,124];rocket=Image.open(p).convert('RGBA').crop(rect)
for y in range(rocket.height):
 for x in range(rocket.width):
  r,g,b,a=rocket.getpixel((x,y))
  if max(r,g,b)-min(r,g,b)>42 and not(r>g*1.6 and r>b*1.6):rocket.putpixel((x,y),(0,0,0,0))
frames=[]
for f in range(4):
 tile=Image.new('RGBA',(64,64));ex=Image.open(R/S['exhaust'][f]['path']).convert('RGBA').resize((9,22),Image.Resampling.NEAREST)
 for y in range(ex.height):
  for x in range(ex.width):
   r,g,b,a=ex.getpixel((x,y));v=max(r,g,b)
   if a:ex.putpixel((x,y),(v,round(v*.65),round(v*.20),a))
 tile.alpha_composite(ex,(28,5));tile.alpha_composite(rocket.resize((10,27),Image.Resampling.NEAREST),(27,22));frames.append(tile)
bank('rack_rocket',frames,64,32,[dict(path=p.relative_to(R).as_posix(),rect=rect,materialMask='red/white/neutral; rack excluded',sha256=sha(p)),dict(exhaust=S['exhaust'][:4])])
(O/'manifest.json').write_text(json.dumps(dict(owner='_BUILD_SOURCE/build_stage1_followup_1031.py',banks=A),indent=2)+'\n',encoding='utf-8')
(R/'assets/stage1_followup_art_1031.js').write_text('"use strict";\nconst S1B_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
Q=R/'_shots/stage1_followup_1031';Q.mkdir(exist_ok=True);out=Image.new('RGB',(1100,len(A)*180),(12,27,34));d=ImageDraw.Draw(out)
for row,(n,a)in enumerate(A.items()):
 d.text((5,row*180+5),n,fill='white');im=Image.open(R/a['path']);c=a['cell']
 for i in range(min(6,a['dirs'])):
  t=im.crop((i*c,0,(i+1)*c,c));t.thumbnail((160,150),Image.Resampling.NEAREST);out.paste(t,(i*180+8,row*180+25),t)
out.save(Q/'new-banks.png');print('Built',len(A),'physical weapon banks')
