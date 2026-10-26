"""Owns the Stage59 source-preserving atlas, cells, anchors and provenance."""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/stage59_1024';O=R/'assets/game/shared/combat/stage59_1024';Q=R/'_shots/stage59_1024';O.mkdir(parents=True,exist_ok=True)
def eye(im):
 a=np.array(im);m=(a[:,:,3]>100)&(a[:,:,1]>110)&(a[:,:,2]>130)&(a[:,:,1].astype(int)-a[:,:,0]>35)&(a[:,:,2].astype(int)-a[:,:,0]>45)
 # Restrict to the actual central lens; tiny blue particles are not anchors.
 yy,xx=np.indices(m.shape);m&=(xx>88)&(xx<168)&(yy>64)&(yy<190)
 ys,xs=np.where(m);assert len(xs)>50
 return [int(round(float(xs.mean()))),int(round(float(ys.mean())))]
art={'sheets':{},'banks':{}};audit={'sources':[],'rejections':['warp: first Pro still reads as a mechanical corridor; superseded by liquid/foam warp_water.','black_charge: expanding rings, gray blobs and external sparks rejected; replaced by source-preserving lens-only composite.','black_drift frames5/6/7: invented colored sparks; use accepted0..4 and reverse instead.'],'outputs':[]}
base=Image.open(D/'references/black-3.png').convert('RGBA');ea=eye(base)
jobs=[('black_drift','black_drift',[0,1,2,3,4,3,2,1,0]),('black_spin','black_spin',list(range(17))),('black_charge','black_charge_clean',list(range(9))),('warp_motion','warp_motion',list(range(25)))]
for name,source,indices in jobs:
 if not (D/'raw'/source/f'{max(indices):02}.png').exists():print('Pending '+source);continue
 size=256 if name=='warp_motion' else 320;pivot=[size//2,size//2];frames=[];cols=5;rows=math.ceil(len(indices)/cols)
 sheet=Image.new('RGBA',(size*cols,size*rows));hit=Image.new('RGBA',sheet.size)
 for i,j in enumerate(indices):
  raw=Image.open(D/'raw'/source/f'{j:02}.png').convert('RGBA');assert raw.size==(256,256)
  measured=eye(raw) if name!='warp_motion' else [128,128]
  if name=='black_charge':
   # PixelLab supplies the animated lens only. Keep every original armor pixel
   # and surrounding space instead of accepting generated rings/props.
   aligned=Image.new('RGBA',(256,256));aligned.paste(raw,(ea[0]-measured[0],ea[1]-measured[1]))
   a=np.array(base);mask=((a[:,:,1].astype(int)-a[:,:,0]>35)&(a[:,:,2].astype(int)-a[:,:,0]>45)&(a[:,:,1]>110)&(a[:,:,3]>100));yy,xx=np.indices(mask.shape);mask&=(abs(xx-ea[0])<20)&(abs(yy-ea[1])<30)
   raw=Image.composite(aligned,base,Image.fromarray((mask*255).astype('uint8')));measured=ea
  cell=Image.new('RGBA',(size,size));offset=(pivot[0]-measured[0],pivot[1]-measured[1]);cell.paste(raw,offset)
  # Shared padding accommodates the spin's longer diagonals, no frame fitting.
  box=cell.getbbox();assert box and all([box[0]>=0,box[1]>=0,box[2]<=size,box[3]<=size])
  sx=i%cols*size;sy=i//cols*size;sheet.paste(cell,(sx,sy));white=Image.new('RGBA',cell.size,'white');white.putalpha(cell.getchannel('A'));hit.paste(white,(sx,sy))
  key='s5924_'+name+'_'+str(i);sheetkey='s5924_sheet_'+name;hitkey=key+'_hit';frames.append({'key':key,'hit':hitkey,'sheet':sheetkey,'hitSheet':sheetkey+'_hit','cell':[sx,sy,size,size],'pivot':pivot})
  audit['sources'].append({'bank':name,'output':i,'source':source,'frame':j,'measuredEye':measured,'translation':offset,'scale':1,'ink':box})
 for suffix,im in [('',sheet),('_hit',hit)]:
  if suffix and name=='warp_motion':continue
  path=O/(name+suffix+'.webp');im.save(path,'WEBP',lossless=True,exact=True);key='s5924_sheet_'+name+suffix;art['sheets'][key]={'key':'nca_'+key,'path':path.relative_to(R).as_posix(),'w':im.width,'h':im.height};audit['outputs'].append({'path':path.relative_to(R).as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 art['banks'][name]={'w':size,'h':size,'pivot':pivot,'fps':20 if name=='warp_motion' else 14,'frames':frames}
 # Contact proof from the exported cells, not a substitute hand-rendered sprite.
 contact=Image.new('RGB',(size*cols,(size+22)*rows),'#17212c');dr=ImageDraw.Draw(contact)
 for i,a in enumerate(frames):
  sx,sy,w,h=a['cell'];im=sheet.crop((sx,sy,sx+w,sy+h));x=i%cols*size;y=i//cols*(size+22);contact.paste(im,(x,y),im);dr.text((x+4,y+size+2),f'{name} {i}',fill='white')
 contact.save(Q/(name+'-export.png'))
(R/'assets/stage59_art_1024.js').write_text('"use strict";\nconst S5924_ART='+json.dumps(art,separators=(',',':'))+';\nfor(const s of Object.values(S5924_ART.sheets))XART._src[s.key]=s.path;\nfor(const b of Object.values(S5924_ART.banks))for(const a of b.frames){BOFX.cells[a.key]=[a.sheet,...a.cell];if(a.hitSheet in S5924_ART.sheets)BOFX.cells[a.hit]=[a.hitSheet,...a.cell];}\n',encoding='utf-8')
(O/'manifest.json').write_text(json.dumps(art,indent=2)+'\n');(D/'export-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
p=R/'assets/data/ART_TAXONOMY.json';tax=json.loads(p.read_text(encoding='utf-8'));tax['s5924_']={'role':'black_horizon_eye_registered_acting_and_water_warp','sheet':None,'owner':'_BUILD_SOURCE/build_stage59_1024.py','note':'Inspected PixelLab black hull drift/spin, original armor plus generated lens-only charge, white hit partners and opaque animated water tunnel. Common scales, fixed measured-eye pivots, even shared cells; no generated external rings or props.'};p.write_text(json.dumps(tax,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'banks':list(art['banks']),'frames':sum(len(b['frames']) for b in art['banks'].values()),'bytes':sum(a['bytes'] for a in audit['outputs'])}))
