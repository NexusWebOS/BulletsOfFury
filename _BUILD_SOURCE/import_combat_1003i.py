"""Import generated originals unchanged; register measured cells and sound provenance."""
from pathlib import Path
import json,hashlib,shutil,urllib.request
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'assets/game/combat_1003i';A.mkdir(parents=True,exist_ok=True)
sources=json.loads((R/'_ART_SOURCES/combat_1003i/images.json').read_text())
images=[]
for j in sources:
 dest=A/(j['name']+'.png')
 if not dest.exists():shutil.copyfile(j['source'],dest)
 im=Image.open(dest)
 images.append({**j,'file':dest.relative_to(R).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'size':list(im.size),'active':j['name']!='laser_muzzles_edit'})
parts=[]
im=Image.open(A/'reaver_parts.png')
for x0,x1,y0,y1 in [(0,418,0,710),(418,835,0,710),(835,1254,0,710),(0,418,710,1254),(418,835,710,1254),(835,1254,710,1254)]:
 bbox=im.getchannel('A').crop((x0,y0,x1,y1)).point(lambda a:255 if a>64 else 0).getbbox()
 parts.append([x0+bbox[0],y0+bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]])
beam=[]
for y in [125,335,548,756,966,1175]:
 beam.append([[x,y-75,350,150] for x in [35,450,855]])
muzzles=[[[x-151,y-124,302,248] for x in [213,512,810]] for y in [137,378,626,875,1124,1377]]
rig={'parts':parts,'beams':beam,'muzzles':muzzles,'colors':['fire','ice','toxic','void','red','gold']}
(A/'cells.json').write_text(json.dumps(rig,indent=2)+'\n')
(R/'assets/combat_art_1003i.js').write_text("'use strict';\nconst AV3_ART="+json.dumps(rig,separators=(',',':'))+';\n',encoding='utf-8')
(A/'manifest.json').write_text(json.dumps({'images':images,'cells':'assets/game/combat_1003i/cells.json'},indent=2)+'\n')
jobs=json.loads((R/'_shots/combat_1003i/downloads_complete.json').read_text())
assert len(jobs)==len({j['name'] for j in jobs})==20, 'Every sound family must appear exactly once'
audio=[]
for j in jobs:
 dest=A/(j['name']+'.mp3')
 if not dest.exists():
  req=urllib.request.Request(j['url'],headers={'User-Agent':'BulletsOfFuryAssetImport/1.0'})
  with urllib.request.urlopen(req,timeout=60) as res:dest.write_bytes(res.read())
 original=R/'_ART_SOURCES/combat_1003i/audio_originals'/dest.name
 if not original.exists():original=dest
 audio.append({k:v for k,v in j.items() if k!='url'}|{'file':dest.relative_to(R).as_posix(),'source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'runtime_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(R/'_ART_SOURCES/combat_1003i/audio.json').write_text(json.dumps({'provider':'ElevenLabs Sound Effects v2','flow_id':'csYhMmwrGgLtEOrL4TGq','cues':audio},indent=2)+'\n')
print(json.dumps({'images':len(images),'sounds':len(audio),'parts':parts}))
