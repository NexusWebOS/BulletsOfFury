"""Source-preserving mechanical module extraction for the Raiden reference pack.

Masks select measured authored pixels; no hull/weapon pixels are synthesized.
Every module uses its assembly's full fixed canvas and registered coordinates.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt, find_objects, label


NEW_ROSTER = {
    'minibosses': [
        ('olive_assault_tank', 'Olive Assault Tank', 'Armor', 'Twin independent turret housings and barrels on a heavy tracked chassis.', 'heavy_rocket'),
        ('quad_battery_fortress', 'Quad Battery Fortress', 'Fortress', 'Four independent corner cannon assemblies and a separate reactor cover.', 'blue_plasma'),
        ('orange_heavy_bomber', 'Orange Heavy Bomber', 'Air', 'Heavy bomber with separate wings, engine pods and forward cannons.', 'heavy_rocket'),
        ('missile_corvette', 'Missile Corvette', 'Naval', 'Armored corvette with independent racks, turret, barrel, bridge and drives.', 'micro_missile'),
    ],
    'bosses': [
        ('iron_bastion_landship', 'Iron Bastion Landship', 'Landship', 'Massive mobile fortress with four turret/barrel pairs, shoulder missile racks and tracked sponsons.', 'plasma_column'),
        ('dreadnought_battleship', 'Dreadnought Battleship', 'Naval', 'Armored warship with two triple-gun batteries, four secondary batteries and separate stern engines.', 'red_torpedo'),
        ('stormwing_sky_carrier', 'Stormwing Sky Carrier', 'Air', 'Wide carrier aircraft with independent wings, engines, four gun pods and two missile bays.', 'twin_cobalt'),
        ('quad_laser_citadel', 'Quad Laser Citadel', 'Citadel', 'Four heavy laser assemblies, four missile racks, and an independent armored reactor cap.', 'gold_charge'),
    ]
}


def part(key, name, shape, mount, explode, weapon=False, muzzle=None):
    return dict(id=key, name=name, shape=shape, mount=mount, explode=explode,
                weapon=weapon, muzzle=muzzle)


def rect(x0, y0, x1, y1):
    return ('polygon', [(x0,y0),(x1,y0),(x1,y1),(x0,y1)])


def poly(points):
    return ('polygon', points)


def ellipse(box):
    return ('ellipse', box)


def mirror(shape, span=384):
    kind, points = shape
    assert kind == 'polygon'
    return kind, [(span-x,y) for x,y in points]


def pair(name, shape, mount, explode=(-60,0), weapon=False, muzzle=None, span=384):
    return [part('left_'+name, 'Left '+name.replace('_',' '), shape, mount, explode, weapon, muzzle),
            part('right_'+name, 'Right '+name.replace('_',' '), mirror(shape,span), (span-mount[0],mount[1]), (-explode[0],explode[1]), weapon,
                 (span-muzzle[0],muzzle[1]) if muzzle else None)]


def regular_layout(key):
    # Coordinates were measured on the original common 384px masters.
    if key == 'steel_interceptor':
        return (pair('wing',poly([(68,156),(147,137),(165,156),(164,247),(136,236),(70,207)]),(158,191))+
                pair('engine',poly([(157,48),(184,48),(184,154),(170,205),(162,252),(145,252),(145,135)]),(168,148),(-27,-54))+
                pair('gun',rect(116,235,141,278),(130,241),(-38,38),True,(130,269)))
    if key == 'olive_attack_jet':
        return (pair('wing',poly([(40,139),(103,137),(127,177),(128,244),(74,233),(44,210)]),(111,185))+
                pair('engine',rect(104,48,151,255),(130,171),(-36,-52)))
    if key == 'red_needle_fighter':
        return (pair('wing',poly([(72,210),(133,159),(166,133),(164,235),(132,257),(75,252)]),(160,204))+
                pair('engine',rect(133,144,164,283),(148,181),(-29,-48)))
    if key == 'teal_strike_drone':
        return (pair('wing',poly([(50,126),(105,119),(131,151),(131,219),(67,211),(49,191)]),(118,173))+
                pair('engine',rect(104,65,151,262),(129,174),(-40,-46)))
    if key == 'ember_gunship':
        return (pair('wing',poly([(47,113),(126,111),(139,143),(139,220),(73,213),(47,196)]),(129,172))+
                pair('engine',rect(124,52,164,234),(145,151),(-36,-57))+
                pair('rotary_cannon',rect(121,228,166,310),(144,235),(-36,47),True,(143,300)))
    if key == 'delta_bomber':
        return (pair('wing',poly([(30,117),(104,102),(133,131),(134,237),(91,206),(32,158)]),(115,161))+
                pair('engine',poly([(105,95),(137,95),(145,130),(145,239),(103,239),(102,130)]),(126,163),(-34,-55))+
                pair('gun',rect(104,228,135,268),(120,234),(-32,45),True,(120,258)))
    if key == 'quad_nacelle_cruiser':
        return [
            part('upper_left_engine','Upper left engine',rect(78,48,131,134),(110,122),(-40,-49)),
            part('upper_right_engine','Upper right engine',rect(253,48,306,134),(274,122),(40,-49)),
            part('lower_left_engine','Lower left engine',rect(78,224,131,302),(111,235),(-40,49)),
            part('lower_right_engine','Lower right engine',rect(253,224,306,302),(273,235),(40,49)),
            *pair('cannon',rect(34,130,75,226),(66,177),(-66,0),True,(50,217))]
    if key == 'violet_stealth_wing':
        return (pair('wing',poly([(35,107),(160,109),(160,219),(111,206),(71,182),(36,139)]),(157,162))+
                pair('tail_fin',poly([(128,48),(162,77),(173,113),(151,126),(129,91)]),(164,110),(-28,-46))+
                pair('emitter_pod',poly([(88,165),(145,165),(151,205),(140,251),(111,251),(91,226)]),(134,186),(-45,42),True,(126,224)))
    if key == 'scout_tank':
        return [*pair('track',rect(94,68,127,294),(121,189),(-55,0)),
                part('turret','Main turret housing',poly([(148,105),(166,91),(214,91),(236,113),(236,173),(215,195),(166,195),(148,174)]),(192,150),(0,-56)),
                part('barrel','Main cannon barrel',poly([(178,171),(205,171),(205,204),(201,325),(181,325),(178,204)]),(192,180),(0,66),True,(191,312))]
    if key == 'twin_cannon_tank':
        return [*pair('track',rect(86,62,123,293),(117,188),(-58,0)),
                *pair('turret',poly([(125,61),(165,61),(181,93),(181,174),(169,196),(133,196),(123,175),(123,95)]),(153,134),(-36,-43)),
                *pair('barrel',rect(136,173,167,325),(152,181),(-30,59),True,(151,313))]
    if key == 'rocket_carrier':
        parts=pair('track',rect(87,82,111,312),(104,191),(-56,0))
        for i,c in enumerate([147,178,210,240]):
            shape=poly([(c,57),(c+12,77),(c+12,220),(c+8,243),(c-8,243),(c-12,220),(c-12,77)])
            parts.append(part('rocket_'+str(i+1),'Rocket tube '+str(i+1),shape,(c,215),((i-1.5)*28,-54),True,(c,75)))
        return parts
    if key == 'wheeled_flak':
        parts=[]
        for side, x0, x1, dx in [('left',93,135,-52),('right',249,291,52)]:
            for i,(y0,y1) in enumerate([(79,149),(155,217),(226,290)]):
                parts.append(part(f'{side}_wheel_{i+1}',f'{side.title()} wheel {i+1}',rect(x0,y0,x1,y1),((x0+x1)//2,(y0+y1)//2),(dx,(i-1)*18)))
        return parts+pair('autocannon',rect(144,205,176,322),(161,214),(-26,55),True,(160,312))
    if key == 'cannon_bunker':
        return [part('turret_ring','Rotating turret housing',ellipse((117,91,267,244)),(192,168),(0,-61)),
                part('cannon_barrel','Cannon barrel',poly([(179,150),(203,150),(207,177),(201,281),(181,281),(177,177)]),(192,160),(0,66),True,(191,271))]
    if key == 'missile_battery':
        return [part('left_launcher','Left launcher',rect(130,54,169,218),(150,187),(-43,-42),True,(150,66)),
                part('center_launcher','Center launcher',rect(174,83,211,220),(192,191),(0,-72),True,(192,95)),
                part('right_launcher','Right launcher',rect(214,54,252,218),(232,187),(43,-42),True,(231,66))]
    if key == 'river_patrol':
        return [part('bridge','Bridge and sensor block',poly([(168,82),(215,82),(220,144),(210,182),(170,182),(164,143)]),(192,145),(0,-58)),
                *pair('side_battery',rect(138,150,164,233),(160,187),(-47,0),True,(150,223)),
                part('bow_battery','Bow gun battery',ellipse((172,251,211,291)),(192,268),(0,57),True,(192,282))]
    if key == 'iron_siege_craft':
        return (pair('wing',poly([(10,78),(82,103),(112,114),(113,184),(74,223),(12,174)]),(109,151),(-64,0))+
                pair('engine',rect(81,42,139,236),(114,143),(-38,-59))+
                pair('heavy_cannon',poly([(100,223),(134,223),(149,248),(149,286),(138,304),(133,354),(103,354),(99,301),(91,286),(91,249)]),(120,240),(-35,62),True,(118,343)))
    raise ValueError(key)


def normalized_layout(key):
    """Measured mechanical regions in each new source hull's normalized bounds."""
    def nr(name, box, mount, explosion, weapon=False, muzzle=None):
        return part(name,name.replace('_',' ').title(),rect(*box),mount,explosion,weapon,muzzle)
    def npart(name, points, mount, explosion, weapon=False, muzzle=None):
        return part(name,name.replace('_',' ').title(),poly(points),mount,explosion,weapon,muzzle)
    if key=='olive_assault_tank':
        return [nr('left_track',(0,.08,.15,.96),(.14,.5),(-.16,0)),nr('right_track',(.85,.08,1,.96),(.86,.5),(.16,0)),
                nr('left_turret',(.17,.2,.42,.61),(.3,.42),(-.1,-.13)),nr('right_turret',(.58,.2,.83,.61),(.7,.42),(.1,-.13)),
                nr('left_barrel',(.255,.52,.355,1),(.3,.54),(-.09,.17),True,(.3,.98)),nr('right_barrel',(.645,.52,.745,1),(.7,.54),(.09,.17),True,(.7,.98))]
    if key=='quad_battery_fortress':
        return [npart('upper_left_cannon',[(0,0),(.37,0),(.37,.3),(.26,.39),(0,.36)],(.25,.27),(-.15,-.15),True,(.1,.08)),
                npart('upper_right_cannon',[(.63,0),(1,0),(1,.36),(.74,.39),(.63,.3)],(.75,.27),(.15,-.15),True,(.9,.08)),
                npart('lower_left_cannon',[(0,.64),(.26,.61),(.37,.7),(.37,1),(0,1)],(.25,.73),(-.15,.15),True,(.1,.92)),
                npart('lower_right_cannon',[(.63,.7),(.74,.61),(1,.64),(1,1),(.63,1)],(.75,.73),(.15,.15),True,(.9,.92)),
                nr('reactor_cover',(.33,.33,.67,.69),(.5,.5),(0,-.2))]
    if key=='orange_heavy_bomber':
        return [npart('left_wing',[(0,.18),(.28,.18),(.32,.66),(.11,.66),(0,.57)],(.27,.43),(-.17,0)),
                npart('right_wing',[(.72,.18),(1,.18),(1,.57),(.89,.66),(.68,.66)],(.73,.43),(.17,0)),
                nr('left_engine',(.25,0,.43,.75),(.34,.4),(-.09,-.15)),nr('right_engine',(.57,0,.75,.75),(.66,.4),(.09,-.15)),
                nr('left_cannon',(.21,.61,.31,.94),(.26,.66),(-.1,.17),True,(.26,.91)),nr('right_cannon',(.69,.61,.79,.94),(.74,.66),(.1,.17),True,(.74,.91))]
    if key=='missile_corvette':
        return [nr('left_drive',(.21,0,.43,.25),(.32,.2),(-.09,-.16)),nr('right_drive',(.57,0,.79,.25),(.68,.2),(.09,-.16)),
                nr('left_missile_rack',(.01,.2,.24,.66),(.23,.43),(-.17,0),True,(.13,.29)),nr('right_missile_rack',(.76,.2,.99,.66),(.77,.43),(.17,0),True,(.87,.29)),
                npart('bridge',[(.39,.27),(.61,.27),(.65,.31),(.65,.45),(.60,.49),(.40,.49),(.35,.45),(.35,.31)],(.5,.39),(0,-.16)),
                npart('bow_turret',[(.40,.51),(.60,.51),(.67,.58),(.67,.69),(.60,.76),(.40,.76),(.33,.69),(.33,.58)],(.5,.64),(0,.13)),
                npart('bow_barrel',[(.455,.66),(.545,.66),(.565,.70),(.555,.83),(.53,.86),(.47,.86),(.445,.83),(.435,.70)],(.5,.68),(0,.23),True,(.5,.83))]
    if key=='iron_bastion_landship':
        parts=[nr('left_track_sponson',(0,.27,.185,.94),(.17,.59),(-.16,0)),nr('right_track_sponson',(.815,.27,1,.94),(.83,.59),(.16,0)),
               nr('left_missile_rack',(.10,.03,.265,.3),(.2,.27),(-.11,-.14),True,(.18,.07)),nr('right_missile_rack',(.735,.03,.9,.3),(.8,.27),(.11,-.14),True,(.82,.07))]
        for side,x,dx in [('left',.33,-.09),('right',.67,.09)]:
            for end,y,dy in [('upper',.26,-.1),('lower',.74,.1)]:
                end_y=.47 if end=='upper' else .995
                parts.extend([npart(f'{end}_{side}_turret',[(x-.08,y-.16),(x+.08,y-.16),(x+.13,y-.10),(x+.13,y+.045),(x+.075,y+.11),(x-.075,y+.11),(x-.13,y+.045),(x-.13,y-.10)],(x,y),(dx,dy)),
                              npart(f'{end}_{side}_barrel',[(x-.03,y+.035),(x+.03,y+.035),(x+.035,y+.09),(x+.029,end_y),(x-.029,end_y),(x-.035,y+.09)],(x,y+.06),(dx,dy+.13),True,(x,end_y-.015))])
        parts.append(part('command_reactor','Armored command reactor',ellipse((.39,.38,.61,.62)),(.5,.5),(0,-.23)))
        return parts
    if key=='dreadnought_battleship':
        parts=[nr('left_stern_engine',(.23,0,.43,.24),(.34,.2),(-.1,-.14)),nr('right_stern_engine',(.57,0,.77,.24),(.66,.2),(.1,-.14)),
               nr('aft_triple_battery',(.27,.12,.73,.37),(.5,.22),(0,-.19),True,(.5,.34)),
               nr('bow_triple_battery',(.27,.70,.73,.97),(.5,.78),(0,.18),True,(.5,.93)),
               nr('bridge',(.35,.37,.65,.69),(.5,.5),(0,-.12))]
        for side,x0,x1,dx in [('port',0,.33,-.17),('starboard',.67,1,.17)]:
            for i,(y0,y1) in enumerate([(.31,.48),(.53,.7)]):
                parts.append(nr(f'{side}_battery_{i+1}',(x0,y0,x1,y1),(.26 if dx<0 else .74,(y0+y1)/2),(dx,(i-.5)*.12),True,(.02 if dx<0 else .98,(y0+y1)/2)))
        return parts
    if key=='stormwing_sky_carrier':
        return [npart('left_wing',[(0,.19),(.19,.19),(.25,.57),(.15,.68),(0,.48)],(.22,.42),(-.18,0)),
                npart('right_wing',[(.81,.19),(1,.19),(1,.48),(.85,.68),(.75,.57)],(.78,.42),(.18,0)),
                nr('left_engine',(.18,0,.35,.72),(.28,.35),(-.11,-.15)),nr('right_engine',(.65,0,.82,.72),(.72,.35),(.11,-.15)),
                nr('left_missile_bay',(.29,.42,.40,.65),(.35,.54),(-.08,-.04),True,(.35,.45)),nr('right_missile_bay',(.60,.42,.71,.65),(.65,.54),(.08,-.04),True,(.65,.45)),
                nr('outer_left_gun',(.20,.64,.31,.91),(.26,.69),(-.13,.14),True,(.26,.88)),nr('outer_right_gun',(.69,.64,.80,.91),(.74,.69),(.13,.14),True,(.74,.88)),
                nr('inner_left_gun',(.34,.72,.42,.94),(.38,.75),(-.07,.22),True,(.38,.91)),nr('inner_right_gun',(.58,.72,.66,.94),(.62,.75),(.07,.22),True,(.62,.91))]
    if key=='quad_laser_citadel':
        parts=[]
        for side,x,dx in [('left',.2,-.15),('right',.8,.15)]:
            for end,y,dy in [('upper',.22,-.12),('lower',.77,.12)]:
                parts.append(nr(f'{end}_{side}_laser',(max(0,x-.2),max(0,y-.22),min(1,x+.18),min(1,y+.28)),(x,y),(dx,dy),True,(x,min(.99,y+.26))))
        parts += [nr('north_missile_rack',(.4,.05,.60,.26),(.5,.24),(0,-.2),True,(.5,.09)),
                  nr('south_missile_rack',(.4,.72,.60,.94),(.5,.74),(0,.2),True,(.5,.75)),
                  nr('west_missile_rack',(0,.40,.17,.62),(.15,.51),(-.23,0),True,(.08,.44)),
                  nr('east_missile_rack',(.83,.40,1,.62),(.85,.51),(.23,0),True,(.92,.44)),
                  part('reactor_cap','Armored reactor cap',ellipse((.34,.31,.67,.66)),(.5,.49),(0,-.22))]
        return parts
    raise ValueError(key)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(im, path):
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path,optimize=True)


