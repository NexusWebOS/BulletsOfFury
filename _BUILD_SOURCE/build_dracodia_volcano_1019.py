"""Lossless native volcano anatomy -> registered articulated components."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_volcano_1019';D=R/'assets/game/levels/stage_08/boss/volcano_modular_1019';O=R/'_shots/dracodia_volcano_1019'
for p in [S,D,O]:p.mkdir(parents=True,exist_ok=True)
raw=(R/'assets/stage8_identity_art_1018.js').read_text(encoding='utf-8');old=json.loads(raw[raw.index('{'):raw.rindex(';')]);parts={};anchors={
'torso':[160,160],'reactor':[159,162],'ventL':[140,108],'ventR':[192,108],
'shoulderL':[113,144],'shoulderR':[210,143],'upperL':[113,144],'upperR':[210,143],
'left':[84,178],'right':[230,182],'thighL':[120,203],'thighR':[196,203],
'footL':[127,231],'footR':[196,231],'head':[160,112],'flareL':[128,67],'flareR':[190,66]}
owners={'torso':'core','reactor':'core','ventL':'ventL','ventR':'ventR','shoulderL':'shoulderL','shoulderR':'shoulderR','upperL':'left','upperR':'right','left':'left','right':'right','thighL':'legL','thighR':'legR','footL':'legL','footR':'legR','head':'head','flareL':'ventL','flareR':'ventR'}
yy,xx=np.indices((320,320));labels={};total=np.zeros((320,320,4),np.uint8)
for name,a in old['volcano'].items():
 im=np.array(Image.open(R/a['path']).convert('RGBA'));total=np.maximum(total,im)
 lab=np.full((320,320),name,object)
 if name=='core':
  lab[:]='torso';lab[((xx-159)**2+(yy-162)**2)<=20**2]='reactor'
  lab[(xx<157)&(yy<112)]='ventL';lab[(xx>174)&(yy<112)]='ventR'
  lab[(xx<132)&(yy>=110)&(yy<167)]='shoulderL';lab[(xx>190)&(yy>=110)&(yy<168)]='shoulderR'
  lab[(xx<110)&(yy>175)]='left'
  lab[(xx>=110)&(xx<146)&(yy>=36)&(yy<67)]='flareL';lab[(xx>=171)&(xx<207)&(yy>=33)&(yy<66)]='flareR'
 if name=='left':lab[yy<178]='upperL'
 if name=='right':lab[yy<182]='upperR'
 if name=='legL':lab[:]='thighL';lab[yy>=231]='footL'
 if name=='legR':lab[:]='thighR';lab[yy>=231]='footR'
 for part in np.unique(lab):
  p=parts.setdefault(part,np.zeros_like(im));sel=(lab==part)&(im[:,:,3]>0);p[sel]=im[sel]
rebuild=np.zeros_like(total);art={'parts':{}};audit={};preview=Image.new('RGB',(320*4,350*5),'#101622');g=ImageDraw.Draw(preview)
for i,(name,arr) in enumerate(parts.items()):
 rebuild=np.maximum(rebuild,arr);im=Image.fromarray(arr);assert im.getbbox(),name
 assert not any(im.getchannel('A').crop(b).getbbox() for b in [(0,0,320,1),(0,319,320,320),(0,0,1,320),(319,0,320,320)])
 p=D/(name+'.png');im.save(p,optimize=True);row=dict(key='vp23_'+name,path=p.relative_to(R).as_posix(),w=320,h=320,pivot=[160,160],anchor=anchors[name],owner=owners[name],bounds=list(im.getbbox()))
 art['parts'][name]=row;audit[name]=dict(**row,bytes=p.stat().st_size,sha256=hashlib.sha256(im.tobytes()).hexdigest())
 x=i%4*320;y=i//4*350;preview.paste(im,(x,y),im);g.text((x+8,y+322),name+' -> '+owners[name],fill='white')
assert np.array_equal(rebuild,total),'Every authored source pixel must survive exactly once'
preview.save(O/'components.png');Image.fromarray(rebuild).save(O/'rebuilt-master.png')
# An existing knee bearing supplies actual authored material behind rotating
# elbows/hips/vent hinges. It is a copied cutout, never invented joint pixels.
socket=Image.new('RGBA',(48,48));patch=Image.fromarray(total).crop((116,217,140,241));mask=Image.new('L',(24,24));ImageDraw.Draw(mask).ellipse((0,0,23,23),fill=255);patch.putalpha(Image.fromarray(np.minimum(np.array(patch.getchannel('A')),np.array(mask))));socket.alpha_composite(patch,(12,12));p=D/'joint_bearing.png';socket.save(p,optimize=True)
art['socket']=dict(key='vp23_joint',path=p.relative_to(R).as_posix(),w=48,h=48,pivot=[24,24],anchor=[24,24],bounds=list(socket.getbbox()))
art['flame']=dict(job='8f1541b6-2c1d-4e40-a981-83697e833c34',pivot=[64,96],w=128,h=128,frames=[])
flames=S/'flame';flames.mkdir(exist_ok=True)
if '--flame' in __import__('sys').argv:
 import urllib.request
 drawing='cf13a431-9785-406f-ba81-426bca718532';p=flames/'exact.png'
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://api.pixellab.ai/mcp/pixel-tools/{drawing}/assets/south/full.png',timeout=90).read())
 grid=Image.open(p).convert('RGBA');assert grid.size==(512,512);frames=[];art['flame']['drawing']=drawing;art['flame']['rejectedGeneration']='The AI clip grew into an unrelated large swaying fireball; exact authored flame with pinned base is accepted instead.'
 for i in range(16):
  im=grid.crop((i%4*128,i//4*128,i%4*128+128,i//4*128+128));a=im.getchannel('A');assert not any(a.crop(b).getbbox() for b in [(0,0,128,1),(0,127,128,128),(0,0,1,128),(127,0,128,128)]),(i,'clipped')
  p=D/f'flame_{i:02}.png';im.save(p,optimize=True);art['flame']['frames'].append(dict(key=f'vp23_flame_{i}',path=p.relative_to(R).as_posix(),w=128,h=128,pivot=[64,96],bounds=im.getbbox()));frames.append(im)
 frames[0].save(O/'vent-flame.webp',save_all=True,append_images=frames[1:],duration=60,loop=0,lossless=True)
 sheet=Image.new('RGB',(512,512),'#101622')
 for i,im in enumerate(frames):sheet.paste(im,(i%4*128,i//4*128),im)
 sheet.save(O/'vent-flame-sheet.png')
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n');(S/'components.json').write_text(json.dumps(dict(reconstructsMaster=True,components=audit),indent=2)+'\n')
(R/'assets/dracodia_volcano_art_1019.js').write_text('"use strict";\n// Owned by build_dracodia_volcano_1019.py; lossless authored anatomy.\nconst VP23_ART='+json.dumps(art,separators=(',',':'))+';\n')
print(json.dumps(dict(components=len(parts),reconstructsMaster=True,flameFrames=len(art['flame']['frames']),bytes=sum(p.stat().st_size for p in D.glob('*.png')))),flush=True)
