from pathlib import Path
import sys,json,subprocess,time,hashlib
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');T=W.parent/'Releases/BulletsOfFury-Windows-2026-11-06';Q=W/'native';Q.mkdir(exist_ok=True)
rows=[];errors=[];proc=None
def check(n,v):rows.append({'name':n,'pass':v});assert v,n;print('PASS',n,flush=True)
try:
 with sync_playwright()as pw:
  proc=subprocess.Popen([str(T/'Bullets of Fury.exe'),'--game','--qa-dir',str(Q),'--profile',str(Q/'profile'),'--debug-port','48876'])
  until=time.monotonic()+60
  while True:
   try:b=pw.chromium.connect_over_cdp('http://127.0.0.1:48876');break
   except Exception:
    if time.monotonic()>until:raise
    time.sleep(.25)
  p=b.contexts[0].pages[0];p.on('pageerror',lambda e:errors.append(str(e)));p.wait_for_function('window.__bofFrames>5',timeout=180000)
  check('packaged game starts fullscreen with high-quality rendering',p.evaluate("location.origin==='https://bof.coleforge.local'&&innerWidth===screen.width&&SS===2"))
  check('packaged source matches the repaired game',hashlib.sha256((T/'game/assets/game.js').read_bytes()).digest()==hashlib.sha256((R/'assets/game.js').read_bytes()).digest())
  check('new audio and page modules are loaded',p.evaluate("typeof AL116==='object'&&typeof SP116==='object'&&SP116_ART.pixelChecks===6748"))
  p.mouse.click(10,10);p.evaluate("()=>{Audio.stopMusic();Snd.prepare('machineGun');}");p.wait_for_function("BOF_AUDIO_LATENCY_1106.ready('machineGun')",timeout=20000,polling=50)
  audio=p.evaluate('''async()=>{const c=Snd._audioCtx();await c.resume();const tap=aq112Tap(),an=c.createAnalyser();tap.connect(an);an.fftSize=2048;const d=new Uint8Array(an.fftSize);let peak=0;Snd._last={};Snd.play('machineGun');
   for(let i=0;i<24;i++){await new Promise(r=>setTimeout(r,10));an.getByteTimeDomainData(d);for(const v of d)peak=Math.max(peak,Math.abs(v-128));}tap.disconnect(an);an.disconnect();return{peak,event:AL116.events.at(-1),errors:AL116.errors};}''')
  check('packaged SFX reaches the actual mixer output',audio['peak']>0 and not audio['errors'])
  p.evaluate("()=>{run.mode='campaign';run.pilot='axel';campaign.unlockedMax=1;openStageSelect(1,{});stateT=2;}");p.wait_for_timeout(300);p.keyboard.press('Enter');p.wait_for_timeout(2300)
  check('packaged campaign Enter deploys',p.evaluate("!campPause&&(state!==GS.STAGESEL||window.sselCommitted)"))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate("()=>{EA11.setup(5,'furious');run.pilot='axel';stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;Input.mouse.active=false;}")
  p.wait_for_function('stageLoadReady(5)&&furyShipReady()',timeout=180000,polling=100)
  p.evaluate("()=>{window.N116=spawnEnemy('s5frigate',worldWidth()/2,200,{});N116.hp=N116.maxhp=9999;}");p.keyboard.down('j');p.wait_for_timeout(2200);p.keyboard.up('j')
  check('packaged space combat uses the new pages without misses',p.evaluate('SP116.draws>10&&SP116.misses===0&&SP116.fallbacks===0&&Number.isFinite(N116.x)&&Number.isFinite(N116.y)'))
  p.screenshot(path=str(Q/'space-combat.png'))
  check('packaged flame revision is present',p.evaluate("()=>{run.stage=1;run.pilot='axel';run.weapon=4;run.wvars=run.wvars||[];run.wvars[4]='flamethrower';return flameDmg(5)===24&&flameReach(1)===184;}"))
  check('native game raises no page exceptions',not errors)
  (Q/'results.json').write_text(json.dumps({'checks':rows,'audio':audio,'errors':errors},indent=2),encoding='utf8');p.evaluate('window.close()');proc.wait(timeout=20);proc=None;b.close()
finally:
 if proc and proc.poll()is None:proc.terminate();proc.wait(timeout=15)
 (Q/'partial.json').write_text(json.dumps({'checks':rows,'errors':errors},indent=2),encoding='utf8')
