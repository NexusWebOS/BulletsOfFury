from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/readable_needle_1023';W.mkdir(exist_ok=True);O=W/'shipping';O.mkdir(exist_ok=True)
def data(name):
 s=(R/'assets'/name).read_text();return json.loads(s[s.index('=')+1:].strip().rstrip(';'))
effects={**data('biome_fleet_art_1022.js')['effects'],**data('pressure_art_1022.js')['effects']};A={'version':1,'owner':'_BUILD_SOURCE/build_readable_needle_1023.py','unit':.25,'angles':32,'cell':32,'banks':{}}
for theme in ['sky','toxic','water','magma']:
 B=effects[theme+'_needle'];src=Image.open(R/B['path']).convert('RGBA');sheet=Image.new('RGBA',(32*8,32*20));ink=B['ink'];cx=(ink[0]+ink[2])*.5;cy=(ink[1]+ink[3])*.5
 for angle in range(32):
  for f,c in enumerate(B['cells']):
   x,y,w,h=c;frame=src.crop((x,y,x+w,y+h)).resize((16,16),Image.Resampling.NEAREST);plate=Image.new('RGBA',(32,32));plate.alpha_composite(frame,(round(16-cx*.25),round(16-cy*.25)));plate=plate.rotate(-angle*360/32,Image.Resampling.NEAREST,center=(16,16));index=angle*B['frames']+f;sheet.alpha_composite(plate,(index%8*32,index//8*32))
 name=theme+'.webp';sheet.save(O/name,lossless=True,exact=True);A['banks'][theme]={'key':'aq23_readable_'+theme,'path':'assets/game/shared/combat/readable_needle_1023/'+name,'frames':B['frames'],'fps':B['fps'],'stage':{'magma':2,'sky':6,'toxic':7,'water':9}[theme],'source':B['path'],'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()}
runtime='''"use strict";
/* The audited 7x7 sky tracer collapsed to a one-pixel-wide core. Reuse the
   existing PixelLab art at one authored .25 unit. Every direction and frame
   is prebaked; collision, targeting, release time and shot velocity stay native. */
const RN23_ART=__ART__,RN23={base:{draw:ovSonicProjectileDraw,load:stageLoadBegin},draws:0};
for(const b of Object.values(RN23_ART.banks))XART._src[b.key]=b.path;
stageLoadBegin=function(n,keys){return RN23.base.load.call(this,n,[...(keys||[]),...Object.values(RN23_ART.banks).filter(b=>b.stage===n).map(b=>b.key)]);};
ovSonicProjectileDraw=function(b){const a=RN23_ART.banks[b?._bf22Theme];if(!a||b._bf22Form!=='needle'||Math.max(b.w||7,b.h||7)>14)return RN23.base.draw.apply(this,arguments);
 if(!XART.rdy(a.key))return RN23.base.draw.apply(this,arguments);
 const angle=Math.atan2(b.vy||0,b.vx||0)-Math.PI/2,bin=((Math.round(angle/TAU*32)%32)+32)%32,f=Math.floor(Math.max(0,efxClock-(b._bf22Born||0))*a.fps)%a.frames,i=bin*a.frames+f;
 ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(a.key),i%8*32,Math.floor(i/8)*32,32,32,Math.round(b.x-16),Math.round(b.y-16),32,32);RN23.draws++;return true;
};
window.BOF_READABLE_NEEDLES=RN23;
'''.replace('__ART__',json.dumps(A,separators=(',',':')))
(O/'readable_needle_1023.js').write_text(runtime,encoding='utf-8');(O/'manifest.json').write_text(json.dumps(A,indent=2))
if '--install'in sys.argv:
 T=R/'assets/game/shared/combat/readable_needle_1023';T.mkdir(parents=True,exist_ok=True)
 for p in O.glob('*.webp'):shutil.copy2(p,T/p.name)
 shutil.copy2(O/'manifest.json',T/'manifest.json');shutil.copy2(O/'readable_needle_1023.js',R/'assets/readable_needle_1023.js');p=R/'index.html';s=p.read_bytes();nl=b'\r\n'if b'\r\n'in s else b'\n'
 if b'readable_needle_1023.js'not in s:s=s.replace(b'</body>',b'<script src="assets/readable_needle_1023.js?v=rn23-1"></script>'+nl+b'</body>');p.write_bytes(s)
print(json.dumps({'themes':list(A['banks']),'frames':sum(b['frames']*32 for b in A['banks'].values()),'minimumNativeUnit':.25,'collisionChanged':False}))
