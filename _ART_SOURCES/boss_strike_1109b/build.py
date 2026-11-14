from pathlib import Path
import json,math,subprocess,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent
ASE=r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
(W/'exports').mkdir(exist_ok=True)
# Source landmarks are reviewed against the full raster, not alpha-box fitting.
config={
 'chronos-overhead':dict(name='blue-overhead',scale=1.25,feet=[262,262,262,262,574,574,574,574,887,887,887,887,1200,1200,1200,1200],tips=[[95,220],[90,209],[95,135],[121,68],[122,55],[125,58],[148,45],[163,38],[166,50],[154,168],[170,257],[155,257],[166,255],[97,232],[100,230],[93,238]]),
 'chronos-sides':dict(name='blue-sides',scale=1.20,feet=[273,273,273,273,583,583,583,583,894,894,894,894,1204,1204,1204,1204],tips=[[95,225],[255,200],[266,177],[276,107],[258,112],[250,132],[175,132],[45,125],[45,125],[61,209],[90,235],[101,232],[100,232],[100,230],[100,232],[100,232]]),
 'drac-overhead':dict(name='corrupt-overhead',scale=1.45,feet=[284,284,284,284,604,604,604,604,917,917,917,917,1221,1221,1221,1221],tips=[[55,235],[70,222],[78,189],[75,132],[90,86],[114,58],[128,55],[156,49],[165,53],[157,247],[165,283],[157,283],[160,285],[87,266],[68,264],[58,265]]),
 'drac-sides':dict(name='corrupt-sides',scale=1.42,feet=[288,288,288,288,603,603,603,603,918,918,918,918,1231,1231,1231,1231],tips=[[55,242],[83,233],[255,155],[130,192],[53,140],[60,145],[45,210],[65,243],[105,89],[103,82],[50,148],[267,166],[260,170],[265,220],[245,252],[56,264]])}
