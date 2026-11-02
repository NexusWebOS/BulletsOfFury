"""Native kamikaze pursuit, roll, damaged pixels and isolation regressions."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP,TRAP_RAF
from stage1_followup_fixture_1031 import SETUP
FIXTURE=SETUP.replace("route:'straight'","route:'straight',_s1Kamikaze:true,_s1LeadRank:0")
W=R/'_shots/kamikaze_orbit_1031';W.mkdir(exist_ok=True);port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:500]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,4):assert not p.evaluate(STEP,min(4,n-i));p.wait_for_timeout(1)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof KO31!=="undefined"');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(1)}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&XART.rdy(KO31_ART.key)}',timeout=180000)
  ck('All512 current authored roll/heading cells preload with fixed even canvas',p.evaluate('KO31_ART.frames===16&&KO31_ART.dirs===32&&KO31_ART.cell===128&&KO31_ART.pivot.every(n=>n===64)&&KO31_ART.tailSockets.every(a=>a.length>0)'))
  for mode in ['normal','hard','furious']:
   for moving in ([False,True,'diagonal']if mode=='furious'else[False,True]):
    initial=p.evaluate(FIXTURE,['s1jetdelta_b',mode]);p.evaluate("()=>{debugUnlocked=true;DBGT.god=true;Input.pollGamepad=()=>{};KO31.events=[];KO31.draws={hull:0,thruster:0};}");trace=[];saved=set()
    for f in range(0,1800,4):
     if moving:p.evaluate("f=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps();Input.keys.a=f%360<180;Input.keys.d=!Input.keys.a;}",f)
     if moving=='diagonal':p.evaluate("f=>{Input.keys.w=f%240<120;Input.keys.s=!Input.keys.w;}",f)
     step(p,4);q=p.evaluate("()=>({t:E.t,x:E.x,y:E.y,hp:E.hp,dead:!!E.dead,player:{x:player.x,y:player.y},phase:E._ko31?.mode,head:E._ko31?.head,roll:E._ko31?.roll,rate:E._ko31?.rollRate,frame:E._ko31?.rollFrame,thruster:E._ko31ThrusterFrame,distance:E._ko31?.distance,attempts:E._ko31?.attempts})");trace.append(q)
     for label,condition in [('orbit',q.get('phase')=='orbit'),('close',q.get('distance',999)<130),('strike',q.get('phase')=='strike')]:
      if condition and label not in saved:p.screenshot(path=str(W/(mode+('-moving-'if moving else'-still-')+label+'.png')));saved.add(label)
     if q['dead']:break
    p.evaluate("()=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;}");events=p.evaluate('KO31.events');runs.append(dict(mode=mode,moving=moving,initial=initial,trace=trace,events=events))
    tag=mode+(' diagonal target'if moving=='diagonal'else' moving target'if moving else' stationary target');rolls={q.get('frame')for q in trace};heads={round(q.get('head',0),1)for q in trace};far=[q['rate']for q in trace if q.get('distance',0)>330];near=[q['rate']for q in trace if q.get('distance',999)<140]
    ck(tag+' uses all authored roll poses and animated thrusters',len(rolls)==16 and len({q.get('thruster')for q in trace})>=6,dict(rolls=len(rolls)))
    ck(tag+' accelerates rolling near impact',bool(far)and bool(near)and max(near)>max(far)*1.8,dict(far=max(far)if far else None,near=max(near)if near else None))
    ck(tag+' banks into orbit and strike with native finite exit/contact',any(q['phase']=='orbit'for q in trace)and any(q['phase']=='strike'for q in trace)and len(heads)>10 and trace[-1]['dead'],dict(phases=sorted(set(q['phase']for q in trace)),last=trace[-1]))
    ck(tag+' preserves native kamikaze HP and fires no bullets',p.evaluate('E.maxhp')==initial['hp']and p.evaluate('S1A.events.filter(q=>q.event==="shot").length')==0)
  # Actual native pixels, not animation-key assertions.
  p.evaluate(FIXTURE,['s1jetdelta_b','hard']);step(p,180)
  pix=p.evaluate("()=>{window.koPixel=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,tan=0;for(let i=0;i<d.length;i+=4){if(d[i+3]<160)continue;if(d[i]>235&&d[i+1]>235&&d[i+2]>235)white++;if(d[i]>d[i+1]*1.2&&d[i+1]>d[i+2]*1.2&&d[i]>80)tan++;}return{white,tan};};const clean=koPixel();hitEnemy(E,.1);return{clean,hit:koPixel()};}");step(p,30);pix['expired']=p.evaluate('koPixel()');ck('Actual earth-camo pixels retain tan between native white hit and expiry',pix['clean']['tan']>200 and pix['hit']['white']>pix['clean']['white']+100 and pix['expired']['white']<pix['hit']['white']*.5,pix)
  n=p.evaluate('()=>{const old=ctx.rotate;let n=0;ctx.rotate=function(){n++;return old.apply(this,arguments)};try{drawEnemy(E)}finally{ctx.rotate=old}return n}');ck('Roll/body/exhaust use cell selection without canvas rotation',n==0,n)
  # Render does not advance a queued aircraft's birth clock.
  p.evaluate(FIXTURE,['s1jetdelta_b','normal']);v=p.evaluate('()=>{E._s1DelayFrames=5;drawEnemy(E);drawEnemy(E);return E._s1DelayFrames}');ck('Repeated drawing does not spend native ripple delay',v==5,v)
  p.evaluate(SETUP,['s1jetdelta_b','normal']);step(p,3);ck('Ordinary Strike Fighter keeps its existing palette/flight owner',p.evaluate('!E._ko31&&E._air13RenderedKey===S1A_ART.strike_heading.key'))
  p.evaluate(FIXTURE,['s1jetdelta_b','furious']);p.evaluate("()=>{spawnEnemy=window.s1bProbeSpawn;window.G=[E,...[.25,.75].map((u,i)=>spawnEnemy('s1jetdelta_b',worldWidth()*u,viewTopY()-100,{_s1Kamikaze:true,_s1LeadRank:i+1,_s1DelayFrames:(i+1)*3}))];spawnEnemy=()=>null;}")
  group=[];closest=999;maxOverlap=0
  for f in range(0,600,4):
   step(p,4);group.append(p.evaluate('G.map(e=>({x:e.x,y:e.y,dead:e.dead,hp:e.hp,phase:e._ko31?.mode,head:e._ko31?.head,roll:e._ko31?.rollFrame}))'))
   from math import hypot
   distance=min(hypot(a['x']-b['x'],a['y']-b['y'])for i,a in enumerate(group[-1])for b in group[-1][i+1:]if not a['dead']and not b['dead'])
   if distance<closest:
    closest=distance
    if distance<100:
     overlap=p.evaluate("()=>{let max=0;for(let a=0;a<G.length;a++)for(let b=a+1;b<G.length;b++){if(Math.hypot(G[a].x-G[b].x,G[a].y-G[b].y)>125)continue;const x=(G[a].x+G[b].x)/2,y=(G[a].y+G[b].y)/2;const masks=[G[a],G[b]].map(e=>{ctx.save();ctx.setTransform(1,0,0,1,cv.width/2-x,cv.height/2-y);ctx.globalAlpha=1;ctx.clearRect(x-cv.width/2,y-cv.height/2,cv.width,cv.height);ko31Blit(e,'#ffffff');ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data});let both=0,n=0,m=0;for(let i=3;i<masks[0].length;i+=4){const A=masks[0][i-3]>180&&masks[0][i-2]>180&&masks[0][i-1]>180,B=masks[1][i-3]>180&&masks[1][i-2]>180&&masks[1][i-1]>180;if(A)n++;if(B)m++;if(A&&B)both++;}max=Math.max(max,both/Math.max(1,Math.min(n,m)));}drawWorld(0);return max;}")
     maxOverlap=max(maxOverlap,overlap);p.screenshot(path=str(W/'native-wave-closest-pass.png'))

  ck('Three-plane wave keeps authored rolling pursuit without extra bullets',all(any(q[i].get('phase')=='orbit'for q in group)for i in range(3))and p.evaluate('S1A.events.filter(q=>q.event==="shot").length')==0)
  from math import hypot
  clearance=min(hypot(a['x']-b['x'],a['y']-b['y'])for row in group for i,a in enumerate(row)for b in row[i+1:]if not a['dead']and not b['dead'])
  ck('Pursuit wave keeps fuselages apart and native hulls readable',clearance>35 and maxOverlap<.45,dict(clearance=clearance,maxOpaqueOverlap=maxOverlap))
  p.screenshot(path=str(W/'native-three-plane-wave.png'));(W/'group-paths.json').write_text(json.dumps(group))
  p.evaluate(FIXTURE,['s1jetdelta_b','furious']);initialLives=p.evaluate('run.lives');p.evaluate('()=>{DBGT.god=false;player.invuln=0;}');contact=False
  for f in range(0,720,4):
   step(p,4)
   if p.evaluate('player.dead||run.lives<'+str(initialLives)):contact=True;p.screenshot(path=str(W/'native-ram-contact.png'));break
  ck('Unprotected player takes the native ram hit',contact);p.evaluate('DBGT.god=true')
  ck('No browser/page/render errors',not errors,errors);b.close()
finally:stop();(W/'native-events.json').write_text(json.dumps(runs,indent=2))
print('RESULT',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks)
