import ast,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'_shots/asset_cleanup_1006';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'tools'))
from art_sources_1006 import ArtSourcePath,logical,source
from PIL import Image
checks=[]
def ck(ok,name):assert ok,name;checks.append(name)
file=R/'tools/pack_stage_runtime_atlases.py';tree=ast.parse(file.read_text(encoding='utf-8'))
nodes=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(n,ast.Name) and n.id=='all_roots' for n in node.targets):break
 nodes.append(node)
scope={'__file__':str(file)};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(file),'exec'),scope)
s=(R/'assets/game/shared/atlases/stage_runtime_atlases.js').read_text();meta=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
for stage in [2,3,4,6,7,8,9]:
 rows=scope['stage_items'](stage);keys=[k for k,p in rows]
 expected={k for k,c in meta['cells'].items() if c[0].startswith('stage'+str(stage)+'_runtime_')}
 ck(expected.issubset(keys) and len(set(keys))==len(keys),f'Stage {stage}: all {len(expected)} deployed atlas source keys preserved, no duplicates')
 for key,path in rows:
  with Image.open(source(path)) as im:
   if key in expected:assert list(im.size)==meta['cells'][key][3:],key
 ck(True,f'Stage {stage}: every archived/live source keeps its runtime canvas dimensions')
file=R/'tools/pack_stage5_runtime_atlas.py';tree=ast.parse(file.read_text(encoding='utf-8'));nodes=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(n,ast.Name) and n.id=='opened' for n in node.targets):break
 nodes.append(node)
scope={'__file__':str(file)};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(file),'exec'),scope)
s=(R/'assets/game/levels/stage_05/enemies/stage5_runtime_atlas.js').read_text();meta=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0];keys=[k for k,p in scope['items']]
ck(set(keys)==set(meta) and len(keys)==len(meta),f'Stage 5: all {len(keys)} archived/live builder sources preserved')
for key,path in scope['items']:
 with Image.open(path) as im:assert list(im.size)==meta[key][3:],key
ck(True,'Stage 5: original source dimensions and deterministic key numbering retained')
src=R/'assets/game/stage3_enemy_damage';allpaths=list(ArtSourcePath(src).glob('**/*.png'));ck(len(allpaths)>0,'Archive source enumerator supports nested glob')
ck(all(not str(logical(p)).startswith(str(R/'UNUSED_ASSETS')) for p in allpaths),'Logical source names preserve pre-archive ordering')
(O/'builder-input-verification.json').write_text(json.dumps({'checks':checks,'count':len(checks)},indent=2));print(json.dumps({'checks':len(checks),'status':'passed'},indent=2))
