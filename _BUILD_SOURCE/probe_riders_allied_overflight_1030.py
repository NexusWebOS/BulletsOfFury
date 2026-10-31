from pathlib import Path
import json,sys,http.server
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_allied_overflight_1030/probe';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[];http=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
M=json.loads((R/'assets/game/levels/stage_06/boss/riders_allied_overflight_1030/manifest.json').read_text());bounds={}
for name,a in M['banks'].items():
 im=Image.open(R/a['path']).convert('RGBA');bb=[]
 for f in range(a['frames']):
  c=im.crop((f%12*128,f//12*128,f%12*128+128,f//12*128+128));b=c.getbbox();bb.append(b)
 ck(name+' has complete, unclipped even fixed cells',all(b and b[0]>0 and b[1]>0 and b[2]<128 and b[3]<128 for b in bb),dict(frames=len(bb),size=im.size));bounds[name]=bb
ck('All nine real pilot identities plus the B-42 variant are authored',len(M['banks'])==20)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text)if e.type=='error'or'draw error'in e.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof RR66!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{run.ngplus=false;diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;}");step(710)
  p.evaluate('()=>{const I=boss._rebels.h3Intro;I.i=I.rows.length;I.t=0;}');step(2)
  p.evaluate('''()=>{window.R=boss._rebels;window.G=rg4Init(boss);G.rescueDone=true;G.releaseAt=Infinity;G.rd21.next=Infinity;s6WingArsenal=()=>{};pBullets=[];for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;}window.beforeHP=boss.hp;window.beforeWing=s6Wing.ships.map(q=>({key:q.key,hp:q.hp}));rd21FleetStart(boss,G,G.rd21);}''')
  for i in range(140):
   step(3)
   if p.evaluate('G.rd21.fleet?.phase==="tell"'):break
  ck('Native formation triggers allied breakaway',p.evaluate('G.rd21.fleet.phase==="tell"&&s6Wing.ships.length>=2&&s6Wing.ships.every(q=>q._rm49Flight?.phase==="out")'))
  ck('Every depth and shadow texture is ready before flight',p.evaluate('Object.values(RR66_ART.banks).every(a=>XART.rdy(a.key))'))
  samples=[]
  for t,label in [(0,'start'),(.30,'near'),(.75,'over'),(1.20,'far'),(1.60,'edge'),(1.85,'gone')]:
   while p.evaluate('Math.min(...s6Wing.ships.map(q=>q._rm49Flight?.t||0))')<t:step(1)
   p.screenshot(path=str(W/(label+'.png')));samples.append(p.evaluate('()=>({ships:s6Wing.ships.map(q=>({key:q.key,x:q.x,y:q.y,phase:q._rm49Flight.phase,t:q._rm49Flight.t,depth:rr66Depth(q),hp:q.hp})),hulls:RR66.hulls,shadows:RR66.shadows})'))
  ck('Jets grow into the foreground overpass',all(q['depth']['i']>22 for q in samples[1]['ships']))
  ck('Jets shrink progressively as they pass the fighters',all(b['depth']['i']<a['depth']['i'] for a,b in zip(samples[2]['ships'],samples[3]['ships'])))
  ck('Every wingman remains in active travel while crossing the fighter row',p.evaluate('RR66.events.filter(e=>e.event==="overflight-crossing").length===beforeWing.length'))
  ck('No wingman enters hold until its actual craft and shadow clear the top',all(q['phase']=='hold'and q['y']<=-90 for q in samples[-1]['ships']))
  ck('Both authored flight and shadow pixels are drawn during travel',samples[-2]['hulls']>samples[0]['hulls']and samples[-2]['shadows']>samples[0]['shadows'])
  ck('Only real edge clearance causes disappearance',samples[-1]['hulls']==samples[-2]['hulls']or all(q['phase']=='hold'for q in samples[-1]['ships']))
  health=p.evaluate('()=>({before:beforeHP,boss:boss.hp,wing:beforeWing.every(a=>s6Wing.ships.some(q=>q.key===a.key&&q.hp===a.hp))})');ck('Overflight preserves allied HP and does not reset the live boss pool',health['boss']<=health['before']and health['wing'],health)
  # Draw-order fixture: real physical aircraft at an overpass point, no gameplay timer edits.
  p.evaluate('''()=>{window.drawOrder=[];const q=s6Wing.ships[0];q._rm49Flight.phase='out';q._rm49Flight.t=.8;q.x=R.ships[0].x;q.y=R.ships[0].y;const draw=ctx.drawImage,enemy=fr27RebelDrawShip,images=new Map(Object.entries(RR66_ART.banks).map(([k,a])=>[XART.get(a.key),k]));ctx.drawImage=function(im,...args){if(images.has(im))drawOrder.push(images.get(im));return draw.call(this,im,...args);};fr27RebelDrawShip=function(q){drawOrder.push('enemy-'+q.key);return enemy.apply(this,arguments);};drawWorld(0);ctx.drawImage=draw;fr27RebelDrawShip=enemy;}''')
  order=p.evaluate('drawOrder');si=[i for i,v in enumerate(order)if v.endswith('_shadow')];hi=[i for i,v in enumerate(order)if v.endswith('_hull')];ei=[i for i,v in enumerate(order)if v.startswith('enemy-')]
  ck('Shadow is under enemies and the allied hull is above their passes',si and hi and ei and max(si)<min(ei)and min(hi)>max(ei),order)
  p.screenshot(path=str(W/'layering.png'))
  p.evaluate('()=>{for(const q of s6Wing.ships){q._rm49Flight.phase="hold";q.y=-120;}G.rd21.fleet=null;}')
  step(180);ck('The original south-edge return restores ordinary wing AI',p.evaluate('s6Wing.ships.every(q=>!q._rm49Flight&&q.phase==="fight")'))
  p.evaluate('()=>{applyLizzieSkin(true)}');ck('B-42 costume selects its matching authored overflight bank',p.evaluate('rr66Model({key:"lizzie"})==="lizzie_b42"'));p.evaluate('applyLizzieSkin(false)')
  p.evaluate('run._gp4StageX=true');ck('Stage X keeps its existing wing behavior',p.evaluate('!rr49Scope()'));p.evaluate('run._gp4StageX=false;run.stage=7');ck('Other stages keep their existing wing behavior',p.evaluate('!rr49Scope()'))
  ck('No real game, draw, console or asset errors',not errors and not http,dict(errors=errors,http=http));(W/'samples.json').write_text(json.dumps(samples,indent=2));br.close()
finally:stop()
print(f'{len(checks)} native/art checks passed')
