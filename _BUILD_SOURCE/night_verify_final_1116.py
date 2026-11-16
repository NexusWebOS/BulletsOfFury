from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';p=R/'_BUILD_SOURCE/night_static_1116.py';s=p.read_text(encoding='utf8')
if "'assets/night_weather_1116.js'"not in s:s=s.replace("'assets/night_city_atlas_1116.js'","'assets/night_city_atlas_1116.js','assets/night_weather_1116.js'")
p.write_text(s,encoding='utf8',newline='\n')
with(O/'full-suite-post-weather.log').open('w',encoding='utf8')as log:q=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,stdout=log,stderr=subprocess.STDOUT)
report={'coreExit':q.returncode};(O/'full-suite-final.log').write_bytes((O/'full-suite-post-weather.log').read_bytes())
with(O/'static-post-weather.log').open('w',encoding='utf8')as log:q=subprocess.run(['python',str(p)],cwd=R,stdout=log,stderr=subprocess.STDOUT)
report['staticExit']=q.returncode;report['nightFilesLF']={p.name:b'\r\n'not in p.read_bytes()for p in(R/'assets').glob('night_*1116.js')};base=json.loads((O/'baseline-hashes.json').read_text());report['preservedOldFiles']={k:hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in base.items()if k!='index.html'}
(O/'final-verification.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2));assert report['coreExit']==report['staticExit']==0 and all(report['nightFilesLF'].values())and all(report['preservedOldFiles'].values())
