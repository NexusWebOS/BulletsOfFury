"""Bake the actual allied aircraft/flame masters into fixed depth/shadow cells."""
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/riders_allied_overflight_1030';O=R/'assets/game/levels/stage_06/boss/riders_allied_overflight_1030'
p=argparse.ArgumentParser();p.add_argument('--aseprite',default=shutil.which('aseprite'));a=p.parse_args()
if not a.aseprite:raise SystemExit('Pass --aseprite with the installed Aseprite executable.')
subprocess.run([a.aseprite,'--batch','--script-param','work='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
pilots=sorted(set(q['pilot']for q in json.loads((D/'sources.json').read_text())));banks={};O.mkdir(parents=True,exist_ok=True)
for pilot in pilots:
 for role,n in [('hull',129),('shadow',43)]:
  name=pilot+'_'+role;f=O/(name+'.png');shutil.copy2(D/(name+'.png'),f);banks[name]=dict(key='rr66_'+name,path=f.relative_to(R).as_posix(),cw=128,ch=128,cols=12,frames=n,pivot=[64,64],sha256=hashlib.sha256(f.read_bytes()).hexdigest())
meta=dict(editor='Aseprite1.3.18.6-dev',banks=banks,heights=list(range(16,101,2)),phaseMs=70,duration=1.8)
(O/'manifest.json').write_text(json.dumps(meta,indent=2));(R/'assets/riders_allied_overflight_art_1030.js').write_text('"use strict";\nconst RR66_ART='+json.dumps(meta,separators=(',',':'))+';\n')
print('Rebuilt20 authored aircraft depth/shadow banks')
