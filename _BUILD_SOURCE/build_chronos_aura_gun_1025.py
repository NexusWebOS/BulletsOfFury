"""Export inspected PixelLab recoil, rotor interior and physical crate opening.

Body stays a whole authored plate. Gun is the existing approved independent
module. Its receiver, handles, silhouette, length and palette stay canonical;
only the moving barrel interior comes from the selected PixelLab frames.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from scipy.ndimage import binary_erosion
import json,math,numpy as np,hashlib,ast
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_aura_gun_1025';O=R/'assets/game/shared/combat/chronos_aura_gun_1025';O.mkdir(exist_ok=True)
def source(file,name):
 p=D/(name+'-original.json')
 if not p.exists():
  s=(R/file).read_text();p.write_text(json.dumps(json.JSONDecoder().raw_decode(s[s.index('{'):])[0],indent=2),encoding='utf8')
 return json.loads(p.read_text())
ch=source('assets/chronos_modular_art_1023.js','ch23');ht=source('assets/hammer_tactical_art_1023.js','ht23')
def cell(art,bank,f=0):
 a=art['banks'][bank][f];im=Image.open(R/art['sheets'][a['sheet']]['path']).convert('RGBA');x,y,w,h=a['cell'];return im.crop((x,y,x+w,y+h))
def palette(im,variant):
 if not variant:return im.copy()
 a=np.array(im);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);lum=rgb@np.array([.2126,.7152,.0722]);neutral=(hi-lo<35)&(lum>30)&(lum<230)
 if variant=='_armor':
  value=np.minimum(235,lum*1.48+6);target=np.stack([value*.96,value*.99,value],2);amount=neutral*.68
 else:
  value=np.minimum(250,np.maximum(hi,lum*1.8));target=np.stack([value,lum*.22,lum*.28],2);amount=neutral*.72
 a[:,:,:3]=np.clip(rgb*(1-amount[:,:,None])+target*amount[:,:,None],0,255).astype('uint8');return Image.fromarray(a)
def export(art,name,frames,pivot,white=None):
 w,h=frames[0].size;assert w%2==h%2==0 and all(f.size==(w,h) for f in frames)
 cols=4;sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)));rows=[]
 for i,im in enumerate(frames):
  x=i%cols*w;y=i//cols*h;sheet.alpha_composite(im,(x,y));row=dict(key=name+'_'+str(i),sheet=name,cell=[x,y,w,h],w=w,h=h,pivot=pivot,bounds=list(im.getbbox() or [0,0,0,0]))
  if white:row['white']=white+'_'+str(i)
  rows.append(row)
 path=O/(name+'.webp');sheet.save(path,lossless=True);art['sheets'][name]=dict(key='nca_'+name,path=path.relative_to(R).as_posix(),w=sheet.width,h=sheet.height,sha256=hashlib.sha256(path.read_bytes()).hexdigest());return rows
def hits(frames):
 out=[]
 for im in frames:
  q=Image.new('RGBA',im.size,'white');q.putalpha(im.getchannel('A'));out.append(q)
 return out

# Reject generated recoil3-5: they invent a side grip/extra weapon silhouette.
# These six accepted whole poses keep the two hands at the original waist mount.
selected=[0,1,2,6,7,8]
body=[Image.open(D/'body'/f'{i:02}.png').convert('RGBA').resize((384,512),Image.Resampling.NEAREST) for i in selected]
# Foreground grips are copied from these same whole poses, not fabricated limbs.
handMask=Image.new('L',(384,512));ImageDraw.Draw(handMask).polygon([(151,260),(163,253),(189,266),(222,252),(239,263),(239,293),(216,307),(167,305),(151,292)],fill=255)
hands=[]
for im in body:
 q=im.copy();q.putalpha(ImageChops.multiply(q.getchannel('A'),handMask));hands.append(q)
base=cell(ch,'barrel');v=np.array(base);yy,xx=np.indices(v.shape[:2]);inside=binary_erosion(v[:,:,3]>64,iterations=2)&(yy>=85)&(yy<187)
rotors=[base]
for i in range(1,9):
 generated=Image.open(D/'barrel'/f'{i:02}.png').convert('RGBA').crop((12,8,116,216));g=np.array(generated);out=v.copy()
 # PixelLab changed illumination in some rotations. Match the original gun's
 # tonal distribution in each rotor section; never copy its altered housing.
 for y0,y1 in [(85,112),(112,145),(145,168),(168,188)]:
  mask=inside&(yy>=y0)&(yy<y1);ref=v[:,:,:3][mask].mean(1);values=g[:,:,:3][mask].mean(1)
  q=np.linspace(0,1,65);old=np.quantile(values,q);target=np.quantile(ref,q);u,indices=np.unique(old,return_index=True);value=np.interp(values,u,target[indices]);out[:,:,:3][mask]=np.clip(value[:,None],0,255).astype('uint8')
 rotors.append(Image.fromarray(out))
crate=[Image.open(D/'crate'/f'{i:02}.png').convert('RGBA') for i in range(9)]
for bank,frames,pivot in [('body',body,[192,230]),('hands',hands,[192,230]),('barrel',rotors,[54,46])]:
 hit='ch23_'+bank+'_hit';ch['banks'][bank+'_hit']=export(ch,hit,hits(frames),pivot)
 for variant in ['', '_armor','_red']:
  ch['banks'][bank+variant]=export(ch,'ch23_'+bank+variant,[palette(im,variant) for im in frames],pivot,hit)
ht['banks']['crate']=export(ht,'ht23_crate',crate,[40,40])
ch['owner']='_BUILD_SOURCE/build_chronos_aura_gun_1025.py';ch['recoilFrames']=selected;ch['jobs1025']=json.loads((D/'jobs.json').read_text())['jobs']
ht['crateOwner1025']=ch['owner']
# Preserve the tactical armor manifest which shares the generated JS file.
p=R/'assets/hammer_tactical_art_1023.js';s=p.read_text();start=s.index('{');_,end=json.JSONDecoder().raw_decode(s[start:]);p.write_text(s[:start]+json.dumps(ht,separators=(',',':'))+s[start+end:],encoding='utf8',newline='\n')
(R/'assets/chronos_modular_art_1023.js').write_text('"use strict";\nconst CH23_ART='+json.dumps(ch,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
(O/'manifest.json').write_text(json.dumps(dict(chaingun=ch,crate=ht['banks']['crate'],sources=dict(bodyFrames=selected,rotor='PixelLab moving interior; original receiver/handles/alpha and measured muzzle preserved',aura='Native current-plate silhouette stencil; exact frame/pivot/scale, bounded short contour echoes')),indent=2),encoding='utf8')
proof=Image.new('RGB',(6*384,3*300),'#101e2d');draw=ImageDraw.Draw(proof)
for row,variant in enumerate(['','_armor','_red']):
 for i in range(6):
  im=Image.new('RGBA',(384,512));im.alpha_composite(palette(body[i],variant));im.alpha_composite(palette(rotors[(i+1)%9],variant),(138,232));im.alpha_composite(palette(hands[i],variant));im=im.crop((70,140,320,440));proof.paste(im,(i*384,row*300),im)
  draw.text((i*384+256,row*300+12),f'{variant or "regular"} {i}',fill='white')
proof.save(R/'_shots/chronos_aura_gun_1025/compiled-gun.png')
print('Exported six whole recoil poses, nine source-preserving rotor poses, and nine actual crate opening poses in all materials.')
