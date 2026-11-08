from pathlib import Path
from PIL import Image
import numpy as np
import json,subprocess,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');A=W/'authored';M=json.loads((A/'manifest.json').read_text());O=W/'art-roundtrip';O.mkdir(exist_ok=True);checks=[];frames=0
for name,b in M['banks'].items():
 png=O/(name+'.png');data=O/(name+'.json')
 subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch',str(A/(name+'.aseprite')),'--sheet',str(png),'--sheet-columns','8','--data',str(data),'--format','json-array'],check=True)
 j=json.loads(data.read_text());sheet=Image.open(png).convert('RGBA');ok=len(j['frames'])==b['frames'];clipped=[]
 for i,frame in enumerate(j['frames']):
  r=frame['frame'];im=sheet.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h']));source=Image.open(A/'frames'/name/(str(i).zfill(3)+'.png')).convert('RGBA');a=np.array(im);s=np.array(source)
  # Fully transparent RGB is irrelevant; visible colour and exact alpha are not.
  ok=ok and a.shape==s.shape and np.array_equal(a[:,:,3],s[:,:,3])and np.array_equal(a[:,:,:3][s[:,:,3]>0],s[:,:,:3][s[:,:,3]>0]);frames+=1
  if name not in ['grade','rain','bolt','core']and max(a[0,:,3].max(),a[-1,:,3].max(),a[:,0,3].max(),a[:,-1,3].max())>64:clipped.append(i)
 # Grade/rain are intentional edge-to-edge tiles; bolt continues off the top.
 checks.append({'name':name,'roundtrip':bool(ok),'unclipped':not clipped,'edgeFrames':clipped,'frames':b['frames'],'size':[b['cw'],b['ch']]})
 print('PASS'if ok and not clipped else'FAIL',name,flush=True)
out={'checks':checks,'frames':frames,'passed':all(c['roundtrip']and c['unclipped']for c in checks),'sources':'Real Aseprite batch re-export; exact visibleRGBA and alpha compared with runtime frame inputs.'};(O/'report.json').write_text(json.dumps(out,indent=2));print('ASEPRITE_ROUNDTRIP',out['passed'],frames,'frames',len(checks),'banks');raise SystemExit(0 if out['passed']else 1)
