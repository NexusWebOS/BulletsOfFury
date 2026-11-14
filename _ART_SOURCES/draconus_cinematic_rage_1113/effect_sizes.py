from pathlib import Path
from PIL import Image
import json,numpy as np
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');E=W/'exports';M=json.loads((W/'manifest.json').read_text())
def save(name,frames,w,h,pivot):
 d=E/name;d.mkdir(exist_ok=True);sheet=Image.new('RGBA',(w*4,h*((len(frames)+3)//4)))
 for i,f in enumerate(frames):f.save(d/f'{i:02}.png');sheet.paste(f,(i%4*w,i//4*h))
 sheet.save(E/(name+'.webp'),lossless=True,method=1);M[name]=dict(cw=w,ch=h,cols=4,count=len(frames),pivot=pivot,meta=[])
ball=[]
for i in range(16):
 f=Image.new('RGBA',(80,80));f.paste(Image.open(E/'ball'/f'{i:02}.png').resize((70,70),Image.Resampling.NEAREST),(5,5));ball.append(f)
save('ball_back',ball,80,80,[40,40])
im=np.array(Image.open(R/'assets/game/shared/combat/chronos_wave_1025/wave_smooth.png').convert('RGBA'));red=im.copy();red[:,:,0]=im[:,:,2];red[:,:,1]=im[:,:,0];red[:,:,2]=im[:,:,0];im=Image.fromarray(red);wave=[]
for i in range(28):
 f=Image.new('RGBA',(384,768));crop=im.crop((i%8*320,i//8*640,i%8*320+320,i//8*640+640));crop=crop.resize((236,472),Image.Resampling.NEAREST);f.paste(crop,(74,6));wave.append(f)
save('wave',wave,384,768,[192,24])
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'draconus_cinematic_rage_art_1113.js').write_text("'use strict';\nconst DCR13_ART="+json.dumps(M,separators=(',',':'))+';\n')
print('Prepared original wave at the native background release distance and readable back-depth energy ball.')
