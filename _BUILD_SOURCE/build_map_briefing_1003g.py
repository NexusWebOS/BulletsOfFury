"""Package generated blank UI plates unchanged; register measured source rectangles."""
from pathlib import Path
from PIL import Image
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/map_briefing_1003g';D=R/'assets/game/map_briefing_1003g'
D.mkdir(parents=True,exist_ok=True)
manifest={'generator':'built-in image_gen','prompts':'_ART_SOURCES/map_briefing_1003g/generation.json','assets':[]}
rects={'briefing_blank.png':[0,98,2170,484],'lizzie_frame.png':[31,45,1191,1167]}
for name,rect in rects.items():
 src=S/name;dst=D/name;shutil.copyfile(src,dst)
 im=Image.open(src);x,y,w,h=rect
 assert im.mode=='RGBA' and x+w<=im.width and y+h<=im.height
 manifest['assets'].append({'path':dst.relative_to(R).as_posix(),'source':src.relative_to(R).as_posix(),
  'rect':rect,'size':list(im.size),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
manifest['lizzie']={'source':'assets/game/pilots_0922/sheets/lizzie_expressions.png',
 'sha256':hashlib.sha256((R/'assets/game/pilots_0922/sheets/lizzie_expressions.png').read_bytes()).hexdigest(),
 'runtime':'assets/map_briefing_1003g.js','method':'Original portrait interior and mouth pixels drawn into fixed generated bezel; no per-frame bounds, scale, body or border change while speaking. Legacy menu and comm keys route through XART._touch. Original files preserved.'}
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Packaged two unchanged generated plates and recorded original Lizzie source.')
