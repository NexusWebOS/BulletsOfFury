"""Re-export the source-authored Golden Aegis grid using Aseprite."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/riders_flight_grid_1030';O=R/'assets/game/levels/stage_06/boss/riders_flight_grid_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',default=shutil.which('aseprite'));a=p.parse_args()
if not a.aseprite:raise SystemExit('Pass --aseprite with the installed Aseprite executable.')
subprocess.run([a.aseprite,'--batch','--script-param','work='+D.as_posix(),'--script',str(D/'author_grid.lua')],check=True)
O.mkdir(parents=True,exist_ok=True);shutil.copy2(D/'gold_grid.png',O/'gold_grid.png')
m=json.loads((O/'manifest.json').read_text());m['sha256']=hashlib.sha256((O/'gold_grid.png').read_bytes()).hexdigest();(O/'manifest.json').write_text(json.dumps(m,indent=2))
print('Rebuilt40 authored fixed480x64 force-field grid cells')
