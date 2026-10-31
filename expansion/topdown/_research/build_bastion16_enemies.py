"""Own the authored Level 7 enemy banks. No procedural sprite drawing.

Source figures are isolated by their connected alpha, never split on approximate
AI sheet row boundaries. This prevents previous-row boots over the next head.
One common .5 nearest-neighbor scale per role, binary alpha and fixed even cell.
"""
from pathlib import Path
import json, hashlib, statistics
import numpy as np
from scipy.ndimage import label, find_objects
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'expansion/topdown/art/bastion16_enemies'
SRC = OUT/'source'
FR = OUT/'frames'
QA = ROOT/'_shots/bastion16_enemies'
FR.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)
CELL = (192, 256)
ANCHOR = (96, 224)
SCALE = .5
ACTIONS = [('idle',4,6),('walk',8,12),('fire',4,14),('vault',6,10),('death',6,9)]
FIRE_MUZZLES = {
    'rifle':[(95,154),(94,150),(95,154),(95,155)],
    'heavy':[(96,170),(96,166),(96,158),(96,170)],
    'rocket':[(105,151),(102,151),(104,150),(102,151)],
    'laser':[(96,163),(94,154),(98,151),(96,162)],
}
D = {'version':'1013-bastion16-enemies-r1', 'assets':{}, 'sequences':{}, 'audit':[], 'sources':{},
     'contract':{'cell':CELL,'anchor':ANCHOR,'sourceScale':SCALE,'alphaThreshold':128,
       'normalization':'connected authored figure isolation; one role-wide proportional nearest scale; integer root registration',
       'palette':'authored slate/ink/copper with purple, red-orange or cyan role accents',
       'generationTool':'built-in image_gen; exact prompt files in source/'}}

