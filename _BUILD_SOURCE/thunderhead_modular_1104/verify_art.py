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
  if name not in ['wind_beam']and max(a[0,:,3].max(),a[-1,:,3].max(),a[:,0,3].max(),a[:,-1,3].max())>64:clipped.append(i)
 # Grade/rain are intentional edge-to-edge tiles; bolt continues off the top.
 checks.append({'name':name,'roundtrip':bool(ok),'unclipped':not clipped,'edgeFrames':clipped,'frames':b['frames'],'size':[b['cw'],b['ch']]})
 print('PASS'if ok and not clipped else'FAIL',name,flush=True)
pages={};packed=True;mask_ok=True;mask_count=0;raw=(R/M['maskPath']).read_bytes()
for name,b in M['banks'].items():
 for i,c in enumerate(b['cells']):
  if c[0]not in pages:pages[c[0]]=Image.open(R/M['pages'][c[0]]['path']).convert('RGBA')
  im=pages[c[0]].crop((c[1],c[2],c[1]+b['cw'],c[2]+b['ch']));s=np.array(Image.open(A/'frames'/name/(str(i).zfill(3)+'.png')).convert('RGBA'));a=np.array(im)
  packed=packed and np.array_equal(a[:,:,3],s[:,:,3])and np.array_equal(a[:,:,:3][s[:,:,3]>0],s[:,:,:3][s[:,:,3]>0])
  if name in M['masks']:
   x,y,w,h,off=M['masks'][name][i];bits=np.unpackbits(np.frombuffer(raw[off:off+(w*h+7)//8],dtype='uint8'),bitorder='little')[:w*h].reshape(h,w);mask_ok=mask_ok and np.array_equal(bits,s[y:y+h,x:x+w,3]>80);mask_count+=1
out={'checks':checks,'frames':frames,'runtimePacking':bool(packed),'collisionMasks':{'passed':bool(mask_ok),'count':mask_count},'passed':all(c['roundtrip']and c['unclipped']for c in checks)and packed and mask_ok,'sources':'Real Aseprite batch re-export; exact visibleRGBA/alpha compared with runtime atlas cells and source-derived collision masks.'};(O/'report.json').write_text(json.dumps(out,indent=2));print('ASEPRITE_ROUNDTRIP',out['passed'],frames,'frames',len(checks),'banks','MASKS',mask_count);raise SystemExit(0 if out['passed']else 1)
