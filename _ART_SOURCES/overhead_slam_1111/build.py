from pathlib import Path
import os,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True)
C=640;P=[320,320];FOOT=474;SCALE=.63
SOURCES={r['name']:r for r in json.loads((W/'source-index.json').read_text())if r.get('accepted')}
# Measured source-space head, end-face and torso seeds; coordinates use the
# generation's1254 reference grid. They register complete drawings only.
HEADS={
 'blue-load':[[150,430],[1030,230],[425,750],[770,1050]],
 'blue-cock':[[405,70],[1020,180],[420,770],[1010,665]],
 'blue-descent':[[320,65],[760,210],[220,1020],[805,1025]],
 'blue-drive':[[415,75],[805,475],[230,1140],[810,1140]],
 'drac-load':[[140,435],[735,350],[470,700],[720,1040]],
 'drac-cock':[[455,105],[1035,145],[460,770],[1040,690]],
 'drac-descent':[[455,105],[1050,285],[450,1010],[1050,1025]],
 'drac-drive':[[450,110],[740,455],[220,1130],[775,1130]]}
CORES={
 'blue-load':[[320,245],[920,280],[325,900],[925,900]],
 'blue-cock':[[315,275],[895,290],[320,870],[900,900]],
 'blue-descent':[[320,270],[900,265],[320,870],[900,870]],
 'blue-drive':[[315,255],[895,250],[315,885],[900,880]],
 'drac-load':[[315,230],[905,235],[320,875],[905,880]],
 'drac-cock':[[305,270],[890,270],[305,875],[890,900]],
 'drac-descent':[[305,260],[890,260],[305,865],[890,870]],
 'drac-drive':[[305,270],[890,270],[305,900],[890,900]]}
# Explicit contact end faces: low forward cap for blue, lower spiked cap for
# purple. The body/weapon artwork is never replaced or assembled from these.
TIPS={('blue-drive',2):[275,1195],('blue-drive',3):[850,1180],
      ('drac-drive',2):[280,1210],('drac-drive',3):[830,1195]}
