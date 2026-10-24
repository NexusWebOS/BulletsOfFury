from pathlib import Path
from PIL import Image
import math,json
import os
W=Path(__file__).resolve().parent;candidate=W.parents[1]
R=Path(os.environ.get('BOF_GAME_ROOT',str(candidate if (candidate/'assets/game.js').exists() else Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'))))
D=json.loads((W/'art_meta.json').read_text())['PT11_ART'];O=W/'art';O.mkdir(exist_ok=True)
meta={};angles=[-1.2+i*.05 for i in range(49)]
for cell in [1,2,4,5]:
 a=D['ice_parts'][cell];k=.32 if cell<3 else .23
 im=Image.open(R/a['path']).convert('RGBA');im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST)
 size=(336,288) if cell<3 else (144,144);pivot=(168,80) if cell<3 else (72,72)
 base=Image.new('RGBA',size);base.alpha_composite(im,(round(pivot[0]-a['pivot'][0]*k),round(pivot[1]-a['pivot'][1]*k)))
 sheet=Image.new('RGBA',(size[0]*7,size[1]*7));white=Image.new('RGBA',sheet.size)
 for i,angle in enumerate(angles):
  fr=base.rotate(-math.degrees(angle),resample=Image.Resampling.NEAREST,center=pivot)
  x=(i%7)*size[0];y=(i//7)*size[1];sheet.paste(fr,(x,y));hit=Image.new('RGBA',size,'white');hit.putalpha(fr.getchannel('A'));white.paste(hit,(x,y))
 key=f'er23_frost_turn_{cell}';path=f'assets/game/shared/combat/encounter_revision_1023/{key}.webp'
 sheet.save(O/(key+'.webp'),lossless=True);white.save(O/(key+'_hit.webp'),lossless=True)
 meta[cell]={'key':key,'path':path,'w':size[0],'h':size[1],'pivot':pivot,'angles':angles,'cols':7}
(W/'encounter_revision_art_1023.js').write_text('const ER23_ART='+json.dumps({'frost':meta},separators=(',',':'))+';\n')
print('196 fixed-pivot turret rotation frames plus hit frames')
