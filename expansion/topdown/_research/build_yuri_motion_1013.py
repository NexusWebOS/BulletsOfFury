"""Export authored Yuri motion with shared bank scale and physical registration.

Original generator sheets stay untouched. Connected silhouettes recover limbs
outside nominal cells; translations register chest/feet without per-frame fit.
No painted, warped, interpolated or duplicated animation drawings.
"""
from pathlib import Path
import json, hashlib, math, statistics
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/yuri_motion_1013'
SRC=OUT/'source'
FRAMES=OUT/'frames'
REVIEW=ROOT/'_shots/overdrive_yuri_motion_1013'
DIRS=['south','southwest','west','northwest','north','northeast','east','southeast']

def components(im):
    mask=np.asarray(im.getchannel('A'))>32
    parents=[];runs=[];previous=[]
    def root(i):
        while parents[i]!=i:
            parents[i]=parents[parents[i]];i=parents[i]
        return i
    for y,line in enumerate(mask):
        edges=np.flatnonzero(np.diff(np.pad(line.astype(np.int8),(1,1))))
        current=[]
        for x0,x1 in zip(edges[::2],edges[1::2]):
            touching=[q[2] for q in previous if q[0]<=x1 and q[1]>=x0]
            if touching:
                label=root(touching[0])
                for other in touching[1:]:parents[root(other)]=label
            else:label=len(parents);parents.append(label)
            current.append((int(x0),int(x1),label));runs.append((int(x0),int(x1),y,label))
        previous=current
    found={}
    for x0,x1,y,label in runs:
        q=found.setdefault(root(label),{'box':[x0,y,x1,y+1],'area':0,'runs':[]})
        b=q['box'];b[0]=min(b[0],x0);b[1]=min(b[1],y);b[2]=max(b[2],x1);b[3]=max(b[3],y+1)
        q['area']+=x1-x0;q['runs'].append((x0,x1,y))
    return list(found.values())

def rows_of(im):
    bodies=sorted([q for q in components(im) if q['area']>1200],key=lambda q:q['box'][1])
    rows=[]
    for q in bodies:
        y=q['box'][1]
        if not rows or abs(y-statistics.median(v['box'][1] for v in rows[-1]))>65:rows.append([])
        rows[-1].append(q)
    return [sorted(row,key=lambda q:q['box'][0]) for row in rows]

def isolate(im,q):
    b=q['box'];box=(b[0]-2,b[1]-2,b[2]+2,b[3]+2)
    cell=im.crop(box);mask=Image.new('L',cell.size);pen=ImageDraw.Draw(mask)
    for x0,x1,y in q['runs']:pen.line((x0-box[0],y-box[1],x1-1-box[0],y-box[1]),fill=255)
    mask=mask.filter(ImageFilter.MaxFilter(5))
    alpha=np.asarray(cell.getchannel('A')).copy();alpha[np.asarray(mask)==0]=0
    cell.putalpha(Image.fromarray(alpha))
    return cell,box

