"""Normalize authored cover/strafe art. Sources retained; one scale per bank.

Equal 320px canvases preserve complete limbs and weapons. The source generator
returned nonuniform cells, so connected silhouettes identify each drawing;
no pose is synthesized, warped, or individually fitted to its cell.
"""
from pathlib import Path
import json, hashlib, statistics
import numpy as np
from PIL import Image, ImageDraw
from build_yuri_motion_1013 import components, isolate

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/cover_motion_1013'
SRC=OUT/'source';FRAMES=OUT/'frames'
REVIEW=ROOT/'_shots/cover_motion_1013'
data={'version':'1013-cover-motion-r1','assets':{},'sequences':{},'audit':[],'sources':{}}

def grid(im,cols,rows):
    bodies=[q for q in components(im) if q['area']>1200]
    cells=[]
    for row in range(rows):
        for col in range(cols):
            candidates=[q for q in bodies if int((q['box'][0]+q['box'][2])/2/im.width*cols)==col and int((q['box'][1]+q['box'][3])/2/im.height*rows)==row]
            assert candidates,(row,col,len(bodies))
            cells.append(max(candidates,key=lambda q:q['area']))
    return cells

def save(key,frame,anchor,source,crop,scale):
    bounds=frame.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox()
    assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<frame.width and bounds[3]<frame.height,(key,bounds)
    path=FRAMES/(key+'.png');frame.save(path,optimize=True)
    data['assets'][key]={'file':path.relative_to(ROOT).as_posix(),'size':list(frame.size),'anchor':anchor,'bounds':bounds}
    data['audit'].append({'key':key,'source':source,'crop':crop,'scale':scale,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})

def bank(filename,cols,rows,groups,target,reference,baseline=256):
    im=Image.open(SRC/filename).convert('RGBA')
    if filename=='enemy_sidestep.png':
        # Generator delivered four four-cell rows and a six-cell walk row.
        # Preserve and document that actual layout instead of clipping it to
        # the requested grid or inventing duplicate missing drawings.
        bodies=sorted([q for q in components(im) if q['area']>1200],key=lambda q:q['box'][1]);lines=[]
        for q in bodies:
            if not lines or q['box'][1]-statistics.median(v['box'][1] for v in lines[-1])>120:lines.append([])
            lines[-1].append(q)
        assert list(map(len,lines))==[4,4,4,4,6],list(map(len,lines))
        cells=sum([sorted(line,key=lambda q:q['box'][0]) for line in lines],[])
    else:cells=grid(im,cols,rows)
    scale=target/statistics.median(cells[i]['box'][3]-cells[i]['box'][1] for i in reference)
    for prefix,indices,motion in groups:
        keys=[]
        for i,index in enumerate(indices):
            q=cells[index];cell,crop=isolate(im,q);a=np.asarray(cell)
            # Register the chest rather than the complete silhouette: an
            # extended rifle or striding boot must not shift the torso root.
            if prefix.startswith('yuri'):
                chest=(a[:,:,0]>65)&(a[:,:,0]>a[:,:,1]*1.55)&(a[:,:,0]>a[:,:,2]*1.3)&(a[:,:,3]>96)
                if filename=='yuri_blindfire_front.png':
                    # Raised rifle extends upward. Register the jacket at a
                    # fixed distance above the boots, not the lifted arm.
                    chest[:max(0,cell.height-250)]=False;chest[max(0,cell.height-135):]=False
                else:chest[int(cell.height*.6):]=False
                ys,xs=np.where(chest);px=float(np.median(xs)) if len(xs)>10 else cell.width/2
            else:
                alpha=a[:,:,3]>96;alpha[int(cell.height*.5):]=False;ys,xs=np.where(alpha);px=float(np.median(xs))
            py=cell.height-2;size=(round(cell.width*scale),round(cell.height*scale));offset=(round(160-px*scale),round(baseline-py*scale))
            assert min(offset)>=0 and offset[0]+size[0]<320 and offset[1]+size[1]<320,(prefix,i,size,offset)
            frame=Image.new('RGBA',(320,320));frame.alpha_composite(cell.resize(size,Image.Resampling.NEAREST),offset)
            key='od_cm_'+prefix+'_'+str(i);save(key,frame,[160,256],filename,crop,scale);keys.append(key)
            if prefix=='yuri_north_blindfire':
                a=np.asarray(frame.getchannel('A'));ys,xs=np.where(a>96);top=int(ys.min());yy,xx=np.where(a[top:top+4]>96)
                data['assets'][key]['muzzle']=[float(np.median(xx)),top+1]
        data['sequences'][prefix]={'frames':keys,'fps':16 if motion else 14,'motion':motion,'stride':96,'contacts':[0,len(keys)//2],'scale':scale}
    data['sources'][filename]=hashlib.sha256((SRC/filename).read_bytes()).hexdigest()

def main():
    FRAMES.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    bank('yuri_sidestep_peek.png',4,4,[('yuri_north_sidestep',range(8),True),('yuri_north_peek',range(8,16),False)],176,range(8))
    bank('yuri_blindfire_knockback.png',4,4,[('yuri_north_knockback',range(8,16),False)],176,[8])
    bank('yuri_blindfire_front.png',4,2,[('yuri_north_blindfire',range(8),False)],125,[0])
    bank('enemy_sidestep.png',4,6,[('robot_south_strafe',range(8),False)],191,range(8),284)
    bank('enemy_sidestep.png',4,6,[('gosfer_south_strafe',range(8,16),False)],242,range(8,16),270)
    bank('enemy_sidestep.png',4,6,[('gosfer_south_walk',range(16,22),False)],242,range(16,22),270)
    im=Image.open(SRC/'bunker.png').convert('RGBA');bounds=im.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox();crop=im.crop(bounds);scale=242/crop.width
    size=(round(crop.width*scale),round(crop.height*scale));frame=Image.new('RGBA',(320,192));frame.alpha_composite(crop.resize(size,Image.Resampling.NEAREST),((320-size[0])//2,160-size[1]))
    save('od_cover_bunker',frame,[160,160],'bunker.png',bounds,scale)
    (OUT/'manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    js='window.TD_COVER_MOTION_ART='+json.dumps(data,separators=(',',':'))+';\nObject.assign(window.TD_ASSAULT_ART.assets,TD_COVER_MOTION_ART.assets);\nObject.assign(window.TD_ASSAULT_ART.sequences,TD_COVER_MOTION_ART.sequences);\n'
    (OUT/'manifest.js').write_text(js,encoding='utf8')
    for bankname,seq in data['sequences'].items():
        contact=Image.new('RGB',(1024,320),(24,33,41));pen=ImageDraw.Draw(contact)
        for i,key in enumerate(seq['frames']):
            im=Image.open(ROOT/data['assets'][key]['file']).resize((128,128),Image.Resampling.NEAREST);contact.paste(im,(i*128,25),im);pen.text((i*128+2,160),str(i+1),fill='white')
            # Onion review in lower row preserves neighbors at their fixed root.
            for j,alpha in [((i-1)%len(seq['frames']),80),(i,180),((i+1)%len(seq['frames']),80)]:
                on=Image.open(ROOT/data['assets'][seq['frames'][j]]['file']).resize((128,128),Image.Resampling.NEAREST);on.putalpha(on.getchannel('A').point(lambda a:a*alpha//255));contact.paste(on,(i*128,180),on)
        pen.text((3,3),bankname,fill='white');contact.save(REVIEW/(bankname+'.png'))
    print('Exported',len(data['assets']),'authored frames; scales, bounds, pivots audited.')

if __name__=='__main__':main()
