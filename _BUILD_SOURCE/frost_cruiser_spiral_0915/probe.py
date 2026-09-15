"""Real Chromium proof for the Hard/Furious Frost Cruiser Retina spiral volley."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'frost_cruiser_spiral_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    checks,errors,shots=[],[],[]
    def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  'if v else'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
        def log_message(self,*a):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        page.goto(f'http://127.0.0.1:{server.server_port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB);fight=page.evaluate("()=>window.__fight(3,'mini','yuri')");ok(fight.get('ok'),'native Stage-3 miniboss route opens in Chromium')
        page.evaluate("""()=>{
          stagePlan=[];stageWave=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];story=null;dlgBox=function(){};
          run.stage=3;curStage=STAGES[2];diffKey='hard';DIFF=DIFFS.hard;player.x=132;player.y=590;player.invuln=1e9;player.dead=false;
          subBoss=null;subBossActive=false;boss=null;bossActive=false;playerLocks=[];warnT=0;warnKind=null;subBossTriggered=true;subBossDone=false;state=GS.PLAY;stateT=1;
          spawnSubBoss('frostcruiser');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=shipBossStationY(subBoss);subBoss._drawY=subBoss.y;subBossActive=true;
          window.__spiral={born:[],atlas:0,sounds:0};
          const old=frostCruiserSpiralRocket;frostCruiserSpiralRocket=function(b,slot,i){const q=old(b,slot,i);if(q)window.__spiral.born.push({slot:slot,i:i,lock:q._lockId,swirl:q._swirl});return q;};
          const ca=combatAtlasDraw;combatAtlasDraw=function(){if(arguments[0]==='cfx_stage4_chain_lightning')window.__spiral.atlas++;return ca.apply(this,arguments);};
          const ms=Audio.SFX.missile;Audio.SFX.missile=function(){window.__spiral.sounds++;if(ms)return ms.apply(this,arguments);};
          jungleCruiserSetState(subBoss,'frostRocketCharge');
          for(const k of ['nsb_frost_cruiser','cfx_stage4_chain_lightning','retm_0','retm_1','retm_2','retm_3','retmb_0','retmb_1','retmb_2','retmb_3'])XART.rdy(k);
        }""")
        for _ in range(220):
            ready=page.evaluate("()=>['nsb_frost_cruiser','cfx_stage4_chain_lightning','retm_0','retm_1','retm_2','retm_3'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Frost hull, lightning and Retina plates decode before capture')
        def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){updatePlay(1/60);stateT+=1/60;}}",n)
        def capture(name):
            page.evaluate("()=>{shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({state:subBoss._jc.state,t:subBoss._jc.t,charge:subBoss._jc.charge,locks:playerLockState(),born:window.__spiral.born.slice(),atlas:window.__spiral.atlas,sounds:window.__spiral.sounds,live:eBullets.filter(q=>q._frostSpiral&&!q.dead).map(q=>({x:q.x,y:q.y,slot:q._frostSlot,i:q._frostIndex,shootable:q._shootable,swirl:q._swirl,lock:q._lockId}))})")
        step(48);charge=capture('frost_spiral_charge')
        step(39);first=capture('frost_spiral_first_release')
        step(51);volley=capture('frost_spiral_full_volley')
        intercept=page.evaluate("""()=>{const q=eBullets.find(x=>x._frostSpiral&&!x.dead);if(!q)return {had:false};const before=eBullets.filter(x=>x._frostSpiral&&!x.dead).length;
          pBullets.push({x:q.x,y:q.y,vx:0,vy:0,w:18,h:28,dmg:1,kind:'mg',t:0,dead:false});updatePlay(1/60);
          return {had:true,before:before,after:eBullets.filter(x=>x._frostSpiral&&!x.dead).length,targetDead:q.dead};}""")
        after=capture('frost_spiral_intercept')
        normal=page.evaluate("""()=>{diffKey='normal';DIFF=DIFFS.normal;playerLocks=[];eBullets=[];subBoss=null;subBossActive=false;spawnSubBoss('frostcruiser');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=shipBossStationY(subBoss);subBossActive=true;
          for(let i=0;i<60;i++)jungleCruiserDirector(subBoss,1/60);return {hard:subBoss._jc.hardVariant,state:subBoss._jc.state,locks:playerLocks.length};}""")
        ok(charge['state']=='frostRocketCharge' and charge['charge']>.55 and len(charge['locks'])==1 and charge['atlas']>=2,'Hard cruiser visibly charges both pods under one player Retina')
        ok(len(first['born'])>=1 and first['born'][0]['slot']=='L' and first['locks'][0]['state']=='locked','first charged rocket releases from the left pod as the Retina locks')
        born=volley['born'];ok(len(born)==6 and ''.join(q['slot'] for q in born)=='LRLRLR','six-round volley alternates physical left and right launch pods')
        ok(all(q['swirl'] and q['shootable'] for q in volley['live']) and len({q['lock'] for q in volley['live']})==1,'all live rockets visibly spiral, remain shootable and share one lock')
        ok(volley['sounds']==6,'each independent rocket release owns one missile sound beat')
        ok(intercept['had'] and intercept['targetDead'] and intercept['after']==intercept['before']-1,'a real player machine round destroys one incoming spiral rocket')
        ok(normal=={'hard':False,'state':'missiles','locks':0},'Normal retains its established missile phase with no added Retina')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'charge':charge,'first':first,'volley':volley,'intercept':intercept,'after':after,'normal':normal},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
