from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/voss_turbo_1028';M=json.loads((D/'manifest.json').read_text());A=M['banks'];checks={}
body=Image.open(R/M['hullSource']).convert('RGBA');new=Image.open(D/'hull.png');cells=lambda im,f,cols:im.crop((f%cols*192,f//cols*192,f%cols*192+192,f//cols*192+192))
checks['actual72PlatesPreserved']=all(cells(body,f,16).tobytes()==cells(new,f,8).tobytes()for f in range(72))
checks['southBoostKeepsFixedPivot']=all(cells(new,72+f,8).tobytes()==cells(body,64+f,16).rotate(180,resample=Image.Resampling.NEAREST,center=(96,96)).tobytes()for f in range(8))
checks['sameAlphaForHitAndShadow']=all(Image.open(D/(n+'.png')).getchannel('A').tobytes()==new.getchannel('A').tobytes()for n in ['hull_hit','shadow'])
checks['evenRegisteredCells']=all(a['cw']%2==0 and a['ch']%2==0 and Image.open(R/a['path']).width%a['cw']==0 and Image.open(R/a['path']).height%a['ch']==0 for a in A.values())
sheet=Image.open(D/'orb.png');errors=[];alpha=True;source=R/'_ART_SOURCES/voss_turbo_1028';w=np.array([.2126,.7152,.0722])
for f in range(8):
 im=Image.open(source/f'florb_{f}.png').convert('RGBA');cell=sheet.crop((f%4*128,f//4*128,f%4*128+128,f//4*128+128));pad=Image.new('RGBA',(128,128));pad.paste(im,((128-im.width)//2,(128-im.height)//2));a=np.array(pad);b=np.array(cell);alpha=alpha and np.array_equal(a[:,:,3],b[:,:,3]);mask=a[:,:,3]>0;errors.extend(abs(a[:,:,:3].astype(float)@w-b[:,:,:3].astype(float)@w)[mask].tolist())
checks['paletteAlphaUnchanged']=alpha;checks['paletteLuminancePreserved']=max(errors)<1
checks['sourcesRetained']=hashlib.sha256((R/M['hullSource']).read_bytes()).hexdigest()==M['hullHash']and all(hashlib.sha256((source/(n+'.png')).read_bytes()).hexdigest()==h for n,h in M['sources'].items())
files=list(D.glob('*.png'))+[D/'manifest.json',R/'assets/voss_turbo_art_1028.js'];before={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in files};subprocess.run(['python',str(R/'_BUILD_SOURCE/build_voss_turbo_1028.py')],cwd=R,check=True,capture_output=True);checks['deterministicRebuild']=all(before[str(p)]==hashlib.sha256(p.read_bytes()).hexdigest()for p in files)
O=R/'_shots/voss_turbo_1028';(O/'art-checks.json').write_text(json.dumps(dict(checks=checks,maxLuminanceError=max(errors)),indent=2));print(checks);raise SystemExit(0 if all(checks.values())else 1)