for role in ('rifle','heavy','rocket','laser'):
    path=SRC/(role+'.png')
    sheet=Image.open(path).convert('RGBA')
    rgba=np.array(sheet)
    labs,total=label(rgba[:,:,3]>=128,np.ones((3,3),dtype=bool))
    objects=find_objects(labs)
    candidates={}
    for ix,sl in enumerate(objects,1):
        yy,xx=np.where(labs[sl]==ix)
        if len(xx)<300: continue
        cx=float(np.mean(xx)+sl[1].start);cy=float(np.mean(yy)+sl[0].start)
        col=max(0,min(3,int(cx*4/sheet.width)))
        row=max(0,min(6,int(cy*7/sheet.height)))
        index=row*4+col
        if index not in candidates or len(xx)>candidates[index]['pixels']:
            candidates[index]={'label':ix,'pixels':len(xx),'box':(sl[1].start,sl[0].start,sl[1].stop,sl[0].stop)}
    assert len(candidates)==28,(role,len(candidates))
    frames=[]
    ground_refs=[]
    for index in range(16):
        b=candidates[index]['box']; row=index//4
        ground_refs.append(b[3]-round(row*sheet.height/7))
    source_base=statistics.median(ground_refs)
    action_index=0
    for action,count,fps in ACTIONS:
        keys=[]
        for phase in range(count):
            index=action_index+phase;obj=candidates[index];b=obj['box'];row=index//4;col=index%4
            local=rgba[b[1]:b[3],b[0]:b[2]].copy()
            mask=labs[b[1]:b[3],b[0]:b[2]]==obj['label']
            local[:,:,3]=np.where(mask,255,0).astype(np.uint8)
            local[:,:,:3][~mask]=0
            cut=Image.fromarray(local,'RGBA')
            top_band=mask[:max(8,round(mask.shape[0]*.18))]
            _,head_x=np.where(top_band)
            root_x=b[0]+float(np.median(head_x))
            if action=='death':
                # Falling backwards retains the center of the same ground lane;
                # do not re-fit or enlarge the foreshortened body.
                root_x=(col+.5)*sheet.width/4
                root_y=round(row*sheet.height/7)+source_base
            elif action=='vault':
                # Authored crouch / airborne tuck / landing root elevation stays.
                root_y=round(row*sheet.height/7)+source_base
            else:
                root_y=b[3]
            size=(round(cut.width*SCALE),round(cut.height*SCALE))
            offset=(round(ANCHOR[0]+(b[0]-root_x)*SCALE),round(ANCHOR[1]+(b[1]-root_y)*SCALE))
            assert min(offset)>0 and offset[0]+size[0]<CELL[0] and offset[1]+size[1]<CELL[1],(role,action,phase,offset,size)
            im=Image.new('RGBA',CELL)
            im.alpha_composite(cut.resize(size,Image.Resampling.NEAREST),offset)
            bounds=im.getchannel('A').getbbox()
            key=f'pb16_{role}_{action}_{phase}'
            dest=FR/(key+'.png');im.save(dest,optimize=True)
            # The authored forward-facing circular barrel is at lower sternum.
            muzzle=[round(ANCHOR[0]),round(offset[1]+cut.height*.43*SCALE)]
            if action=='fire':muzzle=list(FIRE_MUZZLES[role][phase])
            D['assets'][key]={'file':dest.relative_to(ROOT).as_posix(),'size':CELL,'anchor':ANCHOR,'bounds':bounds,'muzzle':muzzle,
                'role':role,'action':action,'phase':phase,'vaultLiftBaked':action=='vault'}
            D['audit'].append({'key':key,'source':path.name,'sourceRect':b,'sourceComponent':obj['label'],
                'sourceRoot':[root_x,root_y],'scale':SCALE,'offset':offset,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
            frames.append(im);keys.append(key)
        D['sequences'][f'pb16_{role}_{action}']={'frames':keys,'fps':fps,'loop':action in ('idle','walk','fire'),
             'rootContract':{'cell':CELL,'anchor':ANCHOR,'commonSourceScale':SCALE},
             'phaseNames':(['left_contact','left_load','right_pass','right_swing','right_contact','right_load','left_pass','left_swing'] if action=='walk' else [])}
        # Adjacent authored frames, not synthetic in-betweens.
        contact=Image.new('RGBA',(CELL[0]*count,CELL[1]),(24,31,43,255))
        onion=contact.copy()
        for phase,key in enumerate(keys):
            im=Image.open(FR/(key+'.png'))
            contact.alpha_composite(im,(phase*CELL[0],0))
            for neighbor,opacity in (((phase-1)%count,65),((phase+1)%count,65),(phase,210)):
                q=Image.open(FR/(keys[neighbor]+'.png'))
                q.putalpha(q.getchannel('A').point(lambda a:a*opacity//255))
                onion.alpha_composite(q,(phase*CELL[0],0))
            d=ImageDraw.Draw(onion)
            d.line((phase*CELL[0]+ANCHOR[0],0,phase*CELL[0]+ANCHOR[0],CELL[1]),fill=(65,150,150,255))
            d.line((phase*CELL[0],ANCHOR[1],(phase+1)*CELL[0],ANCHOR[1]),fill=(65,150,150,255))
        contact.convert('RGB').save(QA/f'pb16_{role}_{action}_contact.png')
        onion.convert('RGB').save(QA/f'pb16_{role}_{action}_onion.png')
        action_index+=count
    idle_keys=D['sequences'][f'pb16_{role}_idle']['frames']
    height=statistics.median(D['assets'][k]['bounds'][3]-D['assets'][k]['bounds'][1] for k in idle_keys)
    target=135 if role=='heavy' else 115
    draw_scale=target/height
    for key,meta in D['assets'].items():
        if meta['role']==role:meta['drawScale']=draw_scale
    for key,meta in D['sequences'].items():
        if key.startswith('pb16_'+role+'_'):meta['drawScale']=draw_scale
    contact=Image.new('RGBA',(4*CELL[0],7*CELL[1]),(24,31,43,255))
    for index,im in enumerate(frames):contact.alpha_composite(im,((index%4)*CELL[0],(index//4)*CELL[1]))
    contact.convert('RGB').save(QA/(role+'_all.png'))
    D['sources'][role]={'file':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'sourceSize':sheet.size,'prompt':(SRC/(role+'_prompt.txt')).relative_to(ROOT).as_posix(),'drawScale':draw_scale,'targetHeight':target}

assert len(D['assets'])==112 and len(D['sequences'])==20
for key,meta in D['assets'].items():
    im=Image.open(ROOT/meta['file'])
    assert im.size==CELL
    assert set(np.unique(np.asarray(im)[:,:,3])).issubset({0,255})
    assert all(n%2==0 for n in im.size)
    b=im.getchannel('A').getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<CELL[0] and b[3]<CELL[1]
    _,components=label(np.asarray(im)[:,:,3]>0,np.ones((3,3)))
    meta['opaqueComponents']=int(components)

(OUT/'manifest.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
(OUT/'manifest.js').write_text('window.TD_BASTION16_ENEMY_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps({'frames':len(D['assets']),'banks':len(D['sequences']),'sources':D['sources'],'review':str(QA)}))
