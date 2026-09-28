"""Verify password-session lifetime and campaign-slot Cole unlocks in Chromium."""
import http.server,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(sh.GAME)
OUT=Path(sh.GAME)/'_shots/repair_0927';OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(str(ROOT));errors=[];result={}
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  context=browser.new_context();p=context.new_page();p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  result['session']=p.evaluate("""()=>{
   const cole=PILOTS.find(p=>p.key==='cole'),bootLocked=isPilotLocked(cole);
   pwInput='';for(const c of 'Cole4u')pwKey(c.toUpperCase());submitPassword();
   const password=!isPilotLocked(cole);pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.mode='campaign';startRun(1);
   const fresh=!isPilotLocked(cole),saved=campSnapshot();campWriteSlot(23);
   const old={...saved,unlocks:{cole:false}};campApply(old);const olderSave=!isPilotLocked(cole);
   setState(GS.PLAY);player.dead=false;player.invuln=0;run.shield=0;playerHit();const death=!isPilotLocked(cole);
   triggerGameOver();const gameOver=!isPilotLocked(cole);
   run.mode='campaign';startRun(1);return{bootLocked,password,fresh,olderSave,death,gameOver,newRun:!isPilotLocked(cole),saved:saved.unlocks.cole};
  }""")
  p.reload();p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  result['restart']=p.evaluate("""()=>{const cole=PILOTS.find(p=>p.key==='cole'),locked=isPilotLocked(cole),saved=campReadSlot(23);campApply(saved);const restored=!isPilotLocked(cole);campApply({...saved,unlocks:{cole:false}});const otherSaveLocked=isPilotLocked(cole);localStorage.removeItem(campSlotKey(23));return{locked,restored,otherSaveLocked};}""")
  result['errors']=errors;browser.close()
finally:stop()
(OUT/'cole-session-probe.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
assert not errors,errors
assert all(result['session'].values()) and all(result['restart'].values()),result
