from pathlib import Path
from PIL import Image
root = Path(__file__).resolve().parents[3]
src = root / 'expansion/topdown/art/assault_1013/source'
im = Image.open(src / 'yuri_directions.png').convert('RGBA')
for i, name in enumerate(['south','southwest','west','northwest','north','northeast','east','southeast']):
    q = im.crop((i%4*384, i//4*512, i%4*384+384, i//4*512+512))
    q.save(src / ('seed_'+name+'.png'))
print('Exported eight identity references; source pixels and alpha preserved.')
