from pathlib import Path
import json,base64,re
from PIL import Image
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import content,upload,start
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/intro_repair_1021'
refs=json.loads((D/'upload-refs.json').read_text());c=PixelLab()
v=c.call('get_image',{'job_id':'0759cde1-2c7b-4634-b154-c1091b7f5e08','index':0})
im=next(q for q in v['content'] if q['type']=='image');p=D/'dispatch-run.png';p.write_bytes(base64.b64decode(im['data']))
im=Image.open(p).convert('RGBA').resize((256,144),Image.Resampling.NEAREST);p=D/'dispatch-run-animation.png';im.save(p)
url=re.search(r'https://[^\s"<>]+',content(c.call('get_upload_url',{}))).group(0)
refs['dispatch-run-animation']=upload(c,p,url);(D/'upload-refs.json').write_text(json.dumps(refs,indent=2)+'\n');c.close()
a=dict(first_frame_url=refs['dispatch-run-animation'],
 description='Fixed256x144 pixel cinematic, locked camera and stationary control room. NON-LOOPING action: the two dispatchers SPRINT SCREEN RIGHT through the bright open doorway toward their jets outside. Lizzie leads, long curly auburn hair and yellow jacket, with real pumping arms, alternating bent knees and flying black boots. Decker follows, blond hair, black rectangular glasses, black-and-yellow jacket, running with urgent articulated strides. They translate across the room and EXIT screen right, first Lizzie then Decker; the final frames show the empty room with abandoned chairs and glowing consoles. Preserve exact faces, outfits, anatomy, room perspective and mounting positions. No in-place running, no camera pan/zoom, no extra people, letters or aircraft.',
 frame_count=32,no_background=False,seed=102111,enhance_prompt=False)
start('dispatch-running','animate_image_pixminimax',a)
