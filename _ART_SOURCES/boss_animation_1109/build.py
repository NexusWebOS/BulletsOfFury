"""Reproducible source normalization: Aseprite owns pixels; Pillow audits/encodes."""
from pathlib import Path
import json,subprocess,hashlib,sys,math
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent
ASE=r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
(W/'exports').mkdir(exist_ok=True)
heads={
 'chronos-overhead':[[90,211],[100,190],[82,161],[98,91],[139,43],[145,40],[163,29],[167,16],[165,28],[155,72],[170,242],[170,242],[165,240],[110,225],[105,225],[100,225]],
 'chronos-sides':[[175,243],[110,215],[95,205],[78,110],[80,90],[67,110],[62,125],[47,117],[46,119],[112,82],[102,128],[75,193],[65,207],[60,207],[60,214],[160,246]],
 'drac-overhead':[[42,246],[64,225],[56,176],[62,106],[80,73],[80,66],[95,58],[130,36],[139,41],[142,61],[160,269],[168,277],[165,267],[68,263],[45,263],[47,261]],
 'drac-sides':[[195,270],[66,259],[54,241],[57,96],[60,128],[48,145],[40,143],[112,85],[108,75],[106,85],[264,158],[264,158],[269,175],[264,175],[264,200],[160,250]]}
jobs=[]
for src,scale in [('chronos-overhead',1.25),('chronos-sides',1.20),('drac-overhead',1.22),('drac-sides',1.22)]:
 frames=json.loads((W/(src+'-measure.json')).read_text())
 # Use feet only, never the hammer/pommel. Source-specific right/left boot spans.
 if src=='drac-sides':
  for i,(x,y) in enumerate([(188,289),(184,289),(184,290),(180,290),(194,286),(186,286),(183,287),(176,287),(183,282),(179,282),(153,282),(145,283),(176,273),(163,273),(155,273),(161,273)]):frames[i]['root']=[x,y]
 for i,z in enumerate(frames):z['tip']=heads[src][i]
 name=src.replace('chronos','blue').replace('drac','corrupt')
 jobs.append(dict(name=name,input=str(W/'generated'/f'{src}.png'),scale=scale,frames=frames,anchor=[288,442],pivot=[288,288],cell=576))
 if src=='chronos-sides':jobs.append(dict(jobs[-1],name='blue-right',mirror=True))
