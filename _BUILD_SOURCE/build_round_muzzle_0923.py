"""Normalize GPT 2.5 circular muzzle frames with one scale and centered anchors."""
from pathlib import Path
import json, hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/laser_round_muzzle_0923'
source=Image.open(OUT/'source.png').convert('RGBA')
frames=[]
for i in range(8):
    x,y=(i%4)*512,(i//4)*576
    cell=source.crop((x,y,x+512,y+576))
    bounds=cell.getchannel('A').point(lambda a:255 if a>96 else 0).getbbox()
    assert bounds
    cx,cy=(bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2
    # Fixed scale retains the authored swelling and contraction across the reel.
    resized=cell.resize((128,144),Image.Resampling.NEAREST)
    frame=Image.new('RGBA',(128,128))
    frame.alpha_composite(resized,(round(64-cx*.25),round(64-cy*.25)))
    name=f'round_{i}.png';frame.save(OUT/name)
    frames.append({'file':name,'sourceCell':[x,y,512,576],'sourceCenter':[cx,cy],'anchor':[64,64]})
(OUT/'frames.json').write_bytes((json.dumps({'scale':.25,'size':[128,128],'frames':frames},indent=2)+'\n').encode())
preview=Image.new('RGBA',(512,256),(8,12,20,255))
for i in range(8):preview.alpha_composite(Image.open(OUT/f'round_{i}.png'),((i%4)*128,(i//4)*128))
preview.save(ROOT/'_shots/round_muzzle_frames.png')
print('Normalized eight centered transparent frames; source SHA256:',hashlib.sha256((OUT/'source.png').read_bytes()).hexdigest())
