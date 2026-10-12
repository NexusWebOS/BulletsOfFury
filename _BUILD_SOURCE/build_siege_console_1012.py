"""Publish Mike's selected vented Siege Console, retaining its authored pixels."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/side_hud_1012/siege-console.png'
OUT=ROOT/'assets/game/shared/ui/siege_console_1012';OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'_ART_SOURCES/side_hud_1012/registration.json').read_text(encoding='utf-8'))
art=next(v for v in data['concepts'] if v['id']=='siege-console')
assert Image.open(SOURCE).size==(1024,1536)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==art['sha256']
art.update(key='hud_siege_console_1012',path='assets/game/shared/ui/siege_console_1012/frame.png',
 approved='Mike, October 12: this looks good, continue (vented Siege Console attachment)',
 columns=[[0,0,512,1536],[512,0,512,1536]],compactHeight=176,
 modules={'scores':[28,52,468,222],'roll':[28,258,238,216],'somer':[266,258,230,216],
 'weapon':[28,474,468,400],'radar':[532,52,464,410],'special':[532,444,464,396],
 'lives':[534,834,230,218],'missiles':[764,834,232,218],'lock':[532,1042,464,304]})
shutil.copyfile(SOURCE,OUT/'frame.png')
(OUT/'registration.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/siege_console_art_1012.js').write_text('"use strict";\n// Owned by build_siege_console_1012.py.\nconst SC12_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
tax=ROOT/'assets/data/ART_TAXONOMY.json';d=json.loads(tax.read_text(encoding='utf-8'))
d['hud_siege_console_1012']={'role':'player_side_hud','sheet':None,'note':'Mike selected the vented Siege Console on October 12. Full paired authored plate, proportional columns and measured wells; compact modules share the same plate. Owner build_siege_console_1012.py; renderer siege_console_1012.js.'}
tax.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Siege Console published: exact approved RGBA plate, fixed wells, compact module crops.')
