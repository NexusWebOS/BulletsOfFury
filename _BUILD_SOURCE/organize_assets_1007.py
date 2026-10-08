"""Owning, reversible BOF asset-layout workflow. --plan / --apply / --verify.

Stable runtime keys and authored RGBA survive all file moves and cell repacks.
Historical QA documents and the earlier unused archive are never rewritten.
"""
from pathlib import Path
from collections import defaultdict,Counter
import argparse,json,re,hashlib,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];G=R/'assets/game'
O=R/'_shots/asset_layout_1007';ARCH=R/'UNUSED_ASSETS/asset_layout_2026-10-07'
PILOTS=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
OLD_SHEETS=['pilots_0','pilots_1','terrain_masters_0','terrain_masters_1','terrain_masters_2','terrain_props_0','terrain_props_1']
parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['--plan','--apply','--verify'],nargs='?',default='--plan')
# Accept the natural flag spelling without argparse treating it as an unknown option.
mode=next((x for x in __import__('sys').argv[1:] if x in ['--plan','--apply','--verify','--catalog']),'--plan')
if mode=='--catalog':
 import runpy
 runpy.run_path(str(R/'_BUILD_SOURCE/refresh_asset_catalog_1007.py'),run_name='__main__');raise SystemExit()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(p):
 p=p.resolve();assert p.is_relative_to(R.resolve()),p;return p
def pilot_of(s):
 m=re.search(r'(?:^|[/_\-])(axel|cole|decker|falva|freezer|juggernaut|lizzie|maverick|yuri)(?:[/_\-.]|$)',s.lower())
 return m.group(1) if m else None
def stage_of(s):
 s=s.lower();m=re.search(r'(?:stage|level|(?:^|[/_])(?:s|l)|(?:^|[/_])(?:nst|nl|bg|norb|nsky|lvl))[_-]?0?([1-9])(?:[^0-9]|$)',s)
 if m:return int(m.group(1))
 m=re.search(r'(?:boss|mini|en|eproj)_s([1-9])',s)
 if m:return int(m.group(1))
 return None
