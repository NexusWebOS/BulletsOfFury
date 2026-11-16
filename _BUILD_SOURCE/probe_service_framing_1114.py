from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/service_framing_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
errors=[];cases=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(150000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?service-framing=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.mode='campaign';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');coopOn=false;beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();ls112Warm(2);return stageLoadInfo(2).ready&&ls112Keys(2).every(k=>XART.rdy(k));}',polling=50)
 p.evaluate("""()=>{bossActive=subBossActive=false;mapScroll=levelScrollRange();player.x=worldWidth()/2;player.y=VH*.78;BOFCinematicDirector.start(2,()=>{});window.terrainRects=[];const draw=ctx.drawImage;ctx.drawImage=function(im,...a){if(im===XART.get(LS112_ART.levels['2'].key)){const q=a.slice(-4),m=ctx.getTransform();terrainRects.push({left:m.a*q[0]+m.c*q[1]+m.e,top:m.b*q[0]+m.d*q[1]+m.f,right:m.a*(q[0]+q[2])+m.c*(q[1]+q[3])+m.e,bottom:m.b*(q[0]+q[2])+m.d*(q[1]+q[3])+m.f});}return draw.call(this,im,...a);};}""")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 for x in [40,340,640]:
  for index in [5,6,7,8,9]:
   for f in [0,.25,.5,.75,.99]:
    q=p.evaluate("""({x,index,f})=>{player.x=x;const s=BOFCinematicDirector.current;s.i=index;s.t=s.beats[index].duration*f;s.shown=s.beats[index].text.length;terrainRects=[];d1110Visual(s.beats[index],s);const frame=SL14.last.framing;return{...SL14.last,rects:terrainRects,screen:{left:12*SS,right:900*SS,top:12*SS,bottom:366*SS}};}""",{'x':x,'index':index,'f':f})
    cases.append(q)
    if x==340 and index in [5,7,8] and f==.5:
     (OUT/('corrected-'+q['mode']+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL()').split(',')[1]))
 # Keep the plane continuous through the warning-to-takeoff handoff.
 continuity=p.evaluate("""()=>{player.x=340;const s=BOFCinematicDirector.current;s.i=7;s.t=s.beats[7].duration;d1110Visual(s.beats[7],s);const before={...SL14.last.ship};s.i=8;s.t=0;d1110Visual(s.beats[8],s);return {before,after:SL14.last.ship};}""")
 b.close()
checks={'actualTerrainBlitsObserved':all(c['rects'] for c in cases),'allSidesCovered':all(any(r['left']<=c['screen']['left']+.01 and r['right']>=c['screen']['right']-.01 and r['top']<=c['screen']['top']+.01 and r['bottom']>=c['screen']['bottom']-.01 for r in c['rects']) for c in cases),'cameraInsideSource':all(c['framing']['visible']['left']>=3.99 and c['framing']['visible']['right']<=c['framing']['terrainW']-3.99 and c['framing']['visible']['top']>=3.99 and c['framing']['visible']['bottom']<=c['framing']['terrainH']-3.99 for c in cases),'noTakeoffJump':abs(continuity['before']['x']-continuity['after']['x'])<.01 and abs(continuity['before']['y']-continuity['after']['y'])<.01,'noErrors':not errors}
report={'checks':checks,'caseCount':len(cases),'cases':cases,'continuity':continuity,'errors':errors};(OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'checks':checks,'cases':len(cases),'continuity':continuity,'errors':errors},indent=2),flush=True)
assert all(checks.values()),checks
