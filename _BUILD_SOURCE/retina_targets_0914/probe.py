"""Native Chromium checks and pixels for Mike's stage 1–5 corrections."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/retina_targets_0914';OUT.mkdir(parents=True,exist_ok=True)
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

        pg.evaluate("()=>{const f=retinaTinted;retinaTinted=function(k,i,p){window.__artKey=k+'_'+i;return f.apply(this,arguments);};const g=drawRetina;drawRetina=function(){try{return g.apply(this,arguments);}finally{window.__artKey=null;}};}")
        fight(6,'boss');step(12)
        pg.evaluate("()=>{boss._mega.phase=2;boss._mega.cd=999;boss._mega.thunderhead=null;boss._mega.nodes.forEach(n=>{n.hp=60;n.maxhp=60;n.dead=false;});boss._bayShield.up=true;boss._bayShield.hp=boss._bayShield.max;boss._lc.playing=false;boss._cn=null;run.bombs=10;eBullets=[];retina={target:null};}")
        ok(pg.evaluate("()=>_lockTargets().length===4&&_lockTargets().every(t=>t.kind==='storm node')&&_lockTargets().indexOf(boss)<0"),'native shielded Stage-6 carrier exposes all four electrical nodes and excludes its hull')
        pg.evaluate("()=>{window.__cycled=[];for(let i=0;i<5;i++){cycleLock();__cycled.push(retina.target.part.id);}window.__selected=retina.target;}")
        ok(pg.evaluate("()=>new Set(__cycled).size===4&&__cycled[0]===__cycled[4]"),'Retina taps cycle through every native electrical node and wrap')
        step(29);ok(pg.evaluate("()=>retina.phase==='locked'&&retina.target===__selected"),'native Retina acquisition settles on the selected electrical node')
        ok(ready("()=>[0,1,2,3].every(i=>!!retinaTinted('retB',i,'yuri'))"),'all authored locked Retina frames decode')
        shot('stage6_node_retina')
        ok(pg.evaluate("()=>__blits.some(q=>/^retB_/.test(q.key))"),'game context draws the authored Retina frame on the electrical node')
        pg.evaluate("()=>{window.__beforeHp=boss.hp;window.__node=retina.target.part;window.__ammo=run.bombs;useBomb();const b=pBullets[pBullets.length-1];b.x=__selected.x;b.y=__selected.y-6;b.spd=1;}");step(2)
        ok(pg.evaluate("()=>__node.hp===36&&boss.hp===__beforeHp&&run.bombs===__ammo-1"),'actual launched manual missile spends one ammo and damages only its selected electrical node')
        pg.evaluate("()=>{boss._bayShield.up=false;boss._bay.L=20;boss._bay.R=20;}")
        ok(pg.evaluate("()=>_lockTargets().filter(t=>t.kind==='missile bay').length===2&&_lockTargets().indexOf(boss)<0"),'open missile bays are selectable while the protected carrier core remains excluded')
        pg.evaluate("()=>{boss._bay.L=0;boss._bay.R=0;boss._bayShield.up=false;}")
        ok(pg.evaluate("()=>_lockTargets().indexOf(boss)>=0"),'destroyed bays and lowered shield expose the carrier hull for Retina selection')
        pg.evaluate("()=>{retina={target:boss,phase:'locked',lockT:5};boss._bayShield.up=true;updateRetina(.01);}")
        ok(pg.evaluate("()=>!retina.target&&!retina.phase"),'shield reformation immediately clears an existing hull lock')
        fight(4,'boss');step(8);pg.evaluate('()=>{subBoss=null;subBossActive=false;}')
        pg.evaluate("()=>{boss.hp=boss.maxhp*.5;boss._s4war.shieldThresholdIndex=2;boss._s4war.coreUnlocked=true;stage4CoreTurretSpawnMissing(boss,.5);boss._s4war.coreTurrets.forEach(t=>{t.spawnT=2;t.materialize=1;});}");step(2)
        details['stage4']=pg.evaluate("()=>({targets:_lockTargets().map(t=>({kind:t.kind,name:t.name,dead:t.dead})),active:boss._s4war.shield.active,rearming:boss._s4war.shield.rearming,helpers:boss._s4war.coreTurrets.map(t=>({dead:t.dead,materialize:t.materialize}))})");print(json.dumps(details['stage4']),flush=True)
        ok(pg.evaluate("()=>{const t=_lockTargets();return t.filter(t=>t.kind==='electrical node').length===boss._s4war.shield.nodes.filter(n=>!n.dead).length&&t.filter(t=>t.kind==='helper').length===2&&t.indexOf(boss)<0;}"),'native Stage-4 scanner exposes every shield node and both independent helpers')
        pg.evaluate("()=>{retina={target:_lockTargets().find(t=>t.kind==='helper'),phase:'seek',seekT:0,ox:player.x,oy:player.y,x:player.x,y:player.y,spin:0,_tick:0};}");step(29);shot('stage4_helper_retina')
        ok(pg.evaluate("()=>retina.phase==='locked'&&retina.target.kind==='helper'"),'authored Retina visibly locks onto an independent chaingun helper')
        details['error']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['error'],'zero Chromium page, console or controlled-loop errors')
        b.close()
    srv.shutdown()
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
    if n!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
