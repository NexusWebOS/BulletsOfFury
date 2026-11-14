from pathlib import Path
import json,hashlib,shutil,subprocess,sys
import os
from PIL import Image
W=Path(__file__).resolve().parent; R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury'); O=W.parents[1]/'outputs/Solid-metal-hammers'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--status'in sys.argv or '--stop-verification'in sys.argv:
 pattern=str(W).replace("'","''")+'\\verify_stage*.py'
 script="$hammerAll=@(Get-CimInstance Win32_Process); $hammerRoots=@($hammerAll | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like '*"+pattern+"*' }); function HammerChildren($parent) { foreach($child in $hammerAll) { if($child.ParentProcessId -eq $parent) { $child; HammerChildren $child.ProcessId } } }; foreach($root in $hammerRoots) { $children=@(HammerChildren $root.ProcessId); [pscustomobject]@{pid=$root.ProcessId; children=@($children | Select-Object ProcessId,Name,WorkingSetSize,UserModeTime)} | ConvertTo-Json -Depth 4; "
 if '--stop-verification'in sys.argv: script+="foreach($child in $children) { Stop-Process -Id $child.ProcessId -Force -ErrorAction SilentlyContinue }; Stop-Process -Id $root.ProcessId -Force -ErrorAction SilentlyContinue; Write-Output 'Stopped only this hammer verifier and its children'; "
 script+='}'
 subprocess.run(['powershell','-NoProfile','-Command',script],check=True)
 sys.exit(0)
plan=json.loads((W/'installation-plan.json').read_text())
if '--finalize'in sys.argv:
 subprocess.run([sys.executable,str(W/'finalize.py')],check=True);sys.exit(0)
for n,h in plan['protected'].items(): assert sha(R/n)==h,('Protected source changed',n)
if '--verify-only'not in sys.argv:
 for n,h in plan['before'].items(): assert sha(R/n)==h,('Changed while preparing',n)
 subprocess.run(['node','--check',str(W/'front_hammer_art_1111.js')],check=True)
 for j in json.loads((W/'aseprite-jobs.json').read_text()):
  a=Image.open(W/'exports'/(j['name']+'_regular.png')).convert('RGBA'); b=Image.open(W/'exports'/(j['name']+'_roundtrip.png')).convert('RGBA'); assert a.tobytes()==b.tobytes(),j['name']
 for n in plan['files']:
  src=W/'front_hammer_art_1111.js'if n.endswith('.js')else W/'exports'/Path(n).name
  shutil.copy2(src,R/n)
 (W/'installation.json').write_text(json.dumps(dict(before=plan['before'],after={n:sha(R/n)for n in plan['files']},protected=plan['protected'],newWholeDrawings=48,overheadTimelineFrames=64),indent=2))
 print('Installed straight-shaft, rigid-head overhead poses in all four forms.',flush=True)
for stage in [5,8]:
 subprocess.run([sys.executable,str(W/f'verify_stage{stage}.py'),str(stage)],check=True)
 q=json.loads((O/f'verification-stage{stage}/checks.json').read_text()); assert not q['errors']and all(c['passed']for c in q['checks']),dict(failed=[c['name']for c in q['checks']if not c['passed']],errors=q['errors'])
subprocess.run([sys.executable,str(W/'verify_password.py')],check=True)
subprocess.run(['node','--check','assets/game.js'],cwd=R,check=True)
full=subprocess.run(['node','_BUILD_SOURCE/test_fl.js'],cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace')
(W/'full-suite.txt').write_text(full.stdout+'\n'+full.stderr,encoding='utf8');(W/'full-suite.json').write_text(json.dumps(dict(exit=full.returncode,lastError=full.stderr[-1600:]),indent=2))
print('Broad suite exit',full.returncode,full.stderr[-500:],flush=True)
