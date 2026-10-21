"""Own PixelLab sonic cells, shared padding/pivots, palette variants and audits."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import numpy as np,json,hashlib,math
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/sonic_effects_1021';D=R/'assets/game/shared/combat/sonic_effects_1021';O=R/'_shots/sonic_effects_1021'
D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
jobs=json.loads((S/'jobs.json').read_text());art={'banks':{},'service':'PixelLab Pixen/PixFlux + PixMiniMax','fps':18};audit=[]
def palette(im,target):
 # Keep luminance and neutral authored highlights. Solve brightness with a
 # white component once a saturated target hue reaches its channel ceiling.
 a=np.array(im);rgb=a[:,:,:3].astype(float)/255;hi=rgb.max(2);lo=rgb.min(2);sat=hi-lo;Y=rgb@np.array([.2126,.7152,.0722]);t=np.array(target,dtype=float);ty=t@np.array([.2126,.7152,.0722]);
 lower=t[None,None,:]*(Y/ty)[:,:,None];white=np.clip((Y-ty)/(1-ty),0,1);upper=t[None,None,:]*(1-white[:,:,None])+white[:,:,None];new=np.where((Y<=ty)[:,:,None],lower,upper)
 strength=np.clip(sat/np.maximum(.001,hi),0,1);out=rgb*(1-strength[:,:,None])+new*strength[:,:,None]
 a[:,:,:3]=np.clip(np.rint(out*255),0,255).astype('uint8');return Image.fromarray(a)
def contact(name,frames):
 w,h=frames[0].size;sheet=Image.new('RGBA',(w*8,(h+18)*math.ceil(len(frames)/8)),(7,13,22,255));draw=ImageDraw.Draw(sheet)
 for i,im in enumerate(frames):
  xy=(i%8*w,i//8*(h+18));sheet.alpha_composite(im,xy);draw.text((xy[0]+4,xy[1]+h+2),str(i),fill='white')
 sheet.convert('RGB').save(O/(name+'-contact.jpg'),quality=95)
 frames[0].save(O/(name+'-motion.webp'),save_all=True,append_images=frames[1:],duration=56,loop=0,lossless=True)
for name,a in jobs.items():
 if name=='tank_charge':continue # Rejected target/matte; superseded by true spiral.
 files=sorted((S/'raw'/name).glob('[0-9][0-9].png'));assert len(files)==a['frames'],(name,len(files))
 source=[Image.open(p).convert('RGBA') for p in files];assert all(list(im.size)==a['canvas'] for im in source)
 contact(name+'-source',source)
 # Remove neutral gray matte debris, retaining colored energy and white light.
 for im in source:
  px=np.array(im);rgb=px[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2)
  matte=(hi<160)&((hi-lo)<hi*.10);px[matte,3]=0;im.putdata([tuple(v) for v in px.reshape(-1,4)])
 selected=[0,1,4,5,6,9,10,11,12,15,16] if name=='tank_ring' else list(range(len(source)))
 source=[source[i] for i in selected]
 # A shared alpha crop recenters these EFFECTS, not the boss/weapon art.
 # Its one canvas and pivot are common to the entire bank, never pose-fitted.
 boxes=[im.getchannel('A').point(lambda p:255 if p>=24 else 0).getbbox() for im in source];assert all(boxes)
 box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
 cw,ch=box[2]-box[0],box[3]-box[1];w=cw+32+(cw%2);h=ch+32+(ch%2)
 if 'charge' in name or name=='tank_ring':w=h=max(w,h)
 offset=((w-cw)//2,(h-ch)//2);frames=[]
 for im in source:
  im=im.crop(box)
  if name.endswith('wave'):im=ImageOps.flip(im)
  c=Image.new('RGBA',(w,h));c.alpha_composite(im,offset);frames.append(c)
 variants={'green':None,'red':(1,.035,.12)} if name.startswith('tank') else {'normal':(.20,1,.30),'fury':(.36,1,.035)}
 if name=='spiral':variants={'green':None,'red':(1,.035,.12),'normal':(.20,1,.30),'fury':(.36,1,.035)}
 for variant,ramp in variants.items():
  stem='heli_blade' if name=='heli_wave' else 'heli_wave' if name=='heli_front' else ('tank_charge' if variant in ['red','green'] else 'heli_spiral') if name=='spiral' else name
  bank=stem+'_'+variant;fs=frames if ramp is None else [palette(im,ramp) for im in frames]
  sheet=Image.new('RGBA',(w*8,h*math.ceil(len(fs)/8)));cells=[]
  for i,im in enumerate(fs):
   x,y=i%8*w,i//8*h;sheet.alpha_composite(im,(x,y));cells.append([x,y,w,h])
  path=D/(bank+'.webp');sheet.save(path,lossless=True,method=6);contact(bank,fs)
  # Charge pivot uses the generated light's source center. The whole bank
  # receives the same source-rectangle translation, preserving animation.
  pivot=[w/2,h/2]
  if 'charge' in name or name in ['tank_ring','spiral']:pivot=[a['canvas'][0]/2-box[0]+offset[0],a['canvas'][1]/2-box[1]+offset[1]]
  entry=dict(key='sx21_'+bank,path=path.relative_to(R).as_posix(),w=w,h=h,pivot=pivot,frames=len(fs),fps=18,cells=cells,inkW=cw,inkH=ch)
  if name=='tank_ring':
   # Dominant bright ring, measured from the source seed at the common pivot.
   arr=np.array(fs[0]);yy,xx=np.indices((h,w));rad=np.rint(np.hypot(xx-pivot[0],yy-pivot[1])).astype(int);lum=arr[:,:,:3]@np.array([.2126,.7152,.0722]);bright=(lum>165)&(arr[:,:,3]>100)
   bins=np.bincount(rad[bright].ravel());entry['ridgeRadius']=int(np.argmax(bins[15:])+15)
  art['banks'][bank]=entry
  audit.append(dict(bank=bank,job=a['job'],seedJob=a['seedJob'],sourceCanvas=a['canvas'],sourceIndices=selected,commonCrop=list(box),sharedOffset=list(offset),paletteTarget=ramp,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),unique=len({hashlib.sha256(im.tobytes()).hexdigest() for im in fs}),**entry))
(R/'assets/sonic_effects_art_1021.js').write_text("'use strict';\nconst SX21_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'export-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
tax=R/'assets/data/ART_TAXONOMY.json';text=tax.read_text(encoding='utf-8')
if 'sx21_' not in json.loads(text):
 entry={'sx21_':{'role':'sonic_tank_and_overlord_pressure_wave_spiral_charge_animation','sheet':None,'owner':'_BUILD_SOURCE/build_sonic_effects_1021.py','note':'Six accepted PixelLab effect-only banks with green/red Razorback and green/lime Overlord palette variants. Shared even canvases, common source-center pivots, fixed proportional scale and native collision-shaped clipping. No boss hull replacements; hit flashes, weapons and warning timing retain native owners.'}}
 prefix=json.dumps(entry,indent=2)[2:-2];tax.write_text('{\n'+prefix+',\n'+text[2:],encoding='utf-8',newline='\n')
print(json.dumps(dict(banks=len(audit),frames=sum(a['frames'] for a in audit),bytes=sum(p.stat().st_size for p in D.glob('*.webp')))))
