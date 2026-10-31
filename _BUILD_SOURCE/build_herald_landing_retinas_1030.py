"""Re-export the source-authored Herald bomb Retina arrival frames."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/herald_landing_retinas_1030';O=R/'assets/game/levels/stage_08/miniboss/herald_landing_retinas_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
shutil.copy2(D/'retina.png',O/'retina.png');m=json.loads((O/'manifest.json').read_text());m['runtimeSha256']=hashlib.sha256((O/'retina.png').read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(m,indent=2));(D/'SOURCES.json').write_text(json.dumps(m,indent=2));print('Rebuilt24 fixed64x32 ground Retina fade/colour frames')
