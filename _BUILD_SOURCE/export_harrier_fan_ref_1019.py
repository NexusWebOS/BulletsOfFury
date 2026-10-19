"""Actual current Harrier fan, one proportional export around its axle."""
from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/harrier_fan_1019';D.mkdir(exist_ok=True)
source=R/'assets/game/levels/stage_08/boss/finale_modular_1003c/harrier.png'
im=Image.open(source).convert('RGBA').crop((0,225,350,615))
scale=.38;pivot=(153,174);out=(160,192);anchor=(80,96)
frame=im.transform(out,Image.Transform.AFFINE,(1/scale,0,pivot[0]-anchor[0]/scale,0,1/scale,pivot[1]-anchor[1]/scale),Image.Resampling.NEAREST)
frame.save(D/'fan-reference.png')
(D/'reference.json').write_text(json.dumps(dict(source=source.relative_to(R).as_posix(),crop=[0,225,350,390],sourceAxle=pivot,canvas=out,pivot=anchor,proportionalScale=scale,normalization='Single fixed transform. Generated interior alone will be clipped; native pod/rim remains.'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(canvas=out,pivot=anchor,scale=scale,ink=frame.getbbox())))
