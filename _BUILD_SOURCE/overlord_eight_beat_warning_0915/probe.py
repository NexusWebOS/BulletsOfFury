"""Real Chromium proof for Overlord-X's eight-beat red pass warning."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'overlord_eight_beat_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
          run.stage=1;curStage=STAGES[0];player.x=240;player.y=430;boss=null;bossActive=false;bossWarned=true;warnT=0;spawnBoss('damkeeper');
          boss._ovIntro.done=true;boss.enter=false;boss._noHit=false;boss._ovInit=1;state=GS.PLAY;stateT=1;
          boss.x=240;boss.y=112;boss._drawY=112;boss._ovState='fight';boss._ovChargeCd=999;boss.fireCd=999;boss.hp=boss.maxhp;
          window.__ovBeats=[];window.__ovDraw=[];window.__ovClock=0;
          Audio.SFX.retinaLockBeep=function(){window.__ovBeats.push({n:boss._chargeTell?boss._chargeTell.beat:-9,t:window.__ovClock});};
          const f=combatWarningDraw;combatWarningDraw=function(b,q){const r=f.apply(this,arguments);window.__ovDraw.push({phase:l23FovPhase(q.progress),p:q.progress,field:!!q.fieldOnly,alert:!!q.alertOnly});return r;};
          l23FovWarm();ovStartChargeTell(boss);
        }""")
        for _ in range(180):
            ready=page.evaluate("()=>['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_green_danger','bmfx_alert_yellow_danger','bmfx_alert_red_danger','ovbody_intact'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'all authored FOV, alert and Overlord plates decode before the warning')
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){window.__ovClock+=1/60;updateOverlordX(boss,1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{window.__ovDraw=[];shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({state:boss._ovState,t:boss._chargeTell&&boss._chargeTell.t,beat:boss._chargeTell&&boss._chargeTell.beat,flash:boss._chargeTell&&boss._chargeTell.flash,locked:boss._chargeTell&&boss._chargeTell.locked,lane:boss._chargeTell?boss._chargeTell.lane:(boss._chg&&boss._chg.lane),x:boss.x,y:boss.y,draw:window.__ovDraw.slice(),beeps:window.__ovBeats.slice(),vulnerable:!boss._noHit})")
        step(1);b1=capture('overlord_warning_beep_1')
        step(35);b4=capture('overlord_warning_beep_4')
        step(24);b6=capture('overlord_warning_beep_6_locked')
        lane=b6['lane'];page.evaluate("()=>{player.x=390;}")
        step(25);b8=capture('overlord_warning_beep_8_committed')
        step(12);dash=capture('overlord_warning_release')
        beats=dash['beeps'];gaps=[beats[i]['t']-beats[i-1]['t'] for i in range(1,len(beats))]
        def red(q):return q['flash']>0 and any(x['phase']=='red' and (x['field'] or x['alert']) for x in q['draw'])
        ok(len(beats)==8 and [x['n'] for x in beats]==list(range(8)),'the warning emits exactly eight ordered beats')
        ok(len(gaps)==7 and all(.16<g<.24 for g in gaps),'all eight existing Retina beeps stay at a readable 0.20-second cadence')
        ok(all(red(q) for q in [b1,b4,b6,b8]),'each sampled beep visibly forces the authored lane and alert red')
        ok(b1['vulnerable'] and b4['vulnerable'] and b6['vulnerable'] and b8['vulnerable'],'the complete warning remains a shooting window')
        ok(b6['locked'] and b8['locked'] and abs(b8['lane']-lane)<.01,'the player lane locks halfway through and cannot chase afterward')
        ok(dash['state']=='chargeOff' and abs(dash['x']-dash['lane'])<.01 and dash['y']>b8['y'],'the eighth beat releases a committed vertical charge')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'b1':b1,'b4':b4,'b6':b6,'b8':b8,'dash':dash},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
