"""Re-export Herald's source-authored tornado lifecycle and lightning feedback."""
from pathlib import Path
import argparse,subprocess,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/herald_storm_1030';O=R/'assets/game/levels/stage_08/miniboss/herald_storm_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for n,v in m.items():shutil.copy2(D/(n+'.png'),O/(n+'.png'));v['sha256']=hashlib.sha256((O/(n+'.png')).read_bytes()).hexdigest()
(O/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/herald_storm_art_1030.js').write_text("'use strict';\nconst HH69_ART="+json.dumps(m,separators=(',',':'))+';\n')
print('Rebuilt tornado fade/flash, summon lightning and metal warning banks')
