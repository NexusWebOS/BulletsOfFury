"""Rebuild the four-frame alien-data barrier from its preserved generated master."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/campaign_0930/east_coast_datawall_v5.png'
O=R/'assets/game/campaign_0930'
im=Image.open(S).convert('RGBA')
assert im.size==(724,2172),im.size
sheet=Image.new('RGBA',(1024,512),(0,0,0,0))
edge=im.crop((3*181,600,4*181-1,1500)).resize((256,512),Image.Resampling.NEAREST).getchannel('A')
cells=[]
for i in range(4):
 box=(i*181,600,(i+1)*181-1,1500)
 frame=im.crop(box).resize((256,512),Image.Resampling.NEAREST)
 frame.putalpha(ImageChops.darker(frame.getchannel('A'),edge))
 assert frame.getchannel('A').getextrema()[0]==0
 sheet.paste(frame,(i*256,0))
 cells.append({'index':i,'source_box':box,'rect':[i*256,0,256,512],'sha256':hashlib.sha256(frame.tobytes()).hexdigest()})
assert len({c['sha256'] for c in cells})==4
sheet.save(O/'east_coast_datawall_v5.png',optimize=True)
(O/'east_coast_datawall_v5.json').write_text(json.dumps({'image':'east_coast_datawall_v5.png','columns':4,'rows':1,'fps':4,'frame_width':256,'frame_height':512,'count':4,'motion':'fixed-position authored alien binary-data flicker','transparent_edge':True,'edge_mask':'authored fourth-frame alpha, shared by all poses','frames':cells},indent=2)+'\n',encoding='utf-8')
print('Built alien data wall.')
