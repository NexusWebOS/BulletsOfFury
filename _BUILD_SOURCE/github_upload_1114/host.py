from pathlib import Path
import subprocess,json,hashlib
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/GitHub-upload-1114';qa=O/'host-selftest';qa.mkdir(exist_ok=True);exe=W/'host/Bullets of Fury.exe'
ps="$p=Start-Process -FilePath '"+str(exe)+"' -ArgumentList @('--self-test','--qa-dir','"+str(qa)+"') -WindowStyle Hidden -PassThru -Wait;exit $p.ExitCode"
p=subprocess.run(['powershell','-NoProfile','-Command',ps],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=45);assert p.returncode==0,p.stdout+p.stderr
checks=json.loads((qa/'self-tests.json').read_text());assert all(q['passed']for q in checks);(O/'native-host-checks.json').write_text(json.dumps(dict(checks=checks,hostSha256=hashlib.sha256(exe.read_bytes()).hexdigest()),indent=2));print('Actual native Windows host:',len(checks),'self-tests passed.',flush=True)
