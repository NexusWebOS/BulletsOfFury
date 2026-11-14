from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;O=(W.parents[1]/'outputs/Draconus-rotor-and-full-stages').resolve();V=(O/'stage-8').resolve();D=(O/'incomplete-stage8-take2').resolve();p=(O/'stage-8-furious.mp4').resolve();r=json.loads((V/'report.json').read_text())
assert V.parent==O and D.parent==O and p.parent==O and not D.exists()
assert not r['completed']and r['stage']==8 and r['reason']=='runtime error'and any("reading 'bounds'"in e for e in r['consoleErrors'])
if p.exists():
 r['discardedIncompleteMovie']=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reason='Incomplete take identified real stale Retina descriptor bug. Screenshots/full trace/error retained; replaying the whole stage after fixing the bug.')
 (V/'report.json').write_text(json.dumps(r,indent=2));p.unlink()
V.rename(D);print('Preserved native failure evidence; prepared full Stage8 replay after the repair.',flush=True)
