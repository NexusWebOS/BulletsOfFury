"""Package the approved faceless plates without cropping or changing pixels."""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/playthrough_1011/returned'
O=R/'assets/game/shared/cinematics/playthrough_1011';O.mkdir(parents=True,exist_ok=True)
rows=[]
for name in ['emergence','contact']:
 source=S/f'mystery-{name}.png';im=Image.open(source).convert('RGB')
 # Preserve every source pixel; one black border pixel makes odd tool output even.
 source_size=im.size
 if im.width%2 or im.height%2:
  canvas=Image.new('RGB',(im.width+im.width%2,im.height+im.height%2));canvas.paste(im,(0,0));im=canvas
 dest=O/f'mystery-{name}.webp';im.save(dest,lossless=True,method=6)
 rows.append(dict(key='pt11_mystery_'+name,path=dest.relative_to(R).as_posix(),width=im.width,height=im.height,sourceSize=source_size,evenPadding=[im.width-source_size[0],im.height-source_size[1]],source=source.relative_to(R).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(O/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows))
