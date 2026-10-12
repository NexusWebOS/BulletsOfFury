"""Own new portal forming/closing art; keep approved loop pixels unchanged."""
from pathlib import Path
from PIL import Image,ImageDraw
from collections import deque
import numpy as np,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/portal_lifecycle_1011/returned'
OLD=ROOT/'assets/game/shared/fx/portals_bof_1011'
OUT=ROOT/'assets/game/shared/fx/portal_lifecycle_1011'
QA=ROOT/'_shots/portal_lifecycle_1011'
for p in [OUT,QA]:p.mkdir(parents=True,exist_ok=True)
old=json.loads((OLD/'manifest.json').read_text(encoding='utf-8'))
main=old['main'];art={};measurements={}
CANVAS=384;PIVOT=192

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parts(mask):
 h,w=mask.shape;seen=np.zeros_like(mask);out=[]
 for y,x in zip(*np.nonzero(mask)):
  if seen[y,x]:continue
  q=deque([(int(x),int(y))]);seen[y,x]=True;pts=[]
  while q:
   xx,yy=q.popleft();pts.append((xx,yy))
   for nx,ny in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)]:
    if 0<=nx<w and 0<=ny<h and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;q.append((nx,ny))
  out.append(np.asarray(pts))
 return out

def anchor(im,prefer_ignition=False):
 a=np.asarray(im);h,w=a.shape[:2];yy,xx=np.indices((h,w));roi=(abs(xx-w/2)<w*.23)&(abs(yy-h/2)<h*.23)
 power=a[:,:,:3].min(2).astype(float)*a[:,:,3]/255
 core=(abs(xx-w/2)<w*.11)&(abs(yy-h/2)<h*.11)
 peak=float(np.where(core,power,0).max())
 dark=(a[:,:,:3].max(2)<8)&(a[:,:,3]>210)&roi
 holes=[] if prefer_ignition else [p for p in parts(dark) if len(p)>=80 and np.linalg.norm(p.mean(0)-[w/2,h/2])<w*.12]
 if holes:
  p=min(holes,key=lambda p:np.linalg.norm(p.mean(0)-[w/2,h/2]))
  return tuple(p.mean(0)),'opaque aperture'
 if peak>120:
  bright=core&(power>=peak*.8);p=np.argwhere(bright);weights=power[bright]
  return (float(np.average(p[:,1],weights=weights)),float(np.average(p[:,0],weights=weights))),'central ignition'
 # Before/after the hole exists, the central hot ignition/implosion is the
 # physical anchor. Ignore distant sparks and low-alpha RGB in the source.
 power=np.where(roi,power,0);peak=power.max()
 if peak>12:
  bright=power>=max(peak*.8,12);p=np.argwhere(bright)
  weights=power[bright];return (float(np.average(p[:,1],weights=weights)),float(np.average(p[:,0],weights=weights))),'central ignition'
 return (w/2,h/2),'empty cell center'

def bounds(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>128)
 return [int(x.max()-x.min()+1),int(y.max()-y.min()+1)] if len(x) else [0,0]
def write(bank,phase,i,im,pivot,**meta):
 p=OUT/f'{bank}_{phase}_{i:02d}.png';im.save(p,optimize=True)
 return dict(key=f'pl11_{bank}_{phase}_{i}',path=p.relative_to(ROOT).as_posix(),w=im.width,h=im.height,pivot=list(pivot),sha256=sha(p),**meta)

