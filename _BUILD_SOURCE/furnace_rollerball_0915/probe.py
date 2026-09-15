"""Real Chromium proof for the Furnace Tyrant's accelerating rollerball core attack."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'furnace_rollerball_0915';OUT.mkdir(parents=True,exist_ok=True)
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
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(2,'boss','yuri')");ok(fight.get('ok'),'native Stage-2 boss route opens in Chromium')
        page.evaluate("""()=>{
          stagePlan=[];enemies=[];eBullets=[];pBullets=[];particles=[];story=null;dlgBox=function(){};
          run.stage=2;curStage=STAGES[1];player.x=130;player.y=378;player.invuln=1e9;boss=null;bossActive=false;bossWarned=true;warnT=0;
          spawnBoss('infernoreaver');furnaceSync(boss);const F=boss._fz;F.phase='core';F.trans=0;F.attack='rollerball';F.idx=2;F.at=0;
          F.startX=boss.x;F.rollY=null;F.rollLeg=-1;boss.enter=false;boss.dead=false;state=GS.PLAY;stateT=1;
          window.__roll={min:9999,max:-9999,peak:[0,0,0,0,0,0],spin:[0,0,0,0,0,0],lastX:boss.x,lastA:F.a,locked:null};
          for(const k of ['fzt_body_rotor','fzt_head_intact','mwfx_flame_shield_0','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'])XART.rdy(k);
        }""")
        for _ in range(180):
            ready=page.evaluate("()=>['fzt_body_rotor','fzt_head_intact','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Furnace core and shared warning plates decode before the attack')
        def step(n):page.evaluate("""n=>{for(let i=0;i<n;i++){const R=window.__roll,F=boss._fz;furnaceTick(boss,1/60);stateT+=1/60;
          if(R.locked==null&&F.rollY!=null)R.locked=F.rollY;R.min=Math.min(R.min,boss.x);R.max=Math.max(R.max,boss.x);
          if(F.rollLive&&F.rollLeg>=0){R.peak[F.rollLeg]=Math.max(R.peak[F.rollLeg],Math.abs(boss.x-R.lastX)*60);R.spin[F.rollLeg]=Math.max(R.spin[F.rollLeg],Math.abs(F.a-R.lastA)*60);}R.lastX=boss.x;R.lastA=F.a;}}""",n)
        def wait_for(expr,limit=900):
            for _ in range(limit):
                if page.evaluate(expr):return True
                step(1)
            return False
        def capture(name):
            page.evaluate("()=>{shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({attack:boss._fz.attack,t:boss._fz.at,leg:boss._fz.rollLeg,live:boss._fz.rollLive,x:boss.x,y:boss.y,a:boss._fz.a,tells:boss._fz.tells.length,locked:window.__roll.locked})")
        step(55);warning=capture('furnace_rollerball_warning')
        wait_for("()=>boss._fz.rollLive&&boss._fz.rollLeg===0");step(35);slow=capture('furnace_rollerball_slow')
        wait_for("()=>boss._fz.rollLive&&boss._fz.rollLeg===2");step(24);fast=capture('furnace_rollerball_fast')
        wait_for("()=>boss._fz.rollLive&&boss._fz.rollLeg===5");step(14);superfast=capture('furnace_rollerball_superfast')
        finished=wait_for("()=>boss._fz.attack==='rotor'")
        final=page.evaluate("()=>({attack:boss._fz.attack,a:boss._fz.a,stats:window.__roll})")
        ok(warning['tells']>0 and not warning['live'],'the lane telegraph is visible before contact becomes dangerous')
        ok(abs(warning['locked']-378)<1,'the rollerball commits to the sampled player lane')
        ok([slow['leg'],fast['leg'],superfast['leg']]==[0,2,5],'captured slow, fast and super-fast crossings from the live sequence')
        ok(final['stats']['peak'][5]>final['stats']['peak'][0]*2.4,'horizontal travel speed more than doubles across the sequence')
        ok(final['stats']['spin'][5]>final['stats']['spin'][0]*2,'rotation visibly accelerates with travel')
        ok(final['stats']['min']<120 and final['stats']['max']>360,'the authored whole boss crosses nearly the full playfield')
        ok(finished and final['attack']=='rotor' and abs(final['a'])<.001,'the bounded set piece restores the normal core rotation')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'warning':warning,'slow':slow,'fast':fast,'superfast':superfast,'final':final},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
