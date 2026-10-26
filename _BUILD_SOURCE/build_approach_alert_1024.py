"""Export the generated critical-enemy alert without changing its artwork."""
from pathlib import Path
from PIL import Image
import hashlib,json

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/approach_alert_1024'
D=R/'assets/game/shared/ui/approach_alert_1024'
D.mkdir(parents=True,exist_ok=True)
source=S/'critical-enemy-source.png'
im=Image.open(source).convert('RGBA')
assert im.getchannel('A').getextrema()==(0,255),'Keep generated transparency'
canvas=(768,640)
scale=min(canvas[0]/im.width,canvas[1]/im.height)
size=(round(im.width*scale),round(im.height*scale))
out=Image.new('RGBA',canvas)
offset=((canvas[0]-size[0])//2,(canvas[1]-size[1])//2)
out.alpha_composite(im.resize(size,Image.Resampling.NEAREST),offset)
dest=D/'critical_enemy.webp'
out.save(dest,lossless=True)
assert out.width%2==out.height%2==0
meta={'key':'alert_critical_1024','path':dest.relative_to(R).as_posix(),
      'resolution':list(canvas),'pivot':[384,320],
      'text':'Warning: Critical Enemy Approaching!',
      'source':source.relative_to(R).as_posix(),'source_resolution':list(im.size),
      'proportional_scale':scale,'offset':list(offset),
      'alpha_preserved':True,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
      'owner':'_BUILD_SOURCE/build_approach_alert_1024.py'}
(D/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf8',newline='\n')
p=R/'assets/data/ART_TAXONOMY.json'
tax=json.loads(p.read_text(encoding='utf8'))
tax['alert_critical_1024']={'owner':meta['owner'],
    'manifest':(D/'manifest.json').relative_to(R).as_posix(),
    'purpose':'New generated steel/red/amber alert emblem and integrated exact critical-enemy copy; boss, miniboss and rival approach UI.'}
p.write_text(json.dumps(tax,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(meta,indent=2))
