"""Cut authored Wind reels with one proportional scale and fixed physical pivots."""
from pathlib import Path
from PIL import Image
import numpy as np
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/wind_projectiles_1011'
DEST=ROOT/'assets/game/shared/player_weapons/wind_1011'
FAMILIES=['bullets','spread','missile','laser','gust','tornado','mist','heavy','electric']
NAMES=['Gale Slugs','Gust Fan','Cyclone Rack','Wind Lance','Gust Torrent','Tornado Orb','Storm Mist','Gale Gatling','Cyclone Sphere']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def components(mask):
    """Measure a physical metal component, excluding disconnected energy sparks."""
    todo=set(map(tuple,np.argwhere(mask)));parts=[]
    while todo:
        seed=todo.pop();part=[seed];stack=[seed]
        while stack:
            y,x=stack.pop()
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]:
                nxt=(y+dy,x+dx)
                if nxt in todo:todo.remove(nxt);stack.append(nxt);part.append(nxt)
        if len(part)>8:parts.append(part)
    return parts

def largest(mask):
    best=max(components(mask),key=len)
    assert len(best)>16,'No physical projectile component'
    q=np.array(best);return [int(q[:,1].min()),int(q[:,0].min()),int(q[:,1].max()+1),int(q[:,0].max()+1)]

def anchor(cell,family):
    p=np.asarray(cell).astype('int16');h,w=p.shape[:2];r,g,b,a=[p[:,:,i] for i in range(4)]
    if family in ['bullets','spread','missile','heavy','electric','gust']:
        m=(a>160)&(r>30)&(r<210)&(abs(g-r)<16)&(abs(b-r)<32)
        m[:,:int(w*.25)]=False;m[:,int(w*.75):]=False
        if family=='gust':m[:int(h*.62)]=False
        elif family=='electric':m[:int(h*.22)]=False;m[int(h*.78):]=False
        else:m[int(h*.66):]=False
        bb=largest(m)
        return [(bb[0]+bb[2])/2,(bb[1]+bb[3])/2],bb
    bright=(a>180)&(r>215)&(g>230)&(b>190)
    bright[:,:int(w*.35)]=False;bright[:,int(w*.65):]=False
    if family=='tornado':
        parts=components(bright)
        # The small white eye is separate from the broad surrounding ribbon.
        part=min(parts,key=lambda q:((np.mean(q,axis=0)-[h*.49,w*.49])**2).sum())
        yy,xx=np.mean(part,axis=0);return [float(xx),float(yy)],None
    if family=='laser':
        # The white centerline and its lower flare are the held beam's mounting point.
        bright[:int(h*.70)]=False;bright[int(h*.92):]=False
    elif family=='mist':bright[:int(h*.36)]=False;bright[int(h*.68):]=False
    else:bright[:int(h*.34)]=False;bright[int(h*.66):]=False
    sums=bright.sum(axis=1);peak=int(sums.max());assert peak>2,family
    candidates=np.where(sums>=peak*.85)[0];groups=np.split(candidates,np.where(np.diff(candidates)>1)[0]+1)
    rows=min(groups,key=lambda q:abs(float(q.mean())-h*(.83 if family=='laser' else .56)))
    y=float(rows.mean());xs=np.where(bright[rows].any(axis=0))[0]
    return [float(xs.mean()),y],None

def lock_orb_core(items,family):
    """Register the unchanged eye/globe texture, not moving peripheral ribbons."""
    first=items[0];center=np.array(first['pos'])
    offset=np.array([0,0]) if family=='tornado' else np.array([-18,-24])
    seed=np.round(center+offset).astype('int');half=14
    ref=np.asarray(first['cell'],dtype='float32')[seed[1]-half:seed[1]+half,seed[0]-half:seed[0]+half,:3][::2,::2]
    for q in items:
        pixels=np.asarray(q['cell'],dtype='float32');bb=q['bb'];expected=np.array([(bb[0]+bb[2])/2,(bb[1]+bb[3])/2])+offset
        best=(float('inf'),None)
        for yy in range(max(half,round(expected[1]-72)),min(pixels.shape[0]-half,round(expected[1]+72)),2):
            for xx in range(max(half,round(expected[0]-72)),min(pixels.shape[1]-half,round(expected[0]+72)),2):
                patch=pixels[yy-half:yy+half:2,xx-half:xx+half:2,:3]
                score=float(np.mean((patch-ref)**2))
                if score<best[0]:best=(score,[xx,yy])
        _,pos=best
        # Refine the coarse alignment at full pixel precision.
        for yy in range(pos[1]-1,pos[1]+2):
            for xx in range(pos[0]-1,pos[0]+2):
                patch=pixels[yy-half:yy+half:2,xx-half:xx+half:2,:3]
                score=float(np.mean((patch-ref)**2))
                if score<best[0]:best=(score,[xx,yy])
        q['pos']=[float(best[1][0]-offset[0]),float(best[1][1]-offset[1])]

