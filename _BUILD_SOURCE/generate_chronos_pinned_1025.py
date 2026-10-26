from pathlib import Path
import json,re
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import upload
D=Path('_ART_SOURCES/chronos_contract_1025');c=PixelLab()
try:
 raw='\n'.join(x.get('text','') for x in c.call('get_upload_url',{}).get('content',[]) if x.get('type')=='text');url=re.search(r'https://[^\s"<>]+',raw).group(0)
 first=upload(c,D/'kneel-clean-256.png',url);last=upload(c,D/'stand-clean-256.png',url)
 args=dict(first_frame_url=first,last_frame_url=last,frame_count=8,no_background=True,seed=1022502,action='Interpolate ONLY the whole empty-handed robot from kneeling to upright standing. FRAME FORMAT256x256 transparent, fixed feet baseline215, common scale. Lift the head and chest, extend the knees and hips and lift the planted hand. The right hand opens gradually as he stands. Smooth weight transfer, all armor remains connected to the torso. Both hands stay EMPTY in every frame, no weapon, no floating object, no shaft, no energy. DO NOT introduce any hammer or other object. Match provided final standing pose exactly. No camera movement, no resizing, no palette change, no fading.')
 r=c.call('animate_image',args);(D/'recover-pinned-job.json').write_text(json.dumps(r,indent=2));print('Pinned recovery submitted, error:',r.get('isError',False))
finally:c.close()
