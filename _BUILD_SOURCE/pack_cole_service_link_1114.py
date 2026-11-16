from pathlib import Path
from PIL import Image
import json,hashlib,shutil
OUT=Path('D:/BOF-Downloads/2026-11-14/RevG-source/_shots/service_link_1114');ART=OUT/'art';ART.mkdir(exist_ok=True)
source=Path(json.loads((OUT/'portrait-provenance.json').read_text())['source']);im=Image.open(source).convert('RGBA');W,H=im.size
frames=[im.crop((round(i%4*W/4),round(i//4*H/2),round((i%4+1)*W/4),round((i//4+1)*H/2))) for i in range(7)]
assert im.getchannel('A').getextrema()==(0,255)
side=max(max(f.size) for f in frames);base=[]
for f in frames:
 square=Image.new('RGBA',(side,side));square.alpha_composite(f,(0,0));q=square.resize((252,252),Image.Resampling.NEAREST)
 c=Image.new('RGBA',(256,256));c.alpha_composite(q,(2,2));base.append(c)
shutil.copy2(source,ART/'cole-cockpit-likeness-source.png')
zooms=[1,1.03,1.065,1.1,1.135,1.17,1.2];sizes=[round(256*z) for z in zooms];sheet=Image.new('RGBA',(308*7,308*7));baselines=[]
for z,size in enumerate(sizes):
 bb=0
 for f,frame in enumerate(base):
  q=frame.resize((size,size),Image.Resampling.NEAREST);sheet.alpha_composite(q,(f*308,z*308));bb=max(bb,q.getbbox()[3])
 baselines.append(bb)
sheet.save(ART/'cole-talk-zoom.webp',lossless=True)
bindings=[]
def asset(file,key,**extra):
 return dict(key=key,path='assets/game/shared/cinematics/service_link_1114/'+file,sha256=hashlib.sha256((ART/file).read_bytes()).hexdigest(),**extra)
talk=asset('cole-talk-zoom.webp','sl14_cole_talk_zoom',w=308,h=308,cols=7,frames=49,sizes=sizes,baselines=baselines,bleeds=[2]*7,native=[256,256],scales=zooms,family='cockpit-reference-cole')
bindings.extend([['FP5','talk-zoom-cole',talk],['CM3','talk-zoom-cole',talk]])
root=Path('D:/BOF-Downloads/2026-11-14/RevG-source');text=(root/'assets/comic_story_art_1111.js').read_text();original=json.loads(text[text.index('{'):text.rfind('}')+1])
for name,a in original['banks'].items():
 if not name.endswith('-cole') or not name.startswith(('talk-','card-','credit-','icon-')):continue
 n=a['w'];out=Image.new('RGBA',(n,n*7));bl=[]
 for i,frame in enumerate(base):
  q=frame.resize((n,n),Image.Resampling.NEAREST);out.alpha_composite(q,(0,i*n));bl.append(q.getbbox()[3])
 file='cole-'+str(n)+'.webp'
 if not (ART/file).exists():out.save(ART/file,lossless=True)
 q=asset(file,'sl14_cole_'+str(n),w=n,h=n,cols=1,frames=7,pivot=[n//2,n//2],baselineY=max(bl),panelBleed=2)
 bindings.append(['C16',name,q])
rooms=['conference','workshop','hangar','lounge','cockpit-sky','cockpit-space','cockpit-tunnel']
for n in [48,64,84,96]:
 out=Image.new('RGBA',(n,n*7));bl=[]
 for i,frame in enumerate(base):
  q=frame.resize((n,n),Image.Resampling.NEAREST);out.alpha_composite(q,(0,i*n));bl.append(q.getbbox()[3])
 file='cole-mini-'+str(n)+'.webp';out.save(ART/file,lossless=True)
 a=asset(file,'sl14_cole_mini_'+str(n),w=n,h=n,cols=1,frames=7,size=n,pilot='cole',baselines=bl)
 for room in rooms:bindings.append(['FP5','mini-'+room+'-cole-'+str(n),dict(a,room=room)])
 bindings.append(['CX4','face-cole-'+str(n),a])
data={'bindings':bindings,'source':str(source),'reference':'assets/game/shared/cinematics/story_1103/cockpit-cole.webp','sourceSize':[W,H],'normalizedCells':7}
(OUT/'service_link_art_1114.js').write_text('"use strict";\nconst SL14_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
base[0].save(OUT/'new-cole-portrait.png');print(json.dumps({'sourceSize':[W,H],'alpha':im.getchannel('A').getextrema(),'bindings':len(bindings),'sizes':sizes,'baselines':baselines}))
