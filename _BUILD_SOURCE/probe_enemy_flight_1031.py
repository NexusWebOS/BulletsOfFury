"""Native renderer/hit, lock, cancellation and ordnance contracts for R46."""
from pathlib import Path
import sys,json,ast,http.server,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,TRAP_RAF
W=R/'_shots/enemy_flight_1031/probe';W.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if passed else'FAIL',name,flush=True)
port,stop=serve(str(R))
PIXELS=r'''(compare=false)=>{
 const e=E;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(e);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;
 let white=0,ink=0,difference=0;for(let i=0;i<a.length;i+=4){if(a[i+3]>80&&a[i]+a[i+1]+a[i+2]>24){ink++;if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;}if(compare&&window.cleanPixels&&(a[i]!==cleanPixels[i]||a[i+1]!==cleanPixels[i+1]||a[i+2]!==cleanPixels[i+2]||a[i+3]!==cleanPixels[i+3]))difference++;}if(!compare)window.cleanPixels=a;return {white,ink,difference,flash:e.flash};
}'''
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  for stage in range(4,10):
   p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('(s)=>EA11.setup(s,"hard")',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000)
   p.evaluate('()=>{window.probePixels='+PIXELS+';}')
   specs=json.loads((R/f'_shots/enemy_flight_1031/before/stage{stage}-specs.json').read_text());seen=set()
   for spec in specs:
    key=spec['type']+'-'+str(spec['opt'].get('_modWeapon',''))
    if key in seen or spec['type']in['barrelx','s4barrel','cometsm']:continue
    seen.add(key);p.evaluate('s=>{EA11.case(s);bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;}',spec)
    # Native motion/entry is allowed to settle. Coordinates only center the QA crop.
    p.evaluate('()=>{for(let i=0;i<100;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=230;camX=E.x-VW/2;drawWorld(0);}')
    initial=p.evaluate('()=>({hp:E.hp,dead:E.dead,noHit:E._noHit,shield:E._esh,flash:E.flash})')
    if initial['dead']:ck(f'S{stage} {key} finite native exit',True,initial);continue
    clean=p.evaluate('probePixels()');p.evaluate('hitEnemy(E,.01)');hit=p.evaluate('probePixels(true)')
    difference=hit['difference']
    native=p.evaluate('()=>({hp:E.hp,flash:E.flash,shield:E._esh,noHit:E._noHit})')
    # Shield/entry gates can legitimately absorb the real impact. Verify the
    # shared markHit route separately without bypassing the combat gate.
    if difference<16:
     p.evaluate('markHit(E,.12)');hit=p.evaluate('probePixels(true)');marked=True
    else:marked=False
    p.evaluate('()=>{for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=230;}');expired=p.evaluate('probePixels(true)')
    ck(f'S{stage} {key} native pixels / hit / expiry',clean['ink']>50 and hit['difference']>32 and hit['flash']>0 and expired['flash']<=0 and expired['white']<hit['white'],dict(clean=clean,hit=hit,expired=expired,native=native,markHitOnly=marked,difference=difference))
   # A real physical round remains outside the live list while its Retina warns.
   spec=next((s for s in specs if s['type']in['s4rocket','s5satellite','s6lancer','cp22drone','s8hunter','s9gunship']),None)
   if spec:
    p.evaluate('s=>{EA11.case(s);E.x=worldWidth()/2;E.y=180;bossWarned=false;}',spec)
    q=p.evaluate('()=>{window.testRound=eShootT(E.x,E.y,Math.PI/2,170,"emissile",{owner:E});return {held:R46.pending.has(testRound),live:eBullets.includes(testRound),lock:playerLocks.some(L=>L.src===E),intercept:enemyOrdnanceCanIntercept(testRound)};}')
    ck(f'S{stage} physical missile native Retina before release',q['held']and not q['live']and q['lock']and q['intercept'],q)
    p.evaluate('()=>{for(let i=0;i<60;i++){updatePlayerLocks(1/60);updateEffects(1/60);}}')
    q=p.evaluate('()=>({live:eBullets.includes(testRound),held:R46.pending.has(testRound),lock:testRound._lockId,finite:Number.isFinite(testRound.x+testRound.y+testRound.vx+testRound.vy)})')
    ck(f'S{stage} physical missile releases with original round',q['live']and not q['held']and q['finite']and q.get('lock'),q)
    q=p.evaluate('()=>{const b=eShootT(E.x,E.y,Math.PI/2,170,"emissile",{owner:E});killEnemy(E);return {pending:R46.pending.has(b),lock:playerLocks.some(L=>L.src===E),dead:b.dead};}')
    ck(f'S{stage} launcher defeat cancels pending warning/round',not q['pending']and not q['lock']and q['dead'],q)
   p.close()
  ck('No page or console errors',not errors,errors);b.close()
finally:
 (W/'checks.json').write_text(json.dumps(checks,indent=2));(W/'errors.json').write_text(json.dumps(errors,indent=2));stop()
sys.exit(0 if all(q['passed']for q in checks)else 1)
