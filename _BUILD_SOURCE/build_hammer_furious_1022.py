from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from scipy.ndimage import label
import json,math,hashlib,shutil,sys
import numpy as np
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/hammer_furious_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Furious-1022';D=W/'shipping';D.mkdir(exist_ok=True)
A={'banks':{},'sheets':{},'legacyRed':{},'sources':{},'version':1};audit=[]
# Explicit row cuts/baselines from source-sheet review; never silhouette-fit
# each pose. Each source image has ONE measured anatomical pixel unit.
S={
 'blue-combo':([0,310,658,921,1254],[309,645,920,1215],1),
 'corrupt-combo':([0,316,658,925,1254],[315,648,925,1219],1),
 'corrupt-redcombo':([0,318,658,927,1254],[315,648,925,1219],1),
 'blue-sides':([0,336,637,964,1254],[335,636,963,1219],1),
 'corrupt-sides':([0,327,633,942,1254],[326,632,940,1205],1),
 'blue-throw':([0,397,751,1086],[396,750,1062],.83),
 'corrupt-throw':([0,375,722,1086],[374,721,1062],.83),
 'corrupt-redthrow':([0,377,723,1086],[374,722,1062],.83),
 'blue-rage':([0,362,702,1086],[357,697,1056],.83),
 'corrupt-rage':([0,370,720,1086],[361,719,1070],.83),
}
def source(name):
 p=W/'generated'/(name+'.png');im=Image.open(p).convert('RGBA');A['sources'][name]={'size':list(im.size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};return im
def cells(name):
 im=source(name);ys,feet,scale=S[name];rows=[];a=np.asarray(im);groups,n=label(a[:,:,3]>20,structure=np.ones((3,3)));sizes=np.bincount(groups.ravel());parts=[]
 for z in np.flatnonzero(sizes>3500):
  if not z:continue
  yy,xx=np.where(groups==z);parts.append((int(z),(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1),float(xx.mean())))
 for i in range(4*(len(ys)-1)):
  r=i//4;c=i%4;cx=(c+.5)*im.width/4
  # Whole authored alpha component, selected by source row baseline/column.
  # Never cut a figure at an imaginary grid boundary or retain its neighbor.
  z,box,_=min(parts,key=lambda q:abs(q[1][3]-feet[r])*2+abs(q[2]-cx))
  x0,y0,x1,y1=box;data=a[y0:y1,x0:x1].copy();data[:,:,3][groups[y0:y1,x0:x1]!=z]=0;crop=Image.fromarray(data);w,h=crop.size
  crop=crop.resize((round(w*scale),round(h*scale)),Image.Resampling.NEAREST);out=Image.new('RGBA',(448,448));out.alpha_composite(crop,(round(224+(x0-cx)*scale),round(382+(y0-feet[r])*scale)));rows.append(out)
 A['sources'][name].update(rowCuts=ys,footBaselines=feet,commonSourceUnit=scale)
 return rows
def head(im,kind):
 a=np.array(im);r,g,b,al=[a[:,:,i].astype(float) for i in range(4)]
 m=(b>160)&(b>r*1.35)&(g>70) if kind=='blue' else (b>170)&(r>135)&(b>g*1.2)
 m&=(al>100);groups,n=label(m);best=None
 for z in range(1,n+1):
  y,x=np.where(groups==z)
  if len(x)<15:continue
  score=len(x)
  if best is None or score>best[0]:best=(score,[round(float(x.mean())),round(float(y.mean()))],[int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1])
 return (best[1],best[2]) if best else ([192,280],[170,250,214,310])
def red(im):
 a=np.array(im);v=a[:,:,:3].astype(float);hi=v.max(2);lo=v.min(2);sat=hi-lo;energy=(v[:,:,2]>v[:,:,0]*1.15)&(v[:,:,2]>70);neutral=(sat<35)&(hi>24)&(hi<220);purple=(v[:,:,2]>v[:,:,1]*1.2)&(v[:,:,2]>35)
 m=(energy|purple|neutral)&(a[:,:,3]>0);lum=v@np.array([.2126,.7152,.0722]);value=np.maximum(hi,lum*1.4)
 for c,f in enumerate([1,.25,.29]):a[:,:,c][m]=np.clip(value[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def chrome(im):
 a=np.array(im);v=a[:,:,:3].astype(float);m=(v.max(2)-v.min(2)<28)&(v.max(2)>27)&(v.max(2)<235)&(a[:,:,3]>0);l=v@np.array([.2126,.7152,.0722]);s=np.minimum(245,130+l*.85)
 for c,f in enumerate([.96,1,1.04]):a[:,:,c][m]=np.clip(s[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def emit(name,ims,kind,pivot=[224,258],points=None,white=True,legacy=None):
 side=ims[0].width;assert all(im.size==(side,side) for im in ims);cols=4;sheet=Image.new('RGBA',(side*cols,side*math.ceil(len(ims)/cols)));hit=sheet.copy();rows=[]
 for i,im in enumerate(ims):
  box=im.getbbox();assert box,(name,i);x=i%cols*side;y=i//cols*side;sheet.alpha_composite(im,(x,y));h=Image.new('RGBA',im.size,'white');h.putalpha(im.getchannel('A'));hit.alpha_composite(h,(x,y));at,bounds=head(im,'blue' if kind=='blue' else 'corrupt');tip=points[i] if points else at
  prefix='hf22_' if name in ['blue_tool','blue_tool_red','corrupt_tool','corrupt_tool_red'] else 'ha21_hf22_'
  row={'key':f'{prefix}{name}_{i}','sheet':'hf22_'+name,'cell':[x,y,side,side],'w':side,'h':side,'pivot':pivot,'bounds':list(box),'tip':tip,'glow':at,'kind':kind,'bank':name,'frame':i,'_hf22':True}
  if white:row['white']=f'{prefix}{name}_hit_{i}'
  rows.append(row);audit.append({'bank':name,'frame':i,'bounds':list(box),'pivot':pivot,'tip':tip})
 for suffix,img in [('',sheet)]+([('_hit',hit)] if white else []):
  p=D/(name+suffix+'.webp');img.save(p,lossless=True,exact=True,method=5);A['sheets']['hf22_'+name+suffix]={'key':'nca_hf22_'+name+suffix,'path':'assets/game/shared/combat/hammer_furious_1022/'+p.name,'w':img.width,'h':img.height,'legacy':bool(legacy)}
 A['banks'][name]=rows;return rows
for kind in ['blue','corrupt']:
 combo=cells(kind+'-combo');sides=cells(kind+'-sides');throw=cells(kind+'-throw');rage=cells(kind+'-rage')
 # Single-frame crossing keys have an explicit measured anatomical source
 # unit and baseline, rather than being fitted to their changing silhouette.
 cross=source(kind+'-cross');scale=.31 if kind=='blue' else .285;root=(640,1066) if kind=='blue' else (690,1108);c=Image.new('RGBA',(448,448));c.alpha_composite(cross.resize((round(cross.width*scale),round(cross.height*scale)),Image.Resampling.NEAREST),(round(224-root[0]*scale),round(382-root[1]*scale)))
 A['sources'][kind+'-cross'].update(commonSourceUnit=scale,sourceFootRoot=root)
 # The generated multi-pose sheet does not consistently follow the requested
 # left/right order. Reviewed physical keys are explicitly reordered.
 if kind=='blue':left=[ImageOps.mirror(sides[0]),ImageOps.mirror(sides[1]),sides[3],c,sides[4],sides[5],sides[6]];right=[sides[8],sides[9],ImageOps.mirror(c),sides[10],sides[11],sides[12],sides[13]]
 else:left=[sides[8],sides[9],sides[10],c,sides[3],sides[4],sides[5],sides[6]];right=[sides[0],sides[1],sides[2],ImageOps.mirror(c),sides[11],sides[12],ImageOps.mirror(sides[5])]
 wind=[combo[0],throw[1],combo[1],throw[2],combo[2],throw[3]] if kind=='blue' else [combo[0],throw[1],throw[2],combo[2],combo[3]]
 descent=[combo[i] for i in ([4,5,6,7] if kind=='blue' else [4,6,7])];bank=wind+descent+[combo[6],combo[8],combo[0]];end=len(wind)+len(descent)-1;A.setdefault('phases',{})[kind]={'windEnd':len(wind)-1,'strikeEnd':end,'recoverStart':end+1};sidebank=left+right+[combo[0]];impact=head(bank[end],kind);tips=[head(im,kind)[0] for im in bank];tips[end]=[impact[0][0],min(441,impact[1][3]+9)]
 A.setdefault('sides',{})[kind]={'left':len(left),'right':len(right),'ready':len(sidebank)-1}
 normal=emit(kind+'_jump',bank,kind,points=tips);side_rows=emit(kind+'_sides',sidebank,kind);throw_rows=emit(kind+'_throw',throw[:8],kind);emit(kind+'_rage',[rage[i] for i in [0,3,4,5,6,7,8,9,10,11]],kind)
 # One physical generated tool is pre-rendered into32 stored orientations.
 tool=throw[8];at,_=head(tool,kind);canvas=Image.new('RGBA',(512,512));canvas.alpha_composite(tool,(256-at[0],256-at[1]));turns=[canvas.rotate(-i*360/32,resample=Image.Resampling.NEAREST,center=(256,256)) for i in range(32)];emit(kind+'_tool',turns,kind,[256,256],points=[[256,256]]*32)
 for name,ims in [('jump',bank),('sides',sidebank),('throw',throw[:8]),('tool',turns)]:
  if kind=='corrupt' and name=='jump':
   re=cells('corrupt-redcombo');rt=cells('corrupt-redthrow');colored=[re[0],rt[1],rt[2],re[2],re[3],re[4],re[6],re[7],re[6],re[8],re[0]]
  elif kind=='corrupt' and name=='throw':colored=cells('corrupt-redthrow')[:8]
  else:colored=[red(im) for im in ims]
  rr=emit(kind+'_'+name+'_red',colored,kind,[256,256] if name=='tool' else [224,258],points=([[256,256]]*32 if name=='tool' else tips if name=='jump' else None))
  for a,b in zip(rr,A['banks'][kind+'_'+name]):a['tip']=b['tip'];a['glow']=b['glow']
 if kind=='blue':
  for name,ims in [('jump',bank),('sides',sidebank),('throw',throw[:8])]:
   rr=emit(kind+'_'+name+'_armor',[chrome(im) for im in ims],kind,points=tips if name=='jump' else None)
   for a,b in zip(rr,A['banks'][kind+'_'+name]):a['tip']=b['tip'];a['glow']=b['glow']
# Fixed red auras, sampled as stored frames, never a browser glow/opacity effect.
aura=source('aura')
for kind,r in [('blue',0),('corrupt',1)]:
 ims=[]
 for col in range(4):
  x0=round(col*aura.width/4);x1=round((col+1)*aura.width/4);y0=round(r*aura.height/2);y1=round((r+1)*aura.height/2);im=aura.crop((x0+3,y0+3,x1-3,y1-3)).resize((320,320),Image.Resampling.NEAREST);cell=Image.new('RGBA',(448,448));cell.alpha_composite(im,(64,74));ims.append(cell)
 emit(kind+'_aura',ims,kind,white=False)
# Stored orientations of the game's actual warning cone. New combo/throw
# tells never rotate or stretch a cone at render time.
hj=json.loads((R/'assets/hammer_jump_art_1022.js').read_text().split('const HJ22_ART=')[1].rstrip(';\n'));warning=[]
for a in hj['banks']['warning_cone']:
 p=R/hj['sheets'][a['sheet']]['path'];im=Image.open(p).convert('RGBA');x,y,w,h=a['cell'];c=Image.new('RGBA',(448,448));c.alpha_composite(im.crop((x,y,x+w,y+h)),(64,32));warning.append(c)
for name,angle,pivot in [('warning_down',0,[224,366]),('warning_up',180,[224,82]),('warning_left',-90,[403,224]),('warning_right',90,[45,224])]:emit(name,[im.rotate(angle,Image.Resampling.NEAREST,center=(224,224)) for im in warning],'shared',pivot,white=False)
# Preserve red armor through the remaining legacy actions without replacing
# their pose or motion owners. These source-sized palettes are loaded lazily.
cache={}
for source_path,marker in [(R/'assets/hammer_acting_art_1021.js','const HA21_ART='),(R/'assets/hammer_correction_art_1022.js','const H22_ART=')]:
 reg=json.loads(source_path.read_text(encoding='utf-8').split(marker)[1].rstrip(';\n'))
 for name,rows in reg['banks'].items():
  if not name.startswith(('blue_','corrupt_')) or not rows or name.endswith('_armor'):continue
  ims=[]
  for a in rows:
   p=reg['sheets'][a['sheet']]['path']
   if p not in cache:cache[p]=Image.open(R/p).convert('RGBA')
   x,y,w,h=a['cell'];ims.append(red(cache[p].crop((x,y,x+w,y+h))))
  # Legacy banks use equal square cells already; no body-size remapping.
  if any(im.size!=ims[0].size for im in ims) or ims[0].width!=ims[0].height:continue
  prefix='legacy_'+('h22_' if 'correction' in source_path.name else 'ha21_')+name;out=emit(prefix,ims,'blue' if name.startswith('blue') else 'corrupt',rows[0]['pivot'],legacy=True)
  for a,b in zip(out,rows):
   a['tip']=b.get('tip',a['tip']);a['glow']=b.get('tip',a['glow']);a['_hf22Legacy']=True
   # Preserve source-space conversion flags and the original physical bank
   # name used by native punch/fist collision. A palette is not a new rig.
   a['bank']=b.get('bank',name)
   for k in ['_h22','_h22Tool']:
    if k in b:a[k]=b[k]
   for k in ['muzzle','handL','handR','gunAngle']:
    if k in b:a[k]=b[k]
   A['legacyRed'][b['key']]=a
manifest={'owner':'_BUILD_SOURCE/build_hammer_furious_1022.py','source':'_ART_SOURCES/hammer_furious_1022','banks':{k:len(v) for k,v in A['banks'].items()},'sources':A['sources'],'phases':A['phases'],'sides':A['sides'],'sheets':[]}
for sid,s in A['sheets'].items():
 p=D/Path(s['path']).name;manifest['sheets'].append(dict(s,id=sid,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(W/'hammer_furious_art_1022.js').write_text('"use strict";\nconst HF22_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8');(W/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(W/'frame-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({'banks':len(A['banks']),'frames':sum(len(v) for v in A['banks'].values()),'sheets':len(A['sheets']),'legacyPalettes':len(A['legacyRed']),'bytes':sum(s['bytes'] for s in manifest['sheets'])}),flush=True)
if '--install' in sys.argv:
 target=R/'assets/game/shared/combat/hammer_furious_1022';target.mkdir(parents=True,exist_ok=True)
 for s in manifest['sheets']:shutil.copy2(D/Path(s['path']).name,target/Path(s['path']).name)
 shutil.copy2(W/'manifest.json',target/'manifest.json')
 for name in ['hammer_furious_art_1022.js','hammer_furious_1022.js']:shutil.copy2(W/name,R/'assets'/name)
 p=R/'index.html';data=p.read_bytes();tag=b'<script src="assets/hammer_furious_art_1022.js?v=furious-1022-1"></script>\n<script src="assets/hammer_furious_1022.js?v=furious-1022-1"></script>\n'
 if b'hammer_furious_1022.js' not in data:p.write_bytes(data.replace(b'</body>',tag+b'</body>'))
 print('Installed reviewed GPT Hammer frames and difficulty choreography.')