def add_wind_projectiles(manifest):
    DEST.mkdir(parents=True,exist_ok=True);audit={};all_banks={}
    for slot,family in enumerate(FAMILIES):
        source=SOURCE/(family+'_raw.png');im=Image.open(source).convert('RGBA');W,H=im.size
        items=[]
        for i in range(16):
            c,r=i%4,i//4;rect=[round(c*W/4),round(r*H/4),round((c+1)*W/4),round((r+1)*H/4)]
            cell=im.crop(rect);p=np.asarray(cell).copy();p[p[:,:,3]<=20]=0;cell=Image.fromarray(p)
            bb=Image.fromarray((p[:,:,3]>80).astype('uint8')*255).getbbox();assert bb,(family,i)
            pos,metal=anchor(cell,family);items.append(dict(cell=cell,rect=rect,bb=bb,pos=pos,metal=metal))
        if family in ['tornado','electric','mist']:lock_orb_core(items,'tornado' if family=='mist' else family)
        # Lock the solid nose/top rather than an animated wake. One body span for the whole bank.
        if family in ['bullets','spread','missile','heavy']:
            body_h=float(np.median([q['metal'][3]-q['metal'][1] for q in items]))
            for q in items:q['pos'][1]=q['metal'][1]+body_h/2
        if family=='gust':
            # The generated nozzle is an emitter reference. The game clips at its top;
            # a player gust consists of the authored pressure plume above that point.
            for q in items:q['pos'][1]=q['metal'][1]
        pivot=[128,192] if family in ['laser','gust'] else [128,112] if family in ['bullets','spread','missile','heavy'] else [128,128]
        L=max(q['pos'][0]-q['bb'][0] for q in items);R=max(q['bb'][2]-q['pos'][0] for q in items)
        T=max(q['pos'][1]-q['bb'][1] for q in items);B=max(q['bb'][3]-q['pos'][1] for q in items)
        k=min((pivot[0]-8)/max(1,L),(248-pivot[0])/max(1,R),(pivot[1]-8)/max(1,T),(248-pivot[1])/max(1,B))
        bank=[];sheet=Image.new('RGBA',(1024,1024))
        for i,q in enumerate(items):
            cell=q['cell'];size=[round(cell.width*k),round(cell.height*k)]
            scaled=cell.resize(size,Image.Resampling.NEAREST);xy=[round(pivot[j]-q['pos'][j]*k) for j in range(2)]
            plate=Image.new('RGBA',(256,256));plate.alpha_composite(scaled,tuple(xy))
            mask=np.asarray(plate)[:,:,3];assert not np.any(mask[:6]) and not np.any(mask[-6:]),(family,i,'vertical clipping')
            assert not np.any(mask[:,:6]) and not np.any(mask[:,-6:]),(family,i,'horizontal clipping')
            out=DEST/(family+'_'+str(i).zfill(2)+'.png');plate.save(out,optimize=True)
            row=dict(key='wp11_'+family+'_'+str(i).zfill(2),path=out.relative_to(ROOT).as_posix(),slot=slot,name=NAMES[slot],frame=i,fps=24,
                     w=256,h=256,pivot=pivot,source='wind_projectiles_1011/'+source.name,source_rect=q['rect'],source_pivot=q['pos'],
                     physical_rect=q['metal'],content_rect=list(q['bb']),translation=xy,scale=k,sha256=sha(out),source_sha256=sha(source))
            if family in ['bullets','spread','missile','heavy']:row['body_height']=body_h*k
            if family=='laser':row['body_rect']=[104,68,48,96];row['tip_rect']=[64,8,128,76];row['root_rect']=[56,158,144,90]
            if family=='gust':row['draw_rect']=[0,0,256,pivot[1]]
            bank.append(row);sheet.alpha_composite(plate,((i%4)*256,(i//4)*256))
        assert len({q['sha256'] for q in bank})==16,(family,'duplicate poses')
        manifest['wind_'+family]=bank;all_banks[family]=bank
        sheet.save(SOURCE/(family+'_registered.png'))
        audit[family]=dict(frames=16,resolution=[256,256],pivot=pivot,common_scale=k,raw_size=[W,H],raw_sha256=sha(source))
    (SOURCE/'registration.json').write_text(json.dumps(dict(banks=all_banks,audit=audit),indent=2),encoding='utf-8')
