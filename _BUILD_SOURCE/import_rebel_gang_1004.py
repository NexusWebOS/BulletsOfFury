"""Register the unchanged, generated RGBA sheet. No atlas repack or pixel edits."""
from pathlib import Path
import hashlib,json
from PIL import Image
R=Path(__file__).resolve().parents[1]
p=R/'assets/game/rebel_gang_1004/decker_effects.png'
im=Image.open(p)
assert im.mode=='RGBA' and im.size==(1536,1024)
assert im.getchannel('A').getextrema()[0]==0
rows=['shield_wave','cloak_swirl','cloak_reveal','chromium_charge']
data={'generator':'builtin imagegen','source':'exec-a3655e9c-ca2b-4436-88aa-5b0b7c8fa1da.png','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sheet':p.relative_to(R).as_posix(),'size':list(im.size),'frames':{name:[[f*256,y*256,256,256] for f in range(6)] for y,name in enumerate(rows)},'alpha':'Generated alpha preserved unchanged','runtime':'assets/rebel_gang_1004.js'}
(p.parent/'manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('24 authored RGBA effect cells registered; source unchanged')
