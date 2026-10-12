"""Own the October 11 generated loose plates; measured pivots, even exports."""
from pathlib import Path
from PIL import Image
import numpy as np, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/playthrough_1011'
OUT=ROOT/'assets/game/shared/combat/playthrough_1011';OUT.mkdir(parents=True,exist_ok=True)
manifest={}
def write(name,i,im,pivot,extra):
    assert im.width%2==im.height%2==0
    path=OUT/f'{name}_{i:02d}.png';im.save(path,optimize=True)
    return dict(key=f'pt11_{name}_{i}',path=path.relative_to(ROOT).as_posix(),w=im.width,h=im.height,pivot=list(pivot),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**extra)
raw=Image.open(SRC/'returned/ice-kit-v1.png').convert('RGBA')
# Measured part windows, not guessed equal cells: generation gave the hull a wider bay.
rects=[(0,0,806,616),(814,24,296,586),(1210,24,266,586),(240,644,332,342),(736,646,252,316),(1198,646,252,316)]
pivots=[(400,302),(62,136),(208,138),(162,166),(122,142),(120,142)]
manifest['ice_parts']=[]
for i,(x,y,w,h) in enumerate(rects):
    im=raw.crop((x,y,x+w,y+h));manifest['ice_parts'].append(write('ice_parts',i,im,pivots[i],dict(sourceRect=[x,y,w,h],source='ice-kit-v1.png')))
raw=Image.open(SRC/'returned/hammer-core-raise-v1.png').convert('RGBA')
sw,sh=raw.width/4,raw.height/4
centers=[(164,108),(478,108),(790,108),(1104,108),(164,420),(478,420),(790,420),(1104,420),
         (164,735),(481,735),(797,735),(1113,739),(176,1088),(490,1088),(804,1088),(1118,1088)]
bank=[];scale=1.20;pivot=(256,224)
hammer_ys=[0,318,618,922,1254]
for i,(cx,cy) in enumerate(centers):
    x,x1=round(i%4*sw),round((i%4+1)*sw)
    y,y1=hammer_ys[i//4:i//4+2]
    cell=raw.crop((x,y,x1,y1));size=(round(cell.width*scale),round(cell.height*scale))
    dx,dy=round(pivot[0]-(cx-x)*scale),round(pivot[1]-(cy-y)*scale)
    out=Image.new('RGBA',(512,512));out.alpha_composite(cell.resize(size,Image.Resampling.NEAREST),(dx,dy))
    oa=np.asarray(out)[:,:,3]
    assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<100,(i,'clipped hammer')
    bank.append(write('hammer_core',i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source='hammer-core-raise-v1.png',scale=scale,physicalAnchor=[cx,cy])))
manifest['hammer_core']=bank
raw=Image.open(SRC/'returned/furnace-head-v1.png').convert('RGBA')
bank=[];scale=.72;pivot=(128,96);sw,sh=raw.width/4,raw.height/4
furnace_ys=[0,318,628,932,1254]
for i in range(16):
    x,x1=round(i%4*sw),round((i%4+1)*sw)
    y,y1=furnace_ys[i//4:i//4+2]
    cell=raw.crop((x,y,x1,y1));a=np.asarray(cell);yy,xx=np.indices(a.shape[:2])
    # Forehead lens alone: the unchanged physical socket, not changing fire bounds.
    mask=(xx>cell.width*.39)&(xx<cell.width*.63)&(yy>cell.height*.23)&(yy<cell.height*.45)&(a[:,:,0]>225)&(a[:,:,1]>160)&(a[:,:,3]>150)
    cx=float(xx[mask].mean());cy=float(yy[mask].mean())
    out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST),(round(pivot[0]-cx*scale),round(pivot[1]-cy*scale)))
    oa=np.asarray(out)[:,:,3]
    assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<100,(i,'clipped furnace head')
    bank.append(write('furnace_head',i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source='furnace-head-v1.png',scale=scale,physicalAnchor=[round(cx+x,2),round(cy+y,2)])))
