"""Normalize only the two actual live Hammer motion references for PixelLab."""
from pathlib import Path
import json
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/hammer_motion_1019';D.mkdir(exist_ok=True)
data={}
for name,index,scale,pivot in [('ball',2,.85,(117,127)),('twirl',8,.55,(150,120))]:
    source=R/f'assets/game/levels/stage_08/boss/finale_motion_1006/hammer_motion_{index}.png'
    im=Image.open(source).convert('RGBA')
    frame=im.transform((256,256),Image.Transform.AFFINE,(1/scale,0,pivot[0]-128/scale,0,1/scale,pivot[1]-128/scale),Image.Resampling.NEAREST)
    box=frame.getbbox();assert min(box)>=10 and box[2]<=246 and box[3]<=246,(name,box)
    frame.save(D/f'{name}-reference.png')
    data[name]={'source':source.relative_to(R).as_posix(),'sourceSize':im.size,'sourcePivot':pivot,'proportionalScale':scale,'canvas':[256,256],'pivot':[128,128],'ink':box}
(D/'reference-registration.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
