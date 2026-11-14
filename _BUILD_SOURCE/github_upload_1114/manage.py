from pathlib import Path
import sys,subprocess
W=Path(__file__).resolve().parent
jobs={'--followup':'followup.py','--status':'status.py','--portable':'portable.py','--plan':'plan.py','--inspect':'inspect_repo.py','--fetch':'fetch.py','--prepare':'prepare.py','--package':'package.py','--verify':'verify.py','--commit':'commit.py','--publish':'publish.py','--receipt':'receipt.py'}
assert len(sys.argv)==2 and sys.argv[1]in jobs
subprocess.run([sys.executable,str(W/jobs[sys.argv[1]])],check=True)
