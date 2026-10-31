"""Rebuild HS53 authored spell art from archived GPT masters and native glass/head art."""
from pathlib import Path
import argparse,subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_08/miniboss/herald_spellcaster_1029';p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for b in m.values():b['sha256']=hashlib.sha256((R/b['path']).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/herald_spellcaster_art_1029.js').write_text('"use strict";\nconst HS53_ART='+json.dumps(m,separators=(',',':'))+';\n',encoding='utf8');print('Exported',len(m),'banks')
