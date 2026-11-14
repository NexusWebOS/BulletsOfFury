from pathlib import Path
import subprocess,sys
W=Path(__file__).resolve().parent
jobs={'--assets':'asset_probe.py','--author':'author.py','--repair':'repair.py','--install':'install.py','--full':'full.py','--targeting':'targeting.py','--finish':'finish.py','--art':'art.py','--native':'native.py'}
assert len(sys.argv)==2 and sys.argv[1]in jobs
subprocess.run([sys.executable,str(W/jobs[sys.argv[1]])],check=True)
