"""Normalize authored HQ/Stage X art; preserve originals and generated alpha."""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
import json, shutil, hashlib
R=Path(__file__).resolve().parents[1]
A=R/'_ART_SOURCES/campaign_landscape_1004f';O=R/'assets/game/campaign_landscape_1004f'
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
A.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
records=[]
for name,file in [('region_hq','exec-61fb7b73-f183-4751-a5c8-23d76a4d0ac3.png'),('flag_x','exec-18ca3c54-10e4-4813-880f-298cc46f130e.png')]:
 src=A/(name+'.png')
 if not src.exists():shutil.copy2(G/file,src)
 im=Image.open(src).convert('RGBA');assert im.getchannel('A').getextrema()[0]==0
 bb=im.getbbox();im=im.crop(bb)
 if name=='region_hq':
  im.thumbnail((724,704),Image.Resampling.NEAREST)
  c=Image.new('RGBA',(768,768));c.alpha_composite(im,((768-im.width)//2,(768-im.height)//2));im=c
 else:im.thumbnail((240,320),Image.Resampling.NEAREST)
 im.save(O/(name+'.png'));alpha=im.getchannel('A')
 gray=ImageOps.grayscale(im).convert('RGBA');gray.putalpha(alpha);gray.save(O/(name+'_lock.png'))
 if name=='region_hq':
  shadow=Image.new('RGBA',im.size,(0,8,22));shadow.putalpha(alpha);shadow.save(O/(name+'_shadow.png'))
  glow=Image.new('RGBA',im.size,(146,230,255));glow.putalpha(alpha.filter(ImageFilter.MaxFilter(9)));glow.save(O/(name+'_glow.png'))
 records.append({'name':name,'source':src.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop':bb,'size':im.size})
 manifest={'generator':'OpenAI built-in imagegen','normalization':'Alpha crop/nearest-neighbor contain; grayscale and silhouette masks only. No invented art.','assets':records,'prompts':json.loads((A/'prompts.json').read_text())}
 for d in [A,O]:(d/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text(encoding='utf-8'))
 d['map4f_']={'role':'campaign_marker','sheet':None,'note':'Generated physical Fury HQ frontage and X-only stage flag. Sources/prompts _ART_SOURCES/campaign_landscape_1004f; builder build_campaign_markers_1004f.py. Alpha/nearest contain only. Supersedes the map4e HQ, retains old source.'}
 p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('HQ and Stage X marker built; original sources retained.')