def components(im):
    rgba=np.asarray(im)
    lab,_=label(rgba[:,:,3]>16)
    pieces=[(i,s) for i,s in enumerate(find_objects(lab),1) if s is not None and np.count_nonzero(lab[s]==i)>10000]
    assert len(pieces)==4
    pieces.sort(key=lambda p: ((p[1][0].start+p[1][0].stop)//1200,p[1][1].start))
    seeds=np.zeros(lab.shape,dtype=np.int16)
    for i,(identity,_) in enumerate(pieces,1): seeds[lab==identity]=i
    _,near=distance_transform_edt(seeds==0,return_indices=True)
    owners=seeds[tuple(near)]
    result=[]
    for i,(_,sl) in enumerate(pieces,1):
        x0,y0=max(0,sl[1].start-8),max(0,sl[0].start-8)
        x1,y1=min(im.width,sl[1].stop+8),min(im.height,sl[0].stop+8)
        crop=rgba[y0:y1,x0:x1].copy();crop[owners[y0:y1,x0:x1]!=i]=0
        result.append((Image.fromarray(crop),[x0,y0,x1-x0,y1-y0]))
    return result


def sheet(frames, columns, gutter=8, padding=8):
    w,h=frames[0].size;rows=math.ceil(len(frames)/columns)
    result=Image.new('RGBA',(columns*w+(columns-1)*gutter+2*padding,rows*h+(rows-1)*gutter+2*padding))
    rects=[]
    for i,im in enumerate(frames):
        x,y=padding+(i%columns)*(w+gutter),padding+(i//columns)*(h+gutter)
        result.paste(im,(x,y));rects.append([x,y,w,h])
    return result,rects


def convert_layout(layout, bbox, frame):
    x0,y0,x1,y1=bbox;w,h=x1-x0,y1-y0
    def point(p): return [round(x0+p[0]*w),round(y0+p[1]*h)]
    result=[]
    for p in layout:
        p=dict(p);kind,shape=p['shape']
        p['shape']=(kind,[*point(shape[:2]),*point(shape[2:])] if kind=='ellipse' else [point(v) for v in shape])
        p['mount']=point(p['mount']);p['explode']=[round(v*frame) for v in p['explode']]
        if p['muzzle'] is not None: p['muzzle']=point(p['muzzle'])
        result.append(p)
    return result


def export_modules(asset, out, normalized=False):
    master=Image.open(out/asset['master']).convert('RGBA');rgba=np.array(master)
    support=rgba[:,:,3]>16;yy,xx=np.where(support)
    bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    layout=normalized_layout(asset['id']) if normalized else regular_layout(asset['id'])
    if normalized: layout=convert_layout(layout,bbox,master.width)
    owners=np.zeros((master.height,master.width),dtype=np.int16)
    for i,p in enumerate(layout,1):
        mask=Image.new('L',master.size);draw=ImageDraw.Draw(mask);kind,shape=p['shape']
        if kind=='ellipse': draw.ellipse(shape,fill=255)
        else: draw.polygon([tuple(v) for v in shape],fill=255)
        owners[np.asarray(mask)>0]=i
    # Keep small attachment pixels with their actual adjoining mechanism rather
    # than leaving disconnected slivers on another layer after an exploded cut.
    # This reassigns source pixels only; it never paints, removes or duplicates.
    seeds=np.zeros(owners.shape,dtype=np.int16)
    for i in range(len(layout)+1):
        regions,_=label((owners==i)&support)
        sizes=np.bincount(regions.ravel());sizes[0]=0
        cutoff=max(20,float(sizes.max())*(.05 if i==0 else .10))
        keep=np.flatnonzero(sizes>=cutoff)
        seeds[np.isin(regions,keep)]=i+1
    _,near=distance_transform_edt(seeds==0,return_indices=True)
    owners=seeds[tuple(near)]-1
    core=part('chassis','Central chassis',None,[master.width//2,master.height//2],[0,0])
    layout=[core]+layout
    records=[];masters=[];natives=[];accum=np.zeros(rgba.shape,dtype=np.uint16)
    visible_count=np.zeros(owners.shape,dtype=np.uint8)
    for i,p in enumerate(layout):
        pixels=rgba.copy();pixels[owners!=i]=0
        assert np.count_nonzero(pixels[:,:,3]>16)>50,(asset['id'],p['id'],'empty mechanical module')
        accum+=pixels.astype(np.uint16);visible_count+=(pixels[:,:,3]>0)
        im=Image.fromarray(pixels);native=im.resize((im.width//2,im.height//2),Image.Resampling.NEAREST)
        white=pixels.copy();white[:,:,:3]=255;white[pixels[:,:,3]==0]=0
        hit=Image.fromarray(white);native_hit=hit.resize(native.size,Image.Resampling.NEAREST)
        root=f'modules/{asset["id"]}/{p["id"]}'
        paths=dict(master=root+'-master.png',native=root+'-native.png',hit_master=root+'-hit-master.png',hit_native=root+'-hit-native.png')
        for name,frame in [('master',im),('native',native),('hit_master',hit),('hit_native',native_hit)]: save(frame,out/paths[name])
        alpha=pixels[:,:,3];yy,xx=np.where(alpha>16)
        rec=dict(id=p['id'],name=p['name'],**paths,master_size=list(master.size),native_size=list(native.size),
                 pivot=p['mount'],native_pivot=[v/2 for v in p['mount']],offset=[0,0],
                 explode=p['explode'],native_explode=[v/2 for v in p['explode']],
                 bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],
                 draw_order=i,weapon=p['weapon'],muzzle=p['muzzle'],source_mask=p['shape'],
                 pixels=int(np.count_nonzero(alpha>16)),mask_cleanup='Nearest substantial source contour owns disconnected attachment pixels',sha256={key:sha(out/value) for key,value in paths.items()})
        records.append(rec);masters.append(im);natives.append(native)
    assert np.array_equal(accum.astype(np.uint8),rgba),'Part union differs from authored source'
    assert np.max(visible_count)==1,'Overlapping module pixels'
    # Native sampling commutes with the disjoint masks: this protects registration.
    merged=np.sum([np.asarray(im).astype(np.uint16) for im in natives],axis=0).astype(np.uint8)
    assert np.array_equal(merged,np.asarray(Image.open(out/asset['native']).convert('RGBA')))
    asset.update(modular=True,parts=records,module_count=len(records),assembly_reconstruction='Exact disjoint source-pixel union',
                 suggested_weapon=asset.get('suggested_weapon'),tier={'enemies':'enemy','minibosses':'miniboss','bosses':'boss'}[asset['group']])
    atlas=[]
    for resolution,frames in [('master',masters),('native',natives)]:
        im,rects=sheet(frames,4,8 if resolution=='master' else 4,8 if resolution=='master' else 4)
        path=f'sheets/modules/{asset["id"]}-{resolution}.png';save(im,out/path)
        atlas.append(dict(path=path,resolution=resolution,size=list(im.size),cell_size=list(frames[0].size),columns=4,rows=math.ceil(len(frames)/4),gutter=8 if resolution=='master' else 4,padding=8 if resolution=='master' else 4))
        for p,rect,frame in zip(records,rects,frames):
            p[resolution+'_sheet']=path;p[resolution+'_sheet_rect']=rect
            assert np.array_equal(np.asarray(im.crop((rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]))),np.asarray(frame))
    asset['module_sheets']=atlas
    return len(records)


def extend_catalog(catalog, src, out):
    root=src.parents[1]
    for group,cell,scale in [('minibosses',512,2/3),('bosses',768,1.0)]:
        path=src/'source'/f'{group}.png';source=Image.open(path).convert('RGBA')
        catalog['source'][group]=dict(path=str(path.relative_to(root)).replace('\\','/'),size=list(source.size),sha256=sha(path))
        masters,natives,records=[],[],[]
        for spec,(crop,source_rect) in zip(NEW_ROSTER[group],components(source)):
            key,name,role,desc,weapon=spec
            size=(round(crop.width*scale),round(crop.height*scale))
            assert max(size)<cell-16
            crop=crop.resize(size,Image.Resampling.NEAREST)
            im=Image.new('RGBA',(cell,cell));offset=((cell-size[0])//2,(cell-size[1])//2);im.paste(crop,offset)
            native=im.resize((cell//2,cell//2),Image.Resampling.NEAREST)
            fm,fn=f'master/{group}/{key}.png',f'native/{group}/{key}.png';save(im,out/fm);save(native,out/fn)
            record=dict(id=key,name=name,role=role,group=group,description=desc,suggested_weapon=weapon,
                        master=fm,native=fn,master_size=[cell,cell],native_size=[cell//2,cell//2],pivot=[cell//2,cell//2],
                        native_pivot=[cell//4,cell//4],source_rect=source_rect,source_offset=list(offset),source_scale=scale,
                        alpha_bbox=list(im.getchannel('A').getbbox()),master_sha256=sha(out/fm),native_sha256=sha(out/fn),direction='south')
            masters.append(im);natives.append(native);records.append(record)
        for resolution,frames in [('master',masters),('native',natives)]:
            gutter=8 if resolution=='master' else 4;im,rects=sheet(frames,2,gutter,gutter)
            path=f'sheets/{group}-{resolution}.png';save(im,out/path)
            catalog['sheets'].append(dict(group=group,resolution=resolution,path=path,size=list(im.size),cell_size=list(frames[0].size),columns=2,rows=2,gutter=gutter,padding=gutter,sha256=sha(out/path)))
            for record,rect in zip(records,rects): record[resolution+'_sheet']=path;record[resolution+'_sheet_rect']=rect
        catalog['assets'].extend(records)
    counts=[]
    for asset in catalog['assets']:
        if asset['group'] in ('enemies','minibosses','bosses'):
            counts.append(export_modules(asset,out,asset['group']!='enemies'))
            if asset['id']=='iron_siege_craft': asset['description']='Heavy armored siege aircraft with independent wings, engines and main cannons.'
    catalog.update(version=2,modular_units=24,module_count=sum(counts),
                   modular_contract='All enemy/miniboss/boss assemblies use independently exported disjoint pixel layers; source pixels reconstruct exactly.',
                   builder='_BUILD_SOURCE/build_raiden_pack_1024.py + _BUILD_SOURCE/raiden_modular_1024.py',
                   generator='Built-in image_gen; five retained reference-guided sheets.',
                   scale_policy='Regular enemy source scale 1, miniboss source scale 2/3, boss source scale 1; each family keeps one proportional scale. Native exports are uniformly half their master.',
                   source_mask_policy='Measured mechanical polygons with nearest-contour attachment cleanup separate existing authored pixels; no duplicate hull backing, replacement geometry or invented hidden surfaces.')
    prompts=json.loads((src/'prompts.json').read_text(encoding='utf-8'))
    prompts['modular_expansion']=json.loads((src/'modular-prompts.json').read_text(encoding='utf-8'))
    (out/'generation-prompts.json').write_text(json.dumps(prompts,indent=2)+'\n',encoding='utf-8')
    print(f'MODULAR EXPORT: 24 units / {sum(counts)} independent modules; exact master and native unions.',flush=True)
