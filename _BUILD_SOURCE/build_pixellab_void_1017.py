"""Export PixelLab's genuine animation frames with fixed physical pivots.

One common proportional scale per clip, no per-frame fitting, reversed
closures or synthesized tween poses. The
one-shot endpoints are transparent / shared open plates for exact joins.
"""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image,ImageDraw
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/pixellab_void_1017'
OUT=ROOT/'assets/game/shared/fx/pixellab_void_1017'
QA=ROOT/'_shots/pixellab_void_1017/export'
parser=argparse.ArgumentParser();parser.add_argument('--partial',action='store_true');args=parser.parse_args()
OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
art={'portals':{},'arenas':[],'code':[],'wind':{}};audit={};arenaAudit=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(key,p,im,pivot):
 assert im.width%2==im.height%2==0
 return dict(key=key,path=p.relative_to(ROOT).as_posix(),w=im.width,h=im.height,pivot=list(pivot),sha256=sha(p))
def source(name):
 files=sorted((SRC/'returned'/name).glob('frame_*.png'))
 assert files,name+' has no frames'
 return [Image.open(p).convert('RGBA') for p in files]
def clip(name):
 alternate=name.rsplit('-',1)[0]+'-standard-'+name.rsplit('-',1)[1]
 chosen=alternate if (SRC/'returned'/alternate).exists() else name
 frames=source(chosen)
 if len(frames) in [17,33]:frames=frames[1:] # PixelLab's unchanged input is not a generated pose.
 assert len(frames) in [16,32],(chosen,len(frames))
 assert len({im.size for im in frames})==1,(chosen,'changing source canvas')
 return frames
def pivot(im):
 a=np.asarray(im);h,w=a.shape[:2];y,x=np.indices((h,w));cx=w/2;cy=h/2
 roi=(abs(x-cx)<w*.24)&(abs(y-cy)<h*.24)
 # Register the primary physical silhouette, not a black-luminance contour
 # that shifts as energy filaments travel across the aperture.
 mask=(a[:,:,3]>128)
 yy,xx=np.where(mask)
 if len(xx):
  nearest=int(np.argmin((xx-cx)**2+(yy-cy)**2));binary=Image.fromarray(mask.astype('uint8')).copy()
  ImageDraw.floodfill(binary,(int(xx[nearest]),int(yy[nearest])),2)
  py0,px0=np.where(np.asarray(binary)==2)
  if len(px0)>=30:
   px,py=float(px0.mean()),float(py0.mean())
   if abs(px-cx)<w*.14 and abs(py-cy)<h*.14:return round(px),round(py),'primary alpha component'
 hot=a[:,:,:3].max(2).astype(float)*a[:,:,3]/255
 hot=np.where((abs(x-cx)<w*.10)&(abs(y-cy)<h*.10),hot,0)
 mask=hot>max(25,float(hot.max())*.75)
 if mask.any():
  yy,xx=np.where(mask);return round(float(np.average(xx,weights=hot[mask]))),round(float(np.average(yy,weights=hot[mask]))),'ignition'
 return round(cx),round(cy),'canvas'
def registered(im):
 assert im.width==im.height and im.width%2==0 and im.width<=256,im.size
 # Some animation outputs accidentally key the enclosed black throat away.
 # Restore only that bounded central transparency component; preserve every
 # exterior alpha pixel and all authored metal/energy pixels verbatim.
 a=np.asarray(im).copy();outside=Image.fromarray((a[:,:,3]<16).astype('uint8')).copy()
 ImageDraw.floodfill(outside,(0,0),255);cx=im.width//2;cy=im.height//2;fixed=0
 if outside.getpixel((cx,cy))==1:
  ImageDraw.floodfill(outside,(cx,cy),2);hole=np.asarray(outside)==2
  if int(hole.sum())>30:
   a[hole,:3]=0;a[hole,3]=255;fixed=int(hole.sum());im=Image.fromarray(a)
 scale=256/im.width
 if im.width!=256:im=im.resize((256,256),Image.Resampling.NEAREST)
 x,y,method=pivot(im);out=Image.new('RGBA',(320,320));out.paste(im,(160-x,160-y))
 return out,{'sourcePivot':[x,y],'translation':[160-x,160-y],'anchor':method,'scale':scale,'restoredApertureAlphaPixels':fixed}

