"""Export an actual PixelLab ocean animation; fixed geometry, one GPU texture.
Spatial overlap, when requested, is identical for every frame. No generated pose
is duplicated to fake motion, and no temporal interpolation is added.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,re,argparse,math
R=Path(__file__).resolve().parents[1]
A=R/'_ART_SOURCES/stormglass_water_pixellab_1020'
D=R/'assets/game/levels/tutorial/stormglass_1020/water'
Q=R/'_shots/stormglass_water_pixellab_1020'
ap=argparse.ArgumentParser();ap.add_argument('--overlap',type=int,default=32);args=ap.parse_args()
for p in [A,D,Q]:p.mkdir(parents=True,exist_ok=True)
def natural(p):return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',p.name)]
paths=sorted((A/'frames').glob('*.png'),key=natural)
assert 24<=len(paths)<=40,('Unexpected raw frame count',len(paths))
raw=[np.array(Image.open(p).convert('RGBA')) for p in paths]
assert all(a.shape==(256,256,4) for a in raw),'PixelLab bank must retain its native common256-square canvas'
assert all(a[:,:,3].min()==255 for a in raw),'Opaque ocean cannot contain cutout holes'
indices=list(range(len(raw)))
endpoint_removed=False
input_removed=False
if len(raw)>32 and np.array_equal(raw[0],raw[-1]):
 raw.pop();indices.pop();endpoint_removed=True
elif len(raw)==33:
 # PixMiniMax returns the unchanged input at0 followed by the32 generated poses.
 # Keep the complete generated bank; exclude only its separate input/reference image.
 raw.pop(0);indices.pop(0);input_removed=True
assert len(raw)==32,('Expected32 generated source poses',len(raw))
assert len({hashlib.sha256(a.tobytes()).hexdigest() for a in raw})>=30,'Animation must contain real distinct poses'
def overlap_axis(a,n,axis):
 if n==0:return a
 a=np.moveaxis(a,axis,0);length=a.shape[0]-n
 out=a[:length].astype(np.float32).copy();weight=np.linspace(0,1,n,dtype=np.float32)[:,None,None]
 out[:n]=a[length:]*(1-weight)+a[:n]*weight
 return np.moveaxis(np.rint(out).astype(np.uint8),0,axis)
assert args.overlap%2==0 and 0<=args.overlap<=48
frames=[overlap_axis(overlap_axis(a,args.overlap,1),args.overlap,0) for a in raw]
N=len(frames);H,W=frames[0].shape[:2];assert W%2==H%2==0
PAD=2;STRIDE=W+PAD*2;COLS=8 if STRIDE*8<=2048 else 6;ROWS=math.ceil(N/COLS)
atlas=Image.new('RGBA',(COLS*STRIDE,ROWS*STRIDE));cells=[]
for i,a in enumerate(frames):
 im=Image.fromarray(a);x=(i%COLS)*STRIDE+PAD;y=(i//COLS)*STRIDE+PAD;atlas.paste(im,(x,y))
 # An even gutter with two pixels of edge extrusion prevents neighboring poses bleeding.
 for j in range(1,PAD+1):
  atlas.paste(im.crop((0,0,1,H)),(x-j,y));atlas.paste(im.crop((W-1,0,W,H)),(x+W-1+j,y))
  atlas.paste(im.crop((0,0,W,1)),(x,y-j));atlas.paste(im.crop((0,H-1,W,H)),(x,y+H-1+j))
 for dx in [-2,-1,W,W+1]:
  for dy in [-2,-1,H,H+1]:atlas.putpixel((x+dx,y+dy),im.getpixel((0 if dx<0 else W-1,0 if dy<0 else H-1)))
 cells.append([x,y,W,H])
atlas.save(D/'ocean.webp',lossless=True,method=6)
meta={'key':'sgw20_ocean','path':'assets/game/levels/tutorial/stormglass_1020/water/ocean.webp',
 'frames':N,'width':W,'height':H,'columns':COLS,'fps':12,'pivot':[W//2,H//2],
 'sheet_width':atlas.width,'sheet_height':atlas.height,'cells':cells,'revision':'pixellab-water-1020',
 'generator':'PixelLab PixMiniMax','seed_job':'09d1b679-e3a5-4506-8be8-011ac609a5c5',
 'animation_job':'afa80ee9-340a-4002-8fff-90a9f79a0d69','source_indices':indices}
(D/'ocean.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
registration="'use strict';\n/* Generated with the ocean atlas by build_stormglass_water_1020.py. */\nconst SG20_WATER="+json.dumps(meta,separators=(',',':'))+";\nXART._src[SG20_WATER.key]=SG20_WATER.path;\nwindow.BOF_STORMGLASS_WATER=SG20_WATER;\n"
(R/'assets/stormglass_water_art_1020.js').write_text(registration,encoding='utf-8',newline='\n')
def seam(a):
 v=a[:,:,:3].astype(float)
 inside=float((np.abs(np.diff(v,axis=0)).mean()+np.abs(np.diff(v,axis=1)).mean())/2)
 return {'horizontal':float(np.abs(v[0]-v[-1]).mean()),'vertical':float(np.abs(v[:,0]-v[:,-1]).mean()),'interior':inside}
def temporal(bank):
 return [float(np.abs(a[:,:,:3].astype(float)-bank[(i+1)%len(bank)][:,:,:3]).mean()) for i,a in enumerate(bank)]
motion=temporal(frames)
audit={'source_size':[256,256],'delivered_size':[W,H],'source_count':len(paths),'frames':N,
 'identical_endpoint_removed':endpoint_removed,'separate_input_reference_removed':input_removed,'overlap_pixels':args.overlap,'scale':1,
 'normalization':'fixed spatial overlap only; no per-frame fitting, phase shuffling, fake duplicates or temporal interpolation',
 'raw_seams':[seam(a) for a in raw],'exported_seams':[seam(a) for a in frames],
 'temporal_mean_absolute_deltas':motion,'unique_frames':len({hashlib.sha256(a.tobytes()).hexdigest() for a in frames}),
 'average_brightness':[float(a[:,:,:3].mean()) for a in frames],
 'runtime_bytes':(D/'ocean.webp').stat().st_size+len(registration.encode()),
 'sheet':[atlas.width,atlas.height],'seed_job':meta['seed_job'],'animation_job':meta['animation_job']}
(A/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
contact=Image.new('RGB',(8*128,4*146),'#07131c');draw=ImageDraw.Draw(contact)
for i,a in enumerate(frames):
 im=Image.fromarray(a).convert('RGB').resize((128,128),Image.Resampling.NEAREST)
 contact.paste(im,((i%8)*128,(i//8)*146));draw.text(((i%8)*128+4,(i//8)*146+130),str(i),fill='#d5e7dc')
contact.save(Q/'all-frames.png')
preview=[Image.fromarray(a).convert('RGB') for a in frames]
preview[0].save(Q/'water-loop.gif',save_all=True,append_images=preview[1:],duration=83,loop=0,optimize=False)
grid=Image.new('RGB',(W*2,H*2))
for x in range(2):
 for y in range(2):grid.paste(preview[0],(x*W,y*H))
grid.save(Q/'tile-seams.png')
print(json.dumps({k:v for k,v in audit.items() if k not in ['raw_seams','exported_seams','average_brightness','temporal_mean_absolute_deltas']}))
print(json.dumps({'wrap_delta':motion[-1],'mean_delta':float(np.mean(motion)),'max_delta':max(motion),'brightness_range':max(audit['average_brightness'])-min(audit['average_brightness']),
 'mean_seam':{k:float(np.mean([q[k] for q in audit['exported_seams']])) for k in ['horizontal','vertical','interior']}}))
