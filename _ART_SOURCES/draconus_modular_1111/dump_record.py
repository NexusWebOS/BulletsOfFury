from pathlib import Path
import subprocess,sys,shutil
W=Path(__file__).resolve().parent;T=W/'diagnostic-tools'
q=subprocess.run([sys.executable,'-m','pip','install','--no-deps','--target',str(T),'py-spy'],capture_output=True,text=True)
print(q.stdout[-1500:],q.stderr[-500:],flush=True);assert q.returncode==0
exe=next(T.rglob('py-spy.exe'));q=subprocess.run([str(exe),'dump','--pid','3932'],capture_output=True,text=True,timeout=30)
(W/'stalled-stage8-stack.txt').write_text(q.stdout+q.stderr);print(q.stdout,q.stderr,flush=True)
