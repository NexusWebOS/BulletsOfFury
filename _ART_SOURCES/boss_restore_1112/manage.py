from pathlib import Path
import sys,subprocess
W=Path(__file__).resolve().parent
jobs={'--install':'install.py','--verify':'verify.py','--record':'record.py','--record-drac':'record_drac.py','--checks':'checks.py','--finish':'finish.py'}
assert len(sys.argv)==2 and sys.argv[1]in jobs
subprocess.run([sys.executable,str(W/jobs[sys.argv[1]])],check=True)
