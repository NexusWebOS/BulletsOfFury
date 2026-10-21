from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';D=R/'assets/game/levels/stage_x/stage/coastal_city_1021';D.mkdir(parents=True,exist_ok=True)
im=Image.open(S/'stagex-city-source.png').convert('RGBA');ratio=768/im.width;h=round(im.height*ratio/2)*2;im=im.resize((768,h),Image.Resampling.NEAREST)
a=np.array(im);rgb=a[:,:,:3].astype(float);yy=np.indices(a.shape[:2])[0]
# A colour mask exposes only saturated marine blue in the authored coastal
# section. Shore foam, concrete, props and city geometry stay pixel-identical.
water=(yy>h*.68)&(rgb[:,:,2]>rgb[:,:,0]*1.65)&(rgb[:,:,2]>rgb[:,:,1]*.97)&(rgb[:,:,1]>45)
a[water,3]=0;Image.fromarray(a).save(D/'city-coast.webp',lossless=True,method=6)
# Northward continuation uses mirrored adjacent authored city blocks. Exact
# matching edge rows, no blended double buildings, no camera reversals.
meta=dict(key='cc21_city',path=(D/'city-coast.webp').relative_to(R).as_posix(),w=768,h=h,urban=864,waterPixels=int(water.sum()),source='stagex-city-source.png',scroll=38,layout='coast once, then alternating original/reflected adjacent urban districts in monotonically northward world coordinates')
card=Image.open(Path(r'C:\Users\Mike\.codex\generated_images\01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f\exec-3973c3f5-2d27-4989-bcdc-d0687ab6570d.png')).convert('RGB');card.resize((960,480),Image.Resampling.NEAREST).save(D/'entrance-card.webp',lossless=True,method=6)
meta['card']='assets/game/levels/stage_x/stage/coastal_city_1021/entrance-card.webp'
(D/'manifest.json').write_text(json.dumps(meta,indent=2));(R/'assets/coastal_city_art_1021.js').write_text('"use strict";\nconst CC21_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print(json.dumps(meta))
