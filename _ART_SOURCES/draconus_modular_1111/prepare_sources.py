from pathlib import Path
from PIL import Image
import subprocess,json,numpy as np
W=Path(__file__).resolve().parent;E=W/'editable';E.mkdir(exist_ok=True)
for mat in ['regular','chrome']:
 for part in ['body','gun','grip']:
  Image.open(W/'exports'/f'{part}_{mat}.webp').save(E/f'{part}_{mat}.png')
exe=r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe'
ps="$a=Start-Process -FilePath '"+exe+"' -ArgumentList @('--batch','--script-param','out="+W.as_posix()+"','--script','"+(W/'author.lua').as_posix()+"') -WindowStyle Hidden -Wait -PassThru;exit $a.ExitCode"
q=subprocess.run(['powershell','-NoProfile','-Command',ps],capture_output=True,text=True)
(W/'aseprite-log.txt').write_text(q.stdout+q.stderr);assert q.returncode==0,q.stderr
checked=0
for mat in ['regular','chrome']:
 for layer,part in enumerate(['body','gun','grip'],1):
  source=Image.open(E/f'{part}_{mat}.png').convert('RGBA')
  result=Image.open(E/f'{mat}-layer-{layer}-roundtrip.png').convert('RGBA')
  for k in range(36):
   out=np.array(result.crop((k%4*512,k//4*512,k%4*512+512,k//4*512+512)))
   expected=Image.new('RGBA',(512,512))
   if part=='gun':
    expected.alpha_composite(source.crop((k%4*104,k//4*208,k%4*104+104,k//4*208+208)),(198,224))
   else:expected.alpha_composite(source)
   a=np.array(expected);mask=a[:,:,3]>0
   assert np.array_equal(a[:,:,3],out[:,:,3])and np.array_equal(a[mask],out[mask]),(mat,part,k)
   checked+=1
(W/'editable-verification.json').write_text(json.dumps(dict(materials=2,frames=72,layers=3,exactLayerFrames=checked,transparentRGBIgnored=True),indent=2))
print('Verified',checked,'exact editable layer frames across both 36-frame sources.',flush=True)
