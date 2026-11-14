from pathlib import Path
from PIL import Image
import json,hashlib,shutil
W=Path(__file__).resolve().parent;ARCHIVED=W.parent.name=='_BUILD_SOURCE';R=W.parent.parent if ARCHIVED else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W/'export'if ARCHIVED else W.parents[1]/'outputs/dam-impact';C=W/'candidate';D=C/'art';D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
names=['index.html','assets/helicopter_death_1111.js','assets/game.js','assets/stage1_repair_1021.js','assets/dracodia_helicopter_1030.js','assets/helicopter_effects_1111.js','assets/dracodia_energy_1110.js']
if not(W/'before.json').exists():
 before={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in names}
 (W/'before.json').write_text(json.dumps(before,indent=2))
backup=R/'_BUILD_SOURCE/dam_impact_1111/helicopter_death_1111.js.before'
source=backup if backup.exists() else R/'assets/helicopter_death_1111.js'
s=source.read_text(encoding='utf-8')
old="D.angle=TAU*(.12*t+.28*t*t);D.x=lerp(D.origin.x,targetX,progress)+Math.sin(t*5)*18*Math.sin(Math.PI*u);D.y=lerp(D.origin.y,targetY,Math.pow(u,2.3))+Math.sin(t*4)*10*Math.sin(Math.PI*u);"
new="D.angle=TAU*(.12*t+.28*t*t);const position=h126Position(D,t,u,targetX,targetY);D.x=position.x;D.y=position.y;"
assert s.count(old)==1
s=s.replace(old,new);needle='function h126Tick(b,dt)';assert s.count(needle)==1
s=s.replace(needle,"function h126Position(D,t,u,targetX,targetY){return{x:lerp(D.origin.x,targetX,u*u)+Math.sin(t*5)*18*Math.sin(Math.PI*u),y:lerp(D.origin.y,targetY,Math.pow(u,2.3))+Math.sin(t*4)*10*Math.sin(Math.PI*u)};}\n"+needle)
assert s.count('b.dying>=6.7')==1
s=s.replace('b.dying>=6.7','b.dying>=(D.damSwapAt??6.7)')
(C/'helicopter_death_1111.js').write_text(s,encoding='utf-8',newline='\n')
A={'version':'H127','frames':[],'pages':{},'logical':[480,512],'levels':32,'dam':{'source':[340,286],'target_src_y':128,'changed_bounds':[88,242,596,578]},'timing':{'run_in':3.6,'approach':3.8,'flash_rise':.16,'flash_hold':.18,'flash_fall':1.18},'contract':'Pre-authored white/alpha full-screen frames; ordinary fixed blits, no runtime opacity animation.'}
for page in range(9):
 im=Image.new('RGBA',(1024,1024));key='h127_'+str(page)
 for slot in range(4):
  level=page*4+slot
  if level>32:break
  q=Image.new('RGBA',(480,512),(255,255,255,round(level/32*255)));x=slot%2*480;y=slot//2*512;im.paste(q,(x,y));A['frames'].append({'key':key,'rect':[x,y,480,512],'alpha':round(level/32*255)})
 height=512 if page==8 else 1024;im=im.crop((0,0,1024,height));im.save(D/(key+'.png'),optimize=True);A['pages'][key]={'path':'assets/game/shared/combat/dam_impact_1111/'+key+'.png','size':list(im.size)}
(O/'art.json').write_text(json.dumps(A,indent=2));(C/'dam_impact_art_1111.js').write_text("'use strict';\nconst H127_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print(json.dumps({'frames':len(A['frames']),'pages':len(A['pages']),'h126_change':'Position-selection hook and optional dam-swap time; default trajectory unchanged.'}))
