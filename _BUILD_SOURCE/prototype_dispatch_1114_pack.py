from pathlib import Path
from PIL import Image,ImageOps
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/prototype_dispatch_1114';OUT.mkdir(parents=True,exist_ok=True)
q=json.loads((ROOT/'docs/PROTOTYPE_DISPATCH_ART_1114.json').read_text(encoding='utf-8'));source=Image.open(ROOT/q['source']).convert('RGB')
frame=ImageOps.contain(source,(1280,720),Image.Resampling.NEAREST);im=Image.new('RGB',(1280,720));im.paste(frame,((1280-frame.width)//2,(720-frame.height)//2));im.save(OUT/'satellite.webp',lossless=True)
a={'key':'kd17_satellite','path':'assets/game/shared/cinematics/prototype_dispatch_1114/satellite.webp','w':1280,'h':720,'cols':1,'frames':1,'sha256':hashlib.sha256((OUT/'satellite.webp').read_bytes()).hexdigest()}
(OUT/'prototype_dispatch_art_1114.js').write_text('"use strict";\nconst KD17_ART='+json.dumps({'banks':{'satellite':a}},separators=(',',':'))+';\n',encoding='utf-8')
print('Rebuilt the staged single-panel satellite illustration and manifest.')
