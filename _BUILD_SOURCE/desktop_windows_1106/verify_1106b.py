from pathlib import Path
import subprocess,time,json,urllib.request,ctypes,ctypes.wintypes,sys,hashlib
from PIL import ImageGrab
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');T=W.parent/'Releases/BulletsOfFury-Windows-2026-11-06'
Q=W/('qa/desktop-v2-'+str(int(time.time())));Q.mkdir();checks=[];u=ctypes.windll.user32
u.SetProcessDPIAware()
def ck(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print('PASS'if value else'FAIL',name,str(data)[:150]if data is not None else'',flush=True)
def logs():
 p=Q/'desktop.jsonl';return [json.loads(s)for s in p.read_text().splitlines()]if p.exists()else[]
def wait(fn,seconds=30):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if fn():return True
  time.sleep(.12)
 return False
def click(h,x,y):
 point=ctypes.wintypes.POINT(x,y);u.ClientToScreen(h,ctypes.byref(point));u.SetForegroundWindow(h);u.SetCursorPos(point.x,point.y);time.sleep(.05);v=(y<<16)|x;u.SendMessageW(h,0x200,0,v);u.SendMessageW(h,0x201,1,v);u.SendMessageW(h,0x202,0,v);time.sleep(.35)
def client(h):
 r=ctypes.wintypes.RECT();u.GetClientRect(h,ctypes.byref(r));return r.right,r.bottom
def screen_click(h,x,y):
 w,hh=client(h);s=max(1,min(w//1024,hh//576));click(h,(w-1024*s)//2+x*s,(hh-576*s)//2+y*s)
def shot(h,name):
 u.SetForegroundWindow(h);time.sleep(.2);r=ctypes.wintypes.RECT();u.GetWindowRect(h,ctypes.byref(r));ImageGrab.grab(bbox=(r.left,r.top,r.right,r.bottom)).save(Q/(name+'.png'))
proc=None
try:
 proc=subprocess.Popen([str(T/'BOF Launcher.exe'),'--qa-dir',str(Q),'--profile',str(Q/'profile')],cwd=T)
 ck('Separate launcher EXE opens the graphical HQ',wait(lambda:any(r['name']=='doors-open'for r in logs())))
 h=u.FindWindowW(None,'Bullets of Fury - Fury HQ');assert h;shot(h,'launcher-home')
 screen_click(h,910,18);ck('Minimize button minimizes the actual native window',wait(lambda:u.IsIconic(h),3))
 u.ShowWindow(h,9);time.sleep(.25);screen_click(h,949,18);ck('Maximize button maximizes the actual native window',wait(lambda:u.IsZoomed(h),3));shot(h,'launcher-maximized')
 screen_click(h,949,18);ck('Restore button returns the original launcher size',wait(lambda:not u.IsZoomed(h)and client(h)==(1024,576),3))
 screen_click(h,986,18);proc.wait(timeout=20);proc=None;ck('X button closes the actual launcher process',True)
 # Save OFF: the direct game executable must still start fullscreen by default.
 (Q/'profile/launcher.json').write_text(json.dumps({'Fullscreen':False,'Sound':True,'QuickDoors':True}))
 port=48976;proc=subprocess.Popen([str(T/'Bullets of Fury.exe'),'--qa-dir',str(Q),'--profile',str(Q/'profile'),'--debug-port',str(port)],cwd=T)
 def endpoint():
  try:
   with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version',timeout=.3)as f:return bool(json.load(f))
  except:return False
 assert wait(endpoint,65),'native game endpoint'
 with sync_playwright()as pw:
  b=pw.chromium.connect_over_cdp(f'http://127.0.0.1:{port}');p=b.contexts[0].pages[0];errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.wait_for_function('window.__bofFrames>3',timeout=180000);p.mouse.click(3,3)
  row=[r for r in logs()if r['name']=='game-navigation'][-1]['data'];ck('Double-click game EXE starts fullscreen without --game, even with saved fullscreen OFF',row['fullscreen']and row['bounds']==row['screen'],row)
  ck('Direct startup uses original high-quality game assets with no GOD mode',p.evaluate('()=>SS===2&&!DBGT.god'))
  p.screenshot(path=str(Q/'direct-game.png'));p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
  p.evaluate(TRAP_RAF)
  colors=p.evaluate('''()=>{const rows=[];for(let i=0;i<PILOTS.length;i++){pilotIndex=i;ctx.setTransform(SS,0,0,SS,0,0);drawPilotBG(PILOTS[i].tint);const g=ctx.getImageData(0,0,cv.width,cv.height),colors=new Set();for(let n=0;n<g.data.length;n+=4)colors.add([g.data[n],g.data[n+1],g.data[n+2],g.data[n+3]].join(','));rows.push({pilot:PILOTS[i].key,expected:PILOT_SOLID_PALETTES_1106[PILOTS[i].key],unique:colors.size,rgb:[...colors][0]});}return rows;}''')
  ck('All nine pilot backgrounds are genuinely flat and have distinct 16-bit palette colors',len(colors)==9 and all(c['unique']==1 for c in colors)and len({c['rgb']for c in colors})==9,colors)
  p.evaluate("()=>{run.mode='arcade';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');setState('pilot');ctx.setTransform(SS,0,0,SS,0,0);drawPilot(0);}");time.sleep(.8);p.evaluate('()=>drawPilot(0)');p.screenshot(path=str(Q/'pilot-cole.png'))
  p.evaluate("()=>{pilotIndex=PILOTS.findIndex(p=>p.key==='freezer');drawPilot(0);}");time.sleep(.8);p.evaluate('()=>drawPilot(0)');p.screenshot(path=str(Q/'pilot-freezer.png'))
  p.evaluate("()=>{EA11.setup(1,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;DBGT.god=true;player.invuln=0;}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',polling=100,timeout=180000)
  collision=p.evaluate('''()=>{window.DA13_OFF=1;const out=[];for(const kind of ['s1bullet','mg','rzbSonic','ovSonic','sg10pressure','s1cannon'])for(const weapon of ['mg','beam','sonic','missile','helix']){
   enemies=[];boss=subBoss=null;bossActive=subBossActive=false;eBullets=[];pBullets=[];player.invuln=0;player.x=240;player.y=450;player.cd=0;run.weapon=weapon==='beam'?3:1;run.wlevel=4;player._beam=null;
   const q=eShootT(240,250,Math.PI/2,.01,kind,{silent:true});const atBirth={proof:q._weaponProof,can:enemyOrdnanceCanIntercept(q)};q._er26Art='fire';q._shootable=true;q.hp=1;
   let pb;if(weapon==='beam'){pShoot();pb=pBullets.find(b=>b.kind==='beam');if(!pb)throw Error('Real level-4 beam not created');pb.x=240;pb.y=450;}else{pb={kind:weapon,x:240,y:250,vx:0,vy:0,w:16,h:20,dmg:4,t:0,life:3,pierce:weapon==='helix',_p:0};pBullets.push(pb);}
   updatePlay(1/60);out.push({kind,weapon,atBirth,can:enemyOrdnanceCanIntercept(q),element:enemyOrdnanceElement(q),alive:!q.dead&&eBullets.includes(q),playerRoundSurvived:!pb.dead});
  }return out;}''')
  ck('MG bullets and sonic waves survive gun/laser/sonic/missile/helix overlaps even with elemental art and stale shootable flags',all(r['alive']and not r['can']and r['element']is None and r['atBirth']['proof']and not r['atBirth']['can']for r in collision),{'cases':len(collision)})
  missile=p.evaluate('''()=>{eBullets=[];pBullets=[];const q=eShootT(240,250,Math.PI/2,.01,'emissile',{silent:true});pBullets.push({kind:'mg',x:240,y:250,vx:0,vy:0,w:12,h:22,dmg:1,t:0,life:2});updatePlay(1/60);return {can:enemyOrdnanceCanIntercept(q),intercepted:!!q.dead};}''')
  ck('Actual physical missile interception remains functional',missile['can']and missile['intercepted'],missile)
  ck('Requested mouse bindings survive the desktop update',p.evaluate("()=>keybind.retina.includes('mouse2')&&keybind.bomb.includes(' ')&&keybind.multilock.includes('mouse3')"))
  ck('No browser runtime errors during the focused checks',not errors,errors)
  (Q/'game-results.json').write_text(json.dumps(dict(colors=colors,collision=collision,missile=missile,errors=errors),indent=2))
  p.evaluate('()=>window.close()');proc.wait(timeout=20);proc=None;b.close()
finally:
 if proc and proc.poll()is None:proc.terminate();proc.wait(timeout=15)
 (Q/'checks.json').write_text(json.dumps(checks,indent=2));(W/'qa/desktop-v2-latest.json').write_text(json.dumps({'directory':str(Q),'checks':checks},indent=2));print('EVIDENCE',Q,flush=True)
 if any(not r['passed']for r in checks):raise SystemExit(1)
