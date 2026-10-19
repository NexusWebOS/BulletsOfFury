"""Register genuine PixelLab quarter-turns; keep charge changes inside the eyes."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/volcano_head_1019';D=R/'assets/game/levels/stage_08/boss/volcano_head_1019';O=R/'_shots/overnight_combat_1019/volcano'
D.mkdir(exist_ok=True);meta=json.loads((S/'measured.json').read_text());ref=Image.open(S/'reference.png').convert('RGBA');refa=np.asarray(ref);yy,xx=np.indices((128,128));eyes=meta['referenceEyes']
aperture=np.zeros((128,128),bool)
for x,y in eyes:aperture|=((xx-x)**2+(yy-y)**2<=4.6**2)
# Only the authored warm lamp pixels inside the two physical eye apertures.
aperture&=(refa[:,:,0]>120)&(refa[:,:,0]>refa[:,:,1]*1.25)&(refa[:,:,3]>180)
banks={'spin':[],'charge':[]};images={};records=[]
def save(bank,i,im,eye,angle=0,source=None):
 assert im.size==(128,128)
 p=D/f'head_{bank}_{i:02}.png';im.save(p,optimize=True)
 a=dict(key=f'vh19_{bank}_{i:02}',path=p.relative_to(R).as_posix(),w=128,h=128,pivot=[64,64],bounds=list(im.getbbox()),eyes=eye,angle=angle)
 banks[bank].append(a);images.setdefault(bank,[]).append(im);records.append(dict(bank=bank,index=i,source=source,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
for row in meta['rows']:
 im=Image.open(S/row['source']).convert('RGBA');dx,dy=[round(64-v) for v in row['center']];out=Image.new('RGBA',(128,128));out.paste(im,(dx,dy))
 assert abs(dx)<=2 and abs(dy)<=2
 assert row['error']<1.3
 save('spin',row['index'],out,[[round(x+dx,3),round(y+dy,3)] for x,y in row['eyes']],row['angle'],row['source'])
charge=[]
for i in range(16):
 source=f'charge/frame_{i+1:02}.png';generated=np.array(Image.open(S/source).convert('RGBA'));a=refa.copy();a[aperture,:3]=generated[aperture,:3]
 # The unchanged armor plate is deliberate: the source candidate whitened the
 # cheeks and jaw as well as the lamps. No such whole-face wash is accepted.
 assert np.array_equal(a[~aperture],refa[~aperture])
 charge.append((float(a[aperture,:3].mean()),source,Image.fromarray(a)))
for i,(energy,source,im) in enumerate(sorted(charge,key=lambda q:q[0])):
 save('charge',i,im,eyes,source=source)
assert len({r['sha256'] for r in records if r['bank']=='spin'})==32
for bank,frames in images.items():
 sheet=Image.new('RGBA',(1024,math.ceil(len(frames)/8)*148),(8,13,23,255));onion=sheet.copy()
 for i,im in enumerate(frames):
  at=(i%8*128,i//8*148);sheet.alpha_composite(im,at);ImageDraw.Draw(sheet).text((at[0]+3,at[1]+128),str(i),fill='white')
  for j in [(i-1)%len(frames),(i+1)%len(frames)]:
   ghost=frames[j].copy();ghost.putalpha(ghost.getchannel('A').point(lambda a:round(a*.2)));onion.alpha_composite(ghost,at)
  onion.alpha_composite(im,at)
 sheet.save(O/(bank+'-accepted.png'));onion.save(O/(bank+'-accepted-onions.png'));frames[0].save(O/(bank+'-accepted.webp'),save_all=True,append_images=frames[1:],duration=75 if bank=='spin' else 90,loop=0,lossless=True)
art=dict(canvas=[128,128],pivot=[64,64],scale=1,banks=banks)
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n');(R/'assets/volcano_head_art_1019.js').write_text('"use strict";\n// Owned by build_volcano_head_1019.py.\nconst VH19_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'accepted-registration.json').write_text(json.dumps(dict(frame=[128,128],pivot=[64,64],scale=1,referenceEyes=eyes,maxTranslation=1,eyeFitMax=max(q['error'] for q in meta['rows']),unique={bank:len({r['sha256'] for r in records if r['bank']==bank}) for bank in banks},method='32 generated poses1..8 from four pinned quarter-turns. Integer lamp-derived mount registration only, no resizing. Charge copies generated lamp pixels only onto the actual authored face, ordered by increasing lamp energy for a charge-up;16 timed frames contain10 distinct lamp states and natural holds.',rejected={'fullLoop':'733f3cb3-aad1-4351-bc46-c54285bfb3d5 only blinked; not shipped','chargeArmor':'Whole-face whitening excluded; only lamp apertures accepted.'},frames=records),indent=2)+'\n')
tax=R/'assets/data/ART_TAXONOMY.json';t=json.loads(tax.read_text(encoding='utf-8-sig'));t['vh19_']={'role':'stage8_volcano_detached_head_animation','sheet':None,'note':'32 genuine PixelLab quarter-turn poses,16 lamp-only charge frames.128x128/pivot64,64,scale1, measured per-frame eyes and angles. Owner build_volcano_head_1019.py; native volcano_head_1019.js.'};tax.write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(spin=32,charge=16,aperturePixels=int(aperture.sum()),bytes=sum(p.stat().st_size for p in D.glob('*.png')))))