PACKS={
 'alien_arena_1005':(8,'stage'),'axel_mega_shield_0923':('axel','abilities'),
 'chaos_harrier':(5,'miniboss'),'chaos_harrier_rift':(5,'effects'),'chaosharrier':(5,'miniboss'),
 'codewall_1003d':(8,'effects'),'cole_fusion_1004l':('cole','abilities'),
 'dracodia_1005':(8,'boss'),'final_boss_0924':(8,'boss'),'final_boss_0925_patterns':(8,'boss'),
 'final_boss_concepts':(8,'boss'),'finale_1003b':(8,'boss'),'finale_modular_1003c':(8,'boss'),
 'finale_motion_1006':(8,'boss'),'hama_art_0928':(5,'boss'),'hammer_time_0927':(5,'boss'),
 'hammer_knight_1005':(8,'boss'),'herald_1003f':(8,'miniboss'),'herald_of_death':(8,'miniboss'),
 'l6_fleet':(6,'enemies'),'rebel_air_1007':(6,'boss'),'rebel_arsenal_1004c':(6,'boss'),
 'rebel_gang_1004':(6,'boss'),'rival_fight_0924':(6,'boss'),'roaming_rebels_0922':(6,'boss'),
 's4_core_revival_1006':(4,'effects'),'s6_carrier_attacks':(6,'boss'),
 's9_asteroids_1001':(9,'enemies'),'s9_attacks':(9,'projectiles'),
 'sky_repair_1004i':(6,'boss'),'stealth_1002':(6,'enemies'),
 'yuri_lightning_orb_0916':('yuri','abilities'),'yuri_v2':('yuri','portraits'),
 'stagex_1001':('x','stage'),'stagex_coast_1004j':('x','stage'),
}
def group_for(rel):
 q=Path(rel).relative_to('assets/game').as_posix();parts=q.split('/');top=parts[0];p=pilot_of(q)
 if p and (top in ['pilots_0922','pilot_bodies','pilot_avatars','pilot_portraits','cinematic_characters','ships_derived','ships_v2'] or q.startswith('atlas/ships/')):
  if top.startswith('ship') or q.startswith('atlas/ships/'):cat='ship_frames'
  elif top=='pilot_bodies' or top=='cinematic_characters' or '/bodies/' in q:cat='body_frames'
  else:cat='portraits'
  return 'pilots/'+p+'/'+cat
 if top in PACKS:
  owner,cat=PACKS[top];return ('pilots/'+owner+'/'+cat if owner in PILOTS else 'levels/stage_'+(f'{owner:02}' if isinstance(owner,int) else owner)+'/'+cat)
 if q.startswith('bosses/'):
  b=parts[1];owner={'furnace':2,'frost':3,'stage3_thermo':3,'razorback':1,'razorback_furious':1,'skycarrier':6,'tempest':6,'rebel_squad_0920':6}.get(b)
  if owner:return f'levels/stage_{owner:02}/'+('miniboss' if b in ['razorback','razorback_furious','tempest'] else 'boss')
 s=stage_of(q)
 if s:
  cat='stage'
  if 'enemy' in q or '/enemies/' in q or 'en_s' in q or 'stage_runtime/' in q or 'runtime_atlas' in q or 'fleet' in q:cat='enemies'
  if 'projectile' in q or 'eproj_' in q or 'ordnance' in q:cat='projectiles'
  if 'boss' in q or '/boss_s' in q or 'hammer' in q or 'archmage' in q or 'raptor' in q or 'warfare' in q:cat='boss'
  if '/mini_s' in q or 'fracture' in q or 'herald' in q:cat='miniboss'
  if 'sewer_' in q or 'core_revival' in q or 'portal' in q or 'warp_lattice' in q:cat='effects'
  if 'cinematic' in q:cat='cinematics'
  if 'font' in q:cat='fonts'
  if Path(q).suffix.lower() in ['.mp3','.wav','.ogg']:cat='audio'
  return f'levels/stage_{s:02}/'+cat
 if top=='hardcorps_1007':return 'levels/stage_08/effects'
 if top.startswith('final') or top.startswith('overnight'):return 'levels/stage_08/boss'
 if top in ['fonts','BlackOpsOne.ttf']:return 'shared/fonts'
 if top in ['music','sounds','sfx_0927','hama_vocals_1001']:return 'shared/audio'
 if top.startswith('campaign') or top.startswith('map_') or top=='gameplay_1004':return 'shared/campaign'
 if top=='ui' or top in ['affiliations','dialogue_0914','comm_portraits_0914'] or q.startswith('atlas/ui_') or top in ['newbootimage.jpg','logo.png','bonus_stage_card.png']:return 'shared/ui'
 if top in ['gravity_mode','furyship_0914','fury_fleet_0922','cinematic_ships']:return 'shared/ships'
 if top.startswith('cinema') or top.startswith('generated_cinematic') or top=='cockpit_pov_0923':return 'shared/cinematics'
 if 'weapon' in top or 'projectile' in top or top in ['flame_v2','laser_mist','laser_round_muzzle_0923','fusion_0930','fusion_1002','special_icons']:return 'shared/player_weapons'
 if top.startswith('fx') or top in ['director_0927','enemy_shields','shared_targeting_0916','warp_fx','warp_gate96','boss_projectile_overhaul','contra_fx_1006']:return 'shared/effects'
 if top=='atlas':return 'shared/atlases'
 return 'shared/combat'
def destination(rel):
 group=group_for(rel);q=Path(rel).relative_to('assets/game').as_posix()
 if q.startswith('atlas/ships/'):tail=Path(q).name
 elif q.startswith('atlas/') and '/' not in q[6:]:tail=Path(q).name
 elif len(q.split('/'))==1:tail=q
 else:tail=q
 return 'assets/game/'+group+'/'+tail
def cell_group(k,old):
 p=pilot_of(k)
 if p:
  cat='body_frames' if k.startswith('pose_') else 'portraits' if k.startswith(('card_','pcard_','aintro_','face_','port_','pemb_')) else 'abilities'
  return 'pilots/'+p+'/'+cat
 s=stage_of(k)
 if s:return f'levels/stage_{s:02}/stage'
 if k.startswith(('bg5_','norb5_')):return 'levels/stage_05/stage'
 return 'shared/'+('ui' if old.startswith('pilots') else 'effects')
def manifest_object():
 p=R/'assets/manifest.js';s=p.read_text(encoding='utf-8');start=s.index('window.BOFX=')+len('window.BOFX=');data,end=json.JSONDecoder().raw_decode(s[start:]);return p,s,start,end,data
