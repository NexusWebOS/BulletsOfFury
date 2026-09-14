"""Native proof for the first easy-to-hard queue entries."""
import base64,json,sys,threading,http.server
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'_shots/supply_audit_0914';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
checks=[];errors=[];shots=[];details={}
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  'if v else'FAIL ')+label,flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate("()=>{__auto=function(){};window.__labels=[];const f=ctx.fillText;ctx.fillText=function(t,x,y){if(String(t).startsWith('SPACE FIGHTER')||String(t).includes('GRAVITY MODE'))__labels.push({text:t,x,y,width:ctx.measureText(t).width});return f.apply(this,arguments);};window.__blits=0;const d=ctx.drawImage;ctx.drawImage=function(){__blits++;return d.apply(this,arguments);};}")
 def step(n):
  for i in range(0,n,30):pg.evaluate('n=>__step(n)',min(30,n-i));pg.wait_for_timeout(12)
 def shot(name,frame=False):
  path=O/(name+'.png')
  if frame:pg.locator('#game-frame').screenshot(path=str(path))
  else:path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")))
  shots.append(path)
 pg.evaluate("()=>{run.mode='arcade';run.stage=5;beginStage(5);run.gravityShipReady=false;setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch(0);gravityModeStart();drawLaunch._phase='gravity';drawLaunch._dist=SEG_B3+SEG_B1+240;gravityMode.phase='reveal';gravityMode.t=.3;gravityMode.dialogueT=0;run.pilot='decker';pilotIndex=PILOTS.findIndex(p=>p.key==='decker');}")
 for _ in range(180):
  if pg.evaluate('()=>!!spaceAtlasCanvas("ship_base","decker")'):break
  pg.wait_for_timeout(35)
 pg.evaluate('()=>{__labels=[];drawLaunch(0);}')
 ok(pg.evaluate("()=>__labels.some(q=>q.text==='SPACE FIGHTER DRAVEN'&&q.x-q.width/2>=0&&q.x+q.width/2<=480)"),'Decker reveals SPACE FIGHTER DRAVEN inside the native screen')
 shot('decker_draven')
 def prep(mode,key):
  pg.evaluate("a=>{run.mode=a[0];diffKey=a[1];DIFF=difficultyForRun(run.mode,diffKey);run.stage=1;curStage=STAGES[0];beginStage(1);setState(GS.PLAY);run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;playerHit=function(){};story=null;stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;bossWarned=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];special=null;__auto=function(){};lifeUpRolled=true;stageTimer=curStage.length*.35+.1;_sc1=_sc2=_mc2=true;_mc1=false;run._missileBonus=null;run.bombs=10;pwTimer=spTimer=0;}",[mode,key])
 for mode in ['campaign','arcade']:
  for key in ['easy','normal','hard','furious']:
   prep(mode,key)
   pg.evaluate('()=>{window.__savedRandom=Math.random;Math.random=()=>.1;}');step(1);pg.evaluate('()=>{Math.random=__savedRandom;}')
   boosted=key in ['hard','furious']
   ok(pg.evaluate('v=>powerups.filter(p=>p.kind==="mcrate").length===1&&!!(run._missileBonus&&run._missileBonus.pending===1)===v',boosted),mode+' '+key+' real level scheduler rolls one bonus only at elevated difficulty')
   ok(pg.evaluate('()=>powerups.filter(p=>p.kind==="mcrate").every(p=>p.x>=camLeftX()+40&&p.x<=camRightX()-40)'),mode+' '+key+' scheduled missile crate stays inside the current camera')
 # Last scene: Arcade/Furious; the original crate blocks its queued extra.
 step(150)
 ok(pg.evaluate('()=>powerups.filter(p=>p.kind==="mcrate").length===1&&run._missileBonus.pending===1'),'bonus waits behind the original missile box')
 shot('original_supply',True)
 pg.evaluate("()=>{const p=powerups.find(p=>p.kind==='mcrate');p.hp=1;p.x=player.x;p.y=player.y-65;p.vy=0;run.weapon=0;run.wlevel=0;}")
 pg.keyboard.down('j');step(30);pg.keyboard.up('j');step(1)
 ok(pg.evaluate("()=>powerups.some(p=>/^missilepack/.test(p.kind))&&!powerups.some(p=>p.kind==='mcrate'&&!p.dead)"),'actual gun input breaks the original box into collectible ammo')
 step(15)
 ok(pg.evaluate("()=>run._missileBonus.pending===1&&!powerups.some(p=>p._bonusSupply)"),'the released ammo pickup also blocks a stacked bonus box')
 pg.evaluate("()=>{for(const p of powerups)if(/^missilepack/.test(p.kind)){p.x=player.x;p.y=player.y;p.vy=0;}}")
 step(2)
 ok(pg.evaluate("()=>powerups.filter(p=>p._bonusSupply).length===1&&run._missileBonus.pending===0&&run.bombs>10"),'collecting real ammo releases one queued bonus without rerolling')
 step(70);shot('bonus_supply',True)
 delay=pg.evaluate('()=>run._missileBonus.delay');pg.evaluate("()=>setState('paused')");step(90)
 ok(abs(pg.evaluate('()=>run._missileBonus.delay')-delay)<1e-9,'pause freezes the bonus-supply delay')
 pg.evaluate("()=>{setState(GS.PLAY);powerups=[];run._missileBonus={pending:1,delay:2};player.dead=false;player.invuln=0;run.shield=0;special=null;window.__realHit();}");step(12)
 details['death']=pg.evaluate('()=>({dead:player.dead,delay:run._missileBonus.delay,kinds:powerups.map(p=>p.kind),bonus:powerups.some(p=>p._bonusSupply)})');print(details['death'],flush=True)
 ok(details['death']['dead'] and details['death']['delay']==2 and not details['death']['bonus'],'dead player cannot advance queued restock')
 # Exercise the shared factory without reviving a retired modular boss art rig.
 prep('arcade','hard');pg.evaluate('()=>{Math.random=()=>.1;}')
 details['phase']=pg.evaluate("()=>{powerups=[];run._missileBonus=null;const p=scriptedMissileSupply(player.x,'missilepack10');return{packs:powerups.map(p=>p._pack),pending:run._missileBonus&&run._missileBonus.pending,inView:p.x>=camLeftX()+40&&p.x<=camRightX()-40};}")
 pg.evaluate('()=>{Math.random=__savedRandom;}')
 q=details['phase'];ok(q.get('packs')==['missilepack10'] and q.get('pending')==1 and q.get('inView'),'scripted supply factory preserves its guaranteed x10 and earns one separate bonus roll')
 pg.evaluate("()=>{powerups=[];run._missileBonus=null;player.dead=false;__fight(1,'boss','yuri');__auto=function(){};}")
 for _ in range(100):
  if pg.evaluate('()=>boss&&!boss.enter'):break
  step(6)
 pg.evaluate("()=>{diffKey='hard';powerups=[];boss._missileSupply={t:0,due:7/missileSupplyRate()};run._missileBonus=null;}")
 step(330)
 ok(pg.evaluate('()=>!powerups.some(p=>p._bossSupply)'),'Hard boss supply does not arrive before its 5.6-second opening delay')
 step(7)
 ok(pg.evaluate('()=>powerups.filter(p=>p._bossSupply).length===1&&boss._missileSupply.due===14.4&&!run._missileBonus'),'Hard boss opening and repeat use 25% faster cadence without a second bonus roll')
 details['loopError']=pg.evaluate('()=>window.__err||null');details['blits']=pg.evaluate('()=>__blits')
 ok(details['blits']>0 and not errors and not details['loopError'],'zero page, console and controlled-loop errors')
 b.close()
srv.shutdown()
(O/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'screenshots':[str(s)for s in shots]},indent=2),encoding='utf-8')
n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
if n!=len(checks):raise SystemExit(1)
