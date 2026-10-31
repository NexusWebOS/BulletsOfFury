from pathlib import Path
import urllib.request,json,tarfile,io,hashlib,re
ROOT=Path(__file__).resolve().parents[3] if Path(__file__).parent.name=='_research' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
OUT=ROOT/'expansion/topdown/vendor/three';OUT.mkdir(parents=True,exist_ok=True)
data=json.load(urllib.request.urlopen('https://registry.npmjs.org/three/0.186.1'))
version=data['version'];raw=urllib.request.urlopen(data['dist']['tarball']).read()
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tar:
 code=tar.extractfile('package/build/three.module.js').read().decode('utf-8')
 core=tar.extractfile('package/build/three.core.js').read()
 license=tar.extractfile('package/LICENSE').read()
(OUT/'three.module.js').write_text(code,encoding='utf-8')
(OUT/'three.core.js').write_bytes(core)
old=OUT/'three.global.js'
if old.is_file():old.unlink()
(OUT/'LICENSE').write_bytes(license)
(OUT/'provenance.json').write_text(json.dumps({'version':version,'source':data['dist']['tarball'],'integrity':data['dist'].get('integrity'),'build':'package/build/three.module.js and three.core.js','buildSHA256':hashlib.sha256(code.encode()).hexdigest(),'wrapper':'None. Unmodified official ES modules, loaded locally.'},indent=2),encoding='utf-8')
print(json.dumps({'version':version,'bytes':len(code)}))
