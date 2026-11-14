from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;O=(W.parents[1]/'outputs/Draconus-rotor-and-full-stages').resolve();V=(O/'stage-5').resolve();D=(O/'incomplete-stage5-take1').resolve();p=(O/'stage-5-furious.mp4').resolve();r=json.loads((V/'report.json').read_text())
assert not r['completed']and r['stage']==5 and V.parent==O and D.parent==O and p.parent==O and not D.exists()
if p.exists():
 r['discardedIncompleteMovie']=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reason='Incomplete recording fixture; no successful stage film existed. Native screenshots and trace retained.');(V/'report.json').write_text(json.dumps(r,indent=2));p.unlink()
V.rename(D)
print('Retained incomplete-run diagnostics; freed only the unsuccessful task recording for the corrected full run.')
