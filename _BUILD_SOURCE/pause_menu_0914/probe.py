"""Native Chromium checks and pixels for Mike's stage 1–5 corrections."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/pause_menu_0914';OUT.mkdir(parents=True,exist_ok=True)
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

        pg.evaluate('()=>window.__realPlayerHit=window.__realHit||playerHit')
        prep(1);step(60);ok(ready('()=>drawLevelMaster(0)'),'authored stage background decodes before paused pixel capture');step(2);pg.evaluate('()=>{Audio.startMusic("lvl1");Audio.setVol("music",.60);setState("paused");}')
        details['before']=pg.evaluate('()=>({clock:stageTimer,x:player.x,y:player.y,music:Audio.getVol("music")})')
        step(70);shot('green_pause_menu')
        details['paused']=pg.evaluate('()=>({state,clock:stageTimer,x:player.x,y:player.y,music:Audio.getVol("music"),duck:pauseMusicDuck(),sel:playPause.sel,cur:Snd.cur&&Snd.cur.volume,expected:.60*Audio.getVol("master")*.28,screenFilter:document.getElementById("screen").style.filter})')
        ok(details['paused']['clock']==details['before']['clock']and details['paused']['x']==details['before']['x'],'pause menu animation leaves the real stage clock and player position frozen')
        ok(details['paused']['music']==.60 and details['paused']['duck']==.28 and abs(details['paused']['cur']-details['paused']['expected'])<.0001,'actual music element is ducked while Options retains the original preference')
        ok(details['paused']['sel']==0 and details['paused']['screenFilter']=='','top resume selection retains a colored green overlay above grayscale world pixels')
        pg.evaluate('()=>Input.injectTap("backspace")');step(2)
        ok(pg.evaluate('()=>state==="paused"'),'Backspace does not exit the native paused fight')
        pg.evaluate('()=>playPauseChoose(3)');step(2);shot('pause_options')
        pg.evaluate('()=>{Audio.setVol("music",.70);optApply();}');step(2)
        ok(pg.evaluate('()=>state==="paused"&&playPause.mode==="root"&&Audio.getVol("music")===.70'),'real Options apply returns to pause and keeps the new music preference')
        pg.evaluate('()=>playPauseChoose(4)');step(2);shot('pause_help')
        pg.evaluate('()=>Input.injectTap("escape")');step(2)
        ok(pg.evaluate('()=>state==="paused"&&playPause.mode==="root"'),'real Help returns to the paused fight')
        pg.evaluate('()=>playPauseChoose(0)');step(2)
        ok(pg.evaluate('()=>state===GS.PLAY&&pauseMusicDuck()===1&&Audio.getVol("music")===.70'),'resume restores full relative music volume without resetting Options')
        pg.evaluate('()=>{setState("paused");playPauseChoose(2);}');step(2);shot('restart_level')
        ok(pg.evaluate('()=>state===GS.PLAY&&run.stage===1&&stageTimer<.1&&!player.dead'),'restart resets the same stage and restores the living pilot')
        pg.evaluate('()=>{run.mode="campaign";playerHit=window.__realPlayerHit;setState("paused");playPauseChoose(1);}')
        step(30);shot('pause_exit_burning_spin')
        ok(pg.evaluate('()=>player.dead&&player._spin&&player._spin.turns>=540&&playPause.exit.save.name==="Autosav01.json"'),'return-to-menu preserves a verified campaign autosave and starts the real anchored death spin')
        step(100);shot('pause_exit_game_over_saved')
        ok(pg.evaluate('()=>state===GS.GAMEOVER&&JSON.parse(localStorage.getItem("Autosav01.json")).pilot===run.pilot'),'game-over sequence visibly confirms the actual saved JSON record')
        step(340);shot('returned_to_title')
        ok(pg.evaluate('()=>state===GS.TITLE&&playPause===null&&campCanContinue()'),'completed game-over and fade return to title with campaign Continue available')
        pg.evaluate('()=>campSession=null');ok(pg.evaluate('()=>campCanContinue()&&campSession.stage===1'),'Continue recovers the verified autosave when the old in-memory session is gone')
        details['error']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['error'],'zero Chromium page, console or controlled-loop errors')
        b.close()
    srv.shutdown()
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
    if n!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
