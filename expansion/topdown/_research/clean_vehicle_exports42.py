"""Atlas extraction repair: discard disconnected pixels belonging to the row above."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
G=Path(__file__).resolve().parents[3];O=G/'expansion/topdown/art/combat42'
src=G/'expansion/topdown/art/combat39/objects/truck_body.png';im=Image.open(src).convert('RGBA');mask=im.getchannel('A').point(lambda v:255 if v>0 else 0)
ImageDraw.floodfill(mask,(600,200),128);a=np.array(im);keep=np.array(mask)==128;a[:,:,3]=np.where(keep,a[:,:,3],0);out=Image.fromarray(a);out.save(O/'truck_body42.png')
j=json.loads((O/'manifest.json').read_text());j['assets']['od39_truck_body']={'file':(O/'truck_body42.png').relative_to(G).as_posix(),'size':list(im.size),'anchor':[0,0],'bounds':list(out.getbbox()),'drawScale':1,'provider':'ImageGen','extraction':'Original body component only; unrelated wheel row fragments removed; no intended body pixels redrawn.'}
(O/'manifest.json').write_text(json.dumps(j,indent=2));(O/'manifest.js').write_text('window.TD_COMBAT42_ART='+json.dumps(j,separators=(',',':'))+';Object.assign(window.TD_NIGHT39_ART.assets,window.TD_COMBAT42_ART.assets);Object.assign(window.TD_NIGHT39_ART.banks,window.TD_COMBAT42_ART.banks);Object.assign(window.TD_ASSAULT_ART.assets,window.TD_COMBAT42_ART.assets);\n')
print('Removed',int((np.array(im)[:,:,3]>0).sum()-(a[:,:,3]>0).sum()),'disconnected atlas-row pixels; truck canvas/root unchanged.')
