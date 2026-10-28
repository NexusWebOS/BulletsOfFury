from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_07/miniboss/dredger_assault_1028';S=R/'_ART_SOURCES/dredger_1028'
checks={};M=json.loads((D/'manifest.json').read_text());A=M['banks']
checks['evenFixedCanvases']=all(a['cw']%2==0 and a['ch']%2==0 and Image.open(R/a['path']).width%a['cw']==0 and Image.open(R/a['path']).height%a['ch']==0 for a in A.values())
source=np.array(Image.open(S/'body.png'));body=np.array(Image.open(D/'body.png'))
mask=np.zeros((192,176),bool)
for x,y,w,h in A['body']['treadBands']:mask[y:y+h,x:x+w]=True
checks['restHullMatchesActualExport']=np.array_equal(source,body[:,:176])
checks['OnlyTreadPixelsMove']=all(np.array_equal(body[:,f*176:(f+1)*176][~mask],source[~mask])for f in range(8))
checks['TrackPhasesAreDistinct']=len({hashlib.sha256(body[:,f*176:(f+1)*176].tobytes()).hexdigest()for f in range(8)})==8
checks['hitCompanionsRetainExactAlpha']=all(np.array_equal(np.array(Image.open(D/(n+'.png')))[:,:,3],np.array(Image.open(D/(n+'_hit.png')))[:,:,3])for n in ['body','gun','top'])
checks['topPreservesActualSourcePixels']=np.array_equal(np.array(Image.open(S/'top.png')),np.array(Image.open(D/'top.png')))
guns=np.array(Image.open(D/'gun.png'));margin=[]
for f in range(256):
 c=guns[f//8*112:(f//8+1)*112,f%8*112:(f%8+1)*112];y,x=np.nonzero(c[:,:,3]);margin.append(min(x.min(),y.min(),111-x.max(),111-y.max()))
checks['NoHeadingOrRecoilIsClipped']=min(margin)>=3
checks['FourDistinctMuzzleChannels']=all(len(row)==2 and abs(row[0][0]-row[1][0])+abs(row[0][1]-row[1][1])>20 for row in A['gun']['sockets'])
checks['SourcesMatchRecordedHashes']=all(hashlib.sha256((S/n).read_bytes()).hexdigest()==h for n,h in M['sources'].items())
files=list(D.glob('*.png'))+[D/'manifest.json',R/'assets/dredger_assault_art_1028.js'];before={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}
subprocess.run(['python',str(R/'_BUILD_SOURCE/build_dredger_assault_1028.py')],check=True,cwd=R,capture_output=True)
checks['OwningBuilderReproducesAllOutputs']=all(hashlib.sha256(p.read_bytes()).hexdigest()==before[str(p)]for p in files)
checks={n:bool(v)for n,v in checks.items()}
O=R/'_shots/dredger_assault_1028';O.mkdir(exist_ok=True);(O/'art-checks.json').write_text(json.dumps(dict(checks=checks,minimumTransparentMargin=int(min(margin))),indent=2))
for n,v in checks.items():print(('PASS 'if v else'FAIL ')+n)
raise SystemExit(0 if all(checks.values())else 1)
