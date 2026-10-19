"""Build compact, reproducible review data from actual native audit outputs."""
from pathlib import Path
import datetime,json,re
R=Path(__file__).resolve().parents[1];S=R/'_shots/overnight_combat_1019';D=R/'docs/previews/overnight_1019';D.mkdir(parents=True,exist_ok=True)
def read(path,default=None):
 p=S/path
 return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
def shipping_report(diff):
 report=read(Path(f'campaign/report-{diff}-shipping-final.json'),{'cases':[]})
 focus=read(Path(f'campaign/report-{diff}-drone-final.json'),{'cases':[]})
 if len(focus['cases'])==1 and focus['cases'][0]['stage']==3 and focus['cases'][0]['outcome']=='complete' and not focus['cases'][0]['errors']:
  report['cases']=[focus['cases'][0] if c['stage']==3 else c for c in report['cases']]
 cloak=read(Path(f'campaign/report-{diff}-stealth-mount-final.json'),{'cases':[]})
 if len(cloak['cases'])==1 and cloak['cases'][0]['stage']==6 and cloak['cases'][0].get('requestedRoute')=='right' and cloak['cases'][0]['outcome']=='complete' and not cloak['cases'][0]['errors']:
  report['cases']=[cloak['cases'][0] if c['stage']==6 and c.get('requestedRoute')=='right' else c for c in report['cases']]
 return report
matrixFolder='enemy_matrix'
matrixReport=read(Path(matrixFolder)/'report.json',{'rows':[]})
for candidate in ['enemy_matrix/native-placement','enemy_matrix/shipping-final','enemy_matrix/shipping-final-provenance','enemy_matrix/shipping-final-ai','enemy_matrix/shipping-final-factory']:
 q=read(Path(candidate)/'report.json',{})
 if (q.get('complete') if q.get('version',1)>=5 else len(q.get('rows',[]))==440) and not q.get('errors'):
  matrixFolder=candidate;matrixReport=q
matrix=matrixReport['rows']
names=json.loads((D/'names.json').read_text(encoding='utf-8')) if (D/'names.json').exists() else {}
legacy=read(Path('enemy_matrix/legacy-final/report.json'),{'rows':[]})['rows']
replacements={(q['stage'],q['difficulty'],q['spec']['type']):q for q in legacy} if matrixReport.get('version',1)<3 else {}
enemies=[]
for q in matrix:
 q=replacements.get((q['stage'],q['difficulty'],q['spec']['type']),q);m=q['metrics'];state=q['state'];c=q['spec']
 first=min([m[k] for k in ['firstProjectile','firstBeam','firstGround'] if m.get(k) is not None],default=None)
 role='gun/ordnance'
 if c['type']=='mm1003_hellhugger':role='claw/ram'
 elif c.get('flight'):role={'red':'stealth missiles','green':'stealth bombs','orange':'stealth guns'}[c['flight']['role']]+' · '+c['flight']['direction']
 elif c['pattern']=='s9meteor' or c['type']=='s4barrel':role='hazard'
 elif state.get('ram'):role='ram'
 elif state.get('support'):role='support'
 img=q.get('screenshot');folder=q.get('sourceFolder') or ('enemy_matrix/legacy-final' if (q['stage'],q['difficulty'],c['type']) in replacements else matrixFolder)
 enemies.append(dict(stage=q['stage'],difficulty=q['difficulty'],type=c['type'],pattern=c['pattern'],movement=(c.get('flight') or {}).get('direction') or (c.get('ai') or {}).get('kind'),flightRole=(c.get('flight') or {}).get('role'),groundWarnings=m.get('groundTraits',[]),role=role,hp=q['initial']['hp'],sourcePoolMeasuredBeforeLateHullFix=matrixReport.get('version',1)<3 and c['type'].startswith('s9') or matrixReport.get('version',1)<4 and c['type'] in ['s7tank','s7barge','s8deathorb','s8carrier','s8bomber','s8tentacle'],seconds=m['age'],visible=m.get('firstPixels'),warning=m.get('firstWarningPixels'),release=first,parentRelease=m.get('firstParentProjectile'),reaction=None if first is None or m.get('firstPixels') is None else first-m['firstPixels'],shots=state.get('shots',0),parentShots=m.get('parentShots'),helperShots=m.get('helperShots'),unattributedShots=m.get('unattributedShots'),beams=state.get('beams',0),ground=state.get('ground',0),helpers=m.get('maxOther',0),kinds=m.get('traits',[]),warnings=m.get('warnings',[]),screenshot=(folder+'/'+img) if img else None))