def void_palette(im):
 # Mike requested the approved rift animation with a purple/black palette.
 # Rotate only saturated blue/cyan energy onto a violet chroma axis. Keep
 # luminance, neutral chrome, black apertures and alpha exactly registered.
 a=np.asarray(im).copy();rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);chroma=hi-lo
 mask=(a[:,:,3]>0)&(hi>20)&(chroma>=hi*.30)&(rgb[:,:,2]-rgb[:,:,0]>=hi*.25)&(rgb[:,:,2]>=rgb[:,:,1]*.85)
 weights=np.array([.2126,.7152,.0722]);y=rgb@weights;violet=np.array([2/3,0.,1.]);axis=violet-violet@weights
 limit=np.full(y.shape,np.inf)
 for c,d in enumerate(axis):limit=np.minimum(limit,(255-y)/d if d>0 else -y/d)
 k=np.maximum(0,np.minimum(chroma,limit));mapped=np.rint(np.clip(y[:,:,None]+k[:,:,None]*axis,0,255)).astype('uint8')
 a[:,:,:3][mask]=mapped[mask]
 assert np.array_equal(a[:,:,3],np.asarray(im)[:,:,3])
 assert float(abs((a[:,:,:3].astype(float)-rgb)@weights).max())<=.51
 return Image.fromarray(a)
def preview(name,frames):
 sheet=Image.new('RGB',(8*160,4*180),'#111c27');g=ImageDraw.Draw(sheet)
 for i,im in enumerate(frames):
  p=im.resize((160,160),Image.Resampling.NEAREST);sheet.paste(p,(i%8*160,i//8*180+20),p);g.text((i%8*160+5,i//8*180+5),str(i),fill='#b3d5e8')
 sheet.save(QA/(name+'-contact.png'))
 onion=Image.new('RGBA',frames[0].size)
 for i in sorted({round(q*(len(frames)-1)) for q in [0,.25,.5,.75,1]}):
  layer=frames[i].copy();layer.putalpha(layer.getchannel('A').point(lambda a:round(a*.22)));onion=Image.alpha_composite(onion,layer)
 onion.save(QA/(name+'-onion.png'))
 frames[0].save(QA/(name+'-first.png'))
 frames[0].save(QA/(name+'.gif'),save_all=True,append_images=frames[1:],duration=60,loop=0,disposal=2)

for bank in ['blue_rift','red_rift','green_rift','black_void']:
 sourceBank='blue_rift' if bank=='black_void' else bank
 if args.partial:
  try:
   for ph in ['form','loop','close']:clip(sourceBank+'-'+ph)
  except (AssertionError,FileNotFoundError):continue
 seed,seedInfo=registered(clip(sourceBank+'-loop')[0]);entry={'fps':len(clip(sourceBank+'-loop'))/1.6,'scaleWidth':256};audit[bank]={}
 if bank=='black_void':entry['derivedFrom']='blue_rift';entry['palette']='purple_black_luminance_preserved'
 for phase in ['form','loop','close']:
  raw=clip(sourceBank+'-'+phase);frames=[];records=[];n=len(raw)
  for im in raw:
   out,info=registered(im);frames.append(out);records.append(info)
  if phase=='loop':frames[0]=seed.copy();records[0]=seedInfo
  elif phase=='form':frames[0]=Image.new('RGBA',(320,320));frames[-1]=seed.copy();records[-1]=seedInfo
  else:frames[0]=seed.copy();frames[-1]=Image.new('RGBA',(320,320));records[0]=seedInfo
  if bank=='black_void':frames=[void_palette(im) for im in frames]
  assert len({im.tobytes() for im in frames})>=16,(bank,phase,'insufficient genuine poses')
  cells=[]
  for i,im in enumerate(frames):
   a=np.asarray(im);assert not np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])[:,3].any(),(bank,phase,i,'edge')
   stem='void_rift' if bank=='black_void' else bank
   dest=OUT/(stem+'_'+phase+'_'+str(i).zfill(2)+'.png');im.save(dest,optimize=True)
   cells.append(record('pxv17_'+stem+'_'+phase+'_'+str(i),dest,im,[160,160]))
  entry[phase]={'fps':n/1.6,'frames':cells};audit[bank][phase]=records;preview(bank+'-'+phase,frames)
 art['portals'][bank]=entry
