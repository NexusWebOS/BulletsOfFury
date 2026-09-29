"""Compose fixed authored housings and animated barrels to check socket alignment."""
from pathlib import Path
from PIL import Image,ImageDraw
import json

root=Path(__file__).resolve().parents[2]/'assets/game/weapon_animation_0928'
m=json.loads((root/'manifest.json').read_text())
pilots=m['pilots'];f=m['families'];reel=f['chaingun_barrel_top'];frames=[]
for n in range(len(reel['frames'])):
    out=Image.new('RGBA',(720,810),(15,24,34,255));d=ImageDraw.Draw(out)
    for i,pilot in enumerate(pilots):
        bx=(i%3)*240;by=(i//3)*270
        d.text((bx+24,by+12),pilot.upper(),fill=(225,235,244))
        for j,side in enumerate(['left','right']):
            housing=f[f'chaingun_mount_{pilot}_{side}']
            h=Image.open(root/housing['frames'][0]['file']).convert('RGBA')
            b=Image.open(root/reel['frames'][n]['file']).convert('RGBA')
            x=bx+42+j*92;y=by+150
            socket=housing['barrelSocket'];rear=reel['anchor']
            out.alpha_composite(b,(x+socket[0]-rear[0],y+socket[1]-rear[1]))
            out.alpha_composite(h,(x,y))
    frames.append(out.convert('RGB'))
frames[0].save(root/'review/chaingun_assemblies.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,disposal=2)
frames[8].save(root/'review/chaingun_assemblies.png')
print('Nine pilot pairs: housing stationary, rotating barrel rear coupling aligned to housing socket.')