campaign=[]
for diff in ['normal','hard','furious']:
 source=read(Path(f'campaign/report-{diff}-overnight.json'),{'cases':[]})
 shipping=shipping_report(diff)
 if len(shipping['cases'])==10 and all(c['outcome']=='complete' and not c['errors'] for c in shipping['cases']):source=shipping
 for c in source['cases']:
  campaign.append(dict(id=c['id'],stage=c['stage'],difficulty=diff,route=c.get('requestedRoute'),outcome=c['outcome'],errors=c['errors'],simSeconds=c.get('latest',{}).get('t'),wallSeconds=c.get('wallSeconds'),captures=c.get('captures',[]),units=[u for u in c.get('attackAudit',{}).get('units',[]) if u.get('role')!='enemy']))
finals=[]
for diff in ['normal','hard','furious']:
 # Current focused reports hold 6R/8. Stage-9 reports would otherwise share
 # their name, so retain the independent case folder's final capture too.
 c=read(Path(f'campaign/report-{diff}-final.json'),{'cases':[]})
 for q in c['cases']:finals.append(dict(id=q['id'],outcome=q['outcome'],errors=q['errors'],stage=q['stage'],route=q.get('requestedRoute')))
 for name in [f'campaign-stage9-{diff}-final.log',f'campaign-focus-{diff}-final.log']:
  p=S/name
  if p.exists():
   for line in p.read_text(encoding='utf-8',errors='replace').splitlines():
    if line.startswith('END '):finals.append(dict(id=line.split()[1],outcome=line.split()[2],log=name))
encounters=[]
encounterSource='encounters'
currentCensus=read(Path('encounters/shipping-final/report-normal-hard-furious.json'),{})
if len(currentCensus.get('rows',[]))==57 and not currentCensus.get('errors') and not any(q['metrics'].get('nonFinite') for q in currentCensus['rows']):
 encounters=currentCensus['rows'];encounterSource='encounters/shipping-final'
else:
 for p in (S/'encounters').glob('report-*.json'):
  for q in json.loads(p.read_text(encoding='utf-8')).get('rows',[]):encounters.append(q)
rebels={}
def rebel_row(c):
 return dict(difficulty=c['diff'],gang=c['initialGang'],seconds=c['metrics']['time'],contacts=len(c['metrics']['hits']),peakEnemy=c['metrics']['peakEnemy'],peakNear=c['metrics']['peakNear'],allies=sum(q['hp']>0 and q['phase']!='leave' for q in c['allies']))
for arm in ['baseline','candidate']:
 rebels[arm]=[rebel_row(c) for c in read(Path(f'rebels/seeded-{arm}-report.json'),{'cases':[]})['cases']]
furiousFinal=[rebel_row(c) for c in read(Path('rebels/final-furious-live-report.json'),{'cases':[]})['cases']]
for q in furiousFinal:
 rebels['candidate']=[q if (p['difficulty'],p['gang'])==(q['difficulty'],q['gang']) else p for p in rebels['candidate']]
rebelSeeds=[]
for seed in [1019,2026,5019]:
 prefix='seeded' if seed==1019 else f'seed{seed}'
 arms={arm:[rebel_row(c) for c in read(Path(f'rebels/{prefix}-{arm}-report.json'),{'cases':[]})['cases']] for arm in ['baseline','candidate']}
 current=[rebel_row(c) for c in read(Path(f'rebels/seed{seed}-focused-furious-report.json'),{'cases':[]})['cases']]
 for q in current:arms['candidate']=[q if (p['difficulty'],p['gang'])==(q['difficulty'],q['gang']) else p for p in arms['candidate']]
 for before in arms['baseline']:
  after=next(p for p in arms['candidate'] if (p['difficulty'],p['gang'])==(before['difficulty'],before['gang']))
  rebelSeeds.append(dict(seed=seed,before=before,after=after))
