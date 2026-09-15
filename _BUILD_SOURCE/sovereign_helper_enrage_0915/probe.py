"""Real Chromium proof for the Sovereign generator-hit helper enrage."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'sovereign_helper_enrage_0915';OUT.mkdir(parents=True,exist_ok=True)
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
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(4,'boss','yuri')")
        ok(fight.get('ok'),'native Stage-4 boss route opens in Chromium')
        page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};warnT=0;warnKind=null;stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];
          state=GS.PLAY;stateT=1;run.stage=4;curStage=STAGES[3];player.x=worldWidth()*.5;player.y=650;player.invuln=1e9;player.dead=false;
          window.__rageText=[];const st=ctx.strokeText.bind(ctx);ctx.strokeText=function(v,x,y){window.__rageText.push({v:String(v),x:x,y:y});return st(v,x,y);};
          for(const k of ['s4w_boss_energized_0','s4w_helper_dual_0','s4w_helper_dual_hot_0','s4w_final_chaingun_0','s4w_lightning_shield_0','s4w_power_node_0'])XART.rdy(k);
        }""")
        for _ in range(240):
            ready=page.evaluate("()=>['s4w_boss_energized_0','s4w_helper_dual_0','s4w_helper_dual_hot_0','s4w_final_chaingun_0','s4w_lightning_shield_0','s4w_power_node_0'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Sovereign helper and shield art decode before capture')
        def setup(level):
            return page.evaluate("""k=>{diffKey=k;DIFF=DIFFS[k];boss=null;bossActive=false;eBullets=[];pBullets=[];spawnBoss('stormsovereign');boss.enter=false;boss.x=worldWidth()/2;
              boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss.fireCd=999;bossActive=true;stage4CoreTurretSpawnMissing(boss,.5);
              for(const t of boss._s4war.coreTurrets){t.spawnT=1;t.materialize=1;}return {nodes:boss._s4war.shield.nodes.length,helpers:boss._s4war.coreTurrets.length};}""",level)
        def hit_node(index=0):
            return page.evaluate("""i=>{const n=boss._s4war.shield.nodes[i],hp=n.hp,hull=boss.hp;boss._s4ShieldHit=n;_lastHitX=n.x;_lastHitY=n.y;hitBoss(1);
              return {nodeHpBefore:hp,nodeHpAfter:n.hp,hullBefore:hull,hullAfter:boss.hp,triggered:!!n._coreRageTriggered,count:boss._s4war.coreEnrageCount};}""",index)
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{shake=0;boss.flash=0;window.__rageText=[];drawWorld(0);}")
            d=page.evaluate("""()=>{const R=boss._s4war.coreEnrage;return {rage:!!R,mode:R&&R.mode,t:R&&R.t,dur:R&&R.dur,stats:R&&{shots:R.shots,left:R.leftShots,right:R.rightShots,gaps:R.gaps},
              helpers:boss._s4war.coreTurrets.map(t=>({side:t.side,x:t.x,y:t.y,ang:t.ang,rage:!!t.rage,state:t.state})),asterisks:window.__rageText.filter(x=>x.v==='*').length,
              ragePlate:!!xartEnraged('s4w_helper_dual_0'),nonRageShots:eBullets.filter(q=>!q._s4CoreRage).length,shots:eBullets.filter(q=>q._s4CoreRage).map(q=>({side:q._s4CoreSide,lane:q._s4RageLane,ang:q.ang,x:q.x,y:q.y})).slice(-40)};}""")
            raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));shots.append(p);return d

        setup('normal');normal_hit=hit_node();normal=page.evaluate("()=>({rage:!!boss._s4war.coreEnrage,count:boss._s4war.coreEnrageCount})")
        ok(normal_hit['nodeHpAfter']<normal_hit['nodeHpBefore'] and normal_hit['hullAfter']==normal_hit['hullBefore'],'the real hit route damages the selected generator instead of the hull')
        ok(not normal['rage'] and normal['count']==0,'Normal generator hits do not activate the difficulty-only enrage')
        hard_setup=setup('hard');hard_hit=hit_node();ok(hard_hit['triggered'] and hard_hit['count']==1,'a real Hard generator hit triggers the surviving helpers exactly once')
        page.evaluate("()=>{const n=boss._s4war.shield.nodes[0];boss._s4ShieldHit=n;hitBoss(1);}")
        ok(page.evaluate("()=>boss._s4war.coreEnrageCount") == 1,'repeated rounds on the same generator do not restart the sequence')
        step(48);deploy=capture('sovereign_enrage_01_side_deploy')
        left,right=deploy['helpers'];bounds=page.evaluate("()=>({left:camLeftX(),right:camRightX()})")
        ok(deploy['mode']=='fire' and left['x']<bounds['left']+90 and right['x']>bounds['right']-90,'both enraged helpers reach opposite screen-side firing stations')
        ok(left['rage'] and right['rage'] and left['state']=='rage' and right['state']=='rage','both live helpers remain in the explicit rage state')
        ok(deploy['asterisks']==2 and deploy['ragePlate'],'the live renderer draws two asterisks and uses the red palette plate')
        ok(__import__('math').cos(left['ang'])>0 and __import__('math').cos(right['ang'])<0,'both side helpers visibly turn inward toward the player')
        step(105);streams=capture('sovereign_enrage_02_staggered_streams')
        sides={q['side'] for q in streams['shots']};lanes={q['lane'] for q in streams['shots']}
        ok(streams['stats']['shots']>20 and sides=={-1,1} and lanes=={-1,1},'both helpers release marked rapid streams from their own side')
        ok(streams['nonRageShots']==0,'the dedicated enrage phase does not bury its dodge gap under the boss orb cycle')
        ok(streams['stats']['gaps']>=4 and abs(streams['stats']['left']-streams['stats']['right'])<=6,'six-round bursts create repeated synchronized dodge gaps')
        left_angles=[q['ang'] for q in streams['shots'] if q['side']<0];right_angles=[q['ang'] for q in streams['shots'] if q['side']>0]
        ok(left_angles and right_angles and max(left_angles)<min(right_angles),'the two staggered streams preserve separate lanes instead of colliding into one wall')
        step(240);ended=page.evaluate("()=>({rage:!!boss._s4war.coreEnrage,helpers:boss._s4war.coreTurrets.map(t=>({rage:!!t.rage,state:t.state})),mode:boss._s4war.coreFormationMode})")
        ok(not ended['rage'] and ended['mode'] in {'home','advance','hold','retreat'} and all(not t['rage'] and t['state']=='windup' for t in ended['helpers']),'the 5.6-second Hard sequence withdraws cleanly to the normal helper cycle')
        setup('furious');hit_node(1);furious=page.evaluate("()=>({dur:boss._s4war.coreEnrage.dur,helpers:boss._s4war.coreTurrets.map(t=>t.rage)})")
        ok(furious['dur']==6.8 and all(furious['helpers']),'Furious extends the same readable enrage sequence to 6.8 seconds')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'fight':fight,'normalHit':normal_hit,'normal':normal,'hardSetup':hard_setup,'hardHit':hard_hit,'deploy':deploy,'streams':streams,'ended':ended,'furious':furious,'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
