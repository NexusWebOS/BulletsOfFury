"""Register measured native imagegen cells; never repaint generated pixels."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
S=R/'_ART_SOURCES/dracodia_1005';O=R/'assets/game/dracodia_1005'
S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
CONFIG={
 'parts':{'file':'exec-2672e9b7-02fa-436c-8a91-747c424b546d.png','xs':[0,420,840,1261],'ys':[0,420,718,965,1247],
 'prompt':'Preserve crowned black/oily/crimson Dracodia identity. Headless torso, two complete arms, nine head-only views: neutral, left, right, up, down, shocked, pre-explosion, split-maw scream and speaking. True alpha; measured native cells; keep complete crown.'}
}
art={};meta={'generator':'built-in image_gen','pixelPolicy':'Native source pixels and alpha unchanged; measured component crops only.','sources':{}}
for name,c in CONFIG.items():
 src=S/(name+'.png')
 if not src.exists():shutil.copyfile(G/c['file'],src)
 im=Image.open(src);assert im.mode=='RGBA';xs=c.get('xs') or [round(im.width*i/c['cols']) for i in range(c['cols']+1)];ys=c.get('ys') or [round(im.height*i/c['rows']) for i in range(c['rows']+1)]
 cells=[]
 for y in range(len(ys)-1):
  for x in range(len(xs)-1):
   n=len(cells);box=[xs[x],ys[y],xs[x+1],ys[y+1]];cell=im.crop(box)
   if name=='parts':
    bb=cell.getbbox();assert bb;box=[box[0]+bb[0],box[1]+bb[1],box[0]+bb[2],box[1]+bb[3]];cell=cell.crop(bb)
   dst=O/(name+'_'+str(n)+'.png');cell.save(dst)
   cells.append({'key':'dr5_'+name+'_'+str(n),'path':dst.relative_to(R).as_posix(),'w':cell.width,'h':cell.height,'sourceBox':box})
 art[name]=cells;meta['sources'][name]={'path':src.relative_to(R).as_posix(),'size':im.size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'prompt':c['prompt']}
(R/'assets/dracodia_art_1005.js').write_text('"use strict";\nconst DR5_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
print('Registered',sum(map(len,art.values())),'native Dracodia cells.')
