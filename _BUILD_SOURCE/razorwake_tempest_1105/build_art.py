"""Fixed-frame Razorwake rolls, tapered exhaust and storm-Helix lifecycle."""
from pathlib import Path
import json,math,subprocess,hashlib
import numpy as np
from PIL import Image,ImageFilter
W=Path(__file__).resolve().parent
P=W.parent/'razorwake_modular_1104'
if not(P/'build_razor.py').exists():P=Path(r'C:/Users/Mike/Documents/New project/BOF-Razorwake-Modular-1104')
# Shared offline authoring/packing functions; never used by the game renderer.
code=(P/'build_razor.py').read_text().split('raw=Image.open')[0]
code=code.replace("W=Path(__file__).resolve().parent",'W=Path('+repr(str(W))+')').replace('razorwake_modular_1104/','razorwake_tempest_1105/').replace('rw117_page_','rw118_page_')
code=code.replace("page.save(O/filename);M['pages'][key]={'path':REL+filename,'w':1024,'h':1024}","bb=page.getbbox()or(0,0,2,2);pw=math.ceil(bb[2]/2)*2;ph=math.ceil(bb[3]/2)*2;page.crop((0,0,pw,ph)).save(O/filename);M['pages'][key]={'path':REL+filename,'w':pw,'h':ph}")
exec(compile(code,str(P/'build_razor.py'),'exec'),globals())
OLD_DIR=P/'authored'if(P/'authored').exists()else R/'assets/game/levels/stage_06/miniboss/razorwake_modular_1104'
OLD_STRIPS=P/'authored/strips'if(P/'authored/strips').exists()else P/'strips'
OLD=json.loads((OLD_DIR/'manifest.json').read_text())
def old(n,i=0):
 B=OLD['banks'][n];im=Image.open(OLD_STRIPS/(n+'.png')).convert('RGBA');return im.crop((i%8*B['w'],i//8*B['h'],i%8*B['w']+B['w'],i//8*B['h']+B['h']))
def projection(im,f):
 co=math.cos(f/12*math.tau);c=max(.16,abs(co));root=im.width//2
 out=im.transform(im.size,Image.Transform.AFFINE,(1/c,0,root-root/c,0,1,0),Image.Resampling.NEAREST)
 if co<0:
  out=out.transpose(Image.Transpose.FLIP_LEFT_RIGHT);a=np.array(out);a[:,:,:3]=(a[:,:,:3].astype(float)*[.48,.68,.67]).astype('uint8');out=Image.fromarray(a)
 return out
body=old('hull');body.alpha_composite(old('left',32));body.alpha_composite(old('right',32))
roll=[];gunroll=[];wreckroll=[]
for f in range(12):
 for direction in[1,-1]:roll.append(projection(body,f).rotate(direction*90,Image.Resampling.NEAREST))
bank('roll',roll,masks=True);bank('roll_hit',[light(x,mode='hit')for x in roll]);bank('roll_shadow',[light(x,mode='shadow')for x in roll])
for f in range(12):
 for spin in range(8):
  for direction in[1,-1]:gunroll.append(projection(old('gun',spin*32),f).rotate(direction*90,Image.Resampling.NEAREST))
 for direction in[1,-1]:wreckroll.append(projection(old('gun_wreck'),f).rotate(direction*90,Image.Resampling.NEAREST))
bank('gun_roll',gunroll);bank('gun_roll_hit',[light(x,mode='hit')for x in gunroll]);bank('gun_roll_wreck',wreckroll)
# A single tapered flame silhouette, with source-pixel light grades only.
flame=Image.open(W/'thruster-generated.png').convert('RGBA');flame=cutout(flame);flame=flame.crop(flame.getbbox())
for label,size in [('cruise',62),('throttle',118)]:
 f=flame.resize((round(flame.width*size/flame.height),size),Image.Resampling.NEAREST);c=Image.new('RGBA',(272,272));c.alpha_composite(f,(136-f.width//2,136-size))
 bank('thrust_'+label,[heading(light(c,g),n)for g in range(6)for n in range(32)])
# Precompose the invariant hull/wing layers offline, retaining the exact same pixels.
# Guns remain independently animated, hittable and detachable at runtime.
for label in ['body','body_hit','body_shadow','body_charge']:
 images=[]
 count=144 if label=='body_charge'else 56
 for i in range(count):
  hot=label=='body_charge';pose=i%24 if hot else i;d=0 if hot or i>=32 else i
  hullname='hull_charge'if hot else 'hull_hit'if label=='body_hit'else 'hull_shadow'if label=='body_shadow'else 'hull'
  wingtail='_charge'if hot else '_hit'if label=='body_hit'else '_shadow'if label=='body_shadow'else ''
  im=old(hullname,i//24 if hot else d)
  for side in ['left','right']:im.alpha_composite(old(side+wingtail,i if hot else pose))
  images.append(im)
 bank(label,images)

# Source-derived perimeter aura; no wind ribbons surrounding the craft.
auras=[]
for g in range(6):
 for f in range(24):
  im=old('hull');im.alpha_composite(old('left',32+f));im.alpha_composite(old('right',32+f));a=im.getchannel('A');outer=np.array(a.filter(ImageFilter.MaxFilter(3+g*2))).astype(int);inner=np.array(a).astype(int)
  rim=Image.new('RGBA',im.size,(32+g*15,178+g*13,163+g*14,0));rim.putalpha(Image.fromarray((np.maximum(0,outer-inner)*(.32+g*.115)).clip(0,255).astype('uint8')));auras.append(rim)
bank('aura',auras)
cock=[];a=np.array(old('hull'));yy,xx=np.indices(a.shape[:2]);mask=(a[:,:,2]>a[:,:,0]*1.6)&(a[:,:,2]>a[:,:,1]*.95)&(abs(xx-192)<21)&(yy>140)&(yy<218)&(a[:,:,3]>0)
for g in range(6):
 b=np.zeros_like(a);b[mask]=a[mask];rgb=b[:,:,:3].astype(float);v=rgb.max(2);rgb[mask]=np.minimum(255,v[mask,None]*np.array([.1+g*.1,.75+g*.06,.69+g*.06])+g*7);b[:,:,:3]=rgb.astype('uint8');cock.append(light(Image.fromarray(b),g))
bank('cockpit',cock)
# Generated internal wind loop: normalize the whole sheet uniformly, no per-frame fitting.
s=Image.open(W/'wind-orb-generated.png').convert('RGBA');orb=[]
for i in range(16):
 rect=(round(i%4*s.width/4),round(i//4*s.height/4),round((i%4+1)*s.width/4),round((i//4+1)*s.height/4));f=cutout(s.crop(rect),'wind');orb.append(f.resize((256,256),Image.Resampling.NEAREST))
for j,d in enumerate([24,40,56,72,88,104,128,152]):
 csize=176;images=[]
 for im in orb:
  c=Image.new('RGBA',(csize,csize));c.alpha_composite(im.resize((d,d),Image.Resampling.NEAREST),((csize-d)//2,(csize-d)//2));images.append(c)
 bank('charge_'+str(j),images)
sizes=[152,192,240,288,344,408,480,560,648,744,848,944]
for j,d in enumerate(sizes):
 cell=math.ceil((d+8)/2)*2;images=[]
 for im in orb[::2]:
  c=Image.new('RGBA',(cell,cell));c.alpha_composite(im.resize((d,d),Image.Resampling.NEAREST),((cell-d)//2,(cell-d)//2));images.append(c)
 bank('orb_'+str(j),images)
M['orbSizes']=sizes
bank('medium',[im.resize((60,60),Image.Resampling.NEAREST)for im in orb])
burst=[]
for f in range(10):
 c=Image.new('RGBA',(256,256));d=round(50*(1-f/13));small=orb[(f*2)%16].resize((d,d),Image.Resampling.NEAREST)
 for i in range(9):
  r=14+f*8;ang=i*math.tau/9;c.alpha_composite(small,(round(128+math.cos(ang)*r-d/2),round(128+math.sin(ang)*r-d/2)))
 burst.append(c)
bank('orb_break',burst)
# Existing approved full-height storm branches; authored strike and cooling cells.
lightning=[]
src=Image.open(R/'assets/game/levels/stage_06/boss/thunderhead_storm_1104/bolt_0.png').convert('RGBA')
for i in range(16):
 f=src.crop((i%8*96,0,i%8*96+96,512));a=np.array(f);rgb=a[:,:,:3].astype(float);v=rgb.max(2);sat=v-rgb.min(2);active=(a[:,:,3]>0)&(sat>24);rgb[active]=np.minimum(255,v[active,None]*np.array([.35,.95,.84])+12);a[:,:,:3]=rgb.astype('uint8')
 if i>=8:a[:,:,3]=(a[:,:,3].astype(float)*(1-(i-7)/9)).astype('uint8')
 c=Image.new('RGBA',(160,544));c.alpha_composite(Image.fromarray(a),(32,16));lightning.append(c)
bank('lightning',lightning)
bank('storm_grade',[Image.new('RGBA',(340,256),(1,7,12,round(i/8*162)))for i in range(9)])
M['banks']['storm_grade']['edgePolicy']='Intentional full-bleed continuous background shade tile.'
M['maskBytes']=len(bitdata);M['maskPath']=REL+'opaque_masks.bin';(O/'opaque_masks.bin').write_bytes(bitdata)
M['sources']={n:hashlib.sha256((W/n).read_bytes()).hexdigest()for n in['wind-orb-generated.png','thruster-generated.png']}
(O/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'razorwake_tempest_art_1105.js').write_text("'use strict';\nconst RW118_ART="+json.dumps(M,separators=(',',':'))+';\n')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local im=Image{fromFile=D..'/strips/'..n..'.png'};local s=Sprite(a.w,a.h,ColorMode.RGB)
for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(i%8*a.w,math.floor(i/8)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/24 end;s:saveAs(D..'/'..n..'.aseprite');s:close()end"""
(O/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+O.as_posix(),'--script',str(O/'author.lua')],check=True)
preview=Image.new('RGBA',(1152,768),(8,16,21,255))
for i,name in enumerate(['roll','aura','thrust_throttle','charge_7','orb_5','lightning']):preview.alpha_composite(frames[name][3 if name=='roll'else 0],(i%3*384,i//3*384))
preview.save(W/'art-review.png');print('ART',sum(x['frames']for x in M['banks'].values()),'frames',len(M['banks']),'banks',len(M['pages']),'pages',flush=True)
