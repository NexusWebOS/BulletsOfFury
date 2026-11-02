"""Export authored cast key poses with one proportional scale per bank.

No generated motion, mirroring, per-frame fitting or body-part reconstruction.
Near-zero alpha (<=8/255) is export matte residue, not visible character art.
"""
from pathlib import Path
import base64, hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects

R = Path(__file__).resolve().parents[1]
S = R / '_ART_SOURCES/cast_cinematics_1102'
O = R / 'assets/game/shared/cinematics/cast_1102'
P = R / 'docs/previews/cast_cinematics_1102'
O.mkdir(parents=True, exist_ok=True)
P.mkdir(parents=True, exist_ok=True)
PILOTS = ['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
POSES = ['neutral','speaking','salute','walk_left','look_back','back']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parts(path, count, rows):
    image = Image.open(path).convert('RGBA')
    a = np.array(image)
    a[a[:,:,3] <= 8] = 0
    clean = Image.fromarray(a)
    labels, _ = label(a[:,:,3] > 8)
    boxes = [s for s in find_objects(labels) if s and
             (s[0].stop-s[0].start)*(s[1].stop-s[1].start) > 15000]
    assert len(boxes) == count, (path, len(boxes))
    groups = [[] for _ in range(rows)]
    for s in boxes:
        box = [s[1].start, s[0].start, s[1].stop, s[0].stop]
        groups[min(rows-1, int((box[1]+box[3])/2/image.height*rows))].append(box)
    boxes = [b for group in groups for b in sorted(group, key=lambda v:v[0])]
    return clean, boxes

def export_bank(name, source, names, cell, pivot, rows):
    original, boxes = parts(source, len(names), rows)
    anchors = []
    for box in boxes:
        a = np.array(original.crop(box))[:,:,3]
        # Project the hip center to the boot baseline. A lowest-boot alpha band
        # shifts side/rear actors when one boot ends a few pixels lower.
        centers=[]
        for row in a[int(a.shape[0]*.43):int(a.shape[0]*.47)]:
            transitions=np.diff(np.pad((row>32).astype(np.int8),(1,1)))
            runs=list(zip(np.where(transitions==1)[0],np.where(transitions==-1)[0]))
            if runs:
                left,right=max(runs,key=lambda r:r[1]-r[0])
                centers.append((left+right)/2)
        x=float(np.median(centers)) if centers else a.shape[1]/2
        anchors.append((x, a.shape[0]))
    w,h = cell
    scale = min((pivot[0]-32)/max(max(x,b[2]-b[0]-x) for b,(x,y) in zip(boxes,anchors)),
                (pivot[1]-32)/max(b[3]-b[1] for b in boxes))
    folder = O/name
    folder.mkdir(exist_ok=True)
    cols = 3 if len(names)==6 else 2
    atlas = Image.new('RGBA',(w*cols,h*math.ceil(len(names)/cols)))
    records = []
    for i,(pose,box,anchor) in enumerate(zip(names,boxes,anchors)):
        crop = original.crop(box)
        # One affine proportional source scale for the entire bank. The same
        # physical ground pivot is translated into each fixed even canvas.
        tx,ty = pivot[0]-anchor[0]*scale,pivot[1]-anchor[1]*scale
        frame = crop.transform(cell, Image.Transform.AFFINE,
            (1/scale,0,-tx/scale,0,1/scale,-ty/scale), Image.Resampling.NEAREST)
        bounds = frame.getbbox()
        assert bounds and min(bounds[0],bounds[1],w-bounds[2],h-bounds[3]) >= 24, (name,pose,bounds)
        dest = folder/(pose+'.png')
        frame.save(dest, optimize=True)
        atlas.paste(frame,((i%cols)*w,(i//cols)*h))
        records.append({'pose':pose,'key':f'c112_{name}_{pose}',
            'file':dest.relative_to(R).as_posix(),'source_rect':box,
            'source_pivot':[box[0]+anchor[0],box[1]+anchor[1]],
            'bounds':list(bounds),'cell':[i%cols*w,i//cols*h,w,h], 'sha256':sha(dest)})
    atlas_path = folder/'sheet.webp'
    atlas.save(atlas_path,lossless=True,method=6)
    return {'cell':list(cell),'pivot':list(pivot),'scale':scale,
            'source':source.relative_to(R).as_posix(),'source_sha256':sha(source),
            'sheet':atlas_path.relative_to(R).as_posix(),'frames':records}

manifest={'tool':'built-in image_gen','version':'cast-1102-1',
    'notes':'Six authored cutscene key poses per Fury pilot; these are not a continuous turntable or animation. Pilot faces follow current native portraits. Each bank retains one shared source scale and ground pivot. Alpha<=8 export matte only is discarded. No live pilot cutscene owner is replaced.',
    'prompts':'_ART_SOURCES/cast_cinematics_1102/prompts.json','pilots':{}}
for pilot in PILOTS:
    manifest['pilots'][pilot] = export_bank(pilot,S/'generated'/(pilot+'.png'),POSES,(512,1024),(256,976),2)
manifest['chronos'] = export_bank('chronos',S/'generated/chronos-avatars.png',
    ['neutral','turn_right','turn_left','stern'],(512,512),(256,480),2)
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

# A compact source registry; the public draw method remains lazy and uses XART.
registry = {'pilots':{p:{f['pose']:f['key'] for f in bank['frames']} for p,bank in manifest['pilots'].items()},
            'chronos':{f['pose']:f['key'] for f in manifest['chronos']['frames']}}
sources={f['key']:f['file'] for bank in [*manifest['pilots'].values(),manifest['chronos']] for f in bank['frames']}
(R/'assets/cast_cinematics_art_1102.js').write_text("'use strict';\nconst C112_ART="+json.dumps(registry,separators=(',',':'))+';\n'+
    'Object.assign(XART._src,'+json.dumps(sources,separators=(',',':'))+');\n',encoding='utf-8',newline='\n')

contact = Image.new('RGB',(1536,1536),'#142333')
draw = ImageDraw.Draw(contact)
for i,pilot in enumerate(PILOTS):
    frame = Image.open(O/pilot/'neutral.png')
    frame.thumbnail((460,465),Image.Resampling.LANCZOS)
    x,y = (i%3)*512,(i//3)*512
    contact.paste(frame,(x+(512-frame.width)//2,y+30),frame)
    draw.text((x+18,y+12),pilot.upper(),fill='white')
contact.save(P/'all-pilots.jpg',quality=94)
taxonomy_path=R/'assets/data/ART_TAXONOMY.json'
taxonomy=json.loads(taxonomy_path.read_text(encoding='utf-8-sig'))
taxonomy['c112_']={'role':'chronos_helmet_avatars_and_nine_pilot_full_body_cutscene_key_poses',
    'owner':'_BUILD_SOURCE/build_cast_cinematics_1102.py',
    'manifest':'assets/game/shared/cinematics/cast_1102/manifest.json',
    'note':'Built-in image_gen, actual native portrait references and canonical Chronos robot.54 full-body512x1024 pilot key poses and four512x512 head avatars. One source scale per bank/common ground pivot, alpha<=8 export matte cutoff, complete hands/boots. No continuous motion claim. Lazy opt-in pilot library; four existing Chronos avatar aliases resolve the neutral helmet, native ending fade retained. Sources/prompts _ART_SOURCES/cast_cinematics_1102; runtime assets/cast_cinematics_1102.js.'}
taxonomy_path.write_text(json.dumps(taxonomy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\r\n')
# A self-contained review avoids running any persistent repository HTTP server.
embedded=json.loads(json.dumps(manifest))
for bank in [*embedded['pilots'].values(),embedded['chronos']]:
    for frame in bank['frames']:
        frame['file']='data:image/png;base64,'+base64.b64encode((R/frame['file']).read_bytes()).decode('ascii')
review=(P/'index.html').read_text(encoding='utf-8')
review=review.replace("const root='../../../'","const root=''")
review=review.replace("fetch(root+'assets/game/shared/cinematics/cast_1102/manifest.json').then(r=>r.json())",'Promise.resolve('+json.dumps(embedded,separators=(',',':'))+')')
review=review.replace('src="all-pilots.jpg"','src="data:image/jpeg;base64,'+base64.b64encode((P/'all-pilots.jpg').read_bytes()).decode('ascii')+'"')
(P/'standalone.html').write_text(review,encoding='utf-8')
print(json.dumps({'pilots':len(PILOTS),'body_frames':54,'chronos_avatars':4,
    'asset_bytes':sum(f.stat().st_size for f in O.rglob('*') if f.is_file())}))
