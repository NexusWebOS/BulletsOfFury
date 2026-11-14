from pathlib import Path
import sys,subprocess
W=Path(__file__).resolve().parent
jobs={'--gate':'gate.py','--install':'install.py','--verify':'verify.py','--record':'record.py','--finish':'finish.py','--checks':'checks.py','--author':'author.py'}
assert len(sys.argv)==2 and sys.argv[1]in jobs
subprocess.run([sys.executable,str(W/jobs[sys.argv[1]])],check=True)
