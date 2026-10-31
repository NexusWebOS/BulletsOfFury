"""Export reviewed PixelLab banks for Overdrive. No per-frame fit or stretching.
Usage: python build_pixellab38.py --source <review-build> --game <repository>
"""
from pathlib import Path
from PIL import Image
import argparse, json, hashlib, math, shutil

ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--game',required=True);args=ap.parse_args()
S=Path(args.source).resolve();G=Path(args.game).resolve();O=G/'expansion/topdown/art/pixellab38';O.mkdir(parents=True,exist_ok=True)
data=json.loads((S/'review/manifest.json').read_text());index={(b['master'],b['action'],b['direction']):b for b in data['banks']}
assets={};banks={};sources=[]
def even(n):return math.ceil(n/2)*2
def rel(p):return p.relative_to(G).as_posix()
def export(master,action,direction='south',factor=1,indices=None,alias=None,muzzle=None):
    b=index[(master,action,direction)];name=alias or '/'.join([master,action,direction]);safe=name.replace('/','_');folder=O/'banks'/safe;folder.mkdir(parents=True,exist_ok=True)
    ids=indices if indices is not None else range(len(b['frames']));ims=[]
    w,h=even(b['size'][0]*factor),even(b['size'][1]*factor);root=[round(n*factor) for n in b['root']]
    for i,ix in enumerate(ids):
        src=(S/'review'/b['frames'][ix]).resolve();im=Image.open(src).convert('RGBA');im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST)
        cell=Image.new('RGBA',(w,h));cell.paste(im,(0,0));ims.append(cell)
    cols=min(8,len(ims));sheet=Image.new('RGBA',(cols*w,math.ceil(len(ims)/cols)*h));keys=[];offsets=b.get('muzzle_offsets')
    for n,(ix,im) in enumerate(zip(ids,ims)):
        rect=[n%cols*w,n//cols*h,w,h];sheet.paste(im,rect[:2]);key='pl38_'+safe+'_'+str(n);keys.append(key)
        ports={}
        if isinstance(offsets,dict):ports={p:[root[j]+round(v[ix][j]*factor) for j in range(2)] for p,v in offsets.items()}
        elif offsets:ports={'main':[root[j]+round(offsets[ix][j]*factor) for j in range(2)]}
        elif muzzle:ports={'main':[root[j]+round(muzzle[j]*factor) for j in range(2)]}
        elif b.get('muzzle_offset'):ports={'main':[root[j]+round(b['muzzle_offset'][j]*factor) for j in range(2)]}
        if master.startswith('yuri_'):
            # Author barrel sockets from opaque hardware, excluding warm muzzle
            # and projectile pixels. This changes metadata, never the drawing.
            if master=='yuri_side':
                band=(-24,-8) if action in ['prone_fire','prone_idle','crawl'] else (-60,-34) if 'crouch' in action else (-78,-53)
                yy0=max(0,root[1]+band[0]);yy1=min(h,root[1]+band[1]);east=direction=='east'
                candidates=[(x,y) for y in range(yy0,yy1) for x in range(w) if (x>root[0]+14 if east else x<root[0]-14) and im.getpixel((x,y))[3] and max(im.getpixel((x,y))[:3])<170]
                if candidates:
                    edge=(max if east else min)(x for x,y in candidates);ys=[y for x,y in candidates if x==edge];ports={'main':[edge,sorted(ys)[len(ys)//2]]}
            else:
                # North-facing rifle is raised on Yuri's right, beside his head.
                candidates=[(x,y) for y in range(max(0,root[1]-112),root[1]-40) for x in range(root[0]-4,min(w,root[0]+25)) if im.getpixel((x,y))[3] and max(im.getpixel((x,y))[:3])<170]
                if candidates:
                    top=min(y for x,y in candidates);xs=[x for x,y in candidates if y==top];ports={'main':[sorted(xs)[len(xs)//2],top]}
        assets[key]={'file':rel(folder/'sheet.png'),'rect':rect,'size':[w,h],'anchor':root,'bounds':list(im.getbbox()),'drawScale':1,'phase':n,'bank':name,'provider':'PixelLab'}
        if ports:assets[key].update(muzzle=next(iter(ports.values())),muzzles=ports,emitter=next(iter(ports.values())))
    sheet.save(folder/'sheet.png')
    q={'frames':keys,'fps':b.get('fps',12),'loop':b.get('loop',False) if indices is None else len(ims)>1,'events':b.get('events',{}) if indices is None else {},'origin':root,'size':[w,h],'duration':len(keys)/b.get('fps',12),'provider':'PixelLab','source_review':b.get('visual_review','pending'),'export_scale':factor,'source_master':master,'source_action':action,'source_direction':direction,'source_indices':list(ids)}
    banks[name]=q;(folder/'clip.json').write_text(json.dumps(q,indent=2))
    sources.append({'bank':name,'source':b['frames'][0],'source_review':b.get('visual_review'),'sha256':hashlib.sha256(sheet.tobytes()).hexdigest(),'source_count':len(b['frames']),'export_scale':factor})
    return q

front={'machine_gunner':(0,-32),'sniper':(0,-37),'rocket_launcher':(-8,-35),'shotgunner':None,'double_barrel':None,'flamethrower':(-1,-34),'flying_alien':(0,-30),'roller_alien':(0,-33),'minigunner':None}
for role,port in front.items():
    factor=1.25 if role=='minigunner' else 2.25
    export(role+'_pseudo3d','fire',factor=factor,muzzle=port)
    # A source ready pose is quiet and shares the firing hardware and body unit.
    export(role+'_pseudo3d','fire',factor=factor,indices=[0],alias=role+'_pseudo3d/ready/south',muzzle=port)
    if role=='minigunner':
        for a in ['spin_up','spin_down']:export(role+'_pseudo3d',a,factor=factor)
    elif (role+'_pseudo3d','draw_forward','south') in index and role not in ['sniper','double_barrel']:
        export(role+'_pseudo3d','draw_forward',factor=factor,muzzle=port)
export('double_barrel_pseudo3d','reload',factor=2.25,muzzle=(-1,-40))
# Matching clean locomotion. Mirroring preserves the complete source bank.
for a in ['idle','walk','run','fire','run_fire','crouch_enter','prone_enter','prone_idle','prone_fire','crawl','roll']:
    export('yuri_side',a,'east',muzzle=(53,-64) if a in ['fire','run_fire'] else None)
for name,q in list(banks.items()):
    if not name.startswith('yuri_side/') or not name.endswith('/east'):continue
    mirrored=name[:-4]+'west';folder=O/'banks'/mirrored.replace('/','_');folder.mkdir(parents=True,exist_ok=True);w,h=q['size'];cols=min(8,len(q['frames']));sheet=Image.new('RGBA',(cols*w,math.ceil(len(q['frames'])/cols)*h));keys=[]
    for i,k in enumerate(q['frames']):
        m=assets[k];src=Image.open(G/m['file']).convert('RGBA');x,y,_,_=m['rect'];cell=src.crop((x,y,x+w,y+h)).transpose(Image.Transpose.FLIP_LEFT_RIGHT);rect=[i%cols*w,i//cols*h,w,h];sheet.paste(cell,rect[:2]);nk='pl38_'+mirrored.replace('/','_')+'_'+str(i);keys.append(nk)
        n={**m,'file':rel(folder/'sheet.png'),'rect':rect,'anchor':[w-q['origin'][0],q['origin'][1]],'bounds':list(cell.getbbox()),'bank':mirrored}
        if m.get('muzzle'):n.update(muzzle=[w-1-m['muzzle'][0],m['muzzle'][1]],emitter=[w-1-m['muzzle'][0],m['muzzle'][1]],muzzles={p:[w-1-v[0],v[1]] for p,v in m['muzzles'].items()})
        assets[nk]=n
    sheet.save(folder/'sheet.png');banks[mirrored]={**q,'frames':keys,'origin':[w-q['origin'][0],q['origin'][1]],'derivation':'whole-bank horizontal mirror of reviewed east bank'}
for a in ['idle','walk','run','fire','crouch_enter','prone_enter','prone_idle','prone_fire']:
    export('yuri_topdown',a,'north',muzzle=(0,-83))
# Boss plates are kept whole; the incomplete volley banks are excluded.
export('gosfer_pseudo3d','fire',muzzle=(0,-84))
export('gosfer_pseudo3d','fire',indices=[0],alias='gosfer_topdown/ready/south',muzzle=(0,-84))
for di in ['east','west','south','north']:export('gosfer_topdown','walk',di,muzzle=(0,-84))
for di in ['south','north']:export('fire_prism_topdown','prism_lightning',di,factor=2,muzzle=(0,-82))
for b in data['banks']:
    if b['family'] in ['door_core','floor_hatch','electrical_gate','elevator_door','wall_turret_gun'] and b.get('visual_review') in ['material animation reviewed','mechanics reviewed']:
        f=664/512 if b['family']=='electrical_gate' else .5 if b['family']=='door_core' else .75 if b['family']=='wall_turret_gun' else 1
        export(b['master'],b['action'],b['direction'],factor=f)

# Native PixelLab effect sheets retain exact frame durations and origin.
fx=json.loads((S/'effects/manifest.json').read_text());directions=json.loads((S/'effects/directional-manifest.json').read_text())['effects']
for e in fx['native_effects']:
    if not e['id'].endswith('toward_viewer') and e['id']!='forward_muzzle_flash':continue
    meta=json.loads((S/e['metadata']).read_text());frames=meta['frames'];rects=[f['frame'] if isinstance(f.get('frame'),list) else [f['frame']['x'],f['frame']['y'],f['frame']['w'],f['frame']['h']] for f in frames] if isinstance(frames,list) and 'frame' in frames[0] else None
    if rects is None:
        if isinstance(frames,dict):frames=list(frames.values())
        rects=[[f['x'],f['y'],f['width'],f['height']] for f in frames]
    name='fx/'+e['id'];target=O/'effects'/e['id'];target.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/e['atlas'],target/'sheet.png');keys=[]
    for i,rect in enumerate(rects):
        k='pl38_fx_'+e['id']+'_'+str(i);keys.append(k);assets[k]={'file':rel(target/'sheet.png'),'rect':rect,'size':e['canvas'],'anchor':e['origin'],'bounds':[0,0,*e['canvas']],'drawScale':1,'phase':i,'bank':name}
    banks[name]={'frames':keys,'fps':1000/e['durations_ms'][0],'durations_ms':e['durations_ms'],'loop':True,'duration':sum(e['durations_ms'])/1000,'provider':'PixelLab'}
for e in directions:
    name='fx/'+e['id'];target=O/'effects'/e['id'];target.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/e['atlas'],target/'sheet.png');keys=[]
    for i,rect in enumerate(e['frame_rects']):
        k='pl38_'+name.replace('/','_')+'_'+str(i);keys.append(k);assets[k]={'file':rel(target/'sheet.png'),'rect':rect,'size':e['canvas'],'anchor':e['origin'],'bounds':[0,0,*e['canvas']],'drawScale':1,'phase':i,'bank':name}
    banks[name]={'frames':keys,'fps':1000/e['durations_ms'][0],'durations_ms':e['durations_ms'],'loop':True,'duration':sum(e['durations_ms'])/1000,'provider':'PixelLab','derivation':e['derivation']}

def still(name,src,origin=(0,0),im=None):
    if im is None:im=Image.open(S/src).convert('RGBA')
    p=O/'environment'/f'{name}.png';p.parent.mkdir(exist_ok=True);im.save(p)
    key='pl38_'+name;assets[key]={'file':rel(p),'size':list(im.size),'anchor':list(origin),'bounds':list(im.getbbox()),'drawScale':1};return key
for name in ['prism_bastion_far','prism_bastion_foreground_clean','service_corridor_far','service_corridor_foreground']:
    still(name,f'environment/{name}/000.png')
# Use the floor material only; layout geometry continues to come from Level36.
ground=Image.open(S/'levels/level3-ground.png').convert('RGBA');tile=ground.crop((48+48,144+36*30,48+96,144+36*31))
floor=Image.new('RGBA',(800,2800))
for y in range(0,2800,36):
    for x in range(0,800,48):floor.paste(tile,(x,y))
still('fortress_floor','levels/level3-ground.png',im=floor)

report={'build':'overdrive1017-pixellab38-r1','assets':assets,'banks':banks,'sequences':{},'sources':sources,'counts':{'banks':len(banks),'frames':sum(len(q['frames']) for q in banks.values()),'atlases':len(set(a['file'] for a in assets.values()))},'limitations':['Only reviewed source frames selected; incomplete pump reload and clipped boss volleys retained on the existing game paths.','Native Chromium playtest blocked by disabled browser setting; required before release.']}
(O/'manifest.json').write_text(json.dumps(report,indent=2))
(O/'manifest.js').write_text('window.TD_PIXELLAB38_ART='+json.dumps(report,separators=(',',':'))+';Object.assign(window.TD_ASSAULT_ART.assets,window.TD_PIXELLAB38_ART.assets);\n')
(O/'provenance.json').write_text(json.dumps(sources,indent=2))
print(json.dumps(report['counts']))
