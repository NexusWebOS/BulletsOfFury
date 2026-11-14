import subprocess,shutil,json
from pathlib import Path
W=Path(__file__).resolve().parent
print('Free bytes:',shutil.disk_usage(W).free,flush=True)
q=subprocess.run(['powershell','-NoProfile','-Command',"Get-Process python,msedge,ffmpeg -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,WorkingSet64,CPU,StartTime | ConvertTo-Json"],capture_output=True,text=True)
print(q.stdout,q.stderr,flush=True)
for p in (W.parents[1]/'outputs/Draconus-rotor-and-full-stages/stage-8').glob('*'):
 if p.is_file():print(p.name,p.stat().st_size,p.stat().st_mtime,flush=True)
for n in [7,8]:
 p=W.parents[1]/f'outputs/Draconus-rotor-and-full-stages/stage-{n}/live.json'
 if p.exists():
  r=json.loads(p.read_text());print('LIVE',n,json.dumps({k:r.get(k)for k in ['wall','state','kind','hp','mode','phase','form','gunPhases','diskFree']}),flush=True)
