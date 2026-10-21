from pathlib import Path
import sys,json,http.server,argparse,hashlib
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot,probe_tutorial_1015 as old
ap=argparse.ArgumentParser();ap.add_argument('--browser',default='msedge');a=ap.parse_args();O=R/'_shots/holoscan_1021';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,ok=bool(v),data=d));print(('PASS ' if v else 'FAIL ')+n,flush=True);(O/(a.browser+'-checks.json')).write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def step(p,n=2):return p.evaluate(shoot.STEP,n)
def card(p,age=5):
 p.evaluate('age=>{for(const k in Input.keys)Input.keys[k]=false;Input.clearTaps();Input.mouse.down=false;TD=null;TUT.i=TUT_LESSONS.findIndex(d=>d.id==="bob_card")-1;tutNext();TUT.typed=10000;TUT.L.age=age;}',age);step(p,3)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.firefox.launch() if a.browser=='firefox' else pw.chromium.launch(channel=a.browser)
  p=br.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(old.SETUP,dict(pilot='cole',mode='arcade',clear=True));p.evaluate('startRun(1)');step(p,60);p.wait_for_function('XART.rdy("ic20_neutral")');step(p,30);p.evaluate('Input.injectTap("j")');step(p,5)
  p.wait_for_function('BOFINSTRUCTOR.artReady&&BOFHOLOSCAN.ready');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  for i in range(120):
   step(p,30)
   if p.evaluate('state===GS.PLAY&&TUT?.L?.def.id==="move"'):break
   p.wait_for_timeout(10)
  ck('Actual tutorial entered',p.evaluate('state===GS.PLAY&&TUT?.L?.def.id==="move"'))
  card(p,.5);ck('Scanning gates deployment and uses selected frame',p.locator('.hs-deploy').is_disabled() and p.evaluate('HS21.visible&&HS21.root.hidden===false&&BOFHOLOSCAN.ready'))
  p.evaluate('document.querySelector(".hs-deploy").click()');step(p,10);ck('Early confirm cannot skip native scan gate',p.evaluate('TUT.L.def.id==="bob_card"'))
  card(p);ck('Actual shared module stats shown',p.evaluate('()=>{const d=BOFHOLOSCAN.stats;return d.total===440&&d.core===240&&d.cannon===110&&d.missile===90&&d.coreMissile===2&&document.querySelector("[data-stat=total]").textContent==="440"}'))
  sizes=[(1920,1080),(1366,768),(768,1024),(390,844),(320,568),(844,390)] if a.browser=='msedge' else [(1366,768),(390,844)]
  for width,height in sizes:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('__bofFit()');step(p,3);p.wait_for_timeout(80)
   for part in range(4):
    p.evaluate('i=>{TUT.L.sel=i;HS21.dirty=true;}',part);step(p,2)
    d=p.evaluate('''()=>{const r=HS21.root.getBoundingClientRect(),s=HS21.root.querySelector('.hs-shell'),bad=[];for(const e of HS21.root.querySelectorAll('h1,h2,p,dt,dd,.hs-objective,button')){const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;if(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2)bad.push({text:e.textContent,w:e.clientWidth,sw:e.scrollWidth,h:e.clientHeight,sh:e.scrollHeight});}return{root:[r.x,r.y,r.right,r.bottom],bad,wide:s.scrollWidth>s.clientWidth+2,bodyWide:document.documentElement.scrollWidth>innerWidth+1,details:[...HS21.root.querySelectorAll('.hs-detail')].filter(e=>e.getBoundingClientRect().height>0).length,part:IC20.cardFrame.part,font:document.fonts.check('16px Holoscan'),canvases:[...HS21.root.querySelectorAll('canvas')].every(c=>c.width%2===0&&c.height%2===0)};}''')
    ck(f'{width}x{height} {part} text/frame/part fit',not d['bad'] and not d['wide'] and not d['bodyWide'] and d['root'][0]>=0 and d['root'][3]<=height+1 and d['font'] and d['canvases'] and d['details']==(1 if width<=900 else 3),d)
    if part==0 or width==390:p.screenshot(path=str(O/f'{a.browser}-{width}-{height}-part{part}.png'))
  p.set_viewport_size(dict(width=1366,height=768));card(p)
  frames=[]
  for f in [0,8,16,24]:
   data=p.evaluate('f=>{TUT.L.yaw=f;HS21.dirty=true;ic20CardDraw(TUT.L);return document.querySelector(".hs-model").toDataURL()}',f);frames.append(hashlib.sha256(data.encode()).hexdigest())
  ck('Authored front side rear frames visibly differ',len(set(frames))==4,frames)
  bounds=p.evaluate('''()=>{const bad=[];let inspected=0;for(let sel=0;sel<4;sel++){TUT.L.sel=sel;for(let f=0;f<32;f++){TUT.L.yaw=f;HS21.dirty=true;ic20CardDraw(TUT.L);for(const c of HS21.root.querySelectorAll('[data-model]')){if(!c.getBoundingClientRect().height)continue;const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let edges=0;for(let x=0;x<c.width;x++){if(d[x*4+3]>0||d[((c.height-1)*c.width+x)*4+3]>0)edges++;}for(let y=0;y<c.height;y++){if(d[(y*c.width)*4+3]>0||d[(y*c.width+c.width-1)*4+3]>0)edges++;}if(edges)bad.push({part:c.dataset.model,frame:f,edges,w:c.width,h:c.height});inspected++;}}}return{inspected,bad};}''')
  ck('All 128 authored poses stay clear of thumbnail and detail edges',not bounds['bad'] and bounds['inspected']>=128,bounds)
  p.evaluate('TUT.L.sel=0;Input.injectTap("s")');step(p,2);ck('Native down selects missile pod',p.evaluate('TUT.L.sel===1&&IC20.cardFrame.part==="missile"'))
  yaw=p.evaluate('TUT.L.yaw');p.evaluate('Input.injectTap("d")');step(p,2);delta=(p.evaluate('TUT.L.yaw')-yaw+32)%32;ck('Native right turns actual bank across the 31-to-0 seam',1<delta<3,dict(delta=delta))
  p.locator('[data-part="2"]').click();step(p,2);ck('Pointer selects actual cannon',p.evaluate('TUT.L.sel===2&&IC20.cardFrame.part==="cannon"'))
  p.locator('.hs-auto').click();step(p,3);row=p.evaluate('({yaw:TUT.L.yaw,draws:HS21.draws})');step(p,90);ck('Auto stop freezes art without freezing readiness clock',p.evaluate('Math.abs(TUT.L.yaw-'+str(row['yaw'])+')<.0001&&HS21.draws-'+str(row['draws'])+'<=1'),p.evaluate('({yaw:TUT.L.yaw,draws:HS21.draws})'))
  box=p.locator('.hs-model').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;oldyaw=p.evaluate('TUT.L.yaw');p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+88,y,steps=6);p.mouse.up();step(p,2);ck('Dragging rotates authored view',abs(p.evaluate('TUT.L.yaw')-oldyaw)>3)
  p.locator('.hs-full').click();step(p,2);ck('Full unit button restores exploded assembly selection',p.evaluate('TUT.L.sel===0'))
  stocks=p.evaluate('({missiles:run.bombs,lives:run.lives,shots:pBullets.length,enemies:enemies.length,timer:stageTimer})');step(p,180);ck('Dossier consumes no ammo or combat stage time',stocks==p.evaluate('({missiles:run.bombs,lives:run.lives,shots:pBullets.length,enemies:enemies.length,timer:stageTimer})'))
  p.locator('.hs-pause').click();step(p,2);ck('Native pause hides modal',p.evaluate('state==="paused"&&!HS21.visible&&HS21.root.hidden'))
  step(p,65);p.evaluate('Input.injectTap("j")');step(p,3);ck('Native resume restores same dossier and rotation preference',p.evaluate('state===GS.PLAY&&TUT.L.def.id==="bob_card"&&HS21.visible&&!HS21.rotating'))
  if a.browser=='msedge':
   p.keyboard.press('f');p.wait_for_timeout(150);step(p,2);ck('Fullscreen keeps DOM dossier in the fullscreen tree',p.evaluate('()=>{const e=document.fullscreenElement;return HS21.visible&&(!e||e.contains(HS21.root))}'))
   p.keyboard.press('f');p.wait_for_timeout(100);step(p,2)
  p.locator('.hs-deploy').click();step(p,150);ck('Pointer deploy uses native lesson completion and releases modal buffers',p.evaluate('TUT.L.def.id==="exam"&&!HS21.visible&&HS21.root.hidden&&[...HS21.root.querySelectorAll("canvas")].every(c=>c.width===2&&c.height===2)'))
  # Inspect the real modular spawn/damage boundary, not a picture's printed stats.
  out=p.evaluate('''()=>{tutClearField();const G=bob20Spawn(TUT.L,'exam');TUT.L.bob=G;const hp=Object.fromEntries(Object.entries(G.parts).map(([id,e])=>[id,e.hp]));for(const id of ['missile','cannon'])killEnemy(G.parts[id]);const e=G.parts.core;_dmgSrc='missile';_dmgBullet={kind:'missile'};const before=e.hp;hitEnemy(e,10);_dmgSrc=null;_dmgBullet=null;return{hp,loss:before-e.hp,coreTarget:bob20Pods(G)===false};}''')
  ck('Dossier HP and missile bonus match actual combat',out['hp']==dict(missile=90,cannon=110,core=240) and out['loss']==20 and out['coreTarget'],out)
  card(p);p.emulate_media(reduced_motion='reduce');HS=p.evaluate('HS21.reduced.matches');row=p.evaluate('TUT.L.yaw');step(p,60);ck('Reduced motion stops automatic turntable',HS and abs(p.evaluate('TUT.L.yaw')-row)<.001);p.evaluate('Input.injectTap("d")');step(p,2);ck('Reduced motion retains manual turning',abs(p.evaluate('TUT.L.yaw')-row)>1);p.emulate_media(reduced_motion='no-preference')
  p.evaluate('tutFinish(false)');step(p,3);ck('Tutorial exit removes modal and returns normal flow',p.evaluate('!tutLive()&&!HS21.visible&&HS21.root.hidden&&!document.body.classList.contains("holoscan-open")'))
  ck('No page/console/resource errors',not errors,errors);br.close()
finally:stop()
print(json.dumps(dict(checks=len(checks),passed=sum(c['ok'] for c in checks),errors=errors)),flush=True)
sys.exit(0 if not errors and all(c['ok'] for c in checks) else 1)