manifest['furnace_head']=bank
raw=Image.open(SRC/'returned/harrier-cannon-v1.png').convert('RGBA')
bank=[];scale=.72;pivot=(80,44)
for i in range(16):
    x,y,x1,y1=round(i%4*raw.width/4),round(i//4*raw.height/4),round((i%4+1)*raw.width/4),round((i//4+1)*raw.height/4)
    cell=raw.crop((x,y,x1,y1));a=np.asarray(cell);yy,xx=np.indices(a.shape[:2])
    mask=(xx>cell.width*.30)&(xx<cell.width*.63)&(yy>cell.height*.06)&(yy<cell.height*.31)&(a[:,:,0]<120)&(a[:,:,1]>135)&(a[:,:,2]>145)&(a[:,:,3]>140)
    assert mask.sum()>12,(i,'missing cannon hinge')
    cx,cy=float(xx[mask].mean()),float(yy[mask].mean())
    out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST),(round(pivot[0]-cx*scale),round(pivot[1]-cy*scale)))
    oa=np.asarray(out)[:,:,3]
    assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<100,(i,'clipped cannon')
    bank.append(write('harrier_cannon',i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source='harrier-cannon-v1.png',scale=scale,physicalAnchor=[round(cx+x,2),round(cy+y,2)])))
manifest['harrier_cannon']=bank
raw=Image.open(SRC/'returned/ice-jets-v2.png').convert('RGBA')
# Eight separated rows were drawn with unequal gutters. Mid-gutter boundaries
# keep the entire exhaust/nose rather than imposing a grid across their ink.
ys=[0,258,470,683,894,1120,1335,1553,1774]
for name,first in [('ice_jet_a',0),('ice_jet_b',4)]:
    bank=[];scale=1.0;pivot=(128,186)
    for i in range(16):
        row=first+i//4;x=round(i%4*raw.width/4);x1=round((i%4+1)*raw.width/4);y,y1=ys[row:row+2]
        cell=raw.crop((x,y,x1,y1));a=np.asarray(cell);yy,xx=np.indices(a.shape[:2])
        mask=(xx>cell.width*.35)&(xx<cell.width*.65)&(yy>cell.height*.52)&(yy<cell.height*.94)&(a[:,:,0]<120)&(a[:,:,1]>170)&(a[:,:,2]>170)&(a[:,:,3]>150)
        assert mask.sum()>20,(name,i)
        cx=float(xx[mask].mean());cy=float(yy[mask].mean())
        dx,dy=round(pivot[0]-cx),round(pivot[1]-cy)
        out=Image.new('RGBA',(256,256));out.alpha_composite(cell,(dx,dy))
        oa=np.asarray(out)[:,:,3]
        assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<100,(name,i,'clipped ink')
        bank.append(write(name,i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source='ice-jets-v2.png',scale=scale,physicalAnchor=[round(cx+x,2),round(cy+y,2)])))
    manifest[name]=bank
for name,source,scale,pivot in [('black_heart','black-heart-v1.png',.72,(128,144)),('fire_wave','furnace-wave-v2.png',.80,(128,160))]:
    raw=Image.open(SRC/'returned'/source).convert('RGBA');bank=[]
    for i in range(16):
        x,y,x1,y1=round(i%4*raw.width/4),round(i//4*raw.height/4),round((i%4+1)*raw.width/4),round((i//4+1)*raw.height/4)
        cell=raw.crop((x,y,x1,y1));a=np.asarray(cell);yy,xx=np.indices(a.shape[:2])
        roi=(xx>cell.width*.42)&(xx<cell.width*.58)&(yy>cell.height*.43)&(yy<cell.height*.78)&(a[:,:,3]>150)
        mask=roi&(a[:,:,0]>(160 if name=='black_heart' else 240))&((a[:,:,1]<70)&(a[:,:,2]<100) if name=='black_heart' else (a[:,:,1]>225)&(a[:,:,2]>150))
        assert mask.sum()>8,(name,i,'missing physical pupil/hotspot')
        cx,cy=float(xx[mask].mean()),float(yy[mask].mean())
        out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST),(round(pivot[0]-cx*scale),round(pivot[1]-cy*scale)))
        oa=np.asarray(out)[:,:,3]
        assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<100,(name,i,'clipped ink')
        bank.append(write(name,i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source=source,scale=scale,physicalAnchor=[round(cx+x,2),round(cy+y,2)])))
    manifest[name]=bank
