"""Native Chromium checks and pixels for Mike's stage 1–5 corrections."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/missile_supplies_0914';OUT.mkdir(parents=True,exist_ok=True)
PREP="""stage=>{run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.stage=stage;curStage=STAGES[stage-1];beginStage(stage);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;playerHit=function(){};story=null;dlgBox=function(){};
stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];pImpacts=[];playerLocks=[];special=null;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);Snd.loopStopAll();window.__auto=function(){};}"""
def main():
    checks=[];errors=[];details={};shots=[]
    def ok(c,label):checks.append({'pass':bool(c),'label':label});print(('ok  'if c else'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    with sync_playwright()as p:
        b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
        pg.evaluate('''()=>{window.__blits=[];window.__artKey=null;const old=ctx.drawImage;ctx.drawImage=function(im){if(window.__artKey)window.__blits.push({key:window.__artKey,args:Array.from(arguments).slice(1),alpha:this.globalAlpha});return old.apply(this,arguments);};
        for(const name of ['weaponFeedbackArt','combatAtlasDraw','drawMfx']){const f=window[name];window[name]=function(key){window.__artKey=key;try{return f.apply(this,arguments);}finally{window.__artKey=null;}};}}''')
        pg.evaluate('''()=>{const f=stage3DroneShotDraw;stage3DroneShotDraw=function(q){window.__artKey='bpfx_proj_laser_0';try{return f.apply(this,arguments);}finally{window.__artKey=null;}};
        const g=l23FovDraw;l23FovDraw=function(b,B,i,p,k){window.__artKey='bmfx_fov_'+l23FovPhase(k)+'_tall';try{return g.apply(this,arguments);}finally{window.__artKey=null;}};}''')
        def step(n):
            for i in range(0,n,30):pg.evaluate('n=>window.__step(n)',min(30,n-i));pg.wait_for_timeout(12)
        def ready(expr):
            for _ in range(160):
                if pg.evaluate(expr):return True
                pg.wait_for_timeout(40)
            return False
        def prep(stage):pg.evaluate(PREP,stage);step(2)
        def fight(stage,role):
            pg.evaluate('a=>window.__fight(a[0],a[1],"yuri")',[stage,role]);pg.evaluate('()=>{stagePlan=[];enemies=[];story=null;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);playerHit=function(){};player.invuln=0;}')
            for _ in range(80):
                if pg.evaluate('()=>{const T=window.__tgt();return T&&!T.enter&&T.y>0&&(!T._rzb||T._rzb.state!=="arrival");}'):break
                step(6)
            step(8)
        def shot(name):
            pg.evaluate('()=>{if(state===GS.PLAY){shake=0;drawWorld(0);}}');r=pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]");path=OUT/(name+'.png');path.write_bytes(base64.b64decode(r));shots.append(path)

        ok(ready('()=>["nmb_box5","nmb_crate10","nmc_20","nmc_50","nmc_100","msl_2_0"].every(k=>XART.rdy(k))'),'all authored supply boxes and loose missile projectile art decode')
        fight(1,'boss');pg.evaluate('()=>{powerups=[];boss._missileSupply=null;}')
        step(410);ok(pg.evaluate('()=>powerups.length===0'),'boss supplies wait through the entrance allowance')
        step(14);shot('boss_supply_arrival')
        details['bossSupply']=pg.evaluate('()=>powerups.map(p=>({kind:p.kind,pack:p._pack,x:p.x,y:p.y}))')
        ok(len(details['bossSupply'])==1 and details['bossSupply'][0]['pack'] in ['missilepack','missilepack10','missilepack20'],'native boss update spawns an approved x5/x10/x20 supply')
        pg.evaluate('()=>{const p=powerups[0];p._pack="missilepack";p.x=player.x;p.y=player.y-65;breakContainer(p);p.dead=true;}')
        step(2);shot('boss_x5_opened')
        pg.evaluate('()=>{const p=powerups.find(p=>p.kind==="missilepack");run.bombs=0;player.x=p.x;player.y=p.y;}');step(2)
        ok(pg.evaluate('()=>run.bombs===5'),'actual native pickup of the x5 box grants exactly five missiles')
        fight(3,'mini');pg.evaluate('()=>{powerups=[];subBoss._missileSupply=null;}');step(425);shot('miniboss_supply')
        ok(pg.evaluate('()=>powerups.some(p=>p._bossSupply&&p.kind==="mcrate")'),'native miniboss combat also receives missile supplies')
        prep(1);pg.evaluate('()=>{window.__drops=[];const d=drawMfx;drawMfx=function(key){if(key==="msl_2_0"){const M=ctx.getTransform();__drops.push({key,angle:Math.atan2(M.b,M.a),args:Array.from(arguments).slice(1)});}return d.apply(this,arguments);};const r=Math.random;Math.random=()=>0;const e=spawnEnemy("s1jetdelta",worldWidth()/2,240,{route:"straight"});e.enter=false;e.ghost=false;e.dropOk=false;hitEnemy(e,9999);Math.random=r;}')
        shot('loose_missiles_first')
        details['looseFirst']=pg.evaluate('()=>powerups.filter(p=>p._looseMissile).map(p=>({x:p.x,y:p.y,t:p.t}))')
        step(22);shot('loose_missiles_scattered')
        details['looseLater']=pg.evaluate('()=>powerups.filter(p=>p._looseMissile).map(p=>({x:p.x,y:p.y,t:p.t}))')
        ok(len(details['looseFirst'])==2 and len(details['looseLater'])==2,'a real fodder hull destruction can grant two collectible projectiles')
        ok(details['looseLater'][1]['x']-details['looseLater'][0]['x']>details['looseFirst'][1]['x']-details['looseFirst'][0]['x'],'the two loose missiles visibly scatter apart during native simulation')
        ok(pg.evaluate('()=>__drops.some(q=>q.angle>.6)&&__drops.some(q=>Math.abs(q.angle)<.01)'),'loose missiles render their authored projectile plate at changing rotation in the game canvas')
        pg.evaluate('()=>{const p=powerups.find(p=>p._looseMissile);run.bombs=10;player.x=p.x;player.y=p.y;}');step(1)
        ok(pg.evaluate('()=>run.bombs===11'),'collecting one scattered missile uses the real one-round ammo path')
        prep(8);pg.evaluate('()=>{powerups=[];for(const [kind,dx]of [["missilepack50",-85],["missilepack100",85]])powerups.push({kind,x:player.x+dx,y:260,vy:.7,t:0,w:48,h:48,bob:0});}');shot('stage8_large_ammo')
        ok(pg.evaluate('()=>["missilepack50","missilepack100"].every(k=>powerups.some(p=>p.kind===k))'),'stage-8 x50 and x100 supply plates render together at authored proportions')
        details['error']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['error'],'zero Chromium page, console or controlled-loop errors')
        b.close()
    srv.shutdown()
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
    if n!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
