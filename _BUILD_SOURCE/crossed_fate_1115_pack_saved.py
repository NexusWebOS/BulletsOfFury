from pathlib import Path
from PIL import Image
import json,io,math,hashlib
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/crossed_fate_1115';M=json.loads((S/'manifest.json').read_text(encoding='utf8'))
checks=[]
def check(name,ok):
 checks.append({'name':name,'ok':bool(ok)})
 assert ok,name
def digest(b):return hashlib.sha256(b).hexdigest()
for name,B in M['banks'].items():
 check(name+' even cells and stable source pivot',B['w']%2==B['h']%2==0 and B['sourceCanvas']==[800,800]and B['pivot']==[400-B['sharedCrop'][0],400-B['sharedCrop'][1]])
 for pi,page in enumerate(B['pages']):
  start=pi*16;n=min(16,B['frames']-start);cols=min(4,n);sheet=Image.new('RGBA',(cols*B['w'],math.ceil(n/cols)*B['h']))
  for j in range(n):
   src=Image.open(S/(name+'-%02d.png'%(start+j))).convert('RGBA');check(name+' source cell '+str(start+j),src.size==(800,800)and bool(src.getbbox()))
   sheet.alpha_composite(src.crop(B['sharedCrop']),((j%cols)*B['w'],(j//cols)*B['h']))
   check(name+' registry cell '+str(start+j),B['cells'][start+j]==[page['key'],(j%cols)*B['w'],(j//cols)*B['h']])
  out=io.BytesIO();sheet.save(out,format='WEBP',lossless=True)
  check(page['key']+' byte-for-byte reproduction',digest(out.getvalue())==page['sha256']==digest((R/page['path']).read_bytes()))
im=Image.open(S/'generated-medals.png').convert('RGBA');w,h=im.size
tiles=[im.crop((i*w//2,0,(i+1)*w//2,h))for i in range(2)];bounds=[t.getbbox()for t in tiles]
box=[min(b[0]for b in bounds),min(b[1]for b in bounds),max(b[2]for b in bounds),max(b[3]for b in bounds)]
k=min(228/(box[2]-box[0]),228/(box[3]-box[1]))
for name,t in zip(['crossed_fate','road_not_taken'],tiles):
 t=t.crop(box);t=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);c=Image.new('RGBA',(256,256));c.alpha_composite(t,((256-t.width)//2,(256-t.height)//2))
 out=io.BytesIO();c.save(out,format='PNG');a=M['icons'][name]
 check(name+' exact generated-medal reproduction',digest(out.getvalue())==a['sha256']==digest((R/a['path']).read_bytes()))
registry='"use strict";\nconst FATE15_ART='+json.dumps(M,separators=(',',':'))+';\n'
check('registry reproduced byte-for-byte',registry.encode()==(R/'assets/crossed_fate_art_1115.js').read_bytes())
O=R/'_shots/crossed_fate_1115';O.mkdir(parents=True,exist_ok=True)
(O/'repack-qa.json').write_text(json.dumps({'checks':checks,'medalSource':list(im.size),'medalSharedCrop':box},indent=2),encoding='utf8')
print(str(len(checks))+' saved-source checks passed; shipping files were not rewritten.',flush=True)