def build_plan():
 files=[p for p in G.rglob('*') if p.is_file() and p.relative_to(G).parts[0] not in ['pilots','levels','shared']]
 mapping={p.relative_to(R).as_posix():destination(p.relative_to(R).as_posix()) for p in files if p.relative_to(G).as_posix() not in ['atlas/'+s+'.png' for s in OLD_SHEETS]}
 assert len(mapping.values())==len(set(v.casefold() for v in mapping.values())),'destination collision'
 records=[{'old':k,'new':v,'bytes':(R/k).stat().st_size,'sha256':sha(R/k)} for k,v in sorted(mapping.items())]
 plan={'version':1,'moves':records,'repackedSheets':OLD_SHEETS,'assetBytes':sum(x['bytes'] for x in records)}
 _,_,_,_,data=manifest_object()
 for k,t in data['cells'].items():
  if t[0] in OLD_SHEETS:assert t[3]+8<=4096 and t[4]+8<=4096,(k,t)
 O.mkdir(parents=True,exist_ok=True);(O/'plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8');return plan,mapping
def repack(data):
 groups=defaultdict(list);opened={};newcells={};newroots={};proof=[];aliases={}
 originalGroups=defaultdict(list)
 for key,row in data['cells'].items():
  if row[0] in OLD_SHEETS:originalGroups[tuple(row)].append(key)
 for keys in originalGroups.values():
  canonical=sorted(keys,key=lambda k:(not k.startswith('ncon_'),k))[0]
  for key in keys:
   if key!=canonical:aliases[key]=canonical
 for old in OLD_SHEETS:
  src=R/data['img']['nca_'+old];im=Image.open(src).convert('RGBA');opened[old]=im
  for k,t in data['cells'].items():
   if t[0]!=old or k in aliases:continue
   cell=im.crop((t[1],t[2],t[1]+t[3],t[2]+t[4]));groups[cell_group(k,old)].append((k,cell))
 for group,items in sorted(groups.items()):
  items.sort(key=lambda q:(-q[1].height,-q[1].width,q[0]));sheets=[];placed=[];x=y=4;shelf=0;bottom=0;usedw=0
  def flush():
   nonlocal placed,x,y,shelf,bottom,usedw
   if not placed:return
   sid='layout_'+group.replace('/','_')+'_'+str(len(sheets));rel='assets/game/'+group+'/frames_'+str(len(sheets))+'.png'
   atlas=Image.new('RGBA',(usedw+4,bottom+4));rows={}
   for k,cell,px,py in placed:atlas.paste(cell,(px,py));rows[k]=[sid,px,py,cell.width,cell.height]
   out=inside(R/rel);out.parent.mkdir(parents=True,exist_ok=True);atlas.save(out,compress_level=6)
   verified=Image.open(out).convert('RGBA')
   for k,cell,px,py in placed:
    actual=verified.crop((px,py,px+cell.width,py+cell.height));assert actual.tobytes()==cell.tobytes(),k
    proof.append({'key':k,'rgbaSHA256':hashlib.sha256(cell.tobytes()).hexdigest(),'row':rows[k],'path':rel})
   newcells.update(rows);newroots['nca_'+sid]=rel;sheets.append(rel);placed=[];x=y=4;shelf=bottom=usedw=0
  for k,cell in items:
   assert cell.width+8<=4096 and cell.height+8<=4096,(k,cell.size)
   if x+cell.width+4>4096:x=4;y+=shelf+4;shelf=0
   if y+cell.height+4>4096:flush()
   placed.append((k,cell,x,y));usedw=max(usedw,x+cell.width);bottom=max(bottom,y+cell.height);x+=cell.width+4;shelf=max(shelf,cell.height)
  flush()
 for im in opened.values():im.close()
 proofByKey={a['key']:a for a in proof}
 for key,canonical in aliases.items():
  newcells[key]=newcells[canonical][:];proof.append({**proofByKey[canonical],'key':key})
 data['cells'].update(newcells);data['img'].update(newroots)
 for k,row in newcells.items():data['img'][k]=newroots['nca_'+row[0]]
 retired=[]
 for old in OLD_SHEETS:
  key='nca_'+old;rel=data['img'].pop(key);src=inside(R/rel);dst=inside(ARCH/rel);dst.parent.mkdir(parents=True,exist_ok=True)
  retired.append({'old':rel,'archive':dst.relative_to(R).as_posix(),'sha256':sha(src)});src.rename(dst)
 return proof,retired
