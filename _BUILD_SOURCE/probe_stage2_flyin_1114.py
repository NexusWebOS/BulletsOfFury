from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/stage2_flyin_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
errors=[];samples=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(120000)
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?stage2-flyin=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';coopOn=false;beginStage(2);warmStage(2);Input.clearTaps();}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("""()=>{BOFCinematicDirector.cancel();story=null;Input.clearTaps();Input.mouse.down=false;
  window.lavaTrace=[];const base=connectorSurface;connectorSurface=function(stage,join,width){const r=base.apply(this,arguments);if(stage===2&&state===GS.LAUNCH)lavaTrace.push({join,phase:drawLaunch._phase,speed:drawLaunch._spd,clock:efxClock,bed:{...LS112.clock.bed}});return r;};
  setState(GS.LAUNCH);drawLaunch._phase=undefined;player.invuln=99999;}""")
 # Native launch at fixed 60 Hz, including its normal countdown and PLAY handoff.
 for sec in range(28):
  for _ in range(4):
   err=p.evaluate(shoot.STEP,15)
   if err:errors.append(err)
   p.wait_for_timeout(5)
  q=p.evaluate('()=>({state,phase:drawLaunch._phase,dist:drawLaunch._dist,speed:drawLaunch._spd,join:VH-launchConnDy(),scroll:mapScroll,bed:{...LS112.clock.bed},player:{x:player.x,y:player.y},size:[cv.width,cv.height]})');samples.append(q)
  if sec in [0,1,3,6,9,12] or q['state']=='play':
   (OUT/('launch-'+str(sec)+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
  if q['state']=='play':break
 trace=p.evaluate('lavaTrace');material=p.evaluate('LS112_ART.materials[LS112_ART.levels["2"].material]')
 # Hold the animation frame fixed; only moving the launch join should move pixels.
 snapshots=[]
 for dy in [1000,935]:
  data=p.evaluate("""dy=>{setState(GS.LAUNCH);efxClock=5;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,VW,VH);connectorSurface(2,VH-dy,worldWidth());return cv.toDataURL();}""",dy)
  path=OUT/('fixed-clock-'+str(dy)+'.png');path.write_bytes(base64.b64decode(data.split(',')[1]));snapshots.append(path.name)
 # Other stages still use their original animation-clock motion.
 other=p.evaluate("""()=>{const out=[];for(const n of [3,4,7,8,9]){run.stage=n;efxClock=5;connectorSurface(n,-1000,worldWidth());out.push({stage:n,bed:{...LS112.clock.bed}});}return out;}""")
 b.close()
from PIL import Image,ImageChops
pixel_difference=ImageChops.difference(Image.open(OUT/snapshots[0]).convert('RGB'),Image.open(OUT/snapshots[1]).convert('RGB')).getbbox() is not None
checks={'reachedPlay':samples[-1]['state']=='play','launchMoved':len(trace)>60 and max(q['bed']['travel'] for q in trace)-min(q['bed']['travel'] for q in trace)>1000,'joinOwnsTravel':all(abs(q['bed']['travel']-(q['join']-512+q['clock']*12))<.0001 for q in trace),'fixedFramePixelsMove':pixel_difference,'noErrors':not errors}
report={'checks':checks,'samples':samples,'material':material,'trace':trace[::30],'otherStages':other,'errors':errors,'scope':'Actual Stage 2 launch checkpoint to PLAY; not a full-stage playthrough.'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'checks':checks,'end':samples[-1],'errors':errors},indent=2),flush=True)
assert all(checks.values()),checks