for src in ['chronos-fold','chronos-roll']:
 im=Image.open(W/'generated'/f'{src}.png').convert('RGBA');w,h=im.size;frames=[]
 for i in range(16):
  x,y,x1,y1=round(i%4*w/4),round(i//4*h/4),round((i%4+1)*w/4),round((i//4+1)*h/4)
  c=im.crop((x,y,x1,y1));b=c.getchannel('A').point(lambda v:255 if v>=96 else 0).getbbox()
  # The fold pelvis rises into a centered shell; do not scale individual poses.
  root=[(b[0]+b[2])/2, (b[3]-150/1.02)*(1-i/15)+(b[1]+b[3])/2*(i/15)] if src.endswith('fold') else [(b[0]+b[2])/2,(b[1]+b[3])/2]
  frames.append(dict(crop=[x,y,x1-x,y1-y],root=root,tip=root))
 jobs.append(dict(name=src.replace('chronos','blue'),input=str(W/'generated'/f'{src}.png'),scale=1.02 if src.endswith('fold') else .43,frames=frames,anchor=[288,288],pivot=[288,288],cell=576))
for src in ['drone-arm','final-arm']:
 im=Image.open(W/'generated'/f'{src}.png');w,h=im.size;frames=[]
 for i in range(16):
  x,y,x1,y1=round(i%4*w/4),round(i//4*h/4),round((i%4+1)*w/4),round((i//4+1)*h/4)
  # Upper-right proximal pauldron socket. Claw tip landmarks reviewed on sheet.
  tips=([[180,235],[160,220],[120,230],[140,170],[140,160],[135,170],[100,205],[80,245],[55,265],[45,275],[45,275],[40,270],[35,275],[75,255],[120,235],[150,235]] if src=='drone-arm' else [[190,255],[175,255],[160,250],[150,180],[135,160],[140,175],[120,225],[100,250],[70,275],[55,280],[55,280],[60,280],[65,285],[100,265],[140,250],[175,255]])
  frames.append(dict(crop=[x,y,x1-x,y1-y],root=[240,55],tip=tips[i]))
 j=dict(name=src,input=str(W/'generated'/f'{src}.png'),scale=.62,frames=frames,anchor=[420,145],pivot=[288,288],cell=576)
 if src=='drone-arm':j['rotate']=-math.pi/6
 jobs.append(j);jobs.append(dict(j,name=src+'-right',mirror=True))
for j in jobs:
 iw,ih=Image.open(j['input']).size
 for z in j['frames']:
  x,y,w,h=z['crop'];xx=max(0,x-28);yy=max(0,y-45);ww=min(iw,x+w+28)-xx;hh=min(ih,y+h+45)-yy
  z['crop']=[xx,yy,ww,hh];z['root']=[z['root'][0]+x-xx,z['root'][1]+y-yy];z['tip']=[z['tip'][0]+x-xx,z['tip'][1]+y-yy]
(W/'jobs.json').write_text(json.dumps(jobs,indent=2))
only=next((a.split('=',1)[1]for a in sys.argv if a.startswith('--only=')),None)
(W/'build-jobs.json').write_text(json.dumps([j for j in jobs if not only or j['name'].startswith(only)],indent=2))
if '--metadata-only'not in sys.argv:subprocess.run([ASE,'--batch','--script-param','out='+W.as_posix(),'--script-param','jobs='+str(W/'build-jobs.json'),'--script',str(W/'author.lua')],check=True)
manifest={}
for j in jobs:
 name=j['name'];meta=[];sheet=Image.open(W/'exports'/f'{name}_regular.png').convert('RGBA')
 for i,z in enumerate(j['frames']):
  c=sheet.crop((i%4*576,i//4*576,(i%4+1)*576,(i//4+1)*576));alpha=c.getchannel('A');bounds=alpha.getbbox();assert bounds and min(bounds)>5 and max(bounds)<571,(name,i,bounds)
  tip=[round(j['anchor'][k]+(z['tip'][k]-z['root'][k])*j['scale']) for k in range(2)]
  if j.get('rotate'):
   dx=tip[0]-j['anchor'][0];dy=tip[1]-j['anchor'][1];cs=math.cos(j['rotate']);sn=math.sin(j['rotate']);tip=[round(j['anchor'][0]+dx*cs-dy*sn),round(j['anchor'][1]+dx*sn+dy*cs)]
  if j.get('mirror'):tip[0]=575-tip[0]
  if alpha.getpixel(tuple(tip))<96:
   candidates=[(x,y)for y in range(max(0,tip[1]-64),min(576,tip[1]+65))for x in range(max(0,tip[0]-64),min(576,tip[0]+65))if alpha.getpixel((x,y))>=96]
   assert candidates,(name,i,'landmark outside anatomy')
   tip=list(min(candidates,key=lambda p:(p[0]-tip[0])**2+(p[1]-tip[1])**2))
  spans=[]
  for y in range(576):
   row=[];active=False
   for x in range(577):
    on=x<576 and alpha.getpixel((x,y))>96
    if on!=active:row.append(x);active=on
   spans.append(row)
  meta.append(dict(tip=tip,grip=[288,337],bounds=bounds,spans=spans,depth=1))
 for mat in ['regular','chrome','red','hit','red_hit']:
  src=W/'exports'/f'{name}_{mat}.png';im=Image.open(src)
  if '--metadata-only'not in sys.argv and(not only or name.startswith(only)):im.save(src.with_suffix('.webp'),lossless=True,quality=100,method=1)
  if mat=='regular':continue
  assert im.getchannel('A').tobytes()==sheet.getchannel('A').tobytes(),(name,mat,'alpha')
 manifest[name]=dict(cell=[576,576],pivot=j['pivot'],cols=4,count=16,meta=meta,sha256=hashlib.sha256(sheet.tobytes()).hexdigest())
 # Diagnostic contact sheet of every pose, with no crop or per-pose rescaling.
 contact=Image.new('RGB',(1024,1104),'#15202b');d=ImageDraw.Draw(contact)
 for i in range(16):
  c=sheet.crop((i%4*576,i//4*576,(i%4+1)*576,(i//4+1)*576));c.thumbnail((256,256));px=i%4*256;py=i//4*276;contact.paste(c,(px,py),c);d.text((px+8,py+258),f'{name} {i}',fill='white')
 contact.save(W/'exports'/f'{name}-contact.png')
(W/'manifest.json').write_text(json.dumps(manifest,separators=(',',':')))
print(json.dumps({'banks':len(manifest),'poses':sum(v['count'] for v in manifest.values()),'source':'built-in GPT image generator; fixed-cell Aseprite normalization'},indent=2))