raw=Image.open(SRC/'returned/drone-raise-v1.png').convert('RGBA')
bank=[];scale=.72;pivot=(160,160)
# The source rows are separated by uneven gutters. A uniform 4x4 cut
# includes the next row's raised claws and clips the current upper hands.
drone_ys=[0,334,594,870,1254]
for i in range(16):
    x,x1=round(i%4*raw.width/4),round((i%4+1)*raw.width/4)
    y,y1=drone_ys[i//4:i//4+2]
    cell=raw.crop((x,y,x1,y1));a=np.asarray(cell);yy,xx=np.indices(a.shape[:2])
    mask=(xx>cell.width*.35)&(xx<cell.width*.65)&(a[:,:,1]>80)&(a[:,:,1]>a[:,:,0]*1.6)&(a[:,:,1]>a[:,:,2]*1.6)&(a[:,:,3]>150)
    assert mask.sum()>15,(i,'missing green eye anchor')
    cx,cy=float(xx[mask].mean()),float(yy[mask].mean())
    out=Image.new('RGBA',(320,320));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST),(round(pivot[0]-cx*scale),round(pivot[1]-cy*scale)))
    oa=np.asarray(out)[:,:,3]
    assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<100,(i,'clipped drone')
    bank.append(write('drone_raise',i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source='drone-raise-v1.png',scale=scale,physicalAnchor=[round(cx+x,2),round(cy+y,2)])))
manifest['drone_raise']=bank
for name,source,scale,size,pivot in [
    ('fire_spray','fire-spray-v1.png',.76,(160,320),(80,300)),
    ('sonic_pulse','sonic-pulse-v1.png',.32,(128,128),(64,100))]:
    raw=Image.open(SRC/'returned'/source).convert('RGBA');bank=[]
    for i in range(16):
        x,y,x1,y1=round(i%4*raw.width/4),round(i//4*raw.height/4),round((i%4+1)*raw.width/4),round((i//4+1)*raw.height/4)
        cell=raw.crop((x,y,x1,y1));a=np.asarray(cell);yy,xx=np.indices(a.shape[:2])
        # The nozzle (fire) / lower pressure ridge (sonic) is a physical origin.
        # Expanding tips do not move this anchor or change the shared scale.
        solid=(a[:,:,3]>180)&(xx>cell.width*.30)&(xx<cell.width*.70)
        rows=np.where(solid.any(axis=1))[0];assert len(rows)
        cy=int(rows[-1]);base=solid&(yy>=cy-8)
        cx=float(xx[base].mean())
        out=Image.new('RGBA',size)
        out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST),
                            (round(pivot[0]-cx*scale),round(pivot[1]-cy*scale)))
        oa=np.asarray(out)[:,:,3];assert max(oa[0].max(),oa[-1].max(),oa[:,0].max(),oa[:,-1].max())<25,(name,i,'clipped weapon')
        ink=np.asarray(out)[:,:,3]>100;iy,ix=np.where(ink)
        bands=[]
        if name=='fire_spray':
            for row in range(0,size[1],8):
                sy,sx=np.where(oa[row:row+8]>160)
                if len(sx):bands.append([row+int(sy.min()),row+int(sy.max())+1,int(sx.min()),int(sx.max())+1])
        bank.append(write(name,i,out,pivot,dict(sourceRect=[x,y,x1-x,y1-y],source=source,scale=scale,
                    physicalAnchor=[round(cx+x,2),cy+y],ink=[int(ix.min()),int(iy.min()),int(ix.max()+1),int(iy.max()+1)],hitBands=bands)))
    # Stable visual length is measured once for the bank, never fitted per pose.
    length=max(pivot[1]-q['ink'][1] for q in bank)
    for q in bank:q['length']=length
    manifest[name]=bank
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(ROOT/'assets/playthrough_art_1011.js').write_text('"use strict";\n// Owned by build_playthrough_art_1011.py.\nconst PT11_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Registered',sum(len(b) for b in manifest.values()),'even cells. Whole strip scales and physical pivots retained.')
