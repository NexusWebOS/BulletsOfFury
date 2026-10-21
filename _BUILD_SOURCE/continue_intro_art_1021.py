from pathlib import Path
import sys,json,re,base64,concurrent.futures
from pixellab_mcp import PixelLab
from pixellab_intro_1021 import content,upload,start
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/intro_repair_1021'
c=PixelLab();url=re.search(r'https://[^\s"<>]+',content(c.call('get_upload_url',{}))).group(0);refs=json.loads((D/'upload-refs.json').read_text())
for name,job in [('satellite','2e062e44-ae8b-4ab7-ac2d-c9b2f3bcac3b'),('logo-fx','cc16e63a-a6a7-498e-8047-95cf644ace9c')]:
 q=c.call('get_image',{'job_id':job,'index':0});im=next(v for v in q['content'] if v['type']=='image');path=D/(name+'.png');path.write_bytes(base64.b64decode(im['data']));refs[name]=upload(c,path,url)
(D/'upload-refs.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8');c.close()
corrupt=dict(image_urls=[refs['satellite']],reference_image_url=refs['dp20_dracodia_portrait'],description='FRAME FORMAT: keep the exact256x256 canvas, center128,128, same satellite size, same pose and perspective. Final state of the supplied Fury satellite taken over by Dracodia. Preserve the recognisable three dishes, two rectangular side decks and eagle insignia. Alien BLACK chrome symbiote tendrils tightly entwine the hull and dishes, replacing clean circuitry with branching magenta-purple glowing machine veins. Central belt and engine turn sinister violet, a red alien mechanical heart blooms at the relay center. Tiny sharp biomechanical spines, parasitic cables, corrupted triangular plate growth. Use the Dracodia reference for alien dark-metal armor, red core and purple energy identity ONLY; no head, person, frame, letters or unrelated ship. Keep transparent margins, silhouette intact and stationary.',width=256,height=256,no_background=True,seed=102104)
fx=dict(first_frame_url=refs['logo-fx'],description='FRAME FORMAT256x128, stationary pivot128,64, identical canvas/scale. Animate ONLY the cyan-white electrical branches and orange sparks around the empty logo-shaped center. A quick horizontal flash races across, bright impact flare, arcs curl outwards and flicker, small sparks scatter and dim until the flare dissipates. No letters, logo, objects, camera shake or zoom. Preserve transparent backdrop and unclipped edges. Real distinct pixel-art effect poses.',frame_count=32,no_background=True,seed=102105,enhance_prompt=False)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for f in [pool.submit(start,'satellite-corrupt','edit_image',corrupt),pool.submit(start,'logo-reveal','animate_image_pixminimax',fx)]:f.result()
