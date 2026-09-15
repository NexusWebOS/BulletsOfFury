"""Native Chromium verification for shared enemy shield-break stun and splash."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
OUT=ROOT/'_shots/enemy_shield_stun_0915';OUT.mkdir(parents=True,exist_ok=True)

def main():
    checks=[];errors=[]
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
        def step(n):
            for i in range(0,n,30):page.evaluate('n=>window.__step(n)',min(30,n-i));page.wait_for_timeout(10)
        page.evaluate("""()=>{run.pilot='freezer';pilotIndex=PILOTS.findIndex(p=>p.key==='freezer');run.stage=2;curStage=STAGES[1];beginStage(2);setState(GS.PLAY);
          player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;playerHit=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;
          boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];pImpacts=[];
          Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);Snd.loopStopAll();window.__auto=function(){};
          _seat=1;run.weapon=4;run.wlevel=5;run.wlevels=run.wlevels||[1,1,1,1,1,1,1];run.wlevels[4]=5;run.wvars=run.wvars||[null,null,null,null,null,null,null];run.wvars[4]='icebreath';player.fireCd=0;
          const e=spawnEnemy('disc',player.x,330,{inPlace:true});e.x=player.x;e.y=330;e.hp=e.maxhp=e._maxhp=120;e.pattern='straight';e.vy=0;e._entry=null;e._volc=null;
          if(!e._esh)enemyShieldEquip(e,'bubble_hex',1,{once:true,drawScale:2.55});e._esh.energy=e._esh.max=.2;e._esh.phase='active';e._esh.impactCd=0;
          const n=spawnEnemy('eye',player.x+88,330,{inPlace:true});n.x=player.x+88;n.y=330;n.hp=n.maxhp=n._maxhp=120;n.pattern='straight';n.vy=0;n._entry=null;n._volc=null;if(n._esh){n._esh.phase='broken';n._esh.energy=0;}
          window.__shieldUnit=e;window.__splashUnit=n;window.__shieldY=e.y;window.__nearHp=n.hp;window.__breakSfx=0;
          const base=Audio.SFX.shieldBreakCombat;Audio.SFX.shieldBreakCombat=function(){window.__breakSfx++;return base&&base();};}""")
        box=page.locator('#screen').bounding_box();page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.72);page.mouse.down();step(1);page.mouse.up()
        ok(page.evaluate("()=>__shieldUnit._esh.phase==='broken'&&!!__shieldUnit._eshStun"),'actual held primary fire breaks the live Stage-2 enemy shield and starts stun')
        ok(page.evaluate('()=>__shieldUnit.hp===120'),'the breaking round is fully absorbed before the hull stun')
        ok(page.evaluate('()=>__splashUnit.hp<__nearHp'),'shield discharge damages the nearby authored enemy')
        page.evaluate('()=>{pBullets=[];}');step(15)
        ok(page.evaluate('()=>__shieldUnit.y<__shieldY&&Math.abs(__shieldUnit._eshStun.angle)>.1'),'the stunned unit is visibly lifted and rotating')
        ok(page.evaluate('()=>!__shieldUnit._frenzy'),'frenzy waits until the punish window ends')
        page.evaluate('()=>{pBullets=[];drawWorld(0);drawHUD();}')
        data=page.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]");(OUT/'shield_break_stun.png').write_bytes(base64.b64decode(data))
        step(55)
        ok(page.evaluate('()=>!__shieldUnit._eshStun&&__shieldUnit._frenzy===1'),'the hull restores and enters its existing frenzy after the stun')
        ok(page.evaluate('()=>Math.abs(__shieldUnit.y-__shieldY)<.001'),'the temporary lift restores the authored movement anchor exactly')
        ok(page.evaluate('()=>__breakSfx===1'),'the break cue plays once without repeating at the stun-to-frenzy handoff')
        controlled=page.evaluate('()=>window.__err||null')
        ok(not errors and not controlled,'zero Chromium page, console or controlled-loop errors')
        browser.close()
    srv.shutdown()
    result={'checks':checks,'errors':errors,'screenshot':'_shots/enemy_shield_stun_0915/shield_break_stun.png'}
    (OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
