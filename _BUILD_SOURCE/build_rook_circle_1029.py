from pathlib import Path
import subprocess,argparse,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/rook_circle_1029'
p=argparse.ArgumentParser();p.add_argument('--aseprite',required=True);a=p.parse_args()
subprocess.run([a.aseprite,'--batch','--script-param','root='+R.as_posix(),'--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
m=json.loads((D/'manifest.json').read_text())
for b in m['banks'].values():b['sha256']=hashlib.sha256((D/b['file']).read_bytes()).hexdigest()
(D/'manifest.json').write_text(json.dumps(m,indent=2))
