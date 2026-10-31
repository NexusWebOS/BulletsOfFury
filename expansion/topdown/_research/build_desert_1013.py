"""Export the authored desert plate at uniform proportional world scale."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/desert_1013'
src=OUT/'source/desert_raw.png'
im=Image.open(src).convert('RGB')
assert im.width%2==0 and im.height%2==0
assert abs(im.width/im.height-800/1200)<.0001
im.resize((800,1200),Image.Resampling.NEAREST).save(OUT/'desert_ground.png')
(OUT/'export.json').write_text(json.dumps({'source':'source/desert_raw.png','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_size':list(im.size),'size':[800,1200],'scale':800/im.width,'uniform_scale':True,'method':'nearest-neighbor proportional downsample','world_bounds':[0,0,800,1200],'blocked_rock_edges':[[0,0,100,1200],[700,0,800,1200]]},indent=2))
print('DESERT plate exported: 800x1200; source retained')
