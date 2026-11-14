from pathlib import Path
import sys,runpy,json,hashlib
W=Path(__file__).resolve().parent;O=(W.parents[1]/'outputs/Recovered-boss-animations').resolve();p=(O/'draconus-restored-side-swings.mp4').resolve();dest=(O/'superseded-draconus-windup-take.mp4').resolve();r=json.loads((O/'stage8-recording.json').read_text())
assert p.parent==O and dest.parent==O and not dest.exists()and r['stage']==8 and r['complete']and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
r['supersededReason']='The full old sheet contained two directional sweeps. The first mapping incorrectly put its second windup at contact. Retained diagnostics only; native source poses5/12 now own left/right contacts.'
(O/'superseded-stage8-recording.json').write_text(json.dumps(r,indent=2));p.rename(dest)
sys.argv.append('--stage8');runpy.run_path(str(W/'record.py'),run_name='__main__')
