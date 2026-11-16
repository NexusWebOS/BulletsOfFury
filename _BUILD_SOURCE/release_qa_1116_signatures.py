from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/signatures';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
prior=json.loads((R/'_shots/release_qa_1116/legacy/signature_specials_1011/report.json').read_text(encoding='utf8'));receipt=next(c['data']['receipt']for c in prior['checks']if c['name'].startswith('Stage X defeat permanently earns'))
checks=[];errors=[]
def ck(n,v,d=None):checks.append({'name':n,'ok':bool(v),'data':d});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8765/index.html?release-signatures=1116');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>{BOFOnline.submitScore=()=>{};}')
 def step(n):
  for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(1)
 for level in [1,2]:
  for pk in p.evaluate('PILOTS.map(p=>p.key)'):
   p.evaluate("q=>{BOFCinematicDirector.cancel();debugFight=null;coopOn=false;pilotIndex=PILOTS.findIndex(p=>p.key===q.pk);run.mode='arcade';FS11.receipt=q.level===2?q.receipt:null;startRun(1);BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;H3.release=false;AP10_X.intro=null;setState(GS.PLAY);stagePlan=[];enemies=[];spawnClock=1e9;special=null;player.invuln=1e8;player._spawnClearT=1e8;FS11.pending=null;FS11.boxes=[];}",{'pk':pk,'level':level,'receipt':receipt})
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&fs11ArtReady(run.pilot)}',polling=50);step(3);p.evaluate("()=>dropPowerup(player.x,player.y,'specialicon')");step(3)
   q=p.evaluate('({pilot:special?.pilot,dur:special?.dur,level:special?._fs11Level,name:ph8Values().name,enhanced:fs11Enhanced()})')
   ck(pk+' actual collected special uses '+str(level)+' tier and correct lifetime',q.get('pilot')==pk and q.get('level')==level and q.get('dur')==(20 if level==2 else 15),q)
   if pk in ['maverick','falva']:
    p.evaluate("pk=>{window.sig16Shot=null;const name=pk==='maverick'?'releaseHelix':'releaseRoller',fn=window[name];window.sig16Original=fn;window[name]=function(){const a=pk==='maverick'?pBullets:rollers,n=a.length,r=fn.apply(this,arguments),b=a[n];if(b)sig16Shot={kind:b.kind||'roller',damage:b.dmg,level:b._fs11Level||1,full:pk==='maverick'?b._isBall:b.full};return r;};}",pk)
    p.keyboard.down('j');step(330 if pk=='falva'else 144);p.keyboard.up('j');step(3)
    q=p.evaluate("pk=>{const name=pk==='maverick'?'releaseHelix':'releaseRoller';window[name]=sig16Original;return sig16Shot;}",pk);ck(pk+' tier'+str(level)+' real held/released charged attack fires',q and q.get('level')==level and q.get('full'),q)
   p.evaluate('()=>SC12.refresh()');p.screenshot(path=str(O/(pk+'-tier'+str(level)+'.jpg')),type='jpeg',quality=86)
 ck('no page or console errors',not errors,errors);b.close()
(O/'report.json').write_text(json.dumps({'scope':'Native base/MkII pickups for all9 pilots, actual hold/release for charged abilities. Enhanced profile is the validated receipt from this pass\'s real native StageX defeat/reward test. This does not assert natural human wins or certify every enemy personal signature.','checks':checks,'errors':errors},indent=2),encoding='utf8');sys.exit(any(not c['ok']for c in checks))
