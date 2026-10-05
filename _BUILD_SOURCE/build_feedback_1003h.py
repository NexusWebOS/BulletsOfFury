"""Preserve original imagegen outputs and record the active art/cell contract."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1]
source=R/'_ART_SOURCES/feedback_1003h/generation.json'
entries=json.loads(source.read_text(encoding='utf-8-sig'))
out=R/'assets/game/feedback_1003h';out.mkdir(parents=True,exist_ok=True)
for e in entries:
 dest=out/(e['name']+'.png');src=Path(e['source'])
 if not dest.exists():shutil.copyfile(src,dest)
 data=dest.read_bytes()
 if src.exists() and hashlib.sha256(data).digest()!=hashlib.sha256(src.read_bytes()).digest():raise ValueError('Changed generated pixels: '+e['name'])
 e['file']=dest.relative_to(R).as_posix();e['sha256']=hashlib.sha256(data).hexdigest()
 e['width']=int.from_bytes(data[16:20],'big');e['height']=int.from_bytes(data[20:24],'big')
 e['active']=e['name'] not in ['orbital_overhead','earth_surface']
 e['tool']='built-in image_gen'
source.write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
manifest={'assets':[{k:e[k] for k in ['name','file','width','height','sha256','active']} for e in entries],
 'runtime':'assets/feedback_1003h.js','source':source.relative_to(R).as_posix(),
 'notes':'Original outputs unchanged. Neutral portrait bounds and uneven rebel pitch bounds are measured in runtime. Closeup is a 2x2 equal grid. Current Furyship reference is furyship_0914/runtime_base.png; legacy-ship cinematic attempts preserved but not loaded.'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
taxonomy=R/'assets/data/ART_TAXONOMY.json';data=json.loads(taxonomy.read_text(encoding='utf-8-sig'))
data['h3_']={'role':'portrait_and_cinematic','sheet':None,'note':manifest['notes']+' Prompts and provenance: _ART_SOURCES/feedback_1003h/generation.json. Build: _BUILD_SOURCE/build_feedback_1003h.py.'}
taxonomy.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\r\n')
print('Preserved',len(entries),'original outputs;',sum(e['active'] for e in entries),'active assets.')
