"""Export only authored input cells; no graphics painted or fabricated."""
from pathlib import Path
from PIL import Image
import numpy as np,json
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/siege_tanks_1010'
out={}
for unit in ['sonic','devastator','deviator']:
 raw=Image.open(SRC/'returned'/f'{unit}_kit.png').convert('RGBA')
 names=['assembled','hull','track_left','track_right','weapon','pod','reactor','sensor']
 # The concept returns have generous spacing but uneven column pitch. Cut
 # their eight connected authored pieces, not nominal grid boundaries.
 mask=np.array(raw)[:,:,3]>160;hh,ww=mask.shape;seen=np.zeros(mask.shape,dtype=bool);pieces=[]
 for yy,xx in zip(*np.where(mask)):
  if seen[yy,xx]:continue
  q=deque([(int(xx),int(yy))]);seen[yy,xx]=True;count=0;x0=x1=int(xx);y0=y1=int(yy)
  while q:
   x,y=q.popleft();count+=1;x0=min(x0,x);x1=max(x1,x);y0=min(y0,y);y1=max(y1,y)
   for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=nx<ww and 0<=ny<hh and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;q.append((nx,ny))
  if count>2000:pieces.append((count,[x0,y0,x1+1,y1+1]))
 pieces=sorted(pieces,reverse=True)[:8]
 if len(pieces)!=8:raise ValueError(f'{unit}: expected eight parts, got {len(pieces)}')
 top=sorted([b for n,b in pieces if (b[1]+b[3])/2<hh/2],key=lambda b:b[0])
 bottom=sorted([b for n,b in pieces if (b[1]+b[3])/2>=hh/2],key=lambda b:b[0])
 rects=top+bottom
 if len(top)!=4 or len(bottom)!=4:raise ValueError(f'{unit}: unexpected part rows')
 out[unit]={}
 for i,name in enumerate(names):
  b=rects[i];rect=[max(0,b[0]-5),max(0,b[1]-5),min(ww,b[2]+5),min(hh,b[3]+5)]
  cell=raw.crop(rect);a=np.array(cell);a[:,:,3][a[:,:,3]<64]=0;cell=Image.fromarray(a)
  box=cell.getchannel('A').point(lambda v:255 if v>160 else 0).getbbox()
  if not box:raise ValueError(f'Empty {unit}/{name}')
  cell.save(SRC/'reference'/f'{unit}_{name}.png')
  out[unit][name]={'rect':rect,'bounds':box}
(SRC/'kit_cells.json').write_text(json.dumps(out,indent=2)+'\n')
print('Exported24 authored seed components')
