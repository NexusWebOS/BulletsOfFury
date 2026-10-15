# Executed by build_enemy_atlas_1013.py with its audited runtime dictionaries.
def put_attacks(e,items,source,replace=False,**meta):
 if replace:e['attacks']=[]
 seen={a['id'] for a in e['attacks']}
 for item in items:
  if item not in seen:e['attacks'].append({'id':item,'name':human(item),'source':source,**meta});seen.add(item)
def set_art(e,keys,records=None):
 e['artKeys']=uniq(keys+e['artKeys']);e['art']=[asset(k) for k in e['artKeys']]
 if records:
  for i,k in enumerate(e['artKeys']):
   if k in records:e['art'][i].update(records[k])
def txt(file):return TEXT.get(file) or (ROOT/file).read_text(encoding='utf-8',errors='replace')
def function_body(file,name):
 text=txt(file); matches=list(re.finditer(r'\b(?:function\s+'+re.escape(name)+r'\s*\(|'+re.escape(name)+r'\s*=\s*function\s*\()',text))
 if not matches:return ''
 m=matches[-1];i=text.index('{',m.end());level=0;quote=None;j=i
 while j<len(text):
  c=text[j];pair=text[j:j+2]
  if quote:
   if c=='\\':j+=2;continue
   if c==quote:quote=None
  elif pair=='//':j=text.find('\n',j);continue
  elif pair=='/*':j=text.find('*/',j+2)+2;continue
  elif c in "'\"`":quote=c
  elif c=='{':level+=1
  elif c=='}':
   level-=1
   if level==0:return text[i:j+1]
  j+=1
 return ''
def mode_strings(body):
 return uniq(re.findall(r"(?:case\s+|\b(?:mode|attack|state|kind)\s*===?\s*)['\"]([^'\"]+)['\"]",body))

# Keep constructor expansion prefixes in coverage instead of displaying a phantom actor.
excluded=[e for e in entries if e['status']=='incomplete-dynamic-prefix']
entries[:]=[e for e in entries if e not in excluded]

# Runtime table aliases: xelite_ is a prefix generated from ten registry members.
for typ,row in R['ELITEX'].items():
 key='xelite_'+typ
 if any(e['id']=='bof-enemy-'+key for e in entries):continue
 e=entry('bof-enemy-'+key,row.get('name',human(typ)),'enemy','bof',[],{'method':'enemy','type':key,'stage':6},status='legacy-spawnable')
 e['runtime']={'controller':'elitexTick','draw':'drawEnemy','definition':row};e['sources']=[symbol_ref('ELITEX'),symbol_ref('spawnDifficultyElite')]
 e['audit']={'statusEvidence':'difficultyElitePlan currently returns without scheduling; runtime constructor remains supported'}
 set_art(e,['xelite_'+typ+'_idle']);put_attacks(e,[row.get('pat','elite volley')],symbol_ref('ELITEX'))

# Weapon-specific modular emplacement variants all use the actual native actor.
modroster={1:['mg','missile'],2:['missile','laser'],3:['laser','sonic'],4:['mg','missile','laser'],6:['mg','laser','sonic'],7:['mg','laser','sonic'],8:['missile','laser','sonic']}
for stage,weapons in modroster.items():
 for weapon in weapons:
  e=entry('bof-ground-modturret-'+str(stage)+'-'+weapon,human(weapon)+' Emplacement','ground','bof',[stage],{'method':'enemy','type':'modturret','stage':stage,'options':{'_modStage':stage,'_modWeapon':weapon,'_modIndex':0}})
  e['runtime']={'controller':'modularGroundTurretTick','draw':'drawModularGroundTurret'};e['difficulties']=['normal','hard','furious'];e['sources']=[symbol_ref('modularGroundTurretPlan'),symbol_ref('modularGroundTurretTick')]
  put_attacks(e,[weapon],symbol_ref('modularGroundTurretTick'));set_art(e,['overhaul_ground_head_'+weapon,'overhaul_ground_base_'+str(stage)])
  e['projectileKinds']={'mg':['mg'],'missile':['emissile'],'laser':[],'sonic':[]}[weapon]
  if weapon in ['laser','sonic']:e['nativeHazards']=[weapon+' geometry']

