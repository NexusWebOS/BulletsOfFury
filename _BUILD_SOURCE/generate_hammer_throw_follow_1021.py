from pathlib import Path
import json,sys,re
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pixellab_mcp import PixelLab
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/hammer_acting_1021';refs=json.loads((D/'upload-refs.json').read_text());c=PixelLab()
pose=json.loads((D/'blue_release_pose-job.json').read_text());receipt='\n'.join(x.get('text','') for x in pose.get('content',[]) if x.get('type')=='text');pose_id=re.search(r'job_id: ([\w-]+)',receipt).group(1)
r=c.call('animate_image',dict(first_frame_url=f'https://api.pixellab.ai/mcp/images/{pose_id}/download?index=0',last_frame_url=refs['blue_empty'],frame_count=8,no_background=True,seed=10215001,action='FRAME FORMAT: 256x256 transparent pixels, same common body scale and fixed chest pivot128,112. Exact same black steel/cyan humanoid with TWO EMPTY HANDS. Begin with the supplied forward-leaning open-hands follow-through. Relax shoulders and draw both EMPTY arms back beside the torso, ending in the supplied unarmed ready stance. Keep the exact same armor, helmet and blue lights. Feet planted throughout; same whole body on transparency, absolutely empty surrounding space. Only body motion, no other objects or energy effects.'))
c.close();(D/'blue_throw_follow-job.json').write_text(json.dumps(r,indent=2)+'\n');print('\n'.join(x.get('text','') for x in r.get('content',[]) if x.get('type')=='text')[:800])
