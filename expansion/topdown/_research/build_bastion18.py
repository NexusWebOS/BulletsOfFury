"""Own the new authored Bastion/Gosfer/controller assets and manifests.

Original imagegen art is preserved. Export only isolates connected figures,
normalizes alpha, registers physical roots, scales proportionally and pads.
"""
from pathlib import Path
import json,hashlib,statistics
import numpy as np
from scipy.ndimage import label,find_objects
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/bastion18';SRC=OUT/'source';FR=OUT/'frames';QA=ROOT/'_shots/bastion18'
for p in (FR,QA):p.mkdir(parents=True,exist_ok=True)
D={'version':'1013-bastion18-r1','assets':{},'sequences':{},'audit':[],'sources':{}}

def load(name):
 im=Image.open(SRC/(name+'.png')).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));return im

def cuts(name,cols,rows,actors=False):
 im=load(name);a=np.array(im);labs,n=label(a[:,:,3]>0,np.ones((3,3)));counts=np.bincount(labs.ravel());sl=find_objects(labs)
 if name in ('wall_wide','wall_after'):
  occupied=(a[:,:,3]>0).sum(axis=1)>2;spans=[];start=None;last=None
  for y,on in enumerate(occupied):
   if on:
    if start is None:start=y
    elif y-last>20:spans.append((start,last+1));start=y
    last=y
  if start is not None:spans.append((start,last+1))
  assert len(spans)==4,(name,spans)
  out=[]
  for y0,y1 in spans:
   q=im.crop((0,y0,im.width,y1));b=q.getbbox();out.append((q.crop(b),(b[0],y0+b[1],b[2],y0+b[3]),(b[0],b[1]),(im.width,y1-y0)))
  return out
 chunks=[]
 for i,box in enumerate(sl,1):
  if box is None or counts[i]<200:continue
  b=(box[1].start,box[0].start,box[1].stop,box[0].stop);cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2;idx=min(rows-1,int(cy*rows/im.height))*cols+min(cols-1,int(cx*cols/im.width));chunks.append((idx,int(counts[i]),i,b))
 out=[]
 for idx in range(cols*rows):
  rect=(round(idx%cols*im.width/cols),round(idx//cols*im.height/rows),round((idx%cols+1)*im.width/cols),round((idx//cols+1)*im.height/rows))
  if actors:
   candidates=[q for q in chunks if q[0]==idx];assert candidates,(name,idx,'no figure');_,_,lid,b=max(candidates,key=lambda q:q[1]);keep=[lid]
   # Include only nearby small detached effects, never a neighboring body.
   for _,ct,other,ob in chunks:
    if other!=lid and ct<700 and ob[0]>=b[0]-18 and ob[2]<=b[2]+18 and ob[1]>=b[1]-12 and ob[3]<=b[3]+12:keep.append(other)
   alpha=np.isin(labs,keep).astype('uint8')*255;q=Image.fromarray(a.copy());q.putalpha(Image.fromarray(alpha));b=q.getbbox();q=q.crop(b);origin=(b[0]-rect[0],b[1]-rect[1]);out.append((q,b,origin,(im.width/cols,im.height/rows)))
  else:
   q=im.crop(rect);b=q.getbbox();assert b,(name,idx);out.append((q.crop(b),(rect[0]+b[0],rect[1]+b[1],rect[0]+b[2],rect[1]+b[3]),(b[0],b[1]),(q.width,q.height)))
 return out

def save(key,im,anchor,source,rect,scale,extra=None):
 b=im.getbbox();assert b,key;assert all(v%2==0 for v in im.size)
 if key!='pb18_room':assert min(b[0],b[1],im.width-b[2],im.height-b[3])>=2,(key,b)
 f=FR/(key+'.png');im.save(f,optimize=True)
 D['assets'][key]={'file':f.relative_to(ROOT).as_posix(),'size':list(im.size),'anchor':list(anchor),'bounds':list(b),'drawScale':1,**(extra or {})}
 D['audit'].append({'key':key,'source':source+'.png','crop':list(rect),'scale':scale,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})

def bank(name,prefix,parts,cell,anchor,s,fps=12,center=False,source_root=False,jump=False,foot_target=None):
 keys=[]
 for i,(q,b,origin,grid)in enumerate(parts):
  cx=grid[0]/2-origin[0] if source_root else q.width/2
  cy=q.height/2 if center else q.height
  if jump:
   # Source uses two rows; keep intentional flight relative to grounded phase.
   ref=parts[0][2][1]+parts[0][0].height if i<4 else parts[-1][2][1]+parts[-1][0].height
   cy=ref-origin[1]
  w=max(2,round(q.width*s/2)*2);h=max(2,round(q.height*s/2)*2)
  q=q.resize((w//2,h//2),Image.Resampling.NEAREST).resize((w,h),Image.Resampling.NEAREST)
  root=foot_target or anchor;x=round(root[0]-cx*s);y=round(root[1]-cy*s)
  assert x>=2 and y>=2 and x+w<=cell[0]-2 and y+h<=cell[1]-2,(prefix,i,(x,y),(w,h),cell)
  im=Image.new('RGBA',cell);im.alpha_composite(q,(x,y));k=prefix+'_'+str(i);extra={}
  if jump:extra['jumpLiftBaked']=True
  if prefix.startswith('pb18_gosfer'):
   ar=np.array(im);red=(ar[:,:,0]>140)&(ar[:,:,0]>ar[:,:,1]*1.6)&(ar[:,:,3]>0);red[int(anchor[1]-(anchor[1]-im.getbbox()[1])*.35):]=False
   yy,xx=np.where(red);extra['muzzle']=[int(np.percentile(xx,97)) if len(xx) else anchor[0]+38,int(np.median(yy)) if len(yy) else anchor[1]-74]
  save(k,im,anchor,name,b,s,extra);keys.append(k)
 D['sequences'][prefix]={'frames':keys,'fps':fps,'drawScale':1,'rootContract':{'cell':list(cell),'anchor':list(anchor),'sourceScale':s,'unit':'common proportional body scale; registered feet/pelvis; authored flight'}}
 contact=Image.new('RGBA',(cell[0]*min(8,len(keys)),cell[1]*((len(keys)+7)//8)),(12,19,27,255));onion=contact.copy()
 for i,k in enumerate(keys):
  pos=((i%8)*cell[0],(i//8)*cell[1]);contact.alpha_composite(Image.open(FR/(k+'.png')),pos)
  for j,alpha in [((i-1)%len(keys),55),((i+1)%len(keys),55),(i,200)]:
   q=Image.open(FR/(keys[j]+'.png'));q.putalpha(q.getchannel('A').point(lambda a:a*alpha//255));onion.alpha_composite(q,pos)
 contact.convert('RGB').save(QA/(prefix+'_contact.png'));onion.convert('RGB').save(QA/(prefix+'_onion.png'));return keys

room=load('room');room=room.resize((320,240),Image.Resampling.NEAREST).resize((640,480),Image.Resampling.NEAREST);save('pb18_room',room,(320,240),'room',(0,0,*load('room').size),640/load('room').width)
wall=cuts('wall_wide',1,4);wall_after=cuts('wall_after',1,4);s=520/wall[0][0].width
bank('wall_wide','pb18_backwall',wall+wall_after,(896,480),(448,240),s,foot_target=(448,270))
# The source wall is wider than the black shell aperture. Fill the room end with
# its flat plate; matching machinery is mounted into actual authored sockets.
D['layout']={'rearFloor':270,'door':[320,250],'core':[318,139],'turrets':[[128,148],[512,148]],'aperture':[160,100,320,168],'wallDepth':4.8,'coverDepth':1.43,'horizon':190}

parts=cuts('machinery',4,4,True)
for prefix,group,width in [('pb18_door_core',parts[:8],66),('pb18_turret_gun',parts[8:12],60),('pb18_turret_laser',parts[12:],60)]:bank('machinery',prefix,group,(96,96),(48,48),width/max(p[0].width for p in group),center=True)
parts=cuts('props',4,4,True)
for prefix,group,cell,anchor,target in [('pb18_barrel',parts[:4],(96,112),(48,100),56),('pb18_barrel_blast',parts[4:8],(160,160),(80,148),120),('pb18_enemy_crate',parts[8:12],(112,128),(56,114),80),('pb18_armored_crate',parts[12:],(112,128),(56,114),80)]:bank('props',prefix,group,cell,anchor,target/max(p[0].width for p in group),fps=12)
ray=cuts('laser_ray',1,4)
bank('laser_ray','pb18_laser_ray',ray,(384,96),(192,48),284/max(p[0].width for p in ray),center=True,fps=16)
parts=cuts('master',4,4)
bank('master','pb18_master',parts,(288,320),(144,160),218/max(p[0].height for p in parts[:8]),center=True)

motion=cuts('helios_motion',4,4,True);hero_s=210/statistics.median(p[0].height for p in motion[:8])
bank('helios_motion','pb18_helios_walk',motion[:8],(320,352),(160,316),hero_s,source_root=True,fps=12)
bank('helios_motion','pb18_helios_run',motion[8:],(320,352),(160,316),hero_s,source_root=True,fps=16)
for name,a1,a2 in [('helios_attack','throw','lightning'),('helios_jump','jump','death'),('helios_idle','idle','hit')]:
 pp=cuts(name,4,4,True)
 bank(name,'pb18_helios_'+a1,pp[:8],(320,352),(160,316),hero_s,source_root=True,jump=a1=='jump',fps=14 if a1=='jump' else 12)
 bank(name,'pb18_helios_'+a2,pp[8:],(320,352),(160,316),hero_s,source_root=True,fps=10)

gw=cuts('gosfer_walk',8,4,True);robot_s=128/statistics.median(p[0].height for p in gw[:8])
for i,face in enumerate(['south','north','east','west']):bank('gosfer_walk','pb18_gosfer_walk_'+face,gw[i*8:(i+1)*8],(256,288),(128,260),robot_s,source_root=True,fps=12)
ga=cuts('gosfer_actions',8,4,True)
for i,action in enumerate(['fire_south','fire_east','dash_east','death']):bank('gosfer_actions','pb18_gosfer_'+action,ga[i*8:(i+1)*8],(256,288),(128,260),robot_s,source_root=True,fps=24 if action.startswith('fire') else 14)

pad=cuts('pads',1,2)
for i,name in enumerate(['m30','genesis']):bank('pads','pb18_pad_'+name,[pad[i]],(768,384),(384,192),680/pad[i][0].width,center=True,fps=0);D['assets']['pb18_pad_'+name]=D['assets']['pb18_pad_'+name+'_0']

for f in SRC.glob('*.png'):D['sources'][f.name]={'size':list(Image.open(f).size),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
for k,m in D['assets'].items():
 im=Image.open(ROOT/m['file']);assert set(np.array(im.getchannel('A')).ravel()).issubset({0,255});assert all(v%2==0 for v in im.size)
(OUT/'manifest.json').write_text(json.dumps(D,indent=2)+'\n',encoding='utf-8',newline='\n');(OUT/'manifest.js').write_text('window.TD_BASTION18_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'assets':len(D['assets']),'banks':len(D['sequences']),'sources':len(D['sources']),'heroScale':hero_s,'gosferScale':robot_s}))
