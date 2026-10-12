"""Register measured generated HUD plates without changing their pixels."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'_ART_SOURCES/side_hud_1012';OUT=ROOT/'docs/previews/side_hud_1012'
boxes=json.loads((SRC/'well-measurements.json').read_text(encoding='utf-8'))
names=[('command-bastion','Command Bastion','Closest to Armored Command. Heavy connected frames and bright amber indicators.'),
 ('split-batteries','Split Batteries','Separate instrument pods, with the maneuvers and stock counters in their own sockets.'),
 ('tactical-rails','Tactical Rails','Even rails, broad display wells and a restrained, uniform instrument layout.'),
 ('siege-console','Siege Console','Vented armor with fewer illuminated seams and a heavier military finish.'),
 ('command-glass','Command Glass','Compact beveled housings with bright recessed meter strips.')]
concepts=[]
for i,(key,name,note) in enumerate(names,1):
 path=SRC/(key+'.png');im=Image.open(path)
 assert im.size==(1024,1536) and im.mode=='RGBA'
 left=sorted([q[:4] for q in boxes[key] if q[0]<512],key=lambda q:(q[1],q[0]))
 right=sorted([q[:4] for q in boxes[key] if q[0]>512],key=lambda q:(q[1],q[0]))
 largeL=[q for q in left if q[3]>100];largeR=[q for q in right if q[3]>100]
 bars=[q for q in left if 40<q[3]<100];maneuvers=sorted([q for q in left if q[3]<40],key=lambda q:q[0])
 assert len(largeL)==len(largeR)==5 and len(bars)==len(maneuvers)==2
 wells=dict(zip(['scores','roll','somer','weapon','pilot'],largeL))
 wells.update(zip(['radar','special','lives','missiles','lock'],largeR))
 wells.update(zip(['speed','shield'],bars));wells.update(zip(['rollBar','somerBar'],maneuvers))
 wells['specialBar']=next(q for q in right if q[3]<40 and largeR[1][1]<q[1]<largeR[2][1])
 concepts.append(dict(id=key,name=name,number=i,note=note,size=list(im.size),wells=wells,
  path='../../../_ART_SOURCES/side_hud_1012/'+key+'.png',sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
record=dict(date='2026-10-12',status='concepts awaiting Mike selection',generator='built-in image_gen',
 canvas=[2048,1152],playfield=[484,0,1080,1152],logicalPlayfield=[480,512],sourceColumn=[512,1536],
 layout='Full-height proportional playfield; left and right HUD columns outside it in every preview state.',concepts=concepts)
(OUT/'concepts.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
(SRC/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Registered five native-alpha 1024x1536 side HUD plates; source pixels unchanged.')
