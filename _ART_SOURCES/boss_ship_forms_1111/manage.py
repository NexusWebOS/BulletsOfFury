from pathlib import Path
import sys,subprocess
W=Path(__file__).resolve().parent
scripts={'--refs':'export_refs.py','--rotor-guide':'export_rotor_guide.py','--inspect':'inspect_sources.py','--build':'build.py','--install':'install.py','--verify':'verify.py','--finalize':'finalize.py'}
if len(sys.argv)!=2 or sys.argv[1]not in scripts:raise SystemExit('Use --refs, --build, --install, --verify, or --finalize for this boss update.')
subprocess.run([sys.executable,str(W/scripts[sys.argv[1]])],check=True)
