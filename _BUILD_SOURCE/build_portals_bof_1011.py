"""Own the BOF redesign: authored pixels, physical aperture registration, fixed shell."""
from pathlib import Path
from collections import deque
from PIL import Image,ImageDraw
import numpy as np,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/portals_bof_1011/returned'
OUT=ROOT/'assets/game/shared/fx/portals_bof_1011';OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT/'_shots/portals_bof_1011';QA.mkdir(parents=True,exist_ok=True)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def components(mask):
 h,w=mask.shape;seen=np.zeros_like(mask);parts=[]
 for sy,sx in zip(*np.nonzero(mask)):
  if seen[sy,sx]:continue
  q=deque([(int(sx),int(sy))]);seen[sy,sx]=True;points=[]
  while q:
   x,y=q.popleft();points.append((x,y))
   for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=xx<w and 0<=yy<h and mask[yy,xx] and not seen[yy,xx]:seen[yy,xx]=True;q.append((xx,yy))
  parts.append(np.asarray(points))
 return parts
def aperture(im):
 a=np.asarray(im);h,w=a.shape[:2];yy,xx=np.indices((h,w))
 mask=(a[:,:,:3].max(axis=2)<7)&(a[:,:,3]>210)&(abs(xx-w/2)<w*.26)&(abs(yy-h/2)<h*.26)
 parts=[p for p in components(mask) if len(p)>80]
 assert parts,'No opaque black core found'
 p=min(parts,key=lambda p:np.linalg.norm(p.mean(axis=0)-[w/2,h/2]))
 center=p.mean(axis=0)
 return tuple(map(float,center)),dict(area=len(p),bounds=[int(p[:,0].min()),int(p[:,1].min()),int(p[:,0].max()+1),int(p[:,1].max()+1)])
def write(bank,i,im,pivot,**extra):
 assert im.width%2==im.height%2==0
 p=OUT/f'{bank}_{i:02d}.png';im.save(p,optimize=True)
 return dict(key=f'pr11b_{bank}_{i}',path=p.relative_to(ROOT).as_posix(),w=im.width,h=im.height,pivot=list(pivot),sha256=sha(p),**extra)

