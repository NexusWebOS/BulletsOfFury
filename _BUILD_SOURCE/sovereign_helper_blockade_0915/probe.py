"""Real Chromium proof for the Sovereign Hard/Furious helper blockade."""
import base64, json, sys, threading, http.server
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_shots'/'sovereign_helper_blockade_0915'
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
        checks.append({'pass':bool(value),'label':label});print(('ok  ' if value else 'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)))
        page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000)
        page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
        fight=page.evaluate("()=>window.__fight(4,'boss','yuri')")
        ok(fight.get('ok'),'native Stage-4 boss route opens in Chromium')
        page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};warnT=0;warnKind=null;stagePlan=[];waveIdx=0;
          enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];state=GS.PLAY;stateT=1;run.stage=4;curStage=STAGES[3];
          player.x=280;player.y=650;player.invuln=1e9;player.dead=false;window.__s4Gets=[];
          const old=XART.get.bind(XART);XART.get=function(k){window.__s4Gets.push(k);return old(k);};
          for(const k of ['s4w_boss_energized_0','s4w_helper_dual_0','s4w_final_chaingun_0','s4w_lightning_shield_0','s4w_power_node_0'])XART.rdy(k);
        }""")
        for _ in range(240):
            ready=page.evaluate("()=>['s4w_boss_energized_0','s4w_helper_dual_0','s4w_final_chaingun_0','s4w_lightning_shield_0','s4w_power_node_0'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Sovereign, helper, rotary barrel, shield and node art decode before capture')

        def setup(level):
            return page.evaluate("""k=>{diffKey=k;DIFF=DIFFS[k];boss=null;bossActive=false;eBullets=[];pBullets=[];spawnBoss('stormsovereign');
              boss.enter=false;boss.x=worldWidth()/2;boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss.fireCd=999;bossActive=true;
              stage4CoreTurretSpawnMissing(boss,.5);for(const t of boss._s4war.coreTurrets){t.spawnT=1;t.materialize=1;}
              return {shields:boss._s4war.coreTurrets.map(t=>t.maxShield)};}""",level)
        def step(n):
            page.evaluate("n=>{for(let i=0;i<n;i++)stage4CoreTurretTick(boss,1/60,2);}",n)
        def capture(name):
            page.evaluate("()=>{shake=0;window.__s4Gets=[];drawWorld(0);}")
            detail=page.evaluate("""()=>({mode:boss._s4war.coreFormationMode,mix:boss._s4war.coreFormationMix,anchor:boss._s4war.coreFormationAnchor,
              gets:Array.from(new Set(window.__s4Gets)),turrets:boss._s4war.coreTurrets.map(t=>({side:t.side,x:t.x,y:t.y,shield:t.shield,maxShield:t.maxShield,state:t.state,ang:t.ang})),
              shotCount:eBullets.filter(q=>q._s4CoreSide).length})""")
            raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            path=OUT/f'{name}.png';path.write_bytes(base64.b64decode(raw));shots.append(path);return detail
        def fire_sample(level):
            setup(level)
            return page.evaluate("""()=>{eBullets=[];for(const t of boss._s4war.coreTurrets){t.state='fire';t.stateT=0;t.fireShot=0;t.mode='down';t.aimTo=t.ang=Math.PI/2;}
              stage4CoreTurretTick(boss,.40,2);const a=eBullets.filter(q=>q._s4CoreSide);return {count:a.length,speed:a.length?Math.hypot(a[0].vx,a[0].vy):0};}""")

        normal_setup=setup('normal');step(210);normal=capture('sovereign_helpers_01_normal_home')
        ok(normal_setup['shields']==[102,102],'Normal helpers keep the existing shield pool')
        ok(normal['mode']=='home' and normal['mix']==0 and all(t['y']<=109 for t in normal['turrets']),'Normal helpers never enter the difficulty blockade row')

        hard_setup=setup('hard');step(210);hard=capture('sovereign_helpers_02_hard_blockade')
        left,right=hard['turrets']
        ok(hard_setup['shields']==[153,153],'Hard gives both helper shields exactly 50 percent more capacity')
        ok(hard['mode']=='hold' and hard['mix']>.99,'Hard completes a timed forward advance and holds the row')
        ok(left['y']>285 and right['y']>285 and abs(left['y']-right['y'])<2,'both helpers form one forward horizontal line')
        ok(105<right['x']-left['x']<128 and abs((left['x']+right['x'])/2-280)<6,'the paired row anchors on the player with a traversable center spacing')
        ok(any(k.startswith('s4w_helper_dual_') for k in hard['gets']) and any(k.startswith('s4w_final_chaingun_') for k in hard['gets']),'the live draw uses authored helper hulls and rotating barrel frames')
        page.evaluate("()=>{player.x=520;}");step(45);tracked=capture('sovereign_helpers_03_hard_tracking')
        track_center=sum(t['x'] for t in tracked['turrets'])/2
        ok(abs(track_center-tracked['anchor'])<8 and tracked['anchor']-hard['anchor']>150,'the blocking row follows the player horizontally during its hold and respects the edge lane')

        normal_fire=fire_sample('normal');hard_fire=fire_sample('hard');furious_fire=fire_sample('furious')
        ok(hard_fire['count']>normal_fire['count'] and furious_fire['count']>hard_fire['count'],'Hard and Furious progressively accelerate the straight rotary stream')
        ok(hard_fire['speed']>normal_fire['speed'] and furious_fire['speed']>hard_fire['speed'],'Hard and Furious helper rounds travel progressively faster')
        furious_setup=page.evaluate("()=>({shields:boss._s4war.coreTurrets.map(t=>t.maxShield),spec:stage4CoreDifficulty()})")
        ok(furious_setup['shields']==[153,153] and furious_setup['spec']['furious'],'Furious inherits the reinforced shields and its faster difficulty profile')
        for path in shots:
            image=Image.open(path).convert('RGB');ok(image.size==(960,1024) and image.getbbox() is not None,f'{path.stem} is a non-empty native gameplay frame')
        ok(not errors,'zero Chromium page or console errors')
        browser.close()
    server.shutdown()
    result={'checks':checks,'errors':errors,'fight':fight,'normalSetup':normal_setup,'normal':normal,'hardSetup':hard_setup,'hard':hard,
      'tracked':tracked,'normalFire':normal_fire,'hardFire':hard_fire,'furiousFire':furious_fire,'furiousSetup':furious_setup,
      'shots':[str(p.relative_to(ROOT)) for p in shots]}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)

if __name__=='__main__':main()
