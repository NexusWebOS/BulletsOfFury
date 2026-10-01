"""Playable release: registered runtime files only; expansion remains separate.
Combat sprites, projectile art, icons and fonts remain lossless. Large scenery,
cinematic and portrait plates use high-quality WebP, without resizing.
Runtime URL strings change in the release copy only.
"""
import concurrent.futures, hashlib, json, os, shutil, zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(os.environ.get('BOF_RELEASE_DIR',str(ROOT.parent/'release_1001'/'BulletsOfFury')))
OUT.mkdir(parents=True,exist_ok=True)
paths=json.loads((ROOT/'_shots/repair_0927/runtime-assets.json').read_text())['paths']
expected={p[:-4]+'.webp' if p.endswith('.png') else p for p in paths}
expected.update(['index.html','README.txt','PLAY_LOCAL.ps1','PLAY_BULLETS_OF_FURY.bat'])
# Remove only previous output files inside this script's verified release directory.
# Build only into a new or previously generated folder. Never delete arbitrary local files.
if any(OUT.iterdir()):
 existing={f.relative_to(OUT).as_posix() for f in OUT.rglob('*') if f.is_file()}
 if existing-expected:raise SystemExit('Release directory has unrelated files; choose a fresh BOF_RELEASE_DIR')
def scenic(rel):
 return (rel.endswith(('furious_review_0927/realm_terrain.png','furious_review_0927/stagex_terrain.png','stage678_repair_0928/sewer_connector.png')) or '/cinematic' in rel or '/generated_cinematic/' in rel or '/backgrounds/' in rel
  or '/pilots_0922/' in rel or '/bg5/' in rel or '/bg6/' in rel
  or any('/atlas/'+k in rel for k in ['ui_menu','ui_dialogue','pilots_','terrain_'])
  or '/levels/' in rel or '/space_loops_' in rel or '/transitions_topdown/' in rel
  or any('/game/'+k in rel for k in ['campaign_0930/','cinema_0930/'])
  or any('/game/'+k in rel for k in ['nst','nsky','mapJungle','mapVolcano','mapIce','nend'])
  or rel.endswith(('/menu.png','/campaign_map.png')))
def high_detail(rel):
 if any('/atlas/'+k in rel for k in ['en_','retired_','fx_weather','stage_runtime/']):return True
 if any(k in rel.lower() for k in ['effect','fx_','reticle','projectile','icon','barrel','beam','shield']):return False
 return any(k in rel for k in ['/realm_0930/','/encounters_0930/','/bosses/','/stage5_hammer/','/stage5_archmage_0916/',
  '/final_boss_0924/','/final_boss_0925_patterns/','/stage7_modular_0927/',
  '/ui/modes_0915/','/ui/forge_modular_0923/concept']) or '/combat_final/stage7_warden_' in rel
def copy(rel):
 src=ROOT/rel;dst=OUT/rel
 if src.suffix.lower()=='.png':
  dst=dst.with_suffix('.webp');dst.parent.mkdir(parents=True,exist_ok=True)
  mode='scenic84' if scenic(rel) else 'detail94' if high_detail(rel) else 'lossless'
  cache=OUT.parent/'compression-cache';cache.mkdir(exist_ok=True)
  marker=cache/(hashlib.sha256(rel.encode()).hexdigest()[:20]+'.'+mode+'.done')
  if not dst.exists() or dst.stat().st_mtime<src.stat().st_mtime or not marker.exists():
   with Image.open(src) as im:
    im.save(dst,'WEBP',lossless=mode=='lossless',quality=94 if mode=='detail94' else 84,method=4,exact=True)
   marker.touch()
 elif src.suffix.lower() in ('.js','.css','.html','.json'):
  dst.parent.mkdir(parents=True,exist_ok=True)
  dst.write_text(src.read_text(encoding='utf-8').replace('.png','.webp'),encoding='utf-8',newline='\n')
 else:
  dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 return dst.stat().st_size
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 total=sum(pool.map(copy,paths))
copy('index.html')
shutil.copy2(ROOT/'PLAY_LOCAL.ps1',OUT/'PLAY_LOCAL.ps1')
(OUT/'PLAY_BULLETS_OF_FURY.bat').write_text('@echo off\ncd /d "%~dp0"\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0PLAY_LOCAL.ps1"\nif errorlevel 1 pause\n',encoding='ascii',newline='\r\n')
(OUT/'README.txt').write_text('Bullets of Fury playable build\nExtract the entire ZIP before playing.\nDouble-click PLAY_BULLETS_OF_FURY.bat for full audio. No Python installation required.\nClick the game once to enable browser audio.\nF toggles fullscreen. Controls are in Help.\n\nThis package excludes development tools, source art, unused music and the separate Overdrive expansion.\nProjectile art, icons and fonts use lossless WebP. Scenery, cinematic plates and high-detail enemy texture atlases use high-quality WebP at original resolution. Audio is unchanged.\n',encoding='utf-8')
zip_path=OUT.parent/'BulletsOfFury-playable-2026-10-01.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(OUT.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(OUT.parent))
report={'files':len(paths),'runtime_bytes':total,'zip_bytes':zip_path.stat().st_size,'zip_sha256':hashlib.file_digest(zip_path.open('rb'),'sha256').hexdigest(),'limit_bytes':500_000_000,'path':str(zip_path)}
(OUT.parent/'build-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if report['zip_bytes']>report['limit_bytes']:raise SystemExit('ZIP exceeds 500 MB')
