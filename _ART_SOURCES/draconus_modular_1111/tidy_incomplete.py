from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;O=(W.parents[1]/'outputs/Draconus-rotor-and-full-stages').resolve();folder=(O/'incomplete-stage8-take1').resolve();p=(folder/'capture-native.mp4').resolve()
done=json.loads((O/'stage-8/report.json').read_text());failed=json.loads((folder/'report.json').read_text())
assert done['completed']and done['decoded']and not failed['completed']
assert folder.parent==O and p.parent==folder and p.name=='capture-native.mp4'
if p.exists():
 note=dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reason='Unsuccessful stalled take only. Completed decoded Stage8 film, original art, screenshots, native failure report and all trace evidence retained.')
 (W/'incomplete-capture-cleanup.json').write_text(json.dumps(note,indent=2));p.unlink()
print('Free bytes after removing only our unsuccessful raw take:',shutil.disk_usage(O).free,flush=True)
