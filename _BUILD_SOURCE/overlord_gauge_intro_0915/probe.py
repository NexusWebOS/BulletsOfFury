"""Real Chromium proof for the Jungle Overlord-X boss gauge entrance."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'overlord_gauge_intro_0915';OUT.mkdir(parents=True,exist_ok=True)
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
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
        fight=page.evaluate("()=>window.__fight(1,'boss','yuri')");ok(fight.get('ok'),'native Stage-1 boss route opens in Chromium')
        page.evaluate("""()=>{
          stagePlan=[];enemies=[];eBullets=[];pBullets=[];particles=[];story=null;dlgBox=function(){};playerHit=function(){};
          window.__ovIntroProbe={music:[],blips:0,selects:0,bars:[]};
          const sm=Audio.startMusic;Audio.startMusic=function(k){window.__ovIntroProbe.music.push(k);};window.__ovIntroProbe.restoreMusic=sm;
          Audio.stopMusic=function(){};Audio.SFX.blip=function(){window.__ovIntroProbe.blips++;};Audio.SFX.select=function(){window.__ovIntroProbe.selects++;};
          const hb=drawHealthBarV2;drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld){
            if(kind==='boss')window.__ovIntroProbe.bars.push({frac:bossHealthFraction(boss),alpha:bossHealthAlpha(boss)});
            return hb.apply(this,arguments);
          };
          run.stage=1;curStage=STAGES[0];boss=null;bossActive=false;bossWarned=true;warnT=0;spawnBoss('damkeeper');
          boss.x=240;player.x=240;player.y=430;state=GS.PLAY;stateT=1;
          bossBarWarm(1);['ovbody_intact','ovrotor_00'].forEach(k=>XART.rdy(k));
        }""")
        for _ in range(180):
            ready=page.evaluate("()=>['ovbody_intact','ovrotor_00','bmbar_frame_boss','bmbar_fill_grey','bmbar_fill_seg'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'Overlord hull, rotor and authored boss gauge decode')
        def step(n):
            page.evaluate("n=>{for(let i=0;i<n;i++){updateBoss(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{window.__ovIntroProbe.bars=[];shake=0;drawWorld(0);}")
            png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>JSON.parse(JSON.stringify({intro:boss._ovIntro,enter:boss.enter,noHit:boss._noHit,bars:window.__ovIntroProbe.bars,music:window.__ovIntroProbe.music,blips:window.__ovIntroProbe.blips,selects:window.__ovIntroProbe.selects,y:boss.y}))")
        step(42);approach=capture('overlord_approach_no_gauge')
        step(62);fade=capture('overlord_gauge_fade')
        step(48);fill1=capture('overlord_gauge_fill_early')
        step(56);fill2=capture('overlord_gauge_fill_late')
        step(22);ready_shot=capture('overlord_gauge_full')
        step(20);fight_shot=capture('overlord_fight_music_start')
        ok(approach['intro']['phase']=='approach' and not approach['bars'],'approach keeps the boss gauge hidden')
        ok(fade['intro']['phase']=='fade' and fade['bars'] and 0<fade['bars'][0]['alpha']<1 and fade['bars'][0]['frac']==0,'authored gauge fades in empty')
        ok(fill1['intro']['phase']=='fill' and 0<fill1['bars'][0]['frac']<fill2['bars'][0]['frac']<1,'boss gauge fills left-to-right over time')
        ok(ready_shot['bars'] and ready_shot['bars'][0]['frac']==1 and ready_shot['music']==[],'full gauge completes before fight music begins')
        ok(fight_shot['intro']['done'] and not fight_shot['enter'] and not fight_shot['noHit'] and fight_shot['music']==['boss1'],'fight and Stage-1 boss music begin together after the gauge')
        ok(fight_shot['blips']==8 and fight_shot['selects']==1,'eight menu-chime beats and one completion chord sound during the fill')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass'] for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
