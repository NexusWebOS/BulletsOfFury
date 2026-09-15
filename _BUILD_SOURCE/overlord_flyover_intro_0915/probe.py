"""Real Chromium proof for Overlord-X bottom flyover, full silhouette shadow and whip spin."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'overlord_flyover_intro_0915';OUT.mkdir(parents=True,exist_ok=True)
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
          run.stage=1;curStage=STAGES[0];player.x=118;player.y=430;boss=null;bossActive=false;bossWarned=true;warnT=0;spawnBoss('damkeeper');state=GS.PLAY;stateT=1;
          window.__fly={over:0};const od=overlordIntroOverflightDraw;overlordIntroOverflightDraw=function(){const q=od.apply(this,arguments);if(q)window.__fly.over++;return q;};
          Audio.startMusic=function(){};Audio.stopMusic=function(){};Audio.SFX.blip=function(){};Audio.SFX.select=function(){};
          ['ovbody_intact','ovrotor_00'].forEach(k=>XART.rdy(k));
        }""")
        for _ in range(180):
            ready=page.evaluate("()=>['ovbody_intact','ovrotor_00'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored helicopter body and rotor decode before the flyover')
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){updateBoss(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{window.__fly.over=0;shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({phase:boss._ovIntro.phase,x:boss.x,y:boss.y,pivot:boss._pivot||0,air:boss._ovAirborne,over:window.__fly.over,bar:bossHealthVisible(boss)})")
        below=capture('overlord_rising_from_bottom');step(30);cross=capture('overlord_shadow_over_player');step(42);whip0=capture('overlord_whip_start');step(8);whip=capture('overlord_whip_spin');step(22);settled=capture('overlord_whip_settled')
        ok(below['y']>512 and below['air'] and not below['bar'],'helicopter begins below the screen with its boss gauge hidden')
        ok(abs(cross['y']-430)<38 and cross['air'] and cross['over']==1,'the authored hull and its complete shadow cross above the player')
        ok(whip0['phase']=='whip' and not whip0['air'] and not whip0['bar'],'flyover settles into the dedicated whip phase before the gauge')
        ok(whip['phase']=='whip' and abs(whip['pivot'])>1.0,'quick whip visibly rotates the complete helicopter plate')
        ok(settled['phase']=='fade' and settled['bar'] and abs(settled['pivot'])<.01,'whip returns level before the empty gauge fades in')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
