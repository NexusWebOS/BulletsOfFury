"""Register R46 art/combat review metadata without replacing native attack books."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];M=json.loads((R/'assets/game/shared/combat/enemy_flight_1031/manifest.json').read_text(encoding='utf-8'))
p=R/'assets/data/ART_TAXONOMY.json';d=json.loads(p.read_text(encoding='utf-8'))
d={'r46_':dict(role='stage4_9_source_motion_socket_and_ordnance_review',owner='_BUILD_SOURCE/build_enemy_flight_1031.py',manifest='assets/game/shared/combat/enemy_flight_1031/manifest.json',note='Complete existing idle/attack/drift/roll/somersault sources in fixed even heading cells, measured sockets, separate native weapon modules. Native projectile/feedback/static-plate export manifests share this directory. Palette variants use actual Royal/Blackice plates. Runtime assets/enemy_flight_1031.js retains native pools, books, hit/death and sound owners.'),**{k:v for k,v in d.items()if k!='r46_'}};p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=R/'assets/data/enemy_atlas_1013.json';d=json.loads(p.read_text(encoding='utf-8'));count=0
for e in d['entries']:
 if e.get('game')!='bof'or e.get('category')!='enemy':continue
 typ=e.get('spawn',{}).get('type');stages=[s for s in e.get('stages',[])if 4<=s<=9]
 if not stages:continue
 models={str(s):M['aliases'][str(s)+'|'+typ]for s in stages if str(s)+'|'+str(typ)in M['aliases']}
 e['flightReview1031']=dict(owner='assets/enemy_flight_1031.js',stages=stages,models=models,nativeAttackBooksRetained=True,physicalMuzzles=True,ordinaryBulletInterception=False,documentation='docs/ENEMY_FLIGHT_REVIEW_1031.md');count+=1
 if models:
  banks=[]
  for name in dict.fromkeys(models.values()):
   m=M['models'][name];c=m['cell'];bank={'id':name}
   for kind,b in m['banks'].items():bank[kind]=dict(kind='cells',path=m['path'],frames=b['frames'],cell=c,pivot=m['pivot'],cells=[[0,(b['row']+f)*c,c,c]for f in range(b['frames'])])
   bank['heading']=dict(kind='cells',path=m['path'],frames=m['dirs'],cell=c,pivot=m['pivot'],cells=[[d*c,m['banks']['idle']['row']*c,c,c]for d in range(m['dirs'])]);banks.append(bank)
  e['animationBanks']=banks
  e['runtime']['draw']='r46DrawBody / native overlays and part owners';e['runtime']['source']='assets/enemy_flight_1031.js'
 if typ in['s4interceptor','s4rocket']:
  e['runtime']['controller']='s4ChaseTick / AIR17 / R46';e['attacks']=[dict(id='r46-native-sortie',name='Curved sortie / native attack and recovery',description='Banks along a finite curved route, gives the native turret/rocket controller a committed attack window, then turns and exits south. Native modular HP and missile Retina queues remain active.')]
d['stage4To9FlightReview1031']=dict(owner='assets/enemy_flight_1031.js',reviewedEntries=count,models=len(M['models']),nativeVariantAudit=116,sourceManifest='assets/game/shared/combat/enemy_flight_1031/manifest.json',notes='Source-preserving whole hull identity, complete motion banks and muzzle/socket agreement; native committed attack books, HP/parts/shields, physical missiles and hit/death owners remain authoritative.')
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print('Registered',count,'Stage4–9 enemy entries')