def rewrite_sources(mapping):
 # Exact paths first. Dynamic legacy filenames use bofAssetPath at the image boundary.
 # Do not rewrite an original path inside UNUSED_ASSETS; it identifies archived donors.
 pattern=re.compile('|'.join(re.escape(x) for x in sorted(mapping,key=len,reverse=True)))
 changes=[];reverse={v:k for k,v in mapping.items()}
 candidates=[]
 for base in ['assets','tools','_BUILD_SOURCE']:
  candidates += [p for p in (R/base).rglob('*') if p.is_file() and p.suffix.lower() in ['.js','.cjs','.mjs','.py','.json','.html','.css','.ps1','.bat']]
 candidates += [p for p in R.iterdir() if p.is_file() and p.suffix.lower() in ['.html','.js','.py','.ps1','.bat']]
 for p in candidates:
  # Preserve historical cleanup journals and self-owned migration/measurement sources.
  if p.name in ['organize_assets_1007.py','asset_layout_probe_1007.py','atlas_cleanup_1006.py']:continue
  b=p.read_bytes()
  try:s=b.decode('utf-8')
  except UnicodeDecodeError:continue
  def replacement(m):
   prefix=s[max(0,m.start()-90):m.start()]
   if 'UNUSED_ASSETS/' in prefix and not re.search(r'[\s"\x27]',prefix.split('UNUSED_ASSETS/')[-1]):return m.group(0)
   return mapping[m.group(0)]
  out=pattern.sub(replacement,s)
  if p.suffix.lower()=='.json' and p.relative_to(R).as_posix() in reverse:
   old_parent=Path(reverse[p.relative_to(R).as_posix()]).parent
   try:
    value=json.loads(out)
    def remap(q):
     if isinstance(q,str) and not q.startswith(('assets/','http:','https:','UNUSED_ASSETS/')):
      old=(old_parent/q).as_posix();return mapping.get(old,q)
     if isinstance(q,list):return [remap(x) for x in q]
     if isinstance(q,dict):return {k:remap(v) for k,v in q.items()}
     return q
    updated=remap(value)
    if updated!=value:out=json.dumps(updated,indent=2,ensure_ascii=False)+'\n'
   except (json.JSONDecodeError,ValueError):pass
  if out!=s:
   backup=O/'text_before'/p.relative_to(R);backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b)
   p.write_bytes(out.encode('utf-8'));changes.append(p.relative_to(R).as_posix())
 return changes
