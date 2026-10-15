"""Native fullscreen, menu, pilot, co-op and authored animation review."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot,json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/playthrough_1011/ui';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name+((' '+json.dumps(data)) if not value else ''),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.wait_for_function('()=>["cf_boot","cfui_panel","cf_logo",...Object.values(DIFF_META).map(a=>a.img)].map(k=>XART.rdy(k)).every(Boolean)')
  p.evaluate('()=>{drawBoot._started=false;stateT=0;ctx.setTransform(SS,0,0,SS,0,0);drawBoot(0);window.__bofFit();}')
  p.screenshot(path=str(OUT/'boot-single-logo.png'))
  p.locator('#fs-btn').click();p.wait_for_timeout(180)
  check('Authored button enters native fullscreen through its click gesture',p.evaluate('!!document.fullscreenElement'))
  check('Fullscreen control remains inside the fullscreen element',p.evaluate('document.fullscreenElement.contains(document.getElementById("fs-btn"))'))
  p.locator('#fs-btn').click();p.wait_for_timeout(100)
  check('Same control exits fullscreen',p.evaluate('!document.fullscreenElement'))
  for name,js in [('credits','drawCredits(0)'),('difficulty','drawDiff(0)'),('modes','drawModeSelect(0)'),('help','helpPageControls()')]:
   if name=='modes':p.wait_for_function('()=>["mode_lock_nexus_0915",...modeList().map(a=>a.pill).filter(Boolean)].map(k=>XART.rdy(k)).every(Boolean)')
   p.evaluate('()=>{Input.mouse.down=false;stateT=1;ctx.setTransform(SS,0,0,SS,0,0);'+js+';window.__bofFit();}')
   p.screenshot(path=str(OUT/(name+'.png')))
  pilots=p.evaluate('OPN_ORDER');p.evaluate('()=>{coleUnlocked=true;setState(GS.PILOT);}')
  p.wait_for_function('()=>openerPairsReady(OPN_ORDER)')
  for width,height,label in [(1600,1000,'wide'),(480,900,'narrow')]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('_setPilotViewport()')
   for pilot in pilots:
    p.evaluate('pk=>{pilotIndex=PILOTS.findIndex(p=>p.key===pk);pilotPending=null;pilotRot=0;drawPilot._pcFor=pk;pcStart(pk);pcard.done=true;stateT=2;ctx.setTransform(SS,0,0,SS,0,0);drawPilot(0);window.__bofFit();}',pilot)
    p.screenshot(path=str(OUT/(label+'-'+pilot+'.png')))
    q=p.evaluate('()=>{const a=PT11_UI.card,v=pilotViewSize();return{...a,inside:[a.body,a.ship,a.info].every(r=>r.every(Number.isFinite)&&r[0]>=0&&r[1]>=0&&r[0]+r[2]<=v.w&&r[1]+r[3]<=v.h),special:pcSpecial(a.pilot).name};}')
    check(label+' '+pilot+' has separate full pilot, large real ship and readable information areas',q['inside'] and q['ship'][3]>=80,q)
  p.set_viewport_size(dict(width=1600,height=1000));p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='maverick',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready&&XART.rdy(AC11_ART.key)}')
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;coopOn=true;run.lives=7;run.bombs=18;run2.pilot="lizzie";run2.lives=2;run2.bombs=9;run2.score=7654;ph8Sync();drawHUDStrip(hudctx);fb9HudSplit();window.__bofFit();}')
  for i in range(5):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();}');p.wait_for_timeout(60)
  p.screenshot(path=str(OUT/'armored-coop.png'))
  q=p.evaluate('PH8.last');check('Co-op shows each seat’s actual independent stocks',len(q)==2 and q[0]['lives']==7 and q[0]['missiles']==18 and q[1]['lives']==2 and q[1]['missiles']==9,q)
  for w,h in [(1280,720),(480,900)]:
   p.set_viewport_size(dict(width=w,height=h));p.evaluate('window.__bofFit()')
   q=p.evaluate('()=>["hud-row","screen","hud-bottom"].map(id=>{const r=document.getElementById(id).getBoundingClientRect();return{x:r.left,y:r.top,right:r.right,bottom:r.bottom}})')
   check(f'Two-seat HUD fits {w}x{h}',all(r['x']>=-1 and r['y']>=-1 and r['right']<=w+1 and r['bottom']<=h+1 for r in q),q)
  p.evaluate('coopOn=false');p.evaluate(shoot.SETUP,dict(state='PLAY',stage=3,pilot='maverick',invuln=True))
  p.wait_for_function('()=>pt11Ready("ice_jet_a")&&pt11Ready("ice_jet_b")')
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle="#101a29";ctx.fillRect(0,0,VW,VH);for(let j=0;j<2;j++){for(let i=0;i<16;i++){ctx.save();ctx.globalAlpha=.16;pt11Plate(j?"ice_jet_b":"ice_jet_a",i,120+j*230,300,1.2);ctx.restore();}}}')
  p.locator('#screen').screenshot(path=str(OUT/'ice-jets-onion.png'))
  check('Ice jet reels load all 32 registered drawn poses',p.evaluate('PT11_ART.ice_jet_a.length===16&&PT11_ART.ice_jet_b.length===16&&PT11.draws.ice_jet_a>=16&&PT11.draws.ice_jet_b>=16'))
  p.set_viewport_size(dict(width=1280,height=800));p.evaluate("()=>{setState(GS.CAMPAIGNINTRO);campaignIntroStart();}")
  p.wait_for_function("()=>{campaignIntroWarm();return ['cpov_male_hand','cin_cockpit_pov_magenta','cin_pilot_maverick_open','cin_terrain_jungle_loop','nbl_logo_0916'].map(k=>XART.rdy(k)).every(Boolean)&&HQ10_ART.radar.map(a=>XART.rdy(a.key)).every(Boolean)}")
  for name,js in [('cockpit-live',"campaignIntroVisual({pov:true},campaignIntro,1.2,cutsceneViewWidth(),VH)"),('opening-pilot',"campaignIntroVisual({comic:true,pilotLine:'resolve'},campaignIntro,2,cutsceneViewWidth(),VH)"),('title-flight',"campaignIntroFinale(campaignIntro,CAMPAIGN_INTRO_FINALE+1.7,cutsceneViewWidth(),VH)")]:
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);'+js+';window.__bofFit();}');p.screenshot(path=str(OUT/(name+'.png')))
  check('Opening instruments animate and the title uses the actual logo and selected pilot',p.evaluate("PT11_UI.radar.frame>0&&PT11_UI.title.logo&&PT11_UI.ship.pilot==='maverick'"))
  q=p.evaluate('''()=>{const old=state,clock=SM10.clock;SM10.clock=.25;const rows=[];for(const pk of OPN_ORDER){state=GS.LAUNCH;const a=XART.get('ship_'+pk);state=GS.PLAY;const b=XART.get('ship_'+pk);const ca=document.createElement('canvas');ca.width=a.width;ca.height=a.height;const g=ca.getContext('2d');g.drawImage(a,0,0);const before=ca.toDataURL();g.clearRect(0,0,ca.width,ca.height);g.drawImage(b,0,0);rows.push(before===ca.toDataURL());}SM10.clock=clock;state=old;return rows;}''')
  check('All nine neutral hulls use identical pixels across the launch-to-play handoff',all(q) and len(q)==9,q)
  check('No native page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)))
sys.exit(1 if report['failed'] or errors else 0)
