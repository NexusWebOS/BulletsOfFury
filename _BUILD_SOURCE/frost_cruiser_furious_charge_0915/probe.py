"""Real Chromium proof for the Furious Frost Cruiser spiral-volley into late-lock body charge."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'frost_cruiser_furious_charge_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks,errors,shots=[],[],[]
    def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  'if v else'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
        def log_message(self,*a):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(3,'mini','yuri')");ok(fight.get('ok'),'native Stage-3 miniboss route opens in Chromium')
        page.evaluate("""()=>{
          stagePlan=[];stageWave=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];story=null;dlgBox=function(){};
          run.stage=3;curStage=STAGES[2];diffKey='furious';DIFF=DIFFS.furious;player.x=120;player.y=590;player.invuln=1e9;player.dead=false;
          subBoss=null;subBossActive=false;boss=null;bossActive=false;playerLocks=[];warnT=0;warnKind=null;subBossTriggered=true;subBossDone=false;state=GS.PLAY;stateT=1;
          spawnSubBoss('frostcruiser');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=shipBossStationY(subBoss);subBoss._drawY=subBoss.y;subBossActive=true;
          window.__fury={born:[],states:[],hits:0,minDash:1e9};
          const old=frostCruiserSpiralRocket;frostCruiserSpiralRocket=function(b,slot,i){const q=old(b,slot,i);if(q)window.__fury.born.push(slot);return q;};
          playerHit=function(){window.__fury.hits++;player.invuln=60;};jungleCruiserSetState(subBoss,'furyRocketCharge');
          for(const k of ['nsb_frost_cruiser','cfx_stage4_chain_lightning','retm_0','retm_1','retm_2','retm_3','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'])XART.rdy(k);
        }""")
        for _ in range(220):
            ready=page.evaluate("()=>['nsb_frost_cruiser','cfx_stage4_chain_lightning','retm_0','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored hull, Retina, lightning and shared FOV plates decode before capture')
        def step(n):page.evaluate("""n=>{for(let i=0;i<n;i++){updatePlay(1/60);stateT+=1/60;const J=subBoss._jc,S=window.__fury;
          if(S.states[S.states.length-1]!==J.state)S.states.push(J.state);if(J.state==='furyDash')S.minDash=Math.min(S.minDash,Math.hypot(subBoss.x-player.x,subBoss.y-player.y));}}""",n)
        def capture(name):
            page.evaluate("()=>{shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({state:subBoss._jc.state,t:subBoss._jc.t,aimX:subBoss._jc.furyAimX,aimY:subBoss._jc.furyAimY,locked:subBoss._jc.furyLocked,rot:subBoss._jc.rot,ghost:subBoss._jcGhost,born:window.__fury.born.slice(),states:window.__fury.states.slice(),hits:window.__fury.hits,minDash:window.__fury.minDash,locks:playerLockState(),live:eBullets.filter(q=>q._frostSpiral&&!q.dead).length})")
        step(155);volley=capture('frost_fury_spiral_combo')
        step(42);yellow=capture('frost_fury_tracking_warning')
        page.evaluate("()=>{player.x=520;}");step(8);prelock=page.evaluate("()=>({locked:subBoss._jc.furyLocked,aim:subBoss._jc.furyAimX})")
        step(6);page.evaluate("()=>{player.x=100;eBullets=[];player.invuln=0;window.__fury.hits=0;}");red=capture('frost_fury_late_lock')
        step(20);dash=capture('frost_fury_committed_dash')
        guard=0
        while page.evaluate("()=>subBoss._jc.state==='furyDash'") and guard<120:step(1);guard+=1
        returned=capture('frost_fury_offscreen_return')
        while page.evaluate("()=>subBoss._jc.state==='furyReturn'") and guard<300:step(1);guard+=1
        recovered=page.evaluate("()=>({state:subBoss._jc.state,ghost:subBoss._jcGhost,hits:window.__fury.hits,minDash:window.__fury.minDash,states:window.__fury.states.slice()})")
        contact=page.evaluate("""()=>{eBullets=[];playerLocks=[];player.x=340;player.y=590;player.invuln=0;window.__fury.hits=0;
          subBoss.x=340;subBoss.y=260;subBoss._drawY=subBoss.y;subBoss._jc.furyAimX=340;subBoss._jc.furyAimY=590;jungleCruiserSetState(subBoss,'furyDash');
          for(let i=0;i<45&&window.__fury.hits===0;i++){
            /* Match the native loop's previously-rendered pose. The focused probe advances
               updatePlay manually, so keep the collision proxy in sync between frames. */
            subBoss._drawY=subBoss.y;updatePlay(1/60);
          }return {hits:window.__fury.hits,state:subBoss._jc.state,ghost:subBoss._jcGhost};}""")
        ok(volley['born']==list('LRLRLR') and volley['live']>=4,'Furious opens with the complete alternating spiral Retina volley')
        ok(yellow['state']=='furyChargeWarn' and not yellow['locked'] and yellow['aimX']<200,'body-charge FOV follows the player during its readable opening')
        ok(not prelock['locked'] and prelock['aim']>480 and red['locked'] and red['aimX']>480,'the charge commits late to the new player lane')
        ok(red['aimX']>480 and dash['state']=='furyDash' and dash['rot']<0,'moving away after lock leaves the boss facing and thrusting down the committed lane')
        ok(recovered['hits']==0 and recovered['minDash']>110,'the last-second lateral dodge clears the committed body charge')
        ok(returned['state']=='furyReturn' and returned['ghost'] and returned['states'][:3]==['furyRocketCharge','furyChargeWarn','furyDash'],'boss exits fully, returns safely from above and preserves the combo order')
        ok(recovered['state']=='recover' and not recovered['ghost'],'offscreen return is bounded and restores the encounter')
        ok(contact['hits']==1 and not contact['ghost'],'staying in the committed lane takes a real sub-boss body hit')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'volley':volley,'yellow':yellow,'prelock':prelock,'red':red,'dash':dash,'returned':returned,'recovered':recovered,'contact':contact},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
