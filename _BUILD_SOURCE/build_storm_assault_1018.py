"""Registered Storm ordnance: one proportional scale per authored 16-pose bank.

Shipping frames have even dimensions, fixed pivots, and shared transparent
padding. Source grids are approximate; the bomb's physical nose registers its
body while the impact uses the unchanged centre of each source cell.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/storm_assault_1018'
OUT=ROOT/'assets/game/levels/stage_04/fx/storm_assault_1018'
QA=ROOT/'_shots/storm_assault_1018'
OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
art={};audit={}
for name,canvas,scale,fps in [('bomb',(128,192),.45,18),('impact',(256,256),.72,20)]:
    filename='lightning_'+name+'.png';im=Image.open(SRC/filename).convert('RGBA')
    pixels=np.array(im);pivot=[canvas[0]//2,canvas[1]//2];frames=[];records=[]
    if name=='bomb':
        labs,n=label(pixels[:,:,3]>100);sizes=np.bincount(labs.ravel())
        boxes=[(s[1].start,s[0].start,s[1].stop,s[0].stop) for i,s in enumerate(find_objects(labs),1) if sizes[i]>30000]
        boxes.sort(key=lambda q:((q[1]+q[3])//2//380,q[0]));assert len(boxes)==16
    for i in range(16):
        if name=='bomb':
            x0,y0,x1,y1=boxes[i];anchor=[(x0+x1)//2,y1-175]
            rect=[max(0,x0-12),max(0,y0-12),min(im.width,x1+12),min(im.height,y1+12)]
        else:
            rect=[round((i%4)*im.width/4),round((i//4)*im.height/4),round((i%4+1)*im.width/4),round((i//4+1)*im.height/4)]
            anchor=[round((i%4+.5)*im.width/4),round((i//4+.5)*im.height/4)]
        crop=im.crop(rect);a=np.array(crop);a[a[:,:,3]<8]=0;crop=Image.fromarray(a)
        crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
        offset=[round(pivot[0]+(rect[0]-anchor[0])*scale),round(pivot[1]+(rect[1]-anchor[1])*scale)]
        cell=Image.new('RGBA',canvas);cell.alpha_composite(crop,offset);bbox=cell.getbbox()
        assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<canvas[0] and bbox[3]<canvas[1],(name,i,bbox)
        key=f'st18_{name}_{i:02d}';path=OUT/(key+'.png');cell.save(path,optimize=True);frames.append(cell)
        records.append({'sourceRect':rect,'sourcePivot':anchor,'bbox':bbox})
    art[name]={'fps':fps,'w':canvas[0],'h':canvas[1],'pivot':pivot,'frames':[{'key':f'st18_{name}_{i:02d}','path':(OUT/f'st18_{name}_{i:02d}.png').relative_to(ROOT).as_posix()} for i in range(16)]}
    audit[name]={'canvas':canvas,'pivot':pivot,'scale':scale,'sourceSha256':hashlib.sha256((SRC/filename).read_bytes()).hexdigest(),'registration':records}
    contact=Image.new('RGBA',(canvas[0]*4,canvas[1]*4),(7,17,30,255));onion=contact.copy();draw=ImageDraw.Draw(contact)
    for i,cell in enumerate(frames):
        x=i%4*canvas[0];y=i//4*canvas[1];contact.alpha_composite(cell,(x,y));draw.text((x+5,y+5),str(i),fill='white')
        prev=frames[(i-1)%16].copy();prev.putalpha(prev.getchannel('A').point(lambda a:a//3));onion.alpha_composite(prev,(x,y))
        cur=cell.copy();cur.putalpha(cur.getchannel('A').point(lambda a:a*2//3));onion.alpha_composite(cur,(x,y))
    contact.save(QA/(name+'-contact.png'));onion.save(QA/(name+'-onion.png'))
(ROOT/'assets/storm_assault_art_1018.js').write_text('"use strict";\n// Owned by build_storm_assault_1018.py: fixed canvases, pivots and bank scales.\nconst ST18_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SRC/'registration.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(json.dumps({'frames':32,'bytes':sum(p.stat().st_size for p in OUT.glob('*.png')),'audit':str(SRC/'registration.json')}))
