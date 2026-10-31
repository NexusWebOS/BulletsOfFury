"""HC79. Source-locked 85% helicopter, fast rotor source cycle, independently
aimed/recoiling pod frames, red pressure fronts and layered digital jungle.
All sprite transforms, palette changes and fades are exported offline.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageFilter
import numpy as np,math,json,hashlib,shutil
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_helicopter_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True)
O=R/'assets/game/levels/stage_08/boss/helicopter_1030';D=R/'_ART_SOURCES/dracodia_helicopter_1030'
O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
def data(name):
 s=(R/'assets'/name).read_text(encoding='utf-8-sig');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
V=data('stage8_pixellab_art_1018.js')['models']['helicopter'];unit=348/320;C=512;P=256
A={'banks':{},'pages':{},'mounts':[],'size':348,'previousSize':410,'rotorFps':48,'sourceRotorFps':12,'logical':[512,512],'pivot':[256,256]};sources={}
PAGE=1024
page=Image.new('RGBA',(PAGE,PAGE));hit=page.copy();px=py=rh=pi=0
def save():
 global page,hit,px,py,rh,pi
 key='hc79_page_'+str(pi);path=O/(key+'.webp');page.save(path,lossless=True,method=4);hp=O/(key+'_hit.webp');hit.save(hp,lossless=True,method=4)
 A['pages'][key]={'path':path.relative_to(R).as_posix(),'hitKey':key+'_hit','hitPath':hp.relative_to(R).as_posix()};pi+=1;page=Image.new('RGBA',(PAGE,PAGE));hit=page.copy();px=py=rh=0
def pack(name,im,pivot,sockets=None):
 global px,py,rh
 b=im.getbbox();assert b,name
 x0=b[0]//2*2;y0=b[1]//2*2;x1=(b[2]+1)//2*2;y1=(b[3]+1)//2*2
 assert x0>0 and y0>0 and x1<im.width and y1<im.height,(name,b,im.size)
 crop=im.crop((x0,y0,x1,y1));w,h=crop.size
 if px+w+2>PAGE:px=0;py+=rh+2;rh=0
 if py+h+2>PAGE:save()
 page.paste(crop,(px,py));rgba=np.array(crop);white=rgba.copy();white[:,:,:3]=255;hit.paste(Image.fromarray(white),(px,py))
 mask=rgba[:,:,3]>48;spans=[np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1)))).tolist()for row in mask];yy,xx=np.where(mask)
 a={'key':'hc79_page_'+str(pi),'rect':[px,py,w,h],'offset':[x0-pivot[0],y0-pivot[1]],'w':w,'h':h,'spans':spans,'target':[round(float(xx.mean()+x0-pivot[0]),2),round(float(yy.mean()+y0-pivot[1]),2)],'bounds':[0,0,w,h]}
 if sockets:a['sockets']=sockets
 A['banks'].setdefault(name,[]).append(a);px+=w+2;rh=max(rh,h);return a
def load(a):
 p=R/a['path'];sources[a['path']]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
def turn(p,deg):
 a=math.radians(deg);return [round(p[0]*math.cos(a)-p[1]*math.sin(a),2),round(p[0]*math.sin(a)+p[1]*math.cos(a),2)]
cores=[load(f['core']).resize((348,348),Image.Resampling.NEAREST)for f in V['frames']]
for bank in range(13):
 deg=(bank-6)*5
 A['mounts'].append({id:turn([(64 if id=='left'else 256)-160,0],deg)for id in []})
 A['mounts'][-1]={id:turn([((64 if id=='left'else 256)-160)*unit,0],deg)for id in ['left','right']}
 for f,im in enumerate(cores):
  out=Image.new('RGBA',(C,C));out.paste(im,(82,82));out=out.rotate(-deg,Image.Resampling.NEAREST,center=(P,P));pack('core_'+str(bank),out,(P,P))
for id in ['left','right']:
 src=load(V['frames'][0][id]);joint=(64 if id=='left'else 256,160);box=src.getbbox();pod=src.crop(box).resize((round((box[2]-box[0])*unit),round((box[3]-box[1])*unit)),Image.Resampling.NEAREST)
 for recoil in range(3):
  shift=[0,-3,-1][recoil]
  for d in range(64):
   deg=d*360/64;out=Image.new('RGBA',(192,192));out.paste(pod,(96+round((box[0]-joint[0])*unit),96+round((box[1]-joint[1])*unit)+shift));out=out.rotate(-deg,Image.Resampling.NEAREST,center=(96,96))
   gun=((52 if id=='left'else 267)-joint[0],(216 if id=='left'else 214)-joint[1]);missile=((65 if id=='left'else 255)-joint[0],192-joint[1])
   sockets={n:turn([p[0]*unit,p[1]*unit+shift],deg)for n,p in [('gun',gun),('missile',missile)]};pack('pod_'+id,out,(96,96),sockets)
# True source pressure front; swap hue while retaining original alpha/luminance.
sonicpath=R/'assets/game/levels/stage_01/miniboss/bosses/razorback/rzb_sonic_wave.png';sources[sonicpath.relative_to(R).as_posix()]=hashlib.sha256(sonicpath.read_bytes()).hexdigest()
src=Image.open(sonicpath).convert('RGBA');v=np.array(src);g=v[:,:,1].astype(float);r=v[:,:,0].astype(float);b=v[:,:,2].astype(float)
v[:,:,0]=np.maximum(g,r);v[:,:,1]=np.minimum(220,r*.40+b*.18);v[:,:,2]=np.minimum(255,b*.7+g*.15);white=(r>200)&(g>200)&(b>150);v[white,:3]=[255,235,240];red=ImageOps.flip(Image.fromarray(v))
for f in range(12):
 t=f/12;w=264+round(math.sin(t*math.tau)*6)*2;h=50+round(math.sin(t*math.tau)*2)*2;out=Image.new('RGBA',(288,80));out.alpha_composite(red.resize((w,h),Image.Resampling.NEAREST),((288-w)//2,(80-h)//2));pack('sonic',out,(144,40))
# Existing rotary muzzle art and red missile source / 64 authored directions.
src=Image.open(R/'assets/game/shared/combat/enemy_overhaul_0925/sprites/weapon_muzzle_rotary_0.png').convert('RGBA')
for f in range(4):
 p=R/f'assets/game/shared/combat/enemy_overhaul_0925/sprites/weapon_muzzle_rotary_{f}.png';sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();src=Image.open(p).convert('RGBA');src.thumbnail((26,32),Image.Resampling.NEAREST)
 for d in range(64):
  out=Image.new('RGBA',(80,80));out.alpha_composite(src,((80-src.width)//2,38));out=out.rotate(-d*360/64,Image.Resampling.NEAREST,center=(40,40));pack('muzzle',out,(40,40))
# The same native tracer, with its six birth/steady frames and all64 headings
# authored here; the revised fight never routes it through legacy shadeglow.
manifest=next(s for s in(R/'assets/manifest.js').read_text(encoding='utf-8-sig').splitlines()if s.startswith('window.BOFX='));M=json.JSONDecoder().raw_decode(manifest[manifest.index('=')+1:])[0]
for f in range(6):
 name='mgcf_5_'+str(f);p=R/M['img'][name];sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();_,x,y,w,h,*_=M['playercells'][name];src=Image.open(p).convert('RGBA').crop((x,y,x+w,y+h))
 for d in range(64):
  out=Image.new('RGBA',(64,64));out.alpha_composite(src,((64-w)//2,(64-h)//2));out=out.rotate(-d*360/64,Image.Resampling.NEAREST,center=(32,32));pack('round',out,(32,32))
save()
# Ground and near canopy are separate image layers, world anchored and scrolling
# at12 and28px/s. The stronger near foliage is confined to the margins.
gen=D/'digital-jungle-generated.png'
if not gen.exists():shutil.copy2(Path(r'C:\Users\Mike\.codex\generated_images\01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f\exec-720d6d2e-6937-4723-9259-a8a50fefd28b.png'),gen)
base=Image.open(gen).convert('RGBA').resize((340,512),Image.Resampling.NEAREST).resize((680,1024),Image.Resampling.NEAREST);a=np.array(base)
# Bake a short wrap blend into the texture, not a runtime fade.
for y in range(48):
 u=y/47;mix=(a[976+y].astype(float)*(1-u)+a[y].astype(float)*u).astype(np.uint8);a[976+y]=mix
base=Image.fromarray(a);base.save(O/'digital_jungle_ground.png')
near=base.copy();n=np.array(near);xx=np.arange(680);alpha=np.clip((110-np.minimum(xx,679-xx))/48,0,1);n[:,:,3]=(n[:,:,3]*alpha[None,:]).astype(np.uint8);near=Image.fromarray(n);near.save(O/'digital_jungle_canopy.png')
wire=np.array(base);lum=np.max(wire[:,:,:3],axis=2).astype(float)/255;wire[:,:,0]=(lum*55).astype(np.uint8);wire[:,:,1]=(lum*35).astype(np.uint8);wire[:,:,2]=(lum*100).astype(np.uint8);Image.fromarray(wire).save(O/'digital_jungle_wire.png')
A['arena']={n:{'key':'hc79_jungle_'+n,'path':(O/('digital_jungle_'+file+'.png')).relative_to(R).as_posix(),'w':680,'h':1024}for n,file in [('ground','ground'),('canopy','canopy'),('wire','wire')]}
(R/'assets/dracodia_helicopter_art_1030.js').write_text('"use strict";\nconst HC79_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
(D/'provenance.json').write_text(json.dumps({'sources':sources,'bodyScale':348/410,'rotorSourceFps':12,'rotorPlaybackFps':48,'packing':'Unrotated even tight crops with fixed logical cells and pivots. All turns/recoil/palette/fades baked offline.','pages':pi,'frames':sum(map(len,A['banks'].values()))},indent=2))
# Inspectable source strip for editable Aseprite handoff.
strip=Image.new('RGBA',(348*4,348));
for i,f in enumerate([0,4,8,12]):
 full=Image.new('RGBA',(320,320))
 for id in ['left','core','right']:full.alpha_composite(load(V['frames'][f][id]))
 strip.paste(full.resize((348,348),Image.Resampling.NEAREST),(348*i,0))
strip.save(D/'helicopter-source-strip.png');base.resize((680,1024)).save(W/'jungle-preview.png')
print(json.dumps({'pages':pi,'frames':sum(map(len,A['banks'].values())),'banks':list(A['banks']),'size':A['size']}))
