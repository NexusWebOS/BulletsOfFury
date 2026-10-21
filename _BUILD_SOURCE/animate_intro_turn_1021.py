from pathlib import Path
import json,base64,re
from PIL import Image
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import content,upload,start
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/intro_repair_1021';refs=json.loads((D/'upload-refs.json').read_text());c=PixelLab()
v=c.call('get_image',{'job_id':'072ca6a1-aa1a-462f-b050-8c72da79820f','index':0});im=next(q for q in v['content'] if q['type']=='image');p=D/'dispatch-turn.png';p.write_bytes(base64.b64decode(im['data']))
im=Image.open(p).convert('RGBA').resize((256,144),Image.Resampling.NEAREST);p=D/'dispatch-turn-animation.png';im.save(p)
url=re.search(r'https://[^\s"<>]+',content(c.call('get_upload_url',{}))).group(0);refs['dispatch-turn-animation']=upload(c,p,url);(D/'upload-refs.json').write_text(json.dumps(refs,indent=2)+'\n');c.close()
a=dict(first_frame_url=refs['dispatch-seated-animation'],last_frame_url=refs['dispatch-turn-animation'],description='Fixed256x144 cinematic, locked camera, stationary room. Both seated dispatchers turn to face each other urgently. LEFT Decker, blond hair, black rectangular glasses, black-and-yellow jacket, pivots his head and shoulders right toward Lizzie. RIGHT Lizzie, curly auburn hair and yellow jacket, turns left to meet his eyes and points toward the exit with her right arm. They speak urgently, then hold the supplied final pose. Preserve both exact faces, clothing, body positions, two chairs, console mounts and window skyline. No zoom, pan, camera wobble, additional people, letters or subtitles. Real articulated turning frames.',frame_count=24,no_background=False,seed=102110,enhance_prompt=False)
start('dispatch-turning','animate_image_pixminimax',a)
