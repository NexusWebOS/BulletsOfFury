"""Apply reviewed hardware apertures without changing any atlas cells or images."""
from pathlib import Path
from PIL import Image
import json

def apply(assets, banks, repo):
    review=json.loads((repo/'expansion/topdown/art/combat39/socket_review41.json').read_text())
    count=0
    for bank, seed in review['banks'].items():
        for key in banks[bank]['frames']:
            m=assets[key];x,y,w,h=m['rect']
            cell=Image.open(repo/m['file']).convert('RGBA').crop((x,y,x+w,y+h))
            points=[]
            for yy in range(max(0,seed[1]-4),min(h,seed[1]+5)):
                for xx in range(max(0,seed[0]-4),min(w,seed[0]+5)):
                    r,g,b,a=cell.getpixel((xx,yy))
                    if a<180 or max(r,g,b)>220 or max(r,g,b)-min(r,g,b)>65:continue
                    points.append(((xx-seed[0])**2+(yy-seed[1])**2,xx,yy))
            # A bright baked flare can cover the hardware completely. Its
            # reviewed aperture stays in place rather than following the flare.
            _,xx,yy=min(points) if points else (0,*seed)
            m['muzzle']=[xx,yy];m['muzzleReview']='socket_review41';count+=1
    return count

if __name__=='__main__':
    repo=Path(__file__).resolve().parents[3]
    folder=repo/'expansion/topdown/art/combat39'
    p=json.loads((folder/'manifest.json').read_text())
    count=apply(p['assets'],p['banks'],repo)
    (folder/'manifest.json').write_text(json.dumps(p,indent=2))
    (folder/'manifest.js').write_text('window.TD_COMBAT39_ART='+json.dumps(p,separators=(',',':'))+';Object.assign(window.TD_ASSAULT_ART.assets,window.TD_COMBAT39_ART.assets);\n')
    print(f'Registered {count} reviewed per-frame hardware sockets; sprite pixels unchanged')
