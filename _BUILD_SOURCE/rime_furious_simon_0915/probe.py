"""Real Chromium proof for the live Rime Wall Furious Simon-Says cannon tell."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'rime_furious_simon_0915';OUT.mkdir(parents=True,exist_ok=True)
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
          run.stage=3;curStage=STAGES[2];diffKey='furious';DIFF=DIFFS.furious;player.x=480;player.y=610;player.invuln=1e9;player.dead=false;player.roll=null;player.somer=null;
          subBoss=null;subBossActive=false;boss=null;bossActive=false;playerLocks=[];warnT=0;warnKind=null;bossTriggered=true;bossDone=false;state=GS.PLAY;stateT=1;
          spawnBoss('cryospear');boss.enter=false;boss.x=worldWidth()/2;boss.y=shipBossStationY(boss);boss._drawY=boss.y;boss.hp=boss.maxhp*.20;boss.fireCd=0;bossActive=true;
          window.__simonGets=[];window.__simonDraws=0;const get0=XART.get.bind(XART),draw0=ctx.drawImage.bind(ctx);
          XART.get=function(k){window.__simonGets.push(k);return get0(k);};ctx.drawImage=function(){window.__simonDraws++;return draw0(...arguments);};
          for(const k of ['nsb_rimewall_intact','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_yellow_danger','bmfx_alert_red_danger','l23fx_rime_laser_3','l23fx_rime_orb_0','retm_0','retm_1','retm_2','retm_3'])XART.rdy(k);
        }""")
        for _ in range(240):
            ready=page.evaluate("()=>['nsb_rimewall_intact','bmfx_fov_yellow_tall','bmfx_fov_red_tall','l23fx_rime_laser_3','l23fx_rime_orb_0','retm_0','retm_1','retm_2','retm_3'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored hull, yellow/red FOV, beam, Retina and Rime-orb art decode before capture')
        started=page.evaluate("""()=>{window.__simonGets=[];shipBossAttack(boss);return {pat:boss._sbPat,feint:!!boss._s3boss.furyFeint,locks:playerLocks.length,launches:playerLocks[0]&&playerLocks[0].launches.length,actual:boss._s3boss.furyFeint&&boss._s3boss.furyFeint.actual};}""")
        ok(started['pat']=='s3walloverdrive' and started['feint'],'the real boss attack selector enters the Furious overdrive feint')
        ok(started['locks']==1 and started['launches']==2,'the repaired live route also opens the Hard-pattern Retina laser-ball pair')
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{shake=0;window.__simonGets=[];window.__simonDraws=0;drawWorld(0);}")
            data=page.evaluate("()=>({gets:window.__simonGets.slice(),draws:window.__simonDraws,feint:boss._s3boss.furyFeint&&{t:boss._s3boss.furyFeint.t,i:boss._s3boss.furyFeint.i,slot:boss._s3boss.furyFeint.seq[Math.min(4,Math.floor(boss._s3boss.furyFeint.t/boss._s3boss.furyFeint.beat))],color:boss._s3boss.furyFeint.colors[Math.min(4,Math.floor(boss._s3boss.furyFeint.t/boss._s3boss.furyFeint.beat))]},beam:boss._l23Beam&&{slots:boss._l23Beam.slots,angles:boss._l23Beam.angles,t:boss._l23Beam.t,warm:boss._l23Beam.warm,active:boss._l23Beam.active,furious:boss._l23Beam._furySimon,released:boss._l23Beam.released}})")
            png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p);return data
        step(5);yellow1=capture('fury_simon_01_yellow')
        step(18);red1=capture('fury_simon_02_red')
        step(21);yellow2=capture('fury_simon_03_yellow')
        step(20);red2=capture('fury_simon_04_red')
        step(19);final=capture('fury_simon_05_red_flash')
        step(20);release=capture('fury_simon_06_committed_beam')
        seq=[yellow1,red1,yellow2,red2,final]
        ok([x['feint']['color'] for x in seq]==['yellow','red','yellow','red','red'],'the visible cue sequence is exactly yellow/red/yellow/red/red')
        ok(all('bmfx_fov_green_tall' not in x['gets'] for x in seq),'Furious never requests the green FOV')
        ok(all(not any(k.startswith('bmfx_alert_') or k in ('nwarn_alert','nwarn_yield') for k in x['gets']) for x in seq),'Furious requests no overhead asterisk/alert plate')
        ok(len({x['feint']['slot'] for x in seq})==2 and final['feint']['slot']==started['actual'],'both physical cannons feint and the final red flash identifies the firing side')
        ok(final['draws']>0 and 'bmfx_fov_red_tall' in final['gets'],'the final committed lane visibly flashes with authored red pixels')
        ok(release['beam'] and release['beam']['furious'] and release['beam']['released'] and release['beam']['slots']==[started['actual']],'only the final Simon-Says cannon releases a live beam')
        angle0=release['beam']['angles'][0]
        page.evaluate("()=>{player.x=80;player.y=700;}");step(8)
        fixed=page.evaluate("()=>boss._l23Beam&&boss._l23Beam.angles[0]")
        ok(fixed is not None and abs(fixed-angle0)<1e-8,'the committed beam does not retarget after the player moves')
        collision=page.evaluate("""()=>{const B=boss._l23Beam,p=shipBossMount(boss,B.slots[0]),a=B.angles[0],hit0=playerHit;eBullets=[];playerLocks=[];run.shield=0;special=null;player.roll=null;player.somer=null;player._spin=null;player.x=p.x+Math.cos(a)*245;player.y=p.y+Math.sin(a)*245;player.invuln=0;player.dead=false;window.__simonHitCalls=0;playerHit=function(){window.__simonHitCalls++;return hit0();};const lives=run.lives,px=player.x-p.x,py=player.y-p.y,along=px*Math.cos(a)+py*Math.sin(a),across=Math.abs(px*Math.sin(a)-py*Math.cos(a)),before={t:B.t,warm:B.warm,active:B.active,p:p,player:{x:player.x,y:player.y},along:along,across:across};l23BossBeamTick(boss,1/60);playerHit=hit0;return {calls:window.__simonHitCalls,lives0:lives,lives1:run.lives,inv:player.invuln,dead:player.dead,before:before,afterT:boss._l23Beam&&boss._l23Beam.t};}""")
        ok(collision['calls']==1,'the released final lane reaches the real player-hit boundary')
        isolation=page.evaluate("""()=>{function arm(k){diffKey=k;DIFF=DIFFS[k];playerLocks=[];eBullets=[];boss._l23Beam=null;boss._s3boss.furyFeint=null;boss._s3boss.charge=null;boss._sbPhase=3;boss._sbStep=0;boss.hp=boss.maxhp*.20;shipBossAttack(boss);return {feint:!!boss._s3boss.furyFeint,beam:!!boss._l23Beam,locks:playerLocks.length};}return {hard:arm('hard'),normal:arm('normal')};}""")
        ok(isolation['hard']=={'feint':False,'beam':True,'locks':1},'Hard keeps the standard three-color beam and receives its live laser-ball pair')
        ok(isolation['normal']=={'feint':False,'beam':True,'locks':0},'Normal keeps the standard beam and receives no Hard-only laser balls')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'started':started,'yellow1':yellow1,'red1':red1,'yellow2':yellow2,'red2':red2,'final':final,'release':release,'collision':collision,'isolation':isolation},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
