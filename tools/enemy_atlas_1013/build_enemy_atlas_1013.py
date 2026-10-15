from pathlib import Path
import json,re,collections,hashlib,functools
from atlas_paths_1013 import ROOT,OUT,OUTPUT,SOURCE_DIR
D=json.loads((OUT/'enemy_atlas_runtime_1013.json').read_text(encoding='utf-8'))
R=D['runtime']['registries']; T=D['runtime']['tables']; X=D['runtime']['xartSources']
E=json.loads((OUT/'enemy_atlas_enrichment_1013.json').read_text(encoding='utf-8')) if (OUT/'enemy_atlas_enrichment_1013.json').exists() else {}
R.update(E.get('registries',{}));X.update(E.get('xartSources',{}))
TEXT={p:(ROOT/p).read_text(encoding='utf-8',errors='replace') for p in D['activeFiles'] if (ROOT/p).exists()}
def uniq(v):return list(dict.fromkeys(x for x in v if x is not None))
def human(v):return re.sub(r'(?<=[a-z])(?=[A-Z])',' ',re.sub(r'[_-]+',' ',str(v))).strip().title()
@functools.cache
def ref(file,symbol):
 text=TEXT.get(file,'')
 if not text and (ROOT/file).exists():text=(ROOT/file).read_text(encoding='utf-8',errors='replace')
 m=re.search(r'\b'+re.escape(symbol)+r'\b',text)
 return {'file':file,'line':text.count('\n',0,m.start())+1 if m else 1,'symbol':symbol}
@functools.cache
def symbol_ref(symbol):
 for f,t in TEXT.items():
  if re.search(r'\b(?:function|const|let|var)\s+'+re.escape(symbol)+r'\b',t):return ref(f,symbol)
 return ref('assets/game.js',symbol)
def asset(k):
 a={'key':k}
 if k in X:a['path']=X[k]
 return a
def entry(id,name,category,game,stages,spawn,**kw):
 z={'id':id,'name':name,'category':category,'game':game,'stages':sorted(uniq(stages)),'spawn':spawn,'runtime':{},'attacks':[],'projectileKinds':[],'animationBanks':[],'artKeys':[],'sources':[],'status':'current',**kw}
 entries.append(z);return z
CONTROLLERS={'tur360':'tur360Tick','bunker':'bunkerTick','mini':'miniTick','orbital':'orbitalTick','s5space':'s5SpaceTick','sewer':'sewerTick','volc':'volcTick','s3ice':'s3IceTick','s4chase':'s4ChaseTick','s6storm':'s6StormTick','jetmaneuver':'jetManeuverTick','s7toxic':'s7ToxicTick','mutator1003':'mm1003Tick','s8mega':'s8MegaTick','elitex':'elitexTick','elite8':'elite8Tick','s9chaos':'s9ChaosTick','s9void':'s9VoidTick','s9meteor':'s9MeteorTick','ai':'aiTick','naval':'navalTick','s1tank':'tankTick','s6strike':'s6StrikeTick','s1jet':'jetTick'}
FLAGS={'_dr':'droneTick','_cn':'droneCannonTick','_l6x':'l6xTick','_h6':'l6PatternTick','_droid':'droidTick','_pt11LegacyFrost':'pt11LegacyFrostTick','_af10Jet':'ac10JetTick'}
entries=[];planned=collections.defaultdict(set);appearances=collections.defaultdict(list)
for plan in D['plans']:
 for c in plan['calls']:
  planned[c['type']].add(plan['stage']);appearances[c['type']].append({'stage':plan['stage'],'difficulty':plan['difficulty'],'wave':c.get('wave')})
 for w in plan['waves']:
  for typ in re.findall(r"(?:spawnEnemy\s*\(\s*|type\s*:\s*)['\"]([^'\"]+)",w['code']):planned[typ].add(plan['stage'])
audits={s['stage']:{r['type']:r for r in s['rows']} for s in D['spawnAudit']}
# Stage 1 map gates hide their captured wave closures from Function.toString.
# Extract only the first live branch, before the older unreachable Stage 1 branch.
g=TEXT['assets/game.js'];a=g.index('if(stageNum===1){',g.index('function buildStagePlan('));b=g.index('return _planSorted(P,stageNum);',a)
for typ in re.findall(r"['\"]([^'\"]+)['\"]",re.sub(r'/\*[\s\S]*?\*/|//[^\n]*','',g[a:b])):
 if typ in audits[1]:planned[typ].add(1)
