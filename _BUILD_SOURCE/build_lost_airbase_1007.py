"""Copy exact generated Stage 4 pixels; no crop, resize, recolor, or atlas change."""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source',type=Path);a=p.parse_args()
src=R/'_ART_SOURCES/hardcorps_1007/stage4_airbase.png'
dst=R/'assets/game/levels/stage_04/stage/hardcorps_1007/stage4_airbase.png'
if a.source:
 assert a.source.is_file();src.parent.mkdir(parents=True,exist_ok=True)
 if src.exists():assert src.read_bytes()==a.source.read_bytes(),'Refuse to replace a different archived source'
 else:shutil.copyfile(a.source,src)
assert src.is_file(),'Supply --source for the first import'
im=Image.open(src);assert im.size==(1024,1536)
dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
sha=hashlib.sha256(src.read_bytes()).hexdigest();assert hashlib.sha256(dst.read_bytes()).hexdigest()==sha
report={'source':str(src.relative_to(R)).replace('\\','/'),'deployed':str(dst.relative_to(R)).replace('\\','/'),'size':list(im.size),'mode':im.mode,'sha256':sha,'bytes':src.stat().st_size,'processing':'Exact byte copy; native pixels retained. Runtime world-scale and alternating Y reflection only.','promptManifest':'_ART_SOURCES/hardcorps_1007/generation_manifest.json'}
(dst.parent/'stage4_airbase_manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
