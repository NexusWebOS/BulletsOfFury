"""Real Chromium proof for the Rime Wall Hard below-half Retina laser pair."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage3_hard_laser_balls_0915';OUT.mkdir(parents=True,exist_ok=True)
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
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(3,'boss','yuri')");ok(fight.get('ok'),'native Stage-3 boss route opens in Chromium')
        page.evaluate("""()=>{
          stagePlan=[];enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];story=null;dlgBox=function(){};
          run.stage=3;curStage=STAGES[2];diffKey='hard';DIFF=DIFFS.hard;player.x=120;player.y=610;player.invuln=1e9;player.dead=false;player.roll=null;player.somer=null;player.rollCd=0;
          subBoss=null;subBossActive=false;boss=null;bossActive=false;playerLocks=[];warnT=0;warnKind=null;bossTriggered=true;bossDone=false;state=GS.PLAY;stateT=1;
          spawnBoss('cryospear');boss.enter=false;boss.x=worldWidth()/2;boss.y=shipBossStationY(boss);boss._drawY=boss.y;boss.hp=boss.maxhp*.45;boss.fireCd=999;bossActive=true;
          window.__hardBalls={born:[],angles:[]};
          const old=stage3BossShot;stage3BossShot=function(b,slot,a,sp,k,o){const q=old(b,slot,a,sp,k,o);if(q&&q._s3LaserBall)window.__hardBalls.born.push({slot:slot,q:q});return q;};
          stage3BossHardLaserPair(boss);
          for(const k of ['nsb_rimewall_intact','l23fx_rime_orb_0','retm_0','retm_1','retm_2','retm_3','retmb_0','retmb_1','retmb_2','retmb_3'])XART.rdy(k);
        }""")
        for _ in range(220):
            ready=page.evaluate("()=>['nsb_rimewall_intact','l23fx_rime_orb_0','retm_0','retm_1','retm_2','retm_3'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Rime Wall, laser-ball and Retina plates decode before capture')
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({locks:playerLockState(),balls:eBullets.filter(q=>q._s3LaserBall&&!q.dead).map(q=>({x:q.x,y:q.y,a:Math.atan2(q.vy,q.vx),lock:q._lockId,hp:q.hp,shootable:q._shootable})),born:window.__hardBalls.born.map(x=>x.slot),roll:!!player.roll})")
        step(25);arming=capture('rime_hard_retina_charge')
        step(12);first=capture('rime_hard_first_laser_ball')
        step(16);pair=capture('rime_hard_laser_pair')
        a0=pair['balls'][0]['a'];page.evaluate("()=>{player.x=worldWidth()-90;}");step(10);tracking=capture('rime_hard_tracking_pair')
        page.evaluate("()=>{player.invuln=0;player.rollCd=0;startRoll(1);}");step(2);broken=capture('rime_hard_roll_break')
        intercept=page.evaluate("""()=>{const q=eBullets.find(x=>x._s3LaserBall&&!x.dead);if(!q)return {had:false};const before=eBullets.filter(x=>x._s3LaserBall&&!x.dead).length;
          pBullets.push({x:q.x,y:q.y,vx:0,vy:0,w:18,h:28,dmg:1,kind:'mg',t:0,dead:false});boss.fireCd=999;updatePlay(1/60);
          return {had:true,before:before,after:eBullets.filter(x=>x._s3LaserBall&&!x.dead).length,targetDead:q.dead};}""")
        step(300);spent=page.evaluate("()=>({live:eBullets.filter(q=>q._s3LaserBall&&!q.dead).length,locks:playerLockState()})")
        normal=page.evaluate("""()=>{diffKey='normal';DIFF=DIFFS.normal;playerLocks=[];eBullets=[];boss.hp=boss.maxhp*.45;return {started:stage3BossHardLaserPair(boss),locks:playerLocks.length};}""")
        ok(len(arming['locks'])==1 and len(arming['balls'])==0,'one Retina warns for both delayed laser-ball releases')
        ok(first['born']==['L'] and len(first['balls'])==1,'first laser ball releases from the physical left mount')
        ok(pair['born']==['L','R'] and len(pair['balls'])==2 and len({q['lock'] for q in pair['balls']})==1,'second release produces a two-mount pair under one lock')
        ok(all(q['shootable'] and q['hp']==2 for q in pair['balls']),'both authored laser balls are shootable two-hit threats')
        ok(abs(tracking['balls'][0]['a']-a0)>.03,'locked laser ball visibly turns toward the moved player')
        ok(broken['locks'] and broken['locks'][0]['state']=='broken' and broken['roll'],'a real barrel roll breaks the shared Retina')
        ok(intercept['had'] and intercept['targetDead'] and intercept['after']==intercept['before']-1,'a real player machine round destroys one laser ball')
        ok(spent['live']==0,'the surviving broken-lock ball flies off screen and is culled')
        ok(normal=={'started':False,'locks':0},'Normal receives no added below-half Retina pair')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'arming':arming,'first':first,'pair':pair,'tracking':tracking,'broken':broken,'intercept':intercept,'spent':spent,'normal':normal},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()

