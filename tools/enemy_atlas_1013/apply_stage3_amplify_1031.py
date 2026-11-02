"""Scoped current ice roster metadata, preserving every unrelated entry."""
from pathlib import Path
import json
MODELS={'sharddart':'shard','s3interceptor':'interceptor','ac10icejet':'interceptor','cryoeye':'eye','glaciercarrier':'carrier','s3mine':'mine'}
NAMES={'sharddart':'Shard Dart','s3interceptor':'Interceptor','ac10icejet':'Ice Interceptor','cryoeye':'Cryoeye','glaciercarrier':'Glacier Carrier','s3mine':'Ice Mine Bomber'}
DESC={'shard':'Larger regenerated ice dagger fighter. Upright banked curves and twin ice slugs; no flips or inverted flight.',
 'interceptor':'Actual eight-view turning flight with exactly two registered cannon mouths, attached muzzle flashes and clear blue-white ice bullets.',
 'eye':'Larger regenerated four-aperture eye. Commits four cardinal green/yellow/red lanes, releases the Stage2 beam texture in ice blue-white, then recovers. Fixed + pattern.',
 'carrier':'Existing whole authored Glacier Carrier pulses through its four-frame reel and fires paired clear ice bullets.',
 'mine':'Distinct ice mine bomber with mine magazines and opening bays. Banks across the field dropping pulsing shootable ice mines, then boosts offscreen; no suicide controller.'}
def apply(data,root):
 root=Path(root);art=json.loads((root/'assets/game/levels/stage_03/enemies/amplify_1031/manifest.json').read_text())
 for e in data['entries']:
  s=e.get('spawn',{});typ=s.get('type');m=MODELS.get(typ);weapon=s.get('options',{}).get('_modWeapon')
  if s.get('stage')!=3:continue
  if m:
   M=art['models'][m];e['name']=NAMES[typ];e['runtime']={'controller':'s3IceTick / I31','draw':'i31Draw','type':typ,'pattern':'s3ice','flags':['_i31'],'source':'assets/stage3_amplify_1031.js'}
   banks=M['banks'];description=DESC[m]
  elif typ=='modturret'and weapon in ['laser','sonic']:
   banks={'heading':art['banks']['turret_'+weapon]};description='Full visible hull placed on the actual ice island top mask; '+('blue source-palette sonic pressure waves.'if weapon=='sonic'else'ice laser emitted from the measured barrel mouth.')
  else:continue
  e['attacks']=[{'id':'ice-refit','name':e['name'],'description':description}];e['attackCount']=1;e['projectileKinds']=[];e['status']='current'
  e['artKeys']=[b['key']for b in banks.values()];e['art']=[{'key':b['key'],'path':b['path'],'frames':b['frames']*b['dirs'],'pivot':b['pivot']}for b in banks.values()]
  e['animationBanks']=[{('attack'if k=='sequence'else'channel'if k=='charge'else k):{**b,'kind':'strip','frames':b['frames']*b['dirs']}for k,b in banks.items()}]
  e['sources']=[{'file':'assets/stage3_amplify_1031.js','symbol':'I31'},{'file':'_BUILD_SOURCE/build_stage3_amplify_1031.py','symbol':'source bank builder'}]
 data['iceRefit1031']={'owner':'tools/enemy_atlas_1013/apply_stage3_amplify_1031.py','artManifest':'assets/game/levels/stage_03/enemies/amplify_1031/manifest.json'}
 return data
if __name__=='__main__':
 root=Path(__file__).resolve().parents[2];p=root/'assets/data/enemy_atlas_1013.json';data=apply(json.loads(p.read_text()),root);p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print('Updated Stage3 catalogue:',len(data['entries']),'entries')
