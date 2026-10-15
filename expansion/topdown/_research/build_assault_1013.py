"""Owning export for the 1013 infantry/fortress/convoy art. Never repaints source.

The generator returned several odd source cells. Exporting into shared 256/384
transparent canvases preserves every crop at 1:1 scale; no individual pose fit,
mirroring, or synthetic rotation. The runtime applies one scale per actor bank.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/art/assault_1013'
SRC = OUT / 'source'
FRAMES = OUT / 'frames'
FRAMES.mkdir(exist_ok=True)
REVIEW = ROOT / '_shots/overdrive_assault_1013'
REVIEW.mkdir(parents=True, exist_ok=True)
data = {'version': '1013-assault-r1', 'assets': {}, 'sequences': {}, 'audit': []}

def save(key, im, anchor, source=None, crop=None):
    assert im.width % 2 == im.height % 2 == 0, (key, im.size)
    path = FRAMES / (key + '.png')
    im.save(path, optimize=True)
    bounds = im.getchannel('A').point(lambda a: 255 if a > 32 else 0).getbbox()
    data['assets'][key] = dict(file=path.relative_to(ROOT).as_posix(), size=list(im.size), anchor=anchor, bounds=bounds)
    if source:
        data['audit'].append(dict(key=key, source=source, crop=crop, scale=1, bounds=bounds))

def cells(filename, cols, rows, canvas, anchor, source_anchor, skip=()):
    im = Image.open(SRC / filename).convert('RGBA')
    # Full-sheet connected components recover feet crossing nominal grid lines
    # and exclude neighboring-frame crumbs without changing the authored pixels.
    mask=np.asarray(im.getchannel('A'))>32
    parents=[]; runs=[]; previous=[]
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
    components={}
    for x0,x1,y,label in runs:
        k=root(label);q=components.setdefault(k,{'box':[x0,y,x1,y+1],'area':0,'runs':[]})
        b=q['box'];b[0]=min(b[0],x0);b[1]=min(b[1],y);b[2]=max(b[2],x1);b[3]=max(b[3],y+1);q['area']+=x1-x0;q['runs'].append((x0,x1,y))
    bodies=[q for q in components.values() if q['area']>450]
    result = []
    for row in range(rows):
        line = []
        for col in range(cols):
            if row in skip:
                line.append((None,None));continue
            box = (round(col*im.width/cols), round(row*im.height/rows), round((col+1)*im.width/cols), round((row+1)*im.height/rows))
            candidates=[q for q in bodies if int((q['box'][0]+q['box'][2])/2/(im.width/cols))==col and int((q['box'][1]+q['box'][3])/2/(im.height/rows))==row]
            assert candidates,(filename,row,col,'no principal drawing')
            body=max(candidates,key=lambda q:q['area']);b=body['box']
            # Include detached muzzle flashes/casings only when they are close to
            # this actor, not any other actor's large connected silhouette.
            keep=[body]+[q for q in components.values() if 8<q['area']<450 and q['box'][0]>=b[0]-18 and q['box'][2]<=b[2]+18 and q['box'][1]>=b[1]-8 and q['box'][3]<=b[3]+8]
            crop=(min(q['box'][0] for q in keep)-2,min(q['box'][1] for q in keep)-2,max(q['box'][2] for q in keep)+2,max(q['box'][3] for q in keep)+2)
            cell=im.crop(crop);sel=Image.new('L',cell.size);pen=ImageDraw.Draw(sel)
            for q in keep:
                for x0,x1,y in q['runs']:pen.line((x0-crop[0],y-crop[1],x1-1-crop[0],y-crop[1]),fill=255)
            sel=sel.filter(ImageFilter.MaxFilter(5))
            alpha=np.asarray(cell.getchannel('A')).copy();alpha[np.asarray(sel)==0]=0;cell.putalpha(Image.fromarray(alpha))
            frame = Image.new('RGBA', (canvas,canvas))
            sa=source_anchor(row) if callable(source_anchor) else source_anchor
            frame.alpha_composite(cell, (round(anchor[0]-sa[0]+crop[0]-box[0]),round(anchor[1]-sa[1]+crop[1]-box[1])))
            line.append((frame,crop))
        result.append(line)
    return result

directions = ['south','southwest','west','northwest','north','northeast','east','southeast']
actions = ['walk','run_fire','jump','crouch','roll','prone_fire','crawl','peek']
for direction in directions:
    filename = 'yuri_'+direction+'.png'
    bank = cells(filename,6,8,256,[128,224],[90.5,178],(5,6) if direction in ('west','east') else ())
    for row,action in enumerate(actions):
        keys = []
        for col,(im,box) in enumerate(bank[row]):
            if im is None:continue
            key = 'od_yuri_'+direction+'_'+action+'_'+str(col)
            save(key,im,[128,224],filename,box)
            keys.append(key)
        data['sequences']['yuri_'+direction+'_'+action] = dict(frames=keys,fps=12 if action in ('run_fire','roll') else 10)

bank=cells('yuri_lateral_prone_v2.png',6,4,320,[160,260],[128,224])
for row,(direction,action) in enumerate([('west','prone_fire'),('west','crawl'),('east','prone_fire'),('east','crawl')]):
    keys=[]
    for col,(im,box) in enumerate(bank[row]):
        # A single common .75 scale for this entire replacement bank matches the
        # source body's physical size to the unchanged walking bank.
        im=im.resize((240,240),Image.Resampling.NEAREST)
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(im,(8,29))
        key='od_yuri_'+direction+'_'+action+'_'+str(col)
        save(key,frame,[128,224],'yuri_lateral_prone_v2.png',box);data['audit'][-1]['scale']=.75;keys.append(key)
    data['sequences']['yuri_'+direction+'_'+action]=dict(frames=keys,fps=10)

bank=cells('infantry_utility.png',6,4,384,[192,300],lambda r:([128,268],[128,292],[128,240],[128,224])[r])
for row,prefix in enumerate(['yuri_death','yuri_grenade','robot_east','elite_east']):
    keys=[]
    for col,(im,box) in enumerate(bank[row]):
        if row<2:
            im=im.resize((268,268),Image.Resampling.NEAREST);delta=(-6,15);scale=268/384
        else:delta=(-64,-80);scale=1
        frame=Image.new('RGBA',(256,256));frame.alpha_composite(im,delta)
        key='od_'+prefix+'_'+str(col);save(key,frame,[128,224] if row<2 else [128,220],'infantry_utility.png',box);data['audit'][-1]['scale']=scale;keys.append(key)
    data['sequences'][prefix]=dict(frames=keys,fps=10)

for filename,cols,rows,size,anchor,src_anchor,prefixes in [
    ('gosfer.png',6,4,320,[160,278],[128,240],['gosfer_south','gosfer_north','gosfer_east','gosfer_west']),
    ('convoy_vehicles.png',4,4,384,[192,192],[156.75,156.75],['silverado','guntruck','gunner','hunter_jet']),
    ('enemy_armor.png',4,4,384,[192,192],[156.75,156.75],['jackal','lancer','manticore','bastion']),
    ('pursuit_robots.png',6,6,256,[128,220],[104.5,199],['robot_north','robot_south','robot_west','elite_north','elite_south','elite_west']),
]:
    bank=cells(filename,cols,rows,size,anchor,src_anchor)
    for row,prefix in enumerate(prefixes):
        keys=[]
        for col,(im,box) in enumerate(bank[row]):
            key='od_'+prefix+'_'+str(col); save(key,im,anchor,filename,box); keys.append(key)
        data['sequences'][prefix]=dict(frames=keys,fps=10)

props=['barrier','barrier_broken','wood','wood_broken','barrel','barrel_broken','crate','crate_broken','wall','wall_broken','server','server_broken','door','door_open','relay','relay_broken']
bank=cells('fortress_props.png',4,4,384,[192,320],[156.75,292])
for i,name in enumerate(props):
    im,box=bank[i//4][i%4]; save('od_cover_'+name,im,[192,320],'fortress_props.png',box)

for name,size in [('fortress_ground',(800,2400)),('night_road',(800,1600))]:
    im=Image.open(SRC/(name+'.png')).convert('RGBA').resize(size,Image.Resampling.NEAREST)
    save('od_'+name,im,[0,0])

(OUT/'manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
(OUT/'manifest.js').write_text('window.TD_ASSAULT_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
# Contact sheets are review output, not runtime art.
for d in ['north','south','east','west']:
    contact=Image.new('RGB',(6*128,8*144),(23,32,39)); draw=ImageDraw.Draw(contact)
    for row,action in enumerate(actions):
        for col,key in enumerate(data['sequences']['yuri_'+d+'_'+action]['frames']):
            im=Image.open(ROOT/data['assets'][key]['file']).resize((128,128),Image.Resampling.NEAREST)
            contact.paste(im,(col*128,row*144),im)
            draw.text((col*128+3,row*144+130),action+' '+str(col),fill='white')
    contact.save(REVIEW/('yuri_'+d+'_review.png'))
print('Exported',len(data['assets']),'even-sized assets;',len(data['sequences']),'authored banks.')
