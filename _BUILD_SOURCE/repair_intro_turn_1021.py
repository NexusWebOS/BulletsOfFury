"""Export PixelLab's guarded subtitle repair; assert all other pixels unchanged."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import urllib.request,json,numpy as np,hashlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/intro_repair_1021';D=S/'raw/turn-clean';D.mkdir(parents=True,exist_ok=True)
image_id='cf1b86f8-848c-490c-8218-c3bfa626f323'
with urllib.request.urlopen('https://api.pixellab.ai/mcp/pixel-tools/'+image_id+'/frames.png',timeout=60) as r:data=r.read()
(S/'turn-repaired-sheet.png').write_bytes(data);sheet=Image.open(BytesIO(data)).convert('RGBA');assert sheet.width%256==0 and sheet.height%144==0;cols=sheet.width//256;assert cols*(sheet.height//144)>=25
rows=[]
for i in range(25):
 im=sheet.crop((i%cols*256,i//cols*144,i%cols*256+256,i//cols*144+144));old=Image.open(S/'raw/turn'/f'{i:02}.png').convert('RGBA');a=np.array(old);b=np.array(im);diff=np.any(a!=b,axis=2);assert not diff[:120].any();assert i in [1,2,3] or not diff.any();im.save(D/f'{i:02}.png');rows.append(dict(frame=i,changed=int(diff.sum()),hash=hashlib.sha256(im.tobytes()).hexdigest()))
q=dict(pixelLabWorkbench=image_id,sourceJob='d47b64e9-2194-445d-a755-2261b8866404',canvas=[256,144],pivot=[128,72],scale=1,rows=rows,operation='Copy stationary source-frame lower letterbox [0,120,255,143] to frames2,3,4 only. No character or room pixels above row120 changed.')
(D/'audit.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(dict(sheet=list(sheet.size),changed=sum(r['changed'] for r in rows),characterPixelsChanged=0)))
