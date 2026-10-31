"""Export the 1014 authored ground art, keeping original sheets and root metadata.
No limb assembly, synthetic inbetweens, per-frame fitting or painted sprites.
"""
from pathlib import Path
import json,hashlib,statistics
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects
R=Path(__file__).resolve().parents[3];O=R/'expansion/topdown/art/bastion19';S=O/'source';F=O/'frames';Q=R/'_shots/bastion19/art';F.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
D={'version':'1014-bastion19-r1','assets':{},'sequences':{},'sources':{},'audit':[]}
def load(n):
 im=Image.open(S/(n+'.png')).convert('RGBA');im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));return im
def cuts(n,cols,rows,actor=True):
 im=load(n);ar=np.array(im);lab,num=label(ar[:,:,3]>0,np.ones((3,3)));counts=np.bincount(lab.ravel());pieces=[]
 for k,sl in enumerate(find_objects(lab),1):
  if sl is None or counts[k]<150:continue
  b=(sl[1].start,sl[0].start,sl[1].stop,sl[0].stop);w=b[2]-b[0];h=b[3]-b[1]
  if actor and (w/h>6 or h/w>9 or h>im.height/rows*1.35):continue
  idx=min(rows-1,int((b[1]+b[3])/2*rows/im.height))*cols+min(cols-1,int((b[0]+b[2])/2*cols/im.width));pieces.append((idx,int(counts[k]),k,b))
 out=[]
 for i in range(cols*rows):
  if actor:
   picks=[x for x in pieces if x[0]==i]
   if not picks and n=='yuri_crawl':out.append(None);continue
   assert picks,(n,i,'missing actor');main=max(picks,key=lambda x:x[1]);ids=[main[2]];b=main[3]
   for _,ct,k,z in picks:
    if k!=main[2] and ct<400 and z[0]>=b[0]-12 and z[2]<=b[2]+12 and z[1]>=b[1]-12 and z[3]<=b[3]+12:ids.append(k)
   q=Image.fromarray(ar.copy());q.putalpha(Image.fromarray(np.isin(lab,ids).astype('uint8')*255));b=q.getbbox();q=q.crop(b)
  else:
   box=(round(i%cols*im.width/cols),round(i//cols*im.height/rows),round((i%cols+1)*im.width/cols),round((i//cols+1)*im.height/rows));q=im.crop(box);bb=q.getbbox();assert bb,(n,i);q=q.crop(bb);b=(box[0]+bb[0],box[1]+bb[1],box[0]+bb[2],box[1]+bb[3])
  out.append((q,b))
 return out
def save(k,im,anchor,n,b,s,extra=None):
 assert all(v%2==0 for v in im.size);bb=im.getbbox();assert bb,k
 if k!='pb19_room':assert min(bb[0],bb[1],im.width-bb[2],im.height-bb[3])>=2,(k,bb)
 path=F/(k+'.png');im.save(path,optimize=True);D['assets'][k]={'file':path.relative_to(R).as_posix(),'size':list(im.size),'anchor':list(anchor),'bounds':list(bb),'drawScale':1,**(extra or {})}
 D['audit'].append({'key':k,'source':n+'.png','sourceRect':list(b),'commonScale':s,'sha12':hashlib.sha256(path.read_bytes()).hexdigest()[:12]})
def bank(n,prefix,pp,cell,anchor,s,mode='feet',fps=12,flip_indices=(),muzzle=None):
 keys=[]
 for i,(q,b)in enumerate(pp):
  if i in flip_indices:q=q.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  a=np.array(q);mask=a[:,:,3]>0;cx=q.width/2;cy=q.height
  if mode in ('yuri','yuri_prone'):
   red=mask&(a[:,:,0]>70)&(a[:,:,0]>a[:,:,1]*1.6)&(a[:,:,0]>a[:,:,2]*1.25);red[int(q.height*.65):]=False;yy,xx=np.where(red)
   if len(xx):cx=float(np.median(xx))
   if mode=='yuri_prone':cy=float(np.median(yy)) if len(yy) else q.height*.5
  elif mode=='helmet':
   white=mask&(a[:,:,0]>140)&(abs(a[:,:,0].astype(int)-a[:,:,1].astype(int))<30)&(abs(a[:,:,0].astype(int)-a[:,:,2].astype(int))<35);white[int(q.height*.27):]=False;yy,xx=np.where(white)
   if len(xx):cx=float(np.median(xx))
  elif mode=='center':cy=q.height/2
  elif mode=='reactor':
   white=mask&(a[:,:,0]>190)&(a[:,:,1]>215)&(a[:,:,2]>215);yy,xx=np.where(white)
   if len(xx):cx=float(np.median(xx));cy=float(np.median(yy))
  w=round(q.width*s);h=round(q.height*s);q=q.resize((w,h),Image.Resampling.NEAREST);x=round(anchor[0]-cx*s);y=round(anchor[1]-cy*s)
  assert x>=2 and y>=2 and x+w<=cell[0]-2 and y+h<=cell[1]-2,(prefix,i,(x,y,w,h),cell)
  im=Image.new('RGBA',cell);im.alpha_composite(q,(x,y));extra={}
  ar=np.array(im);valid=ar[:,:,3]>0
  if muzzle in ('cyan','cyan_tip'):
   mm=valid&(ar[:,:,1]>140)&(ar[:,:,2]>140)&(ar[:,:,0]<ar[:,:,1]*.85);yy,xx=np.where(mm)
   if len(xx):
    take=xx>=np.percentile(xx,95) if muzzle=='cyan_tip' else np.ones(len(xx),dtype=bool);extra['muzzle']=[round(float(np.median(xx[take]))),round(float(np.median(yy[take])))]
  elif muzzle=='orange':
   mm=valid&(ar[:,:,0]>190)&(ar[:,:,1]>20)&(ar[:,:,0]>ar[:,:,1]*1.10)&(ar[:,:,2]<75);mm[int(anchor[1]-(anchor[1]-im.getbbox()[1])*.38):]=False;yy,xx=np.where(mm)
   if len(xx):
    take=xx>=np.percentile(xx,95);extra['muzzle']=[round(float(np.median(xx[take]))),round(float(np.median(yy[take])))]
  if prefix.startswith('pb19_helios_throw'):
   mm=valid&(ar[:,:,0]>225)&(ar[:,:,1]>190)&(ar[:,:,2]<190);yy,xx=np.where(mm);keep=xx>anchor[0]+20
   if keep.any():extra['emitter']=[int(np.percentile(xx[keep],90)),int(np.median(yy[keep]))]
  k=prefix+'_'+str(i);save(k,im,anchor,n,b,s,extra);keys.append(k)
 D['sequences'][prefix]={'frames':keys,'fps':fps,'drawScale':1,'rootContract':{'cell':list(cell),'anchor':list(anchor),'sourceScale':s,'method':mode,'unit':'whole authored figures; shared scale and physical root; no per-frame resizing'}}
 ct=Image.new('RGBA',(cell[0]*min(8,len(keys)),cell[1]*((len(keys)+7)//8)),(15,20,27,255));on=ct.copy()
 for i,k in enumerate(keys):
  pos=((i%8)*cell[0],(i//8)*cell[1]);im=Image.open(F/(k+'.png'));ct.alpha_composite(im,pos)
  for j,alpha in [((i-1)%len(keys),45),((i+1)%len(keys),45),(i,190)]:
   z=Image.open(F/(keys[j]+'.png'));z.putalpha(z.getchannel('A').point(lambda a:a*alpha//255));on.alpha_composite(z,pos)
 ct.convert('RGB').save(Q/(prefix+'_contact.png'));on.convert('RGB').save(Q/(prefix+'_onion.png'))
 # A native-sized animation deliverable allows honest visual motion review.
 ims=[]
 for k in keys:
  z=Image.new('RGBA',cell,(15,20,27,255));z.alpha_composite(Image.open(F/(k+'.png')));ims.append(z.convert('RGB'))
 ims[0].save(Q/(prefix+'.webp'),save_all=True,append_images=ims[1:],duration=round(1000/max(1,fps)),loop=0,lossless=True)
 return keys
def alias(old,new):D['sequences'][old]=D['sequences'][new]
def asset_alias(old,new):D['assets'][old]=D['assets'][new]
def unit_scale(pp,height,indices=None):return height/statistics.median(pp[i][0].height for i in (indices or range(len(pp))))
room=load('room').resize((320,240),Image.Resampling.NEAREST).resize((640,480),Image.Resampling.NEAREST);save('pb19_room',room,(320,240),'room',(0,0,*load('room').size),640/load('room').width);asset_alias('pb18_room','pb19_room')
pp=cuts('backwall_final',4,2,False);s=176/pp[0][0].width;bank('backwall_final','pb19_backwall',pp,(256,208),(128,190),s);alias('pb18_backwall','pb19_backwall')
for i in range(8):asset_alias('pb18_backwall_'+str(i),'pb19_backwall_'+str(i))
pp=cuts('reactor',4,4,False);bank('reactor','pb19_reactor',pp,(288,336),(144,174),.71,mode='reactor',fps=12);alias('pb18_master','pb19_reactor')
pp=cuts('cover_props_clean',4,4,False);s=156/pp[0][0].width
bank('cover_props_clean','pb19_cover',pp[:8],(192,128),(96,116),s)
bank('cover_props_clean','pb19_enemy_wall',[pp[i]for i in[0,3,5,7]],(112,96),(56,86),s*72/156)
alias('pb17_enemy_cover_wall','pb19_enemy_wall')
for i,j in enumerate([0,3,5,7]):asset_alias('pb16_wall_'+str(i),'pb19_cover_'+str(j))
bank('cover_props_clean','pb19_barrel',pp[8:12],(80,96),(40,86),48/pp[8][0].height);alias('pb18_barrel','pb19_barrel')
bank('cover_props_clean','pb19_crate',pp[12:],(112,96),(56,86),72/pp[12][0].width);alias('pb18_enemy_crate','pb19_crate');alias('pb18_armored_crate','pb19_crate')
pp=cuts('machinery',4,4,False)
for pre,group,width,old in [('core',pp[:8],30,'pb18_door_core'),('turret_gun',pp[8:12],30,'pb18_turret_gun'),('turret_laser',pp[12:],30,'pb18_turret_laser')]:bank('machinery','pb19_'+pre,group,(64,64),(32,32),width/group[0][0].width,'center');alias(old,'pb19_'+pre)
pp=cuts('prism_fx',4,4)
for pre,group,cell,anchor,scale_,mode in [('orb',pp[:4],(80,80),(40,40),48/pp[0][0].width,'center'),('warning',pp[4:8],(128,160),(64,146),84/pp[4][0].width,'feet'),('geyser',pp[8:12],(160,224),(80,210),170/max(x[0].height for x in pp[8:12]),'feet'),('lightning',pp[12:],(320,224),(160,112),250/max(x[0].width for x in pp[12:]),'center')]:bank('prism_fx','pb19_'+pre,group,cell,anchor,scale_,mode,16)
for n,actions in [('helios_idle_hit',['idle','hit']),('helios_lightning_death',['lightning','death'])]:
 pp=cuts(n,4,4);s=210/pp[0][0].height
 for j,act in enumerate(actions):bank(n,'pb19_helios_'+act,pp[j*8:j*8+8],(384,384),(192,346),s,fps=12);alias('pb18_helios_'+act,'pb19_helios_'+act)
for n,act,cols,rows in [('helios_walk_final','walk',4,2),('helios_run','run',4,4),('helios_throw','throw',4,4),('helios_jump','jump',4,4)]:
 pp=cuts(n,cols,rows);s=210/pp[0][0].height
 bank(n,'pb19_helios_'+act,pp,(384,384),(192,346),s,fps=18 if act=='run' else 16,flip_indices=range(8,16)if act=='run'else());alias('pb18_helios_'+act,'pb19_helios_'+act)
for n,acts in [('gosfer_motion',['walk_south','walk_east']),('gosfer_fire',['fire_south','fire_east']),('gosfer_dash_death',['dash_east','death']),('vault_gosfer_rear',['enemy_vault','walk_north'])]:
 pp=cuts(n,4,4)
 for j,act in enumerate(acts):
  group=pp[j*8:j*8+8];height=140 if act=='enemy_vault' else 144;s=height/group[0][0].height;pre='pb19_rifle_vault'if act=='enemy_vault'else'pb19_gosfer_'+act
  bank(n,pre,group,(384,384),(192,346),s,'helmet',fps=14,muzzle='orange')
  if act!='enemy_vault':alias('pb18_gosfer_'+act,pre)
for n,act in [('enemies_walk','walk'),('enemies_fire','fire'),('enemies_death','death'),('enemies_crouch','crouch')]:
 pp=cuts(n,8,4)
 for i,kind in enumerate(['rifle','heavy','rocket','laser']):
  group=pp[i*8:i*8+8];s=(180 if kind=='heavy' else 140)/group[0][0].height
  bank(n,'pb19_'+kind+'_'+act,group,(256,272),(128,248),s,fps=12,muzzle='cyan_tip' if kind=='laser' else 'orange')
  alias('pb16_'+kind+'_'+act,'pb19_'+kind+'_'+act);alias('pb17_'+kind+'_'+act,'pb19_'+kind+'_'+act)
for kind in ['rifle','heavy','rocket','laser']:
 walk=D['sequences']['pb19_'+kind+'_walk'];D['sequences']['pb16_'+kind+'_idle']={**walk,'frames':[walk['frames'][0]]}
alias('pb16_rifle_vault','pb19_rifle_vault');alias('pb17_elite_walk','pb19_rifle_walk');alias('pb17_elite_fire','pb19_rifle_fire');alias('pb17_elite_death','pb19_rifle_death');alias('pb17_elite_vault','pb19_rifle_vault');alias('pb17_elite_crouch','pb19_rifle_crouch')
PC=(192,224);PA=(96,160)
dirs=['south','west','north','east'];diags=['southwest','northwest','northeast','southeast']
for n,act,ds in [('yuri_fire','fire',dirs),('yuri_walk','walk',dirs),('yuri_diagonal','walk',diags),('yuri_grenade','grenade',dirs),('yuri_grenade_diagonal','grenade',diags)]:
 pp=cuts(n,8,4);s=88/statistics.median(pp[i*8][0].height for i in range(4))
 for i,d in enumerate(ds):
  bank(n,'pb19_yuri_'+d+'_'+act,pp[i*8:i*8+8],PC,PA,s,'yuri',fps=8/.6 if act=='grenade' else 20 if act=='fire' else 12,muzzle='cyan');alias('yuri_'+d+'_'+act,'pb19_yuri_'+d+'_'+act)
for d in dirs+diags:
 alias('yuri_'+d+'_run_fire','pb19_yuri_'+d+'_walk');D['sequences']['yuri_'+d+'_walk']['motion']=True;D['sequences']['yuri_'+d+'_walk']['stride']=64
 D['sequences']['yuri_'+d+'_idle']={**D['sequences']['yuri_'+d+'_fire'if d in dirs else'yuri_'+d+'_walk'],'frames':[D['sequences']['yuri_'+d+'_fire'if d in dirs else'yuri_'+d+'_walk']['frames'][0]],'motion':False}
 if d in diags:D['sequences']['yuri_'+d+'_fire']={**D['sequences']['yuri_'+d+'_idle'],'fps':20}
pp=cuts('yuri_cover',8,4);s=88/pp[7][0].height
for i,act in enumerate(['peek','blindfire','crouch_sidestep','cover_fire']):
 bank('yuri_cover','pb19_yuri_north_'+act,pp[i*8:i*8+8],PC,PA,s,'yuri',fps=16,muzzle='cyan');alias('yuri_north_'+act,'pb19_yuri_north_'+act)
for n,i,act in [('yuri_recovery',0,'death'),('yuri_recovery',1,'revive'),('yuri_recovery',2,'hop'),('yuri_recovery',3,'prone_transition')]:
 pp=cuts(n,8,4);s=88/pp[16][0].height;bank(n,'pb19_yuri_north_'+act,pp[i*8:i*8+8],PC,PA,s,'yuri',fps=12,muzzle='cyan')
alias('yuri_north_knockback','pb19_yuri_north_death')
pp=cuts('yuri_prone_transition',4,4);s=88/pp[8][0].height
bank('yuri_prone_transition','pb19_yuri_west_crawl',pp[:8],PC,PA,s,'yuri_prone',fps=12,muzzle='cyan');bank('yuri_prone_transition','pb19_yuri_east_crawl',[(q.transpose(Image.Transpose.FLIP_LEFT_RIGHT),b)for q,b in pp[:8]],PC,PA,s,'yuri_prone',fps=12,muzzle='cyan')
bank('yuri_prone_transition','pb19_yuri_west_prone_transition',pp[8:],PC,PA,s,'yuri',fps=16,muzzle='cyan')
pp=cuts('yuri_crawl',8,4)
for i,d in [(0,'south')]:bank('yuri_crawl','pb19_yuri_'+d+'_crawl',pp[i*8:i*8+8],PC,PA,88/statistics.median(q.height for q,b in pp[i*8:i*8+8]),'yuri_prone',fps=12,muzzle='cyan')
pp=cuts('yuri_north_crawl_final',4,2);bank('yuri_north_crawl_final','pb19_yuri_north_crawl',pp,PC,PA,54/statistics.median(q.width for q,b in pp),'yuri_prone',fps=12,muzzle='cyan')
for d in dirs:
 alias('yuri_'+d+'_crawl','pb19_yuri_'+d+'_crawl');D['sequences']['yuri_'+d+'_crawl']['motion']=True;D['sequences']['yuri_'+d+'_crawl']['stride']=44
 D['sequences']['yuri_'+d+'_prone_fire']={**D['sequences']['yuri_'+d+'_crawl'],'motion':False,'frames':[D['sequences']['yuri_'+d+'_crawl']['frames'][0]]}
for path in S.glob('*.png'):D['sources'][path.name]={'size':list(Image.open(path).size),'sha12':hashlib.sha256(path.read_bytes()).hexdigest()[:12]}
(O/'manifest.json').write_text(json.dumps(D,indent=2)+'\n',encoding='utf-8',newline='\n');(O/'manifest.js').write_text('window.TD_BASTION19_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'assets':len(D['assets']),'uniquePNG':len(list(F.glob('*.png'))),'banks':len(D['sequences']),'sources':len(D['sources'])}))