signatureControls=[]
for label,folder in [('Unmodified signature','signature-controls'),('Locked missile control','locked-rocket-controls')]:
 for c in read(Path('rebels')/folder/'report.json',{'rows':[]})['rows']:
  m=c['metrics'];signatureControls.append(dict(control=label,difficulty=c['difficulty'],pilot=c['pilot'],kind=c['kind'],warm=c['initial']['warm'],locked=c['initial']['locked'],seconds=m['time'],contacts=len(m['contacts']),caught=m['caught'],rounds=m['shots'],ordnance=m['ord'],beams=m['beams'],phases=m['phases'],travel=m['maxTravel'],interceptable=m['interceptable']))
native={}
for label,path in [('Rime','../rime_defense_1019/native-report.json'),('Stealth','stealth/native-report.json'),('Herald escapes','herald/escape-report.json'),('Hammer','hammer/native-report.json'),('Harrier fans','fans/native-report.json'),('Volcano head','volcano/native-report.json'),('Warden timing','warden/native-report.json'),('Ally brightness','rebels/bullet-pixels-report.json'),('Lizzie Spread','lizzie-spread-native.json'),('Stage 5 hulls','stage5-hulls-native.json'),('Stage 9 hulls','late-hulls-native.json'),('Sewer entry','sewer-entry/native-report.json'),('Late heavy fleet','late-fleet/native-report.json'),('Large side arrivals','side-arrival/native-report.json'),('Restored co-op pools and pixels','restored-coop/complete/native-report.json')]:
 q=read(Path(path),{})
 checks=q.get('checks',[]);native[label]=dict(passed=q.get('passed',sum(bool(c.get('passed')) for c in checks)),failed=q.get('failed',sum(not c.get('passed') for c in checks)),errors=q.get('errors',[]),path=path)
q=read(Path('drone-commit/native-report.json'),{})
if q:native['Diagonal drone commitment']=dict(passed=q['passed'],failed=q['failed'],errors=q['errors'],path='drone-commit/native-report.json')
q=read(Path('stealth-pilots/native-report.json'),{})
if q:native['All nine cloaked pilots and docked mount']=dict(passed=q['passed'],failed=q['failed'],errors=q['errors'],path='stealth-pilots/native-report.json')
gallery=[('Rime inside the shoulder rings','../rime_defense_1019/after-normal-shoulder-charge.png'),('Nyx cloak','stealth/nyx-loop-warning.png'),('Friendly stealth silhouette','stealth/friendly-stealth.png'),('Native Hammer rolling','hammer/ball.png'),('Native Hammer spin','hammer/spin.png'),('Harrier rotors; left covering missile rack destroyed','fans/normal-fans.png'),('Herald wing-rake escape','herald/escape-wing-rake.png'),('Rebels Normal','rebels/seeded-candidate-normal-gang-025.png'),('Rebels Furious','rebels/seeded-candidate-furious-gang-025.png')]
gallery=[dict(title=t,path=p) for t,p in gallery if (S/p).exists()]
gallery.extend(dict(title=t,path=p) for t,p in [('Volcano head: real generated turn and twin-eye beams','volcano/native-03.jpg'),('Warden Furious claw warning','warden/furious-claw.jpg')] if (S/p).exists())
gallery.extend(dict(title=t,path=p) for t,p in [('Toxic skimmer: repaired top entrance','sewer-entry/furious-top.jpg'),('Highway rocket plane: real volley after its tell','side-arrival/s4rocket.jpg'),('Orbital skimmer: now survives its large side spawn','side-arrival/s5skimmer.jpg'),('Storm skimmer: fixed landing targets','side-arrival/s6skimmer.jpg'),('Restored toxic barge hull','late-fleet/s7barge.jpg'),('Restored Stage 8 carrier','late-fleet/s8carrier.jpg')] if (S/p).exists())
gallery.extend(dict(title=t,path=p) for t,p in [('Co-op toxic tank: native two-seat HUD and restored pool','restored-coop/complete/s7tank.jpg'),('Co-op carrier: restored party pool','restored-coop/complete/s8carrier.jpg')] if (S/p).exists())
gallery.extend(dict(title='Diagonal ice drone: native Furious charge and release',path='drone-commit/furious-volley.jpg') for _ in [0] if (S/'drone-commit/furious-volley.jpg').exists())
gallery.extend(dict(title=t,path=p) for t,p in [('Lizzie before: mount remains behind while the formation moves','stealth-pilots/lizzie-mounted-before.jpg'),('Lizzie after: the native docked mount follows her cloaked hull','stealth-pilots/lizzie-natural-mounted-cloak.jpg')] if (S/p).exists())
art=[dict(title='Hammer: 31 real rolling poses',path='hammer-ball-accepted.webp',onion='hammer-ball-onions.png',frames=31),dict(title='Hammer: eight real directions on the native reel',path='hammer-twirl-accepted.webp',onion='hammer-twirl-onions.png',frames=8),dict(title='Stealth: 32-pose loop',path='cloak-loop.webp',onion='cloak-loop-onions.png',frames=32),dict(title='Stealth: 29-pose forming sequence',path='cloak-in.webp',onion='cloak-in-onions.png',frames=29),dict(title='Stealth: 29-pose dissipation, accepted forming poses reversed',path='cloak-out.webp',onion='cloak-out-onions.png',frames=29)]
art.append(dict(title='Harrier: 16 authored rotor positions from PixelLab exact workbench',path='harrier-fan-accepted.webp',onion='harrier-fan-onions.png',frames=16))
art.extend(dict(title=t,path='volcano/'+p+'-accepted.webp',onion='volcano/'+p+'-accepted-onions.png',frames=n) for t,p,n in [('Volcano head: 32 generated turning poses','spin',32),('Volcano head: 16 charge frames, ten distinct lamp states','charge',16)])
forms=[]
for c in read(Path('forms/isolated-final/report.json'),{'cases':[]})['cases']:
 m=c['metrics'];forms.append(dict(scene=c['scene'],difficulty=c['difficulty'],seconds=m['time'],morphed=bool(m.get('finishedByMorph')),shots=m['shots'],beam=m['firstBeamPixels'],modules={k:dict(keys=len(v['keys']),rotation=v['maxRot']-v['minRot'],travel=v['maxX']-v['minX']) for k,v in m['modules'].items()},sounds=m['sounds']))
