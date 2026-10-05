"""Normalize generated floating Stage X art; retain source and original alpha."""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
import json, hashlib, shutil
R=Path(__file__).resolve().parents[1]
A=R/'_ART_SOURCES/campaign_stagex_1004g';O=R/'assets/game/campaign_stagex_1004g'
A.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
src=A/'region_hub_source.png'
if not src.exists():
 shutil.copy2(Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-c0271a87-613f-4e51-b53a-a8bc88d94208.png'),src)
im=Image.open(src).convert('RGBA');assert im.getchannel('A').getextrema()[0]==0
bb=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
im=im.crop(bb);im.thumbnail((724,724),Image.Resampling.NEAREST)
c=Image.new('RGBA',(768,768));c.alpha_composite(im,((768-im.width)//2,(768-im.height)//2));im=c
im.save(O/'region_hub.png');alpha=im.getchannel('A')
gray=ImageOps.grayscale(im).convert('RGBA');gray.putalpha(alpha);gray.save(O/'region_hub_lock.png')
shadow=Image.new('RGBA',im.size,(0,8,22));shadow.putalpha(alpha);shadow.save(O/'region_hub_shadow.png')
glow=Image.new('RGBA',im.size,(146,230,255));glow.putalpha(alpha.filter(ImageFilter.MaxFilter(9)));glow.save(O/'region_hub_glow.png')
m={'generator':'OpenAI built-in imagegen','source':src.name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop':bb,'size':im.size,'normalization':'Nearest contain with original RGBA alpha; grayscale and authored silhouette masks only.','prompt':json.loads((A/'prompt.json').read_text())}
for d in (A,O):(d/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text(encoding='utf-8'))
d['map4e_region_hub']={'role':'campaign_landmark','sheet':None,'note':'Floating Stage X city with generated deep rock underside; campaign_stagex_1004g. Supersedes coastal hub art without deleting it. Builder build_campaign_stagex_1004g.py.'}
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Floating Stage X city normalized; original preserved.')