art={};registered={};cells={};analysis={}
files={'blue_rift':'blue.png','red_rift':'red.png','green_rift':'green.png','black_void':'black-void.png','gate_energy':'gate-energy-opaque.png'}
labels={'blue_rift':'Ion-blue rift','red_rift':'Crimson rift','green_rift':'Emerald rift','black_void':'Chromium singularity','gate_energy':'Fury gate membrane'}
for bank,filename in files.items():
 raw=Image.open(SRC/filename).convert('RGBA');records=[];frames=[];raws=[];edge_max=0
 for i in range(32):
  x,x1=[round(n*raw.width/4) for n in (i%4,i%4+1)]
  y,y1=[round(n*raw.height/8) for n in (i//4,i//4+1)]
  cell=raw.crop((x,y,x1,y1));(cx,cy),measure=aperture(cell)
  dx,dy=round(160-cx),round(160-cy)
  frame=Image.new('RGBA',(320,320));frame.paste(cell,(dx,dy))
  a=np.asarray(cell);edge=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
  source_edge=int(edge[:,3].max());edge_max=max(edge_max,source_edge)
  b=np.asarray(frame);border=np.concatenate([b[0],b[-1],b[:,0],b[:,-1]])
  assert border[:,3].max()==0,(bank,i,'padded border not clear')
  records.append(write(bank,i,frame,(160,160),source=filename,sourceRect=[x,y,x1-x,y1-y],
   sourceAnchor=[round(cx,5),round(cy,5)],translation=[dx,dy],scale=1,
   centerError=[round(cx+dx-160,5),round(cy+dy-160,5)],measurement=measure,sourceBorderAlphaMax=source_edge))
  frames.append(frame);raws.append(cell)
 assert len({r['sha256'] for r in records})==32
 art[bank]=dict(label=labels[bank],fps=24 if bank!='black_void' else 20,frames=records,role='component' if bank=='gate_energy' else 'animation')
 registered[bank]=frames;cells[bank]=raws
 analysis[bank]=dict(maxCenterError=max(max(abs(v) for v in r['centerError']) for r in records),sourceBorderAlphaMax=edge_max)

# Static authored machinery. The opening mask is derived from its negative
# space, with energy behind it; there is no per-frame hull fitting or warping.
raw=Image.open(SRC/'gate-shell.png').convert('RGBA');a=np.asarray(raw);h,w=a.shape[:2];axis=w//2
mask=np.zeros((h,w),dtype='uint8')
for y in range(round(h*.22),h):
 if a[y,axis,3]>70:continue
 ls=np.flatnonzero(a[y,:axis,3]>110);rs=np.flatnonzero(a[y,axis:,3]>110)
 if len(ls) and len(rs):
  left,right=int(ls[-1])+1,axis+int(rs[0])
  # The armored feet narrow the central opening. A quarter-width cutoff
  # incorrectly blanks its lower rows and leaves a floating energy panel.
  if right-left>w*.12:mask[y,left:right]=255
ys,xs=np.nonzero(mask);gate_anchor=((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)
shell_scale=.40;pivot=(256,352);offset=(round(256-gate_anchor[0]*shell_scale),round(352-gate_anchor[1]*shell_scale))
shell=Image.new('RGBA',(512,640));opening=Image.new('L',shell.size)
size=(round(w*shell_scale),round(h*shell_scale))
shell.paste(raw.resize(size,Image.Resampling.NEAREST),offset)
opening.paste(Image.fromarray(mask).resize(size,Image.Resampling.NEAREST),offset)
shell.save(OUT/'gate-shell.png');opening.save(OUT/'gate-aperture-mask.png')
frames=[];records=[];energy_scale=2.2
for i,cell in enumerate(cells['gate_energy']):
 cx,cy=art['gate_energy']['frames'][i]['sourceAnchor']
 off=(round(256-cx*energy_scale),round(352-cy*energy_scale))
 energy=Image.new('RGBA',shell.size)
 energy.paste(cell.resize((round(cell.width*energy_scale),round(cell.height*energy_scale)),Image.Resampling.NEAREST),off)
 ea=np.asarray(energy).copy();ea[:,:,3]=(ea[:,:,3].astype('uint16')*np.asarray(opening).astype('uint16')//255).astype('uint8')
 frame=Image.alpha_composite(Image.fromarray(ea),shell);frames.append(frame)
 records.append(write('amethyst_gate',i,frame,pivot,source='gate-shell.png + gate-energy-opaque.png',
  shellScale=shell_scale,shellOffset=list(offset),shellAnchor=list(gate_anchor),energyScale=energy_scale,energyOffset=list(off),
  centerError=[round(cx*energy_scale+off[0]-256,5),round(cy*energy_scale+off[1]-352,5)]))
art['amethyst_gate']=dict(label='Fury breach gate',fps=24,frames=records,role='animation',components=['gate-shell.png','gate-aperture-mask.png','gate_energy'])
registered['amethyst_gate']=frames
analysis['amethyst_gate']=dict(maxCenterError=max(max(abs(v) for v in r['centerError']) for r in records),shellFixed=True)

main=['amethyst_gate','black_void','blue_rift','red_rift','green_rift']
for bank,frames in registered.items():
 fw,fh=frames[0].size;sheet=Image.new('RGBA',(fw*4,fh*8))
 for i,frame in enumerate(frames):sheet.paste(frame,(i%4*fw,i//4*fh))
 sheet.save(OUT/(bank+'-sheet.png'),optimize=True)
 art[bank]['sheet']=dict(path=(OUT/(bank+'-sheet.png')).relative_to(ROOT).as_posix(),columns=4,rows=8,cell=[fw,fh])
 # Measure real displayed change over a dark field, not invisible RGB in alpha.
 displayed=[]
 for frame in frames:
  back=Image.new('RGBA',frame.size,'#0d1720');displayed.append(np.asarray(Image.alpha_composite(back,frame)).astype('float32'))
 dist=[float(np.abs(displayed[i]-displayed[(i+1)%32]).mean()) for i in range(32)]
 analysis[bank].update(seamChange=round(dist[-1],4),medianFrameChange=round(float(np.median(dist[:-1])),4),seamToMedian=round(dist[-1]/max(.001,float(np.median(dist[:-1]))),3))
 contact=Image.new('RGB',(1024,8*284),'#0d1720');draw=ImageDraw.Draw(contact)
 for i,frame in enumerate(frames):
  field=Image.new('RGBA',frame.size,'#0d1720')
  for j,opacity in [((i-1)%32,.28),((i+1)%32,.28),(i,.78)]:
   layer=frames[j].copy();layer.putalpha(layer.getchannel('A').point(lambda v:round(v*opacity)))
   field=Image.alpha_composite(field,layer)
  k=min(240/fw,248/fh);thumb=field.resize((round(fw*k),round(fh*k)),Image.Resampling.NEAREST)
  x=i%4*256+(256-thumb.width)//2;y=i//4*284+28;contact.paste(thumb.convert('RGB'),(x,y))
  px=x+art[bank]['frames'][0]['pivot'][0]*k;py=y+art[bank]['frames'][0]['pivot'][1]*k
  draw.line((px-5,py,px+5,py),fill='#91ffc1');draw.line((px,py-5,px,py+5),fill='#91ffc1');draw.text((i%4*256+12,i//4*284+8),f'{i+1:02d}/32',fill='#d8e7ee')
 contact.save(QA/(bank+'-onion.png'))
 if bank in main:frames[0].save(OUT/(bank+'.webp'),save_all=True,append_images=frames[1:],duration=round(1000/art[bank]['fps']),loop=0,lossless=True,method=3)

manifest=dict(generator='built-in image_gen',revision='bof-material-redesign',main=main,art=art,alignment=analysis,
 sources={p.name:sha(p) for p in SRC.glob('*.png')},prompts='_ART_SOURCES/portals_bof_1011/prompts.json',
 repairPrompt='_ART_SOURCES/portals_bof_1011/core-opacity-repair.json',styleReferences='_ART_SOURCES/portals_bof_1011/reference/sources.json',
 rules='Even fixed canvases, opaque aperture registration, integer translation, common scale. Native alpha preserved; authored static gate shell. No synthetic poses.',
 supersedes='portals_1011 artwork; original reference-literal pack retained separately',status='generated-review-pack')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
(ROOT/'assets/portal_bof_art_1011.js').write_text('"use strict";\n// Owned by build_portals_bof_1011.py.\nconst PR11B_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(QA/'alignment.json').write_text(json.dumps(analysis,indent=2)+'\n',encoding='utf-8',newline='\n')
tax=ROOT/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8'))
data['pr11b_']=dict(role='bof_plasma_chromium_and_armored_portal_review_pack',sheet=None,
 note='October11 BOF-style redesign after Mike rejected GIF copies. Five32-frame loops: angular blue/red/emerald plasma rifts, black/chrome alien singularity with purple/green veins, and armored Fury breach gate with a static generated shell plus32 purple membrane poses. Main160 plus32 component frames. All320x320/pivot160,160 except gate512x640/pivot256,352. Native alpha, physical black-aperture registration, common proportional scale. Source prompts and actual BOF style references _ART_SOURCES/portals_bof_1011. Owner build_portals_bof_1011.py registers pixels, sheets, manifest and portal_bof_art_1011.js together. Supersedes only the portal review art; no live encounter assignment. Review docs/previews/portals_1011; QA docs/qa/portals_bof_1011.json.')
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(analysis),flush=True)
