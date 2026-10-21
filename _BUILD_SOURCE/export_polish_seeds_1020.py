from pathlib import Path
from PIL import Image
import sys,json,uuid,urllib.request
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');A=R/'_ART_SOURCES/performance_finish_1020';D=A/'refs';D.mkdir(exist_ok=True,parents=True)
seeds={}
turret=Image.open(R/'assets/game/levels/stage_06/boss/siege_carrier_1013/turrets.png').convert('RGBA').crop((0,0,128,160));out=Image.new('RGBA',(160,192));out.alpha_composite(turret,(16,16));seeds['carrier_turret']=out
# Rasterize the existing native 13:36 cannon presentation once, retaining its current silhouette.
raw=Image.open(R/'assets/game/shared/combat/polish_0927b/bomber.png').convert('RGBA').crop((351,615,588,1150));out=Image.new('RGBA',(104,240));out.alpha_composite(raw.resize((78,216),Image.Resampling.NEAREST),(13,12));seeds['bomber_cannon']=out
raw=Image.open(R/'assets/game/shared/player_fx/context_deaths_1019/erase_00.png').convert('RGBA')
import numpy as np
a=np.array(raw);rgb=a[:,:,:3].copy();a[:,:,0]=rgb[:,:,1];a[:,:,1]=np.maximum(rgb[:,:,0],rgb[:,:,1]);a[:,:,2]=rgb[:,:,2];seeds['laser_terminal']=Image.fromarray(a)
seeds['dark_terminal']=raw
seeds['ice_shatter']=Image.open(R/'assets/game/shared/player_fx/context_deaths_1019/ice_08.png').convert('RGBA')
rows={}
for name,im in seeds.items():
 p=D/(name+'.png');im.save(p);boundary='bof-'+uuid.uuid4().hex;body=('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="'+p.name+'"\r\nContent-Type: image/png\r\n\r\n').encode()+p.read_bytes()+('\r\n--'+boundary+'--\r\n').encode()
 req=urllib.request.Request(sys.argv[1],data=body,headers={'Content-Type':'multipart/form-data; boundary='+boundary},method='POST')
 with urllib.request.urlopen(req,timeout=120) as resp:ref=json.load(resp)['ref']
 rows[name]={'ref':ref,'size':im.size,'path':str(p)}
(A/'effect-boss-refs.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows))
