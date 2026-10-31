"""Re-export Herald's red claw laser/muzzle frames through Aseprite."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/herald_claw_lasers_1030';O=R/'assets/game/levels/stage_08/miniboss/herald_claw_lasers_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((O/'manifest.json').read_text())
for n in ['projectile','muzzle']:
 shutil.copy2(D/(n+'.png'),O/(n+'.png'));m['banks'][n]=hashlib.sha256((O/(n+'.png')).read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(m,indent=2));(D/'SOURCES.json').write_text(json.dumps(m,indent=2))
print('Rebuilt8-phase64-direction red lasers and larger muzzle frames')
