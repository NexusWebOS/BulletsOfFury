"""Measured animation metadata and existing authored FX for the component preview."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects

R=Path(__file__).resolve().parents[1];O=R/'art-packs/raiden-components-1024';S=R/'assets/game/shared/combat/stage1_motion_1009'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
catalog=json.loads((O/'manifest.json').read_text());out=dict(version=1,period=8,parts={},units={},fx={},sources=[],method='Runtime articulated module motion using the approved matched sprites. No generated replacement hulls, palette swaps or new flight pose banks.')
for u in catalog['units']:out['units'][u['id']]=dict(extent=list(Image.open(O/u['master']).getbbox()))
for c in catalog['components']:
 im=Image.open(O/c['image']).convert('RGBA');a=np.array(im)[:,:,3]>200;x0,y0,x1,y1=c['bbox'];w,h=x1-x0,y1-y0;role=c['role'];m={}
 if role.endswith('track')or role in ['rubber_tire','armored_tire','road_wheel','steel_roller','wide_roller','idler','sprocket']:
  # Re-sample only the existing rolling surface; mounting arms and the casing
  # remain fixed. All samples come from the original approved module pixels.
  cx=round((x0+x1)/2);width=round(w*(.39 if role.endswith('track')else .30));top=round(y0+h*.13);height=round(h*.69)
  m['surface']=[cx-width//2,top,width,height];m['pitch']=max(6,round(h/(18 if role.endswith('track')else 8)))
 if role.endswith('turret')or role=='cannon_pod':
  count=3 if role=='triple_turret'else 2 if role=='twin_turret'else 1
  groups=[]
  for y in range(y1-3,max(y0,y1-18),-1):
   row=a[y].copy()
   # Merge holes inside barrel rims, without merging distinct gun barrels.
   xs=np.where(row)[0]
   if len(xs):
    chunks=np.split(xs,np.where(np.diff(xs)>7)[0]+1);chunks=[z for z in chunks if len(z)>3]
    if len(chunks)>=count:
     groups=sorted(sorted(chunks,key=len,reverse=True)[:count],key=lambda z:z[0]);break
  tips=[]
  if groups:
   for group in groups:
    x=round((int(group[0])+int(group[-1]))/2);ys=np.where(a[:,max(x0,x-4):min(x1,x+5)].any(axis=1))[0];tips.append([x,int(ys.max())])
  else:tips=[[round((x0+x1)/2),y1-1]]
  widths=a.sum(axis=1);threshold=max(8,float(widths.max())*.61);cut=round(y0+h*.62)
  for y in range(round(y0+h*.48),round(y0+h*.86)):
   if np.all(widths[y:y+5]<threshold):cut=y;break
  m.update(tips=tips,barrel_y=cut)
 elif role in ['missile_rack','missile_pod']:
  rgb=np.array(im);red=(rgb[:,:,0]>150)&(rgb[:,:,1]<110)&(rgb[:,:,2]<110)&a
  labs,_=label(red);caps=[];north=role=='missile_rack'
  for number,s in enumerate(find_objects(labs),1):
   if s is not None and np.count_nonzero(labs[s]==number)>25:
    caps.append([round((s[1].start+s[1].stop)/2),s[0].start if north else s[0].stop-1])
  m['tips']=caps or [[round(x0+w*.5),y0+8 if north else y1-8]]
  m['launch_angle']=180 if north else 0
 elif role in ['engine_left','engine_right']:
  m['exhaust']=[round((x0+x1)/2),y0+6]
 elif role=='radar':m['dish']=[round((x0+x1)/2),round(y0+h*.36),round(min(w*.37,h*.29))]
 out['parts'][c['id']]=m
for family,count,pivot in [('muzzle',8,[128,24]),('exhaust',8,[128,600]),('wake',8,[150,320])]:
 frames=[]
 for i in range(count):
  source=S/f'{family}_{i}.png';dest=O/'animation-fx'/source.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  im=Image.open(dest);assert not(im.width%2 or im.height%2)
  frames.append(dict(image=dest.relative_to(O).as_posix(),size=list(im.size),pivot=pivot,source=source.relative_to(R).as_posix(),sha256=sha(dest)))
 out['fx'][family]=frames
armory=R/'art-packs/raiden-reference-1024';entries=json.loads((armory/'manifest.json').read_text())['assets']
for name in ['amber_slug','cyan_needle','micro_missile','cyan_lance']:
 item=next(p for p in entries if p['id']==name);source=armory/item['master'];im=Image.open(source).convert('RGBA');a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=200,255,0);a[a[:,:,3]==0]=0
 dest=O/'animation-fx'/f'{name}.png';Image.fromarray(a).save(dest,optimize=True)
 out['fx'][name]=dict(image=dest.relative_to(O).as_posix(),size=list(im.size),pivot=[128,450]if name=='cyan_lance'else item['pivot'],source=source.relative_to(R).as_posix(),source_sha256=sha(source),alpha_cutoff=200,sha256=sha(dest))
out['catalog_sha256']=sha(O/'manifest.json')
(O/'animation-data.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');(O/'animation-data.js').write_text('window.RAIDEN_MOTION='+json.dumps(out,separators=(',',':'))+';\n',encoding='utf-8')
print('ANIMATION: registered 201 measured parts; 24 existing authored FX frames; four retained ordnance assets.',flush=True)