# Registry attack fields belong to the individual type (not an entire family's superset).
for e in entries:
 if e['game']!='bof' or e['spawn'].get('method')!='enemy':continue
 typ=e['spawn']['type'];rows=origins.get(typ,[])
 for origin in rows:
  row=origin['row']
  if not isinstance(row,dict):continue
  for k in ['atk','attack','mode']:
   if isinstance(row.get(k),str):put_attacks(e,[row[k]],symbol_ref(origin['table']),registryField=k)
 if e['runtime'].get('pattern')=='naval':e['category']='naval'
 if e['runtime'].get('fields',{}).get('prop') or e['runtime'].get('pattern')=='prop':e['category']='hazard'
 if typ in R['DRONE_BEHAV']:
  e['runtime']['definition']=R['DRONE_BEHAV'][typ]
  row=R['DRONE_BEHAV'][typ]
  put_attacks(e,[v for k,v in row.items() if k in ['atk','attack','mode','pat'] and isinstance(v,str)],symbol_ref('DRONE_BEHAV'))
 if typ in ['ac10firejet','ac10icejet']:
  put_attacks(e,['paired-burst'],ref('assets/arcade_combat_1010.js','ac10JetTick'),replace=True);e['projectileKinds']=['s2needle' if typ=='ac10firejet' else 's3shard']
 if typ in ['ash','skim','disc','eye','lance','s3mine','s3interceptor']:
  put_attacks(e,['committed-ram'],ref('assets/arcade_combat_1010.js','ac10RamTick'),replace=True);e['projectileKinds']=[]
 if typ=='mm1003_riflelocust':e['projectileKinds']=['mg'];e['attacks']=[a for a in e['attacks'] if a['id']!='ep13-charge']
 if typ=='s9beacon':e['projectileKinds']=['warpshard']
 if typ=='s6buoy':e['audit']['statusEvidence']='playthrough_1011.js explicitly returns null for s6buoy on stage 6; retained for inventory only'

# Every current boss gets its current attack controller and exact attack identifiers.
bosscontrollers={'razorback':('assets/game.js','razorbackCombat'),'damkeeper':('assets/game.js','updateOverlordX'),'magmaward':('assets/encounters_0926.js','er26Tick'),'infernoreaver':('assets/game.js','furnaceCombat'),'frostcruiser':('assets/encounters_0926.js','er26Tick'),'cryospear':('assets/encounters_0926.js','er26Tick'),'olivewarden':('assets/part2_combat_1010.js','p2IronTick'),'stormsovereign':('assets/part2_combat_1010.js','p2StormTick'),'spacebomber':('assets/combat_polish_0927b.js','siegeBomberTick'),'siegebomber':('assets/combat_polish_0927b.js','siegeBomberTick'),'chromehammer':('assets/game.js','hammerBossTick'),'warhive':('assets/stage6_carrier_1013.js','warhiveTick'),'dualscoopdredger':('assets/stage7_modular_0927.js','s7mTick'),'sludgeemperor':('assets/stage7_modular_0927.js','s7mTick'),'heralddeath':('assets/herald_1003f.js','hd1003Tick'),'vileexistence':('assets/finale_structure_1003j.js','j3Tick'),'voidhorizon':('assets/late_encounters_0927.js','late27Tick'),'tidalfusion':('assets/game.js','s9FusionBossTick')}
bossattacks={
 'damkeeper':(['twin-mg','rocket-volley','green-volley','rotor-tempest','gun-sweep','missile-lock','rush','sonic-combo'],'ovStartSweep'),
 'spacebomber':(['bombs','crossfire','missiles','charge','beam','lob','carpet','overdrive'],'siegeBomberTick'),
 'siegebomber':(['bombs','crossfire','missiles','charge','beam','lob','carpet','overdrive'],'siegeBomberTick'),
 'chromehammer':(['hammer-leap','hammer-throw','spike-ball','chromium-shield','hammer-recharge','chain-gun','spell','mega-beam','storm','orbital-hammer'],'hammerArsenalNext'),
 'warhive':(['BATTERY CASCADE','CROSS-DECK GATES','ALTERNATING COMB','rocket-volley'],'sc13Sequence'),
 'dualscoopdredger':(['tank-cross','caustic-lob','tank-mortar','tank-charge','tank-orbits','pressure-salvo'],'s7mNext'),
 'sludgeemperor':(['chase','chain','mortar','spore-lob','orbs','bounce','jump','crawl','aim','portal-volley','laser'],'s7mNext'),
 'heralddeath':(['skulls','lances','salvo'],'hd1003Start'),
 'voidhorizon':(['needle-relay','rift-gates','horizon-orbit','prism-sweep'],'late27Book'),
 'tidalfusion':(['warden-crossfire','warden-missiles','fusion-ring'],'s9FusionBossTick')}
