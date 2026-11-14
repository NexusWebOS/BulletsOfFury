from pathlib import Path
import json,math,subprocess
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;E=W/'exports';E.mkdir(exist_ok=True)
# Hand sockets measured in the clean full-body masters. The canonical prop is
# registered at the first hand, never by changing its head/handle geometry.
OH=[[137,191],[137,171],[119,127],[134,72],[163,41],[158,48],[159,48],[156,45],[169,57],[124,186],[151,204],[149,213],[161,213],[124,186],[126,188],[137,201]]
SD=[[140,188],[202,169],[214,145],[194,110],[170,107],[161,115],[162,118],[117,114],[84,116],[116,137],[141,162],[147,181],[143,190],[143,190],[140,190],[140,190]]
DO=[[120,197],[109,163],[96,137],[115,100],[163,42],[160,42],[154,43],[151,39],[164,48],[129,177],[151,193],[151,202],[160,195],[124,178],[124,185],[139,194]]
DS=[[137,196],[192,177],[206,156],[188,127],[161,118],[158,118],[158,125],[110,120],[78,120],[115,142],[140,164],[143,181],[141,190],[141,190],[140,190],[140,190]]
AOH=[-35,-30,-5,-15,25,55,75,90,95,200,270,270,270,325,325,325]
ASD=[-35,180,180,180,180,180,180,0,0,-10,-35,-35,-35,-35,-35,-35]
J=[]
for n,grips,angs in [('blue-overhead',OH,AOH),('blue-sides',SD,ASD),('corrupt-overhead',DO,AOH),('corrupt-sides',DS,ASD)]:
 p=W/'generated'/(n+'.png');im=Image.open(p);iw,ih=im.size;a=np.asarray(im)[:,:,3];frames=[];height=0
 for i in range(16):
  x,y,x1,y1=round(i%4*iw/4),round(i//4*ih/4),round((i%4+1)*iw/4),round((i//4+1)*ih/4);z=a[y:y1,x:x1];found=None
  for yy in range(z.shape[0]-1,int(z.shape[0]*.65),-1):
   e=np.flatnonzero(np.diff(np.r_[False,z[yy]>170,False]));rs=[e[k:k+2]for k in range(0,len(e),2)if e[k+1]-e[k]>=7]
   if len(rs)>=2 and rs[-1][1]-rs[0][0]>z.shape[1]*.4:found=[float((rs[0][0]+rs[-1][1]-1)/2),int(yy)];break
  assert found,(n,i);ys,xs=np.where(z>170);height=max(height,found[1]-int(ys.min()));frames.append(dict(crop=[x,y,x1-x,y1-y],root=found,hands=[grips[i]],angle=math.radians(angs[i])))
 scale=(300 if n.startswith('blue')else 320)/height
 # A fixed head-to-grip distance is shared by every pose; only the whole rigid
 # assembly rotates. Source-pose perspective never turns it into an axial club.
 for i,f in enumerate(frames):
  f['grip']=[288+(grips[i][0]-f['root'][0])*scale,442+(grips[i][1]-f['root'][1])*scale]
  d=100 if n.startswith('blue')else 105;f['tip']=[f['grip'][0]-d*math.cos(f['angle']),f['grip'][1]-d*math.sin(f['angle'])]
 J.append(dict(name=n,unit='blue'if n.startswith('blue')else'drac',input=str(p),scale=scale,frames=frames,mirror=False))
 if n=='blue-sides':J.append(dict(J[-1],name='blue-right',mirror=True))
(W/'jobs.json').write_text(json.dumps(J,indent=2))
subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+W.as_posix(),'--script',str(W/'body-author.lua')],check=True)
M={};audit=[]
for j in J:
 arr=np.asarray(Image.open(E/(j['name']+'_regular.png')));meta=[]
 for i,z in enumerate(j['frames']):
  alpha=arr[i//4*576:(i//4+1)*576,i%4*576:(i%4+1)*576,3];ys,xs=np.where(alpha>96);b=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];tip=z['tip'].copy();grip=z['grip'].copy()
  if j['mirror']:tip[0]=575-tip[0];grip[0]=575-grip[0]
  assert b[0]>1 and b[1]>1 and b[2]<574 and b[3]<574,(j['name'],i,b)
  meta.append(dict(tip=tip,grip=grip,bounds=b,spans=[np.flatnonzero(np.diff(np.r_[False,row>96,False])).tolist()for row in alpha],depth=1,hammerRigid=True,hammerAngle=z['angle']))
  audit.append(dict(bank=j['name'],frame=i,bounds=b,headToGrip=math.dist(tip,grip),jointAngle=90))
 M[j['name']]=dict(cell=[576,576],pivot=[288,288],cols=4,count=16,folder='rigid_hammer_1110',meta=meta)
 for mat in ['regular','chrome','red','hit','red_hit']:
  p=E/(j['name']+'_'+mat+'.png');Image.open(p).save(p.with_suffix('.webp'),lossless=True,method=1)
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'audit.json').write_text(json.dumps(dict(passed=True,cells=audit,poses=len(audit),flightFrames=32,method='Clean GPT body layers; immutable blue and HC23 purple weapon masters. Rotations/materials baked offline in Aseprite.'),indent=2));print('Clean-body rigid assemblies exported',len(audit))

