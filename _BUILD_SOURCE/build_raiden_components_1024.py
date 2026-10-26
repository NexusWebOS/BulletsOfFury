"""Complete generated chassis + whole mounted hardware; replaces breakup cuts."""
from pathlib import Path
import csv, hashlib, json, math, zipfile, sys
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects, distance_transform_edt, binary_fill_holes

R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/raiden_components_1024';O=R/'art-packs/raiden-components-1024'
KITS={
 'light_air': [('steel_interceptor','Steel Interceptor','enemy'),('red_needle_fighter','Red Needle Fighter','enemy'),('teal_strike_drone','Teal Strike Drone','enemy')],
 'heavy_air': [('olive_attack_jet','Olive Attack Jet','enemy'),('ember_gunship','Ember Gunship','enemy'),('delta_bomber','Delta Bomber','enemy')],
 'elite_air': [('quad_nacelle_cruiser','Quad-Nacelle Cruiser','enemy'),('violet_stealth_wing','Violet Stealth Wing','enemy'),('iron_siege_craft','Iron Siege Craft','enemy')],
 'field_armor': [('scout_tank','Scout Tank','enemy'),('twin_cannon_tank','Twin-Cannon Tank','enemy'),('rocket_carrier','Rocket Carrier','enemy')],
 'fixtures': [('wheeled_flak','Wheeled Flak','enemy'),('cannon_bunker','Cannon Bunker','enemy'),('missile_battery','Missile Battery','enemy')],
 'naval': [('river_patrol','River Patrol','enemy'),('missile_corvette','Missile Corvette','miniboss'),('dreadnought_battleship','Dreadnought Battleship','boss')],
 'siege_ground': [('olive_assault_tank','Olive Assault Tank','miniboss'),('iron_bastion_landship','Iron Bastion Landship','boss'),('quad_laser_citadel','Quad Laser Citadel','boss')],
 'capital_air': [('quad_battery_fortress','Quad Battery Fortress','miniboss'),('orange_heavy_bomber','Orange Heavy Bomber','miniboss'),('stormwing_sky_carrier','Stormwing Sky Carrier','boss')]
}
AIR={'light_air','heavy_air','elite_air','capital_air'}
GROUND=['scout_tank','twin_cannon_tank','rocket_carrier','olive_assault_tank','iron_bastion_landship','quad_laser_citadel','wheeled_flak']
GEAR=[('light_track','Light track cassette'),('heavy_track','Heavy track cassette'),('rubber_tire','Rubber wheel'),('armored_tire','Armored wheel'),('road_wheel','Road wheel'),('sprocket','Drive sprocket'),('idler','Idler wheel'),('bogie','Twin wheel bogie'),('suspension','Suspension arm'),('steel_roller','Steel roller'),('wide_roller','Wide road wheel')]
NAMES={
 'wing_left':'Left wing','wing_right':'Right wing','engine_left':'Left engine','engine_right':'Right engine','cannon_pod':'Autocannon pod','missile_pod':'Missile pod',
 'single_turret':'Single cannon turret','twin_turret':'Twin cannon turret','missile_rack':'Missile rack','rotary_turret':'Rotary cannon turret','radar':'Radar module','power':'Power module',
 'drive':'Stern drive','triple_turret':'Triple cannon turret','bridge':'Bridge module','laser_turret':'Laser cannon turret'
}