CACHE={};source_audit=[]
def raw(name,cell):
 key=(name,cell)
 if key in CACHE:return dict(CACHE[key])
 p=Path(SOURCES[name]['file']);p=p if p.is_absolute()else W/p
 im=Image.open(p).convert('RGBA');a=np.asarray(im);h,w=a.shape[:2];opaque=a[:,:,3]>180
 counts=opaque.sum(axis=1);lo,hi=int(h*.42),int(h*.60);empty=counts[lo:hi]==0
 z=np.flatnonzero(np.diff(np.r_[False,empty,False]));runs=[(int(z[i]),int(z[i+1]))for i in range(0,len(z),2)]
 split=lo+sum(max(runs,key=lambda r:r[1]-r[0]))//2 if runs else h//2
 x0,x1=[0,w//2,w][cell%2:cell%2+2];y0,y1=[0,split,h][cell//2:cell//2+2]
 crop=opaque[y0:y1,x0:x1]
 assert not(crop[0].any()or crop[-1].any()or crop[:,0].any()or crop[:,-1].any()),('source clipped',key)
 xs,ys=np.meshgrid(np.arange(w),np.arange(h));r,g,b=[a[:,:,i].astype(float)for i in range(3)]
 def xy(q):return [q[0]*w/1254,q[1]*h/1254]
 cx,cy=xy(CORES[name][cell]);roi=(abs(xs-cx)<38)&(abs(ys-cy)<34)
 purple=name.startswith('drac');hot=opaque&roi&((r>170)&(r>g*1.25)&(r>b*1.25)if purple else(b>180)&(b>r*1.2))
 yy,xx=np.where(hot);assert len(xx)>30,('core seed',key);rootx=float(xx.mean())
 # Right boot is clear of the low left-hand hammer. Never use the weapon's
 # lower pixels as the character's sole/baseline.
 foot=opaque&(xs>rootx+55)&(xs<rootx+190)&(ys>max(y0,y1-210))&(ys<y1)
 fy,fx=np.where(foot);assert len(fx)>100,('boot missing',key);sole=float(fy.max())
 hx,hy=xy(HEADS[name][cell]);near=(abs(xs-hx)<78)&(abs(ys-hy)<82)
 hot=opaque&near&((r>145)&(b>150)&(r>g*1.2)&(b>g*1.3)if purple else(b>180)&(b>r*1.2))
 yy,xx=np.where(hot);assert len(xx)>30,('hammer seed',key);centre=[float(xx.mean()),float(yy.mean())]
 tip=xy(TIPS[key])if key in TIPS else [centre[0],min(y1-2,centre[1]+(64 if purple else 35))]
 tx,ty=map(round,tip)
 if not opaque[max(0,min(h-1,ty)),max(0,min(w-1,tx))]:
  yy,xx=np.where(opaque&(abs(xs-tx)<30)&(abs(ys-ty)<30));assert len(xx),('contact outside source',key)
  j=np.argmin((xx-tx)**2+(yy-ty)**2);tip=[float(xx[j]),float(yy[j])]
 out=dict(input=str(p),source=name,sourceCell=cell,crop=[x0,y0,x1-x0,y1-y0],root=[rootx-x0,sole-y0],tip=[tip[0]-x0,tip[1]-y0],headCenter=[centre[0]-x0,centre[1]-y0],grip=[cx-x0,cy-y0],scale=SCALE,mirror=False)
 source_audit.append(dict(source=name,cell=cell,root=out['root'],tip=out['tip'],headCenter=out['headCenter'],sourceEdgeIssue=False))
 CACHE[key]=out;return dict(out)
jobs=[]
for unit in ['blue','drac']:
 seq=[('load',0),('load',1),('load',2),('cock',0),('cock',1),('cock',2),('cock',2),('cock',3),('descent',0),('descent',1),('descent',2),('drive',2),('drive',3),('descent',3),('load',3),('load',0)]
 frames=[]
 for i,(group,f)in enumerate(seq):
  q=raw(unit+'-'+group,f)
  # The whole symmetric copied actor turns the same pose toward its left-hand
  # contact plane. No isolated hammer/arm/head flip or assembly.
  q['mirror']=unit=='drac'and group=='descent'and f>0
  q['phase']='behind-head'if i in [4,5,6]else'contact'if i==11 else'downstroke'if i in [7,8,9,10]else'recovery'if i>11 else'load'
  frames.append(q)
 jobs.append(dict(name=('blue'if unit=='blue'else'corrupt')+'-overhead',unit=unit,frames=frames,cell=C,pivot=P,foot=FOOT))
(W/'jobs.json').write_text(json.dumps(jobs,indent=2))
subprocess.run([os.environ.get('ASEPRITE',r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'),'--batch','--script-param','out='+W.as_posix(),'--script',str(W/'author.lua')],check=True)
M={};audit=[]
for j in jobs:
 n=j['name'];arr=np.asarray(Image.open(E/(n+'_regular.png')));meta=[]
 for i,z in enumerate(j['frames']):
  alpha=arr[i//4*C:(i//4+1)*C,i%4*C:(i%4+1)*C,3];yy,xx=np.where(alpha>96);bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
  assert min(bounds[:2])>0 and max(bounds[2:])<C,('normalized crop',n,i,bounds)
  def pos(p):
   v=[P[0]+(p[0]-z['root'][0])*SCALE,FOOT+(p[1]-z['root'][1])*SCALE]
   if z['mirror']:v[0]=C-1-v[0]
   return v
  row=dict(tip=pos(z['tip']),headCenter=pos(z['headCenter']),grip=pos(z['grip']),bounds=bounds,spans=[np.flatnonzero(np.diff(np.r_[False,v>96,False])).tolist()for v in alpha],depth=1,wholeGenerated=True,faceForward=True,source=z['source'],sourceCell=z['sourceCell'],phase=z['phase'])
  tx,ty=map(round,row['tip']);assert alpha[ty,tx]>96,(n,i,'target off alpha',row['tip'])
  meta.append(row);audit.append(dict(bank=n,frame=i,source=z['source'],cell=z['sourceCell'],phase=z['phase'],mirror=z['mirror'],bounds=bounds,tip=row['tip']))
 M[n]=dict(cell=[C,C],pivot=P,cols=4,count=16,folder='overhead_slam_1111',meta=meta)
 for mat in ['regular','chrome','red','hit','red_hit']:
  p=E/(n+'_'+mat+'.png');Image.open(p).save(p.with_suffix('.webp'),lossless=True,method=1)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'overhead_slam_art_1111.js').write_text("'use strict';\n/* Complete generated behind-head attacks; no separate held weapon. */\nObject.assign(BA119_ART,"+json.dumps(M,separators=(',',':'))+');\n')
(W/'audit.json').write_text(json.dumps(dict(passed=True,cells=audit,sources=source_audit,uniqueDrawings=len(CACHE),normalization='whole figure registration at torso symmetry/right-boot sole; one .63 scale; complete-pose flips only'),indent=2))
print('Exported',len(audit),'whole attack cells;',len(CACHE),'distinct source drawings; all source/cell edges and target alpha pass.')
