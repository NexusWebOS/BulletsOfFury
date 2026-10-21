"""PixelLab phoenix master -> lossless articulated avian anatomy, fixed pivots."""
from pathlib import Path
import json,math,hashlib,urllib.request
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/dracodia_phoenix_1020';D=R/'assets/game/levels/stage_08/boss/corrupted_phoenix_1020';O=R/'_shots/dracodia_phoenix_1020'
for p in [S,D,O]:p.mkdir(parents=True,exist_ok=True)
im=Image.open(S/'master.png').convert('RGBA');assert im.size==(256,256)
raw=np.asarray(im);yy,xx=np.indices((256,256));lab=np.full((256,256),'torso',object)
lab[(xx<108)&(yy<118)]='upperL';lab[(xx>=148)&(yy<118)]='upperR'
lab[(xx<80)&(yy<117)]='ventL';lab[(xx>=176)&(yy<117)]='ventR'
lab[((xx-96)**2+(yy-99)**2<14**2)]='shoulderL';lab[((xx-160)**2+(yy-99)**2<14**2)]='shoulderR'
lab[(xx<100)&(yy>=115)]='left';lab[(xx>=156)&(yy>=115)]='right'
lab[(yy>=146)&(xx>=100)&(xx<128)]='thighL';lab[(yy>=146)&(xx>=128)&(xx<156)]='thighR'
lab[(yy>=174)&(xx<120)]='footL';lab[(yy>=174)&(xx>=136)]='footR'
lab[(yy>=193)&(xx>=116)&(xx<128)]='flareL';lab[(yy>=193)&(xx>=128)&(xx<140)]='flareR'
lab[(xx>=108)&(xx<149)&(yy<98)]='head'
lab[((xx-128)**2+(yy-118)**2<=12**2)]='reactor'
anchors={'torso':[128,128],'reactor':[128,118],'head':[128,77],
 'shoulderL':[96,99],'shoulderR':[160,99],'upperL':[96,89],'upperR':[160,89],
 'ventL':[78,58],'ventR':[178,58],'left':[83,119],'right':[173,119],
 'thighL':[113,154],'thighR':[143,154],'footL':[105,181],'footR':[151,181],
 'flareL':[124,198],'flareR':[132,198]}
owners={'torso':'core','reactor':'core','head':'head','shoulderL':'shoulderL','shoulderR':'shoulderR',
 'upperL':'ventL','upperR':'ventR','ventL':'ventL','ventR':'ventR','left':'left','right':'right',
 'thighL':'legL','thighR':'legR','footL':'legL','footR':'legR','flareL':'legL','flareR':'legR'}
names={'torso':'breastplate','reactor':'furnace_heart','head':'phoenix_head','shoulderL':'left_wing_root_armor','shoulderR':'right_wing_root_armor',
 'upperL':'left_inner_wing','upperR':'right_inner_wing','ventL':'left_blade_feathers','ventR':'right_blade_feathers','left':'left_furnace_cannon','right':'right_furnace_cannon',
 'thighL':'left_haunch','thighR':'right_haunch','footL':'left_talon','footR':'right_talon','flareL':'left_fire_tail','flareR':'right_fire_tail'}
art={'parts':{},'identity':'Corrupted Fire Phoenix','sourceJob':'a3ed4f8a-edd3-49c0-8ba3-479f887a287f','muzzles':{'left':[108,172],'right':[212,172]}}
rebuilt=np.zeros((320,320,4),np.uint8);sheet=Image.new('RGB',(1280,1750),'#10101b');g=ImageDraw.Draw(sheet)
for i,name in enumerate(anchors):
 a=np.zeros_like(raw);sel=lab==name;a[sel]=raw[sel];part=Image.new('RGBA',(320,320));part.alpha_composite(Image.fromarray(a),(32,32));assert part.getbbox(),name
 p=D/(names[name]+'.png');part.save(p,optimize=True);rebuilt=np.maximum(rebuilt,np.asarray(part))
 art['parts'][name]=dict(key='vp23_phoenix_'+name,path=p.relative_to(R).as_posix(),w=320,h=320,pivot=[160,160],anchor=[v+32 for v in anchors[name]],owner=owners[name],bounds=list(part.getbbox()))
 x=i%4*320;y=i//4*350;sheet.paste(part,(x,y),part);g.text((x+8,y+322),names[name],fill='white')
