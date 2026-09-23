"""Slice GPT2.5 wide lashes; retain authored curls; bake matching collision.

No deformation or mirroring. --install synchronizes runtime metadata and paths.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'assets/game/player_weapons/fire_whip_lash_0923'
OUT=ROOT/'assets/game/player_weapons/fire_whip_sweep_0923'
def lum(a):return a[...,0]*.299+a[...,1]*.587+a[...,2]*.114
refs=[np.asarray(Image.open(OLD/(n+'_palette.png')).convert('RGBA')) for n in ['fireorb','flamethrower']]
pool=np.concatenate([a[a[:,:,3]>200,:3] for a in refs]).astype(float)
colors,counts=np.unique(pool,axis=0,return_counts=True);light=lum(colors)
ramp=np.array([colors[np.argmin(np.abs(light-min(224,i))*4+colors[:,2]*.035-np.log1p(counts)*.2)] for i in range(256)],dtype='uint8')
sheet=Image.open(OUT/'source_raw.png').convert('RGBA');cw,ch=sheet.width//4,sheet.height//4
wide=[]
for i in range(16):
 im=sheet.crop(((i%4)*cw,(i//4)*ch,(i%4+1)*cw,(i//4+1)*ch))
 a=np.array(im);a[:,:,3][a[:,:,3]<=12]=0
 a[:,:,:3]=ramp[np.clip(np.rint(lum(a[:,:,:3].astype(float))),0,255).astype(int)]
 solid=a[:,:,3]>96;ys,xs=np.where(solid);bottom=int(ys.max())
 # Bright root bulb is at the bottom of each authored cell, not its geometric center.
 ry,rx=np.where(solid & (np.indices(solid.shape)[0]>=bottom-16))
 root=np.array([np.average(rx,weights=lum(a[ry,rx,:3].astype(float))),bottom-3])
 # Match longest source pose to the existing 180px source-space reach.
 # Normalize the extended generated lashes to equal reach; retained curls recoil naturally.
 wide.append((Image.fromarray(a),root))
reach=max(np.hypot(*(np.array(np.where(np.array(im)[:,:,3]>96))[::-1]-root[:,None])).max() for im,root in wide)
normalized=[]
for im,root in wide:
 yy,xx=np.where(np.array(im)[:,:,3]>96)
 scale=180/float(np.hypot(xx-root[0],yy-root[1]).max())
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
 canvas=Image.new('RGBA',(384,256));canvas.alpha_composite(im,(round(192-root[0]*scale),round(224-root[1]*scale)));normalized.append(canvas)
# Preserve the approved coil poses inside each broad side-to-side stroke.
order=[('wide',i) for i in [0,1,2,3]]+[('curl',i) for i in [3,4,5,7]]+[('wide',i) for i in [4,5,6,7]]
order += [('wide',i) for i in [8,9,10,11]]+[('curl',i) for i in [11,12,14,15]]+[('wide',i) for i in [12,13,14,15]]
frames=[];masks=[];extents=[];maxreach=0
for i,(kind,n) in enumerate(order):
 im=normalized[n] if kind=='wide' else Image.open(OLD/f'pose_{n}.png').convert('RGBA')
 # The generated frames contain the moving bend. Keep their root at the
 # ship's muzzle while the lower shaft and tip whip across either side.
 im.save(OUT/f'pose_{i}.png');frames.append(im);mask=np.array(im)[:,:,3]>96;cells=[]
 for y in range(0,256,4):
  for x in range(0,384,4):
   if np.count_nonzero(mask[y:y+4,x:x+4])<2:continue
   if cells and cells[-1][1]==y and cells[-1][0]+cells[-1][2]==x:cells[-1][2]+=4
   else:cells.append([x,y,4,4])
 yy,xx=np.where(mask);maxreach=max(maxreach,float(np.hypot(xx-192,yy-224).max()))
 extents.append([int(xx.min()-192),int(xx.max()-192),int(yy.min()-224),int(yy.max()-224)]);masks.append(cells)
meta={'size':[384,256],'anchor':[192,224],'reach':round(maxreach,3),'frames':masks}
(OUT/'collision.json').write_text(json.dumps(meta,separators=(',',':'))+'\n')
manifest={'asset_id':'bf2adfda-6b5c-4b59-b2e4-f30572fe2159','model':'gpt-image-2.5-sunburst','credits':55,'reference_asset_id':'7eebc4c8-e086-42fc-8951-26f5ad1dc255','retained_curl_asset_id':'c1fe952b-34ab-4e7a-843f-0f07643864b7','frame_count':24,'order':order,'extents':extents,'palette':'Same sampled fire-orb/flamethrower ramp and approved muzzle as fire_whip_lash_0923','source_note':'Canonical pixel conversion incorrectly produced 33x33; recovered full-resolution raw_url from same owned asset. Reported to SpriteCook.','files':[{'file':p.name,'sha12':hashlib.sha256(p.read_bytes()).hexdigest()[:12]} for p in sorted(OUT.glob('*.png'))]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
contact=Image.new('RGBA',(384*6,256*4))
for i,im in enumerate(frames):contact.alpha_composite(im,((i%6)*384,(i//6)*256))
contact.save(ROOT/'_shots/firewhip_wide_contact.png')
if argparse.ArgumentParser().parse_known_args()[1]==['--install']:
 p=ROOT/'assets/game.js';s=p.read_bytes().decode('utf-8')
 start=s.index('const FIRE_WHIP_POSES=');end=s.index('\nfunction fireWhipFrame',start)
 s=s[:start]+'const FIRE_WHIP_POSES='+json.dumps(meta,separators=(',',':'))+';'+s[end:]
 s=s.replace("f<16;f++)X._src['fire_whip_pose_'+f]='assets/game/player_weapons/fire_whip_lash_0923/pose_'", "f<24;f++)X._src['fire_whip_pose_'+f]='assets/game/player_weapons/fire_whip_sweep_0923/pose_'")
 s=s.replace("f<16;f++)XART.rdy('fire_whip_pose_'+f)","f<FIRE_WHIP_POSES.frames.length;f++)XART.rdy('fire_whip_pose_'+f)")
 s=s.replace("i<16;i++)XART.rdy('fire_whip_pose_'+i)","i<FIRE_WHIP_POSES.frames.length;i++)XART.rdy('fire_whip_pose_'+i)")
 s=s.replace('return Math.min(15,Math.floor(phase*8));','return Math.min(FIRE_WHIP_POSES.frames.length-1,Math.floor(phase*FIRE_WHIP_POSES.frames.length/2));')
 s=s.replace('built together by build_fire_whip_lash_0923.py.','built together by build_fire_whip_sweep_0923.py --install.')
 if "      const f=fireWhipFrame(b,(b.t||0)/b.duration),key='fire_whip_pose_'+f;\n      const scale=b.reach/FIRE_WHIP_POSES.reach;" not in s:
  s=s.replace("      const f=fireWhipFrame(b,(b.t||0)/b.duration),key='fire_whip_pose_'+f;", "      const f=fireWhipFrame(b,(b.t||0)/b.duration),key='fire_whip_pose_'+f;\n      const scale=b.reach/FIRE_WHIP_POSES.reach;")
 s=s.replace("      if(XART.rdy(key)){\n        const scale=b.reach/FIRE_WHIP_POSES.reach;", "      if(XART.rdy(key)){")
 s=s.replace('roundLaserMuzzleDraw(ctx,b.x+FIRE_WHIP_POSES.baseX[f]*scale,b.y,24,FIRE_WHIP_PALETTE,', 'roundLaserMuzzleDraw(ctx,b.x,b.y,24,FIRE_WHIP_PALETTE,')
 p.write_bytes(s.encode('utf-8'))
print('Built',len(frames),'frames; bounds',extents,'collision cells',sum(map(len,masks)))
