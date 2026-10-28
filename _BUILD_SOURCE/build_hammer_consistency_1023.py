from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import label
import numpy as np
import json, math, hashlib, shutil, sys

R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/hammer_consistency_1023' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Consistency-1023'
O=W/'shipping';O.mkdir(exist_ok=True)
UNIT=.13
master=Image.open(W/'weapon-master.png').convert('RGBA')
master=master.resize((round(master.width*UNIT),round(master.height*UNIT)),Image.Resampling.NEAREST)
HEAD=(round(334*UNIT),round(442*UNIT))
prop=Image.new('RGBA',(640,640));prop.alpha_composite(master,(320-HEAD[0],320-HEAD[1]))
A={'banks':{},'sheets':{},'version':1,'weaponSource':'weapon-master.png','weaponSourceUnit':UNIT,'headPivot':[320,320]}
rig=[]
CACHE={}
S={'combo':([0,316,658,925,1254],[315,648,925,1219],1),
   'sides':([0,327,633,942,1254],[326,632,940,1205],1),
   'throw':([0,375,722,1086],[374,721,1062],.83),
   'rage':([0,370,720,1086],[361,719,1070],.83)}
def red(im):
 a=np.array(im);v=a[:,:,:3].astype(float);hi=v.max(2);lo=v.min(2);m=(((v[:,:,2]>v[:,:,0]*1.15)&(v[:,:,2]>70))|((hi-lo<35)&(hi>24)&(hi<220))|((v[:,:,2]>v[:,:,1]*1.2)&(v[:,:,2]>35)))&(a[:,:,3]>0)
 value=np.maximum(hi,(v@np.array([.2126,.7152,.0722]))*1.4)
 for c,f in enumerate([1,.25,.29]):a[:,:,c][m]=np.clip(value[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def body(name,i):
 if name not in CACHE:
  im=Image.open(W/(name+'.png')).convert('RGBA');ar=np.array(im);groups,_=label(ar[:,:,3]>20,structure=np.ones((3,3)));sizes=np.bincount(groups.ravel());parts=[]
  for z in np.flatnonzero(sizes>3500):
   if not z:continue
   yy,xx=np.where(groups==z);parts.append((int(z),(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1),float(xx.mean())))
  CACHE[name]=(im,ar,groups,parts)
 im,ar,groups,parts=CACHE[name];ys,feet,unit=S[name];r,c=divmod(i,4);cx=(c+.5)*im.width/4
 z,box,_=min(parts,key=lambda q:abs(q[1][3]-feet[r])*2+abs(q[2]-cx));x0,y0,x1,y1=box
 data=ar[y0:y1,x0:x1].copy();data[:,:,3][groups[y0:y1,x0:x1]!=z]=0;crop=Image.fromarray(data);crop=crop.resize((round(crop.width*unit),round(crop.height*unit)),Image.Resampling.NEAREST)
 out=Image.new('RGBA',(640,640));out.alpha_composite(crop,(round(320+(x0-cx)*unit),round(478+(y0-feet[r])*unit)))
 def point(p):return (round(320+(p[0]-cx)*unit),round(478+(p[1]-feet[r])*unit))
 return out,point

# Authored hand mounts, in untouched source-sheet coordinates. They are NOT
# silhouette-fitting scales. The same rigid prop unit is used for every pose.
M={
 'combo':{0:([(140,233),(247,182)],-26),2:([(756,70),(833,70)],0),3:([(1041,34),(1130,68)],20),4:([(173,354),(154,421)],106),6:([(812,520),(811,494)],-90),7:([(1121,523),(1118,496)],-90),9:([(390,703),(518,752)],21),10:([(782,769),(837,781)],12),11:([(1027,745),(1085,752)],7)},
 'sides':{0:([(100,45),(166,69)],20),1:([(449,111),(484,163)],56),2:([(749,133),(902,190)],20),3:([(1094,193),(1149,197)],4),4:([(110,479),(159,488)],10),5:([(449,480),(498,486)],7),6:([(777,522),(824,527)],6),8:([(131,706),(201,681)],-20),9:([(385,814),(453,840)],21),10:([(780,798),(838,790)],-8),11:([(1094,800),(1155,813)],12),12:([(175,1033),(219,1042)],12),13:([(443,1021),(494,1047)],27),14:([(825,1074),(866,1096)],28),15:([(1074,1121),(1180,1067)],-27)},
 'throw':{0:([(166,266),(273,213)],-26),1:([(600,197),(661,197)],0),2:([(906,76),(1004,101)],14),3:([(1247,74),(1333,84)],7),4:([(167,503),(249,543)],26)},
 'rage':{3:([(1227,274),(1326,214)],-31),4:([(165,595),(270,548)],-24),5:([(533,598),(639,550)],-24),6:([(895,599),(1002,548)],-25),7:([(1258,598),(1362,552)],-24)}
}
def mount(name,i,flip=False,weapon=True,colored=False):
 im,point=body(name,i);hands=[];angle=0;head=(320,430)
 if weapon:
  raw,angle=M[name][i];hands=[point(p) for p in raw];g=(sum(p[0] for p in hands)/len(hands),sum(p[1] for p in hands)/len(hands));a=math.radians(angle);head=(round(g[0]-110*math.cos(a)),round(g[1]-110*math.sin(a)))
  turn=prop.rotate(-angle,resample=Image.Resampling.NEAREST,center=(320,320));out=im.copy();out.alpha_composite(turn,(head[0]-320,head[1]-320))
  # Foreground glove cutouts are authored body pixels, keeping the rigid shaft
  # inside the fingers. This is baked into the whole actor, never a live rig.
  for x,y in hands:
   b=(x-13,y-12,x+14,y+13);p=im.crop(b);out.alpha_composite(p,(b[0],b[1]))
  im=out
 if colored:im=red(im)
 if flip:im=ImageOps.mirror(im);head=(639-head[0],head[1]);hands=[(639-x,y) for x,y in hands];angle=180-angle
 # Store the actual bottom of the rotated striking head, not a nominal circle.
 headOnly=Image.new('RGBA',prop.size);headOnly.alpha_composite(master.crop((0,0,round(535*UNIT),master.height)),(320-HEAD[0],320-HEAD[1]));bb=headOnly.rotate(-angle,Image.Resampling.NEAREST,center=(320,320)).getbbox();contact=[head[0],head[1]+bb[3]-320-1]
 row={'source':name,'sourceFrame':i,'head':list(head),'contact':contact,'hands':hands,'angle':angle,'unit':UNIT,'armed':weapon,'flip':flip}
 return im,row
def emit(name,frames,tool=False):
 rows=[];sheet=Image.new('RGBA',(640*4,640*math.ceil(len(frames)/4)));hit=sheet.copy()
 for i,(im,meta) in enumerate(frames):
  box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<640,(name,i,box)
  x,y=i%4*640,i//4*640;sheet.alpha_composite(im,(x,y));wh=Image.new('RGBA',im.size,'white');wh.putalpha(im.getchannel('A'));hit.alpha_composite(wh,(x,y));prefix='hf22_' if tool else 'ha21_hc23_';pivot=[320,320] if tool else [320,354];head=meta['head'];tip=meta.get('contact',head) if 'jump' in name and i in [7,8] else head
  row={'key':prefix+name+'_'+str(i),'sheet':'hc23_'+name,'cell':[x,y,640,640],'w':640,'h':640,'pivot':pivot,'bounds':list(box),'tip':tip,'glow':head,'white':prefix+name+'_hit_'+str(i),'kind':'corrupt','bank':name,'frame':i,'_hf22':True,'_hc23':True,'weaponUnit':UNIT,'armed':meta.get('armed',True)};rows.append(row);rig.append(dict(bank=name,frame=i,**meta))
 for suffix,img in [('',sheet),('_hit',hit)]:
  p=O/(name+suffix+'.webp');img.save(p,lossless=True,exact=True,method=5);A['sheets']['hc23_'+name+suffix]={'key':'nca_hc23_'+name+suffix,'path':'assets/game/shared/combat/hammer_consistency_1023/'+p.name,'w':img.width,'h':img.height,'legacy':False}
 A['banks'][name]=rows

# Keep existing sequence clocks/counts. Only authored frames/mounts change.
jump=[mount('combo',0),mount('throw',1),mount('throw',2),mount('combo',2),mount('combo',3),mount('combo',4),mount('combo',6),mount('combo',7),mount('combo',6),mount('combo',0),mount('combo',0)]
left=[mount('sides',8),mount('combo',2),mount('throw',1),mount('sides',3,True),mount('sides',4),mount('sides',5),mount('sides',6),mount('sides',6)]
right=[mount('sides',0),mount('combo',3),mount('throw',1,True),mount('sides',3),mount('sides',4,True),mount('sides',5,True),mount('sides',6,True)]
sides=left+right+[mount('combo',0)]
throws=[mount('throw',i,weapon=i<5) for i in range(8)]
for name,frames in [('corrupt_jump',jump),('corrupt_sides',sides),('corrupt_throw',throws)]:
 emit(name,frames);emit(name+'_red',[(red(im),meta) for im,meta in frames])
# Rage's existing code/aura body art is retained, but its five armed poses use
# the exact same weapon source and unit, coloured offline from that source.
rage=[]
for i in [0,3,4,5,6,7,8,9,10,11]:
 if i in M['rage']:
  im,meta=mount('rage',i); # body already red; only purple prop needs red palette
  im=red(im)
 elif i==0:
  im,point=body('rage',i);parked=prop.rotate(0);at=(205,430);im.alpha_composite(red(parked),(at[0]-320,at[1]-320));meta={'source':'rage','sourceFrame':i,'head':list(at),'hands':[],'angle':0,'unit':UNIT,'armed':True,'parked':True}
 else:im,meta=mount('rage',i,weapon=False)
 rage.append((im,meta))
emit('corrupt_rage',rage)
turns=[]
for i in range(32):turns.append((prop.rotate(-i*360/32,resample=Image.Resampling.NEAREST,center=(320,320)),{'source':'weapon-master','head':[320,320],'unit':UNIT,'angle':i*360/32,'armed':True}))
emit('corrupt_tool',turns,True);emit('corrupt_tool_red',[(red(im),meta) for im,meta in turns],True)
# Generic armed action banks point to the same baked rig; no runtime assembly.
# Destruction keeps that head/core, then leaves the unarmed fire owner alone.
broken=[]
for i in range(6):
 im,point=body('throw',7);hand=point((1232,582));head=(hand[0]-20+(i%2),hand[1]-3);stub=master.crop((0,0,HEAD[0]+72,master.height));im.alpha_composite(stub,(head[0]-HEAD[0],head[1]-HEAD[1]));glove=body('throw',7)[0].crop((hand[0]-14,hand[1]-12,hand[0]+14,hand[1]+13));im.alpha_composite(glove,(hand[0]-14,hand[1]-12));broken.append((im,{'source':'weapon-master','sourceFrame':i,'head':list(head),'unit':UNIT,'hands':[hand],'armed':True,'broken':True}))
for name,frames in [('corrupt_hold',[mount('combo',0)]),('corrupt_spin_fixed',sides[:-1]),('corrupt_break_fixed',[mount('combo',0),mount('sides',3),mount('combo',6)]+broken)]:
 emit(name,frames);emit(name+'_red',[(red(im),meta) for im,meta in frames])
(W/'hammer_consistency_art_1023.js').write_text('"use strict";\nconst HC23_ART='+json.dumps(A,separators=(',',':'))+';\nObject.assign(HF22_ART.banks,HC23_ART.banks);Object.assign(HF22_ART.sheets,HC23_ART.sheets);\n',encoding='utf-8')
manifest={'owner':'_BUILD_SOURCE/build_hammer_consistency_1023.py','source':'_ART_SOURCES/hammer_consistency_1023','unit':UNIT,'weaponHeadPivot':HEAD,'banks':{n:len(r) for n,r in A['banks'].items()},'sources':{n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in ['combo.png','sides.png','throw.png','rage.png','weapon-master.png']},'sheets':[dict(v,sha256=hashlib.sha256((O/Path(v['path']).name).read_bytes()).hexdigest()) for v in A['sheets'].values()]}
(W/'manifest.json').write_text(json.dumps(manifest,indent=2));(W/'rig.json').write_text(json.dumps(rig,indent=2))
for name in ['corrupt_jump','corrupt_sides','corrupt_throw','corrupt_rage']:
 frames=[];c=Image.new('RGB',(640*4,670*math.ceil(len(A['banks'][name])/4)),'#13202c');d=ImageDraw.Draw(c)
 for i,a in enumerate(A['banks'][name]):
  x,y,w,h=a['cell'];im=Image.open(O/(name+'.webp')).crop((x,y,x+w,y+h));c.paste(im,(i%4*640,i//4*670),im);d.text((i%4*640+5,i//4*670+642),str(i),fill='white');f=Image.new('RGB',(640,640),'#13202c');f.paste(im,(0,0),im);frames.append(f)
 c.thumbnail((1280,1400));c.save(W/(name+'-contact.png'));frames[0].save(W/(name+'.gif'),save_all=True,append_images=frames[1:],duration=100,loop=0)
print(json.dumps({'banks':len(A['banks']),'frames':sum(len(b) for b in A['banks'].values()),'weaponSources':1}))
if '--install' in sys.argv:
 target=R/'assets/game/shared/combat/hammer_consistency_1023';target.mkdir(exist_ok=True)
 for p in O.glob('*.webp'):shutil.copy2(p,target/p.name)
 shutil.copy2(W/'manifest.json',target/'manifest.json')
 for n in ['hammer_consistency_art_1023.js','hammer_consistency_1023.js']:shutil.copy2(W/n,R/'assets'/n)
 p=R/'index.html';data=p.read_bytes()
 if b'hammer_consistency_art_1023.js' not in data:data=data.replace(b'<script src="assets/hammer_furious_1022.js',b'<script src="assets/hammer_consistency_art_1023.js?v=hc23-2"></script>\n<script src="assets/hammer_furious_1022.js').replace(b'</body>',b'<script src="assets/hammer_consistency_1023.js?v=hc23-2"></script>\n</body>');p.write_bytes(data)
 print('Installed Stage8-only rigid hammer frames; Stage5 unchanged.')
