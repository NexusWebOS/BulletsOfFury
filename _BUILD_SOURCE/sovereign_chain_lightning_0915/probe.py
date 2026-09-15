"""Real Chromium proof for Sovereign Hard/Furious chain lightning."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'sovereign_chain_lightning_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image
def main():
  checks,errors,shots=[],[],[]
  def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
  class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
    def log_message(self,*a):pass
  srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
  with sync_playwright() as pw:
    br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{srv.server_port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
    fight=page.evaluate("()=>window.__fight(4,'boss','yuri')");ok(fight.get('ok'),'native Stage-4 boss route opens in Chromium')
    page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];state=GS.PLAY;stateT=1;run.stage=4;curStage=STAGES[3];player.x=worldWidth()*.5;player.y=650;player.invuln=1e9;player.dead=false;
      window.__chainGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__chainGets.push(k);return g(k);};for(const k of ['s4w_boss_energized_0','s4w_lightning_lance_0','s4w_lightning_ball_0','s4w_muzzle_lightning_0'])XART.rdy(k);}""")
    for _ in range(240):
      ready=page.evaluate("()=>['s4w_boss_energized_0','s4w_lightning_lance_0','s4w_lightning_ball_0'].every(k=>XART.rdy(k))")
      if ready:break
      page.wait_for_timeout(35)
    ok(ready,'authored Sovereign, lightning-lance and lightning-ball art decode before capture')
    def setup(level):page.evaluate("""k=>{diffKey=k;DIFF=DIFFS[k];boss=null;bossActive=false;eBullets=[];pBullets=[];spawnBoss('stormsovereign');boss.enter=false;boss.x=worldWidth()/2;boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss.fireCd=999;bossActive=true;stage4WarfareSetMode(boss,'lightning');}""",level)
    def fire(times):
      for t in times:page.evaluate("t=>{boss._s4war.t=t;stage4WarfareBossTick(boss,0);}",t)
    def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}",n)
    def snap(name):
      page.evaluate("()=>{shake=0;boss.flash=0;window.__chainGets=[];drawWorld(0)}");d=page.evaluate("""()=>({mode:boss._s4war.mode,bolts:boss._s4war.chainBolts,orbs:boss._s4war.chainOrbs,angles:eBullets.filter(q=>q._s4ChainBolt&&q._s4ChainGroup<2).map(q=>q._s4ChainAngle),
        balls:eBullets.filter(q=>q._s4ChainOrb).map(q=>({i:q._s4ChainOrbIndex,side:q._s4wLift&&q._s4wLift.side,shootable:!!q._shootable,x:q.x,y:q.y})),gets:Array.from(new Set(window.__chainGets))})""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));shots.append(p);return d
    setup('normal');fire([1.13,1.69,2.29,2.93]);normal=page.evaluate("()=>({bolts:boss._s4war.chainBolts,orbs:boss._s4war.chainOrbs,profile:stage4SovereignChainProfile()})");ok(normal['bolts']==5 and normal['orbs']==1 and normal['profile']['outer']==[-.24,.24],'Normal retains the exact original chain-lightning count and width')
    setup('hard');fire([1.13,1.69,2.29]);step(18);hard=snap('sovereign_chain_01_hard_wide_double')
    ok(hard['bolts']==9 and hard['orbs']==0,'Hard doubles both side-cannon volleys and retains the heavy center bolt')
    ok(min(hard['angles'])<=-.38 and max(hard['angles'])>=.38 and len(set(hard['angles']))==8,'Hard visibly widens eight distinct side-cannon lanes')
    ok('cfx_stage4_chain_lightning' in hard['gets'],'the Hard render requests the authored chain-lightning combat atlas')
    setup('furious');step(175);furious=snap('sovereign_chain_02_furious_balls')
    ok(furious['bolts']==9 and furious['orbs']==3,'Furious completes nine bolts plus three lightning balls on its faster clock')
    ok(furious['balls'] and [x['side'] for x in furious['balls']]==[-1,1,-1] and all(x['shootable'] for x in furious['balls']),'the three shootable balls alternate the authored left/right racks')
    ok(any(k.startswith('s4w_lightning_ball_') for k in furious['gets']),'the Furious render requests the authored animated lightning-ball reel')
    page.evaluate("()=>{boss._s4war.t=3.35;stage4WarfareBossTick(boss,0)}");ok(page.evaluate("()=>boss._s4war.mode")=='burst','Furious exits its accelerated lightning phase at the explicit beat')
    for p in shots:
      im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
    ok(not errors,'zero Chromium page or console errors');br.close()
  srv.shutdown();res={'checks':checks,'errors':errors,'fight':fight,'normal':normal,'hard':hard,'furious':furious,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
  if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
