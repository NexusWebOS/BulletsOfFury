from pathlib import Path
import json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent
ASE=r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
(W/'exports').mkdir(exist_ok=True)
config={
 'drac-overhead':dict(name='corrupt-overhead',scale=1.42,tips=[[54,217],[61,212],[57,162],[49,132],[50,110],[92,65],[90,50],[151,31],[164,45],[165,84],[160,272],[160,272],[165,260],[60,235],[45,215],[52,222]]),
 'drac-sides':dict(name='corrupt-sides',scale=1.42,tips=[[160,270],[160,270],[55,217],[40,166],[40,145],[45,141],[45,190],[160,270],[55,230],[55,184],[225,153],[267,141],[265,150],[270,215],[160,265],[160,265]])}
jobs=[]
for src,cfg in config.items():
 im=Image.open(W/'generated'/f'{src}.png').convert('RGBA');iw,ih=im.size;frames=[]
 for i in range(16):
  x,y,x1,y1=round(i%4*iw/4),round(i//4*ih/4),round((i%4+1)*iw/4),round((i//4+1)*ih/4)
  a=np.array(im)[y:y1,x:x1,3];found=None
  for yy in range(a.shape[0]-1,int(a.shape[0]*.65),-1):
   edges=np.flatnonzero(np.diff(np.r_[False,a[yy]>=128,False])).tolist();runs=[]
   for k in range(0,len(edges),2):
    lo,hi=edges[k:k+2]
    if runs and lo-runs[-1][1]<=3:runs[-1][1]=hi
    else:runs.append([lo,hi])
   runs=[q for q in runs if q[1]-q[0]>=8]
   if len(runs)>=2 and runs[-1][1]-runs[0][0]>=a.shape[1]*.50:found=((runs[0][0]+runs[-1][1]-1)/2,yy);break
  assert found,(src,i,'two sole registration')
  xx=max(0,x-18);yy=max(0,y-18)
  frames.append(dict(crop=[xx,yy,min(iw,x1+18)-xx,min(ih,y1+18)-yy],root=[found[0]+x-xx,found[1]+y-yy],tip=[cfg['tips'][i][0]+x-xx,cfg['tips'][i][1]+y-yy],sourceFrame=i))
 jobs.append(dict(name=cfg['name'],input=str(W/'generated'/f'{src}.png'),scale=cfg['scale'],frames=frames,anchor=[288,442],pivot=[288,288],cell=576))
(W/'jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
subprocess.run([ASE,'--batch','--script-param','out='+W.as_posix(),'--script-param','jobs='+str(W/'jobs.json'),'--script',str(W/'author.lua')],check=True)
manifest={};audit=[]
for j in jobs:
 name=j['name'];meta=[];sheet=Image.open(W/'exports'/f'{name}_regular.png').convert('RGBA')
 for i,z in enumerate(j['frames']):
  c=sheet.crop((i%4*576,i//4*576,(i%4+1)*576,(i//4+1)*576));alpha=np.array(c)[:,:,3];ys,xs=np.where(alpha>96);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
  assert min(bounds)>5 and max(bounds)<571,(name,i,bounds)
  tip=[round(j['anchor'][k]+(z['tip'][k]-z['root'][k])*j['scale'])for k in range(2)]
  if not(0<=tip[0]<576 and 0<=tip[1]<576 and alpha[tip[1],tip[0]]>96):
   d=(xs-tip[0])**2+(ys-tip[1])**2;k=np.argmin(d);assert d[k]<90**2,(name,i,'tip distance',d[k]);tip=[int(xs[k]),int(ys[k])]
  spans=[np.flatnonzero(np.diff(np.r_[False,alpha[y]>96,False])).tolist()for y in range(576)]
  meta.append(dict(tip=tip,grip=[288,337],bounds=bounds,spans=spans,depth=1))
  audit.append(dict(bank=name,frame=i,bounds=bounds,tip=tip,sourceFrame=i,opaque=int((alpha>96).sum())))
 for mat in ['regular','chrome','red','hit','red_hit']:
  src=W/'exports'/f'{name}_{mat}.png';im=Image.open(src);assert im.getchannel('A').tobytes()==sheet.getchannel('A').tobytes(),(name,mat,'alpha mismatch');im.save(src.with_suffix('.webp'),lossless=True,quality=100,method=1)
 manifest[name]=dict(cell=[576,576],pivot=j['pivot'],cols=4,count=16,folder='boss_hammer_frontal_1109c',meta=meta,sha256=hashlib.sha256(sheet.tobytes()).hexdigest())
 contact=Image.new('RGB',(1024,1104),'#14202b');d=ImageDraw.Draw(contact)
 for i in range(16):
  c=sheet.crop((i%4*576,i//4*576,(i%4+1)*576,(i//4+1)*576));c.thumbnail((256,256));x=i%4*256;y=i//4*276;contact.paste(c,(x,y),c);d.text((x+8,y+258),f'{name} {i}',fill='white')
 contact.save(W/'exports'/f'{name}-contact.png')
(W/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')),encoding='utf8')
(W/'audit.json').write_text(json.dumps(dict(cells=audit,banks=len(manifest),poses=len(audit),materials=5,passed=True),indent=2),encoding='utf8')
print(json.dumps(dict(banks=len(manifest),cells=len(audit))))
