"""Authored fixed-unit clips and 9-sliced generated HUD. Original sources retained."""
from pathlib import Path
import json,statistics,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects
R=Path(__file__).resolve().parents[3]
prefix=(R/'expansion/topdown/_research/build_bastion19.py').read_text(encoding='utf-8').split("room=load('room')")[0]
prefix=prefix.replace("  elif mode=='center':cy=q.height/2", "  elif mode=='jump_root':\n   white=mask&(a[:,:,0]>140)&(abs(a[:,:,0].astype(int)-a[:,:,1].astype(int))<30)&(abs(a[:,:,0].astype(int)-a[:,:,2].astype(int))<35);white[int(q.height*.27):]=False;yy,xx=np.where(white)\n   if len(xx):cx=float(np.median(xx));cy=float(np.median(yy))+126/s if i in (2,3,4) else q.height\n  elif mode=='helmet_root':\n   white=mask&(a[:,:,0]>140)&(abs(a[:,:,0].astype(int)-a[:,:,1].astype(int))<30)&(abs(a[:,:,0].astype(int)-a[:,:,2].astype(int))<35);white[int(q.height*.27):]=False;yy,xx=np.where(white)\n   assert len(xx),(prefix,i,'missing helmet root')\n   cx=float(np.median(xx));cy=float(np.median(yy))+126/s\n  elif mode=='heart_root':\n   heart=mask&(a[:,:,0]>245)&(a[:,:,1]>235)&(a[:,:,2]>160);heart[:int(q.height*.3)]=False;heart[int(q.height*.55):]=False;heart[:,:int(q.width*.5)]=False;heart[:,int(q.width*.8):]=False\n   labs,num=label(heart);counts=np.bincount(labs.ravel());counts[0]=0;idx=int(counts.argmax());yy,xx=np.where(labs==idx)\n   assert idx>0 and len(xx),(prefix,i,'missing diamond heart root')\n   cx=float(np.median(xx))-28/s;cy=float(np.median(yy))+112/s\n  elif mode=='center':cy=q.height/2")
exec(prefix.replace('bastion19','bastion20'))
D['version']='1014-gosfer20-r1'
def single_set(stem):return [cuts(stem+'_'+str(i),1,1)[0]for i in range(8)]
def sockets(keys,front=False):
 for k in keys:
  im=Image.open(F/(k+'.png'));ar=np.array(im);a=D['assets'][k]['anchor'];bb=im.getbbox();mask=(ar[:,:,3]>0)&(ar[:,:,0]>220)&(ar[:,:,1]>65)&(ar[:,:,1]<225)&(ar[:,:,2]<100);mask[:bb[1]+int((bb[3]-bb[1])*.26)]=False;mask[a[1]-int((bb[3]-bb[1])*.38):]=False
  if front:mask[:,:a[0]-20]=False;mask[:,a[0]+20:]=False
  labs,n=label(mask);items=[]
  for j,sl in enumerate(find_objects(labs),1):
   if sl is None:continue
   yy,xx=np.where(labs==j)
   if len(xx)>=2:items.append((len(xx),float(np.median(xx)),float(np.median(yy))))
  if items:
   q=max(items,key=lambda q:q[0]if front else q[1]);D['assets'][k]['muzzle']=[round(q[1]),round(q[2])]
pp=single_set('gwalk');s=144/statistics.median(q.height for q,b in pp);keys=bank('gwalk_single','pb20_gosfer_walk',pp,(384,384),(192,346),s,'helmet',fps=14);sockets(keys)
pp=cuts('gsouth',4,2);s=144/statistics.median(q.height for q,b in pp);keys=bank('gsouth','pb20_gosfer_walk_south',pp,(384,384),(192,346),s,'helmet',fps=14);sockets(keys)
pp=cuts('gfire',8,2);s=144/statistics.median(q.height for q,b in pp)
for i,n in enumerate(['south','angle']):
 s=144/statistics.median(q.height for q,b in pp[i*8:i*8+8]);keys=bank('gfire','pb20_gosfer_fire_'+n,pp[i*8:i*8+8],(384,384),(192,346),s,'helmet',fps=22);sockets(keys,n=='south')
