from pathlib import Path
import subprocess,json,time,hashlib
W=Path(__file__).resolve().parent;O=(W.parents[1]/'outputs/Draconus-rotor-and-full-stages').resolve();V=(O/'stage-8').resolve();D=(O/'incomplete-stage8-take1').resolve()
assert V.parent==O and D.parent==O and not D.exists()
q=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter 'ProcessId=29732' | Select-Object ProcessId,CommandLine | ConvertTo-Json"],capture_output=True,text=True,check=True)
info=json.loads(q.stdout);assert info['ProcessId']==29732 and 'draconus_rotor_stages_1111' in info['CommandLine']and'--record-8'in info['CommandLine'],info
subprocess.run(['taskkill','/PID','29732','/T','/F'],capture_output=True,check=True);time.sleep(2)
r=json.loads((V/'report.json').read_text());r.update(completed=False,reason='Recorder/browser stopped responding during native rebirth; no successful full film. Full raw bytes/screenshots/last state and Python stack retained.',lastState=json.loads((V/'live.json').read_text()))
(V/'report.json').write_text(json.dumps(r,indent=2));V.rename(D)
print('Stopped only the verified task recorder tree. Retained its incomplete take and prepared a fresh Stage 8 folder.',flush=True)