native_by_kind={q['request'].get('kind'):q for q in E.get('encounters',[]) if q['request'].get('kind')}
for e in entries:
 if e['game']!='bof' or e['category'] not in ['boss','miniboss','password-boss','form']:continue
 kind=e['spawn'].get('kind');native=native_by_kind.get(kind,{});books=native.get('books',{}).get('er26')
 if kind in bosscontrollers:
  f,controller=bosscontrollers[kind];e['runtime']['controller']=controller;e['sources'].append(ref(f,controller))
 if books:
  e['attacks']=[]
  for level,book in books.items():
   for attack in uniq(book):
    prior=next((a for a in e['attacks'] if a['id']==attack),None)
    if prior:prior['ranks'].append(int(level))
    else:e['attacks'].append({'id':attack,'name':human(attack),'ranks':[int(level)],'source':ref('assets/encounters_0926.js','er26Book'),'evidence':'current native er26Book, after all loaded overrides'})
 if kind=='razorback':
  e['attacks']=[]
  for bookname in ['RZB_ATTACKS','RZB_FURY_ATTACKS']:
   for phase,attacks in R[bookname].items():
    for attack in uniq(attacks):e['attacks'].append({'id':attack,'name':human(attack),'phase':phase,'difficulties':['furious'] if 'FURY' in bookname else ['easy','normal','hard'],'source':symbol_ref(bookname)})
  e['projectileKinds']=['rzbMissile'];set_art(e,['rzb_hull_base','rzb_turret'])
 if kind=='infernoreaver':
  e['attacks']=[]
  for phase,attacks in R['FZT_ATTACKS'].items():put_attacks(e,uniq(attacks),symbol_ref('FZT_ATTACKS'),phase=phase)
 if kind in bossattacks:
  attacks,sym=bossattacks[kind];put_attacks(e,attacks,ref(bosscontrollers[kind][0],sym),replace=True)
 if kind in ['siegesonic','siegedeviator','siegedevastator']:
  unit=R['SG10']['kinds'][kind];put_attacks(e,{'sonic':['pulse','charge','sweep'],'deviator':['missiles','fan','lock'],'devastator':['cannons','fan']}[unit],ref('assets/siege_tanks_1010.js','sg10StartAttack'),replace=True)
  e['runtime']['controller']='sg10Tick';e['runtime']['draw']='sg10Draw';set_art(e,[R['SG10_ART'][unit+'_hull'][0]['key']]);e['animationBanks']=[{'id':unit,'banks':{k:v for k,v in R['SG10_ART'].items() if k.startswith(unit+'_')}}]
 if kind=='warhive':
  e['name']='Warhive Siege Carrier';set_art(e,['s6cargo13_hull']);e['nativeHazards']=['turret beam rays'];e['projectileKinds']=['emissile'];e['difficultyProfiles']=R['SC13_CFG']
 if kind in ['spacebomber','siegebomber']:set_art(e,['mr27_space' if kind=='spacebomber' else 'polish_bomber'])
 if kind in ['stormsovereign','cryospear','olivewarden']:set_art(e,['mr27_'+{'stormsovereign':'storm','cryospear':'rime','olivewarden':'iron'}[kind]])
 if kind=='chromehammer':set_art(e,['arch_stand_0','hammer_ship']);e['animationBanks'].append({'id':'hammer-effects','banks':R['HM10_ART']})
 if kind=='sludgeemperor':set_art(e,['s7m_body','s7m_warden'])
 if kind=='dualscoopdredger':e['name']='Caustic Siege Tank';set_art(e,['s7m_tank'])
 if kind=='heralddeath':set_art(e,[R['HD1003_ART']['key']]);e['animationBanks'].append({'id':'herald-modules','atlas':R['HD1003_ART']})
 if kind=='voidhorizon':set_art(e,['ns9x_horizon_0'])
 if kind=='tidalfusion':set_art(e,['ns9_wardenL_0','ns9_wardenR_0'])
 if kind=='vileexistence':
  phase=e['spawn'].get('phase',0);form=e['spawn'].get('mimic')
  if form is None:
   e['name']=['The Mutated Drone','The Ghost in the Code','The Vile Colossus'][phase]
   sig=R['HF7_BOOK'][['host','ghost','home'][phase]];put_attacks(e,[sig['name']],symbol_ref('HF7_BOOK'))
   e['runtime']['controller']='j3Tick';e['runtime']['draw']='r30DrawBoss'
  else:
   fd=R['F1003B_FORMS'][form];e['name']=fd['name'];e['runtime']['controller']='f1003bTick / gd4Tick / hf7Tick';e['runtime']['draw']='r30DrawBoss'
   if fd['id'] in R['FMC_ART']:
    fa=R['FMC_ART'][fd['id']];set_art(e,[fa['key']]);e['animationBanks'].append({'id':fd['id'],'atlas':fa})
   if form==5:put_attacks(e,['leapSlash','shieldSmite','blade-tempest','code-shockwave'],ref('assets/finale_forms_1008.js','ff8TempestStart'));set_art(e,['hk5_knight_0'])
   if form==8:put_attacks(e,['chromium-void-rift','chromium-shield','hammer-storm'],ref('assets/hammer_knight_1005.js','hk5HammerTick'));set_art(e,['hk5_hammer_0'])
 if not e['artKeys'] and kind:
  keys=E.get('bossAssets',{}).get(kind,{}).get('keys',[])
  if keys:set_art(e,keys)

