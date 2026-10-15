"""Drawn rigid views, complete flame tips and continuous atomic progression.

Invoked by build_part2_art_1010.py. Only cropping, transparent padding,
translation, common proportional scaling and Mike's requested palette swaps.
The original sources and the rejected motion banks remain on disk.
"""
from pathlib import Path
import colorsys, hashlib, json
from collections import deque
import numpy as np
from PIL import Image, ImageDraw
from repair_part2_art_1011 import clean, rect_for, palette, save

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/part2_motion_1011'
OUT=ROOT/'assets/game/shared/combat/part2_1010'

def isolated_cell(raw,i,cols,rows):
    """Measure the actual drawn plate, including poses crossing nominal gutters.

    Generated grid spacing is imperfect. An expanded read finds the central
    aircraft's opaque connected plate before cropping; neighboring fragments
    cannot become part of its bounds or physical registration.
    """
    nominal=rect_for(raw,i,cols,rows)
    rect=[max(0,nominal[0]-28),max(0,nominal[1]-28),min(raw.width,nominal[2]+28),min(raw.height,nominal[3]+28)]
    cell=clean(raw.crop(rect)); p=np.asarray(cell); mask=(p[:,:,3]>128).copy()
    components=[]; H,W=mask.shape
    for y,x in zip(*np.nonzero(mask)):
        if not mask[y,x]:continue
        queue=deque([(y,x)]);mask[y,x]=False; count=0;l=x;r=x;t=y;b=y
        while queue:
            yy,xx=queue.popleft();count+=1;l=min(l,xx);r=max(r,xx);t=min(t,yy);b=max(b,yy)
            for ny,nx in ((yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)):
                if 0<=ny<H and 0<=nx<W and mask[ny,nx]:mask[ny,nx]=False;queue.append((ny,nx))
        components.append((count,l,t,r+1,b+1))
    _,l,t,r,b=max(components)
    bounds=[max(0,l-3),max(0,t-3),min(W,r+3),min(H,b+3)]
    source_rect=list(map(int,[rect[0]+bounds[0],rect[1]+bounds[1],rect[0]+bounds[2],rect[1]+bounds[3]]))
    return clean(raw.crop(source_rect)),source_rect

def energy_palette(cell, full):
    p=np.asarray(cell).copy()
    for y,x in zip(*np.nonzero(p[:,:,3])):
        r,g,b,a=map(int,p[y,x]); h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        if s<.10: continue
        target=(.73+(.07-h)*1.6)%1 if full else (h+.28)%1
        lum=(.2126*r+.7152*g+.0722*b)/255
        for _ in range(32):
            rgb=colorsys.hsv_to_rgb(target,s,1)
            peak=sum(q*w for q,w in zip(rgb,[.2126,.7152,.0722]))
            if peak>=lum: break
            s*=.94
        p[y,x,:3]=[round(q*min(1,lum/peak)*255) for q in rgb]
    return Image.fromarray(p)

def register_air(cell,motion):
    p=np.asarray(cell); ys,xs=np.nonzero(p[:,:,3]>128)
    cy=(float(ys.min())+float(ys.max())+1)/2
    if motion=='roll':
        # Nose axis, not wing-tip midpoint: a banking wing may hide the other.
        xx=np.nonzero((p[:,:,3]>128)&(np.indices(p.shape[:2])[0]>=ys.max()-12))[1]
        tail=np.nonzero((p[:,:,3]>128)&(np.indices(p.shape[:2])[0]<=ys.min()+12))[1]
        cx=(float(np.median(xx))+float(np.median(tail)))/2+.5
    else: cx=(float(xs.min())+float(xs.max())+1)/2
    k=.66; move=[round(128-cx*k),round(128-cy*k)]
    c=Image.new('RGBA',(256,256)); c.alpha_composite(cell.resize((round(cell.width*k),round(cell.height*k)),Image.Resampling.NEAREST),move)
    return c,dict(source_pivot=[cx,cy],scale=k,translation=move)

