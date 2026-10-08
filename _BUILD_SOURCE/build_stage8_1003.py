"""Import generated Stage 8 reels. Crop/registration only; preserve native RGBA.
Explicit measured boundaries are deliberate: generation is not a uniform atlas.
"""
from pathlib import Path
from PIL import Image
import json, shutil, hashlib
R=Path(__file__).resolve().parents[1]
SRC=R/'_ART_SOURCES/stage8_1003'; DST=R/'assets/game/stage8_1003'
GEN=Path.home()/'.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c'
FILES={'knight':'7c8be3fc-e777-494a-bfff-7579731249c2','wall':'0d5f2a49-602d-4215-80b3-3e24a0b22419','teleport':'205d867d-0050-4b8f-823e-922efebd2887','morph':'c25b9e04-a1b3-419e-89f7-8d25d928ba37','gravity':'6d9604e4-3925-4d12-81bd-c16b17f930d2','stalker':'99e9c865-94eb-4c49-bfcc-6d9b2ac1c523','prism':'e2ed7148-5334-4ee9-9bdd-df3a9aa27f44','beams':'b9c02a82-edff-4ea4-b548-7eb0549701d1','fov':'d1d648ff-9b80-4293-9e20-b03c3b2e50a5'}
SRC.mkdir(parents=True,exist_ok=True); DST.mkdir(parents=True,exist_ok=True)
meta={}
FILES.update({'impact':'1dc62267-4eaf-44a9-9339-5c8b71b148a9','shatter':'623152cd-259c-4b71-9e7a-4f7c8ba1759c'})
for name,uid in FILES.items():
 source=SRC/(name+'.png')
 if not source.exists():shutil.copyfile(GEN/('exec-'+uid+'.png'),source)
 im=Image.open(source).convert('RGBA'); W,H=im.size
 assert im.getchannel('A').getextrema()[0]==0, name+' lacks transparency'
 cells=[]
 if name=='knight':
  # Row boundaries and hips were measured on the padded accepted sheet.
  xs=[0,333,636,966,W]; ys=[0,422,826,H]
  anchors=[(174,267),(493,268),(813,268),(1110,268),(177,653),(499,653),(813,653),(1119,653),(177,1040),(495,1040),(803,1040),(1112,1040)]
  for i,(ax,ay) in enumerate(anchors):
   c,r=i%4,i//4;box=(xs[c],ys[r],xs[c+1],ys[r+1]);tile=im.crop(box)
   canvas=Image.new('RGBA',(448,448));canvas.paste(tile,(224-round(ax-box[0]),224-round(ay-box[1])))
   cells.append(canvas.resize((336,336),Image.Resampling.LANCZOS))
 elif name in ('gravity','stalker','prism'):
  for i in range(4):cells.append(im.crop((round(i*W/4),0,round((i+1)*W/4),H)).resize((216,288),Image.Resampling.LANCZOS))
 elif name in ('impact','shatter'):
  rows=2 if name=='impact' else 4
  for i in range(4*rows):cells.append(im.crop((round(i%4*W/4),round(i//4*H/rows),round((i%4+1)*W/4),round((i//4+1)*H/rows))).resize((256,256),Image.Resampling.LANCZOS))
 else:
  cols=4;ys={'wall':[0,447,830,H],'fov':[0,451,854,H],'morph':[0,423,811,H],'teleport':[0,627,H],'beams':[0,750,H]}[name]
  for row in range(len(ys)-1):
   for col in range(cols):
    box=(round(col*W/4),ys[row],round((col+1)*W/4),ys[row+1]);tile=im.crop(box)
    # Same row rectangle for every frame retains the authored loop origin.
    size=(192,256) if name in ('wall','fov') else (160,336) if name=='teleport' else (112,448) if name=='beams' else (256,336)
    cells.append(tile.resize(size,Image.Resampling.LANCZOS))
 cw,ch=cells[0].size;cols=4;rows=(len(cells)+cols-1)//cols
 sheet=Image.new('RGBA',(cw*cols,ch*rows))
 for i,cell in enumerate(cells):sheet.paste(cell,((i%cols)*cw,(i//cols)*ch))
 sheet.save(DST/(name+'.png'),optimize=True)
 meta[name]={'key':'s81003_'+name,'path':'assets/game/levels/stage_08/stage/stage8_1003/'+name+'.png','cw':cw,'ch':ch,'cols':cols,'frames':len(cells),'source':str(source.relative_to(R)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_size':[W,H]}
 # Four isolated crystal/code chunks from late shatter cells. Crop only:
 # particle motion comes from the runtime; all visible shapes are generated.
 if name=='shatter':
  boxes=[(351,953,450,1052),(491,975,584,1080),(359,1103,454,1200),(480,1108,574,1202)]
  out=Image.new('RGBA',(384,96))
  for j,box in enumerate(boxes):
   tile=im.crop(box);tile.thumbnail((80,80),Image.Resampling.LANCZOS);out.paste(tile,(j*96+(96-tile.width)//2,(96-tile.height)//2))
  out.save(DST/'shards.png',optimize=True)
  meta['shards']={'key':'s81003_shards','path':'assets/game/levels/stage_08/stage/stage8_1003/shards.png','cw':96,'ch':96,'cols':4,'frames':4,'source':meta[name]['source'],'sourceBoxes':boxes,'source_sha256':meta[name]['source_sha256']}
(DST/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
(R/'assets/stage8_art_1003.js').write_text('/* Generated reels; owning importer: build_stage8_1003.py. */\nconst S81003_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Imported',sum(a['frames'] for a in meta.values()),'RGBA frames in',len(meta),'families')
