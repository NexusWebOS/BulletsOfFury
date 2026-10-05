"""Keyboard password flow and deployed playable review in real Chromium."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_1005'
port,stop=sh.serve(str(R));report={'checks':[],'errors':[]}
def ck(v,n):report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def errors(p):
 p.on('pageerror',lambda e:report['errors'].append(str(e)))
 p.on('console',lambda m:report['errors'].append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950});errors(p)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();debugFight=null;coopOn=false;diffKey="furious";DIFF=DIFFS.furious;pilotIndex=0;}')
  for code in p.evaluate('()=>Object.keys(ON5_CODES)'):
   p.evaluate('()=>{_pwTyped=[];pwInput="";setState(GS.PASSWORD);Input.clearTaps?.();drawPassword(0);}')
   p.keyboard.type(code,delay=8);p.evaluate('()=>drawPassword(1/60)')
   ck(p.evaluate('(c)=>pwInput===c',code),code+' accepted by actual keyboard password input')
   p.keyboard.press('Enter');p.evaluate('()=>drawPassword(1/60)')
   ck(p.evaluate('(c)=>state===GS.DIFF&&ON5.pending?.code===c&&PENDING_STAGE===ON5_CODES[c].stage',code),code+' retains shortcut through difficulty selection')
   if code in ['FINAL1','FINAL2','FINAL3','MINI8','KNIGHT']:
    p.keyboard.press('Enter');p.evaluate('()=>{for(let i=0;i<30&&state===GS.DIFF;i++)drawDiff(1/60);}')
    ck(p.evaluate('()=>state===GS.PILOT&&!!ON5.pending'),'native difficulty confirmation keeps '+code)
    p.evaluate('()=>{pilotIndex=0;stateT=.5;drawPilot(1/60);}')
    p.keyboard.press('Enter');p.evaluate('()=>{for(let i=0;i<120&&state===GS.PILOT;i++){stateT+=1/60;drawPilot(1/60);}}')
    ck(p.evaluate('(c)=>state===GS.PLAY&&ON5.pending===null&&run.stage===ON5_CODES[c].stage&&!!(ON5_CODES[c].role==="boss"?boss:subBoss)',code),'native pilot deployment launches '+code)
  p.goto(f'http://127.0.0.1:{port}/_shots/overnight_1005/review.html',timeout=120000)
  for code in ['REBEL6','FINAL1','FINAL2','FINAL3','KNIGHT','ACE8','HAMA']:
   p.locator('[data-code="'+code+'"]').click()
   p.wait_for_function('()=>document.querySelector("#status").textContent==="Practice ready."',timeout=120000)
   f=p.frame_locator('#arena');frame=p.frames[1]
   ck(frame.evaluate('(c)=>state===GS.PLAY&&bossActive&&run.stage===ON5_CODES[c]?.stage||state===GS.PLAY&&bossActive&&["REBEL6","HAMA"].includes(c)',code),'review button launches live '+code)
   frame.evaluate(sh.TRAP_RAF)
   frame.evaluate('()=>r30Warm()');frame.wait_for_function('()=>ON5_ART.knight.every(a=>XART.rdy(a.key))',timeout=120000,polling=50)
   for i in range(0,120,20):frame.evaluate('()=>{for(let i=0;i<20;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(8)
   ck(frame.evaluate('()=>{const key="overnight-practice-proof";localStorage.setItem(key,"write");return localStorage.getItem(key)===null;}'),'practice '+code+' blocks campaign save writes')
  ck(not report['errors'],'zero page and console errors in keyboard flow and review');b.close()
finally:stop();(O/'review-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if all(q['ok'] for q in report['checks']) and not report['errors'] else 1)
