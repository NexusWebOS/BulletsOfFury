from pathlib import Path
import json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;(W/'exports').mkdir(exist_ok=True)
ASE=r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
def cells(path):
 im=Image.open(path).convert('RGBA');iw,ih=im.size;out=[]
 for i in range(16):
  x,y,x1,y1=round(i%4*iw/4),round(i//4*ih/4),round((i%4+1)*iw/4),round((i//4+1)*ih/4)
  c=im.crop((x,y,x1,y1));b=c.getchannel('A').point(lambda a:255 if a>=96 else 0).getbbox();assert b
  out.append((x,y,x1,y1,b))
 return out
fold=cells(W/'generated/drac-fold.png');roll=cells(W/'generated/drac-roll.png');scale=1.25
# One unit scale per bank; compaction is drawn into the source poses.
diam=(fold[-1][4][2]-fold[-1][4][0])*scale
rscale=diam/(sum(q[4][2]-q[4][0]for q in roll)/16)
jobs=[]
for src,parts,k in [('fold',fold,scale),('roll',roll,rscale)]:
 frames=[]
 for i,(x,y,x1,y1,b)in enumerate(parts):
  root=[(b[0]+b[2])/2,(b[1]+b[3])/2]
  if src=='fold':root[1]=(b[3]-154/scale)*(1-i/15)+root[1]*(i/15)
  frames.append(dict(crop=[x,y,x1-x,y1-y],root=root,tip=root,sourceFrame=i))
 cell=384 if src=='fold'else 256
 jobs.append(dict(name='corrupt-'+src,input=str(W/'generated'/f'drac-{src}.png'),scale=k,frames=frames,anchor=[cell//2,cell//2],pivot=[cell//2,cell//2],cell=cell))
(W/'jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
subprocess.run([ASE,'--batch','--script-param','out='+W.as_posix(),'--script-param','jobs='+str(W/'jobs.json'),'--script',str(W/'author.lua')],check=True)
M={};audit=[]
for j in jobs:
 name=j['name'];cell=j['cell'];pivot=j['pivot'];sheet=Image.open(W/'exports'/f'{name}_regular.png').convert('RGBA');meta=[]
 for i,z in enumerate(j['frames']):
  c=sheet.crop((i%4*cell,i//4*cell,(i%4+1)*cell,(i//4+1)*cell));a=np.array(c)[:,:,3];ys,xs=np.where(a>96);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];assert min(bounds)>5 and max(bounds)<cell-5,(name,i,bounds)
  spans=[np.flatnonzero(np.diff(np.r_[False,a[y]>96,False])).tolist()for y in range(cell)]
  meta.append(dict(tip=pivot,grip=pivot,muzzle=pivot,bounds=bounds,spans=spans,depth=1));audit.append(dict(bank=name,frame=i,bounds=bounds))
 for mat in ['regular','chrome','red','hit','red_hit']:
  p=W/'exports'/f'{name}_{mat}.png';im=Image.open(p);assert im.getchannel('A').tobytes()==sheet.getchannel('A').tobytes();im.save(p.with_suffix('.webp'),lossless=True,method=1)
 M[name]=dict(cell=[cell,cell],pivot=pivot,cols=4,count=16,folder='dracodia_ball_1109',meta=meta,sha256=hashlib.sha256(sheet.tobytes()).hexdigest())
 contact=Image.new('RGB',(1024,1104),'#14202b');d=ImageDraw.Draw(contact)
 for i in range(16):
  c=sheet.crop((i%4*cell,i//4*cell,(i%4+1)*cell,(i//4+1)*cell));c.thumbnail((256,256));x=i%4*256;y=i//4*276;contact.paste(c,(x,y),c);d.text((x+6,y+258),f'{name} {i}',fill='white')
 contact.save(W/'exports'/f'{name}-contact.png')
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')),encoding='utf8');(W/'audit.json').write_text(json.dumps(dict(passed=True,cells=audit,scales={j['name']:j['scale']for j in jobs},diameter=diam),indent=2))
print('Exported32 poses, five matching-alpha materials; diameter',diam)
