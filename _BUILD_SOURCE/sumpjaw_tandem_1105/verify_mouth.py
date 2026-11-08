"""Verify every emission phase stays inside the approved toxic mouth pixels."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');A=W/'authored';m=json.loads((R/'assets/game/levels/stage_07/miniboss/sumpjaw_serpents_1104/manifest.json').read_text());b=m['banks']['body0'];strip=Image.open(A/'strips/mouth.png').convert('RGBA');checks=[]
for jaw in [0,1]:
 index=jaw*32;p=next(p for p in b['pages']if p['start']<=index<p['start']+p['frames']);i=index-p['start'];im=Image.open(R/p['path']).convert('RGBA').crop((i%b['cols']*176,i//b['cols']*176,i%b['cols']*176+176,i//b['cols']*176+176));a=np.array(im);yy,xx=np.indices(a.shape[:2]);cx,cy=90,116+jaw*4
 mask=(((xx-cx)/17)**2+((yy-cy)/16)**2<1)&(a[:,:,1]>a[:,:,0].astype(float)*1.12)&(a[:,:,1]>a[:,:,2].astype(float)*1.22)&(a[:,:,3]>0)
 for d in range(32):
  expected=np.array(Image.fromarray(mask.astype('uint8')*255).rotate(-d*360/32,Image.Resampling.NEAREST,center=(88,88)))>0
  phases=[]
  for level in range(4):
   for phase in range(8):
    j=(level*8+phase)*64+jaw*32+d;f=np.array(strip.crop((j%8*176,j//8*176,j%8*176+176,j//8*176+176)))
    checks.append(bool(np.array_equal(f[:,:,3]>0,expected)));phases.append(f.tobytes())
  # The approved orb source includes held frames. Retain that authored timing;
  # each emission level must animate, and levels must also remain different.
  checks.append(all(len(set(phases[level*8:(level+1)*8]))>1 for level in range(4))and len(set(phases))>=16)
out=dict(passed=all(checks),frames=2048,headingAndJawVariants=64,timelineCellsPerVariant=32,distinctImagesPerVariant=16,checks=len(checks),note='All nonzero-alpha emission pixels exactly match the rotated original inner toxic core mask; no outer body/tail rim pixels. Source hold frames retained.');(W/'mouth-checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));raise SystemExit(0 if out['passed']else 1)
