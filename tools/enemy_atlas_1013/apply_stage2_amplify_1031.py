"""Owning, scoped catalogue migration for the Stage2 volcanic refit."""
from pathlib import Path
import json,copy

MODELS={'ash':'ash','skim':'skimmer','cinderwasp':'wasp','lance':'thunder','firejet1002':'thunder','ac10firejet':'interceptor','basaltbomber':'basalt','cruc':'crucible','miner':'minelayer','carrier':'carrier','crawl':'snake','lavasnake':'snake','lavamaw':'maw','pod':'pod','disc':'disc'}
NAMES={'ash':'Ash Fighter','skim':'Lava Skimmer','cinderwasp':'Cinderwasp','lance':'Thunderlance','firejet1002':'Thunderlance / Reinforced','ac10firejet':'Fire Interceptor','basaltbomber':'Basalt Bomber','cruc':'Crucible Gunship','miner':'Magma Minelayer','carrier':'Magma Carrier','crawl':'Lava Mechanical Serpent','lavasnake':'Lava Mechanical Serpent','lavamaw':'Lavamaw','pod':'Magma Pod','disc':'Magma Disc'}
DESCRIPTIONS={'ash':'Flame-thruster approach, firing spiral that tightens around the pilot, then a committed kamikaze dive. Ordinary fire bullets are unshootable.',
 'skimmer':'Large distinct twin-boom hull banks through curved passes, firing paired fire rounds from the actual forward rails.',
 'wasp':'Distinct four-wing Cinderwasp follows curved routes and fires short aimed fire-bullet bursts from its paired cannons.',
 'thunder':'Black/fire-red/cobalt jet, paired fire-electric gun bursts and shootable physical thunderfire missiles. Missile Retina lock and audible beeps precede launch.',
 'interceptor':'Large red jet with exactly four firing mounts: two wing guns and two forward guns. Committed FOV tell, large fire-bullet burst, recovery and exit.',
 'basalt':'Luminance-preserving gray/black steel variant of the authored Forge bomber, dropping visible arcing magma bombs onto committed ground Retinas.',
 'crucible':'Black twin-core gunship. Native one-way fire shield must be depleted before hull damage; paired large shootable magma orbs, curved repositioning, visible flashes.',
 'minelayer':'Distinct magazine-and-booster hull drops pulsing shootable air mines, then ignites engines and escapes. Eighty percent choose the short two-second laying run; others linger five seconds.',
 'carrier':'Side-entry volcanic Harrier bay opens and closes real sliding doors, deploying four new elite jets with twin flamethrowers, magma balls, turbo machine guns and moving fire walls.',
 'snake':'Erupts at a lower mountain edge, makes three snaking jumps across the field, warns a committed bite, lunges with open jaws, then recovers to the edge.',
 'maw':'Magma balls erupt from the actual top crater into a circular pattern of committed ground Retinas. Warning, eruption and recovery shorten on higher difficulty.',
 'pod':'Distinct six-petal mechanical pod opens around its core and releases an eight-position warned magma eruption, then closes and recovers.',
 'disc':'Exactly nine authored spike tips. Spins and glows, commits nine green/yellow/red FOV lanes, fires nine red fire lasers simultaneously, then releases into recovery.',
 'elite':'Carrier-launched Furnace Wing with authored heading, recoil, drift, roll and somersault banks; its role selects twin flamethrowers, paired magma balls, turbo fire guns or a moving fire wall.'}

def apply(data,root):
 root=Path(root);p=root/'assets/game/levels/stage_02/enemies/amplify_1031/manifest.json'
 if not p.is_file():return data
 art=json.loads(p.read_text(encoding='utf-8'));data['entries']=[e for e in data['entries']if e.get('spawn',{}).get('type')not in ['eye','magmaeye','magmaorb']]
 for role in ['flame','balls','guns','wall']:
  typ='v31elite_'+role
  if not any(e.get('spawn',{}).get('type')==typ for e in data['entries']):
   data['entries'].append({'id':'bof-enemy-'+typ,'name':'Furnace Wing / '+{'flame':'Flamethrowers','balls':'Magma Balls','guns':'Turbo Guns','wall':'Fire Walls'}[role],'game':'bof','category':'enemy','status':'current','stages':[2],'spawn':{'method':'enemy','type':typ,'stage':2,'options':{'_v31Role':role}}})
 for e in data['entries']:
  typ=e.get('spawn',{}).get('type');m='elite'if str(typ).startswith('v31elite_')else MODELS.get(typ)
  if 2 not in e.get('stages',[])or not m:continue
  if typ=='crawl':e['id']='bof-enemy-lavasnake';e['spawn']['type']='lavasnake';typ='lavasnake'
  if typ in NAMES:e['name']=NAMES[typ]
  M=art['models'][m];e['status']='current';e['runtime']={'controller':'volcTick / V31','draw':'v31DrawHull','type':e['spawn']['type'],'pattern':'volc','flags':['_v31'],'source':'assets/stage2_amplify_1031.js'}
  e['attacks']=[{'id':'volcanic-refit','name':e['name'],'description':DESCRIPTIONS[m]}];e['attackCount']=1;e['projectileKinds']=[]
  e['artKeys']=[b['key']for b in M['banks'].values()];e['art']=[{'key':b['key'],'path':b['path'],'frames':b['frames']*b['dirs'],'pivot':b['pivot']}for b in M['banks'].values()]
  e['animationBanks']=[{('attack'if k=='sequence'else'channel'if k=='charge'else k):{**b,'kind':'strip','frames':b['frames']*b['dirs']}for k,b in M['banks'].items()}]
  e['sources']=[{'file':'assets/stage2_amplify_1031.js','symbol':'V31'},{'file':'_BUILD_SOURCE/build_stage2_amplify_1031.py','symbol':'authored bank builder'}]
 data['volcanicRefit1031']={'owner':'tools/enemy_atlas_1013/apply_stage2_amplify_1031.py','removedEnemies':['eye','magmaorb'],'replacement':{'crawl':'lavasnake'},'artManifest':p.relative_to(root).as_posix()}
 counts=data.setdefault('coverage',{}).setdefault('catalogueCounts',{});counts.update(all=len(data['entries']),bof=sum(e.get('game')=='bof'for e in data['entries']),current=sum(e.get('status')=='current'for e in data['entries']))
 return data

if __name__=='__main__':
 root=Path(__file__).resolve().parents[2];p=root/'assets/data/enemy_atlas_1013.json';d=apply(json.loads(p.read_text(encoding='utf-8')),root);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print('Updated Stage2 catalogue through its owning migration:',len(d['entries']),'entries')
