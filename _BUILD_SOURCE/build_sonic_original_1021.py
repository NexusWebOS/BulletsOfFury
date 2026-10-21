"""Original pixels are authoritative; PixelLab animates their energy intensity.

No generated geometry or palette enters the game. Every output RGB pixel is
the actual source RGB, every alpha remains inside the original silhouette,
and frame0 is the exact original. Fixed256 canvas/pivot128 and scale1.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/sonic_original_1021';D=R/'assets/game/shared/combat/sonic_original_1021';O=R/'_shots/sonic_original_1021'
D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
jobs=json.loads((S/'jobs.json').read_text());art={'banks':{},'service':'PixelLab PixMiniMax with original-pixel projection','fps':18};audit=[]
def contact(name,frames):
 c=Image.new('RGBA',(256*5,274*math.ceil(len(frames)/5)),(7,13,22,255));draw=ImageDraw.Draw(c)
 for i,im in enumerate(frames):
  xy=(i%5*256,i//5*274);c.alpha_composite(im,xy);draw.text((xy[0]+4,xy[1]+258),str(i),fill='white')
 c.convert('RGB').save(O/(name+'-contact.jpg'),quality=95)
 frames[0].save(O/(name+'-motion.webp'),save_all=True,append_images=frames[1:],duration=56,loop=0,lossless=True)
for bank,a in jobs.items():
 original=Image.open(a['source']).convert('RGBA');src=np.array(original);assert original.size==(256,256)
 motion=np.array(Image.open(a.get('motionSource',a['source'])).convert('RGBA'))
 sourceL=(motion[:,:,:3]@np.array([.2126,.7152,.0722]))*(motion[:,:,3]/255)
 files=sorted((S/'raw'/a.get('rawBank',bank)).glob('[0-9][0-9].png'));assert len(files)==9,(bank,len(files));raw=[Image.open(p).convert('RGBA') for p in files];assert all(im.size==(256,256) for im in raw)
 frames=[original.copy()]
 for im in raw[1:]:
  px=np.array(im);light=(px[:,:,:3]@np.array([.2126,.7152,.0722]))*(px[:,:,3]/255)
  # H3's moving luminance is the only generated signal used. Original rings,
  # crescents, metal, streaks, colours and registration cannot be replaced.
  gain=1-.28*np.clip((sourceL-light)/np.maximum(8,sourceL),0,1)
  out=src.copy();out[:,:,3]=np.where(src[:,:,3]>0,np.maximum(1,np.rint(src[:,:,3]*gain)),0).astype('uint8')
  assert np.array_equal(out[:,:,:3],src[:,:,:3]);assert np.array_equal(out[:,:,3]>0,src[:,:,3]>0)
  frames.append(Image.fromarray(out))
 # The end pose is also the exact source; no repeated painted approximation.
 frames[-1]=original.copy();assert frames[0].tobytes()==original.tobytes()==frames[-1].tobytes()
 sheet=Image.new('RGBA',(256*5,256*2));cells=[]
 for i,im in enumerate(frames):
  x,y=i%5*256,i//5*256;sheet.paste(im,(x,y));cells.append([x,y,256,256])
 path=D/(bank+'.webp');sheet.save(path,lossless=True,method=6,exact=True);contact(bank,frames)
 decoded=Image.open(path).convert('RGBA');assert decoded.crop((0,0,256,256)).tobytes()==original.tobytes()
 entry=dict(key='so21_'+bank,path=path.relative_to(R).as_posix(),sourceKey=('rzbf_' if bank.endswith('_red') else 'rzb_')+'sonic_'+bank.split('_')[0],w=256,h=256,pivot=[128,128],frames=9,fps=18,cells=cells)
 art['banks'][bank]=entry
 audit.append(dict(**entry,source=Path(a['source']).relative_to(R).as_posix(),job=a['job'],motionSource=a.get('motionSource',a['source']),sourceSha256=hashlib.sha256(original.tobytes()).hexdigest(),firstFrameExact=True,lastFrameExact=True,allRGBExact=True,allSilhouettesExact=True,minimumAlphaGain=.72,unique=len({im.tobytes() for im in frames}),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(R/'assets/sonic_original_art_1021.js').write_text("'use strict';\nconst SX21_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'export-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
tax=R/'assets/data/ART_TAXONOMY.json';s=tax.read_text(encoding='utf-8')
s=s.replace('Six accepted PixelLab effect-only banks with green/red Razorback', 'Superseded by so21_ original-pixel animation; retained candidate sources only. Six PixelLab effect-only banks with green/red Razorback')
if 'so21_' not in json.loads(s):
 entry={'so21_':{'role':'original_sonic_sprite_animation','sheet':None,'owner':'_BUILD_SOURCE/build_sonic_original_1021.py','note':'Actual original green/red rzb/rzbf bullet, crescent wave, ring and charge sprites. PixelLab reference animation drives opacity only; every exported RGB pixel and silhouette exactly matches its original, first/last poses byte-identical. Fixed256 cells/pivot128,128/scale1. Native geometry and palettes, no added glyphs or invented shapes. Supersedes sx21_ redesign.'}}
 prefix=json.dumps(entry,indent=2)[2:-2];tax.write_text('{\n'+prefix+',\n'+s[2:],encoding='utf-8',newline='\n')
print(json.dumps(dict(banks=len(audit),frames=72,bytes=sum(p.stat().st_size for p in D.glob('*.webp')),unique=[(a['key'],a['unique']) for a in audit])))
