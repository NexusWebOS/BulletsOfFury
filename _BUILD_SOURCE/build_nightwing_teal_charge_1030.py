"""Re-export Nightwing's smaller vortex and source-contour teal charge in Aseprite."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/nightwing_teal_charge_1030';O=R/'assets/game/levels/stage_06/boss/nightwing_teal_charge_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',default=shutil.which('aseprite'));a=p.parse_args()
if not a.aseprite:raise SystemExit('Pass --aseprite with the installed Aseprite executable.')
subprocess.run([a.aseprite,'--batch','--script-param','work='+D.as_posix(),'--script-param','root='+R.as_posix(),'--script',str(D/'author.lua')],check=True)
O.mkdir(parents=True,exist_ok=True);m=json.loads((O/'manifest.json').read_text())
for k,b in m['banks'].items():
 f=O/(k+'.png');shutil.copy2(D/f.name,f);b['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(m,indent=2));print('Rebuilt24+24 wind phases and18 teal aura poses')