for s,row in R.get('MM1003_SLOTS',{}).items():
 for original,kind in row.items():
  if int(s) in planned[original]:planned['mm1003_'+kind].add(int(s))
for s in range(1,10):
 for typ in list(planned):
  actual=audits[s].get(typ,{}).get('actual')
  if s in planned[typ] and actual:planned[actual].add(s)
origins=collections.defaultdict(list)
for r in D['runtime']['roster']:origins[r['type']].append({'table':r['table'],'row':r['row']})
am={}
for k,a in R['AM13_ART'].items():
 for alias in a.get('aliases',[k]):am[alias]=a
for typ in sorted(audits[1]):
 stages=sorted(planned[typ]); a=am.get(typ)
 if not stages and a:stages=a.get('stages',[a.get('stage',1)])
 if not stages:
  m=re.match(r's([1-9])',typ)
  if m:stages=[int(m[1])]
 stage=stages[0] if stages else 1; sample=audits[stage][typ]
 successful=[s for s in range(1,10) if not audits[s][typ].get('error')]
 if sample.get('error') and successful:stage=successful[0];sample=audits[stage][typ]
 fields=sample.get('fields',{});actual=sample.get('actual',typ);flags=sample.get('flags',[])
 replacements={str(s):audits[s][typ].get('actual') for s in range(1,10) if audits[s][typ].get('actual') not in [None,typ]}
 defs=[o['row'] for o in origins[typ] if isinstance(o['row'],dict)]
 name=sample.get('name') or (a or {}).get('name') or next((o.get('name') for o in defs if o.get('name')),None) or human(typ)
 if typ.startswith('mm1003_'):name=R['MM1003_DEF'].get(typ[7:],{}).get('name',name)
 controller=next((v for k,v in FLAGS.items() if k in flags),CONTROLLERS.get(sample.get('pattern'),'updatePlay'))
 status='current' if planned[typ] else 'legacy-spawnable'
 if not successful:status='culled' if typ=='s6buoy' else 'spawn-error'
 if typ=='s6buoy':status='culled';stage=6;sample=audits[6][typ]
 if typ=='xelite_':status='incomplete-dynamic-prefix'
 if replacements:status='replaced' if all(str(s) in replacements for s in stages) else 'stage-variant'
 e=entry('bof-enemy-'+typ,name,'ground' if sample.get('ground') else 'enemy','bof',stages,{'method':'enemy','type':typ,'stage':stage},status=status)
 e['runtime']={'controller':controller,'draw':'drawEnemy','type':actual,'pattern':sample.get('pattern'),'flags':flags,'fields':fields,'replacements':replacements}
 e['sources']=uniq([])+[symbol_ref(controller)]+D['literalSpawnReferences'].get(typ,[])[:8]
 e['tableOrigins']=[o['table'] for o in origins[typ]]
 e['audit']={'successfulStages':successful,'errors':{str(s):audits[s][typ]['error'] for s in range(1,10) if audits[s][typ].get('error')},'stageEvidence':'native stage-plan calls + source literals; fallback atlas metadata/type prefix','attackCoverage':'native controller + source metadata; runtime preview executes controller'}
 keys=[]
 if a:
  e['animationBanks']=[{'id':a['id'],'name':a['name'],'heading':a['heading'],'roll':a.get('roll')}]
  keys.append(a['heading']['key'])
 if typ.startswith('mm1003_'):
  md=R['MM1003_DEF'].get(typ[7:],{}); ma=R['MM1003_ART'].get(typ[7:])
  if ma:keys.append(ma['key']);e['animationBanks'].append({'id':typ,'rig':R['MM1003_RIGS'].get(md.get('rig','')),'atlas':ma})
  if md.get('attack'):e['attacks'].append({'id':md['attack'],'name':human(md['attack']),'source':ref('assets/mutator_1003.js','MM1003_DEF')})
 keys += [fields.get('art'),sample.get('art')]+[o.get('art') for o in defs]
 e['artKeys']=uniq(keys);e['art']=[asset(k) for k in e['artKeys']]
 row=sample.get('volley',{}).get('row')
 if row:e['attacks'].append({'id':row.get('pat','volley'),'name':human(row.get('pat','Native Volley')),'definition':row,'source':symbol_ref('ENEMY_VOLLEY')})
 for s,fam in R['EP13']['families'].items():
  for attack in fam.get(actual,[]):
   e['attacks'].append({'id':'ep13-'+attack,'name':{'sweep':'Sweeping laser','charge':'Charged beam','ring':'Gapped pellet ring','missile':'Missile volley','rifle':'Rifle burst','shards':'Crystal shard volley'}[attack],'stage':int(s),'source':ref('assets/enemy_patterns_1013.js','ep13Start')})
   if attack=='ring':e['projectileKinds'].append({'5':'s5split','7':'blob','8':'s8pair','9':'photon'}[s])
   if attack=='missile':e['projectileKinds'].append('emissile')
   if attack=='rifle':e['projectileKinds'].append('mg')
   if attack=='shards':e['projectileKinds'].append('warpshard')
 e['projectileKinds']=uniq(e['projectileKinds']+[o.get('fk',o.get('proj')) for o in defs]+[sample.get('fk'),fields.get('fk')])

