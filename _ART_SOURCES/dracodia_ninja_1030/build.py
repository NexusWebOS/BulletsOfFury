"""RD77: authored physical ninja motion from the approved colossus anatomy.
All pose/depth/rotation/hit-light transforms are baked here, never at runtime.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,math,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=Path(__file__).parent;O=R/'assets/game/levels/stage_08/boss/ninja_claws_1030';D=R/'_ART_SOURCES/dracodia_ninja_1030';O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
def data(file):
 s=(R/'assets'/file).read_text(encoding='utf-8-sig');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
V=data('stage8_identity_art_1018.js')['clips']['colossus_scythe']['frames'];IDLE=data('stage8_pixellab_art_1018.js')['models']['colossus']['frames'];C=512;P=256;unit=410/320
art={'banks':{},'pages':{},'logicalCell':[512,512],'pivot':[256,256],'source':'Approved24-pose colossus scythe and16-pose colossus. Offline shoulder-joint turns, body bank and depth; source-alpha hit frames.'};source={};poses=[]
def ease(x):return x*x*(3-2*x)
def part(source_pose,id,arm=0,bank=0,depth=1,yaw=1):
 a=source_pose['layers'][id] if'layers'in source_pose else source_pose[id];p=R/a['path'];source[a['path']]=hashlib.sha256(p.read_bytes()).hexdigest();im=Image.open(p).convert('RGBA').resize((410,410),Image.Resampling.NEAREST);out=Image.new('RGBA',(C,C));out.paste(im,(51,51));root=(51+round((112 if id=='left'else 208)*unit),51+round(113*unit))
 if id!='core':out=out.rotate(arm,Image.Resampling.NEAREST,center=root)
 if bank:out=out.rotate(bank,Image.Resampling.NEAREST,center=(P,P))
 if depth!=1 or yaw!=1:
  w=round(C*depth*yaw);h=round(C*depth);small=out.resize((w,h),Image.Resampling.NEAREST);out=Image.new('RGBA',(C,C));out.paste(small,((C-w)//2,(C-h)//2))
 return out
for name,count in [('guard',16),('recede',16),('approach',16),('slashL',24),('slashR',24)]:
 art['banks'][name]=[]
 for f in range(count):
  u=f/(count-1);e=ease(u);depth=1;bank=0;yaw=1;arms={'left':0,'right':0}
  if name=='guard':idx=round(e*6)
  elif name=='recede':idx=6;depth=1-.62*e
  elif name=='approach':idx=round(6*(1-e));depth=.38+.62*e
  else:
   idx=0;side=-1 if name=='slashL'else 1;bank=side*(-10+22*e);yaw=1-.13*math.sin(math.pi*u)
   arms['left']=side*(45-90*e) if side<0 else(-25+35*e)
   arms['right']=side*(45-90*e) if side>0 else(25-35*e)
  layers={id:part(V[idx],id,arms[id] if id!='core'else 0,bank,depth,yaw)for id in ['left','core','right']}
  full=Image.new('RGBA',(C,C))
  for id in ['left','core','right']:full.alpha_composite(layers[id])
  bounds=full.getbbox();assert bounds and min(bounds[:2])>1 and max(bounds[2:])<511,(name,f,bounds)
  art['banks'][name].append({'depth':depth,'parts':{}});poses.append((name,f,layers))
page=Image.new('RGBA',(2048,2048));hit=Image.new('RGBA',(2048,2048));px=py=rh=0;pi=0
def save():
 global page,hit,pi,px,py,rh
 key='rd77_page_'+str(pi);path=O/(key+'.webp');page.save(path,lossless=True,method=6);hp=O/(key+'_hit.webp');hit.save(hp,lossless=True,method=6);art['pages'][key]={'path':path.relative_to(R).as_posix(),'hitKey':key+'_hit','hitPath':hp.relative_to(R).as_posix()};pi+=1;page=Image.new('RGBA',(2048,2048));hit=Image.new('RGBA',(2048,2048));px=py=rh=0
for name,f,layers in poses:
 for id,im in layers.items():
  b=im.getbbox();x0=b[0]//2*2;y0=b[1]//2*2;x1=(b[2]+1)//2*2;y1=(b[3]+1)//2*2;crop=im.crop((x0,y0,x1,y1));w,h=crop.size
  if px+w+2>2048:px=0;py+=rh+2;rh=0
  if py+h+2>2048:save()
  page.paste(crop,(px,py));a=np.array(crop);white=a.copy();white[:,:,:3]=255;hit.paste(Image.fromarray(white),(px,py))
  mask=a[:,:,3]>48;spans=[]
  for row in mask:
   edges=np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1))));spans.append(edges.tolist())
  yy,xx=np.where(mask);target=[float(xx.mean()+x0-P),float(yy.mean()+y0-P)]
  pts=[]
  for index in np.linspace(0,len(xx)-1,5).astype(int):pts.append([int(xx[index]+x0-P),int(yy[index]+y0-P)])
  art['banks'][name][f]['parts'][id]={'key':'rd77_page_'+str(pi),'rect':[px,py,w,h],'offset':[x0-P,y0-P],'w':w,'h':h,'spans':spans,'target':target,'rupture':pts,'logical':[512,512]}
  px+=w+2;rh=max(rh,h)
save()
(R/'assets/dracodia_ninja_art_1030.js').write_text('"use strict";\nconst RD77_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
# Inspectable source strip, then convert to editable Aseprite without changing runtime packing.
strip=Image.new('RGBA',(512*24,512*4))
for row,name in enumerate(['guard','approach','slashL','slashR']):
 for n,f,layers in poses:
  if n!=name:continue
  full=Image.new('RGBA',(C,C))
  for id in ['left','core','right']:full.alpha_composite(layers[id])
  strip.paste(full,(f*512,row*512))
strip.save(D/'ninja-source-strip.png')
audit={'pages':pi,'poses':96,'layers':288,'logicalCell':[512,512],'fixedPivot':[256,256],'evenExportCrops':True,'packing':'Unrotated, no dedup; metadata restores each logical512 canvas/pivot. Tight even source rectangles, native1:1 destinations.','sources':source,'sourceTool':'Pillow deterministic offline author; source strip provided for Aseprite import.'}
(D/'provenance.json').write_text(json.dumps(audit,indent=2));print(json.dumps({k:audit[k]for k in ['pages','poses','layers','evenExportCrops']}))
