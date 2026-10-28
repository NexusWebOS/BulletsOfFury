"""Existing whole Voss plates, fixed pivots, own-pixel power and source orb palette."""
from pathlib import Path
import json,colorsys,hashlib
import numpy as np
from PIL import Image
from scipy import ndimage
from pixel_glow_1015 import rings,RING_A
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/voss_turbo_1028';D.mkdir(parents=True,exist_ok=True)
S=R/'_ART_SOURCES/voss_turbo_1028';source=R/'assets/game/levels/stage_06/boss/rough_riders_1028/flight_voss.png'
src=Image.open(source).convert('RGBA');sheet=Image.new('RGBA',(192*8,192*10));out={}
for f in range(80):
 sf=f if f<72 else 64+f-72;im=src.crop((sf%16*192,sf//16*192,sf%16*192+192,sf//16*192+192))
 if f>=72:im=im.rotate(180,resample=Image.Resampling.NEAREST,center=(96,96))
 sheet.paste(im,(f%8*192,f//8*192))
def save(name,im,cw,ch,cols,n,pivot):
 im.save(D/(name+'.png'));out[name]=dict(key='vs41_'+name,path=(D/(name+'.png')).relative_to(R).as_posix(),cw=cw,ch=ch,cols=cols,frames=n,pivot=pivot)
save('hull',sheet,192,192,8,80,[96,96]);hit=Image.new('RGBA',sheet.size,(255,255,255,0));hit.putalpha(sheet.getchannel('A'));save('hull_hit',hit,192,192,8,80,[96,96]);shadow=Image.new('RGBA',sheet.size);shadow.putalpha(sheet.getchannel('A'));save('shadow',shadow,192,192,8,80,[96,96])
outer=Image.new('RGBA',sheet.size);inner=Image.new('RGBA',sheet.size)
for f in range(80):
 x=f%8*192;y=f//8*192;a=np.array(sheet.crop((x,y,x+192,y+192)));opaque=a[:,:,3]>130;yy,xx=np.mgrid[:192,:192];rad=np.hypot(xx-96,yy-96)
 edge=opaque&(ndimage.distance_transform_edt(opaque)<=1.5)&(rad<58)
 rgb=np.zeros((192,192,3),np.float32);rgb[:]=[255,68,29]
 g=rings(edge,rgb,RING_A,1,.5);outer.paste(Image.fromarray(g.clip(0,255).astype('uint8')),(x,y))
 v=a[:,:,:3].max(2);lo=a[:,:,:3].min(2);lights=opaque&(rad<43)&(v>145)&(((v-lo)>65)|((v>225)&(lo>160)))
 g=rings(lights,a[:,:,:3].astype(np.float32),RING_A,1,.52);inner.paste(Image.fromarray(g.clip(0,255).astype('uint8')),(x,y))
save('outer',outer,192,192,8,80,[96,96]);save('inner',inner,192,192,8,80,[96,96])
orb=Image.new('RGBA',(128*4,128*2));orbglow=Image.new('RGBA',orb.size);hashes={}
for f in range(8):
 im=Image.open(S/f'florb_{f}.png').convert('RGBA');assert max(im.size)<=128,im.size
 a=np.array(im);rgb=a[:,:,:3].astype(float)/255
 # Preserve alpha, value/luminance structure, dark outlines and the white-hot core.
 for y in range(im.height):
  for x in range(im.width):
   if not a[y,x,3]:continue
   h,s,v=colorsys.rgb_to_hsv(*rgb[y,x]);weights=np.array([.2126,.7152,.0722]);light=float(rgb[y,x]@weights)*255
   hue=np.array(colorsys.hsv_to_rgb(.025,1,1));delta=hue-float(hue@weights);chroma=s*255
   for d in delta:
    if d>0:chroma=min(chroma,(255-light)/d)
    elif d<0:chroma=min(chroma,light/-d)
   a[y,x,:3]=np.rint(light+delta*chroma).clip(0,255)
 cell=Image.new('RGBA',(128,128));cell.paste(Image.fromarray(a),((128-im.width)//2,(128-im.height)//2));orb.paste(cell,(f%4*128,f//4*128))
 a=np.array(cell);mask=(a[:,:,3]>160)&(a[:,:,:3].max(2)>160);g=rings(mask,a[:,:,:3].astype(float),RING_A,1,.35);orbglow.paste(Image.fromarray(g.clip(0,255).astype('uint8')),(f%4*128,f//4*128))
 hashes['florb_'+str(f)]=hashlib.sha256((S/f'florb_{f}.png').read_bytes()).hexdigest()
save('orb',orb,128,128,4,8,[64,64]);save('orb_glow',orbglow,128,128,4,8,[64,64]);hit=Image.new('RGBA',orb.size,(255,255,255,0));hit.putalpha(orb.getchannel('A'));save('orb_hit',hit,128,128,4,8,[64,64])
meta=dict(banks=out,unit=1.15,sockets=[[66,106],[126,106]],builder='_BUILD_SOURCE/build_voss_turbo_1028.py',sources=hashes,hullSource=str(source.relative_to(R)),hullHash=hashlib.sha256(source.read_bytes()).hexdigest())
(D/'manifest.json').write_text(json.dumps(meta,indent=2));(R/'assets/voss_turbo_art_1028.js').write_text('"use strict";\nconst VS41_ART='+json.dumps(meta,separators=(',',':'))+';\n')
contact=Image.new('RGBA',(192*4,192*2),(12,20,25,255))
for i,f in enumerate([8,48,72,76,24,56,64,68]):contact.alpha_composite(sheet.crop((f%8*192,f//8*192,f%8*192+192,f//8*192+192)),(i%4*192,i//4*192))
contact.save(S/'hull-contact.png');orb.save(S/'red-orb-contact.png')
tax=R/'assets/data/ART_TAXONOMY.json';raw=tax.read_text(encoding='utf8')
if '"vs41_"'not in raw:
 entry=dict(role='voss_twin_blaster_overhead_turbo',owner=meta['builder'],manifest=str((D/'manifest.json').relative_to(R)).replace('\\','/'),note='80 fixed192 source-preserving whole plates, 1015 outer/inner companions, exact alpha shadows/white hits,8 fixed128 red-orange palette frames from native florb. Native HP/module ownership remains.')
 tax.write_text('{\n  "vs41_": '+json.dumps(entry,separators=(',',':'))+','+raw[1:],encoding='utf8')
print('Voss:80 hull poses, source shadows/1015 layers,8 red-white orb frames')
