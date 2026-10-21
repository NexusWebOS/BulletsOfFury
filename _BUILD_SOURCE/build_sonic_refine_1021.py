"""Export reference-driven PixelLab charge/rifle flight loops, fixed 256px cells."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json, hashlib, math
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/sonic_refine_1021';D=R/'assets/game/shared/combat/sonic_refine_1021';O=R/'_shots/sonic_refine_1021'
D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
jobs=json.loads((S/'jobs.json').read_text());banks={};audit=[]
for kind,a in jobs.items():
 raw=[Image.open(p).convert('RGBA') for p in sorted((S/'raw'/kind).glob('[0-9][0-9].png'))]
 assert len(raw)==9 and all(im.size==(256,256) for im in raw)
 for color in ['red','green']:
  src=Image.open(R/('assets/game/levels/stage_01/miniboss/bosses/'+('razorback_furious/rzbf_' if color=='red' else 'razorback/rzb_')+'sonic_'+kind+'.png')).convert('RGBA')
  original=np.array(src);frames=[]
  for n,im in enumerate(raw):
   px=np.array(im);rgb=px[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2)
   # Gray model matte is not sonic light. Actual metal is restored below.
   px[(hi<155)&((hi-lo)<hi*.15),3]=0
   if color=='green':
    red=(rgb[:,:,0]>rgb[:,:,1]*1.20)&(rgb[:,:,0]>rgb[:,:,2]*1.15)
    ramp=np.array([.24,1,.14]);luma=np.array([.2126,.7152,.0722]);level=rgb[red]@luma
    px[red,:3]=np.clip(level[:,None]*ramp/(ramp@luma),0,255).round().astype('uint8')
   if kind=='bullet':
    y=np.indices(px.shape[:2])[0]
    # The moving energy never replaces the authored metal core and nose.
    metal=(original[:,:,3]>0)&(y>=116)&(original[:,:,1]>=original[:,:,0]*.42)
    px[metal]=original[metal]
   # Keep the original energy structure visible through the generated pulse;
   # the model's dissipating middle frames must never blank the charge.
   if kind=='charge':
    base=src.copy();base.putalpha(src.getchannel('A').point(lambda v:round(v*.90)))
    light=Image.fromarray(px);light.putalpha(light.getchannel('A').point(lambda v:round(v*.56)))
    out=Image.alpha_composite(base,light)
   else:
    permitted=src.getchannel('A').point(lambda v:255 if v else 0).filter(ImageFilter.MaxFilter(25))
    px[:,:,3]=np.minimum(px[:,:,3],np.array(permitted));out=Image.fromarray(px)
   if n==0 or n==8:out=src.copy()
   frames.append(out)
  sheet=Image.new('RGBA',(1280,512));cells=[]
  contact=Image.new('RGBA',(1280,548),(7,13,22,255));pen=ImageDraw.Draw(contact)
  for n,im in enumerate(frames):
   x,y=n%5*256,n//5*256;sheet.paste(im,(x,y));cells.append([x,y,256,256]);contact.alpha_composite(im,(x,n//5*274));pen.text((x+5,n//5*274+258),str(n),fill='white')
  name=kind+'_'+color;path=D/(name+'.webp');sheet.save(path,lossless=True,exact=True,method=6)
  contact.convert('RGB').save(O/(name+'-contact.jpg'),quality=95)
  frames[0].save(O/(name+'-motion.webp'),save_all=True,append_images=frames[1:],duration=65,loop=0,lossless=True)
  entry=dict(key='sr21_'+name,path=path.relative_to(R).as_posix(),sourceKey=('rzbf_' if color=='red' else 'rzb_')+'sonic_'+kind,w=256,h=256,pivot=[128,128],frames=9,fps=16,cells=cells)
  banks[name]=entry;audit.append(dict(**entry,job=a['job'],source=a['source'],firstLastExact=True,metalOriginal=kind=='bullet',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),unique=len({f.tobytes() for f in frames})))
(R/'assets/sonic_refine_art_1021.js').write_text("'use strict';\nObject.assign(SX21_ART.banks,"+json.dumps(banks,separators=(',',':'))+');\n',newline='\n')
(S/'export-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
tax=R/'assets/data/ART_TAXONOMY.json';text=tax.read_text(encoding='utf-8')
if 'sr21_' not in json.loads(text):
 entry={'sr21_':{'role':'reference_sonic_charge_and_missile_animation','sheet':None,'owner':'_BUILD_SOURCE/build_sonic_refine_1021.py','note':'PixelLab animations seeded with actual original red sonic charge and metal-core sound round. Four256x256 banks, pivot128,128 and common scale1. Original charge remains visible under the generated ripples; original metal pixels restored. Green energy derivative preserves original green family. Supersedes so21 charge/bullet opacity-only banks; original so21 wave/ring animations remain active.'}}
 tax.write_text('{\n'+json.dumps(entry,indent=2)[2:-2]+',\n'+text[2:],encoding='utf-8',newline='\n')
print(json.dumps(dict(banks=4,frames=36,bytes=sum(p.stat().st_size for p in D.glob('*.webp')))))
