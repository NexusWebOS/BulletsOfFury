"""Native Chromium verification for the completed Retina component-router audit."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/retina_audit_0915';OUT.mkdir(parents=True,exist_ok=True)
PREP="""stage=>{run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.stage=stage;curStage=STAGES[stage-1];beginStage(stage);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;playerHit=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];pImpacts=[];playerLocks=[];special=null;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);Snd.loopStopAll();window.__auto=function(){};}"""

def main():
    checks=[];errors=[];details={}
    def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    with sync_playwright() as p:
        browser=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)))
        page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
        page.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
        page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
        page.evaluate("""()=>{window.__retinaBlits=0;const base=retinaTinted;retinaTinted=function(){const im=base.apply(this,arguments);if(im)window.__retinaBlits++;return im;};}""")
        def step(n):
            for i in range(0,n,30):page.evaluate('n=>window.__step(n)',min(30,n-i));page.wait_for_timeout(10)
        def prep(stage):page.evaluate(PREP,stage);step(2)
        def fight(stage,role):
            page.evaluate('a=>window.__fight(a[0],a[1],"yuri")',[stage,role]);page.evaluate('()=>{stagePlan=[];enemies=[];story=null;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);playerHit=function(){};player.invuln=0;}')
            for _ in range(90):
                if page.evaluate('()=>{const t=window.__tgt();return t&&!t.enter&&t.y>0;}'):break
                step(6)
            step(4)
        def shot(name):
            page.evaluate('()=>{shake=0;drawWorld(0);drawHUD();}')
            data=page.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")
            (OUT/(name+'.png')).write_bytes(base64.b64decode(data))

        fight(2,'boss')
        ok(page.evaluate('()=>!!(boss&&boss._furnace)'),'native Stage-2 boss uses the authored Furnace Tyrant component encounter')
        page.evaluate("""()=>{furnaceSync(boss);if(boss._mwBarrier)boss._mwBarrier.active=false;furnaceEnter(boss,'arms');boss._fz.trans=0;boss._fz.t=0;boss._fz.at=0;boss.x=worldWidth()/2;boss.y=150;bossActive=true;run.bombs=8;retina={target:null};eBullets=[];}""")
        ok(page.evaluate("()=>{const t=_lockTargets();return t.length===2&&t.every(q=>/^furnace /.test(q.kind))&&t.indexOf(boss)<0;}"),'live Furnace arms replace its hull in the shared lock list')
        page.keyboard.press('c');step(30)
        ok(page.evaluate("()=>retina.phase==='locked'&&retina.target&&/^furnace /.test(retina.target.kind)"),'an actual Retina key tap locks a live Furnace arm')
        shot('furnace_arm_retina')
        ok(page.evaluate('()=>window.__retinaBlits>0'),'the game canvas draws the authored Retina animation on that moving arm')
        page.evaluate('()=>{window.__picked=retina.target;window.__part=retina.target._retinaId;window.__hp=boss._fz.pools[window.__part];window.__other=window.__part==="left"?boss._fz.pools.right:boss._fz.pools.left;}')
        page.keyboard.down('c');page.keyboard.down('k');step(1);page.keyboard.up('k');page.keyboard.up('c')
        ok(page.evaluate('()=>pBullets.some(b=>b.tgt===window.__picked)'),'actual missile input launches toward the selected component wrapper')
        page.evaluate('()=>{const b=pBullets.find(q=>q.tgt===window.__picked);if(b){b.x=window.__picked.x;b.y=window.__picked.y;b.spd=1;}}');step(3)
        ok(page.evaluate('()=>boss._fz.pools[window.__part]<window.__hp'),'the launched missile reaches the existing Furnace part-damage router')
        ok(page.evaluate('()=>{const now=window.__part==="left"?boss._fz.pools.right:boss._fz.pools.left;return now===window.__other;}'),'the opposite Furnace arm does not take the selected missile damage')
        page.evaluate('()=>{boss._mwBarrier.active=true;retina={target:boss,phase:"locked",lockT:5};updateRetina(.01);}')
        ok(page.evaluate('()=>!retina.target&&!retina.phase&&_lockTargets().length===0'),'the Furnace shield immediately removes protected hull and part locks')

        page.evaluate("""()=>{furnaceEnter(boss,'core');boss._fz.trans=0;boss.x=player.x;boss.y=330;boss._mwBarrier.active=false;
          _seat=1;run.weapon=4;run.wlevel=5;run.wlevels[4]=5;run.wvars[4]='flamethrower';player.fireCd=0;special=null;
          pBullets=[];floaters=[];stageTimer=20;window.__fireHp=boss._fz.pools.body;}""")
        box=page.locator('#screen').bounding_box();page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.72);page.mouse.down();step(10);page.mouse.up()
        details['fireInput']=page.evaluate("()=>({state:state,play:GS.PLAY,seat:_seat,bind:keybindFor(_seat).fire,dead:player.dead,cd:player.fireCd,weapon:run.weapon,down:Input.down('j'),bullets:pBullets.map(b=>b.kind),texts:floaters.map(f=>f.txt),hp:boss._fz.pools.body,before:window.__fireHp})")
        print(json.dumps(details['fireInput']),flush=True)
        ok(page.evaluate("()=>pBullets.some(b=>b.kind==='flame'&&b._el==='fire')"),'actual fire input creates the player flamethrower with fire identity')
        ok(page.evaluate("()=>floaters.some(f=>f.txt==='FIRE DMG ABSORBED!')"),'same-element fire contact creates the requested absorbed-damage text')
        ok(page.evaluate('()=>boss._fz.pools.body<window.__fireHp'),'the Furnace still takes the retained half-damage through its body router')
        shot('furnace_fire_absorbed')

        prep(3)
        page.evaluate("""()=>{const e=spawnEnemy('s3tank',player.x,330,{vy:0});e.hp=e._maxhp=1000;e._stagger=100;
          eBullets=[];pBullets=[];floaters=[];run.weapon=4;run.wlevel=5;run.wlevels[4]=5;run.wvars[4]='flamethrower';
          player.fireCd=0;window.__iceTarget=e;window.__iceHp=e.hp;
          const r=elementalDamageResult(e,'enemy',{kind:'flame',_el:'fire'},10,e.x,e.y);window.__weakExact=r.dmg;}""")
        page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.72);page.mouse.down();step(10);page.mouse.up()
        ok(page.evaluate('()=>window.__weakExact===20'),'the live browser resolves generic fire-on-ice damage at exactly 2x')
        ok(page.evaluate("()=>pBullets.some(b=>b.kind==='flame'&&b._el==='fire')&&window.__iceTarget.hp<window.__iceHp"),'actual primary-fire input damages an authored Stage-3 ice unit')
        ok(page.evaluate("()=>window.__iceTarget._hitFlashColor==='#ff3b30'"),'the opposing-element contact selects the authored red hit response')
        page.evaluate('()=>{pBullets=[];window.__iceTarget.flash=.16;}')
        shot('stage3_fire_weakness')

        details['layouts']=page.evaluate("""()=>{
          const old={boss,subBoss,bossActive,subBossActive,enemies};const out={};enemies=[];
          try{
            boss=null;bossActive=false;subBossActive=true;
            subBoss={x:240,y:150,w:196,h:180,hp:300,maxhp:300,dead:false,enter:false,_ql:true,_qlHullOpen:false,_qlCan:[{id:'L',hb:[60,90,40,55],hp:30,dead:false},{id:'R',hb:[284,90,40,55],hp:30,dead:false}]};out.quad=_lockTargets().map(t=>t.kind);
            subBoss={x:240,y:150,w:130,h:125,hp:400,maxhp:400,dead:false,enter:false,_rzb:{state:'guns',trans:0,a:0,pools:{left:40,right:40,turret:100,hull:100},flash:{}}};out.razor=_lockTargets().map(t=>t.kind);
            subBoss={x:240,y:150,w:77,h:84,hp:200,maxhp:200,dead:false,enter:false,_tlv:{vuln:true,phase:'chase',ap:[0,1,2,3].map(()=>({hp:10,max:10}))}};out.tempest=_lockTargets().map(t=>t.kind);
            subBoss=null;subBossActive=false;bossActive=true;boss={x:240,y:160,w:300,h:230,hp:800,maxhp:800,dead:false,enter:false,_s7warden:{noHit:false,final:{phase:'stun',cores:[{side:-1,hp:30,dead:false},{side:1,hp:30,dead:false}]}}};out.warden=_lockTargets().map(t=>t.kind);
            return out;
          }finally{boss=old.boss;subBoss=old.subBoss;bossActive=old.bossActive;subBossActive=old.subBossActive;enemies=old.enemies;}
        }""")
        ok(details['layouts']['quad']==['laser turret','laser turret'],'quad-laser hull is replaced by its two live turret locks')
        ok(details['layouts']['razor']==['razorback left','razorback right'],'Razorback exposes only its current destructible gun phase')
        ok(len(details['layouts']['tempest'])==5 and details['layouts']['tempest'].count('aperture')==4,'Tempest exposes four apertures and its hittable hull separately')
        ok(details['layouts']['warden']==['toxic core','toxic core'],'the Warden stun window exposes both toxic canisters and no false hull target')
        details['controlledError']=page.evaluate('()=>window.__err||null')
        ok(not errors and not details['controlledError'],'zero Chromium page, console or controlled-loop errors')
        browser.close()
    srv.shutdown()
    result={'checks':checks,'errors':errors,'details':details}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
