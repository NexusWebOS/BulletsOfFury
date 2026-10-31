"""Rebuild authored Rough Riders defense/warning source cells with Aseprite."""
from pathlib import Path
import argparse,subprocess,shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/riders_defense_1029'
p=argparse.ArgumentParser();p.add_argument('--aseprite',default=shutil.which('aseprite'));a=p.parse_args()
if not a.aseprite:raise SystemExit('Pass --aseprite with your installed Aseprite executable.')
subprocess.run([a.aseprite,'--batch','--script-param','work='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for k,v in m['banks'].items():v['sha256']=hashlib.sha256((D/(k+'.png')).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2));print('Rebuilt authored defense and warning banks.')
