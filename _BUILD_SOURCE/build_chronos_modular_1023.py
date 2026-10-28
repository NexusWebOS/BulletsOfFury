from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import binary_erosion,binary_dilation,label
import numpy as np,json,math,hashlib
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/chronos_modular_1023';O=W/'shipping';O.mkdir(exist_ok=True)
A={'sheets':{},'banks':{},'gunSocket':[0,48],'gunPivot':[54,46],'muzzle':[54,172],'angles':[-.48,-.36,-.24,-.12,0,.12,.24,.36,.48],'owner':'_BUILD_SOURCE/build_chronos_modular_1023.py','jobs':json.loads((W/'jobs.json').read_text())};audit=[]
def hard(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>127,255,0);return Image.fromarray(a)
def chrome(im):
 a=np.array(im);v=a[:,:,:3].astype(float);lum=v@np.array([.2126,.7152,.0722]);m=binary_erosion(a[:,:,3]>0)&(v.max(2)-v.min(2)<34)&(lum>56)&(lum<236);shine=np.interp(lum,[0,56,80,110,145,190,236,255],[0,56,105,145,181,222,247,255])
 for c,f in enumerate([.94,.98,1]):a[:,:,c][m]=np.clip(shine[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def red(im):
 a=np.array(im);v=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(v[:,:,2]>90)&(v[:,:,2]>v[:,:,0]*1.25)&(v.max(2)-v.min(2)>35);bright=v.max(2)
 for c,f in enumerate([1,.2,.26]):a[:,:,c][m]=np.clip(bright[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def white(im):
 c=Image.new('RGBA',im.size,'white');c.putalpha(im.getchannel('A'));return c
def emit(name,ims,pivot,cols=4,hit=False):
 w,h=ims[0].size;assert w%2==h%2==0;sheet=Image.new('RGBA',(cols*w,math.ceil(len(ims)/cols)*h));rows=[]
 for i,im in enumerate(ims):
  assert im.size==(w,h);b=im.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<w and b[3]<h,(name,i,b)
  rect=[i%cols*w,i//cols*h,w,h];sheet.alpha_composite(im,rect[:2]);rows.append({'key':f'ch23_{name}_{i}','sheet':'ch23_'+name,'cell':rect,'w':w,'h':h,'pivot':list(pivot),'bounds':list(b)})
  audit.append({'key':rows[-1]['key'],'even':True,'noClip':True,'binary':set(np.unique(np.asarray(im)[:,:,3])).issubset({0,255})})
 path=O/(name+'.webp');sheet.save(path,lossless=True,exact=True);A['sheets']['ch23_'+name]={'key':'nca_ch23_'+name,'path':'assets/game/shared/combat/chronos_modular_1023/'+path.name,'w':sheet.width,'h':sheet.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};A['banks'][name]=rows
 return rows
# PixelLab's motion supplies the articulated shoulders. Lock the approved face,
# reactor, grip and planted feet exactly; one unit/pivot, never per-frame fitting.
seed=hard(Image.open(W/'body-seed.png'));raw=seed.copy();grip=W/'raw/grip/00.png'
if grip.exists():
 edit=hard(Image.open(grip));box=(86,105,169,155);raw.paste((0,0,0,0),box);raw.alpha_composite(edit.crop(box),box[:2]);box=(119,103,139,122);raw.paste((0,0,0,0),box);raw.alpha_composite(seed.crop(box),box[:2])
c=Image.new('RGBA',(384,512));c.alpha_composite(raw.resize((448,448),Image.Resampling.NEAREST),(-32,34));body=[c]
# The receiver and outside contour never wobble: only source pixels inside the
# actual rotary assembly are allowed to move. These are generated rotation poses.
base=hard(Image.open(W/'barrel-seed.png'));barrel=[];keep=np.asarray(base)[:,:,3]>0;inside=binary_erosion(keep,iterations=1);yy,xx=np.indices(keep.shape);moving=inside&(yy>=101)&(yy<194)
for i in range(9):
 raw=np.asarray(hard(Image.open(W/'raw/barrel'/f'{i:02}.png')));out=np.array(base);valid=moving&(raw[:,:,3]>0);out[valid]=raw[valid];im=Image.fromarray(out)
 # PixelLab's muzzle changed bore count. Retain the exact approved five-bore
 # rotor and author8 physical axial rotation poses (72deg symmetry) offline.
 # Circularize the existing perspective ellipse, turn it, restore perspective.
 rotor=base.crop((42,194,88,230)).resize((46,46),Image.Resampling.NEAREST);rotor=rotor.rotate((max(0,i-1)/8*72)if i else 0,resample=Image.Resampling.NEAREST,center=(23,23)).resize((46,36),Image.Resampling.NEAREST)
 im.paste((0,0,0,0),(42,194,88,230));im.alpha_composite(rotor,(42,194));im=im.resize((104,208),Image.Resampling.NEAREST);barrel.append(im)
for name,frames,pivot in [('body',body,(192,230)),('barrel',barrel,(54,46))]:
 for suffix,ims in [('',frames),('_armor',[chrome(im)for im in frames]),('_red',[red(im)for im in frames])]:
  rows=emit(name+suffix,ims,pivot)
  for i,a in enumerate(rows):a['white']=f'ch23_{name}_hit_{i}'
 emit(name+'_hit',[white(im)for im in frames],pivot)
# Foreground fingers keep an actual two-hand grip around the independent receiver.
hands=[]
for im in body:
 c=Image.new('RGBA',im.size);box=(157,258,233,304);c.paste(im.crop(box),box[:2]);hands.append(c)
for suffix,ims in [('',hands),('_armor',[chrome(im)for im in hands]),('_red',[red(im)for im in hands])]:
 rows=emit('hands'+suffix,ims,(192,230))
 for i,a in enumerate(rows):a['white']=f'ch23_hands_hit_{i}'
emit('hands_hit',[white(im)for im in hands],(192,230))
# Pre-render directional rounds from the exact native Chronos chaingun FX. No
# runtime rotation or new ordnance classification is used.
bullets=[]
for off in A['angles']:
 for phase in [4,5]:
  p=R/f'assets/game/levels/stage_05/boss/stage5_archmage_0916/blaster_0922/fx_{phase}.png';im=hard(Image.open(p)).resize((12,28),Image.Resampling.NEAREST);c=Image.new('RGBA',(40,40));c.alpha_composite(im,(14,6));c=c.rotate(-math.degrees(off),resample=Image.Resampling.NEAREST,center=(20,20));bullets.append(c)
emit('round',bullets,(20,20))
# Existing authored FOV material, exported at measured fixed cone angles. The
# 12px apex overlap sits behind the barrel and covers the bullet's own width.
for color,file in [('green','fov-light-green.png'),('yellow','fov-yellow.png'),('red','fov-neon-red.png')]:
 raw=Image.open(R/'assets/bossmode/ui'/file).convert('RGBA').crop((0,0,640,640));box=raw.getbbox();raw=raw.crop(box)
 for kind,angle,cellw in [('fan',.48,448),('down',.18,200)]:
  # Original wide cone sides reach half-width at about335px below its apex.
  width=round(raw.width*(512/raw.height)*math.tan(angle)/(.746));im=raw.resize((width,512),Image.Resampling.NEAREST);c=Image.new('RGBA',(cellw,528));c.alpha_composite(im,((cellw-width)//2,8));emit('warn_'+kind+'_'+color,[c],(cellw//2,20),cols=1)
(O/'manifest.json').write_text(json.dumps(A,indent=2));(W/'chronos_art.js').write_text("'use strict';\nconst CH23_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8');(W/'asset-audit.json').write_text(json.dumps(audit,indent=2))
# Source/contact review and onion sheet, saved outside the game presentation.
preview=Image.new('RGB',(320*4,380*3),(20,29,41));d=ImageDraw.Draw(preview)
for n,i in enumerate([0,1,2,3,4,5,6,7,8]):
 c=body[0].copy();g=barrel[i];c.alpha_composite(g,(192-54,230+48-46));c.alpha_composite(hands[0]);b=c.getbbox();q=c.crop(b);q.thumbnail((300,330),Image.Resampling.NEAREST);x=n%4*320;y=n//4*380;preview.paste(q,(x+(320-q.width)//2,y+28),q);d.text((x+8,y+7),f'body + independent barrel {i}',fill='white')
preview.save(W/'composite-review.png');print(json.dumps({'frames':len(audit),'sheets':len(A['sheets']),'allEvenNoClip':all(a['even']and a['noClip']for a in audit),'actorBinary':all(a['binary']for a in audit if '_warn_'not in a['key'])}))
