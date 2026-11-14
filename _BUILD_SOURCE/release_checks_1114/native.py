from pathlib import Path
import subprocess,sys
W=Path(__file__).resolve().parent
for n in ['native_behavior.py','native_gate.py']:subprocess.run([sys.executable,str(W/n)],check=True)