def save(im,path):path.parent.mkdir(parents=True,exist_ok=True);im.save(path,optimize=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def extract(im):
 a=np.array(im);lab,_=label(a[:,:,3]>24);objs=[]
 for i,s in enumerate(find_objects(lab),1):
  if s is not None:
   count=np.count_nonzero(lab[s]==i)
   if count>2000:objs.append((count,i,s))
 objs=sorted(objs,reverse=True)[:9];assert len(objs)==9
 objs.sort(key=lambda x:(x[2][0].start+x[2][0].stop)/2)
 objs=sum([sorted(objs[i:i+3],key=lambda x:x[2][1].start)for i in [0,3,6]],[])
 seeds=np.zeros(lab.shape,dtype=np.int16)
 for number,(_,i,s)in enumerate(objs,1):seeds[lab==i]=number
 _,near=distance_transform_edt(seeds==0,return_indices=True);owners=seeds[tuple(near)]
 crops=[]
 for number,(_,i,s)in enumerate(objs,1):
  x0,y0=max(0,s[1].start-6),max(0,s[0].start-6);x1,y1=min(im.width,s[1].stop+6),min(im.height,s[0].stop+6)
  p=a[y0:y1,x0:x1].copy();p[owners[y0:y1,x0:x1]!=number]=0
  crops.append((Image.fromarray(p),[x0,y0,x1-x0,y1-y0]))
 return crops

def roles(kit):
 if kit in AIR:return ['wing_left','wing_right','engine_left','engine_right','cannon_pod','missile_pod']
 if kit=='naval':return ['drive','twin_turret','triple_turret','missile_rack','bridge','radar']
 if kit=='siege_ground':return ['twin_turret','laser_turret','missile_rack','rotary_turret','radar','power']
 return ['single_turret','twin_turret','missile_rack','rotary_turret','radar','power']

def pivot(role,b):
 x0,y0,x1,y1=b;w,h=x1-x0,y1-y0
 u,v=(.5,.5)
 if role=='wing_left':u,v=.92,.71
 elif role=='wing_right':u,v=.08,.71
 elif role.endswith('turret'):v=.38
 elif role=='cannon_pod':v=.19
 elif role in ['engine_left','engine_right','drive']:v=.5
 elif role in ['missile_pod','missile_rack']:v=.46
 elif role=='radar':v=.73
 return [round(x0+u*w),round(y0+v*h)]

def plan(key,kit):
 slots=[]
 def add(name,role,u,v,scale,kind='weapon',angle=0):slots.append(dict(id=name,role=role,uv=[u,v],scale=scale,kind=kind,angle=angle))
 if kit in AIR and key!='quad_battery_fortress':
  add('port_wing','wing_left',.13,.50,.60,'wing');add('starboard_wing','wing_right',.87,.50,.60,'wing')
  add('port_engine','engine_left',.25,.40,.38,'engine',180);add('starboard_engine','engine_right',.75,.40,.38,'engine',180)
  add('port_weapon','cannon_pod',.32,.63,.33);add('starboard_weapon','missile_pod',.68,.63,.33)
  if key=='quad_nacelle_cruiser':
   add('port_aft_engine','engine_left',.25,.18,.32,'engine',180);add('starboard_aft_engine','engine_right',.75,.18,.32,'engine',180)
  if key=='stormwing_sky_carrier':
   add('port_inner_weapon','cannon_pod',.36,.64,.29);add('starboard_inner_weapon','cannon_pod',.64,.64,.29)
   add('port_missiles','missile_pod',.30,.28,.28);add('starboard_missiles','missile_pod',.70,.28,.28)
 elif key=='quad_battery_fortress':
  for side,u in [('port',.23),('starboard',.77)]:
   for end,v in [('aft',.22),('forward',.76)]:add(side+'_'+end,'cannon_pod',u,v,.43)
  add('missile_pack','missile_pod',.5,.5,.33)
 elif kit=='naval':
  add('port_drive','drive',.35,.09,.24,'engine',180);add('starboard_drive','drive',.65,.09,.24,'engine',180)
  add('bridge','bridge',.5,.42,.34,'utility')
  add('bow_battery','twin_turret' if key=='river_patrol' else 'triple_turret',.5,.73,.36)
  if key!='river_patrol':
   add('port_missiles','missile_rack',.24,.55,.30);add('starboard_missiles','missile_rack',.76,.55,.30)
  if key=='dreadnought_battleship':
   add('aft_battery','triple_turret',.5,.20,.36)
   for side,u in [('port',.18),('starboard',.82)]:
    for end,v in [('upper',.38),('lower',.64)]:add(side+'_'+end,'twin_turret',u,v,.23)
 elif key in ['rocket_carrier','missile_battery']:
  add('port_rack','missile_rack',.28,.50,.38);add('starboard_rack','missile_rack',.72,.50,.38)
  add('sensor','radar',.5,.16,.25,'utility')
 elif key=='scout_tank':add('main_turret','single_turret',.5,.43,.57)
 elif key in ['twin_cannon_tank','wheeled_flak','olive_assault_tank']:
  for side,u in [('port',.28),('starboard',.72)]:add(side+'_turret','rotary_turret' if key=='wheeled_flak' else 'twin_turret',u,.43,.36)
 elif key=='cannon_bunker':add('main_turret','single_turret',.5,.48,.68)
 elif key in ['iron_bastion_landship','quad_laser_citadel']:
  for side,u in [('port',.26),('starboard',.74)]:
   for end,v in [('aft',.28),('forward',.70)]:add(side+'_'+end,'laser_turret' if key=='quad_laser_citadel' else 'twin_turret',u,v,.35)
  for side,u in [('port',.17),('starboard',.83)]:add(side+'_missiles','missile_rack',u,.13,.29)
  add('command_power','power',.5,.5,.33,'utility')
 else:raise ValueError(key)
 return slots

def layer(im,frame,mount,center,scale,angle=0):
 angle=math.radians(angle);c,s=math.cos(angle),math.sin(angle);mx,my=mount;px,py=center
 return im.transform((frame,frame),Image.Transform.AFFINE,(c/scale,s/scale,px-(c*mx+s*my)/scale,-s/scale,c/scale,py+(s*mx-c*my)/scale),resample=Image.Resampling.NEAREST)

def running_gear(catalog):
 parts=[]
 for filename,selection in [('track_modules.png',range(2)),('wheel_modules.png',range(9))]:
  path=S/'source'/filename;crops=extract(Image.open(path).convert('RGBA'))
  common=min(1,464/max(max(c.size)for c,_ in crops))
  for index in selection:
   key,name=GEAR[len(parts)];crop,rect=crops[index];size=[round(v*common)for v in crop.size]
   frame=Image.new('RGBA',(512,512));offset=[(512-v)//2 for v in size];frame.paste(crop.resize(size,Image.Resampling.NEAREST),offset)
   a=np.array(frame);yy,xx=np.where(a[:,:,3]>128);bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
   pid='running_gear/'+key;normal=f'components/{pid}.png';native=f'components/{pid}-native.png';hit=f'components/{pid}-hit.png'
   save(frame,O/normal);save(frame.resize((256,256),Image.Resampling.NEAREST),O/native)
   white=a.copy();white[:,:,:3]=255;white[a[:,:,3]==0]=0;save(Image.fromarray(white),O/hit)
   part=dict(id=pid,kit='running_gear',role=key,name=name,image=normal,native=native,hit=hit,size=[512,512],bbox=bbox,pivot=[256,256],source=str(path.relative_to(R)).replace('\\','/'),source_rect=rect,source_scale=common,source_offset=offset,largest_central_deck_hole=0,sha256=sha(O/normal))
   parts.append(part);catalog['components'].append(part)
 catalog['kits'].append(dict(id='running_gear',sources=['source/track_modules.png','source/wheel_modules.png'],parts=[p['id']for p in parts]))
 return {p['role']:p for p in parts}

def gear_mounts(key,base,gear,frame,us):
 if key not in GROUND:return []
 x0,y0,x1,y1=base['bbox'];bw,bh=x1-x0,y1-y0;out=[]
 support=np.asarray(Image.open(O/base['image']))[:,:,3]>192
 _,nearest=distance_transform_edt(~(distance_transform_edt(support)>6),return_indices=True)
 def add(side,role,index,v,height,order):
  c=gear[role];gx0,gy0,gx1,gy1=c['bbox'];scale=bh*height/(gy1-gy0)
  # Gear center is outboard; its inboard axle overlaps the intact hull.
  direction=-1 if side=='port'else 1;edge=x0 if direction<0 else x1
  cx=edge+direction*(gx1-gx0)*scale*(-.30 if role=='suspension'else .24);cy=y0+v*bh
  sx=round(edge-direction*min(16,bw*.07));sy=round(cy)
  sy,sx=[int(q)for q in nearest[:,sy,sx]]
  compatible=['light_track','heavy_track']if role.endswith('track')else ['suspension']if role=='suspension'else ['rubber_tire','armored_tire']if key=='wheeled_flak'else ['road_wheel','steel_roller','wide_roller','sprocket','idler','bogie']
  out.append(dict(id=f'{side}_{role}_{index}',name=f'{side.title()} {NAMES.get(role,c["name"]).lower()} {index}',position=[frame/2+(cx-256)*us,frame/2+(cy-256)*us],base_attachment_pixel=[sx,sy],scale=scale*us,angle=0,kind='running_gear',layer='under',order=order,default=c['id'],compatible=[gear[r]['id']for r in compatible]))
 for side in ['port','starboard']:
  for i,v in enumerate([.20,.50,.80],1):add(side,'suspension',i,v,.13,0)
  if key=='wheeled_flak':
   for i,v in enumerate([.20,.50,.80],1):add(side,'rubber_tire',i,v,.23,10)
  else:
   for i,(v,role)in enumerate([(.12,'sprocket'),(.31,'road_wheel'),(.50,'road_wheel'),(.69,'road_wheel'),(.88,'idler')],1):add(side,role,i,v,.19,10)
   add(side,'heavy_track'if key in GROUND[3:6]else'light_track',1,.50,.99,20)
 return sorted(out,key=lambda m:m['order'])

def build():
 O.mkdir(parents=True,exist_ok=True);catalog=dict(version=4,title='Raiden Component Foundry',components=[],units=[],kits=[],contract='Complete surfaced chassis. All mobile ground running gear is independent: tracks, individual wheels, sprockets, idlers and suspension. No breakup masks or baked wheels.')
 gear=running_gear(catalog);hullpath=S/'source/ground_hulls.png';hulls=extract(Image.open(hullpath).convert('RGBA'))
 for kit,units in KITS.items():
  path=S/'source'/f'{kit}.png';im=Image.open(path).convert('RGBA');crops=extract(im)
  common=min(1,464/max(max(c.size)for c,_ in crops));keys=[u[0]for u in units]+roles(kit);parts=[]
  for i,key in enumerate(keys[:3]):
   if key in GROUND:crops[i]=hulls[GROUND.index(key)]
  for i,(key,(crop,rect))in enumerate(zip(keys,crops)):
   size=(round(crop.width*common),round(crop.height*common));crop=crop.resize(size,Image.Resampling.NEAREST)
   frame=Image.new('RGBA',(512,512));offset=((512-size[0])//2,(512-size[1])//2);frame.paste(crop,offset)
   a=np.array(frame);support=a[:,:,3]>128;yy,xx=np.where(support);bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
   holes=binary_fill_holes(support)&~support;labs,_=label(holes);hole_sizes=np.bincount(labs.ravel())[1:];largest=int(hole_sizes.max())if len(hole_sizes)else 0
   deck=holes.copy();x0,y0,x1,y1=bbox;deck[:,:round(x0+.2*(x1-x0))]=False;deck[:,round(x1-.2*(x1-x0)):]=False
   dl,_=label(deck);ds=np.bincount(dl.ravel())[1:];deck_hole=int(ds.max())if len(ds)else 0
   role='base' if i<3 else key;pid=kit+'/'+key;normal=f'components/{pid}.png';native=f'components/{pid}-native.png';hit=f'components/{pid}-hit.png'
   save(frame,O/normal);save(frame.resize((256,256),Image.Resampling.NEAREST),O/native)
   white=a.copy();white[:,:,:3]=255;white[a[:,:,3]==0]=0;save(Image.fromarray(white),O/hit)
   rec=dict(id=pid,kit=kit,role=role,name=units[i][1]+' chassis'if i<3 else NAMES[key],image=normal,native=native,hit=hit,size=[512,512],bbox=bbox,pivot=[256,256]if i<3 else pivot(role,bbox),source_rect=rect,source_scale=common,source_offset=list(offset),largest_internal_alpha_hole=largest,largest_central_deck_hole=deck_hole,sha256=sha(O/normal))
   if key in GROUND:rec.update(source=str(hullpath.relative_to(R)).replace('\\','/'),source_sha256=sha(hullpath),running_gear_baked=False)
   assert i>=3 or deck_hole<128,(kit,key,'Incomplete central chassis surface',deck_hole)
   parts.append(rec);catalog['components'].append(rec)
  catalog['kits'].append(dict(id=kit,source=str(path.relative_to(R)).replace('\\','/'),source_sha256=sha(path),parts=[p['id']for p in parts]))
  lookup={p['role']:p for p in parts[3:]}
  for i,(key,name,tier)in enumerate(units):
   base=parts[i];frame={'enemy':512,'miniboss':768,'boss':1024}[tier];us={'enemy':.70,'miniboss':1.05,'boss':1.35}[tier]
   bare=layer(Image.open(O/base['image']),frame,[frame/2,frame/2],[256,256],us)
   mounts=gear_mounts(key,base,gear,frame,us);assembled=Image.new('RGBA',(frame,frame));bx0,by0,bx1,by1=base['bbox']
   for m in mounts:
    c=gear[m['default'].split('/')[-1]];assembled=Image.alpha_composite(assembled,layer(Image.open(O/c['image']),frame,m['position'],c['pivot'],m['scale']))
   assembled=Image.alpha_composite(assembled,bare)
   gearfile=f'units/{key}-running-gear.png';save(assembled,O/gearfile)
   support=np.asarray(Image.open(O/base['image']))[:,:,3]>192
   solid=distance_transform_edt(support)>6
   _,nearest=distance_transform_edt(~solid,return_indices=True)
   for slot in plan(key,kit):
    comp=lookup[slot['role']];u,v=slot['uv'];tx,ty=round(bx0+u*(bx1-bx0)),round(by0+v*(by1-by0))
    sy,sx=[int(q)for q in nearest[:,ty,tx]];x=frame/2+(sx-256)*us;y=frame/2+(sy-256)*us
    allowed=[p['id']for p in parts[3:]if (slot['kind']=='weapon'and p['role']in ['single_turret','twin_turret','triple_turret','rotary_turret','laser_turret','missile_rack','cannon_pod','missile_pod'])or(slot['kind']=='utility'and p['role']in ['radar','power','bridge'])or(slot['kind']=='engine'and p['role']in ['drive','engine_left','engine_right'])or(slot['kind']=='wing'and p['role']==slot['role'])]
    mount=dict(id=slot['id'],name=slot['id'].replace('_',' ').title(),position=[x,y],base_attachment_pixel=[sx,sy],scale=slot['scale']*us,angle=slot['angle'],kind=slot['kind'],default=comp['id'],compatible=allowed)
    mounts.append(mount);assembled=Image.alpha_composite(assembled,layer(Image.open(O/comp['image']),frame,[x,y],comp['pivot'],mount['scale'],mount['angle']))
   native=f'units/{key}.png';master=f'units/{key}-master.png';basefile=f'units/{key}-bare.png'
   save(assembled,O/master);save(assembled.resize((frame//2,frame//2),Image.Resampling.NEAREST),O/native);save(bare,O/basefile)
   catalog['units'].append(dict(id=key,name=name,tier=tier,kit=kit,frame=frame,base=base['id'],body_scale=us,body_position=[frame/2,frame/2],mounts=mounts,image=native,master=master,bare=basefile,running_gear=gearfile if key in GROUND else None))
 catalog['units'].sort(key=lambda u:({'enemy':0,'miniboss':1,'boss':2}[u['tier']],u['name']))
 from match_raiden_components_1025 import apply
 apply(sys.modules[__name__],catalog)
 assert len(catalog['units'])==24 and len(catalog['components'])==201
 text=json.dumps(catalog,indent=2)+'\n';(O/'manifest.json').write_text(text,encoding='utf-8');(O/'catalog.js').write_text('window.FOUNDRY='+text.rstrip()+';\n',encoding='utf-8')
 (O/'generation-prompts.json').write_bytes((S/'prompts.json').read_bytes())
 (O/'running-gear-prompts.json').write_bytes((S/'running-gear-prompts.json').read_bytes())
 with (O/'roster.csv').open('w',newline='',encoding='utf-8')as f:
  w=csv.writer(f);w.writerow(['id','name','tier','complete_base','hardpoints']);[w.writerow([u['id'],u['name'],u['tier'],u['base'],len(u['mounts'])])for u in catalog['units']]
 print('BUILT: 24 complete chassis, 177 matching modules, seven independent running-gear assemblies.',flush=True)
 return catalog

def package():
 path=O.parent/'raiden-components-1024.zip'
 catalog=json.loads((O/'manifest.json').read_text());used=set()
 for c in catalog['components']:
  used.update(c[k]for k in ['image','native','hit'])
 for u in catalog['units']:
  used.update(u[k]for k in ['image','master','bare']);used.add(u['running_gear'])
 motion=O/'animation-data.json'
 if motion.exists():
  for bank in json.loads(motion.read_text())['fx'].values():
   used.update(f['image']for f in(bank if isinstance(bank,list)else[bank]))
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
  for p in sorted(O.rglob('*')):
   relative=p.relative_to(O).as_posix()
   if p.is_file()and('/'not in relative or relative in used):z.write(p,str(p.relative_to(O.parent)))
 print('ZIP:',path.stat().st_size,flush=True)

if __name__=='__main__':build();package()
