"""Normalize the four authored portal loops around their physical apertures.

Only fixed-scale sampling, integer translation, padding and the stationary
authored gate's aperture mask. No synthetic poses, image rotation or warping.
"""
from pathlib import Path
from collections import deque
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/portals_1011/returned'
OUT=ROOT/'assets/game/shared/fx/portals_1011';OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT/'_shots/portals_1011';QA.mkdir(parents=True,exist_ok=True)

def components(mask):
    h,w=mask.shape;seen=np.zeros_like(mask);result=[]
    for sy,sx in zip(*np.nonzero(mask)):
        if seen[sy,sx]:continue
        queue=deque([(int(sx),int(sy))]);seen[sy,sx]=True;points=[]
        while queue:
            x,y=queue.popleft();points.append((x,y))
            for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if 0<=xx<w and 0<=yy<h and mask[yy,xx] and not seen[yy,xx]:
                    seen[yy,xx]=True;queue.append((xx,yy))
        result.append(np.asarray(points))
    return result

def anchor(cell,kind):
    a=np.asarray(cell);h,w=a.shape[:2];yy,xx=np.indices((h,w))
    if kind=='void':
        mask=(a[:,:,:3].max(axis=2)<7)&(abs(xx-w/2)<w*.27)&(abs(yy-h/2)<h*.27)
        parts=[p for p in components(mask) if len(p)>200]
        part=min(parts,key=lambda p:np.linalg.norm(p.mean(axis=0)-[w/2,h/2]))
    elif kind=='gate-energy':
        # The focal spark has four disconnected bright arms in some poses.
        # Measure them together inside the dark moat, excluding the travelling
        # outer rings. Picking one connected arm visibly moves the focal point.
        cx,cy=w/2,h*.60
        for _ in range(5):
            roi=(xx-cx)**2+(yy-cy)**2<11**2
            weight=np.maximum(0,a[:,:,1].astype(float)-90)*roi
            cx=float((xx*weight).sum()/weight.sum());cy=float((yy*weight).sum()/weight.sum())
        ys,xs=np.nonzero(weight)
        return cx,cy,dict(method='focal-spark-weighted-centroid',area=len(xs),bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
    else:
        # Close only tiny breaks in the bright rim for measurement. The native
        # image and alpha are not altered by this analysis mask.
        rim=(a[:,:,:3].min(axis=2)>110)&(a[:,:,3]>100)
        rim=np.asarray(Image.fromarray((rim*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5)))>0
        parts=[p for p in components(~rim) if len(p)>120 and p[:,0].min()>0 and p[:,1].min()>0 and p[:,0].max()<w-1 and p[:,1].max()<h-1]
        assert parts,(kind,'no enclosed aperture')
        part=max(parts,key=len)
    cx,cy=part.mean(axis=0)
    return float(cx),float(cy),dict(area=len(part),bounds=[int(part[:,0].min()),int(part[:,1].min()),int(part[:,0].max()+1),int(part[:,1].max()+1)])

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(bank,i,im,pivot,**extra):
    assert im.width%2==im.height%2==0
    path=OUT/f'{bank}_{i:02d}.png';im.save(path,optimize=True)
    return dict(key=f'pr11_{bank}_{i}',path=path.relative_to(ROOT).as_posix(),w=im.width,h=im.height,
                pivot=list(pivot),sha256=sha(path),**extra)

art={};analysis={};raw_cells={};registered={}
for source,bank in [('blue','blue_rift'),('red','red_rift'),('void','black_void'),('gate-energy','gate_energy')]:
    raw=Image.open(SRC/f'{source}.png').convert('RGBA');frames=[];cells=[];records=[]
    for i in range(32):
        x,x1=[round(n*raw.width/4) for n in (i%4,i%4+1)]
        y,y1=[round(n*raw.height/8) for n in (i//4,i//4+1)]
        cell=raw.crop((x,y,x1,y1));cx,cy,measure=anchor(cell,source)
        target=(160,160);dx,dy=round(target[0]-cx),round(target[1]-cy)
        normalized=Image.new('RGBA',(320,320),(0,0,0,255) if source=='void' else (0,0,0,0))
        normalized.paste(cell,(dx,dy))
        err=[round(cx+dx-target[0],4),round(cy+dy-target[1],4)]
        edge=np.asarray(normalized)
        border=np.concatenate([edge[0],edge[-1],edge[:,0],edge[:,-1]])
        assert (border[:,:3].max()<8 if source=='void' else border[:,3].max()==0),(source,i,'clipped')
        frames.append(normalized);cells.append(cell)
        records.append(write(bank,i,normalized,target,source=f'{source}.png',sourceRect=[x,y,x1-x,y1-y],
            sourceAnchor=[round(cx,4),round(cy,4)],translation=[dx,dy],scale=1,centerError=err,measurement=measure))
    assert len({a['sha256'] for a in records})==32
    art[bank]=dict(label={'blue_rift':'Azure teleport rift','red_rift':'Crimson teleport rift','black_void':'Black void tunnel','gate_energy':'Amethyst energy membrane'}[bank],
        fps=24 if source!='void' else 16,frames=records,role='component' if source=='gate-energy' else 'animation')
    registered[bank]=frames;raw_cells[bank]=cells
    analysis[bank]=dict(maxCenterError=max(max(abs(e) for e in a['centerError']) for a in records),
        sourceAnchors=[a['sourceAnchor'] for a in records])

# One immutable gate shell. Its negative space defines the actual aperture;
# the source arch itself remains authored, unchanged pixels at one fixed scale.
raw=Image.open(SRC/'gate-frame.png').convert('RGBA');a=np.asarray(raw);h,w=a.shape[:2]
axis=w//2;mask=np.zeros((h,w),dtype='uint8')
for y in range(round(h*.22),h):
    if a[y,axis,3]>70:continue
    ls=np.flatnonzero(a[y,:axis,3]>110);rs=np.flatnonzero(a[y,axis:,3]>110)
    if len(ls) and len(rs):
        l=int(ls[-1])+1;r=axis+int(rs[0])
        if r-l>w*.25:mask[y,l:r]=255
ys,xs=np.nonzero(mask);gate_anchor=((xs.min()+xs.max())/2,(ys.min()+ys.max())/2)
gate_scale=.40;pivot=(256,352);size=(round(w*gate_scale),round(h*gate_scale))
offset=(round(pivot[0]-gate_anchor[0]*gate_scale),round(pivot[1]-gate_anchor[1]*gate_scale))
shell=Image.new('RGBA',(512,640));shell.paste(raw.resize(size,Image.Resampling.NEAREST),offset)
opening=Image.new('L',(512,640));opening.paste(Image.fromarray(mask).resize(size,Image.Resampling.NEAREST),offset)
opening.save(OUT/'gate-aperture-mask.png');shell.save(OUT/'gate-shell.png')
records=[];gate_frames=[];scale=2.6
for i,cell in enumerate(raw_cells['gate_energy']):
    cx,cy=art['gate_energy']['frames'][i]['sourceAnchor']
    offset_energy=(round(pivot[0]-cx*scale),round(pivot[1]-cy*scale))
    energy=Image.new('RGBA',shell.size)
    energy.paste(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST),offset_energy)
    ea=np.asarray(energy).copy();ea[:,:,3]=(ea[:,:,3].astype('uint16')*np.asarray(opening).astype('uint16')//255).astype('uint8')
    energy=Image.fromarray(ea);im=Image.alpha_composite(energy,shell)
    gate_frames.append(im)
    records.append(write('amethyst_gate',i,im,pivot,source='gate-energy.png + gate-frame.png',
        energyScale=scale,shellScale=gate_scale,shellAnchor=list(gate_anchor),shellOffset=list(offset),
        energyOffset=list(offset_energy),centerError=[round(cx*scale+offset_energy[0]-pivot[0],4),round(cy*scale+offset_energy[1]-pivot[1],4)]))
art['amethyst_gate']=dict(label='Amethyst gate',fps=24,frames=records,role='animation',components=['gate-shell.png','gate-aperture-mask.png','gate_energy'])
registered['amethyst_gate']=gate_frames
analysis['amethyst_gate']=dict(maxCenterError=max(max(abs(e) for e in a['centerError']) for a in records),shellFixed=True)

main=['amethyst_gate','black_void','blue_rift','red_rift']
for name,frames in registered.items():
    # Sprite sheets use their declared common canvas dimensions. The preview
    # never shrinks individual frames to changing alpha bounds.
    fw,fh=frames[0].size;sheet=Image.new('RGBA',(fw*4,fh*8))
    for i,frame in enumerate(frames):sheet.paste(frame,(i%4*fw,i//4*fh))
    sheet.save(OUT/f'{name}-sheet.png',optimize=True)
    art[name]['sheet']=dict(path=(OUT/f'{name}-sheet.png').relative_to(ROOT).as_posix(),columns=4,rows=8,cell=[fw,fh])
    seq=[np.asarray(im).astype('float32') for im in frames]
    distances=[float(np.abs(seq[i]-seq[(i+1)%32]).mean()) for i in range(32)]
    analysis[name]['seamChange']=round(distances[-1],4)
    analysis[name]['medianFrameChange']=round(float(np.median(distances[:-1])),4)
    analysis[name]['seamToMedian']=round(distances[-1]/max(.001,float(np.median(distances[:-1]))),3)
    # Onion evidence uses every frame at one fixed declared pivot/canvas.
    strip=Image.new('RGB',(4*256,8*284),'#101c24');draw=ImageDraw.Draw(strip)
    for i,frame in enumerate(frames):
        field=Image.new('RGBA',frame.size,'#101c24')
        for j,alpha in [((i-2)%32,.14),((i-1)%32,.24),(i,1)]:
            layer=frames[j].copy();layer.putalpha(layer.getchannel('A').point(lambda v:round(v*alpha)))
            field=Image.alpha_composite(field,layer)
        k=min(240/fw,248/fh);thumb=field.resize((round(fw*k),round(fh*k)),Image.Resampling.NEAREST)
        x=i%4*256+(256-thumb.width)//2;y=i//4*284+28
        strip.paste(thumb.convert('RGB'),(x,y));px=x+art[name]['frames'][0]['pivot'][0]*k;py=y+art[name]['frames'][0]['pivot'][1]*k
        draw.line((px-5,py,px+5,py),fill='#89ffa0');draw.line((px,py-5,px,py+5),fill='#89ffa0')
        draw.text((i%4*256+12,i//4*284+8),f'{i+1:02d} / 32',fill='#d9e8ed')
    strip.save(QA/f'{name}-onion.png')
    if name in main:
        frames[0].save(OUT/f'{name}.webp',save_all=True,append_images=frames[1:],duration=round(1000/art[name]['fps']),loop=0,lossless=True,method=3)

manifest=dict(generator='built-in image_gen',main=main,art=art,alignment=analysis,
    sourceFiles={p.name:sha(p) for p in SRC.glob('*.png')},
    rejected={'blue-v1-rejected.png':'Initial glow envelopes were too close to neighboring cells; regenerated.'},
    rules='Even fixed canvases, measured aperture anchors, common proportional scale; integer translation only. No rotated/tweened duplicates.',
    prompts='_ART_SOURCES/portals_1011/prompts.json',status='generated-review-pack')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
(ROOT/'assets/portal_art_1011.js').write_text('"use strict";\n// Generated by build_portals_1011.py.\nconst PR11_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(QA/'alignment.json').write_text(json.dumps(analysis,indent=2)+'\n',encoding='utf-8',newline='\n')
tax=ROOT/'assets/data/ART_TAXONOMY.json'
taxonomy=json.loads(tax.read_text(encoding='utf-8'))
taxonomy['pr11_']=dict(role='portal_and_black_void_review_pack',sheet=None,
    note='October11: four generated32-pose loops matching Mike\'s portal.gif,void-portal.gif,tp.gif,tp2.gif. Amethyst gate512x640/pivot256,352 with immutable authored shell; blue/red rifts and black tunnel320x320/pivot160,160. Separate32-pose gate membrane. Aperture registration by integer translation, common proportional scales; no synthetic rotated/tweened duplicates. Native alpha retained; black tunnel intentionally opaque. Original image_gen outputs/prompts _ART_SOURCES/portals_1011. Owner build_portals_1011.py registers all160 cells, sheets and portal_art_1011.js together. Review docs/previews/portals_1011/index.html, QA docs/qa/portals_1011.json. Review pack only, not assigned to live encounters.')
tax.write_text(json.dumps(taxonomy,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({name:{k:v for k,v in values.items() if k!='sourceAnchors'} for name,values in analysis.items()}),flush=True)
