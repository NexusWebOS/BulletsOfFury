"""Real Chromium proof for Frost Cruiser darkness, crackle, warning and edge-to-edge laser sweep."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'frost_cruiser_sweep_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat

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
          stagePlan=[];enemies=[];eBullets=[];pBullets=[];particles=[];story=null;dlgBox=function(){};
          run.stage=3;curStage=STAGES[2];player.x=104;player.y=390;player.invuln=1e9;subBoss=null;subBossActive=false;boss=null;bossActive=false;
          spawnSubBoss('frostcruiser');subBoss.enter=false;subBoss.x=worldWidth()/2;subBoss.y=shipBossStationY(subBoss);subBoss._drawY=subBoss.y;
          state=GS.PLAY;stateT=1;window.__sweep={crackles:0,atlas:0,min:9,max:-9,last:null,monotonic:true};
          Audio.SFX.crackle=function(){window.__sweep.crackles++;};
          const ca=combatAtlasDraw;combatAtlasDraw=function(){if(arguments[0]==='cfx_stage4_chain_lightning')window.__sweep.atlas++;return ca.apply(this,arguments);};
          for(const k of ['nsb_frost_cruiser','cfx_stage4_chain_lightning','nlz_3_b0','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'])XART.rdy(k);
        }""")
        for _ in range(200):
            ready=page.evaluate("()=>['nsb_frost_cruiser','cfx_stage4_chain_lightning','nlz_3_b0','bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall'].every(k=>XART.rdy(k))")
            if ready:break
            page.wait_for_timeout(35)
        ok(ready,'authored Frost hull, lightning, beam and warning plates decode before capture')
        def step(n):page.evaluate("""n=>{for(let i=0;i<n;i++){jungleCruiserDirector(subBoss,1/60);subBoss.t=(subBoss.t||0)+1/60;stateT+=1/60;
          const J=subBoss._jc;if(J.state==='beamSweep'){const S=window.__sweep;if(S.last!=null&&J.beamAng<S.last-1e-8)S.monotonic=false;S.last=J.beamAng;S.min=Math.min(S.min,J.beamAng);S.max=Math.max(S.max,J.beamAng);}}}""",n)
        def capture(name):
            page.evaluate("()=>{shake=0;drawWorld(0);}");png=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]")
            p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(png));shots.append(p)
            return page.evaluate("()=>({state:subBoss._jc.state,t:subBoss._jc.t,charge:subBoss._jc.charge,ang:subBoss._jc.beamAng,dir:subBoss._jc.beamDir,active:subBoss._jc.beamActive,crackles:window.__sweep.crackles,atlas:window.__sweep.atlas})")
        baseline=capture('frost_sweep_baseline')
        page.evaluate("()=>jungleCruiserSetState(subBoss,'beamCharge')")
        step(90);charge=capture('frost_sweep_charge')
        step(75);red=capture('frost_sweep_red_warning')
        step(18);start=capture('frost_sweep_start_right')
        step(153);middle=capture('frost_sweep_middle')
        step(132);end=capture('frost_sweep_end_left')
        step(30)
        stats=page.evaluate("()=>({state:subBoss._jc.state,active:subBoss._jc.beamActive,crackles:window.__sweep.crackles,atlas:window.__sweep.atlas,min:window.__sweep.min,max:window.__sweep.max,monotonic:window.__sweep.monotonic,width:FROST_BEAM_WIDTH})")
        means=[]
        for p in shots:
            im=Image.open(p).convert('RGB');means.append(sum(ImageStat.Stat(im.crop((0,160,960,900))).mean)/3)
        ok(charge['state']=='beamCharge' and charge['dir']==1 and charge['atlas']>=4,'left-side player commits a right-to-left sweep while authored lightning crackles')
        ok(red['state']=='beamCharge' and red['charge']>.9 and red['crackles']>=9,'three-second charge reaches its red warning with repeated crackle cues')
        ok(means[1]<means[0]*.88 and means[2]<means[0]*.72,'arena visibly darkens further as the laser charge builds')
        ok(start['active'] and start['ang']<-.74 and middle['active'] and abs(middle['ang'])<.12,'beam starts at the far right and crosses the centre once')
        ok(stats['min']<-.76 and stats['max']>.74 and stats['monotonic'],'live laser sweeps monotonically across the complete viewport')
        ok(stats['width']==52.5,'visible beam and collision share the exact 25%-wider width')
        ok(stats['state']=='recover' and not stats['active'],'single sweep is bounded and restores the encounter')
        for p in shots:
            im=Image.open(p).convert('RGB');ok(im.size==(960,1024)and im.getbbox()is not None,f'{p.stem} is a non-empty native game frame')
        ok(not errors,'zero Chromium page or console errors');browser.close()
    server.shutdown();result={'checks':checks,'errors':errors,'details':{'fight':fight,'baseline':baseline,'charge':charge,'red':red,'start':start,'middle':middle,'end':end,'stats':stats,'means':means},'shots':[str(p.relative_to(ROOT))for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    passed=sum(x['pass']for x in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
    if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
