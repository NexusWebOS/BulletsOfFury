"""Real Chromium proof for the Olive Warden Hard/Furious assault cycle."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'olive_warden_hard_assault_0915'
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'))
import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks,errors,shots=[],[],[]
    def ok(value,label):
        checks.append({'pass':bool(value),'label':label})
        print(('ok  ' if value else 'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)))
        page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000)
        page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF)
        page.evaluate(capture3.LIB)
        fight=page.evaluate("()=>window.__fight(4,'mini','yuri')")
        ok(fight.get('ok'),'native Stage-4 miniboss route opens in Chromium')
        page.evaluate("""()=>{
          __auto=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];story=null;dlgBox=function(){};
          run.stage=4;curStage=STAGES[3];diffKey='hard';DIFF=DIFFS.hard;player.x=worldWidth()*.5;player.y=650;
          player.invuln=1e9;player.dead=false;player.roll=null;player.somer=null;boss=null;bossActive=false;
          subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=true;bossTriggered=false;state=GS.PLAY;stateT=1;
          spawnSubBoss('olivewarden');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=subBoss._s4war.homeY;
          subBoss._drawY=subBoss.y;subBoss.fireCd=999;subBoss._act=null;subBoss._actQ=[];subBossActive=true;
          window.__wardenGets=[];const get0=XART.get.bind(XART);XART.get=function(k){window.__wardenGets.push(k);return get0(k);};
          for(const k of ['nsb_olivewarden_intact','mgcf_1_5','bpfx_proj_missile_0','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_green_danger','bmfx_alert_yellow_danger','bmfx_alert_red_danger'])XART.rdy(k);
        }""")
        for _ in range(240):
            ready=page.evaluate("()=>['nsb_olivewarden_intact','mgcf_1_5','bpfx_proj_missile_0','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'].every(k=>XART.rdy(k))")
            if ready: break
            page.wait_for_timeout(35)
        ok(ready,'authored Warden hull, ammunition and three-color warning art decode before capture')

        def step(n):
            page.evaluate("n=>{for(let i=0;i<n;i++){subBoss.fireCd=999;updatePlay(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{shake=0;warnT=0;warnKind=null;window.__wardenGets=[];drawWorld(0);}")
            data=page.evaluate("()=>({mode:subBoss._s4war.mode,x:subBoss.x,y:subBoss.y,scale:subBoss._s4war.scale,safe:!!subBoss._s4MiniSafe,gets:window.__wardenGets.slice(),bullets:eBullets.filter(q=>q._s4Mini).map(q=>({kind:q._s4wKind,slot:q._s4Slot,x:q.x,y:q.y,w:q.w,h:q.h}))})")
            png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path=OUT/f'{name}.png';path.write_bytes(base64.b64decode(png));shots.append(path)
            return data
        def set_mode(mode):
            page.evaluate("mode=>{eBullets=[];stage4WarfareSetMode(subBoss,mode);subBoss._s4war.poseRot=0;subBoss._drawY=subBoss.y;}",mode)

        set_mode('burst');step(12);burst=capture('warden_01_rapid_spread')
        spread_slots={q['slot'] for q in burst['bullets'] if q['kind']=='machine'}
        ok({'L','R'}.issubset(spread_slots),'rapid spread fire leaves both authored side turrets')
        set_mode('center');step(9);center=capture('warden_02_center_flurry')
        center_slots={q['slot'] for q in center['bullets'] if q['kind']=='machine'}
        ok({'CL','CR'}.issubset(center_slots),'the middle section fires a dual straight machine-gun flurry')

        page.evaluate("()=>{eBullets=[];stage4MiniHardSet(subBoss,'hardCircle');}")
        start=page.evaluate("()=>({x:subBoss.x,y:subBoss.y})")
        step(28);circle=capture('warden_03_circular_assault')
        ok(circle['mode']=='hardCircle' and abs(circle['x']-start['x'])>10,'Hard mode performs a visible circular assault without a position snap')
        ok(any(q['kind']=='machine' for q in circle['bullets']),'the circular assault keeps firing mounted machine rounds')

        for _ in range(120):
            if page.evaluate("()=>subBoss._s4war.mode==='hardGlide'"): break
            step(1)
        step(18);glide=capture('warden_04_glide_flurry')
        ok(glide['mode']=='hardGlide','the orbit flows into the horizontal glide state')
        ok({'CL','CR'}.issubset({q['slot'] for q in glide['bullets'] if q['kind']=='machine'}),'the glide uses both center gun hardpoints')

        page.evaluate("()=>{eBullets=[];player.x=430;stage4MiniHardSet(subBoss,'hardWarn');subBoss._s4war.t=.18;stage4MiniHardTick(subBoss,0,shipBossPhase(subBoss));}")
        green=capture('warden_05_warning_green')
        page.evaluate("()=>{subBoss._s4war.t=.52;stage4MiniHardTick(subBoss,0,shipBossPhase(subBoss));}")
        yellow=capture('warden_06_warning_yellow')
        page.evaluate("()=>{subBoss._s4war.t=.95;stage4MiniHardTick(subBoss,0,shipBossPhase(subBoss));}")
        red=capture('warden_07_warning_red')
        ok('bmfx_fov_green_tall' in green['gets'],'the charge lane begins with the shared green FOV')
        ok('bmfx_fov_yellow_tall' in yellow['gets'],'the same charge lane advances to yellow')
        ok('bmfx_fov_red_tall' in red['gets'],'the final committed dodge window visibly flashes red')
        locked=page.evaluate("()=>({lane:subBoss._s4war.miniHard.lane,locked:subBoss._s4war.miniHard.locked,x:subBoss.x})")
        page.evaluate("()=>{player.x=90;subBoss._s4war.t=1.08;stage4MiniHardTick(subBoss,0,shipBossPhase(subBoss));}")
        locked_after=page.evaluate("()=>({lane:subBoss._s4war.miniHard.lane,locked:subBoss._s4war.miniHard.locked,x:subBoss.x})")
        ok(locked['locked'] and locked_after['locked'] and abs(locked_after['lane']-locked['lane'])<.001,'the Warden turns the tracked warning into a committed dodge lane')

        page.evaluate("()=>{subBoss._s4war.t=1.21;stage4MiniHardTick(subBoss,0,shipBossPhase(subBoss));}")
        step(9);ram=capture('warden_08_committed_ram')
        ok(ram['mode']=='hardRam' and not ram['safe'] and ram['y']>subBoss_home(page),'the whole upright Warden commits south through the player lane')

        collision=page.evaluate("""()=>{const hit0=playerHit;window.__wardenHits=0;playerHit=function(){window.__wardenHits++;};
          eBullets=[];special=null;run.shield=0;player.x=subBoss.x;player.y=450;player.invuln=0;player.dead=false;subBoss._s4war.mode='hardRam';subBoss._s4war.miniHard.speed=0;
          subBoss.y=player.y;subBoss._drawY=subBoss.y;subBoss._s4MiniSafe=false;const pre={active:subBossActive,dead:subBoss.dead,enter:subBoss.enter,safe:subBoss._s4MiniSafe,px:player.x,py:player.y,pinv:player.invuln,pdead:player.dead,bx:subBoss.x,by:subBoss.y,dy:subBoss._drawY,seats:seatList().length};updatePlay(1/60);const ramHits=window.__wardenHits;
          subBoss.x=player.x;subBoss.y=player.y;subBoss._drawY=subBoss.y;stage4MiniHardSet(subBoss,'hardReturn');
          updatePlay(1/60);const total=window.__wardenHits,safe=!!subBoss._s4MiniSafe;playerHit=hit0;
          return {ramHits:ramHits,returnHits:total-ramHits,safe:safe,mode:subBoss._s4war.mode,pre:pre,after:{px:player.x,py:player.y,pinv:player.invuln,pdead:player.dead,bx:subBoss.x,by:subBoss.y,dy:subBoss._drawY}};}""")
        ok(collision['ramHits']==1,'the active body ram reaches the real player-hit boundary')
        ok(collision['returnHits']==0 and collision['safe'] and collision['mode']=='hardReturn','the off-screen curved return cannot deal a hidden collision')
        page.evaluate("()=>{player.x=worldWidth()/2;player.y=650;player.invuln=1e9;subBoss.x=430;subBoss.y=VH+subBoss.h*.72;subBoss._drawY=subBoss.y;stage4MiniHardSet(subBoss,'hardReturn');}")
        step(30)
        ret=capture('warden_09_safe_curved_return')

        isolation=page.evaluate("""()=>{function runOne(k){diffKey=k;DIFF=DIFFS[k];subBoss=null;subBossActive=false;spawnSubBoss('olivewarden');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=subBoss._s4war.homeY;subBoss._drawY=subBoss.y;subBossActive=true;const S=subBoss._s4war;stage4WarfareSetMode(subBoss,'rockets');S.t=3.11;stage4MiniDirector(subBoss,1/60);return {mode:S.mode,ram:S.miniRamCount,hard:!!S.miniHard};}return {normal:runOne('normal'),hard:runOne('hard'),furious:runOne('furious')};}""")
        ok(isolation['normal']['mode']=='burst' and not isolation['normal']['hard'],'Normal retains the established three-pattern Warden cycle')
        ok(isolation['hard']['mode']=='hardCircle' and isolation['furious']['mode']=='hardCircle','Hard and Furious both inherit the new assault cycle')
        pose=page.evaluate("()=>{diffKey='hard';DIFF=DIFFS.hard;return shipBossVisualPose(subBoss);}")
        ok(abs(pose['rot'])<1e-9,'the authored whole boss plate remains upright through the new movement')
        for path in shots:
            image=Image.open(path).convert('RGB')
            ok(image.size==(960,1024) and image.getbbox() is not None,f'{path.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown()
    result={'checks':checks,'errors':errors,'details':{'fight':fight,'burst':burst,'center':center,'circle':circle,'glide':glide,'green':green,'yellow':yellow,'red':red,'locked':locked,'lockedAfter':locked_after,'ram':ram,'collision':collision,'return':ret,'isolation':isolation,'pose':pose},'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks)
    print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks): raise SystemExit(1)

def subBoss_home(page):
    return page.evaluate("()=>subBoss._s4war.homeY")

if __name__=='__main__': main()