for bank,raw_name in [('blue_rift','blue'),('red_rift','red'),('green_rift','green'),('black_void','black_void'),('gate_energy','gate_energy')]:
 art[bank]={'label':old['art'][bank]['label'],'fps':old['art'][bank]['fps'],'scaleWidth':320}
 loops=[]
 for i,f in enumerate(old['art'][bank]['frames']):
  im=Image.new('RGBA',(CANVAS,CANVAS));im.paste(Image.open(ROOT/f['path']).convert('RGBA'),(32,32))
  loops.append(write(bank,'loop',i,im,(PIVOT,PIVOT),source=f['path'],padding=[32,32],sourceSha256=f['sha256']))
 art[bank]['loop']={'fps':art[bank]['fps'],'frames':loops,'playback':'loop'}
 seed=Image.open(ROOT/loops[0]['path']).convert('RGBA');target=bounds(seed)
 for phase in ['form','close']:
  file=SRC/f'{raw_name}_{phase}.png';raw=Image.open(file).convert('RGBA');source=[];rects=[]
  for i in range(32):
   x,x1=[round(v*raw.width/4) for v in [i%4,i%4+1]];y,y1=[round(v*raw.height/8) for v in [i//4,i//4+1]]
   source.append(raw.crop((x,y,x1,y1)));rects.append([x,y,x1-x,y1-y])
  endpoint=31 if phase=='form' else 0
  # One proportional scale for the entire phase, measured at its full-open
  # endpoint. Tiny forming/collapsing poses are NEVER independently enlarged.
  source_bounds=bounds(source[endpoint]);scale=sum(target)/sum(source_bounds)
  frames=[];records=[]
  for i,cell in enumerate(source):
   # Once the visible throat pinches shut, anchor the hot implosion, not an
   # off-center black crevice between the remaining chrome/plasma ribbons.
   switch={'black_void':15,'gate_energy':12}.get(bank,18)
   (cx,cy),method=anchor(cell,phase=='close' and i>=switch)
   if bank=='gate_energy' and phase=='close' and 7<=i<=11:
    # Onion review of the native 887x1774 sheet: the narrowing throat is
    # around (112,127), below brighter lightning. Follow its remaining black
    # pixels, then its ignition in this measured local window.
    a=np.array(cell);yy,xx=np.indices(a.shape[:2]);zone=(abs(xx-112)<=7)&(abs(yy-127)<=7)
    dark=zone&(a[:,:,:3].max(2)<8)&(a[:,:,3]>210)
    if dark.any():cy,cx=map(float,np.argwhere(dark).mean(0))
    else:
     power=a[:,:,:3].min(2).astype(float)*a[:,:,3]/255;power=np.where(zone,power,0)
     points=np.argwhere(power>=power.max()*.8);cy,cx=map(float,points.mean(0))
    method='measured narrowing gate throat'
   scaled=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST)
   dx,dy=round(PIVOT-cx*scale),round(PIVOT-cy*scale)
   im=Image.new('RGBA',(CANVAS,CANVAS));im.paste(scaled,(dx,dy))
   lock=None
   if i==endpoint:im=seed.copy();lock='approved loop frame 0'
   if phase=='close' and i==31:im=Image.new('RGBA',(CANVAS,CANVAS));lock='terminal transparent frame'
   a=np.array(im);border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
   assert border[:,3].max()==0,(bank,phase,i,'canvas clipping')
   records.append(write(bank,phase,i,im,(PIVOT,PIVOT),source=file.relative_to(ROOT).as_posix(),sourceRect=rects[i],
    sourceAnchor=[round(cx,5),round(cy,5)],anchorMethod=method,scale=round(scale,7),translation=[dx,dy],
    centerError=[round(cx*scale+dx-PIVOT,5),round(cy*scale+dy-PIVOT,5)],endpointLock=lock))
   frames.append(im)
  art[bank][phase]={'fps':art[bank]['fps'],'frames':records,'playback':'once','duration':32/art[bank]['fps']}
  measurements[f'{bank}_{phase}']={'scale':scale,'maxCenterError':max(max(abs(v) for v in f['centerError']) for f in records),
   'sourceSize':list(raw.size),'sourceSha256':sha(file),'uniqueCells':len({im.tobytes() for im in frames})}

shell=Image.open(OLD/'gate-shell.png').convert('RGBA');mask=Image.open(OLD/'gate-aperture-mask.png').convert('L')
art['amethyst_gate']={'label':'Fury breach gate','fps':24,'scaleWidth':512,'loop':old['art']['amethyst_gate']}
for phase in ['form','close']:
 records=[]
 for i,f in enumerate(art['gate_energy'][phase]['frames']):
  energy=Image.open(ROOT/f['path']).convert('RGBA').resize((round(CANVAS*2.2),round(CANVAS*2.2)),Image.Resampling.NEAREST)
  canvas=Image.new('RGBA',shell.size);canvas.paste(energy,(round(256-PIVOT*2.2),round(352-PIVOT*2.2)));a=np.array(canvas).copy()
  a[:,:,3]=(a[:,:,3].astype('uint16')*np.array(mask).astype('uint16')//255).astype('uint8')
  im=Image.alpha_composite(Image.fromarray(a),shell)
  if (phase=='form' and i==31) or (phase=='close' and i==0):im=Image.open(OLD/'amethyst_gate_00.png').convert('RGBA')
  if phase=='close' and i==31:im=shell.copy()
  records.append(write('amethyst_gate',phase,i,im,(256,352),component=f['key'],energyScale=2.2,shellFixed=True))
 art['amethyst_gate'][phase]={'fps':24,'frames':records,'playback':'once','duration':32/24}

for bank,entry in art.items():
 for phase in ['form','loop','close']:
  clip=entry[phase];frames=[Image.open(ROOT/f['path']).convert('RGBA') for f in clip['frames']];w,h=frames[0].size
  sheet=Image.new('RGBA',(w*4,h*8))
  for i,im in enumerate(frames):sheet.paste(im,(i%4*w,i//4*h))
  sheet_path=OUT/f'{bank}_{phase}-sheet.png';sheet.save(sheet_path,optimize=True)
  clip['sheet']={'path':sheet_path.relative_to(ROOT).as_posix(),'columns':4,'rows':8,'cell':[w,h]}
  webp=OUT/f'{bank}_{phase}.webp';frames[0].save(webp,save_all=True,append_images=frames[1:],duration=round(1000/clip['fps']),loop=0 if phase=='loop' else 1,lossless=True,method=3)
  clip['webp']=webp.relative_to(ROOT).as_posix()
  # Inspect all neighbours, clamped for one-shots (never wrap close to open).
  contact=Image.new('RGB',(1024,8*280),'#0d1720');d=ImageDraw.Draw(contact)
  for i,im in enumerate(frames):
   field=Image.new('RGBA',im.size,'#0d1720')
   for j,opacity in [(max(0,i-1),.25),(min(31,i+1),.25),(i,.8)]:
    layer=frames[j].copy();layer.putalpha(layer.getchannel('A').point(lambda v:round(v*opacity)));field=Image.alpha_composite(field,layer)
   k=min(240/w,248/h);thumb=field.resize((round(w*k),round(h*k)),Image.Resampling.NEAREST)
   x=i%4*256+(256-thumb.width)//2;y=i//4*280+24;contact.paste(thumb.convert('RGB'),(x,y))
   px=x+clip['frames'][i]['pivot'][0]*k;py=y+clip['frames'][i]['pivot'][1]*k
   d.line((px-4,py,px+4,py),fill='#85ffb4');d.line((px,py-4,px,py+4),fill='#85ffb4');d.text((i%4*256+8,i//4*280+6),f'{phase} {i+1:02d}',fill='#bed0dc')
  contact.save(QA/f'{bank}_{phase}-onion.png')

manifest={'generator':'built-in image_gen','main':main,'art':art,'measurements':measurements,
 'rules':'Fixed even canvases; common scale per phase; aperture/ignition registration; native alpha; exact approved join pose; terminal blank. Gate shell stays fixed.',
 'loopSource':'assets/game/shared/fx/portals_bof_1011/manifest.json','prompts':'_ART_SOURCES/portal_lifecycle_1011/prompts.json',
 'owner':'_BUILD_SOURCE/build_portal_lifecycle_1011.py'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
(ROOT/'assets/portal_lifecycle_art_1011.js').write_text('"use strict";\n// Owned by build_portal_lifecycle_1011.py.\nconst PL11_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
tax=ROOT/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8'))
data['pl11_']={'role':'portal_form_and_close','sheet':None,'note':'32 forming and 32 separately generated closing cells for the approved BOF blue/red/green rifts, black chromium singularity and armored Fury gate. Stable pivots and common phase scale; fixed gate shell. Approved loop pixels remain pr11b_. Owner build_portal_lifecycle_1011.py. Runtime portal_lifecycle_1011.js shares continuous playback with preview and Stage 8.'}
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(measurements),flush=True)
