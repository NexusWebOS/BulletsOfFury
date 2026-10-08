"""Refresh the human inventory without moving files or changing frame coordinates."""
from pathlib import Path
import json, hashlib, sys
from PIL import Image
R=Path(__file__).resolve().parents[1]
G=R/'assets/game';C=R/'assets/data/asset_catalog.json'
c=json.loads(C.read_text(encoding='utf-8'))
if '--registry' in sys.argv:
 reg=json.loads(Path(sys.argv[sys.argv.index('--registry')+1]).read_text(encoding='utf-8'));records=[];roots={}
 for key,path in reg['src'].items():
  root=reg['roots'].get(key,key);actual=reg['src'].get(root,path)
  if not isinstance(actual,str) or not actual.startswith('assets/game/') or not (R/actual).is_file():continue
  row=next((reg[t][key] for t in ['cells','playercells','ecells','ships'] if key in (reg.get(t) or {})),None)
  records.append({'key':key,'root':root,'path':actual,'owner':'','cell':row})
  if root not in roots:roots[root]={'path':actual,'owner':'','keys':[]}
  roots[root]['keys'].append(key)
 c['assets']=records;c['textures']=roots;c['stageQueues']=reg.get('stageQueues',{})
def owner(path):
 p=Path(path).parts
 return '/'.join(p[2:4])
for a in c['assets']:a['owner']=owner(a['path'])
for a in c['textures'].values():a['owner']=owner(a['path'])
registered={a['path'] for a in c['assets']}
text=(R/'assets/manifest.js').read_text(encoding='utf-8');start=text.index('window.BOFA=')+len('window.BOFA=');audio=json.JSONDecoder().raw_decode(text[start:])[0];c['audio']=audio
for table in audio.values():
 if isinstance(table,dict):registered.update(v for v in table.values() if isinstance(v,str) and v.startswith('assets/'))
c['files']=[]
for p in sorted(G.rglob('*')):
 if not p.is_file() or p.name in ['README.md','asset_index.json']:continue
 rel=p.relative_to(R).as_posix();a={'path':rel,'owner':owner(rel),'bytes':p.stat().st_size,'role':'registered runtime asset' if rel in registered else 'source or supporting file'}
 if p.suffix.lower() in ['.png','.jpg','.jpeg','.webp']:
  try:
   with Image.open(p) as im:a['width'],a['height']=im.size
  except Exception:a['role']='legacy supporting file; not a decodable texture'
 c['files'].append(a)
c['loading']={'boot':'UI, fonts, idle portraits only','deployment':'selected pilot portraits, shared player weapons, required stage textures','transition':'release previous stage textures and derived caches; preserve explicitly queued copied-form dependencies','quality':'automatic native resolution on low-memory/low-core devices; reduce supersampling after sustained slow play frames'}
C.write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
for d in [*sorted((G/'pilots').iterdir()),*sorted((G/'levels').iterdir()),G/'shared']:
 if not d.is_dir():continue
 own=d.relative_to(G).as_posix()
 assets=[a for a in c['assets'] if a['owner']==own or a['owner'].startswith(own+'/')]
 files=[a for a in c['files'] if a['owner']==own or a['owner'].startswith(own+'/')]
 deps=['shared/fonts','shared/ui','shared/player_weapons','shared/effects','shared/ships']
 index={'owner':own,'loading':c['loading'],'sharedDependencies':deps,'assets':assets,'files':files,'audio':{kind:{k:v for k,v in entries.items() if isinstance(v,str) and v.startswith('assets/game/'+own+'/')} for kind,entries in audio.items() if isinstance(entries,dict)}}
 if own.startswith('pilots/'):
  index['frameFolders']=['portraits','body_frames','ship_frames','abilities']
  index['furyShip']='Common hull in shared/ships; this pilot applies a runtime palette.'
 if own.startswith('levels/'):
  stage=own.rsplit('_',1)[-1]
  index['deploymentRoots']=c.get('stageQueues',{}).get(str(int(stage)),[]) if stage.isdigit() else []
  index['audioDescription']='Level music and stage-specific sounds are in audio/. Common music and reusable sounds are registered in BOFA and stored once in shared/audio.'
  if own.endswith('08'):index['copiedForms']='Final copied forms additionally use donor-stage roots selected by warmStage.'
 (d/'asset_index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
 link='../../../docs/ASSET_LAYOUT_1007.md' if own=='shared' else '../../../../docs/ASSET_LAYOUT_1007.md'
 (d/'README.md').write_text('# '+own+'\n\n`asset_index.json` lists physical files, logical frame keys, source textures and crops. A frame in an atlas is a crop, not a second PNG. Original pack names identify the owning art workflow.\n\n'+('Portraits, body animation, aircraft and abilities are separated. The Furyship hull is stored once in `../../shared/ships` and receives this pilot’s palette at runtime.\n\n' if own.startswith('pilots/') else 'Common weapons, sounds, fonts and effects are shared. Stage 8 copied forms also load their original donor-stage roots. Empty categories are intentional places for future owned assets.\n\n')+'See [loading and editing guide]('+link+').\n',encoding='utf-8')
print(json.dumps({'logicalFrames':len(c['assets']),'textureRoots':len(c['textures']),'physicalFiles':len(c['files'])}))
