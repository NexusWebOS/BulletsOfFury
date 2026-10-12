"""Register drawn Wind projectile badges and its separate elemental emblem."""
from pathlib import Path
from PIL import Image
import numpy as np
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/wind_icons_1011'
DEST=ROOT/'assets/game/shared/ui/wind_icons_1011'
NAMES=['Wind bullets','Wind spread','Wind missile','Wind laser','Gust breath',
       'Tornado orb','Wind mist','Heavy Wind slugs','Electric Wind orb']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def runs(line):
    found=[];start=None
    for i,value in enumerate(list(line)+[False]):
        if value and start is None:start=i
        elif not value and start is not None:found.append([start,i]);start=None
    return found

def visible_cell(im,rect):
    cell=im.crop(rect).convert('RGBA');p=np.asarray(cell).copy()
    p[p[:,:,3]<=20]=0
    cell=Image.fromarray(p);mask=Image.fromarray((p[:,:,3]>96).astype('uint8')*255)
    bb=mask.getbbox();assert bb,'Empty generated icon'
    bb=[max(0,bb[0]-2),max(0,bb[1]-2),min(cell.width,bb[2]+2),min(cell.height,bb[3]+2)]
    # Only crop/pad/register authored pixels; never redraw frames or numerals.
    return cell,bb

def add_wind_icons(manifest):
    DEST.mkdir(parents=True,exist_ok=True)
    rows=[];audits={}
    for file,cols,nrows,base in [('base_raw.png',3,3,True),('tiers_raw.png',4,9,False)]:
        green=file.replace('_raw.png','_green_raw.png')
        if (SOURCE/green).exists():file=green
        f=SOURCE/file;im=Image.open(f).convert('RGBA');W,H=im.size;items=[]
        ink=np.asarray(im)[:,:,3]>96
        xs=runs(ink.sum(axis=0)>20);ys=runs(ink.sum(axis=1)>20)
        assert len(xs)==cols and len(ys)==nrows,'Generated badge count does not match requested bank'
        for i in range(cols*nrows):
            c,r=i%cols,i//cols
            # The returned tier sheet has unequal outside margins. Measure its
            # real blank gutters so Roman tags never cross a nominal cell cut.
            rect=[max(0,xs[c][0]-8),max(0,ys[r][0]-8),min(W,xs[c][1]+8),min(H,ys[r][1]+8)]
            cell,bb=visible_cell(im,rect);items.append((cell,bb,rect))
        k=110/max(max(b[2]-b[0],b[3]-b[1]) for _,b,_ in items)
        for i,(cell,bb,rect) in enumerate(items):
            slot=i if base else i//4;level=1 if base else i%4+2
            # A common scale per source bank preserves every drawn proportion.
            crop=cell.crop(bb);size=[max(1,round(crop.width*k)),max(1,round(crop.height*k))]
            crop=crop.resize(size,Image.Resampling.NEAREST)
            xy=[(128-size[0])//2,(128-size[1])//2]
            plate=Image.new('RGBA',(128,128));plate.alpha_composite(crop,tuple(xy))
            suffix='' if level==1 else '_'+str(level)
            out=DEST/f'wind_icon_{slot}{suffix}.png';plate.save(out,optimize=True)
            rows.append(dict(key=f'ap10_wind_icon_{slot}{suffix}',path=out.relative_to(ROOT).as_posix(),
                slot=slot,level=level,name=NAMES[slot],w=128,h=128,pivot=[64,64],
                source='wind_icons_1011/'+file,source_rect=rect,content_rect=list(bb),
                scale=k,translation=xy,sha256=sha(out),source_sha256=sha(f)))
        audits[file]=dict(grid=[cols,nrows],frames=len(items),columns=xs,rows=ys,common_scale=k,raw_sha256=sha(f))
    rows.sort(key=lambda a:(a['slot'],a['level']))
    assert len(rows)==45 and len({a['sha256'] for a in rows})==45
    f=SOURCE/'symbol_raw.png';im=Image.open(f).convert('RGBA')
    cell,bb=visible_cell(im,[0,0,*im.size]);crop=cell.crop(bb);k=110/max(crop.size)
    size=[round(crop.width*k),round(crop.height*k)];crop=crop.resize(size,Image.Resampling.NEAREST)
    plate=Image.new('RGBA',(128,128));xy=[(128-size[0])//2,(128-size[1])//2];plate.alpha_composite(crop,tuple(xy))
    out=DEST/'wind_symbol.png';plate.save(out,optimize=True)
    symbol=dict(key='ap10_wind_symbol',path=out.relative_to(ROOT).as_posix(),w=128,h=128,pivot=[64,64],
        source='wind_icons_1011/symbol_raw.png',source_rect=list(bb),scale=k,translation=xy,
        sha256=sha(out),source_sha256=sha(f))
    manifest['wind_icons']=rows;manifest['wind_symbol']=[symbol]
    for a in rows+[symbol]:
        p=np.asarray(Image.open(ROOT/a['path']));assert not np.any(p[:8,:,3]) and not np.any(p[-8:,:,3])
        assert not np.any(p[:,:8,3]) and not np.any(p[:,-8:,3]),a['key']
    (SOURCE/'registration.json').write_text(json.dumps(dict(banks={'wind_icons':rows,'wind_symbol':[symbol]},audit=audits),indent=2),encoding='utf-8')
    card=Image.new('RGBA',(5*128,10*128))
    for a in rows:card.alpha_composite(Image.open(ROOT/a['path']).convert('RGBA'),((a['level']-1)*128,a['slot']*128))
    card.alpha_composite(plate,(2*128,9*128));card.save(SOURCE/'registered_preview.png')
