from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/cinematic_rework_1114';ART=OUT/'art';ART.mkdir(exist_ok=True)
sources=json.loads((ROOT/'docs/CINEMATIC_REWORK_ART_1114.json').read_text(encoding='utf-8'));banks={}
SCRIPTS=Path('C:/Users/Mdogg/.codex/plugins/cache/openai-curated-remote/game-studio/0.1.2/scripts')
for a in sources['assets']:
 if not a['accepted']:continue
 key=a['key'];im=Image.open(ROOT/a['source']).convert('RGBA');cols=3 if key=='workshop'else 4;count=6 if key=='workshop'else 8
 cells=[]
 for i in range(count):
  q=im.crop((round(i%cols*im.width/cols),round(i//cols*im.height/2),round((i%cols+1)*im.width/cols),round((i//cols+1)*im.height/2)))
  if key!='firewave':q=q.crop((4,4,q.width-4,q.height-4))
  if key=='photon':q=q.transpose(Image.Transpose.ROTATE_270)
  cells.append(q)
 W,H={'workshop':(480,360),'photon':(512,384),'firewave':(540,360)}[key]
 maxw=max(q.width for q in cells);maxh=max(q.height for q in cells);scale=min(W/maxw,H/maxh)
 if key=='firewave':
  strip=Image.new('RGBA',(maxw*count,maxh))
  for i,q in enumerate(cells):strip.alpha_composite(q,(i*maxw,0))
  strip.save(OUT/'firewave-horizontal.png')
  subprocess.run(['python',str(SCRIPTS/'normalize_sprite_strip.py'),'--input',str(OUT/'firewave-horizontal.png'),'--out-dir',str(OUT/'firewave-normalized'),'--frames','8','--frame-size',str(W)],check=True)
  cells=[Image.open(OUT/'firewave-normalized'/('%02d.png'%(i+1))).convert('RGBA').crop((0,W-H,W,W))for i in range(8)]
 else:
  result=[]
  for q in cells:
   shared=Image.new('RGBA',(maxw,maxh));shared.alpha_composite(q,(0,0));shared=shared.resize((round(maxw*scale),round(maxh*scale)),Image.Resampling.NEAREST);f=Image.new('RGBA',(W,H));f.alpha_composite(shared,((W-shared.width)//2,(H-shared.height)//2));result.append(f)
  cells=result
 atlas=Image.new('RGBA',(W*cols,H*2));frameDir=OUT/(key+'-frames');frameDir.mkdir(exist_ok=True)
 for i,q in enumerate(cells):atlas.alpha_composite(q,(i%cols*W,i//cols*H));q.save(frameDir/('%02d.png'%(i+1)))
 dest=ART/(key+'.webp');atlas.save(dest,lossless=True)
 subprocess.run(['python',str(SCRIPTS/'render_sprite_preview_sheet.py'),'--frames-dir',str(frameDir),'--out',str(OUT/(key+'-preview.png')),'--columns',str(cols)],check=True)
 banks[key]={'key':'cw16_'+key,'path':'assets/game/shared/cinematics/cinematic_rework_1114/'+dest.name,'w':W,'h':H,'cols':cols,'frames':count,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'sourceSize':list(im.size),'sharedScale':scale,'offlineQuarterTurn':key=='photon'}
 if key=='firewave':assert atlas.getchannel('A').getextrema()==(0,255)
(OUT/'cinematic_rework_art_1114.js').write_text('"use strict";\nconst CW16_ART='+json.dumps({'banks':banks},separators=(',',':'))+';\n',encoding='utf-8')
(OUT/'packing.json').write_text(json.dumps({'banks':banks},indent=2),encoding='utf-8')
print(json.dumps(banks,indent=2))
