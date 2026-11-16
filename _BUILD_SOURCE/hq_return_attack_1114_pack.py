from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'_shots/hq_return_attack_1114';O.mkdir(parents=True,exist_ok=True);S=O/'install';A=S/'assets/game/shared/cinematics/hq_return_attack_1114';A.mkdir(parents=True,exist_ok=True);G=R/'_ART_SOURCES/hq_return_attack_1114'
inputs={name:name+'-source.png'for name in ['exterior','radar','corridor']}
meta={'generator':'Built-in image_gen, no SpriteCook','banks':{}};sources=S/'_ART_SOURCES/hq_return_attack_1114';sources.mkdir(parents=True,exist_ok=True)
for name,src in inputs.items():
 im=Image.open(G/src).convert('RGB');shutil.copy2(G/src,sources/(name+'-source.png'));shutil.copy2(G/(name+'-prompt.txt'),sources/(name+'-prompt.txt'))
 if name=='corridor':
  sheet=Image.new('RGB',(im.width,im.height+(im.height%2)));sheet.paste(im,(0,0));sheet.paste(im.crop((0,im.height-1,im.width,im.height)),(0,im.height));w,h=sheet.size;frames=1;cols=1
 else:
  w,h,frames,cols=418,236,16,4;cells=[]
  for f in range(16):
   x=f%4*w;y=[0,235,470,706][f//4];c=Image.new('RGB',(w,h));raw=im.crop((x,y,x+w,y+235));c.paste(raw,(0,0));c.paste(raw.crop((0,234,w,235)),(0,235));cells.append(c)
  # Fixed environment plate; only authored moving hardware/screens/lamps vary.
  regions=[(169,85,249,123)]if name=='exterior'else[(157,0,320,153)]
  fixed=[]
  for cell in cells:
   c=cells[0].copy()
   for box in regions:c.paste(cell.crop(box),box[:2])
   if name=='radar':
    # Extract authored alarm emission instead of rectangular lamp/background crops.
    base=cells[0].load();src=cell.load();dst=c.load()
    for yy in range(h):
     for xx in range(w):
      if 157<=xx<320 and yy<153:continue
      rr,gg,bb=src[xx,yy];old=base[xx,yy]
      if rr>max(gg,bb)*1.22 and rr-old[0]>12:
       blend=min(1,(rr-max(gg,bb))/64);dst[xx,yy]=tuple(min(255,round(old[k]+max(0,src[xx,yy][k]-old[k])*blend))for k in range(3))
   fixed.append(c)
  sheet=Image.new('RGB',(w*4,h*4))
  for f,c in enumerate(fixed):sheet.paste(c,((f%4)*w,(f//4)*h))
  print(name,'distinct normalized frames',len({hashlib.sha256(c.tobytes()).hexdigest()for c in fixed}))
  for f in [0,7,15]:fixed[f].save(O/(name+'-fixed-%02d.png'%f))
 dest=A/(name+'.webp');sheet.save(dest,lossless=True);meta['banks'][name]={'key':'hq19_'+name,'path':str(dest.relative_to(S)).replace('\\','/'),'w':w,'h':h,'frames':frames,'cols':cols,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':str((sources/(name+'-source.png')).relative_to(S)).replace('\\','/')}
shutil.copy2(G/'actual-crew-reference.jpg',sources/'actual-crew-reference.jpg');(S/'assets/hq_return_attack_art_1114.js').write_text('"use strict";\nconst HQ19_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
shutil.copy2(R/'assets/hq_return_attack_1114.js',S/'assets/hq_return_attack_1114.js')
s=(R/'index.html').read_text(encoding='utf8');
if 'assets/hq_return_attack_1114.js'not in s:s=s.replace('</body>','<script src="assets/hq_return_attack_art_1114.js?v=1"></script>\n<script src="assets/hq_return_attack_1114.js?v=1"></script>\n</body>')
(S/'index.html').write_text(s,encoding='utf8',newline='\n');(O/'asset-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('Ready',S)