books=[]
for c in read(Path('forms/colossus-book/report.json'),{'cases':[]})['cases']:
 m=c['metrics'];events=m.get('archives',[]);books.append(dict(difficulty=c['difficulty'],seconds=m['time'],beam=m['firstBeamPixels'],missiles=sum(e['event']=='core-missile' for e in events),arms=[dict(side=e['side'],reaction=e['reaction']) for e in events if e['event']=='arm-laser'],shots=m['shots']))
escapes=[dict(difficulty=c['difficulty'],pilot=c['pilot'],kind=c['kind'],edge=c['edge'],warm=c['initial']['warm'],contacts=len(c['metrics']['contacts']),caught=c['metrics']['caught']) for c in read(Path('rebels/escapes/report.json'),{'rows':[]})['rows']]
wardens={}
for arm,folder in [('before','warden-long'),('after','warden-final')]:
 wardens[arm]=[dict(difficulty=q['difficulty'],seconds=q['metrics']['time'],shots=q['metrics']['shots'],ground=q['metrics']['ground'],phases=q['metrics']['phases'],warnings=q['metrics']['warningCalls']) for q in read(Path('encounters')/folder/'report-normal-hard-furious.json',{'rows':[]})['rows']]
passwordReport=read(Path('passwords/final-shipping/report.json'),{'rows':[],'errors':[]})
coopReport=read(Path('restored-coop/complete/native-report.json'),{'rows':[]})
coopPools=[dict(stage=q['stage'],difficulty=q['difficulty'],kind=q['kind'],solo=q['solo'],before=q['before'],party=q['party'],multiplier=q['multiplier'],ratio=q['ratio']) for q in coopReport['rows']]
passwords=[dict(code=q['code'],difficulty=q['difficulty'],seconds=q['metrics']['sim'],realtime=q['realtime'],shots=q['metrics']['shots'],first=q['metrics']['firstProjectile'],warning=q['metrics']['firstWarning'],peak=q['metrics']['peak'],clockDrift=q.get('maxClockDrift'),mediaAdvance=q.get('mediaAdvanced'),finite=q['finite']) for q in passwordReport['rows']]
motions=[];projectiles=[]
fleetMotions=[];shippingProgress=[]
for diff in ['normal','hard','furious']:
 for c in read(Path(f'campaign/report-{diff}-late-fleet-final.json'),{'cases':[]})['cases']:
  fleetMotions.append(dict(stage=c['stage'],difficulty=diff,outcome=c['outcome'],errors=c['errors'],seconds=c.get('latest',{}).get('t')))
 for c in shipping_report(diff)['cases']:
  shippingProgress.append(dict(id=c['id'],stage=c['stage'],difficulty=diff,route=c.get('requestedRoute'),outcome=c['outcome'],errors=c['errors'],seconds=c.get('latest',{}).get('t')))
