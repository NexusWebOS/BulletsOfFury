from pathlib import Path
import hashlib,json,sys,shutil
W=Path(__file__).resolve().parent;work=W.parent.resolve();R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury/_ART_SOURCES');maps={n:n for n in ['heavy_hammer_1111','three_way_hammer_1111','front_hammer_1111','solid_hammer_1111','cap_strikes_1111','overhead_slam_1111']};maps['ship_forms_1111']='boss_ship_forms_1111';eligible=[];totals={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for folder,archive in maps.items():
 root=(work/folder).resolve();dest=R/archive
 if not dest.is_dir():continue
 total=0
 for p in root.rglob('*'):
  if not p.is_file()or p.suffix not in ['.png','.webp','.aseprite']or p.is_symlink():continue
  other=dest/p.relative_to(root)
  if other.is_file()and p.stat().st_size==other.stat().st_size and sha(p)==sha(other):
   eligible.append(dict(temporary=str(p),canonical=str(other),bytes=p.stat().st_size,sha256=sha(p)));total+=p.stat().st_size
 totals[folder]=total
report=dict(bytes=sum(q['bytes']for q in eligible),folders=totals,files=eligible,free=shutil.disk_usage(W).free,scope='Only our temporary work-folder graphics with byte-identical canonical source-archive copies. No delivered outputs, canonical masters, prompts, code, uploads or project assets.')
(W/'duplicate-working-exports.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='files'}),flush=True)
if '--tidy'in sys.argv:
 for q in eligible:
  p=Path(q['temporary']).resolve();master=Path(q['canonical']);assert p.is_relative_to(work)and p.parent!=work and p.suffix in ['.png','.webp','.aseprite'];assert master.is_file()and sha(master)==q['sha256']and sha(p)==q['sha256'];p.unlink()
 report['freeAfter']=shutil.disk_usage(W).free;(W/'working-cache-cleanup.json').write_text(json.dumps(report,indent=2));print('Freed only verified duplicate temporary graphics:',report['bytes'],flush=True)
