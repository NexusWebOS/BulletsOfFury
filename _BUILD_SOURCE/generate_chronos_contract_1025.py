from pathlib import Path
import json,re
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload
D=Path('_ART_SOURCES/chronos_contract_1025');c=PixelLab()
try:
 raw='\n'.join(x.get('text','') for x in c.call('get_upload_url',{}).get('content',[]) if x.get('type')=='text');url=re.search(r'https://[^\s"<>]+',raw).group(0)
 ref=upload(c,D/'kneel-empty-256.png',url)
 args=dict(first_frame_url=ref,frame_count=16,no_background=True,seed=1022501,description='FRAME FORMAT256x256 transparent, fixed common canvas and same robot scale. The whole connected robot recovers from this empty-handed kneel. He lifts his head, straightens his torso, lifts his planted hand from the ground, then slowly stands up into a broad combat stance with BOTH EMPTY hands, right arm ready to catch his hammer from above. Feet stay planted at same baseline. Smooth weight transfer through knees and hips, coherent arms and fingers. No hammer or weapon in any frame, no new objects, no magic, no circles, no glow outside the robot, no rotation, zoom, camera movement or fade. Exact same chromium armored robot identity throughout.',subject_description='a whole faceless black and silver chromium robot with blue eyes and round cyan chest reactor and two empty hands',initial_pose='kneeling with left hand on floor and empty right fist beside knee',view='low top-down',direction='south')
 r=c.call('animate_image_pixminimax',args);(D/'recover-job.json').write_text(json.dumps(r,indent=2));print('Recovery submitted, error:',r.get('isError',False))
finally:c.close()