def add_motion_banks(bank):
    bank['stealth']=[a for a in bank['stealth'] if a['pose'] in ['idle','damaged']]
    for motion in ['roll','somer']:
        name='stealth_'+motion; bank[name]=[]
        for role,hue in [('blue',None),('red',.995),('green',.33),('orange',None)]:
            rawname=('orange_' if role=='orange' else '')+motion+'_raw.png'
            raw=Image.open(SRC/rawname).convert('RGBA')
            for i in range(16):
                cell,rect=isolated_cell(raw,i,4,4)
                if hue is not None: cell,_=palette(cell,hue)
                c,meta=register_air(cell,motion)
                a=save(bank[name],f'{name}_{role}_{i:02d}',c,[128,128],role=role,pose=i,motion=motion,
                       source='part2_motion_1011/'+rawname,source_rect=rect,source_sha256=hashlib.sha256((SRC/rawname).read_bytes()).hexdigest(),**meta)
                if role=='orange' and motion=='roll' and i==0:
                    for pose in ['idle','damaged']:
                        save(bank['stealth'],f'stealth_orange_{pose}',c,[128,128],role=role,pose=pose,
                             source=a['source'],source_rect=rect,source_sha256=a['source_sha256'],**meta)
    bank['fire_tip']=[]; raw=Image.open(SRC/'tip_raw.png').convert('RGBA')
    for i in range(16):
        rect=rect_for(raw,i,4,4); cell=clean(raw.crop(rect)); p=np.asarray(cell)
        # Register the actual terminal crown; the bottom is a joining seam.
        strong=(p[:,:,3]>128)&(p[:,:,0]>180)&(p[:,:,1]>60)
        yy,xx=np.nonzero(strong); top=int(yy.min()); base=int(yy.max())
        bottom=np.nonzero(strong & (np.indices(p.shape[:2])[0]>=base-8))[1]
        cx=(float(bottom.min())+float(bottom.max())+1)/2
        move=[round(192-cx),64-top]; c=Image.new('RGBA',(384,384)); c.alpha_composite(cell,move)
        save(bank['fire_tip'],f'fire_tip_{i:02d}',c,[192,64],source='part2_motion_1011/tip_raw.png',source_rect=rect,
             scale=1,translation=move,join_width=200,join_y=base+move[1]-4)
    bank['atom']=[]; raw=Image.open(SRC/'atom_raw.png').convert('RGBA')
    order=list(range(32)); order[7],order[8]=order[8],order[7] # monotonic rising-cap order
    for index,i in enumerate(order):
        rect=rect_for(raw,i,4,8); cell=clean(raw.crop(rect)); p=np.asarray(cell)
        mask=p[:,:,3]>96; ys,xs=np.nonzero(mask); lower=int(ys.max())
        # The bright horizontal contact ridge is above drifting floor embers.
        lo=max(0,lower-18); ridge=lo+int(mask.sum(axis=1)[lo:lower+1].argmax())
        xx=np.nonzero(mask[max(0,ridge-1):ridge+2])[1]
        cx=(float(xx.min())+float(xx.max())+1)/2
        move=[round(192-cx*2),480-ridge*2]; c=Image.new('RGBA',(384,576))
        c.alpha_composite(cell.resize((cell.width*2,cell.height*2),Image.Resampling.NEAREST),move)
        save(bank['atom'],f'atom_{index:02d}',c,[192,480],source='part2_motion_1011/atom_raw.png',source_index=i,
             source_rect=rect,source_pivot=[cx,ridge],scale=2,translation=move)
    for name,full in [('maverick',False),('maverick_full',True)]:
        bank[name]=[]
        for i,a in enumerate(bank['jace']):
            cell=Image.open(ROOT/a['path']).convert('RGBA'); colored=energy_palette(cell,full)
            c=Image.new('RGBA',(288,288));c.alpha_composite(colored,(16,16))
            save(bank[name],f'{name}_{i:02d}',c,[144,144],source=a['path'],source_sha256=a['sha256'],scale=1,padding=[16,16],
                 palette='Purple/blue overdrive' if full else 'Green half charge',alpha_preserved=True)
    audit={}
    for name in ['stealth_roll','stealth_somer','fire_tip','atom','maverick','maverick_full']:
        cells=bank[name]; bounds=[c['opaque_bounds'] for c in cells]
        audit[name]=dict(frames=len(cells),unique_hashes=len({a['sha256'] for a in cells}),
            union_bounds=[min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds)],
            padded_edges=all(b[0]>=2 and b[1]>=2 and b[2]<=c['w']-2 and b[3]<=c['h']-2 for c,b in zip(cells,bounds)),
            common_scale=len({a['scale'] for a in cells})==1)
        assert audit[name]['padded_edges'],(name,audit[name])
        assert audit[name]['unique_hashes']==len(cells),(name,audit[name])
        contact=Image.new('RGBA',(256*4,288*((len(cells)+3)//4)),(15,23,34,255))
        label=ImageDraw.Draw(contact)
        for i,a in enumerate(cells):
            im=Image.open(ROOT/a['path']); im.thumbnail((240,256),Image.Resampling.NEAREST)
            x=(i%4)*256+(256-im.width)//2; y=(i//4)*288+(256-im.height)//2
            contact.alpha_composite(im,(x,y)); label.text(((i%4)*256+8,(i//4)*288+265),a['key'],fill='white')
        contact.save(SRC/(name+'_contact.png'))
    (SRC/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    (SRC/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen; requested palette swaps; no warped or duplicated animation poses',banks={k:bank[k] for k in audit}),indent=2),encoding='utf-8')
    print(json.dumps(audit))
