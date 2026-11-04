from pathlib import Path
from PIL import Image
import json,hashlib
W=Path('BOF-StageX-Box-Rotation-1104');R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');im=Image.open(W/'power_turn_64.png').convert('RGBA');masks=[];Q=[];centres=[]
for n in range(16):
 a=im.crop((n*64,0,(n+1)*64,64));b=im.crop(((n+16)*64,0,(n+17)*64,64));mask=a.getchannel('A').tobytes();masks.append(mask);box=a.getbbox();centres.append([(box[0]+box[2])/2,(box[1]+box[3])/2]);Q.append({'name':'pose'+str(n)+' matching hit silhouette','ok':mask==b.getchannel('A').tobytes()});Q.append({'name':'pose'+str(n)+' complete boundary','ok':all(a.getpixel(p)[3]==0 for p in [(i,0)for i in range(64)]+[(i,63)for i in range(64)]+[(0,i)for i in range(64)]+[(63,i)for i in range(64)])})
Q.append({'name':'16 distinct yaw silhouettes','ok':len(set(masks))==16});Q.append({'name':'fixed64px32cell strip','ok':im.size==(2048,64)});Q.append({'name':'pivot alignment within one pixel','ok':all(abs(c[0]-32)<=1 and abs(c[1]-32)<=1 for c in centres)})
B=json.loads((W/'speed-before.json').read_text());Q.append({'name':'speed pill artwork unchanged','ok':all(hashlib.sha256((R/'assets/game/levels/stage_06/pickups/stagex_1104'/n).read_bytes()).hexdigest()==h for n,h in B.items())});(W/'asset-qa.json').write_text(json.dumps({'checks':Q,'centres':centres},indent=2),encoding='utf8');print(len(Q),'checks; failed',[q for q in Q if not q['ok']])
