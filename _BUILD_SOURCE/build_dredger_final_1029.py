"""Rebuild DF55 from the approved tank, toxic orb, ooze and ground Retina art."""
from pathlib import Path
import json,subprocess,argparse,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_07/miniboss/dredger_final_1029'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for b in m.values():b['sha256']=hashlib.sha256((R/b['path']).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/dredger_final_art_1029.js').write_text('"use strict";\nconst DF55_ART='+json.dumps(m,separators=(',',':'))+';\n',encoding='utf8');print('Exported',len(m),'banks')
