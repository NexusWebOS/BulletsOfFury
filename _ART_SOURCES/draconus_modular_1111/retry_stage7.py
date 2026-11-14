from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;O=(W.parents[1]/'outputs/Draconus-rotor-and-full-stages').resolve();V=(O/'stage-7').resolve();D=(O/'incomplete-stage7-take1').resolve();p=(O/'stage-7-furious.mp4').resolve();r=json.loads((V/'report.json').read_text())
assert not r['completed'] and r['stage']==7 and r['reason']=='recording space limit'
assert V.parent==O and D.parent==O and p.parent==O and not D.exists()
assert shutil.disk_usage(O).free>1_400_000_000
if p.exists():
 r['discardedIncompleteMovie']=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reason='Incomplete full-stage take stopped for drive space. Screenshots, complete trace and native source hashes retained.')
 (V/'report.json').write_text(json.dumps(r,indent=2));p.unlink()
V.rename(D)
print('Preserved unsuccessful Stage 7 diagnostics; prepared a fresh complete recording. Free bytes:',shutil.disk_usage(O).free)
