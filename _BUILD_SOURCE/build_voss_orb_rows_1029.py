"""Rebuild Voss's authored fixed-cell spin/glow and hit banks in Aseprite."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/voss_orb_rows_1029'
p=argparse.ArgumentParser();p.add_argument('--aseprite',default=shutil.which('aseprite'));args=p.parse_args()
if not args.aseprite:raise SystemExit('Pass --aseprite with your installed Aseprite executable.')
subprocess.run([args.aseprite,'--batch','--script-param','work='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text());m['sha256']=hashlib.sha256((D/'orb_rows.png').read_bytes()).hexdigest();(D/'manifest.json').write_text(json.dumps(m,indent=2))
print('Rebuilt Voss orb source,64 fixed cells and provenance hash.')
