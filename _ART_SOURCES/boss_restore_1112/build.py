from pathlib import Path
from PIL import Image,ImageOps
import json,copy,hashlib,numpy as np
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');E=W/'exports';E.mkdir(exist_ok=True)
s=(R/'assets/boss_strike_art_1109b.js').read_text();source=json.JSONDecoder().raw_decode(s[s.index('Object.assign(BA119_ART,')+len('Object.assign(BA119_ART,'):].lstrip())[0]
M={k:copy.deepcopy(source[k])for k in ['blue-sides','blue-right','corrupt-sides']};M['corrupt-right']=copy.deepcopy(source['corrupt-sides'])
maps={'corrupt-sides':[0,0,1,1,2,2,3,4,5,5,5,6,6,7,7,7],'corrupt-right':[8,8,8,9,9,10,10,11,12,12,12,13,13,14,14,15]}
for name,order in maps.items():
 M[name]['folder']='boss_restore_1112';M[name].pop('sha256',None)
 M[name]['meta']=[dict(copy.deepcopy(source['corrupt-sides']['meta'][f]),sourceFrame=f)for f in order]
provenance=[]
for a in M.values():
 for m in a['meta']:m['wholeGenerated']=True
for mat in ['regular','chrome','red','hit','red_hit']:
 p=R/f'assets/game/shared/combat/boss_strike_1109b/corrupt-sides_{mat}.webp';im=Image.open(p).convert('RGBA')
 for name,order in maps.items():
  out=Image.new('RGBA',im.size)
  for f,src in enumerate(order):
   x=src%4*576;y=src//4*576;out.paste(im.crop((x,y,x+576,y+576)),(f%4*576,f//4*576))
  out.save(E/f'{name}_{mat}.webp',lossless=True)
  provenance.append(dict(source=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),output=f'{name}_{mat}.webp',frames=order,operation='Exact original whole cells. The old sheet contains two eight-pose sweeps; split them into left/right timelines with deliberate contact/recovery holds. No repaint, warp or interpolation.'))
for bank in M:
 for mat in ['regular','chrome','red','hit','red_hit']:
  p=E/f'{bank}_{mat}.webp'if bank.startswith('corrupt')else R/f'assets/game/shared/combat/boss_strike_1109b/{bank}_{mat}.webp'
  assert p.exists(),p
(W/'boss_restore_art_1112.js').write_text("'use strict';\n/* Recover the earlier complete sideways-swing actors before atlas registration. */\nObject.assign(BA119_ART,"+json.dumps(M,separators=(',',':'))+');\n')
(W/'manifest.json').write_text(json.dumps(dict(banks=M,provenance=provenance),separators=(',',':')))
print('Recovered Chronus full sweeps and both original eight-pose Draconus directional sweeps, with native-contact holds in all five materials.')
