"""Rebuild fixed-cell Herald chaos art through Aseprite. Uses archived project sources."""
from pathlib import Path
import argparse,subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_08/miniboss/herald_chaos_1029'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
def data(name):
 s=(R/name).read_text(encoding='utf8');return json.JSONDecoder().raw_decode(s[s.index('{'):])[0]
(D/'inputs.json').write_text(json.dumps({'art':data('assets/encounter_revision_art_1027.js'),'parts':data('assets/herald_art_1003f.js')['parts']}))
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for bank in m.values():bank['sha256']=hashlib.sha256((R/bank['path']).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2))
(R/'assets/herald_chaos_art_1029.js').write_text('"use strict";\nconst HH52_ART='+json.dumps(m,separators=(',',':'))+';\n',encoding='utf8')
print('Authored banks:',len(m))
