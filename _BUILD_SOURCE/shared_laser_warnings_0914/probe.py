"""Native Chromium checks and pixels for Mike's stage 1–5 corrections."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/shared_laser_warnings_0914';OUT.mkdir(parents=True,exist_ok=True)
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

        prep(3);ok(ready('()=>["l23fx_rime_laser_3","l23fx_inferno_laser_3","bmfx_fov_green_tall","bmfx_fov_yellow_tall","bmfx_fov_red_tall"].every(k=>XART.rdy(k))'),'all shared warning plates and authored beam families decode')
        for family in ['rime','inferno','legion','future']:
            pg.evaluate('f=>{window.__warningOwner={_ship:"rimewall",x:worldWidth()/2,y:140,w:195,h:195,t:0};l23BossBeamStart(__warningOwner,f,["C"],[Math.PI/2],.2,.5,.2,34);window.__blits=[];}',family)
            for color,t in [('green',.35),('yellow',1.4),('red',2.7)]:
                pg.evaluate('t=>{const b=__warningOwner;b._l23Beam.t=t;drawWorld(0);ctx.save();if(worldWidth()>viewW())ctx.translate(-camX,0);l23BossBeamDraw(b);ctx.restore();}',t)
                path=OUT/(family+'_'+color+'.png');path.write_bytes(base64.b64decode(pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")))
            ok(pg.evaluate('()=>["green","yellow","red"].every(c=>__blits.some(q=>q.key==="bmfx_fov_"+c+"_tall"))'),family+' laser warning renders all three authored FOV colors in real game drawImage')
        fight(3,'boss');pg.evaluate('()=>{boss._l23Beam=null;boss._sba=null;stage3BossAttack(boss,"s3wallcannons",0,0,1);}')
        step(195);shot('dark_blue_cannon_release')
        ok(pg.evaluate('()=>boss._l23Beam&&boss._l23Beam.released&&boss._l23Beam.slots.every(s=>s==="L"||s==="R")'),'native stage-3 beams retain only the actual side cannon release slots')
        details['error']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['error'],'zero Chromium page, console or controlled-loop errors')
        b.close()
    srv.shutdown()
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    n=sum(c['pass']for c in checks);print('%d passed / %d failed'%(n,len(checks)-n),flush=True)
    if n!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
