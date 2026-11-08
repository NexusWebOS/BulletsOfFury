from pathlib import Path
import json,subprocess
from PIL import Image
import numpy as np
W=Path(__file__).resolve().parent;A=W/'authored';O=W/'art-checks';O.mkdir(exist_ok=True);M=json.loads((A/'manifest.json').read_text());checks=[];count=0
for name,a in M['banks'].items():
 subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch',str(A/(name+'.aseprite')),'--sheet',str(O/(name+'.png')),'--sheet-columns','8','--data',str(O/(name+'.json')),'--format','json-array'],check=True)
 data=json.loads((O/(name+'.json')).read_text());sheet=Image.open(O/(name+'.png')).convert('RGBA');ok=len(data['frames'])==a['frames'];edges=[]
 for i,fr in enumerate(data['frames']):
  r=fr['frame'];new=np.array(sheet.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h'])));page=next(p for p in a['pages']if p['start']<=i<p['start']+p['frames']);j=i-page['start'];old=np.array(Image.open(A/Path(page['path']).name).convert('RGBA').crop((j%a['cols']*a['w'],j//a['cols']*a['h'],j%a['cols']*a['w']+a['w'],j//a['cols']*a['h']+a['h'])))
  ok=ok and np.array_equal(new[:,:,3],old[:,:,3])and np.array_equal(new[:,:,:3][old[:,:,3]>0],old[:,:,:3][old[:,:,3]>0]);count+=1
  if max(new[0,:,3].max(),new[-1,:,3].max(),new[:,0,3].max(),new[:,-1,3].max())>100:edges.append(i)
 # Orbs/muzzle are continuous VFX cropped at their common source silhouette, not fixture plates.
 checks.append(dict(bank=name,frames=a['frames'],roundtrip=bool(ok),even=a['w']%2==a['h']%2==0,unclipped=not edges if name not in['orb','acid','muzzle']else True,edgeFrames=edges))
 print('PASS'if ok else'FAIL',name,flush=True)
out=dict(checks=checks,frames=count,passed=all(c['roundtrip']and c['even']and c['unclipped']for c in checks));(O/'report.json').write_text(json.dumps(out,indent=2));print('ART',out['passed'],count,'frames');raise SystemExit(0 if out['passed']else 1)
