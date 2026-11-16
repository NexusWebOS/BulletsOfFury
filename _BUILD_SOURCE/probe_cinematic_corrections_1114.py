import sys,json,base64
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=Path(__file__).resolve().parents[1]/'_shots/opening_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
errors=[];seen=[];shots=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?corrections-review=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
 p.evaluate("""()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(5);BAL7.setup({stage:5,kind:'chromehammer',pilot:'cole',diff:'normal',seconds:120,fire:false});hf17Warm();h3Warm();furyShipWarm();}""")
 p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&hf17Warm()&&furyShipReady()&&XART.rdy("h3_earth");}',polling=50)
 p.evaluate("""()=>{window.rejectedComicDraws=0;const old=cb1110ChronosDraw;cb1110ChronosDraw=function(){rejectedComicDraws++;return old.apply(this,arguments)};BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];B.x=worldWidth()/2;B.y=VH*.31;B.enter=B.dead=B._noHit=false;B._hammer.state='storm_raise';B._hammer.t=2;player.x=B.x;player.y=VH*.81;player.dead=player.out=false;player.invuln=99999;camX=clamp(player.x-VW/2,0,worldWidth()-VW);eBullets=[];pBullets=[];enemies=[];l5Rocks=[];l5RockT=999;stagePlan=[];B.hp=0;bossDie();window.__bofFit?.();SC12.refresh();}""")
 identity=p.evaluate('h3EndingDraw===CB1110.base.endingDraw&&hf17Warm===CB1110.base.warm')
 for i in range(420):
  err=p.evaluate(shoot.STEP,5)
  if err:errors.append(err)
  q=p.evaluate('()=>({phase:H3.ending?.hf17?.phase,t:H3.ending?.hf17?.t,after:H3.ending?.phase,state})')
  phase=q.get('phase')
  if phase not in seen:
   seen.append(phase);name='restored-stage5-'+str(phase)+'.png'
   (OUT/name).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]));shots.append(name)
  if phase=='burst' and .7<q.get('t',0)<.8:
   (OUT/'restored-stage5-fragments.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
  if phase=='after':break
  p.wait_for_timeout(4)
 result=p.evaluate('()=>({comicDraws:rejectedComicDraws,events:HF17.events,render:HF17.last,draws:HF17.draws,score:run.score})')
 # Independently show the native reentry without waiting through all radio holds.
 p.evaluate("()=>{const e=H3.ending;e.hf17.phase='after';e.phase='descent';e.t=28;e.homeAge=3;e.descent=3;e.cheer=H3_CHEERS.length;h3EndingDraw();h3Warm();}")
 p.wait_for_function('()=>H3_ART.slice(5).every(k=>XART.rdy("h3_"+k))&&furyShipReady()',polling=50)
 (OUT/'restored-stage5-earth.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
 p.evaluate("()=>{const e=H3.ending;e.descent=9.79;h3EndingTick(1/30);}")
 continuation=p.evaluate('H3.ending===null&&state===GS.STAGECLEAR')
 # Verify a real gutter passes through the viewport during the strip pan.
 p.evaluate("()=>{FURY14.preview('stage1','cole');}")
 p.wait_for_function('()=>fury14Ready(BOFCinematicDirector.current.d1110Keys)')
 p.evaluate("()=>{const s=BOFCinematicDirector.current;s.i=1;s.t=.825;s.shown=s.beats[1].text.length;d1110Visual(s.beats[1],s);}")
 (OUT/'comic-strip-mid-pan.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
 pan=p.evaluate('FIXC14.last')
 b.close()
report={'restoredNativeRenderer':identity,'phases':seen,'result':result,'nativeStageClear':continuation,'midPan':pan,'errors':errors,'screenshots':shots,'scope':'Native death checkpoint through normal phase clocks; reentry inspected at a selected time, not a full campaign playthrough.'}
(OUT/'corrections.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
assert identity and continuation and not errors
assert seen==['drain','pulse','lock','missile','engulf','burst','after'],seen
assert result['comicDraws']==0
assert 400<pan['camera']<540 and pan['detachedPortrait']==False
assert len([x for x in result['events'] if x['event']=='core-impact'])==1
