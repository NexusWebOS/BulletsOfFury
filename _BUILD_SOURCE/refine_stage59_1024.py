from pathlib import Path
import json,re,sys
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/stage59_1024'
c=PixelLab()
try:
 raw='\n'.join(x.get('text','') for x in c.call('get_upload_url',{}).get('content',[]) if x.get('type')=='text');url=re.search(r'https://[^\s"<>]+',raw).group(0)
 if 'charge' in sys.argv:
  ref=upload(c,D/'references/black-3.png',url);name='black_charge_clean';args=dict(first_frame_url=ref,last_frame_url=ref,frame_count=8,no_background=True,seed=10224090,action='FRAME FORMAT256x256 transparent pixels; fixed eye128,128, common scale. Keep the ENTIRE black aircraft perfectly motionless and unchanged. ONLY animate a restrained brightening pulse of cyan and white strictly INSIDE the existing central EYE lens. The tiny lens interior shimmers as it charges and relaxes. All surrounding space and every black armor pixel stay unchanged. NO circles, rings, halos, smoke, sparks, debris, rays, damage, new objects or external effects. No movement or camera zoom.')
 else:
  ref=upload(c,D/'raw/warp_water/00.png',url);name='warp_motion';args=dict(first_frame_url=ref,last_frame_url=ref,frame_count=24,no_background=False,seed=10224091,description='FRAME FORMAT256x256 opaque pixels, common scale, fixed vanishing point128,128. Seamlessly loop rushing FORWARD at incredible warp speed through this exact tunnel of WATER. Liquid wave ribs spiral and expand from the central vanishing point toward every edge, foam crests stream past the camera, bubbles and cyan water streaks accelerate outward in depth. Fluid continuous forwards flow, no camera orbit, no ship, text, machinery, black border, cuts, fading or flashing. Preserve the detailed arcade pixel style and deep navy/cobalt/aqua/white-foam liquid palette. Every frame completely fills all four edges with water.',subject_description='a full-screen liquid ocean vortex tunnel with foam, bubbles and aqua water speed streaks',initial_pose='looking into the central vanishing point of a rushing water vortex',view='high top-down',direction='north')
 p=D/(name+'-job.json')
 if not p.exists() or json.loads(p.read_text()).get('isError'):
  r=c.call('animate_image' if 'charge' in sys.argv else 'animate_image_pixminimax',args);p.write_text(json.dumps(r,indent=2)+'\n');print(name,r.get('isError',False))
finally:c.close()
