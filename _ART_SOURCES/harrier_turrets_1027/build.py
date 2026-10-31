from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,os,shutil,subprocess
W=Path(__file__).resolve().parent
R=W.parents[1]
O=W/'compiled';O.mkdir(exist_ok=True);A={}
S=R/'assets/game/levels/stage_06/boss/bosses/skycarrier/carrier_closed_wells.png'
if not S.exists():S=R/'_ART_SOURCES/encounter_revision_1027/source/whv_closed_w.png'
im=Image.open(S).convert('RGBA')
# These complete dark-metal silhouettes are hand outlined over the two native
# coloured gun assemblies. HH21 files are brightness-only WHITE HIT masks.
outline=[(8,5),(14,5),(17,8),(19,12),(21,17),(20,22),(17,27),(17,35),(12,35),(12,28),(10,28),(10,35),(5,35),(5,27),(2,23),(1,18),(2,13),(5,8)]
native=[]
for i,(x,y)in enumerate([(200,76),(290,76)]):
 q=im.crop((x,y,x+22,y+36));mask=Image.new('L',q.size);d=ImageDraw.Draw(mask);d.polygon(outline,fill=255);q.putalpha(mask)
 native.append(q);q.save(O/f'coloured-source-{i}.png')
for i in range(4):
 q=native[0 if i<2 else 1];frames=[];sockets=[];bounds=[]
 for cycle,recoil in enumerate([0,-2,-1,0]):
  pose=Image.new('RGBA',(32,40));base=q.crop((0,0,22,25));shaft=q.crop((0,25,22,36));pose.alpha_composite(base,(5,2));pose.alpha_composite(shaft,(5,27+recoil))
  k=.9*1.45;size=96;scaled=pose.resize((round(32*k),round(40*k)),Image.Resampling.NEAREST);origin=(size//2-scaled.width//2,size//2-scaled.height//2);cell=Image.new('RGBA',(size,size));cell.alpha_composite(scaled,origin)
  # The common pad pivot is16,20. Two native bore ends alternate their shots.
  tips=[((5+x)*scaled.width/32+origin[0],(2+34+recoil)*scaled.height/40+origin[1])for x in [8,14]]
  for direction in range(64):
   theta=direction*math.tau/64;f=cell.rotate(-direction*360/64,Image.Resampling.NEAREST);frames.append(f);bounds.append(f.getbbox());c,s=math.cos(theta),math.sin(theta)
   sockets.append([[round(c*(x-size/2)-s*(y-size/2),2),round(s*(x-size/2)+c*(y-size/2),2)]for x,y in tips])
 for hit in [False,True]:
  key=f'gun_{i}'+('_hit'if hit else '');sheet=Image.new('RGBA',(96*8,96*32))
  for j,f in enumerate(frames):
   if hit:t=Image.new('RGBA',f.size,(255,255,255,0));t.putalpha(f.getchannel('A'))
   else:t=f
   sheet.alpha_composite(t,(j%8*96,j//8*96))
  sheet.save(O/f'{key}.png',optimize=True);A[key]={'key':'ht28_'+key,'path':f'assets/game/levels/stage_06/boss/harrier_turrets_1027/{key}.png','cw':96,'ch':96,'cols':8,'frames':256,'pivot':[48,48],'angles':64,'cycles':4}
  if not hit:A[key].update(muzzles=sockets,bounds=bounds)
out='"use strict";\nconst HT28_ART='+json.dumps(A,separators=(',',':'))+';\n';(W/'harrier_turrets_art_1027.js').write_text(out,encoding='utf-8')
(O/'manifest.json').write_text(json.dumps(A,indent=2),encoding='utf-8')
board=Image.new('RGBA',(768,384),(14,24,34,255));d=ImageDraw.Draw(board)
for i,di in enumerate([0,8,16,24,32,40,48,56]):
 a=A['gun_0'];sheet=Image.open(O/'gun_0.png');f=sheet.crop((di%8*96,di//8*96,di%8*96+96,di//8*96+96));board.alpha_composite(f.resize((192,192),Image.Resampling.NEAREST),(i%4*192,i//4*192));d.text((i%4*192+8,i//4*192+8),f'{di*360/64:g}deg',fill='#9cd7e5')
board.save(W/'coloured-directions.png')
ase=os.environ.get('ASEPRITE_EXE')or shutil.which('aseprite')
if ase:subprocess.run([ase,'--batch',str(O/'gun_0.png'),'--save-as',str(O/'gun-colour.aseprite')],capture_output=True,check=True)
print('Authored eight opaque gun/hit banks, fixed mounting pivots and per-bore directional/recoil sockets.')

for a in A.values():
 target=R/a["path"];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/(target.stem+".png"),target)
shutil.copy2(W/"harrier_turrets_art_1027.js",R/"assets/harrier_turrets_art_1027.js")