def export():
    FRAMES.mkdir(exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    data={'version':'1013-yuri-motion-r1','assets':{},'sequences':{},'audit':[],'sources':{}}
    for d in DIRS:
        filename='yuri_'+d+'.png';im=Image.open(SRC/filename).convert('RGBA');rows=rows_of(im)
        expected={'south':[6]*5,'north':[8]*6,'northwest':[8]*6,'northeast':[7]*4+[6]*2}.get(d,[6]*6)
        assert list(map(len,rows))==expected,(d,list(map(len,rows)))
        groups={'walk':sum(rows[:2],[]),'run_fire':sum(rows[2:3 if d=='south' else 4],[]),'crawl':sum(rows[-2:],[])}
        # Match the approved 176 px standing body height, then hold that scale
        # through walk/run/crawl. No individual-pose resizing is performed.
        shared_scale=176/statistics.median(q['box'][3]-q['box'][1] for q in groups['walk'])
        for action,bodies in groups.items():
            source=filename;sheet=im;scale=shared_scale
            if d=='south' and action=='run_fire':
                source='yuri_south_run_fire.png';sheet=Image.open(SRC/source).convert('RGBA')
                fire_rows=rows_of(sheet);assert list(map(len,fire_rows))==[4,4,4]
                bodies=sum(fire_rows,[]);scale=176/statistics.median(q['box'][3]-q['box'][1] for q in bodies)
            keys=[]
            for i,q in enumerate(bodies):
                cell,box=isolate(sheet,q);a=np.asarray(cell)
                red=(a[:,:,0]>65)&(a[:,:,0]>a[:,:,1]*1.55)&(a[:,:,0]>a[:,:,2]*1.3)&(a[:,:,3]>96)
                # Torso registration ignores the rifle and swinging feet. This
                # prevents bounding-box centering from making the head jitter.
                red[int(cell.height*.63):]=False
                yy,xx=np.where(red);assert len(xx)>30,(d,action,i)
                if action=='crawl':
                    # Stable prone ground point below the upper torso, measured
                    # on the authored bank; no rotation/mirroring or cut limbs.
                    px=float(np.median(xx));py=cell.height*.72+20/scale
                else:
                    px=float(np.median(xx));py=cell.height-2
                size=(round(cell.width*scale),round(cell.height*scale))
                resized=cell.resize(size,Image.Resampling.NEAREST)
                # Shared 32 px transparent padding preserves the rifle/boots
                # when the physical torso pivot is asymmetric in side views.
                offset=(round(160-px*scale),round(256-py*scale))
                assert offset[0]>=0 and offset[1]>=0 and offset[0]+size[0]<=320 and offset[1]+size[1]<=320,(d,action,i,size,offset)
                frame=Image.new('RGBA',(320,320));frame.alpha_composite(resized,offset)
                bounds=frame.getchannel('A').point(lambda v:255 if v>32 else 0).getbbox()
                assert bounds and min(bounds[:2])>0 and max(bounds[2:])<320,(d,action,i,bounds)
                key=f'od_ym_{d}_{action}_{i}';path=FRAMES/(key+'.png');frame.save(path,optimize=True)
                data['assets'][key]={'file':path.relative_to(ROOT).as_posix(),'size':[320,320],'anchor':[160,256],'bounds':bounds}
                data['audit'].append({'key':key,'source':source,'source_size':sheet.size,'crop':box,'scale':scale,'source_pivot':[round(px+box[0],3),round(py+box[1],3)],'offset':offset,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
                keys.append(key)
            n=len(keys);stride=48 if action=='crawl' else 96;speed=63 if action=='crawl' else 165
            data['sequences']['yuri_'+d+'_'+action]={'frames':keys,'fps':n*speed/stride,'stride':stride,'motion':True,'scale':scale,'contacts':[0,n//2]}
            data['sources'][source]=hashlib.sha256((SRC/source).read_bytes()).hexdigest()
        print(d,[(a,len(data['sequences']['yuri_'+d+'_'+a]['frames'])) for a in groups])
    (OUT/'manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    script='window.TD_YURI_MOTION_ART='+json.dumps(data,separators=(',',':'))+';\n'
    script+='Object.assign(window.TD_ASSAULT_ART.assets,TD_YURI_MOTION_ART.assets);\nObject.assign(window.TD_ASSAULT_ART.sequences,TD_YURI_MOTION_ART.sequences);\n'
    (OUT/'manifest.js').write_text(script,encoding='utf-8')
    for d in DIRS:
        contact=Image.new('RGB',(8*128,6*144),(23,32,39));pen=ImageDraw.Draw(contact)
        for j,action in enumerate(['walk','run_fire','crawl']):
            for i,key in enumerate(data['sequences']['yuri_'+d+'_'+action]['frames']):
                frame=Image.open(ROOT/data['assets'][key]['file']).resize((128,128),Image.Resampling.NEAREST)
                x=(i%8)*128;y=(j*2+i//8)*144;contact.paste(frame,(x,y),frame)
                pen.text((x+2,y+129),action+' '+str(i+1),fill='white')
        contact.save(REVIEW/(d+'_frames.png'))
    print('Exported',len(data['assets']),'unique authored frames /',len(data['sequences']),'motion banks.')

if __name__=='__main__':export()
