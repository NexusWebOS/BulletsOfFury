from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');SRC=ROOT/'_ART_SOURCES/hq_turns_1115';OUT=ROOT/'_shots/hq_turns_1115';INSTALL=OUT/'reproduced';meta=json.loads((SRC/'manifest.json').read_text(encoding='utf8'));checks=[]
for pk,a in meta['pilots'].items():
 sheet=Image.new('RGBA',(1280,1024))
 for f in range(20):sheet.alpha_composite(Image.open(SRC/pk/('%02d.png'%f)).convert('RGBA'),((f%5)*256,(f//5)*256))
 dest=INSTALL/a['path'];dest.parent.mkdir(parents=True,exist_ok=True);sheet.save(dest,lossless=True);h=hashlib.sha256(dest.read_bytes()).hexdigest();assert h==a['sha256'];checks.append({'pilot':pk,'sha256':h,'exact':True})
(INSTALL/'assets/hq_turn_art_1115.js').write_text('"use strict";\nconst HQ21_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
assert (INSTALL/'assets/hq_turn_art_1115.js').read_bytes()==(ROOT/'assets/hq_turn_art_1115.js').read_bytes()
(OUT/'reproduction-qa.json').write_text(json.dumps({'checks':checks,'registryExact':True},indent=2),encoding='utf8');print('All10 turn pages and registry reproduce byte-for-byte from retained source cells')
