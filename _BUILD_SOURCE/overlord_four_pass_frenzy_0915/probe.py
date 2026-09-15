"""Real Chromium proof for Overlord-X's alternating four-pass half-health frenzy."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'overlord_four_pass_frenzy_0915';OUT.mkdir(parents=True,exist_ok=True)
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
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(1,'boss','yuri')");ok(fight.get('ok'),'native Stage-1 boss route opens in Chromium')
        page.evaluate("""()=>{
          stagePlan=[];enemies=[];eBullets=[];pBullets=[];particles=[];story=null;dlgBox=function(){};playerHit=function(){};
          run.stage=1;curStage=STAGES[0];player.x=110;player.y=430;boss=null;bossActive=false;bossWarned=true;warnT=0;spawnBoss('damkeeper');
          boss._ovIntro.done=true;boss.enter=false;boss._noHit=false;boss._ovInit=1;boss._enraged=true;boss._ovPassUsed=false;boss._ovPassSeq=null;
          boss._ovState='fight';boss._ovChargeCd=0;boss.fireCd=999;boss.x=240;boss.y=112;boss._pivot=0;state=GS.PLAY;stateT=1;
          window.__passLog=[];window.__rainLog=[];window.__beeps=0;
          const sr=ovPassRain;ovPassRain=function(b,Q){window.__rainLog.push({pass:Q.pass,x:b.x,y:b.y});return sr.apply(this,arguments);};
          Audio.SFX.retinaLockBeep=function(){window.__beeps++;};l23FovWarm();
        }""")
        for _ in range(180):
            ready=page.evaluate("()=>['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_green_danger','bmfx_alert_yellow_danger','bmfx_alert_red_danger','ovbody_intact'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Overlord, warning and projectile plates decode before the frenzy')
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){updateOverlordX(boss,1/60);stateT+=1/60;}}",n)
        def wait_for(expr,limit=500):
            for _ in range(limit):
                if page.evaluate(expr):return True
                step(1)
            return False
        def capture(name):
            page.evaluate("()=>{shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({state:boss._ovState,pass:boss._chargeTell?boss._chargeTell.pass:(boss._chg&&boss._chg.pass),dir:boss._chargeTell?boss._chargeTell.dir:(boss._chg&&boss._chg.dir),lane:boss._chargeTell?boss._chargeTell.baseLane:(boss._chg&&boss._chg.lane),x:boss.x,y:boss.y,pivot:boss._pivot,bullets:eBullets.length,beeps:window.__beeps,rains:window.__rainLog.slice()})")
        step(60);w1=capture('overlord_pass_1_warning_top')
        wait_for("()=>boss._ovState==='chargeOff'&&boss._chg.pass===0");step(22);p1=capture('overlord_pass_1_down')
        wait_for("()=>boss._ovState==='chargeTell'&&boss._chargeTell.pass===1");step(60);w2=capture('overlord_pass_2_warning_bottom')
        wait_for("()=>boss._ovState==='chargeOff'&&boss._chg.pass===1");step(26);p2=capture('overlord_pass_2_up_bullet_rain')
        page.evaluate("()=>{eBullets=[];player.x=380;}")
        wait_for("()=>boss._ovState==='chargeOff'&&boss._chg.pass===2");step(22);p3=capture('overlord_pass_3_down')
        wait_for("()=>boss._ovState==='chargeOff'&&boss._chg.pass===3");step(26);p4=capture('overlord_pass_4_up_bullet_rain')
        finished=wait_for("()=>boss._ovState==='reentry'&&!boss._ovPassSeq")
        final=page.evaluate("()=>({state:boss._ovState,beeps:window.__beeps,rains:window.__rainLog.slice(),used:boss._ovPassUsed})")
        rows=[w1,p1,w2,p2,p3,p4];passes=[p1,p2,p3,p4]
        ok([q['pass'] for q in passes]==[0,1,2,3],'four committed crossings run in exact order')
        ok([q['dir'] for q in passes]==[1,-1,1,-1],'crossings alternate down, up, down, up')
        ok(len(set(q['lane'] for q in passes))==4,'all four crossings use distinct player-sampled lane bands')
        ok(final['beeps']==32,'each crossing receives its complete eight-beat warning')
        ok(len(final['rains'])>4 and set(q['pass'] for q in final['rains'])=={1,3},'only passes two and four rain machine bullets downfield')
        ok(p2['bullets']>0 and p4['bullets']>0,'authored machine rounds are visible during both bullet-rain passes')
        ok(finished and final['state']=='reentry' and final['used'],'the bounded frenzy exits into the existing curved return')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'w1':w1,'p1':p1,'w2':w2,'p2':p2,'p3':p3,'p4':p4,'final':final},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