# Distinct rebel signatures currently override the older generic attack roles.
rebel_roles={'voss':['turbo','fusion'],'nyx':['cloak'],'rook':['slug','ram','rookhook'],'kaia':['rockets'],'jace':['helix','ram']}
for e in entries:
 if e['game']=='bof' and e['category']=='rebel':
  key=e['spawn']['type'];e['attacks']=[]
  for attack in ['machine-gun']+rebel_roles[key]:
   e['attacks'].append({'id':attack,'name':R['RA4_NAMES'].get(attack,{'rookhook':'Rookhook','machine-gun':'Aimed machine gun'}.get(attack,human(attack))),'source':ref('assets/rebel_arsenal_1004c.js','ra4AttackKind') if attack!='rookhook' else ref('assets/hardcorps_finale_1007.js','hc7Rook')})
  e['projectileKinds']=['s6tracer']+(['emissile'] if key=='kaia' else [])
  e['nativeHazards']=['fusion beam'] if key=='voss' else ['grapple chain'] if key=='rook' else []
for e in entries:
 if e['game']=='bof' and e['spawn'].get('password') in ['REBEL6','XREBEL']:
  e['attacks']=[{'id':'squad','name':'Five personal arsenals','members':['bof-rebel-'+k for k in R['REBEL_KEYS']],'source':ref('assets/rebel_arsenal_1004c.js','ra4AttackKind')}];set_art(e,['rr_ship_'+R['REBEL_SHIPS'][0]])
 if e['game']=='bof' and e['spawn'].get('password') in ['HARR6','XHARR']:
  put_attacks(e,uniq(sum(R.get('HARRIER_STAND_ATTACKS',{}).values(),[])) if isinstance(R.get('HARRIER_STAND_ATTACKS'),dict) else ['harrier-cannons','harrier-beam','missiles'],symbol_ref('HARRIER_STAND_ATTACKS'))
  e['sources'].append(symbol_ref('warhiveInit'))

# Old boss constructors are retained as clearly labelled legacy inventory.
represented={e['spawn'].get('kind') for e in entries if e['game']=='bof'}
for kind,role in E.get('bossDefinitions',{}).items():
 if kind in represented:continue
 native=E.get('bossAssets',{}).get(kind,{});row=R['SHIPBOSS'].get(kind,R['MEGABOSS'].get(kind,{}))
 e=entry('bof-legacy-'+role+'-'+kind,native.get('name',human(kind)),'boss' if role=='boss' else 'miniboss','bof',[],{'method':'encounter','kind':kind,'role':role,'stage':1},status='legacy-unverified')
 e['runtime']={'controller':'updateBoss' if role=='boss' else 'updateSubBoss','draw':'drawBoss' if role=='boss' else 'drawSubBoss','nativeLaunch':'spawnBoss(kind)' if role=='boss' else 'spawnSubBoss__inner(kind)'}
 e['sources']=[symbol_ref('spawnBoss' if role=='boss' else 'spawnSubBoss__inner')];e['audit']={'statusEvidence':'Constructor exists; not a current stage/password slot. Native drawability is not asserted until preview verifies required archived art.'}
 put_attacks(e,uniq(row.get('pats',[])+([row['pat']] if row.get('pat') else [])+([row['atk']] if row.get('atk') else [])),symbol_ref('SHIPBOSS'))
 set_art(e,uniq(([row['key']] if row.get('key') else [])+native.get('keys',[])))

# Structured phase/animation metadata kept separate from frame cropping guesses.
atlas_records={}
def walk_assets(v):
 if isinstance(v,dict):
  if isinstance(v.get('key'),str) and isinstance(v.get('path'),str):atlas_records[v['key']]={k:x for k,x in v.items() if k in ['path','rect','rects','cells','cw','ch','cols','frames','pivot','w','h','size']}
  for w in v.values():walk_assets(w)
 elif isinstance(v,list):
  for w in v:walk_assets(w)
for n,v in R.items():
 if 'ART' in n:walk_assets(v)
for e in entries:
 if e['game']=='bof':set_art(e,[],atlas_records)
 e['projectileKinds']=uniq(e['projectileKinds']);e['attackCount']=len({a['id'] for a in e['attacks']})
 if e['spawn'].get('method')=='enemy' and not e['attacks']:
  e['attackNotes']='Native movement/contact actor or controller-specific attack state; live preview records genuine shots. No guessed projectile assignment.'

exec((SOURCE_DIR/'enemy_atlas_descriptions_1013.py').read_text(encoding='utf-8'))
