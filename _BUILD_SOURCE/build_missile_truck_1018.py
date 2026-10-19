"""Normalize generated whole banks: integer registration, one scale, fixed pivots.

No shared atlas edits. Source component bounds are measured, not assumed from
the generator's approximate grid; every shipping canvas is 192x256 RGBA.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/missile_truck_1018'
OUT=ROOT/'assets/game/levels/stage_01/enemies/missile_truck_1018'
QA=ROOT/'_shots/truck_furnace_1018'
OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
CANVAS=(192,256);SCALE=.625;PIVOT=(96,128)

def source_cells(filename,count):
    im=Image.open(SRC/filename).convert('RGBA');a=np.array(im)
    labs,n=label(a[:,:,3]>80);sizes=np.bincount(labs.ravel())
    pieces=[]
    for ident,s in enumerate(find_objects(labs),1):
        if sizes[ident]>1500:
            box=(s[1].start,s[0].start,s[1].stop,s[0].stop)
            pieces.append((ident,box))
    pieces.sort(key=lambda q:((q[1][1]+q[1][3])//2//360,q[1][0]))
    cells=[];records=[]
    for i,(ident,box) in enumerate(pieces[:count]):
        # Lower mounting latch / bumper is a fixed physical reference. Variable
        # rocket and smoke height never changes the crop scale or vertical pivot.
        x=(box[0]+box[2])//2;y=box[3]-(169 if count==8 else 146)
        x0,y0,x1,y1=box
        rect=(max(0,x0-3),max(0,y0-3),min(im.width,x1+3),min(im.height,y1+3))
        crop=im.crop(rect)
        # Keep the authored connected sprite and its near-edge alpha. Discard
        # only generator dust beyond its own component; never nearby cells.
        b=np.array(crop);mask=b[:,:,3]<8;b[mask]=0;crop=Image.fromarray(b)
        rw=round(crop.width*SCALE);rh=round(crop.height*SCALE)
        crop=crop.resize((rw,rh),Image.Resampling.NEAREST)
        dx=round(PIVOT[0]+(rect[0]-x)*SCALE);dy=round(PIVOT[1]+(rect[1]-y)*SCALE)
        cell=Image.new('RGBA',CANVAS);cell.alpha_composite(crop,(dx,dy))
        bbox=cell.getbbox()
        assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<192 and bbox[3]<256,(filename,i,bbox)
        cells.append(cell);records.append({'sourceRect':rect,'sourcePivot':[x,y],'scale':SCALE,'bbox':bbox})
    assert len(cells)==count
    return cells,records

def black_paint(im):
    a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
    # Olive paint only. Red/white ordnance, lamps, black outlines and metal
    # highlights retain their authored pixels and alpha.
    mask=(a[:,:,3]>0)&(g>=r*.85)&(g>b*1.20)&(r<g*1.3)&(g>15)
    lum=.299*r+.587*g+.114*b
    for c,k in enumerate([.88,.98,1.10]):a[:,:,c][mask]=np.clip(lum[mask]*k,0,255)
    return Image.fromarray(a)

art={};audit={'canvas':CANVAS,'pivot':PIVOT,'scale':SCALE,'banks':{}}
for name,file,n,fps in [('hull','truck_modules.png',8,14),('launcher','launcher_cycle.png',16,12)]:
    frames,registration=source_cells(file,n)
    for palette in ['olive','black']:
        bank=[];bank_frames=[black_paint(c) for c in frames] if palette=='black' else frames
        for i,cell in enumerate(bank_frames):
            key=f'mt18_{name}_{palette}_{i:02d}';path=OUT/(key+'.png');cell.save(path,optimize=True)
            bank.append({'key':key,'path':path.relative_to(ROOT).as_posix(),'w':192,'h':256,'pivot':PIVOT})
        art[name+'_'+palette]={'fps':fps,'frames':bank}
    audit['banks'][name]={'frames':n,'registration':registration,'sha256':hashlib.sha256((SRC/file).read_bytes()).hexdigest()}
    # Native-size contact and neighbor onion sheets are review output only.
    contact=Image.new('RGBA',(192*4,256*((n+3)//4)),(8,20,29,255));d=ImageDraw.Draw(contact)
    onion=Image.new('RGBA',contact.size,(8,20,29,255))
    for i,c in enumerate(frames):
        x=(i%4)*192;y=(i//4)*256
        contact.alpha_composite(c,(x,y));d.text((x+5,y+5),str(i),fill='white')
        prev=frames[(i-1)%n].copy();prev.putalpha(prev.getchannel('A').point(lambda a:a//3));onion.alpha_composite(prev,(x,y))
        cur=c.copy();cur.putalpha(cur.getchannel('A').point(lambda a:a*2//3));onion.alpha_composite(cur,(x,y))
    contact.save(QA/(name+'-contact.png'));onion.save(QA/(name+'-onion.png'))
(ROOT/'assets/missile_truck_art_1018.js').write_text('"use strict";\n// Generated banks: fixed192x256, pivot96,128; owned by build_missile_truck_1018.py.\nconst MT18_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SRC/'registration.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(json.dumps({'frames':sum(len(b['frames']) for b in art.values()),'bytes':sum(p.stat().st_size for p in OUT.glob('*.png')),'audit':str(SRC/'registration.json')}))
