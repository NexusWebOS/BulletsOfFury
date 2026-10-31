from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,re,numpy as np
R=Path(__file__).resolve().parents[2]
def obj(path):
 s=(R/path).read_text(encoding='utf-8');return json.JSONDecoder().raw_decode(s[s.index('{'):])[0]
O=R/'assets/game/levels/stage_06/boss/carrier_revision_1028';O.mkdir(parents=True,exist_ok=True)
SRC=R/'_ART_SOURCES/carrier_revision_1028';SRC.mkdir(parents=True,exist_ok=True)
banks={};aliases={};sources={}
def save(name,im,meta):
 path=O/(name+'.png');im.save(path);banks[name]=dict(key='cr31_'+name,path=path.relative_to(R).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**meta)
def red(im):
 a=np.array(im.convert('RGBA'));c=a[:,:,:3].astype(np.int16);lo=c.min(2);hi=c.max(2)
 # Change chromatic blue/cyan only. Retain neutral outlines, white cores,
 # exact alpha, silhouettes and source rectangles. Preserve HSV value/chroma.
 mask=(a[:,:,3]>0)&(c[:,:,2]>c[:,:,0]+8)&(hi-lo>12)
 out=c.copy();out[:,:,0]=hi;out[:,:,1]=lo;out[:,:,2]=lo+((hi-lo)*.10).astype(np.int16)
 a[:,:,:3]=np.where(mask[:,:,None],out,c).astype(np.uint8);return Image.fromarray(a)
laser=obj('assets/audio_fx_art_1010.js')['ice_laser']
muzzles=obj('assets/laser_muzzles_art_1027.js')['banks']
for i,a in enumerate(laser):
 name=f'laser_{i:02d}';path=R/a['path'];sources[a['path']]=hashlib.sha256(path.read_bytes()).hexdigest();im=Image.open(path);save(name,red(im),dict(cw=im.width,ch=im.height,cols=1,frames=1,pivot=a['pivot']));aliases[a['key']]=name
for name,a in muzzles.items():
 path=R/a['path'];sources[a['path']]=hashlib.sha256(path.read_bytes()).hexdigest();save('muzzle_'+name,red(Image.open(path)),{k:a[k]for k in ['cw','ch','cols','frames','directions','pivot']});aliases[a['key']]='muzzle_'+name
s=(R/'assets/manifest.js').read_text(encoding='utf-8');m=re.search(r'window\.BOFX\s*=',s);fx=json.JSONDecoder().raw_decode(s[m.end():])[0]
smoke=Image.new('RGBA',(8*128,160));smokeframes=[]
for i in range(8):
 key=f'nsd_chim_{i}';source=fx['img'][key];path=R/source;sources[source]=hashlib.sha256(path.read_bytes()).hexdigest();_,x,y,w,h=fx['cells'][key][:5]
 im=Image.open(path).convert('RGBA').crop((x,y,x+w,y+h));frame=Image.new('RGBA',(128,160));frame.alpha_composite(im.resize((96,126),Image.Resampling.NEAREST),(16,18));smoke.alpha_composite(frame,(i*128,0));smokeframes.append(frame)
save('fan_smoke',smoke,dict(cw=128,ch=160,cols=8,frames=8,fps=12,pivot=[64,144],sourceKeys=[f'nsd_chim_{i}'for i in range(8)]))
manifest=dict(banks=banks,aliases=aliases,sources=sources,scope='Stage 6 Warhive carrier laser draw only; passive fan smoke in native carrier local coordinates',smokeConcurrency=2)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(R/'assets/carrier_revision_art_1028.js').write_text('"use strict";\nconst CR31_ART='+json.dumps(dict(banks=banks,aliases=aliases),separators=(',',':'))+';\n',encoding='utf-8')
preview=Image.new('RGBA',(640,280),(12,23,32,255));d=ImageDraw.Draw(preview);d.text((12,8),'Carrier red beam / focused muzzle / attached fan smoke',fill='white')
preview.alpha_composite(Image.open(R/banks['laser_06']['path']).resize((112,224)),(20,36))
mu=Image.open(R/banks['muzzle_large']['path']);preview.alpha_composite(mu.crop((16*64,6*64,17*64,7*64)).resize((128,128),Image.Resampling.NEAREST),(190,80))
for j,i in enumerate([0,3]):preview.alpha_composite(smokeframes[i],(350+j*140,65))
preview.save(SRC/'contact.png');(SRC/'source-hashes.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
for i,im in enumerate(smokeframes):im.save(SRC/f'smoke_{i:02d}.png')
print(json.dumps(dict(banks=len(banks),smokeFrames=8,alphaPreserved=all(np.array(Image.open(R/a['path']))[:,:,-1].tobytes()==np.array(Image.open(R/banks[aliases[a['key']]]['path']))[:,:,-1].tobytes()for a in laser))))
