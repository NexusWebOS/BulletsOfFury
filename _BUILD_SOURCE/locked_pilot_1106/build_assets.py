from pathlib import Path
import subprocess,json,hashlib
W=Path(__file__).resolve().parent;A=Path(r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe')
for n in ['editable','exports']:(W/n).mkdir(exist_ok=True)
p=subprocess.run([str(A),'--batch','--script-param','root='+W.as_posix(),'--script',str(W/'build_locked.lua')],capture_output=True,text=True,timeout=90);print(p.stdout,p.stderr);assert p.returncode==0
m=json.loads((W/'manifest.json').read_text())
for a in m['banks'].values():a['sha256']=hashlib.sha256((W/'exports'/Path(a['path']).name).read_bytes()).hexdigest()
for n in ['pilot','ship']:m['sources'][n].update(json.loads((W/'source'/(n+'.json')).read_text()));m['sources'][n]['sha256']=hashlib.sha256((W/'source'/(n+'.png')).read_bytes()).hexdigest()
(W/'manifest.json').write_text(json.dumps(m,indent=2));print('READY',len(m['banks']),'banks')