def encounter(request,id,category,password=None):
 matches=[a for a in D['encounterAudit'] if all(a['request'].get(k)==v for k,v in request.items())]
 sample=next((a for a in matches if a.get('difficulty')=='normal'),matches[0] if matches else {})
 s=request['stage'];role=request['role'];kind=request.get('kind') or next((f['kind'] for f in D['runtime']['fights'] if f['stage']==s and f['role']==role),None)
 name=sample.get('name') or request.get('name') or D['runtime']['bossNames'].get(kind,human(kind))
 spawn={'method':'password' if password else 'encounter','stage':s,'role':role,'kind':kind,**{k:v for k,v in request.items() if k in ['phase','mimic']}}
 if password:spawn['password']=password
 e=entry(id,name,category,'bof',[s],spawn)
 e['runtime']={'controller':'bossTick','draw':'drawBoss' if role=='boss' else 'drawSubBoss','flags':sample.get('flags',[]),'fields':sample.get('fields',{}),'nativeLaunch':'on5LaunchEncounter({stage,role,kind,phase,mimic})'}
 e['audit']={'difficulties':{a['difficulty']:{'hp':a.get('fields',{}).get('hp'),'name':a.get('name'),'error':a.get('error')} for a in matches},'attackCoverage':'native books and registry metadata; native preview executes all controller states'}
 e['sources']=[ref('assets/options_nav_1005.js','on5LaunchEncounter'),symbol_ref('spawnBoss')]
 e['parts']=sample.get('parts',[])
 bd=R['SHIPBOSS'].get(kind,R['MEGABOSS'].get(kind,{})); keys=[]
 if bd.get('key'):keys.append(bd['key'])
 for p in uniq(bd.get('pats',[])+([bd['pat']] if bd.get('pat') else [])):e['attacks'].append({'id':p,'name':human(p),'source':symbol_ref('SHIPBOSS')})
 if bd.get('proj'):e['projectileKinds']=[bd['proj']]
 books=sample.get('books',{})
 for book,values in books.items():
  if isinstance(values,list):
   for p in values:
    if isinstance(p,str):e['attacks'].append({'id':p,'name':human(p),'book':book})
 if 'mimic' in request:
  f=R['F1003B_FORMS'][request['mimic']];e['name']=f['name']
  e['attacks'] += [{'id':p,'name':human(p),'source':symbol_ref('F1003B_FORMS')} for p in uniq(f['book'])]
  sig=R['HF7_BOOK'].get(str(request['mimic']))
  if sig:e['attacks'].append({'id':sig['kind'],'name':sig['name'],'definition':sig,'source':symbol_ref('HF7_BOOK')})
  e['sources'].append(symbol_ref('F1003B_FORMS'))
 e['artKeys']=uniq(keys);e['art']=[asset(k) for k in e['artKeys']]
 return e
for f in D['runtime']['fights']:encounter({'stage':f['stage'],'role':f['role'],'kind':f['kind']},'bof-'+('boss-' if f['role']=='boss' else 'miniboss-')+f['kind'],'boss' if f['role']=='boss' else 'miniboss')
for code,request in R['ON5_CODES'].items():
 if re.fullmatch(r'(?:BOSS|MINI)[1-9]',code):
  e=next(e for e in entries if e['spawn'].get('method')=='encounter' and e['spawn']['stage']==request['stage'] and e['spawn']['role']==request['role']);e.setdefault('passwords',[]).append(code)
 else:
  ident='bof-form-vileexistence-'+str(request['mimic']) if 'mimic' in request else 'bof-password-'+code
  encounter(request,ident,'form' if 'mimic' in request else 'password-boss',code)
