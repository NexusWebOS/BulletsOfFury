"""Own the intro's fixed-canvas banks, source audit and runtime registration."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,math
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/intro_repair_1021'
D=R/'assets/game/shared/cinematics/intro_repair_1021';D.mkdir(parents=True,exist_ok=True)
O=R/'_shots/intro_repair_1021';O.mkdir(parents=True,exist_ok=True)
spec={'clean':(S,[S/'satellite.png']),'corruption':(S/'raw/corruption',None),
      'dispatch':(S/'raw/dispatch',None),'turn':(S/'raw/turn-clean',None),
      'run':(S/'raw/run',None),'logo':(S/'raw/logo',None)}
art={'banks':{}};audit=[]
expected={'clean':1,'corruption':33,'dispatch':17,'turn':25,'run':33,'logo':33}
for bank,(folder,files) in spec.items():
 files=files or sorted(folder.glob('[0-9][0-9].png'))
 assert len(files)==expected[bank],(bank,'incomplete source bank',len(files),expected[bank])
 frames=[Image.open(p).convert('RGBA') for p in files];w,h=frames[0].size
 assert w%2==0 and h%2==0 and all(im.size==(w,h) for im in frames)
 assert bank=='clean' or len(frames)>=16
 columns=min(8,len(frames));sheet=Image.new('RGBA',(columns*w,math.ceil(len(frames)/columns)*h))
 for i,im in enumerate(frames):sheet.paste(im,(i%columns*w,i//columns*h))
 path=D/(bank+'.webp');sheet.save(path,lossless=True,method=6)
 contact=Image.new('RGBA',(columns*w,math.ceil(len(frames)/columns)*(h+18)),(7,13,22,255));onions=contact.copy()
 for i,im in enumerate(frames):
  xy=(i%columns*w,i//columns*(h+18));contact.alpha_composite(im,xy)
  ImageDraw.Draw(contact).text((xy[0]+3,xy[1]+h+1),str(i),fill='white')
  for j in [max(0,i-1),min(len(frames)-1,i+1)]:
   ghost=frames[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda v:round(v*.20)));onions.alpha_composite(ghost,xy)
  ghost=im.copy();ghost.putalpha(ghost.getchannel('A').point(lambda v:round(v*.65)));onions.alpha_composite(ghost,xy)
 contact.convert('RGB').save(O/(bank+'-accepted.jpg'),quality=95);onions.save(O/(bank+'-accepted-onions.png'))
 frames[0].save(O/(bank+'-accepted.webp'),save_all=True,append_images=frames[1:],duration=110,loop=1,lossless=True)
 a=dict(key='ip21_'+bank,path=path.relative_to(R).as_posix(),w=w,h=h,frames=len(frames),columns=columns,pivot=[w//2,h//2],sourceScale=1)
 art['banks'][bank]=a
 audit.append(dict(bank=bank,**a,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                   sources=[p.relative_to(R).as_posix() for p in files],
                   unique=len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames}),
                   normalization='Identity; uniform cells and pivot, no frame fitting, interpolation or generated duplicate holds.'))
(R/'assets/intro_repair_art_1021.js').write_text('const IP21_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
(S/'export-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
tax=R/'assets/data/ART_TAXONOMY.json';source=tax.read_text(encoding='utf-8')
if 'ip21_' not in json.loads(source):
 entry={'ip21_':{'role':'campaign_opening_plates_and_logo_effects','sheet':None,
  'note':'PixelLab Fury satellite corruption, Lizzie/Decker dispatch/turn/run and effect-only logo flash. Fixed even cells, centered common pivots and source scale1; own build_intro_repair_1021.py registers all sheets/cells. Native pilot cockpit/aircraft and original nbl_logo_0916 remain authoritative. Guarded PixelLab lower-band subtitle repair preserves every character pixel.'}}
 prefix=json.dumps(entry,indent=2,ensure_ascii=False)[2:-2];assert source.startswith('{\n')
 tax.write_text('{\n'+prefix+',\n'+source[2:],encoding='utf-8',newline='\n')
print(json.dumps(dict(banks=len(audit),frames=sum(a['frames'] for a in audit),runtimeBytes=sum(p.stat().st_size for p in D.glob('*.webp')))))
