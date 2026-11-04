from pathlib import Path
import json,hashlib
W=Path(__file__).parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
A={q['asset']['id']:q for q in json.loads((W/'source-inventory.json').read_text())}
for d in ['exports','sources']: (W/d).mkdir(exist_ok=True)
jobs=[];banks={};icons={};prefix='assets/game/shared/combat/coleforge_1104/'
def add(id,files,cw,ch=None,pivot=None,durations=None,**kw):
 ch=ch or cw;cols=min(8,len(files));j=dict(id=id,files=files,cw=cw,ch=ch,cols=cols,out=str(W/'exports'/f'{id}.png'),source=str(W/'sources'/f'{id}.aseprite'),durations=durations or[67]*len(files),**kw);jobs.append(j)
 banks[id]=dict(key='cf114_'+id,path=prefix+id+'.png',cw=cw,ch=ch,cols=cols,frames=len(files),pivot=pivot or[cw//2,ch//2],durations=j['durations']);return j
for name,source,sizes in [('ring','Explosion_Shockwave_Ring',[64,96,128,192,256,384,512]),('smoke','Smoke_Radial_Impact',[24,40,64,96]),('column','Smoke_Boss_Column',[96,160,256]),('fire','Fire_Ignition',[32,48,64,96]),('small','Explosion_Small',[24,40,64]),('dust','smoke_05_sand_cloud',[32,64,96]),('atomic','nuclear_atomic_05_rolling_mushroom',[128,256,512]),('cole_nuke','nuclear_atomic_01_compact_tactical',[128,256,384])]:
 q=A[source];m=q['meta']if isinstance(q['meta'],dict)else q['meta'][0];dur=m.get('timings_ms',m.get('timing_ms',[50]*len(q['frameFiles'])));p=m['pivot'];p=[p['x'],p['y']]if isinstance(p,dict)else p;sw=q['asset'].get('cell',None)or m['cell'];sw=sw.get('width',0)if isinstance(sw,dict)else sw[0]if isinstance(sw,list)else sw
 for size in sizes:
  # Source flame/column/nuclear pivots are ground anchors; clouds/rings use centre.
  ground=name in ['column','fire','atomic','cole_nuke'];pivot=[round(p[0]*size/sw),round(p[1]*size/sw)]if ground else[size//2,size//2]
  files=q['frameFiles']+([q['frameFiles'][-1]]*6 if name=='column' else[])
  times=dur+([80]*6 if name=='column' else[])
  add(f'{name}_{size}',files,size,pivot=pivot,durations=times,palette='cole'if name=='cole_nuke'else'none',fadeStart=16 if name=='column' else 0)
for family,source in [('shield_blue','blue_hex_shield_growth'),('shield_green','green_energy_shield_charge')]:
 q=A[source];m=q['meta'];sw,sh=m['cell']
 for size in [64,96,128,192,256,384]:
  h=round(sh*size/sw/2)*2
  add(f'{family}_{size}',q['frameFiles'],size,h,pivot=[size//2,h//2],durations=m['timings_ms'],dither=True)
  add(f'{family}_hold_{size}',[q['frameFiles'][-1]]*6,size,h,pivot=[size//2,h//2],durations=[80]*6,dither=True,pulses=[-.10,0,.10,.15,.10,0])
  add(f'{family}_hit_{size}',[q['frameFiles'][-1]],size,h,pivot=[size//2,h//2],dither=True,palette='white')
for family,source in [('spread','spreadfire_cannon_muzzle'),('plasma','plasma_cannon_muzzle')]:
 q=A[source];m=q['meta'];add(f'{family}_muzzle',q['frameFiles'],32,pivot=[16,16],durations=m['timings_ms'],palette='blue'if family=='plasma'else'none')
for family,source in [('spread','spreadfire_cannon_impact'),('plasma','plasma_cannon_impact_small')]:
 q=A[source];m=q['meta'];add(f'{family}_impact',q['frameFiles'],48,pivot=[24,24],durations=m['timings_ms'],palette='blue'if family=='plasma'else'none')
fan=A['spreadfire_cannon_horizontal_fan']['frameFiles'][0];orb=A['vol2_ion_bloom_orb_loop_north']['frameFiles'][1]
for lv in range(1,6):
 a=[.14,.18,.22,.26,.30][lv-1];angles=[-a,0,a]
 add(f'spread_{lv}',[fan]*18,64,projectile=True,crop=[54,18,20,60],bodyHeight=[22,26,30,34,38][lv-1],angles=angles,glow=True,pulses=[-.10,0,.10,.15,.10,0],dirs=3)
 banks[f'spread_{lv}']['dirs']=3;banks[f'spread_{lv}']['angles']=angles
 add(f'plasma_{lv}',[orb]*6,48,projectile=True,crop=[18,18,28,28],bodyHeight=[18,22,26,30,34][lv-1],angles=[0],glow=True,pulses=[-.10,0,.10,.15,.10,0],dirs=1)
 banks[f'plasma_{lv}']['dirs']=1
for family in ['spread','plasma']:
 for lv in range(1,6):
  for size in [16,20,24,28,32,36,40,48,56,64,80,96,112]:
   id=f'{family}_icon_{lv}_{size}';j=add(id,['icon'],size,icon=family,level=lv,fan=fan,orb=orb)
   icons.setdefault(f'space_{family}_icon_{lv}',{})[str(size)]=id
  add(f'{family}_icon_{lv}_hit',['icon'],40,icon=family,level=lv,fan=fan,orb=orb,palette='white')
cfg={'iconSources':{family:str(W/'generated_icons'/f'{family}_master.png')for family in ['spread','plasma']},'jobs':jobs,'atlas':str(R/'assets/game/shared/atlases/bof_gravity_mode_space_weapons.png'),'atlasMeta':str(R/'assets/game/shared/atlases/bof_gravity_mode_space_weapons.json')}
(W/'build-config.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
meta={'banks':banks,'icons':icons,'provenance':[{ 'id':q['asset']['id'],'frames':[{'path':f,'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest()}for f in q['frameFiles']]}for q in A.values()],'generatedIcons':[{'family':family,'source':str(W/'generated_icons'/f'{family}-generated.png'),'sha256':hashlib.sha256((W/'generated_icons'/f'{family}-generated.png').read_bytes()).hexdigest(),'method':'Built-in image_gen; original hex frame and Roman tier plaque retained in Aseprite'}for family in ['spread','plasma']],'contract':'Static projectile poses; six brightness palette steps only. All rotations/sizes/alpha are baked offline in Aseprite. Runtime source-over blits only.'}
(W/'asset-metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
print('Prepared',len(jobs),'fixed-cell banks')
