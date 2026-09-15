"""Real Chromium proof for the Furious Sovereign giant lightning strike."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'sovereign_giant_strike_0915';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
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
    keys=['s4w_boss_charge_6','s4w_boss_energized_0','cfx_stage4_chain_lightning','s4w_lightning_ball_0','bmfx_fov_yellow_tall','bmfx_fov_red_tall','bmfx_alert_yellow_danger','bmfx_alert_red_danger']
    page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];state=GS.PLAY;stateT=1;run.stage=4;curStage=STAGES[3];diffKey='furious';DIFF=DIFFS.furious;player.x=camLeftX()+28;player.y=VH-54;player.invuln=0;player.dead=false;player.alive=true;run.shield=3;
      boss=null;bossActive=false;spawnBoss('stormsovereign');boss.enter=false;boss.x=(camLeftX()+camRightX())*.5;boss.y=boss._s4war.homeY;boss._drawY=boss.y;boss.fireCd=999;boss._s4war.shield.active=false;boss._s4war.shield.rearming=false;for(const n of boss._s4war.shield.nodes)n.dead=true;bossActive=true;
      window.__giantGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__giantGets.push(k);return g(k);};ks.forEach(k=>XART.rdy(k));stage4GiantStrikeStart(boss);} """,keys)
    ready=False
    for _ in range(260):
      ready=page.evaluate("ks=>ks.every(k=>XART.rdy(k))",keys)
      if ready:break
      page.wait_for_timeout(35)
    ok(ready,'authored yellow/red FOV, alert, core and lightning art decode before capture')
    def step(n):page.evaluate("n=>{for(let i=0;i<n;i++){boss.t=(boss.t||0)+1/60;stage4WarfareBossTick(boss,1/60);}}",n)
    def snap(name):
      page.evaluate("()=>{shake=0;window.__giantGets=[];drawWorld(0)}");d=page.evaluate("""()=>({mode:boss._s4war.mode,t:boss._s4war.giantStrike&&boss._s4war.giantStrike.t,released:boss._s4war.giantStrike&&boss._s4war.giantStrike.released,color:boss._s4war.giantStrike&&stage4GiantStrikeColor(boss._s4war.giantStrike),bounds:stage4GiantStrikeBounds(),hits:boss._s4war.giantStrikeHits,gets:Array.from(new Set(window.__giantGets))})""")
      raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));shots.append(p);return d
    step(132);yellow=snap('sovereign_giant_01_yellow_charge');ok(yellow['color']=='yellow' and not yellow['released'],'the first charge phase is yellow and nonlethal')
    ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow uses the authored system FOV and alert frame')
    step(124);red=snap('sovereign_giant_02_red_charge');ok(red['color']=='red' and not red['released'],'the final charge phase turns red before release')
    ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red uses the authored system FOV and alert frame')
    step(50);strike=snap('sovereign_giant_03_strike');ok(strike['released'] and strike['mode']=='giantStrike','the giant strike releases only after the five-second charge')
    ok('cfx_stage4_chain_lightning' in strike['gets'],'the released strike is built from the authored chain-lightning atlas')
    ok(strike['hits']==0,'the ship survives untouched in the left safe corner')
    page.evaluate("()=>{const r=stage4GiantStrikeBounds();player.x=(r.left+r.right)*.5;player.invuln=0;stage4WarfareBossTick(boss,1/60)}")
    central=page.evaluate("()=>boss._s4war.giantStrikeHits");ok(central==1,'the central lightning field hits once while the corners stay safe')
    # At the canvas backing scale, the centre should be materially brighter than both clear bottom corners.
    im=Image.open(shots[-1]).convert('RGB');w,h=im.size;band=im.crop((0,int(h*.70),w,h));left=band.crop((0,0,int(w*.14),band.height));center=band.crop((int(w*.40),0,int(w*.60),band.height));right=band.crop((int(w*.86),0,w,band.height));
    lum=lambda x:sum(ImageStat.Stat(x).mean)/3
    ok(lum(center)>max(lum(left),lum(right))*1.10,'native pixels show a bright central strike with two visibly clear corner lanes')
    for p in shots:
      im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
    ok(not errors,'zero Chromium page or console errors');br.close()
  srv.shutdown();res={'checks':checks,'errors':errors,'fight':fight,'yellow':yellow,'red':red,'strike':strike,'centralHits':central,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
  if passed!=len(checks):raise SystemExit(1)
if __name__=='__main__':main()
