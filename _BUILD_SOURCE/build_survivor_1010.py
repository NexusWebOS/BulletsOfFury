"""Own survivor ending pixels and registration; native crop/pad/translation only."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'_ART_SOURCES/survivor_1010'
DEST=ROOT/'assets/game/shared/cinematics/survivor_1010'
DEST.mkdir(parents=True,exist_ok=True)
banks={};sources=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def visible(im):return im.getchannel('A').point(lambda a:255 if a>80 else 0).getbbox()
def core_anchor(cell):
 p=np.asarray(cell).astype(float);h,w=p.shape[:2]
 # Measure visible light, including alpha, rather than a bright but nearly
 # transparent fringe. This is the core actually seen against the dark dish.
 rgb=p[:,:,:3]*p[:,:,3:4]/255
 score=rgb[:,:,1]-rgb[:,:,0]-rgb[:,:,2]*.45
 score[rgb[:,:,1]<180]=-1000
 assert score.max()>80,'Missing readable emerald core'
 # The whole luminous lens defines the station. Picking the single brightest
 # pixel can switch sides as a highlight changes or alpha is rounded by Canvas.
 remaining=set(map(tuple,np.argwhere(score>score.max()*.72)));groups=[]
 while remaining:
  seed=remaining.pop();todo=[seed];group=[seed]
  while todo:
   y,x=todo.pop()
   for dy,dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
    q=(y+dy,x+dx)
    if q in remaining:remaining.remove(q);todo.append(q);group.append(q)
  groups.append(group)
 lens=max(groups,key=lambda g:sum(score[y,x] for y,x in g));mass=sum(score[y,x] for y,x in lens)
 return [round(sum(x*score[y,x] for y,x in lens)/mass),round(sum(y*score[y,x] for y,x in lens)/mass)]
def plate(name):
 p=RAW/(name+'_raw.png');im=Image.open(p).convert('RGBA');w,h=im.size
 size=(w+w%2,h+h%2);out=Image.new('RGBA',size);out.alpha_composite(im,(0,0))
 path=DEST/(name+'.png');out.save(path,optimize=True)
 banks[name]=[dict(key='sv10_'+name,path=path.relative_to(ROOT).as_posix(),w=size[0],h=size[1],
  pivot=[size[0]//2,size[1]//2],content_rect=[0,0,w,h],sha256=sha(path),clip=name,source_rect=[0,0,w,h],scale=1)]
 sources.append(dict(bank=name,path=p.relative_to(ROOT).as_posix(),size=[w,h],sha256=sha(p)))
def reel(name,cols,rows,core=True):
 p=RAW/(name+'_raw.png');im=Image.open(p).convert('RGBA');assert im.getchannel('A').getextrema()[0]==0,(name,'Background is opaque')
 cells=[]
 for i in range(cols*rows):
  c,r=i%cols,i//cols;rect=[round(c*im.width/cols),round(r*im.height/rows),round((c+1)*im.width/cols),round((r+1)*im.height/rows)]
  cell=im.crop(rect);b=visible(cell);assert b,(name,i,'Empty slot')
  assert b[0]>2 and b[1]>2 and b[2]<cell.width-2 and b[3]<cell.height-2,(name,i,'Artwork crosses cell boundary',b,cell.size)
  anchor=core_anchor(cell) if core else [cell.width//2,cell.height//2]
  pivot=[192,192];shift=[pivot[0]-anchor[0],pivot[1]-anchor[1]]
  out=Image.new('RGBA',(384,384));out.alpha_composite(cell,tuple(shift))
  expected=[b[0]+shift[0],b[1]+shift[1],b[2]+shift[0],b[3]+shift[1]]
  assert list(visible(out))==expected,(name,i,'Visible pixels clipped',expected,visible(out))
  path=DEST/(name+'_'+str(i).zfill(2)+'.png');out.save(path,optimize=True)
  cells.append(dict(key='sv10_'+name+'_'+str(i).zfill(2),path=path.relative_to(ROOT).as_posix(),
   w=384,h=384,pivot=pivot,sha256=sha(path),clip=name,source_rect=rect,source_pivot=anchor,
   translation=shift,opaque_bounds=list(visible(out)),scale=1,
   registration='Measured emerald core' if core else 'Shared effect cell center'))
 assert len({q['sha256'] for q in cells})==cols*rows,(name,'Duplicate animation cells')
 banks[name]=cells
 sources.append(dict(bank=name,path=p.relative_to(ROOT).as_posix(),size=list(im.size),sha256=sha(p),grid=[cols,rows],frames=len(cells)))
plate('background');plate('detail')
reel('crawl',8,4);reel('burst',8,4);reel('contact',4,4,False)
(ROOT/'assets/survivor_art_1010.js').write_text('"use strict";\nconst SV10_ART='+json.dumps(banks,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
manifest=dict(tool='built-in image_gen',sources=sources,shipping_assets=[a for b in banks.values() for a in b],
 prompts='prompts.json',generation_ids='accepted_generations.json',native_references='references/native-manifest.json',
 normalization='One native scale per bank, integer translation to a measured emerald core, even shared transparent canvas, unchanged RGBA pixels. No repainting, per-frame fitting or interpolation.')
(RAW/'generation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({name:len(bank) for name,bank in banks.items()}))
