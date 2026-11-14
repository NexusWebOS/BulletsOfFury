from pathlib import Path
from PIL import Image
import numpy as np,json,subprocess
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');E=W/'exports';E.mkdir(exist_ok=True)
s=(W/'assets__stage5_bomber_assault_art_1114.js').read_text();M=json.loads(s[s.index('const S5B14_ART=')+len('const S5B14_ART='):].rstrip(';\r\n'))
sheet=Image.open(R/'assets/game/levels/stage_05/miniboss/assault_1114/retina.webp').convert('RGBA');frames=[]
for base in range(8):
 im=sheet.crop((base%4*80,base//4*80,base%4*80+80,base//4*80+80))
 for heading in range(16):
  for bright in [False,True]:
   a=np.array(im.rotate(-heading*22.5,Image.Resampling.NEAREST));mask=a[:,:,3]>0;a[mask,:3]=np.clip(a[mask,:3].astype(float)*(1.2 if bright else .46),0,255).astype('uint8');a[~mask]=0;frames.append(Image.fromarray(a))
out=Image.new('RGBA',(80*16,80*16));folder=E/'retina_tracking_1114';folder.mkdir(exist_ok=True)
for i,f in enumerate(frames):out.paste(f,(i%16*80,i//16*80));f.save(folder/f'{i:03}.png')
out.save(E/'retina_tracking_1114.webp',lossless=True);assert all(not f.crop((30,30,50,50)).getbbox()for f in frames)
M['banks']['retina_tracking_1114']=dict(cw=80,ch=80,count=256,cols=16,pivot=[40,40]);(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'stage5_bomber_assault_art_1114.js').write_text("'use strict';\nconst S5B14_ART="+json.dumps(M,separators=(',',':'))+';\n')
audit=dict(frames=256,canvas=[80,80],pivot=[40,40],headings=16,trackingPoses=8,brightnessStates=2,emptyCenters=True,alphaValues=sorted(int(v)for v in np.unique(np.array(out)[:,:,3])),runtimeTransforms=False)
(W/'tracking-art-audit.json').write_text(json.dumps(audit,indent=2));out.save(W/'tracking-frames.png')
print('Prepared256 fixed-pivot rotation/flash frames from the approved optic; no runtime transforms.',flush=True)