master=Image.new('RGBA',(320,320));master.alpha_composite(im,(32,32));assert np.array_equal(np.asarray(master),rebuilt)
master.save(O/'phoenix-master.png');sheet.save(O/'components.png')
# Authored circular wing bearing, copied without drawing replacement material.
socket=Image.new('RGBA',(48,48));patch=im.crop((65,45,91,71));socket.alpha_composite(patch,(11,11));p=D/'wing_bearing.png';socket.save(p,optimize=True)
art['socket']=dict(key='vp23_phoenix_joint',path=p.relative_to(R).as_posix(),w=48,h=48,pivot=[24,24],anchor=[24,24],bounds=list(socket.getbbox()))
old=(R/'assets/dracodia_volcano_art_1019.js').read_text();previous=json.loads(old[old.index('{'):old.rindex(';')]);art['flame']=previous['flame']
# New physical skull replaces the old robot in BOTH assembled and detached states.
head=Image.new('RGBA',(128,128));head.alpha_composite(im.crop((108,52,149,98)),(44,39));head.save(S/'head-reference.png')
art['head']={'banks':{'charge':[],'spin':[]}}
eyes=[[58,59],[70,59]]
source=np.array(head);eyemask=np.zeros((128,128),bool);hy,hx=np.indices((128,128))
for x,y in eyes:eyemask|=((hx-x)**2+(hy-y)**2<=5**2)
eyemask&=(source[:,:,3]>0)
chargefile=S/'head-charge.png'
generated=Image.open(chargefile).convert('RGBA') if chargefile.exists() else head
gen=np.array(generated)
for bank,count in [('charge',16),('spin',32)]:
 for i in range(count):
  angle=i*math.tau/count if bank=='spin' else 0
  pose=head.copy()
  if bank=='charge':
   arr=source.copy();u=i/15;arr[eyemask,:3]=np.round(source[eyemask,:3]*(1-u)+gen[eyemask,:3]*u).astype(np.uint8);pose=Image.fromarray(arr)
  if bank=='spin':pose=pose.rotate(-math.degrees(angle),Image.Resampling.NEAREST,center=(64,64))
  pts=[[round(64+(x-64)*math.cos(angle)-(y-64)*math.sin(angle),4),round(64+(x-64)*math.sin(angle)+(y-64)*math.cos(angle),4)] for x,y in eyes]
  p=D/f'head_{bank}_{i:02}.png';pose.save(p,optimize=True);art['head']['banks'][bank].append(dict(key=f'vh19_{bank}_phoenix_{i:02}',path=p.relative_to(R).as_posix(),w=128,h=128,pivot=[64,64],bounds=list(pose.getbbox()),eyes=pts,angle=angle))
for name in ['feather','plume','beam']:
 p=S/(name+'.png')
 if p.exists():
  a=Image.open(p).convert('RGBA');out=D/(name+'.png');a.save(out,optimize=True);art[name]=dict(key='ph20_'+name,path=out.relative_to(R).as_posix(),w=a.width,h=a.height,pivot=[a.width/2,a.height/2],bounds=list(a.getbbox()))
# One PixelLab clip supplies coordinated wing feathers, tail fire and the
# furnace charge. Each pose retains the same320 canvas and anatomical pivots.
art['motion']={}
for name in ['upperL','upperR','ventL','ventR','reactor','flareL','flareR']:
 bank=[]
 for i in range(9):
  file=S/'wing-charge'/f'{i:02}.png'
  if not file.exists():break
  arr=np.array(Image.open(file).convert('RGBA'));arr[lab!=name]=0;pose=Image.new('RGBA',(320,320));pose.alpha_composite(Image.fromarray(arr),(32,32));p=D/f'{names[name]}_{i:02}.png';pose.save(p,optimize=True)
  bank.append({**art['parts'][name],'key':f'vp23_phoenix_{name}_{i:02}','path':p.relative_to(R).as_posix(),'bounds':list(pose.getbbox())})
 if len(bank)==9:art['motion'][name]=bank
for name,job in [('plume','8fae5f5b-d5fd-4b27-b977-789be6c7420b'),('beam','84fa5caa-2910-42de-8cf7-2bc8469ae631')]:
 frames=[]
 for i in range(16):
  folder='beam-motion-clean' if name=='beam' and (S/'beam-motion-clean').exists() else name+'-motion'
  file=S/folder/f'{i+1:02}.png'
  if not file.exists():break
  pose=Image.open(file).convert('RGBA');p=D/f'{name}_{i:02}.png';pose.save(p,optimize=True);frames.append(dict(key=f'ph20_{name}_{i:02}',path=p.relative_to(R).as_posix(),w=pose.width,h=pose.height,pivot=[pose.width/2,pose.height/2],bounds=list(pose.getbbox())))
 if len(frames)==16:
  art[name]['frames']=frames;art[name]['job']=job if name!='beam' or folder!='beam-motion-clean' else '344bdb15-4628-4260-8190-438a67737b3f'
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n')
(R/'assets/dracodia_phoenix_art_1020.js').write_text('"use strict";\n// Owned by build_dracodia_phoenix_1020.py. PixelLab-authored forward phoenix.\nconst PH20_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'provenance.json').write_text(json.dumps(dict(masterJob=art['sourceJob'],frontFacing=True,losslessReconstruction=True,canvas=[320,320],sourceCanvas=[256,256],padding=[32,32],parts=len(anchors),headChargeJob='01ab246b-e121-4006-9ef4-238e0d34d4d9',flapJob='40f92480-fd27-4286-b87e-db372e4e0298',plumeJob='6b1ca499-cabc-492f-9ba3-006b3c6cc2d5',featherJob='ac817c6c-04a2-4b0d-9731-b259ed949e24'),indent=2)+'\n')
tax=R/'assets/data/ART_TAXONOMY.json';taxonomy=json.loads(tax.read_text(encoding='utf-8-sig'))
for prefix,role,note in [('vp23_phoenix_','stage8_corrupted_phoenix_modules','Forward-facing PixelLab fire phoenix. Seventeen320-square lossless parts and nine coordinated poses; fixed anatomical pivots.'),('ph20_','stage8_corrupted_phoenix_attacks','PixelLab molten feather, sixteen muzzle blooms and sixteen continuous beam heat-pulse frames.'),('vh19_charge_phoenix_','stage8_phoenix_head_charge','Sixteen eye-only charge states on a fixed128-square canvas; physical eye sockets.'),('vh19_spin_phoenix_','stage8_phoenix_head_turn','Thirty-two fixed-pivot turns of the new PixelLab phoenix skull; matching eye sockets.')]:taxonomy[prefix]={'role':role,'sheet':None,'note':note+' Owner build_dracodia_phoenix_1020.py / dracodia_phoenix_1020.js.'}
tax.write_text(json.dumps(taxonomy,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(parts=len(anchors),headFrames=48,reconstructsMaster=True,bytes=sum(p.stat().st_size for p in D.glob('*.png')))),flush=True)