for i in range(3):
 im=source('arena2-open-seed' if i==2 else 'arena'+str(i)+'-seed')[0];assert im.size in [(512,512),(400,400)],im.size
 scale=512/im.width;arenaAudit.append({'phase':i,'sourceSize':list(im.size),'scale':scale,'pivot':[256,256]})
 # A smaller opaque backdrop needs one proportional scale, not black side
 # padding whose hard edges would frame the supposedly boundless void.
 if im.size!=(512,512):im=im.resize((512,512),Image.Resampling.NEAREST)
 bg=Image.new('RGBA',(512,512),'black');bg.alpha_composite(im);dest=OUT/('arena_'+str(i)+'.png');bg.save(dest,optimize=True)
 art['arenas'].append(record('pxv17_arena_'+str(i),dest,bg,[256,256]))
raw=clip('code-loop')
frames=[]
for i,im in enumerate(raw):
 assert im.size in [(192,192),(128,128)],im.size
 padded=Image.new('RGBA',(256,256));padded.paste(im,((256-im.width)//2,(256-im.height)//2));dest=OUT/('code_'+str(i).zfill(2)+'.png');padded.save(dest,optimize=True);frames.append(padded)
 art['code'].append(record('pxv17_code_'+str(i),dest,padded,[128,128]))
preview('code-loop',frames)
for family,name in [('bullets','windBullets'),('spread','windSpread'),('heavy','windHeavy')]:
 if args.partial and not (SRC/'returned'/(name+'-loop')).exists():continue
 raw=clip(name+'-loop');assert len(raw)==16 and all(im.size==(64,64) for im in raw)
 boxes=[im.getbbox() for im in raw if im.getbbox()];bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
 span=max(bounds[2]-bounds[0],bounds[3]-bounds[1]);cells=[]
 for i,im in enumerate(raw):
  dest=OUT/(name+'_'+str(i).zfill(2)+'.png');im.save(dest,optimize=True);a=record('pxv17_'+name+'_'+str(i),dest,im,[32,32]);a.update(span=span,bounds=bounds,sx=0,sy=0,fps=16);cells.append(a)
 art['wind'][family]=cells;preview(name+'-loop',raw)
(ROOT/'assets/pixellab_void_art_1017.js').write_text('"use strict";\n// Generated by build_pixellab_void_1017.py.\nconst PXV17_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
manifest={'provider':'PixelLab','source':'_ART_SOURCES/pixellab_void_1017','processing':'One common proportional scale per animation (256/sourceWidth), integer anchor translations, shared transparent padding, exact shared open plate and transparent one-shot endpoints. Unchanged reference input excluded from generated clips. Opaque arena plates use one proportional scale to512x512, without side padding.','audit':audit,'arenaNormalization':arenaAudit,'art':art}
(SRC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
tax=ROOT/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8'))
data['pxv17_']={'role':'pixellab_stage7_stage8_portal_lifecycles_three_void_arenas_and_compact_wind_rounds','sheet':None,'note':'Four separate16–32-pose form/loop/close portal families, three512x512 open dark arenas,16 authored code-parallax poses and three16-pose compact Wind round families. Actual PixelLab frames on even320x320,256x256 and64x64 canvases, fixed center pivots, one common proportional scale per animation. Runtime pixellab_void_1017; owning exporter build_pixellab_void_1017.py. No reversed closure, per-frame stretching or combat changes.'}
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Exported',sum(len(e[p]['frames']) for e in art['portals'].values() for p in ['form','loop','close']),'portal poses,',len(art['code']),'code poses,',sum(len(b) for b in art['wind'].values()),'Wind poses and 3 arena plates with shared pivots.')
