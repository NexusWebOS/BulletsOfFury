"""Export the approved cast's seated, locomotion and emotional action banks.

One source scale per bank; source-image pixels/poses are never reconstructed.
"""
from pathlib import Path
import base64, io, json, hashlib, math
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/cast_performance_1102'
O=R/'assets/game/shared/cinematics/cast_performance_1102'
P=R/'docs/previews/cast_cinematics_1102'
O.mkdir(parents=True,exist_ok=True)
PILOTS=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
POSES={'movement':['walk_0','walk_1','walk_2','walk_3','run_0','run_1','run_2','run_3'],
       'seated':['sit_idle','sit_speaking','dispatch_side','dispatch_typing','dispatch_command','sit_laugh'],
       'emotion':['sad','angry','ecstatic','happy','jump_cheer','falling','laugh','floor_laugh']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def horizontal_pivot(crop,group):
    if group!='movement':return crop.width/2
    alpha=np.array(crop)[:,:,3];centers=[]
    for row in alpha[int(alpha.shape[0]*.38):int(alpha.shape[0]*.42)]:
        edges=np.diff(np.pad((row>32).astype(np.int8),(1,1)))
        runs=list(zip(np.where(edges==1)[0],np.where(edges==-1)[0]))
        if runs:
            left,right=max(runs,key=lambda r:r[1]-r[0]);centers.append((left+right)/2)
    return float(np.median(centers)) if centers else crop.width/2
def extract(path,count,rows,columns):
    a=np.array(Image.open(path).convert('RGBA'))
    a[a[:,:,3]<=8]=0
    labels,_=label(a[:,:,3]>8)
    slices=find_objects(labels)
    boxes=[(i+1,s) for i,s in enumerate(slices) if s and (s[0].stop-s[0].start)*(s[1].stop-s[1].start)>15000]
    assert len(boxes)==count,(path.name,len(boxes),count)
    # Equal spatial rows, then reading order within the measured row. Sources
    # contain different transparent gutters but exactly the authored actor count.
    grouped=[[] for _ in range(rows)]
    for ident,s in boxes:
        box=[s[1].start,s[0].start,s[1].stop,s[0].stop]
        row=min(rows-1,int((box[1]+box[3])/2/a.shape[0]*rows))
        grouped[row].append((ident,box))
    ordered=[item for row in grouped for item in sorted(row,key=lambda b:b[1][0])]
    assert len(ordered)==count
    crops=[]
    for ident,box in ordered:
        x0,y0,x1,y1=box
        crop=a[y0:y1,x0:x1].copy()
        # A wide pose rectangle can overlap a neighbouring pose's raised arm.
        # Keep only this complete actor/prop component, never those neighbours.
        crop[labels[y0:y1,x0:x1]!=ident]=0
        crops.append(Image.fromarray(crop))
    return crops,[box for _,box in ordered]

manifest={'version':'cast-performance-1102-1','tool':'built-in image_gen','cell':[768,1024],
          'pivot':[384,960],'pilots':{},'chronos':None,'ship_scenes':{},
          'notes':'22 new authored frames per pilot. Four-key stride loops are staged cutscene motion, not new gameplay locomotion. Standing and seated/floor poses keep the shared bank source scale. Jump feet remain visibly raised. Illustrated hangar stills reference fresh exports of each actual live aircraft.'}
registry={'pilots':{},'metadata':{},'chronos':{},'shipScenes':{}}
sources={}
for pilot in PILOTS:
    manifest['pilots'][pilot]={}
    registry['pilots'][pilot]={}
    for group,names in POSES.items():
        source=S/'generated'/f'{pilot}-{group}.png'
        rows=2 if group=='movement' or pilot=='cole' else 3
        columns=4 if group=='movement' or (group=='emotion' and pilot=='cole') else 3 if pilot=='cole' or group=='emotion' else 2
        crops,boxes=extract(source,len(names),rows,columns)
        # Keep low/airborne poses at their actual anatomical size: the common
        # scale comes from the tallest whole actor/prop in this bank.
        height_limit=800 if group=='emotion' else 880
        anchors=[horizontal_pivot(crop,group) for crop in crops]
        scale=min(height_limit/max(b[3]-b[1] for b in boxes),344/max(max(x,b[2]-b[0]-x) for b,x in zip(boxes,anchors)))
        folder=O/pilot/group;folder.mkdir(parents=True,exist_ok=True)
        atlas=Image.new('RGBA',(768*4,1024*math.ceil(len(names)/4)))
        records=[]
        for i,(pose,box) in enumerate(zip(names,boxes)):
            crop=crops[i]
            # Horizontal extent is deliberately reserved for complete dispatch
            # props and falling limbs. There is no per-frame resize.
            x=anchors[i];y=crop.height
            air=100 if pose=='jump_cheer' else 32 if group=='movement' and pose in ['run_1','run_3'] else 0
            tx,ty=384-x*scale,960-air-y*scale
            frame=crop.transform((768,1024),Image.Transform.AFFINE,(1/scale,0,-tx/scale,0,1/scale,-ty/scale),Image.Resampling.NEAREST)
            bounds=frame.getbbox();assert bounds and min(bounds[0],bounds[1],768-bounds[2],1024-bounds[3])>=24,(pilot,pose,bounds)
            file=folder/(pose+'.png');frame.save(file,optimize=True)
            atlas.paste(frame,((i%4)*768,(i//4)*1024))
            key=f'cp112_{pilot}_{pose}'
            record={'pose':pose,'key':key,'file':file.relative_to(R).as_posix(),'source_rect':box,
                    'cell':[i%4*768,i//4*1024,768,1024],'bounds':list(bounds),'air_pixels':air,'sha256':sha(file)}
            records.append(record);registry['pilots'][pilot][pose]=key;sources[key]=record['file'];registry['metadata'][key]={'cell':[768,1024],'pivot':[384,960]}
        sheet=folder/'sheet.webp';atlas.save(sheet,lossless=True,method=4)
        manifest['pilots'][pilot][group]={'source':source.relative_to(R).as_posix(),'source_sha256':sha(source),
                    'scale':scale,'cell':[768,1024],'pivot':[384,960],'source_rows':rows,'source_columns':columns,
                    'sheet':sheet.relative_to(R).as_posix(),'frames':records,
                    'walk_facing':'right','run_facing':'left' if pilot in ['yuri','lizzie'] else 'right'}

source=S/'generated/chronos-dialogue.png'
im=Image.open(source).convert('RGBA');im=im.resize((512,512),Image.Resampling.NEAREST)
a=np.array(im);a[a[:,:,3]<=8]=0;im=Image.fromarray(a)
file=O/'chronos-dialogue.png';im.save(file,optimize=True)
manifest['chronos']={'key':'cp112_chronos_dialogue','file':file.relative_to(R).as_posix(),'cell':[512,512],
                     'source':source.relative_to(R).as_posix(),'source_sha256':sha(source),'sha256':sha(file)}
registry['chronos']['dialogue']='cp112_chronos_dialogue';sources['cp112_chronos_dialogue']=manifest['chronos']['file']
for pilot in PILOTS:
    scene=O/'ship_scenes'/(pilot+'.png')
    illustrated=S/'generated'/(pilot+'-ship-scene.png')
    if illustrated.exists():
        scene.parent.mkdir(parents=True,exist_ok=True)
        plate=Image.open(illustrated).convert('RGB')
        assert plate.size==(1536,1024),(pilot,plate.size)
        plate.save(scene,optimize=True)
    if scene.exists():
        key='cp112_'+pilot+'_ship_scene';record={'key':key,'file':scene.relative_to(R).as_posix(),'cell':[1536,1024],'sha256':sha(scene),
                'source':illustrated.relative_to(R).as_posix(),'source_sha256':sha(illustrated),'reference':f'_ART_SOURCES/cast_performance_1102/references/{pilot}-ship-identity.png'}
        manifest['ship_scenes'][pilot]=record;registry['shipScenes'][pilot]=key;sources[key]=record['file']
(O/'ship_scenes/manifest.json').write_text(json.dumps({'method':'Selected built-in image_gen illustrated stills, guided by exported native aircraft identity references. Native composition guides remain in the source references directory.','scenes':manifest['ship_scenes']},indent=2)+'\n',encoding='utf-8')
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(R/'assets/cast_performance_art_1102.js').write_text("'use strict';\nconst CP112_ART="+json.dumps(registry,separators=(',',':'))+';\nObject.assign(XART._src,'+json.dumps(sources,separators=(',',':'))+');\n',encoding='utf-8',newline='\n')
prompts=json.loads((S/'prompts.json').read_text(encoding='utf-8'))
for spec in (S/'specs').glob('*.json'):prompts[spec.stem]=json.loads(spec.read_text(encoding='utf-8'))
(S/'prompts.json').write_text(json.dumps(prompts,indent=2)+'\n',encoding='utf-8')
taxonomy_path=R/'assets/data/ART_TAXONOMY.json';raw=taxonomy_path.read_bytes();taxonomy=json.loads(raw.decode('utf-8-sig'))
taxonomy['cp112_']={'role':'approved_pilot_seated_dispatch_stride_emotion_and_ship_reference_scenes',
    'owner':'_BUILD_SOURCE/build_cast_performance_1102.py','manifest':'assets/game/shared/cinematics/cast_performance_1102/manifest.json',
    'note':'198 new full-body768x1024 frames (22per pilot), nine1536x1024 illustrated hangar stills referenced from current native aircraft, framed Chronos512x512 dialogue closeup. Current approved faces/outfits, common scale per bank, hip projection for stride registration, visible airborne cheer gap, actual authored poses/no mirroring or runtime rotation. Separate opt-in cutscene library; native Chronos dialogue/fade owners retained. Built-in image_gen sources/prompts and native ship exports retained under _ART_SOURCES/cast_performance_1102.'}
taxonomy_path.write_text(json.dumps(taxonomy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\r\n' if b'\r\n' in raw else '\n')
print(json.dumps({'new_frames':sum(len(bank['frames']) for p in manifest['pilots'].values() for bank in p.values()),'ship_scenes':len(manifest['ship_scenes'])}))
