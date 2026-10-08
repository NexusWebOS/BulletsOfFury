"""Own Rebel UI/FX registration and the requested authored red/orange swaps."""
from pathlib import Path
import colorsys, hashlib, json, shutil
from PIL import Image
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/rebel_arsenal_1004c';O=R/'assets/game/rebel_arsenal_1004c'
S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
gen=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
sources={'ui':'exec-3818d97e-1768-4348-b3c2-36b6baae12c7.png','fx':'exec-eca3046b-840b-4772-9371-b9b6bcf29b09.png'}
for name,src in sources.items():
 shutil.copy2(gen/src,S/(name+'.png'));shutil.copy2(S/(name+'.png'),O/(name+'.png'))
def inkrect(im,rect):
 x,y,w,h=rect;a=im.getchannel('A').crop((x,y,x+w,y+h));b=a.point(lambda v:255 if v>32 else 0).getbbox()
 assert b,(rect,'empty cell')
 l,t,r,bm=b;return [x+max(0,l-3),y+max(0,t-3),min(w,r+3)-max(0,l-3),min(h,bm+3)-max(0,t-3)]
ui=Image.open(O/'ui.png');fx=Image.open(O/'fx.png')
assert ui.mode==fx.mode=='RGBA' and ui.size==fx.size==(1536,1024)
assert ui.getchannel('A').getextrema()[0]==fx.getchannel('A').getextrema()[0]==0
edges=[0,320,620,925,1230,1536];names=['voss','nyx','rook','kaia','jace']
cells={}
for row,tag in [(0,'box'),(1,'icon')]:
 for i,k in enumerate(names):cells[f'{tag}_{k}']=inkrect(ui,[edges[i],40 if row==0 else 375,edges[i+1]-edges[i],335 if row==0 else 305])
reels={n:[inkrect(fx,[i*256,row*256,256,256]) for i in range(6)] for row,n in enumerate(['dash','nova','launcher','rocket'])}
palette={};weights=(.2126,.7152,.0722)
for src in sorted((S/'authored').glob('*.png')):
 im=Image.open(src).convert('RGBA');data=[];maxerr=0;changed=0
 for red,green,blue,a in im.getdata():
  rgb=[red/255,green/255,blue/255];y=sum(c*w for c,w in zip(rgb,weights))
  if a and max(rgb)-min(rgb)>.065 and y>.015:
   # Real color-ramp remap. Keep neutral metal, outlines and alpha untouched.
   hue=.005+.095*min(1,y/.76);base=list(colorsys.hsv_to_rgb(hue,.98,1));by=sum(c*w for c,w in zip(base,weights))
   if y<=by:out=[c*y/by for c in base]
   else:out=[c+(1-c)*(y-by)/(1-by) for c in base]
   rgb8=tuple(round(c*255) for c in out);changed+=1
  else:rgb8=(red,green,blue)
  yy=sum(c/255*w for c,w in zip(rgb8,weights));maxerr=max(maxerr,abs(yy-y));data.append((*rgb8,a))
 result=Image.new('RGBA',im.size);result.putdata(data)
 assert result.getchannel('A').tobytes()==im.getchannel('A').tobytes()
 assert maxerr<.004
 dest=O/('jace_'+src.name);result.save(dest)
 palette[src.stem]={'key':'ra4_'+src.stem,'path':dest.relative_to(R).as_posix(),'size':list(im.size),'changed':changed,'max_luminance_error':maxerr,'alpha_identical':True}
meta={'generator':'builtin imagegen','prompts':'docs/rebel_arsenal_prompts_1004c.json','sources':sources,'sheets':{n:{'path':(O/(n+'.png')).relative_to(R).as_posix(),'sha256':hashlib.sha256((O/(n+'.png')).read_bytes()).hexdigest(),'size':[1536,1024]} for n in sources},'cells':cells,'reels':reels,'palette':palette,'alpha':'generated sheet alpha preserved byte-identically; palette swaps preserve source alpha'}
(O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
(R/'assets/rebel_arsenal_art_1004c.js').write_text("'use strict';\nconst RA4_ART="+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
p=R/'index.html';b=p.read_bytes();needle=b'<script src="assets/campaign_focus_1004b.js"></script>'
if b'assets/rebel_arsenal_1004c.js' not in b:
 assert b.count(needle)==1
 p.write_bytes(b.replace(needle,needle+b'\r\n<script src="assets/rebel_arsenal_art_1004c.js"></script>\r\n<script src="assets/rebel_arsenal_1004c.js"></script>'))
p=R/'assets/data/ART_TAXONOMY.json';taxonomy=json.loads(p.read_text(encoding='utf-8'))
taxonomy['ra4_']={'role':'rebel_personal_arsenals_ui_and_effects','sheet':None,'note':'October 4: generated five boxes and five hex special icons, six-frame turbo wakes/nova bursts/rocket pods/missiles. Authored Maverick ball and charge palette swaps preserve alpha, luminance and neutral outlines. Whole Rebel hulls retained. Owning workflow _BUILD_SOURCE/build_rebel_arsenal_1004c.py; measured cells, provenance and palette metrics assets/game/levels/stage_06/boss/rebel_arsenal_1004c/manifest.json.'}
p.write_text(json.dumps(taxonomy,indent=2)+'\n',encoding='utf-8')
print('Registered 10 generated UI assets, 24 effect cells, and 12 measured palette swaps.')