for key in R['REBEL_KEYS']:
 a=R['AM13_ART'].get(key,{});e=entry('bof-rebel-'+key,a.get('name',human(key)),'rebel','bof',[6,10],{'method':'rebel','type':key,'stage':6,'role':'boss'})
 e['runtime']={'controller':'rebelSquadTick','draw':'rebelSquadDraw','nativeLaunch':'rebelSquadInit(b); isolate b._rebels.ships by key'}
 ship=R['REBEL_SHIPS'].get(key) if isinstance(R['REBEL_SHIPS'],dict) else R['REBEL_SHIPS'][R['REBEL_KEYS'].index(key)]
 e['animationBanks']=[{'id':key,'heading':a.get('heading'),'roll':a.get('roll')}];e['artKeys']=uniq([a.get('heading',{}).get('key'),ship if isinstance(ship,str) else ship.get('key')])
 e['art']=[asset(k) for k in e['artKeys']];e['sources']=[symbol_ref('rebelSquadInit'),symbol_ref('REBEL_SHIPS')]
for code,route,stage in [('HARR6','left',6),('REBEL6','right',6),('XHARR','left',10),('XREBEL','right',10)]:
 e=entry('bof-password-'+code,('Harrier' if route=='left' else 'Rebel Fighters')+(' · Stage X' if stage==10 else ' · Stage 6'),'password-boss','bof',[stage],{'method':'password','password':code,'stage':6,'displayStage':stage,'role':'boss','route':route})
 e['runtime']={'nativeLaunch':"GP4.route=route; GP4.stage6Only=displayStage===6; beginStage(6); GP4.routeReady=true; gp4QuickEncounter()"};e['sources']=[ref('assets/gameplay_repair_1004.js','gp4QuickEncounter')]
for code in ['HAMMER','HAMA']:
 e=entry('bof-password-'+code,'Chromium Hammer'+(' · HAMA variant' if code=='HAMA' else ''),'password-boss','bof',[5],{'method':'password','password':code,'stage':5,'role':'boss','kind':'chromehammer'})
 e['runtime']={'nativeLaunch':'ht27Start()' if code=='HAMMER' else 'ht27Variant=HAMA_VARIANT; hamaPending=true; ht27Start()'};e['sources']=[symbol_ref('ht27Start')]

OD=D['overdrive'];ostages=collections.defaultdict(list)
for mission in OD['missions']:
 for u in mission['data'].get('units',[]):
  if isinstance(u,dict):ostages[u.get('type')].append(mission['id'])
odart={}
for registry in OD['art'].values():
 if isinstance(registry,dict):odart.update(registry.get('assets',{}))
for typ,row in OD['registries']['ET'].items():
 e=entry('overdrive-enemy-'+typ,human(typ),'ground' if typ!='convoyJet' else 'enemy','overdrive',ostages[typ],{'method':'overdrive-unit','type':typ,'stage':ostages[typ][0] if ostages[typ] else 2},status='expansion')
 e['runtime']={'controller':'TD.unitTick','draw':'TD.drawUnit','nativeLaunch':'TD.makeUnit(type,x,y,options)','definition':row}
 e['sources']=[ref('expansion/topdown/js/tank.js','makeUnit')]
 if row.get('gun'):e['attacks']=[{'id':row['gun'],'name':human(row['gun']),'source':ref('expansion/topdown/js/tank.js','enemyFire')}]
 e['projectileKinds']={'burst':['mg'],'shell':['shell'],'twin':['shell'],'snipe':['snipe'],'rocket':['missile']}.get(row.get('gun'),[])
 e['artKeys']=uniq([row.get('art')]);e['art']=[{'key':k,**odart.get(k,{})} for k in e['artKeys']]