def catalog(mapping):
 # Registry keys are stable. New rows come from the migrated owning manifest.
 reg=json.loads((O/'baseline/registry.json').read_text(encoding='utf-8'));_,_,_,_,data=manifest_object()
 src={k:mapping.get(v,v) if isinstance(v,str) else v for k,v in reg['src'].items()};src.update(data['img'])
 cells=dict(reg['cells']);cells.update(data['cells']);roots={};records=[]
 for key,path in src.items():
  if not isinstance(path,str) or not path.startswith('assets/') or not (R/path).is_file():continue
  if key in cells:root='nca_'+str(cells[key][0]);row=cells[key]
  elif key in reg['playercells']:root=reg['playercells'][key][0];row=reg['playercells'][key]
  elif key in reg['ships']:root='nsa_ship_'+(pilot_of(key) or '?');row=reg['ships'][key]
  else:root=key;row=None
  actual=src.get(root,path);owner='/'.join(Path(actual).parts[2:5]) if actual.startswith('assets/game/') else 'shared'
  records.append({'key':key,'root':root,'path':actual,'owner':owner,'cell':row})
  if root not in roots:roots[root]={'path':actual,'owner':owner,'keys':[]}
  roots[root]['keys'].append(key)
 (R/'assets/data/asset_catalog.json').write_text(json.dumps({'version':1,'frameContract':'original dimensions, stable keys, lossless RGBA','assets':records,'textures':roots},indent=2)+'\n',encoding='utf-8')
 # Small runtime table: path migration only. Ownership derives directly from real folders.
 (R/'assets/asset_paths_1007.js').write_text("'use strict';\n/* Generated only by organize_assets_1007.py. Old builder URLs resolve to the owned file. */\nwindow.BOF_ASSET_PATHS="+json.dumps(mapping,separators=(',',':'))+";\nfunction bofAssetPath(path){return typeof path==='string'?(window.BOF_ASSET_PATHS[path]||path):path;}\nfunction bofAssetOwner(path){const p=bofAssetPath(path),m=typeof p==='string'&&/^assets\\/game\\/(levels\\/stage_[0-9x]+|pilots\\/[a-z]+|shared\\/[a-z_]+)/.exec(p);return m?m[1]:'shared';}\n",encoding='utf-8')
 runtime=R/'assets/asset_paths_1007.js'
 runtime.write_text(runtime.read_text(encoding='utf-8')+"function bofAssetLoadingAllowed(path){if(document.readyState!=='loading'||window.__bofAssetRuntimeReady)return true;const owner=bofAssetOwner(path);return owner==='shared/ui'||owner==='shared/fonts'||owner.endsWith('/portraits')||/weapon_special_icons/.test(bofAssetPath(path));}\n",encoding='utf-8')
 for owner in ['pilots/'+p for p in PILOTS]+['levels/stage_'+f'{n:02}' for n in range(1,10)]+['levels/stage_x','shared']:
  d=G/owner;d.mkdir(parents=True,exist_ok=True)
  for cat in (['portraits','body_frames','ship_frames','abilities'] if owner.startswith('pilots/') else ['stage','enemies','boss','miniboss','projectiles','effects','cinematics','audio'] if owner.startswith('levels/') else []):(d/cat).mkdir(exist_ok=True)
  selected=[r for r in records if r['owner'].startswith(owner)]
  index={'owner':owner,'loading':'XART logical key -> root texture -> authored crop; atlas pixels are not separate duplicated PNGs','assets':selected}
  (d/'asset_index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
  (d/'README.md').write_text('# '+owner+'\n\nActual owned runtime files are below this directory. `asset_index.json` lists every logical key, root texture, file and crop. Do not renumber frames or edit generated atlas coordinates by hand.\n\n'+('Aircraft frames belong to this pilot. The Furyship hull is shared in `../../shared/ships`; this pilot\'s paint is applied by the runtime, so the common hull is stored once.\n' if owner.startswith('pilots/') else 'Shared player weapons, weather, fonts and cinematics live under `../../shared`. Stage 8 copied forms also load their original donor-stage art through stable keys.\n')+'\nSee `../../../../docs/ASSET_LAYOUT_1007.md` for the owner workflow and loading lifecycle.\n',encoding='utf-8')
 return len(records),len(roots)
def verify():
 journal=json.loads(((O/'journal.json') if (O/'journal.json').exists() else R/'docs/qa/asset_layout_1007_journal.json').read_text(encoding='utf-8'));bad=[]
 for q in journal['moves']:
  p=R/q['new']
  if not p.exists():bad.append('missing '+q['new'])
  elif p.suffix.lower() in ['.png','.jpg','.jpeg','.webp','.mp3','.wav','.ttf','.woff','.woff2'] and sha(p)!=q['sha256']:bad.append('bytes '+q['new'])
  if (R/q['old']).exists():bad.append('duplicate old '+q['old'])
 for q in journal['retired']:
  if (R/q['archive']).exists() and sha(R/q['archive'])!=q['sha256']:bad.append('archive '+q['old'])
 images={}
 for q in journal['repacked']:
  if q['path'] not in images:images[q['path']]=Image.open(R/q['path']).convert('RGBA')
  im=images[q['path']];t=q['row'];cell=im.crop((t[1],t[2],t[1]+t[3],t[2]+t[4]))
  if hashlib.sha256(cell.tobytes()).hexdigest()!=q['rgbaSHA256']:bad.append('cell '+q['key'])
 print(json.dumps({'moves':len(journal['moves']),'identicalCells':len(journal['repacked']),'bad':bad},indent=2));assert not bad
if mode=='--verify':verify();raise SystemExit()
assert not (O/'journal.json').exists(),'Migration already applied: use --verify.'
plan,mapping=build_plan();print(json.dumps({'files':len(mapping),'bytes':plan['assetBytes'],'groups':dict(Counter(group_for(k) for k in mapping))},indent=2),flush=True)
if mode=='--plan':raise SystemExit()
for q in plan['moves']:
 src=inside(R/q['old']);dst=inside(R/q['new']);assert not dst.exists(),dst;dst.parent.mkdir(parents=True,exist_ok=True);src.rename(dst)
# Rewrite files now at their owned destinations, and all active code/build references.
changes=rewrite_sources(mapping)
p,s,start,end,data=manifest_object();backup=O/'manifest_before_repack.js';backup.write_text(s,encoding='utf-8')
proof,retired=repack(data);p.write_text(s[:start]+json.dumps(data,separators=(',',':'))+s[start+end:],encoding='utf-8',newline='')
count,rootcount=catalog(mapping)
journal={**plan,'retired':retired,'repacked':proof,'changedText':changes,'logicalKeys':count,'roots':rootcount}
(O/'journal.json').write_text(json.dumps(journal,indent=2)+'\n',encoding='utf-8')
# Remove only proven-empty old directories, bottom up, wholly inside assets/game.
for d in sorted(G.rglob('*'),key=lambda p:len(p.parts),reverse=True):
 if d.is_dir() and d.relative_to(G).parts[0] not in ['pilots','levels','shared']:
  try:inside(d).rmdir()
  except OSError:pass
verify()