rebelFinals=[dict(stage=c['stage'],difficulty='furious',route=c.get('requestedRoute'),outcome=c['outcome'],errors=c['errors'],seconds=c.get('latest',{}).get('t')) for c in read(Path('campaign/report-furious-rebel-final.json'),{'cases':[]})['cases']]
for diff in ['normal','hard','furious']:
 for c in read(Path(f'campaign/report-{diff}-motion-final.json'),{'cases':[]})['cases']:
  motions.append(dict(stage=c['stage'],difficulty=diff,outcome=c['outcome'],errors=c['errors'],seconds=c.get('latest',{}).get('t')))
  for u in c.get('attackAudit',{}).get('units',[]):
   if u['role']=='enemy':continue
   for t in u.get('projectileTraits',[]):projectiles.append(dict(stage=c['stage'],difficulty=diff,owner=u['kind'],**t))
earlyComparisons=[dict(kind=q['kind'],difficulty=q['difficulty'],seconds=q['metrics']['time'],rounds=q['metrics']['shots'],first=q['metrics']['firstProjectile'],beams=q['metrics']['beamFrames']/60,speed=q['metrics']['maxSpeed']) for q in read(Path('encounters/early-seeded-comparison/report-normal-hard-furious.json'),{'rows':[]})['rows']]
hammerBooks=[]
for q in read(Path('forms/hammer-full-book/report.json'),{'cases':[]})['cases']:
 m=q['metrics'];keys=m.get('stateKeys',{});hammerBooks.append(dict(difficulty=q['difficulty'],seconds=m['time'],morphed=bool(m.get('finishedByMorph')),warn=len(keys.get('fight:warn',[])),ball=len(keys.get('fight:ball',[])),whirl=len(keys.get('fight:whirlwind',[])),nova=len(keys.get('fight:nova_charge',[])),rounds=m['shots']))
data=dict(generated=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Native Chromium; protected visible pilot. Full campaign runs verify progression, not human win rates. The isolated roster uses a sixteen-second window without player fire. First warning pixels are measured through the native warning renderer; a dash means unobserved, not necessarily absent. Equal-window encounter census includes native opening/armor/intro time.',matrixVersion=matrixReport.get('version'),matrixComplete=matrixReport.get('complete',False),matrixExpected=matrixReport.get('expected'),matrixMethod=matrixReport.get('method'),matrixSource=matrixFolder,encounterSource=encounterSource,campaign=campaign,shippingProgress=shippingProgress,finals=finals,enemies=enemies,encounters=encounters,earlyComparisons=earlyComparisons,hammerBooks=hammerBooks,rebels=rebels,rebelSeeds=rebelSeeds,signatureControls=signatureControls,rebelFinals=rebelFinals,native=native,gallery=gallery,art=art,forms=forms,books=books,escapes=escapes,wardens=wardens,passwords=passwords,passwordErrors=passwordReport['errors'],motions=motions,fleetMotions=fleetMotions,coopPools=coopPools,projectiles=projectiles,names=names)
(D/'report.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
qa=R/'docs/qa/overnight_combat_1019.json';qa.write_text(json.dumps(dict(generated=data['generated'],campaignCases=len(campaign),campaignCompleted=sum(c['outcome']=='complete' and not c['errors'] for c in campaign),shippingProgress=shippingProgress,enemyCases=len(enemies),matrixVersion=data['matrixVersion'],matrixComplete=data['matrixComplete'],matrixExpected=data['matrixExpected'],matrixSource=matrixFolder,matrixMethod=data['matrixMethod'],encounterCases=len(encounters),encounterSource=encounterSource,earlyComparisons=earlyComparisons,hammerBooks=hammerBooks,native=native,finals=finals,motionFinals=motions,fleetMotions=fleetMotions,coopPools=coopPools,rebelFinals=rebelFinals,rebelSeeds=rebelSeeds,signatureControls=signatureControls,passwordCases=len(passwords),passwordErrors=data['passwordErrors'],method=data['method']),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(campaign=len(campaign),completed=sum(c['outcome']=='complete' for c in campaign),enemies=len(enemies),encounters=len(encounters),native=native)))
