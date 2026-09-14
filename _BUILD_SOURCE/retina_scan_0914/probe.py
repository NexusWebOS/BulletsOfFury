"""Native Chromium checks and pixels for Mike's stage 1–5 corrections."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/retina_scan_0914';OUT.mkdir(parents=True,exist_ok=True)
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
        pg.evaluate("()=>{boss._mega.phase=2;boss._mega.cd=999;boss._mega.thunderhead=null;boss._mega.nodes.forEach(n=>{n.hp=100;n.maxhp=100;n.dead=false;});boss._bayShield.up=true;boss._bayShield.hp=boss._bayShield.max;boss._lc.playing=false;boss._cn=null;run.bombs=10;eBullets=[];window.__auto=function(){};retina={target:null};player._retinaScan=null;run.retinaScan=false;}")
        pg.evaluate("()=>{window.__badText=[];const f=ctx.fillText;ctx.fillText=function(t){if(t==null||t==='undefined')__badText.push(String(t));return f.apply(this,arguments);};}")
        pg.evaluate("()=>{breakContainer({kind:'mcrate',x:player.x-35,y:player.y-55,_pack:'missilepack'});}")
        ok(pg.evaluate("()=>powerups.filter(p=>p.kind==='retinascan').length===1"),'breaking a native missile crate makes one Retina Scan upgrade available')
        ok(ready("()=>[0,1,2,3].every(i=>!!retinaTinted('retA',i,'yuri'))"),'existing authored Retina pickup frames decode')
        shot('retina_scan_pickup');ok(pg.evaluate('()=>__badText.length===0'),'crate break uses the authored shock effect and never prints undefined')
        pg.evaluate("()=>{const p=powerups.find(p=>p.kind==='retinascan');p.x=player.x;p.y=player.y;p.vy=0;}");step(2)
        ok(pg.evaluate("()=>run.retinaScan&&!powerups.some(p=>p.kind==='retinascan')"),'native pickup collision grants Retina Scan to the pilot')
        pg.evaluate("()=>{powerups=[];run.bombs=10;window.__blits=[];window.__fired=[];const fire=useBomb;useBomb=function(){const n=pBullets.length,v=fire.apply(this,arguments);for(const q of pBullets.slice(n))if(q.kind==='gmiss')__fired.push({frame:window.__i,target:q.tgt&&q.tgt.part&&q.tgt.part.id,ammo:run.bombs});return v;};}")
        pg.evaluate('()=>{player.x=worldWidth()/2+100;}')
        pg.keyboard.down('c');step(1)
        for _ in range(4):
            pg.keyboard.down('ArrowUp');step(1);pg.keyboard.up('ArrowUp');step(1)
        for key in ['ArrowLeft','ArrowLeft','ArrowRight','ArrowRight']:
            pg.keyboard.down(key);step(1);pg.keyboard.up(key);step(1)
        ok(pg.evaluate('()=>!player.roll&&!player.somer'),'holding Retina consumes scan taps before roll and somersault input')
        pg.keyboard.up('c');step(30)
        details['scan']=pg.evaluate("()=>({marks:retinaScanState().marks.map(m=>({id:m.target.part&&m.target.part.id,phase:m.phase,life:m.lockT})),single:!!retina.target,ammo:run.bombs,targets:_lockTargets().map(t=>({x:t.x,y:t.y})),cam:[camLeftX(),camRightX()],player:[player.x,player.y]})")
        print(json.dumps(details['scan']),flush=True)
        ok(pg.evaluate("()=>retinaScanState().marks.length===4&&retinaScanState().marks.every(m=>m.phase==='locked')&&!retina.target"),'real held Retina and directional taps acquire four separate node locks')
        shot('four_node_retinas')
        ok(pg.evaluate("()=>__blits.filter(q=>/^retB_/.test(q.key)).length>=4"),'game context draws all four authored locked Retina plates')
        pg.keyboard.down('k');step(1);pg.keyboard.up('k');step(18)
        details['launches']=pg.evaluate('()=>__fired')
        ok(pg.evaluate("()=>__fired.length===4&&new Set(__fired.map(q=>q.target)).size===4&&run.bombs===6"),'one missile press launches four different locked targets and spends exactly four ammo')
        ok(pg.evaluate("()=>__fired.every((q,i)=>i===0||q.frame-__fired[i-1].frame>=3)"),'actual missile launches are separated by at least 50 milliseconds of game time')
        shot('sequential_missiles')
        pg.keyboard.down('c');step(1)
        pg.evaluate("()=>{pBullets=[];retina={target:null};boss._mega.nodes.forEach(n=>{n.dead=false;n.hp=100;});retinaScanClear();retinaScanAdd(_lockTargets()[0]);}");step(28)
        step(232);shot('retina_expiry_flash');step(73);pg.keyboard.up('c')
        ok(pg.evaluate("()=>!retinaScanState().marks.length&&!retinaScanState().queue"),'holding Retina does not extend the five-second multi-lock expiry')
        shot('retina_expired')
        pg.evaluate("()=>{retinaScanAdd(_lockTargets()[0]);}");step(28);pg.evaluate("()=>setState('paused')")
        life=pg.evaluate('()=>retinaScanState().marks[0].lockT');step(90)
        ok(abs(pg.evaluate('()=>retinaScanState().marks[0].lockT')-life)<.001,'pause freezes the multi-lock countdown')
        pg.evaluate("()=>{setState('play');player.dead=true;}");step(1)
        ok(pg.evaluate('()=>!player._retinaScan'),'death cancels all acquired and queued scan targets')
        details['error']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['error'],'zero Chromium page, console or controlled-loop errors')
        b.close()
    srv.shutdown()
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
    if n!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
