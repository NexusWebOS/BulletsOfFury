"""Normalize authored full poses, share the game's fire ramp, and bake collision masks."""
from pathlib import Path
from PIL import Image,ImageSequence
import numpy as np,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/game/player_weapons/fire_whip_lash_0923'
def lum(a):return a[...,0]*.299+a[...,1]*.587+a[...,2]*.114
# Use real game colors: fire-orb gold core and flamethrower orange shadows.
refs=[np.asarray(Image.open(OUT/(n+'_palette.png')).convert('RGBA')) for n in ['fireorb','flamethrower']]
pool=np.concatenate([a[a[:,:,3]>200,:3] for a in refs]).astype(float)
colors,counts=np.unique(pool,axis=0,return_counts=True);light=lum(colors)
ramp=[]
for level in range(256):
 target=min(224,level)
 # Prefer the orb's saturated fire highlights to a pink-white muzzle core.
 score=np.abs(light-target)*4+colors[:,2]*.035-np.log1p(counts)*.2
 ramp.append(colors[np.argmin(score)].astype('uint8'))
ramp=np.array(ramp,dtype='uint8')
def recolor(im):
 a=np.array(im.convert('RGBA'));a[:,:,3][a[:,:,3]<=12]=0
 value=np.clip(np.rint(lum(a[:,:,:3].astype(float))),0,255).astype(int)
 a[:,:,:3]=ramp[value];return Image.fromarray(a)
frames=[];poses=[];maxreach=0
for i,raw in enumerate(ImageSequence.Iterator(Image.open(OUT/'animation.webp'))):
 im=recolor(raw);a=np.array(im);solid=a[:,:,3]>96;ys,xs=np.where(solid)
 # Emission bulb is the wide bright region in the lowest twelve ink rows.
 bottom=int(ys.max());rootmask=solid.copy();rootmask[:bottom-10]=False
 ry,rx=np.where(rootmask);weights=lum(a[ry,rx,:3].astype(float))
 root=[float(np.average(rx,weights=weights)),float(bottom-2)]
 canvas=Image.new('RGBA',(384,256));offset=[round(192-root[0]),round(224-root[1])];canvas.alpha_composite(im,tuple(offset))
 arr=np.array(canvas);mask=arr[:,:,3]>96;cells=[]
 for y in range(0,256,4):
  row=[]
  for x in range(0,384,4):
   if np.count_nonzero(mask[y:y+4,x:x+4])>=2:row.append(x)
  # Merge adjacent cells on each row to keep collision metadata small.
  for x in row:
   if cells and cells[-1][1]==y and cells[-1][0]+cells[-1][2]==x:cells[-1][2]+=4
   else:cells.append([x,y,4,4])
 yy,xx=np.where(mask);maxreach=max(maxreach,float(np.hypot(xx-192,yy-224).max()))
 name=f'pose_{i}.png';canvas.save(OUT/name);poses.append({'file':name,'anchor':[192,224],'cells':cells})
 frames.append(canvas)
for i in range(8):recolor(Image.open(ROOT/f'assets/game/laser_round_muzzle_0923/round_{i}.png')).save(OUT/f'muzzle_{i}.png')
runtime={'size':[384,256],'anchor':[192,224],'reach':round(maxreach,3),'frames':[p['cells'] for p in poses]}
(OUT/'collision.json').write_text(json.dumps(runtime,separators=(',',':'))+'\n')
manifest={'asset_id':'c1fe952b-34ab-4e7a-843f-0f07643864b7','source_asset_id':'7eebc4c8-e086-42fc-8951-26f5ad1dc255',
 'animation_source_asset_id':'a980929d-629a-4d6f-bc09-8237e238da7e','model':'pixel-engine-v1.5','frame_count':len(poses),'animation_credits':26,'master_credits':16,
 'palette':'Sampled from live nfw2_2 / #ff6924 and nfb_orb3_3. Same luminance ramp on whip and muzzle, hot end capped at 224 to retain saturated gold.',
 'size':runtime['size'],'anchor':runtime['anchor'],'reach':runtime['reach'],
 'files':[{'file':p.name,'sha12':hashlib.sha256(p.read_bytes()).hexdigest()[:12]} for p in sorted(OUT.glob('*.png'))]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
c=Image.new('RGBA',(384*4,256*4))
for i,f in enumerate(frames):c.alpha_composite(f,((i%4)*384,(i//4)*256))
c.save(ROOT/'_shots/whip_authored_frames.png')
print('Authored poses:',len(poses),'max reach:',maxreach,'collision cells:',sum(len(p['cells']) for p in poses))
