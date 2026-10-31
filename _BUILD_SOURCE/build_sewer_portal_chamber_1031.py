"""Re-export approved PixelLab gates. No API calls, new generations or runtime art."""
from pathlib import Path
import argparse,json,subprocess,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_07/effects/portal_chamber_1031';p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args();I=json.loads((D/'inputs.json').read_text())
for bank in I['banks'].values():
 for f in bank['frames']:assert hashlib.sha256((R/f['path']).read_bytes()).hexdigest()==f['sha256']
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for bank in m.values():bank['sha256']=hashlib.sha256((R/bank['path']).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2));(R/'assets/sewer_portal_chamber_art_1031.js').write_text("'use strict';\nconst SC86_ART="+json.dumps(m,separators=(',',':'))+';\n')
A=R/'_ART_SOURCES/sewer_portal_chamber_1031';A.mkdir(parents=True,exist_ok=True)
for f in D.glob('*.aseprite'):shutil.copy2(f,A/f.name)
print('Exported177 fixed-cell frames,7 editable banks')
