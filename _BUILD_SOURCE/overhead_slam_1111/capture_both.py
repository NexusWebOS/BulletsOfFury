from pathlib import Path
import subprocess,sys

script=Path(__file__).with_name('capture_hammers.py')
for unit in ['chronos','dracodia']:
 print('Starting isolated '+unit+' recording.',flush=True)
 subprocess.run([sys.executable,str(script),unit],check=True)
