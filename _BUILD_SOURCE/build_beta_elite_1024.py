from pathlib import Path
import json,hashlib,urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/beta_elite_1024';D.mkdir(parents=True,exist_ok=True)
job='1b12770a-6007-4ae8-8750-06309aad112b'
def get(i):
 p=D/f'candidate-{i}.png'
 if not p.exists():
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=90) as f:data=f.read()
  assert data.startswith(b'\x89PNG');p.write_bytes(data)
 return p
if __name__=='__main__':
 p=get(0);im=Image.open(p).convert('RGBA');out=R/'assets/game/shared/ui/beta_elite_1024';out.mkdir(parents=True,exist_ok=True)
 frame=im.crop((9,3,119,13));tile=im.crop((30,20,32,24));fill=Image.new('RGBA',(100,4))
 for x in range(0,100,2):fill.paste(tile,(x,0))
 frame.save(out/'frame.png');fill.save(out/'fill.png')
 A={'source_job':job,'resolution':[128,32],'frame':{'key':'bet24_elite_frame','w':110,'h':10,'path':str((out/'frame.png').relative_to(R)).replace(chr(92),'/')},'fill':{'key':'bet24_elite_fill','w':100,'h':4,'path':str((out/'fill.png').relative_to(R)).replace(chr(92),'/')},'aperture':[5,2,100,4],'source_crops':{'frame':[9,3,110,10],'fill_tile':[30,20,2,4]}}
 for k in ['frame','fill']:
  a=A[k];assert a['w']%2==a['h']%2==0;a['sha256']=hashlib.sha256((R/a['path']).read_bytes()).hexdigest()
 (out/'manifest.json').write_text(json.dumps(A,indent=2)+'\n')
 (R/'assets/beta_elite_art_1024.js').write_text('"use strict";\nglobalThis.BET24_ART='+json.dumps(A)+';\nfor(const a of [BET24_ART.frame,BET24_ART.fill]){XART._src[a.key]=a.path;XART.rdy(a.key); }\n',encoding='utf8')
 tax=R/'assets/data/ART_TAXONOMY.json';T=json.loads(tax.read_text());T['beta_elite_1024']={'owner':'_BUILD_SOURCE/build_beta_elite_1024.py','manifest':'assets/game/shared/ui/beta_elite_1024/manifest.json','purpose':'PixelLab ordinary shielded elite health gauge, separate empty frame and fill'};tax.write_text(json.dumps(T,indent=2)+'\n',encoding='utf8')
 print('Exported frame110x10 and fill100x4; even native crops, tiled authored fill pixels')
