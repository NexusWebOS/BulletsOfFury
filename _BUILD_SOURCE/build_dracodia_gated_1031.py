"""Re-export actual PixelLab mechanical purple/red gates. No service/API calls."""
from pathlib import Path
import argparse,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_08/effects/gated_possession_1031'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args();I=json.loads((D/'inputs.json').read_text())
for bank in I['banks'].values():
 for f in bank['frames']:assert hashlib.sha256((R/f['path']).read_bytes()).hexdigest()==f['sha256']
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for n,v in m.items():v['sha256']=hashlib.sha256((D/(n+'.png')).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/dracodia_gated_art_1031.js').write_text("'use strict';\nconst RD94_ART="+json.dumps(m,separators=(',',':'))+';\n')
print('Rebuilt',sum(v['frames']for v in m.values()),'fixed-cell gated frames and six Aseprite banks')
