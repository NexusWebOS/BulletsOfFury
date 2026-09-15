"""Real Chromium proof for the Sovereign shared unpowered-ram warning."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'sovereign_shared_ram_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image
def main():
  checks,errors,shots=[],[],[]
  def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
  class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
    def log_message(self,*a):pass
  srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
  with sync_playwright() as pw:
    br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{srv.server_port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
    fight=page.evaluate("()=>window.__fight(4,'boss','yuri')");ok(fight.get('ok'),'native Stage-4 boss route opens in Chromium')
    keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['s4w_boss_charge_2','s4w_boss_flight_0']
    page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];state=GS.PLAY;stateT=1;run.stage=4;curStage=STAGES[3];diffKey='normal';DIFF=DIFFS.normal;player.x=camLeftX()+120;player.y=VH-62;player.invuln=99;player.dead=false;player.alive=true;run.shield=3;
      boss=null;bossActive=false;spawnBoss('stormsovereign');boss.enter=false;boss.x=(camLeftX()+camRightX())*.5;boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss.fireCd=999;boss._s4war.shield.active=false;boss._s4war.shield.rearming=false;for(const n of boss._s4war.shield.nodes)n.dead=true;bossActive=true;
      window.__ramGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__ramGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));stage4RamStart(boss);} """,keys)
    ready=False
    for _ in range(260):
      ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
      if ready:break
      page.wait_for_timeout(35)
    ok(ready,'authored green, yellow and red FOV/alert art decodes before capture')
    def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.t=(boss.t||0)+1/60;stage4WarfareBossTick(boss,1/60);}}",n)
    def snap(name):
      page.evaluate('()=>{shake=0;window.__ramGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const R=boss._s4war.ram,B=boss._combatWarnings['sovereign-unpowered-ram'];return {mode:boss._s4war.mode,t:R&&R.t,lane:R&&R.lane,locked:R&&R.locked,y:boss.y,warn:B&&{t:B.t,warm:B.warm,released:B.released},gets:Array.from(new Set(window.__ramGets))}}""")
      raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));shots.append(p);return d
    step(12);green=snap('sovereign_ram_01_green');ok(green['mode']=='ramTell' and not green['locked'],'green warning tracks the player during the early aiming window');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green uses the shared authored field and overhead alert')
    page.evaluate('()=>{player.x=camRightX()-130}');step(18);yellow=snap('sovereign_ram_02_yellow');ok(yellow['mode']=='ramTell' and yellow['locked'] and yellow['lane']!=green['lane'],'yellow commits after following the player to a new lane');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow uses the shared authored field and overhead alert')
    locked=yellow['lane'];page.evaluate('()=>{player.x=camLeftX()+45}');step(12);red=snap('sovereign_ram_03_red');ok(red['mode']=='ramTell' and red['locked'] and red['lane']==locked,'red retains the committed lane through a late dodge');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red uses the shared authored field and overhead alert')
    step(19);release=snap('sovereign_ram_04_release');ok(release['mode']=='ramDive' and release['warn']['released'] and release['lane']==locked,'the Sovereign releases only after the full shared warning and dives on the committed lane')
    for p in shots:
      im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
    ok(not errors,'zero Chromium page or console errors');br.close()
  srv.shutdown();res={'checks':checks,'errors':errors,'fight':fight,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
  if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
