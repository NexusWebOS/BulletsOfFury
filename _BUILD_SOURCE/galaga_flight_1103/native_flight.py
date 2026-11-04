from pathlib import Path
import ast,sys,time
R=Path(__file__).resolve().parents[2]
W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'))
SETUP=next(ast.literal_eval(n.value)for n in t.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='SETUP'for x in n.targets))
def boot(p):
 p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,body='window.BOF_ONLINE_CONFIG={};',content_type='application/javascript'))
 p.goto('http://127.0.0.1:65042/game/index.html?quality=high&flight=1103',wait_until='load',timeout=180000)
 p.wait_for_function('window.__bofFrames>4',timeout=60000)
 p.evaluate(TRAP_RAF)
def setup(p,stage=6):
 p.evaluate(SETUP,{'stage':stage,'diff':'furious','pilot':'cole'})
 p.evaluate('''()=>{CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=999999;_adaptiveSpawnT=999999;tryAdaptiveReinforcement=()=>{};subBossDone=subBossTriggered=aminiTriggered=true;curStage={...curStage,length:99999};player.x=worldWidth()/2;player.y=VH-55;camX=player.x-VW/2;}''')
 p.evaluate('''s=>{const keys=new Set(ls112Keys(s)),seen=new Set();function visit(v){if(!v||typeof v!=='object'||seen.has(v))return;seen.add(v);if(typeof v.key==='string'&&XART._src[v.key])keys.add(v.key);for(const x of Object.values(v))if(x&&typeof x==='object')visit(x);}visit({1:S1A_ART,2:V31_ART,3:I31_ART,4:S411_ART,5:S511_ART,6:S611_ART,7:S711_ART,8:S811_ART,9:S911_ART}[s]);for(const m of Object.values(R46_ART.models))if(m.stages?.includes(s))visit(m);window.qaFlightKeys=[...keys];for(const k of qaFlightKeys)XART.rdy(k);}''',stage)
 for i in range(1200):
  ready=p.evaluate('()=>{stageLoadTick();return qaFlightKeys.every(k=>XART.rdy(k));}')
  if ready:break
  p.wait_for_timeout(25)
 assert ready,'Native art did not warm'
 # Draw empty native scene to request the current pilot/HUD sources, then wait
 # for decoding. No aircraft or attack timers are advanced before spawning.
 p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 p.wait_for_timeout(700)
def spawn(p,kind):
 return p.evaluate('''kind=>{enemies=[];eBullets=[];pBullets=[];GF113.groups=[];GF113.serial=0;GF113.events=[];window.fleet=[];const left=worldWidth()*.28,right=worldWidth()*.72;
 const specs=kind==='small'?[['l6v_s0',left,3],['l6v_r0',right,3]]:kind==='medium'?[['s6skimmer',left,2],['s6skimmer',right,2]]:kind==='large'?[['l6v_s1',left,2],['l6v_r1',right,2]]:[['l6v_s0',left,2],['s6skimmer',right,2],['l6v_r1',left,1],['l6v_s1',right,1]];
 for(const [type,x,n]of specs)for(let i=0;i<n;i++)fleet.push(spawnEnemy(type,x,-240,{}));
 return fleet.map(e=>({type:e.type,id:e._gf113?.id,size:e._gf113?.size,hp:e.hp,w:e.w,h:e.h}));}''',kind)
