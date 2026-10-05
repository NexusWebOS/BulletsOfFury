"""Actual keyboard password entry and immediate boss launches in Chromium."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/password_routes_1004d';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>{Storage.prototype.setItem=function(){};Storage.prototype.removeItem=function(){};ht27Stop();debugFight=null;coopOn=false;diffKey="furious";DIFF=DIFFS.furious;pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");}')
  codes={'FURY':1,'IRON':2,'DAM5':3,'STRM':4,'ORBT':5,'TURB':6,'SEWR':7,'DETH':8,'RIFT9':9,'XHARR':6,'XREBEL':6,'HARR6':6,'REBEL6':6}
  for code,stage in codes.items():
   p.evaluate('()=>{_pwTyped=[];pwInput="";setState(GS.PASSWORD);Input.clearTaps?.();ctx.setTransform(SS,0,0,SS,0,0);drawPassword(0);}')
   p.keyboard.type(code,delay=15);p.evaluate('()=>drawPassword(1/60)')
   ck(p.evaluate('(c)=>pwInput===c',code),code+' fits and renders through real keyboard entry')
   if code in ['HARR6','REBEL6']:shot(p,'password-'+code)
   p.keyboard.press('Enter');p.evaluate('()=>drawPassword(1/60)')
   ck(p.evaluate('(s)=>state===GS.DIFF&&passwordDifficulty&&PENDING_STAGE===s&&run.mode==="arcade"',stage),code+' routes to difficulty with the right stage')
   if code in ['HARR6','REBEL6','XHARR','XREBEL']:
    p.evaluate('()=>startRun(PENDING_STAGE)')
    target='rebelsquad' if code in ['REBEL6','XREBEL'] else 'warhive';x=code.startswith('X')
    ck(p.evaluate('([kind,x])=>state===GS.PLAY&&bossActive&&boss.kind===kind&&!!run._gp4StageX===x&&subBossDone&&s6Wing.ships.length===4',[target,x]),code+' immediately launches the correct full fight and five-ship wing')
    frames(p,140);p.evaluate('()=>{rg4Warm();gp4AceWarm();}');p.wait_for_timeout(500);frames(p,20);shot(p,'fight-'+code)
    ck(p.evaluate('()=>stagePlan.length===0&&waveIdx===9999&&s6Wing.fakeDone&&!s6Opening'),code+' skips normal level waves and route choice')
  # Selecting the ordinary Stage 6 code after any fight still starts the regular stage.
  p.evaluate('()=>{setState(GS.PASSWORD);pwInput="TURB";submitPassword();startRun(PENDING_STAGE);}')
  ck(p.evaluate('()=>!GP4.routeReady&&!run._gp4StageX&&stagePlan.length>0&&!bossActive'),'ordinary Stage 6 password retains its normal mission opening')
  ck(not errors,'zero page and console errors');b.close()
finally:stop()
data={'checks':checks,'errors':errors,'passwords':codes};(O/'checks.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('RESULT',sum(c['ok'] for c in checks),'/',len(checks));sys.exit(bool(errors) or any(not c['ok'] for c in checks))
