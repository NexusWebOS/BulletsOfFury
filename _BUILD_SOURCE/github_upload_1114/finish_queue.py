from pathlib import Path
import time,sys,subprocess,json,os
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';started=time.monotonic();receipt=O/'package-receipt.json'
print('Final verification/publication queued behind the current installer upload.',flush=True)
while True:
 assert time.monotonic()-started<3600,'Installer upload did not finish within the bounded wait.'
 try:
  data=json.loads(receipt.read_text());assert data['parts'];break
 except(FileNotFoundError,json.JSONDecodeError):time.sleep(3)
for job in ['verify.py','publish.py','receipt.py']:
 (O/'pipeline-state.json').write_text(json.dumps(dict(phase=job,pid=os.getpid()),indent=2));print('STARTING',job,flush=True);subprocess.run([sys.executable,str(W/job)],check=True)
(O/'pipeline-state.json').write_text(json.dumps(dict(phase='complete',pid=os.getpid()),indent=2));print('ALL UPLOAD, VALIDATION, PUBLICATION AND SOURCE RECEIPT STEPS COMPLETE.',flush=True)
