"""Dredger: actual source treads, two twin-barrel turrets, and native circular FOV.
Fixed even cells and pivots; directional/recoil art is baked, never spun live.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw
from pixel_glow_1015 import emissive,used_mask,rings,RING_A

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/dredger_1028'
D=R/'assets/game/levels/stage_07/miniboss/dredger_assault_1028'
D.mkdir(parents=True,exist_ok=True)
A={}

def save(name,im,cell,pivot,frames=1,cols=1,**meta):
 im.save(D/(name+'.png'))
 A[name]=dict(key='dc40_'+name,path=(D/(name+'.png')).relative_to(R).as_posix(),cw=cell[0],ch=cell[1],pivot=pivot,cols=cols,frames=frames,**meta)

def hit(name,im):
 out=Image.new('RGBA',im.size,(255,255,255,0));out.putalpha(im.getchannel('A'))
 a=A[name];save(name+'_hit',out,[a['cw'],a['ch']],a['pivot'],a['frames'],a['cols'])

body=Image.open(S/'body.png').convert('RGBA')
sheet=Image.new('RGBA',(176*8,192))
for phase in range(8):
 im=np.array(body)
 # Eight-pixel authored links cycle within each tread run. Rails/caps/hull stay fixed.
 for x0,x1 in [(15,31),(145,161)]:
  for y0 in range(20,156,8):
   im[y0:y0+8,x0:x1]=np.roll(np.array(body)[y0:y0+8,x0:x1],-phase,axis=0)
 sheet.paste(Image.fromarray(im), (phase*176,0))
save('body',sheet,[176,192],[88,96],8,8,treadBands=[[15,20,16,136],[145,20,16,136]],pixelsPerPhase=1.5)
hit('body',sheet)

# Keep the complete source housing. One actual barrel under each side pod replaces
# the redundant inner barrel of each former four-barrel assembly.
src=Image.open(S/'gun-0.png').convert('RGBA')
housing=src.copy()
for rect in [(12,50,30,76),(54,50,73,76)]:housing.paste((0,0,0,0),rect)
barrels=[src.crop((14,50,21,71)),src.crop((63,50,70,71))]
sheet=Image.new('RGBA',(112*8,112*32));sockets=[];contact=Image.new('RGBA',(112*8,112*4))
k=.94
for cycle,back in enumerate([0,3,2,1]):
 pose=housing.copy()
 for im,x in zip(barrels,[18,59]):pose.alpha_composite(im,(x,50-back))
 # A single proportional scale with the physical housing trunnion as pivot.
 base=pose.transform((112,112),Image.Transform.AFFINE,(1/k,0,42-56/k,0,1/k,31-56/k),Image.Resampling.NEAREST)
 for direction in range(64):
  a=direction*math.tau/64;frame=cycle*64+direction
  im=base.rotate(-direction*360/64,resample=Image.Resampling.NEAREST,center=(56,56))
  sheet.paste(im,((frame%8)*112,(frame//8)*112))
  points=[]
  for x in [21.5,62.5]:
   dx=(x-42)*k;dy=(70-back-31)*k
   points.append([56+dx*math.cos(a)-dy*math.sin(a),56+dx*math.sin(a)+dy*math.cos(a)])
  sockets.append(points)
  if direction%8==0:contact.paste(im,((direction//8)*112,cycle*112))
save('gun',sheet,[112,112],[56,56],256,8,angles=64,cycles=4,sockets=sockets,sourceScale=k,sourceTrunnion=[42,31],recoilPixels=[0,3,2,1])
hit('gun',sheet)

top=Image.open(S/'top.png').convert('RGBA')
save('top',top,[76,68],[38,34]);hit('top',top)
a=np.array(top);mask=emissive(a,used_mask(68,76,[[0,0,76,68]]),1)
glow=rings(mask,a[:,:,:3].astype(np.float32),RING_A,1,.48)
save('top_glow',Image.fromarray(glow.clip(0,255).astype(np.uint8)),[76,68],[38,34])

# Reproject the approved broad FOV's actual source pixels into a north-facing
# 300-degree circular field. The south 60-degree opening is also absent in fire.
yy,xx=np.mgrid[:192,:192];dx=xx-96;dy=yy-96
radius=np.hypot(dx,dy);angle=np.arctan2(dx,-dy);allowed=(radius<=90)&(abs(angle)<=math.radians(150))
for name,file in [('green','fov-light-green.png'),('yellow','fov-yellow.png'),('red','fov-neon-red.png')]:
 original=np.array(Image.open(R/'assets/bossmode/ui'/file).convert('RGBA'))
 sa=angle/math.radians(150)*math.radians(36)
 sx=np.rint(320+np.sin(sa)*radius/90*425).astype(int).clip(0,639)
 sy=np.rint(23+np.cos(sa)*radius/90*425).astype(int).clip(0,639)
 im=original[sy,sx].copy();im[~allowed]=0
 save('circle_'+name,Image.fromarray(im),[192,192],[96,96],sectorDegrees=300,facing='north',source=file)

contact.save(S/'turret-contact.png')
preview=Image.new('RGBA',(640,420),(18,22,20,255))
for i in range(3):preview.alpha_composite(body,(40+i*200,20));preview.alpha_composite(top,(90+i*200,42))
for i in range(3):
 for side in [-1,1]:
  f=i*64+(0 if side<0 else 0);cell=sheet.crop(((f%8)*112,(f//8)*112,(f%8+1)*112,(f//8+1)*112))
  preview.alpha_composite(cell,(40+i*200+88+side*43-56,20+96+66-56))
preview.save(S/'assembled-contact.png')
manifest=dict(builder='_BUILD_SOURCE/build_dredger_assault_1028.py',exporter='_BUILD_SOURCE/export_dredger_1028.py',sources={n:hashlib.sha256((S/n).read_bytes()).hexdigest() for n in ['body.png','top.png','gun-0.png']},banks=A)
(D/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(R/'assets/dredger_assault_art_1028.js').write_text('"use strict";\nconst DC40_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8')
tax=R/'assets/data/ART_TAXONOMY.json';raw=tax.read_text(encoding='utf8')
if '"dc40_"' not in raw:
 entry=dict(role='dredger_treads_twin_turrets_warning',owner=manifest['builder'],manifest=(D/'manifest.json').relative_to(R).as_posix(),note='October28 source-pixel treads, 64 fixed trunnion headings and shot-linked recoil, two barrels per turret, actual sockets/white hit alpha, top 1015 glow, native-palette north-facing circular FOV. Native hull and HP preserved.')
 tax.write_text('{\n  "dc40_": '+json.dumps(entry,separators=(',',':'))+','+raw[1:],encoding='utf8')
print('Dredger: 8 tread cells, 256 twin-barrel recoil/heading cells, top glow, 3 circular FOV colours')