pp=cuts('gaction',4,4);s=144/statistics.median(q.height for q,b in pp[:8]);bank('gaction','pb20_gosfer_roll',pp[8:],(384,384),(192,346),s,'feet',fps=15)
pp=cuts('gmotion',8,3);s=144/statistics.median(q.height for q,b in pp[8:16])
for i,n in enumerate(['run','strafe','jump']):keys=bank('gmotion','pb20_gosfer_'+n,pp[i*8:i*8+8],(384,384),(192,346),s,'helmet_root'if n=='run'else'jump_root'if n=='jump'else'helmet',fps=16);sockets(keys,n=='strafe')
pp=single_set('hrun');s=185/statistics.median(q.height for q,b in pp);bank('hrun_single','pb20_helios_run',pp,(384,384),(192,346),s,'heart_root',fps=16);alias('pb19_helios_run','pb20_helios_run')
pp=cuts('hmotion',8,2);s=210/statistics.median(q.height for q,b in pp[:8]);bank('hmotion','pb20_helios_walk',pp[:8],(384,384),(192,346),s,'feet',fps=14);bank('hmotion','pb20_helios_strafe',pp[8:],(384,384),(192,346),s,'feet',fps=14);alias('pb19_helios_walk','pb20_helios_walk');alias('pb19_helios_strafe','pb20_helios_strafe')
pp=cuts('ywall',8,4);s=88/pp[31][0].height
for i,n in enumerate(['wall_crouch','wall_prone','roll_prone','roll_stand']):bank('ywall','pb20_yuri_'+n,pp[i*8:i*8+8],(192,224),(96,160),s,'yuri',fps=16,muzzle='cyan')
pp=cuts('portraits',4,2,False);s=256/statistics.median(q.width for q,b in pp)
for i,n in enumerate(['yuri','gosfer']):bank('portraits','pb20_portrait_'+n,pp[i*4:i*4+4],(272,272),(136,136),s,'center',fps=6)
pp=cuts('hud',2,4,False)
def panel(i,n,size):
 q,b=pp[i];sc=(size[1]-4)/q.height;q=q.resize((round(q.width*sc),size[1]-4),Image.Resampling.NEAREST);out=Image.new('RGBA',size);cap=min(q.width//3,(size[0]-4)//3);out.alpha_composite(q.crop((0,0,cap,q.height)),(2,2));out.alpha_composite(q.crop((q.width-cap,0,q.width,q.height)),(size[0]-cap-2,2));mid=q.crop((cap,0,q.width-cap,q.height)).resize((size[0]-4-2*cap,q.height),Image.Resampling.NEAREST);out.alpha_composite(mid,(cap+2,2));save(n,out,(size[0]//2,size[1]//2),'hud',b,sc,{'nineSlice':{'left':cap,'right':cap,'top':5,'bottom':5}})
for i,n,size in [(0,'top',(624,58)),(1,'bottom',(624,44)),(2,'boss',(300,42)),(3,'dialogue',(362,96))]:panel(i,'pb20_hud_'+n,size)
for i,n in [(4,'portrait_player'),(5,'portrait_enemy')]:bank('hud','pb20_hud_'+n,[pp[i]],(144,144),(72,72),132/pp[i][0].width,'center')
im=load('hud');ia=np.array(im);il,ic=label((ia[:,:,3]>0)&(np.indices(ia.shape[:2])[0]>=round(im.height*.75)),np.ones((3,3)));components=[]
for j,sl in enumerate(find_objects(il),1):
 if sl is None:continue
 yy,xx=np.where(il==j)
 if len(xx)>25:components.append((min(7,int(float(np.median(xx))*8/im.width)),j))
for i,n in enumerate(['roll','prone','shield','retina','grenade','ammo','armor','cover']):
 ids=[j for group,j in components if group==i];q=im.copy();q.putalpha(Image.fromarray(np.isin(il,ids).astype('uint8')*255));bb=q.getbbox();x0=0;q=q.crop(bb);sc=48/max(q.size);out=Image.new('RGBA',(56,56));q=q.resize((round(q.width*sc),round(q.height*sc)),Image.Resampling.NEAREST);out.alpha_composite(q,((56-q.width)//2,(56-q.height)//2));save('pb20_icon_'+n,out,(28,28),'hud',(x0+bb[0],bb[1],x0+bb[2],bb[3]),sc)
pp=cuts('gfx',4,4,False);sc=200/statistics.median(q.height for q,b in pp[:8]);bank('gfx','pb20_gosfer_shield',pp[:8],(256,256),(128,128),sc,'center',fps=16);sc=212/statistics.median(q.height for q,b in pp[8:]);bank('gfx','pb20_gosfer_lightning',pp[8:],(256,256),(128,128),sc,'center',fps=18)
for path in S.glob('*.png'):D['sources'][path.name]={'size':list(Image.open(path).size),'sha12':hashlib.sha256(path.read_bytes()).hexdigest()[:12]}
(O/'manifest.json').write_text(json.dumps(D,indent=2)+'\n',encoding='utf-8',newline='\n');(O/'manifest.js').write_text('window.TD_BASTION20_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'assets':len(D['assets']),'banks':len(D['sequences']),'sources':len(D['sources'])}))
