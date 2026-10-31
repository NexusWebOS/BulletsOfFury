"""Import the approved Contra-style exports without repainting or rescaling pixels."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, shutil, hashlib
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
S=Path('C:/Users/Mike/Documents/Codex/2026-10-15/fo/outputs')
D=R/'expansion/topdown/art/contra34'; D.mkdir(parents=True,exist_ok=True)
P={'build':'overdrive1016-contra34-r1','assets':{},'sequences':{},'sources':[], 'roles':{}}
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def clip(src,tag,role,name,c,scale=1,side=None):
 path=c.get('left_sheet') if side=='west' else c['sheet']; original=src/path
 rel=Path(tag)/path; target=D/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,target)
 im=Image.open(original).convert('RGBA');size=c.get('cell',c.get('frame_size'));anchor=c['origin'];count=c.get('frame_count',c.get('frames'))
 rects=c.get('rects') or [[i%c['columns']*size[0],i//c['columns']*size[1],*size] for i in range(count)]
 bank='_'.join(['c34',tag,role,name]+([side] if side else []));keys=[]
 for i,rect in enumerate(rects):
  x,y,w,h=rect;assert w%2==h%2==0 and x+w<=im.width and y+h<=im.height,(bank,i,rect,im.size)
  cell=im.crop((x,y,x+w,y+h));bounds=cell.getchannel('A').getbbox();assert bounds,(bank,i)
  key=f'{bank}_{i}';meta={'file':'expansion/topdown/art/contra34/'+rel.as_posix(),'rect':rect,'size':size,'anchor':anchor,'bounds':bounds,'drawScale':scale,'role':role,'action':name,'phase':i}
  muzzles=c.get('muzzles_by_frame');muzzle=(muzzles[i][0] if muzzles and i<len(muzzles) and muzzles[i] else (c.get('muzzles') or [[anchor[0],anchor[1]-int((anchor[1]-bounds[1])*.55)]])[0])
  if tag=='side':
   # Barrel tip in the upper body band; exclude feet and backpack below it.
   band=cell.getchannel('A').crop((0,max(bounds[1],anchor[1]-38),w,anchor[1]-15));bb=band.getbbox()
   if bb:muzzle=[bb[0] if side=='west' else bb[2]-1,max(bounds[1],anchor[1]-38)+(bb[1]+bb[3])//2]
  meta['muzzle']=muzzle;meta['emitter']=muzzle
  if tag=='front' and role.startswith(('wall_turret','door_core')):
   meta['anchor']=[(bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2]
  P['assets'][key]=meta;keys.append(key)
 P['sequences'][bank]={'frames':keys,'fps':c.get('fps',12),'loop':c.get('loop',True),'origin':anchor,'scale':scale}
 P['sources'].append({'file':rel.as_posix(),'source':str(original),'sha256':hashlib.sha256(original.read_bytes()).hexdigest()})
 return keys
side=S/'bof-overdrive-enemies'; sm=json.loads((side/'manifest.json').read_text(encoding='utf-8'))
for a in sm['enemies']:
 # One proportional body unit per character across every side-view action.
 scale=(100 if a['id']=='minigunner' else 88)/a['standing_art_height'];P['roles'][a['id']]={'sideScale':scale}
 for name,c in a['clips'].items():
  for facing in ['east','west']:clip(side,'side',a['id'],name,c,scale,facing)
front=S/'bof-overdrive-generated-frames';fm=json.loads((front/'manifest.json').read_text(encoding='utf-8'))
for a in fm['assets']:
 first=a['clips'][0];im=Image.open(front/first['sheet']);r=first['rects'][0];b=im.crop((r[0],r[1],r[0]+r[2],r[1]+r[3])).getbbox()
 height=(b[3]-b[1]) if a['type']=='prop' else first['origin'][1]-b[1];target=240 if a['id']=='fire_prism' else 142 if a['id']=='minigunner' else 125
 if a['type']=='prop':target=44
 scale=target/max(1,height);P['roles'].setdefault(a['id'],{})['frontScale']=scale
 for c in a['clips']:clip(front,'front',a['id'],c['id'],c,scale)
# Preserve the newly authored Helios locomotion; only its volley is replaced by the newer sheet.
pseudo=S/'bof-overdrive-pseudo3d';pm=json.loads((pseudo/'manifest.json').read_text(encoding='utf-8'))
for a in pm['assets']:
 if a['id']=='fire_prism':
  idle=next(c for c in a['clips'] if c['id']=='idle');height=idle['origin'][1]-idle['bounds'][0][1];scale=240/height
  for c in a['clips']:
   if c['id'] in ['idle','walk','run','prism_lightning','ground_slam','overload_death']:clip(pseudo,'motion',a['id'],c['id'],c,scale)
for c in fm['forward_effects']:clip(front,'fx',c['id'],'flight',c,1)
for src in [side,front,pseudo]:
 write(D/'source'/f'{src.name}-manifest.json',(src/'manifest.json').read_text(encoding='utf-8'))
 for name in ['PROMPTS.json','GENERATION-PROVENANCE.json','START-HERE.txt','ANIMATION-NOTES.txt']:
  if(src/name).exists():shutil.copy2(src/name,D/'source'/f'{src.name}-{name}')
write(D/'manifest.json',json.dumps(P,indent=2)+'\n')
write(D/'manifest.js','window.TD_CONTRA34_ART='+json.dumps(P,separators=(',',':'))+';Object.assign(window.TD_ASSAULT_ART.assets,TD_CONTRA34_ART.assets);Object.assign(window.TD_ASSAULT_ART.sequences,TD_CONTRA34_ART.sequences);\n')
# Inspect original pixels at a common display unit, plus adjacent walk poses.
out=R/'_shots/contra34';out.mkdir(parents=True,exist_ok=True)
cv=Image.new('RGB',(960,700),(22,31,42));d=ImageDraw.Draw(cv)
for row,role in enumerate(['machine_gunner','minigunner','sniper','rocket_launcher','shotgunner','double_barrel','flying_alien','roller_alien']):
 d.text((8,row*86+4),role,fill='white')
 for j in range(8):
  k=P['sequences'][f'c34_side_{role}_walk_west']['frames'][j];m=P['assets'][k];im=Image.open(R/m['file']);x,y,w,h=m['rect'];cell=im.crop((x,y,x+w,y+h));b=cell.getbbox();cell=cell.crop(b);s=m['drawScale']*.62;cell=cell.resize((round(cell.width*s),round(cell.height*s)),Image.Resampling.NEAREST);cv.paste(cell,(175+j*95,row*86+77-cell.height),cell)
cv.save(out/'side_walk_review.png')
print(json.dumps({'frames':len(P['assets']),'clips':len(P['sequences']),'sheets':len(P['sources'])}))
