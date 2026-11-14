from pathlib import Path
import json, subprocess, math
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');E=W/'exports';E.mkdir(exist_ok=True)
jobs=[]
for unit,height in [('chronos',300),('drac',320)]:
 for bank,n,cols in [('charge',16,4),('palms',24,6)]:
  p=W/'generated'/f'{unit}-{bank}.png';im=Image.open(p);a=np.array(im)[:,:,3];iw,ih=im.size;frames=[]
  for i in range(n):
   x,y,x1,y1=round(i%cols*iw/cols),round(i//cols*ih/4),round((i%cols+1)*iw/cols),round((i//cols+1)*ih/4)
   z=a[y:y1,x:x1];found=None
   for yy in range(z.shape[0]-1,int(z.shape[0]*.60),-1):
    edges=np.flatnonzero(np.diff(np.r_[False,z[yy]>=190,False]));runs=[edges[k:k+2]for k in range(0,len(edges),2)if edges[k+1]-edges[k]>=6]
    if len(runs)>=2 and runs[-1][1]-runs[0][0]>z.shape[1]*.40:found=[float((runs[0][0]+runs[-1][1]-1)/2),int(yy)];break
   assert found,(unit,bank,i)
   frames.append(dict(crop=[x,y,x1-x,y1-y],root=found))
  h=max(z['root'][1]-int(np.where(a[z['crop'][1]:z['crop'][1]+z['crop'][3],z['crop'][0]:z['crop'][0]+z['crop'][2]]>=190)[0].min())+1 for z in frames)
  for depth,k,cw,ch,pv in [('fore',1,384,448,[192,224]),('back',.42,176,208,[88,104])]:
   if bank=='charge'and depth=='back':continue
   jobs.append(dict(name=f'{unit}_{bank}_{depth}',unit=unit,bank=bank,input=str(p),scale=height/h*k,frames=frames,cw=cw,ch=ch,pivot=pv,foot=pv[1]+150*k,depth=k))
# Existing authored effects, converted losslessly for Aseprite ingestion.
fx={}
for n in ['lightning','gather','wave_purple','wave_red']:
 p=R/'assets/game/shared/combat/dracodia_chronos_1030'/f'{n}.webp';out=E/(n+'-source.png');Image.open(p).save(out);fx[n]=str(out)
(W/'jobs.json').write_text(json.dumps(dict(jobs=jobs,fx=fx),indent=2))
(W/'author-jobs.json').write_text(json.dumps(dict(jobs=[j for j in jobs if '--only-charge'not in __import__('sys').argv or j['bank']=='charge'],fx=fx)))
if '--metadata-only'not in __import__('sys').argv:subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+W.as_posix(),'--script-param','jobs='+str(W/'author-jobs.json'),'--script',str(W/'author.lua')],check=True)
manifest={};audit=[]
for j in jobs:
 name=j['name'];cw,ch=j['cw'],j['ch'];im=Image.open(E/(name+'_power.png'));arr=np.array(im);meta=[]
 for i in range(len(j['frames'])):
  a=arr[i//4*ch:(i//4+1)*ch,i%4*cw:(i%4+1)*cw];alpha=a[:,:,3];ys,xs=np.where(alpha>=128);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];assert min(bounds)>1 and bounds[2]<cw-1 and bounds[3]<ch-1,(name,i,bounds)
  # Both palm sockets are measured from the source hand's metal, never guessed from the body box.
  # Authored extension frame3: source coordinates are stable within each 8-pose cycle.
  if j['bank']=='palms':
   source=Image.open(j['input']);sw,sh=source.size;w=sw/6;h=sh/4
   palmcoords=([[190,92],[69,124]]if j['unit']=='chronos'else[[152,117],[43,173]])
   if i//8==1:palmcoords=([[190,124],[65,92]]if j['unit']=='chronos'else[[153,173],[42,120]])
   if i//8==2:palmcoords=([[194,109],[67,109]]if j['unit']=='chronos'else[[160,158],[39,158]])
   root=j['frames'][i]['root'];palms=[[round(j['pivot'][0]+(p[0]-root[0])*j['scale']),round(j['foot']+(p[1]-root[1])*j['scale'])]for p in palmcoords]
  else:palms=[[j['pivot'][0]+round(56*j['depth']),j['pivot'][1]+round(15*j['depth'])],[j['pivot'][0]-round(56*j['depth']),j['pivot'][1]+round(15*j['depth'])]]
  spans=[np.flatnonzero(np.diff(np.r_[False,alpha[y]>128,False])).tolist()for y in range(ch)]
  meta.append(dict(bounds=bounds,palms=palms,tip=[round(sum(p[0]for p in palms)/2),round(sum(p[1]for p in palms)/2)],spans=spans))
  audit.append(dict(bank=name,frame=i,bounds=bounds,root=j['pivot'],opaque=int((alpha>128).sum())))
 manifest[name]=dict(cw=cw,ch=ch,pivot=j['pivot'],count=len(meta),cols=4,depth=j['depth'],meta=meta)
 for mat in ['power','hit']+(['plain']if j['bank']=='charge'else[]):
  p=E/f'{name}_{mat}.png';Image.open(p).save(p.with_suffix('.webp'),lossless=True,method=1)
for p in E.glob('fx_*.png'):Image.open(p).save(p.with_suffix('.webp'),lossless=True,method=1)
(W/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')))
(W/'audit.json').write_text(json.dumps(dict(passed=True,poses=len(audit),cells=audit),indent=2))
print('Authored',len(audit),'registered poses')
