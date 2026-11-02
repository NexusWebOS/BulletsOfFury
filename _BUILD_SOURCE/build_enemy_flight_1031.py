"""Stage4-9 source-preserving directional banks and measured sockets.
Retains complete authored motion reels and exports heading cells offline.
No generation, atlases or native health/attack books are changed here.
"""
from pathlib import Path
from io import BytesIO
import json,math,hashlib,sys
from PIL import Image
R=Path(__file__).resolve().parents[1];O=R/'assets/game/shared/combat/enemy_flight_1031';O.mkdir(parents=True,exist_ok=True)
Q=R/'_shots/enemy_flight_1031';Q.mkdir(exist_ok=True)
def data(f,n):return json.JSONDecoder().raw_decode((R/f).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
AF=data('assets/air_refit_art_1021.js','AF21_ART');BF=data('assets/biome_fleet_art_1022.js','BF22_ART');CP=data('assets/pressure_art_1022.js','CP22_ART')
META={'owner':'_BUILD_SOURCE/build_enemy_flight_1031.py','models':{},'aliases':{},'modules':{},'sources':{}}
audit=json.loads((Q/'before/audit.json').read_text())
legacy={}
for q in audit['rows']:
 k=str(q['stage'])+'|'+q['spec']['type'];legacy.setdefault(k,set())
 for d in q.get('stats',{}).get('draws',[]):
  key=d['key']
  if key.startswith(('af21_','bf22_','cp22_','sm10_','s4atk_','s5atk_','s6atk_','s7atk_','s8atk_','s9atk_','n6v','n6x','ns9e_','ns9c_','overhaul_stage','xelite_')):legacy[k].add(key)
PORTS={'s4interceptor':{'port':[42,78],'starboard':[86,78],'centre':[64,108],'exhaustPort':[53,30],'exhaustStarboard':[75,30]},
 's4rocket':{'port':[50,76],'starboard':[78,76],'centre':[64,92],'exhaustPort':[46,47],'exhaustStarboard':[82,47]},
 's4command':{'port':[44,81],'starboard':[84,81],'centre':[64,107],'exhaustPort':[51,31],'exhaustStarboard':[77,31]},
 's4heavyjet':{'port':[43,85],'starboard':[85,85],'centre':[64,107],'exhaustPort':[51,36],'exhaustStarboard':[77,36]},
 's4bomber':{'port':[43,91],'starboard':[85,91],'centre':[64,101],'exhaustPort':[41,37],'exhaustStarboard':[87,37]},
 's5frigate':{'port':[39,88],'starboard':[89,88],'centre':[64,109],'exhaustPort':[46,35],'exhaustStarboard':[82,35]},
 's5interceptor':{'port':[42,84],'starboard':[86,84],'centre':[64,103],'exhaustPort':[47,33],'exhaustStarboard':[81,33]},
 's5skimmer':{'port':[40,96],'starboard':[88,96],'centre':[64,105],'exhaustPort':[49,34],'exhaustStarboard':[79,34]},
 's8interceptor':{'port':[49,74],'starboard':[79,74],'centre':[64,101],'exhaustPort':[47,38],'exhaustStarboard':[81,38]},
 's8razor':{'port':[49,81],'starboard':[79,81],'centre':[64,64],'exhaustPort':[57,37],'exhaustStarboard':[71,37]}}
allmodels={}
for name,M in AF['models'].items():
 if any(s in range(4,10)for s in M['stages'])and name not in ['jace','kaia','rook','nyx','voss','s1jetbomber','s1jetdelta','s1jetdelta_b']:allmodels['af_'+name]=M
for name,M in {**BF['models'],**CP['models']}.items():
 if any(s in range(4,10)for s in M['stages']):allmodels['bf_'+name]=M
if '--modules-only'in sys.argv:META=json.loads((O/'manifest.json').read_text());allmodels={}
for name,M in allmodels.items():
 frames=[];banks={};radius=0
 for kind,B in M['banks'].items():
  im=Image.open(R/B['path']).convert('RGBA');fs=[]
  for x,y,w,h in B['cells']:
   t=im.crop((x,y,x+w,y+h));assert t.size==(128,128),(name,kind,t.size);bbox=t.getbbox()
   if bbox:radius=max(radius,*[math.hypot(x-64,y-64)for x in bbox[::2]for y in bbox[1::2]])
   fs.append(t)
  banks[kind]={'row':len(frames),'frames':len(fs)};frames.extend(fs)
 cell=160 if radius<76 else 192;dirs=16;out=Image.new('RGBA',(cell*dirs,cell*len(frames)));pad=(cell-128)//2
 for f,t in enumerate(frames):
  tile=Image.new('RGBA',(cell,cell));tile.alpha_composite(t,(pad,pad))
  for d in range(dirs):out.alpha_composite(tile.rotate(-d*360/dirs,Image.Resampling.NEAREST,center=(cell/2,cell/2)),(d*cell,f*cell))
 p=O/(name+'.webp');bio=BytesIO();out.save(bio,format='WEBP',lossless=True,method=4);p.write_bytes(bio.getvalue());key='r46_'+name
 sockets=M.get('sockets',{}).copy()
 if not M.get('_bf22'):sockets={k:[64+v[0],64+v[1]]for k,v in sockets.items()}
 sockets.update(PORTS.get(name[3:],{}));sockets.setdefault('centre',[64,104]);sockets['core']=[64,64];sockets.setdefault('port',[44,90]);sockets.setdefault('starboard',[84,90]);sockets.setdefault('exhaustPort',[52,31]);sockets.setdefault('exhaustStarboard',[76,31])
 META['models'][name]={'id':name,'key':key,'path':p.relative_to(R).as_posix(),'cell':cell,'dirs':dirs,'pivot':[cell//2]*2,'sourcePivot':[64,64],'span':M['span'],'nativeRatios':M.get('nativeRatios',{}),'banks':banks,'frames':len(frames),'sockets':sockets,'aliases':M['aliases'],'stages':M['stages'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'legacyKeys':sorted({k for stage in M['stages']for alias in M['aliases']for k in legacy.get(str(stage)+'|'+alias,set())}), 'sources':{k:{'path':v['path'],'cells':v['cells'],'sha256':hashlib.sha256((R/v['path']).read_bytes()).hexdigest()}for k,v in M['banks'].items()}}
 for stage in M['stages']:
  if stage in range(4,10):
   for alias in M['aliases']:META['aliases'][str(stage)+'|'+alias]=name
 print('EXPORTED',name,len(frames),cell,flush=True)
# Keep the three actual silver jet identities across their native palette groups.
for group in ['s','r','b']:
 for i in range(3):META['aliases']['6|l6v_'+group+str(i)]='af_l6v_'+group+str(i)if'af_l6v_'+group+str(i)in META['models']else'af_l6v_s'+str(i)
for alias,model in AF.get('reusedFamilies',{}).items():
 name='af_'+model
 if name in META['models']and '6|'+alias not in META['aliases']:META['aliases']['6|'+alias]=name
escort=META['aliases'].get('8|s8crescent')
if escort:
 META['aliases']['7|s8crescent']=escort
 if 7 not in META['models'][escort]['stages']:META['models'][escort]['stages'].append(7)
# Existing authored hardware is exported independently, preserving module owners.
for name,path in [('jet_rotary','assets/game/shared/combat/encounters_0930/jet_rotary.png'),('jet_missile','assets/game/shared/combat/encounters_0930/jet_missile.png'),('jet_laser','assets/game/shared/combat/encounters_0930/jet_laser.png'),('ground_laser','assets/game/shared/combat/enemy_overhaul_0925/sprites/ground_head_laser.png'),('ground_sonic','assets/game/shared/combat/enemy_overhaul_0925/sprites/ground_head_sonic.png')]:
 im=Image.open(R/path).convert('RGBA');cell=160;k=128/max(im.size);tile=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);t=Image.new('RGBA',(cell,cell));t.alpha_composite(tile,((cell-tile.width)//2,(cell-tile.height)//2));out=Image.new('RGBA',(cell*32,cell))
 for d in range(32):out.alpha_composite(t.rotate(-d*360/32,Image.Resampling.NEAREST),(cell*d,0))
 p=O/(name+'.webp');out.save(p,format='WEBP',lossless=True,method=4);META['modules'][name]={'key':'r46_'+name,'path':p.relative_to(R).as_posix(),'cell':cell,'dirs':32,'frames':1,'source':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(O/'manifest.json').write_text(json.dumps(META,indent=2)+'\n',encoding='utf-8')
(R/'assets/enemy_flight_art_1031.js').write_text('"use strict";\nconst R46_ART='+json.dumps(META,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Registered',len(META['models']),'complete models and',len(META['aliases']),'stage/type aliases')