for kind,name,stage,factory,file in [('warrior','Iron Warrior',2,'makeWarrior','boss_warrior.js'),('fortress','Fortress',3,'makeFortress','campaign.js'),('machinists','Machinists · Rebel Siege',4,'makeMachinists','boss_machinists.js'),('exhibit','The Exhibit',5,'makeExhibit','boss_exhibit.js'),('gosfer','Gosfer',3,'makeGosfer','fortress_1013.js')]:
 e=entry('overdrive-boss-'+kind,name,'boss','overdrive',[stage],{'method':'overdrive-boss','kind':kind,'stage':stage,'factory':factory},status='expansion')
 e['runtime']={'nativeLaunch':'TD.'+factory+'(G,x,y)','controller':'boss.tick(G,dt)','draw':'boss.draw(ctx,G)'};e['sources']=[ref('expansion/topdown/js/'+file,factory)]
 if kind=='fortress':e['status']='legacy-spawnable'
for form in [1,2,3]:
 e=entry('overdrive-form-exhibit-'+str(form),['On Display','Breakout','Overdrive'][form-1],'form','overdrive',[5],{'method':'overdrive-boss','kind':'exhibit','factory':'makeExhibit','stage':5,'phase':form},status='expansion')
 e['runtime']={'nativeLaunch':'TD.makeExhibit(G,x,y); native form transition','controller':'exhibit.tick','draw':'exhibit.draw'};e['sources']=[ref('expansion/topdown/js/boss_exhibit.js','makeExhibit')]
for typ,name in [('wren','Wren · Foundry'),('rolf','Rolf · Vector'),('chaz','Chaz · Redline')]:
 e=entry('overdrive-rebel-'+typ,name,'rebel','overdrive',[4],{'method':'overdrive-boss','kind':'machinists','factory':'makeMachinists','stage':4,'member':typ},status='expansion')
 e['sources']=[ref('expansion/topdown/js/boss_machinists.js','makeMachinists')]

exec((SOURCE_DIR/'enrich_enemy_atlas_metadata.py').read_text(encoding='utf-8'))

result={'schemaVersion':1,'generated':'2026-10-13','title':'Bullets of Fury · Native Enemy Atlas','auditStatus':'source audit in progress; native roster and spawn census complete','entrypoints':{'bof':'index.html?bossmode=1&enemyAtlas=1','overdrive':'expansion/topdown/index.html?enemyAtlas=1'},'stages':[{'id':s['n'],'name':s['sub'],'game':'bof'} for s in R['STAGES']]+[{'id':10,'name':'Stage X · Coastal City','game':'bof'}]+[{'id':m['id'],'name':m['data'].get('name'),'game':'overdrive','hidden':m.get('hidden',False)} for m in OD['missions']],'entries':entries,'projectileCatalogue':D['runtime']['fireKinds'],'coverage':{'mainCandidateCount':len(audits[1]),'mainStagesAudited':list(audits),'encounterRuns':len(D['encounterAudit']),'overdriveUnitCount':len(OD['registries']['ET']),'overdriveMissionCount':len(OD['missions']),'nativeErrors':D['errors'],'stagePlanFaults':[{'stage':p['stage'],'difficulty':p['difficulty'],'faults':p['faults']} for p in D['plans'] if p['faults']],'sources':D['activeFiles'],'passwordPages':D['runtime']['passwordPages'],'statusCounts':dict(collections.Counter(e['status'] for e in entries)),'limitations':['Static registry books do not enumerate every dynamic attack branch. Native preview is authoritative for animation and attack behavior.','Enemy aliases and culled legacy units are retained explicitly instead of silently omitted.','Stage membership comes from current native stage-plan traces plus source literals and animation metadata; conditional reinforcements can have additional routes.']}}
result['auditStatus']='Source-backed catalogue built; native previews remain authoritative for dynamic attack sequences.'
result['coverage']['sourceDigests']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in D['activeFiles'] if (ROOT/p).is_file()}
result['coverage']['catalogueCounts']={'all':len(entries),'bof':sum(e['game']=='bof' for e in entries),'overdrive':sum(e['game']=='overdrive' for e in entries),'current':sum(e['status']=='current' for e in entries),'emptyCurrentAttackLists':sum(e['status']=='current' and not e['attacks'] for e in entries),'missingCurrentAttackDescriptions':sum(e['status']=='current' and not a.get('description') for e in entries for a in e['attacks'])}
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
OUTPUT.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print('Saved',len(entries),'entries;',dict(collections.Counter(e['game'] for e in entries)))
