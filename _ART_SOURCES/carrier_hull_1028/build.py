from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2]
O=R/'assets/game/levels/stage_06/boss/carrier_hull_1028';O.mkdir(parents=True,exist_ok=True)
S=R/'_ART_SOURCES/carrier_hull_1028';S.mkdir(parents=True,exist_ok=True)
def obj(path):
 s=(R/path).read_text(encoding='utf-8');return json.JSONDecoder().raw_decode(s[s.index('{'):])[0]
er=obj('assets/encounter_revision_art_1027.js');banks={};sources={};aliases={};masks={};preview=Image.new('RGBA',(1024,864),(8,14,22,255))
for side in ['closed','open']:
 a=er['clean_whv_'+side+'_w'];path=R/a['path'];im=Image.open(path).convert('RGBA');sources[a['path']]=hashlib.sha256(path.read_bytes()).hexdigest();rgba=np.array(im);rgb=rgba[:,:,:3].astype(float);alpha=rgba[:,:,3];solid=alpha>64;yy,xx=np.indices(alpha.shape)
 # 1015-style hard pixel light: derive all contour/seam pixels from this
 # actual hull. Four source-space cardinal fronts progressively reach inward.
 distance=np.minimum.reduce([xx/(im.width/2),(im.width-1-xx)/(im.width/2),yy/(im.height/2),(im.height-1-yy)/(im.height/2)])
 edge=solid&~np.array(Image.fromarray((solid*255).astype('uint8')).filter(ImageFilter.MinFilter(3))).astype(bool)
 luma=rgb.mean(2);local=np.array(Image.fromarray(luma.astype('uint8')).filter(ImageFilter.MinFilter(3)))
 seams=solid&((luma-local)>17)&(luma>45)
 frames=[]
 for f in range(17):
  if f==16:
   white=np.array(im);white[:,:,:3]=255;frame=Image.fromarray(white)
  else:
   extent=(f+1)/12 if f<12 else 1;strength=[.65,.9,.72,.50][(f-12)%4]if f>=12 else .25+f/11*.55
   hot=solid&(distance<=min(1,extent));amount=np.where(hot,strength,0)
   target=np.stack([np.minimum(255,65+luma*1.7),luma*.28,luma*.20],2)
   color=rgb*(1-amount[:,:,None])+target*amount[:,:,None]
   lamps=(edge|seams)&hot;ring=np.array(Image.fromarray((lamps*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)))>0
   out=np.array(im);out[:,:,:3]=np.clip(color,0,255).astype('uint8');out[lamps,:3]=[255,90 if f in [13,14]else 40,28]
   # Hard two-pixel red spill. Baked alpha, no runtime additive composition.
   glow=ring&~solid;out[glow,:3]=[210,20,28];out[glow,3]=145
   frame=Image.fromarray(out)
  frames.append(frame)
 sheet=Image.new('RGBA',(4*512,5*288))
 for i,frame in enumerate(frames):sheet.alpha_composite(frame,((i%4)*512,(i//4)*288))
 p=O/(side+'.png');sheet.save(p);banks[side]=dict(key='hc32_'+side,path=p.relative_to(R).as_posix(),cw=512,ch=288,cols=4,frames=17,pivot=[256,144],sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 aliases[a['key']]=side;aliases['whv_'+side+'_w']=side
 rows=[]
 for row in solid:
  bits=np.flatnonzero(np.diff(np.r_[False,row,False].astype('int8')));rows.append([[int(bits[j]),int(bits[j+1])]for j in range(0,len(bits),2)])
 masks[side]=rows
 if side=='closed':
  for j,f in enumerate([0,5,11,13,16]):
   preview.alpha_composite(frames[f],((j%2)*512,(j//2)*288))
  for j,frame in enumerate(frames):frame.save(S/f'hull_{j:02d}.png')
# Small fixed chimney columns use the existing exact native authored art.
source='assets/game/levels/stage_06/boss/carrier_revision_1028/fan_smoke.png';p=R/source;sources[source]=hashlib.sha256(p.read_bytes()).hexdigest();big=Image.open(p).convert('RGBA');small=Image.new('RGBA',(8*64,80))
for i in range(8):small.alpha_composite(big.crop((i*128,0,(i+1)*128,160)).resize((64,80),Image.Resampling.NEAREST),(i*64,0))
p=O/'smoke.png';small.save(p);banks['smoke']=dict(key='hc32_smoke',path=p.relative_to(R).as_posix(),cw=64,ch=80,cols=8,frames=8,pivot=[32,72],fps=12,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
art=dict(banks=banks,aliases=aliases,masks=masks,laserMounts=[dict(id='laser0',source=[176,168],dx=-80,dy=24),dict(id='laser3',source=[336,168],dx=80,dy=24)],hullRatio=.25)
(O/'manifest.json').write_text(json.dumps(dict(**art,sources=sources),indent=2),encoding='utf-8');(R/'assets/carrier_hull_art_1028.js').write_text('"use strict";\nconst HC32_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8');(S/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf-8');preview.save(S/'contact.png');print('Built two 17-frame hull banks, masks and eight-frame smoke')
