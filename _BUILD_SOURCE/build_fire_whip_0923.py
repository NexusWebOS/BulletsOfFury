"""Normalize generated flame frames without painting or synthesizing sprite artwork."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/game/player_weapons/fire_whip_0923'
im=Image.open(OUT/'source.png').convert('RGBA');frames=[]
for i in range(8):
 x0,x1=round(i%4*im.width/4),round((i%4+1)*im.width/4)
 y0,y1=round(i//4*im.height/2),round((i//4+1)*im.height/2)
 cell=im.crop((x0,y0,x1,y1))
 # Remove near-invisible background residue before measuring the anchors.
 cell.putalpha(cell.getchannel('A').point(lambda a:0 if a<=8 else a))
 bb=cell.getchannel('A').getbbox();assert bb
 # Lock the emitting root to x=32. Trim only empty rows; retain the authored needle tip.
 root=cell.getchannel('A').crop((0,max(bb[1],bb[3]-12),cell.width,bb[3])).getbbox()
 cx=(root[0]+root[2])/2
 cell=cell.crop((round(cx)-32,bb[1],round(cx)+32,bb[3]))
 cell=cell.resize((64,256),Image.Resampling.NEAREST)
 name=f'flame_{i}.png';cell.save(OUT/name)
 frames.append({'file':name,'sha12':hashlib.sha256((OUT/name).read_bytes()).hexdigest()[:12],'root':[32,256],'tip':'authored tapered alpha silhouette'})
manifest={'asset_id':'88bf8613-369c-4dc6-90d4-bddf1ad46fcf','model':'gpt-image-2.5-sunburst','credits':14,
 'source':{'file':'source.png','sha12':hashlib.sha256((OUT/'source.png').read_bytes()).hexdigest()[:12]},
 'layout':[4,2],'runtime_size':[64,256],'fps':16,'frames':frames}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Normalized eight anchored flame frames.')
