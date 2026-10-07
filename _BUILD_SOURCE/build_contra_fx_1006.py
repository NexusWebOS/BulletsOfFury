"""Copy the authored RGBA reel unchanged; emit native clip metadata. No raster edits."""
from pathlib import Path
import argparse, hashlib, json, shutil, struct
root=Path(__file__).resolve().parents[1]
source=root/'_ART_SOURCES/contra_fx_1006/boss_signature_fx.png'
qa=json.loads((root/'_ART_SOURCES/contra_fx_1006/source_manifest.json').read_text(encoding='utf-8'))
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()==qa['sha256'], 'Source changed'
assert data[:8]==b'\x89PNG\r\n\x1a\n'
assert struct.unpack('>II',data[16:24])==(1448,1086)
clips={name:{'row':row,'frames':list(range(row*4,row*4+4)),'durationSeconds':duration,'pivot':[181,362*pivot]}
       for name,row,duration,pivot in [('joint',0,.65,.58),('breach',2,1,.5)]}
out=root/'assets/game/contra_fx_1006'
manifest={'id':'hc1006_signature','file':'boss_signature_fx.png','nativeSize':[1448,1086],'cellSize':[362,362],'grid':[4,3],'clips':clips,'collision':'cosmetic_only','loop':False,'processing':'Exact source copy; no pixel editing','sha256':qa['sha256'],'source':'_ART_SOURCES/contra_fx_1006/boss_signature_fx.png','prompt':'_ART_SOURCES/contra_fx_1006/prompt.txt','sourceQA':qa['frames'],'minimumSignificantAlphaPadding':qa['minimumSignificantAlphaPadding'],'notes':'Only joint and breach rows used on Herald. Contact row retained, unused. Native blending/anchor review captured in docs/qa/contra_herald_1006.json.'}
ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
if args.write:
    out.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,out/'boss_signature_fx.png')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
else:
    assert hashlib.sha256((out/'boss_signature_fx.png').read_bytes()).hexdigest()==manifest['sha256']
    assert json.loads((out/'manifest.json').read_text(encoding='utf-8'))==manifest
print(json.dumps({'verified':True,'sha256':manifest['sha256'],'clips':list(clips),'nativeSize':manifest['nativeSize'],'pixelsEdited':False}))
