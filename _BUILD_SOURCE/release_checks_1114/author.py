from pathlib import Path
from PIL import Image
import subprocess,json,numpy as np
W=Path(__file__).resolve().parent;exe=r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
help=subprocess.run([exe,'--help'],capture_output=True,text=True);(W/'aseprite-help.txt').write_text(help.stdout+help.stderr);assert help.returncode==0
ps="$a=Start-Process -FilePath '"+exe+"' -ArgumentList @('--batch','--script-param','out="+W.as_posix()+"','--script','"+(W/'author.lua').as_posix()+"') -WindowStyle Hidden -Wait -PassThru;exit $a.ExitCode"
q=subprocess.run(['powershell','-NoProfile','-Command',ps],capture_output=True,text=True);(W/'aseprite-log.txt').write_text(q.stdout+q.stderr);assert q.returncode==0,q.stderr
M=json.loads((W/'author-manifest.json').read_text())['banks'];count=0
for n,a in M.items():
 expected=np.array(Image.open(W/'exports'/(n+'.webp')).convert('RGBA'));actual=np.array(Image.open(W/'exports'/(n+'_roundtrip.png')).convert('RGBA'));mask=expected[:,:,3]>0
 assert np.array_equal(expected[:,:,3],actual[:,:,3])and np.array_equal(expected[mask],actual[mask]),n
 count+=a['count']
(W/'editable-verification.json').write_text(json.dumps(dict(banks=len(M),exactFrames=count,errors=[]),indent=2));print('Editable Aseprite roundtrip exact:',count,'frames in',len(M),'banks.',flush=True)
