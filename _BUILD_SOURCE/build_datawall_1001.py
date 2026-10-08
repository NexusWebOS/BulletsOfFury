"""Import the eight generated binary animation frames, preserving their RGBA pixels."""
from pathlib import Path
from PIL import Image
import shutil,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/campaign_1001/binary_wall_v7.png'
RUNTIME=ROOT/'assets/game/shared/campaign/campaign_1001/binary_wall_v7.png'
RUNTIME.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(SOURCE,RUNTIME)
im=Image.open(SOURCE)
assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
# The generator returned 1254-square, so cell boundaries are measured as integers.
frames=[]
for row in range(2):
 for col in range(4):
  x0=round(col*im.width/4);x1=round((col+1)*im.width/4)
  y0=round(row*im.height/2);y1=round((row+1)*im.height/2)
  cell=im.crop((x0,y0,x1,y1))
  frames.append({'rect':[x0,y0,x1-x0,y1-y0],'sha256':hashlib.sha256(cell.tobytes()).hexdigest(),'alpha':cell.getchannel('A').getextrema()})
assert len({f['sha256'] for f in frames})==8
data={'path':'assets/game/shared/campaign/campaign_1001/binary_wall_v7.png','width':im.width,'height':im.height,'columns':4,'count':8,'fps':6,'aspect':.5,'frames':frames,'motion':'Eight generated binary-row/scan-packet frames; stationary panel destination. Original alpha retained.'}
RUNTIME.with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/datawall_art_1001.js').write_text('"use strict";\nconst DATAWALL_1001='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print(json.dumps({'sheet':str(RUNTIME),'frames':len(frames),'size':im.size,'alpha':im.getchannel('A').getextrema()}))