jobs=[]
for source,cfg in config.items():
 im=Image.open(W/'generated'/f'{source}.png').convert('RGBA');iw,ih=im.size;frames=[]
 for i in range(16):
  si=7 if source=='chronos-sides'and i==8 else i # intentional full-extension contact hold; edge-clipped source9 is rejected
  x,y,x1,y1=round(si%4*iw/4),round(si//4*ih/4),round((si%4+1)*iw/4),round((si//4+1)*ih/4)
  a=np.array(im)[y:y1,x:x1,3]
  # Lowest row with two substantial separated soles. A lowered central hammer
  # or one boot's antialias fringe cannot masquerade as the support root.
  found=None
  for yy in range(a.shape[0]-1,int(a.shape[0]*.65),-1):
   edges=np.flatnonzero(np.diff(np.r_[False,a[yy]>=128,False])).tolist();runs=[]
   for k in range(0,len(edges),2):
    lo,hi=edges[k:k+2]
    if runs and lo-runs[-1][1]<=3:runs[-1][1]=hi
    else:runs.append([lo,hi])
   runs=[q for q in runs if q[1]-q[0]>=8]
   if len(runs)>=2 and runs[-1][1]-runs[0][0]>=a.shape[1]*.50:
    found=((runs[0][0]+runs[-1][1]-1)/2,yy);break
  assert found,(source,i,'two sole registration')
  rootx,floor=found
  frames.append(dict(crop=[x,y,x1-x,y1-y],root=[rootx,floor],tip=cfg['tips'][si],sourceFrame=si))
 j=dict(name=cfg['name'],input=str(W/'generated'/f'{source}.png'),scale=cfg['scale'],frames=frames,anchor=[288,442],pivot=[288,288],cell=576)
 jobs.append(j)
 if source=='chronos-sides':jobs.append(dict(j,name='blue-right',mirror=True))
for source,scale,angle in [('drone-arm',.55,-math.radians(53)),('final-arm',.55,-math.pi/12)]:
 im=Image.open(W/'generated'/f'{source}.png');iw,ih=im.size;frames=[]
 tips=[[102,220],[105,175],[106,123],[123,64],[161,40],[193,65],[112,192],[75,228],[45,226],[45,225],[41,231],[44,218],[86,211],[109,166],[100,183],[110,211]] if source=='drone-arm'else[[98,210],[105,162],[109,118],[130,70],[162,45],[151,96],[101,198],[69,222],[46,228],[44,225],[44,225],[69,194],[75,171],[103,172],[110,194],[108,213]]
 for i in range(16):
  x,y,x1,y1=round(i%4*iw/4),round(i//4*ih/4),round((i%4+1)*iw/4),round((i//4+1)*ih/4)
  frames.append(dict(crop=[x,y,x1-x,y1-y],root=[322,56],tip=tips[i],sourceFrame=i))
 j=dict(name=source,input=str(W/'generated'/f'{source}.png'),scale=scale,rotate=angle,frames=frames,anchor=[404 if source=='drone-arm'else 420,145],pivot=[288,288],cell=576)
 jobs.append(j);jobs.append(dict(j,name=source+'-right',mirror=True))
# Shared padded source rectangles keep complete low hammer spikes and followthroughs.
for j in jobs:
 iw,ih=Image.open(j['input']).size
 for z in j['frames']:
  x,y,w,h=z['crop'];xx=max(0,x-20);yy=max(0,y-22);ww=min(iw,x+w+20)-xx;hh=min(ih,y+h+22)-yy
  z['crop']=[xx,yy,ww,hh];z['root']=[z['root'][0]+x-xx,z['root'][1]+y-yy];z['tip']=[z['tip'][0]+x-xx,z['tip'][1]+y-yy]
(W/'jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
selected=[j for j in jobs if '--only-hammers'not in sys.argv or 'arm'not in j['name']]
(W/'build-jobs.json').write_text(json.dumps(selected,indent=2),encoding='utf8')
if '--metadata-only'not in sys.argv:subprocess.run([ASE,'--batch','--script-param','out='+W.as_posix(),'--script-param','jobs='+str(W/'build-jobs.json'),'--script',str(W/'author.lua')],check=True)
manifest={};audit=[]
for j in jobs:
 name=j['name'];meta=[];sheet=Image.open(W/'exports'/f'{name}_regular.png').convert('RGBA')
 for i,z in enumerate(j['frames']):
  c=sheet.crop((i%4*576,i//4*576,(i%4+1)*576,(i//4+1)*576));alpha=np.array(c)[:,:,3];ys,xs=np.where(alpha>96);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
  assert min(bounds)>5 and max(bounds)<571,(name,i,bounds)
  tip=[round(j['anchor'][k]+(z['tip'][k]-z['root'][k])*j['scale'])for k in range(2)]
  if j.get('rotate'):
   dx=tip[0]-j['anchor'][0];dy=tip[1]-j['anchor'][1];cs=math.cos(j['rotate']);sn=math.sin(j['rotate']);tip=[round(j['anchor'][0]+dx*cs-dy*sn),round(j['anchor'][1]+dx*sn+dy*cs)]
  if j.get('mirror'):tip[0]=575-tip[0]
  if not(0<=tip[0]<576 and 0<=tip[1]<576 and alpha[tip[1],tip[0]]>96):
   d=(xs-tip[0])**2+(ys-tip[1])**2;k=np.argmin(d);assert d[k]<90**2,(name,i,'tip distance',d[k]);tip=[int(xs[k]),int(ys[k])]
  spans=[]
  for y in range(576):
   on=alpha[y]>96;edges=np.flatnonzero(np.diff(np.r_[False,on,False])).tolist();spans.append(edges)
  meta.append(dict(tip=tip,grip=[288,337],bounds=bounds,spans=spans,depth=1))
  audit.append(dict(bank=name,frame=i,bounds=bounds,tip=tip,sourceFrame=z['sourceFrame'],opaque=int((alpha>96).sum())))
 for mat in ['regular','chrome','red','hit','red_hit']:
  src=W/'exports'/f'{name}_{mat}.png';im=Image.open(src)
  assert im.getchannel('A').tobytes()==sheet.getchannel('A').tobytes(),(name,mat,'alpha mismatch')
  if '--metadata-only'not in sys.argv and j in selected:im.save(src.with_suffix('.webp'),lossless=True,quality=100,method=1)
 manifest[name]=dict(cell=[576,576],pivot=j['pivot'],cols=4,count=16,folder='boss_strike_1109b',meta=meta,sha256=hashlib.sha256(sheet.tobytes()).hexdigest())
 if 'arm'in name:manifest[name]['mount']=[(-1 if name.endswith('-right')else 1)*(22 if name.startswith('drone')else 20),-3 if name.startswith('drone')else -5]
 contact=Image.new('RGB',(1024,1104),'#14202b');d=ImageDraw.Draw(contact)
 for i in range(16):
  c=sheet.crop((i%4*576,i//4*576,(i%4+1)*576,(i//4+1)*576));c.thumbnail((256,256));x=i%4*256;y=i//4*276;contact.paste(c,(x,y),c);d.text((x+8,y+258),f'{name} {i}',fill='white')
 contact.save(W/'exports'/f'{name}-contact.png')
(W/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')),encoding='utf8')
(W/'audit.json').write_text(json.dumps(dict(cells=audit,banks=len(manifest),poses=len(audit),materials=5,passed=True),indent=2),encoding='utf8')
print(json.dumps(dict(banks=len(manifest),cells=len(audit))))
