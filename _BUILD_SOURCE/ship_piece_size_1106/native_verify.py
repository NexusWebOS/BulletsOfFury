from pathlib import Path
import json,time,hashlib,subprocess
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');T=W.parent/'Releases/BulletsOfFury-Windows-2026-11-06';Q=W/'native';Q.mkdir(exist_ok=True)
rows=[];errors=[];console=[];proc=None
def check(n,v):
 rows.append({'name':n,'passed':bool(v)});print('PASS'if v else'FAIL',n,flush=True);assert v,n
try:
 with sync_playwright()as pw:
  proc=subprocess.Popen([str(T/'Bullets of Fury.exe'),'--game','--qa-dir',str(Q),'--profile',str(Q/'profile'),'--debug-port','48877'])
  until=time.monotonic()+60
  while True:
   try:b=pw.chromium.connect_over_cdp('http://127.0.0.1:48877');break
   except Exception:
    if time.monotonic()>until:raise
    time.sleep(.25)
  p=b.contexts[0].pages[0];p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:console.append(m.text)if m.type=='error'else None)
  p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(10,10)
  check('updated native game opens in fullscreen/high quality',p.evaluate("location.origin==='https://bof.coleforge.local'&&innerWidth===screen.width&&SS===2"))
  check('both packaged scene sources match the repaired source',all(hashlib.sha256((T/'game'/n).read_bytes()).digest()==hashlib.sha256((R/n).read_bytes()).digest()for n in ['assets/game.js','assets/layered_stages_1102.js']))
  check('native Stage5 uses original backdrop; other layered stages remain active',p.evaluate("_levelCfg(5).master==='bg_stage05_loop_0923'&&!ls112Live(5)&&ls112Live(6)&&ls112Live(9)"))
  check('native kit uses the new 64px assembly cells',p.evaluate('FURY_PART_ORBIT_CELL===64&&SPACE_SHIP_SIZE===48'))
  p.evaluate("()=>{run.mode='arcade';run.pilot='axel';diffKey='furious';run.gravityShipReady=false;beginStage(5);DBGT.god=true;}")
  p.wait_for_function("drawLaunch._furyIntro?.t>5&&drawLaunch._furyIntro?.phase==='sky'",timeout=180000,polling=30)
  p.screenshot(path=str(Q/'ascent.png'))
  check('native ascent selects dedicated sky route',p.evaluate("drawLaunch._furyIntro.build&&!drawLaunch._furyIntro.space&&XART.rdy(STAGE6_TRANSITION_SKY)&&furyIntroDraw.toString().includes('stage5AscentBackgroundDraw')"))
  p.wait_for_function('state===GS.PLAY&&stageLoadReady(5)',timeout=180000,polling=50)
  p.screenshot(path=str(Q/'space.png'))
  check('native transformation completes into original starfield',p.evaluate("run.gravityShipReady&&furyShipReady()&&XART.rdy('bg_stage05_loop_0923')&&_levelCfg().master==='bg_stage05_loop_0923'"))
  check('original scenery parallax and optimized pages/audio remain active',p.evaluate("typeof l5FieldDraw==='function'&&typeof SP116==='object'&&typeof AL116==='object'&&FURY_STREAM.failed===0"))
  # Direct original sky/outbound draws at the same source clock must match exactly.
  check('Stage4 outbound uses the same original sky pixels',p.evaluate('''()=>{const stage=run.stage;run.stage=4;ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;
   try{stage5AscentBackgroundDraw(1234);const a=ctx.getImageData(0,0,VW*SS,VH*SS).data;s45Sky(1234,1,1);const z=ctx.getImageData(0,0,VW*SS,VH*SS).data;return a.every((v,i)=>v===z[i]);}finally{ctx.restore();run.stage=stage;}}'''))
  check('no native page exceptions or console errors',not errors and not console)
  (Q/'results.json').write_text(json.dumps({'checks':rows,'errors':errors,'consoleErrors':console},indent=2),encoding='utf8')
  p.evaluate('window.close()');proc.wait(timeout=20);proc=None;b.close()
finally:
 if proc and proc.poll()is None:proc.terminate();proc.wait(timeout=15)
 (Q/'partial.json').write_text(json.dumps({'checks':rows,'errors':errors,'consoleErrors':console},indent=2),encoding='utf8')
