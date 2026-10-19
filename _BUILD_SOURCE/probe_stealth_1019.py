"""Native cloak poses, actual Nyx hull/flash, friendly stealth and counter-scan."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/stealth';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'))
  p.evaluate('''()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;window.G=rg4Init(B);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;
   rg4Warm();s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;for(const q of s6Wing.ships){q.phase='fight';q.fcd=q.specialCd=q.missileCd=999;}
   G.scene=null;G.rescueDone=true;G.rescueAt=Infinity;G.releaseAt=999;for(const q of R.ships){q.rg4.cd=q.rg4.gunCd=999;q.rg4.act=null;}
   VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;warnT=0;warnKind=null;player.invuln=1e9;powerups=[];
   window.Q=R.ships.find(q=>q.key==='nyx');window.sk19KeysSeen=[];const get=XART.get;XART.get=function(k){sk19KeysSeen.push(k);return get.apply(this,arguments);};
   window.sk19Pixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
   SC12.refresh();__bofFit();}''')
  p.wait_for_function('()=>{stageLoadTick();rg4Warm();return stageLoadReady(6)&&sk19Ready()&&XART.rdy(RA7.sheet)&&bmfReady("game")}',polling=50)
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/(name+'.png')))
  poses=p.evaluate('''()=>{const out=[],d=ctx.drawImage;let calls=0;ctx.drawImage=function(){calls++;return d.apply(this,arguments);};try{for(const [bank,a]of Object.entries(SK19_ART.banks)){const before=calls;for(let i=0;i<a.length;i++)sk19Draw(bank,i,200,200,.7,1);out.push({bank,frames:a.length,calls:calls-before});}}finally{ctx.drawImage=d;}return out;}''')
  ck('Every delivered PixelLab pose actually blits through the game context',len(poses)==3 and all(q['frames']>=16 and q['frames']==q['calls'] for q in poses),poses)
  p.evaluate('rg4Attack(Q,R,G,"cloak")');frames(40);snap('nyx-forming')
  ck('Nyx formation uses the new in bank around the actual aircraft',p.evaluate('sk19KeysSeen.some(k=>k.startsWith("sk19_in_"))&&Q.rg4.act.kind==="cloak"'))
  frames(60);snap('nyx-loop-warning')
  ck('Nyx looping effect has front/back layers and a visible native ship',p.evaluate('SK19.draws.some(q=>q.key.startsWith("sk19_loop_")&&q.front)&&SK19.draws.some(q=>q.key.startsWith("sk19_loop_")&&!q.front)&&Q.frCloak>0'))
  ck('Cloak removes missile acquisition while keeping the warned Ghostknife attack',p.evaluate('!retinaBossTargets(B).some(t=>t._retinaId==="nyx-hull")&&!!Q.rg4.act._ra7Pulse'))
  frames(75);snap('nyx-ambush')
  ck('Cloaked Nyx releases actual Ghostknife bullets',p.evaluate('RA7.events.some(e=>e.event==="ghostknifeVolley")'))
  flash=p.evaluate('''()=>{const old=Q.flash;Q.flash=0;const a=sk19Pixels(()=>fr27RebelDrawShip(Q));const hp=Q.hp;pBullets.push({kind:'mg',x:Q.x,y:Q.y,vx:0,vy:0,w:12,h:20,dmg:3,t:0});updatePlay(1/60);const timer=Q.flash,b=sk19Pixels(()=>fr27RebelDrawShip(Q));let pixels=0;for(let i=0;i<a.length;i+=4)if(b[i+3]>30&&Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)pixels++;return{hpLoss:hp-Q.hp,timer,pixels};}''')
  ck('Blind native gunfire damages Nyx and changes actual hit pixels while cloaked',flash['hpLoss']>0 and flash['timer']>0 and flash['pixels']>20,flash);snap('nyx-hit')
  frames(30);ck('Nyx hit flash expires on the native clock',p.evaluate('Q.flash===0'))
  p.evaluate('Q.rg4.act.t=5.19');frames(4);snap('nyx-reveal')
  ck('Cloak reveal uses real reverse forming poses in the out bank',p.evaluate('SK19.draws.some(q=>q.key.startsWith("sk19_out_"))'))
  frames(38);ck('Nyx missile acquisition returns after the actual reveal',p.evaluate('retinaBossTargets(B).some(t=>t._retinaId==="nyx-hull")'))
  # The real rescue director creates the friendly formation and source ships.
  p.evaluate('G.rescueDone=false;rg4RescueStart(B,G);G.scene.castAt=0;G.scene.age=3.2;G.cloak=1;SK19.draws=[];');snap('friendly-stealth')
  ck('All five real friendly aircraft receive the centered new cloak',p.evaluate('G.members.length===5&&G.members.every(m=>SK19.draws.some(q=>Math.hypot(q.x-m.ref.x,q.y-m.ref.y)<.01))'))
  friendly=p.evaluate('''()=>{const m=G.members.find(m=>m.ref===player),key='ship_'+m.key,im=XART.get(key),h=SHIP_DRAW_H,w=h*im.width/im.height;
   const a=sk19Pixels(()=>{ctx.drawImage(im,player.x-w/2,player.y-h/2,w,h);}),b=sk19Pixels(()=>rg4Friendly(m,G));let visible=0,ink=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>180){ink++;if(b[i+3]>=120)visible++;}return{ink,visible,ratio:visible/ink};}''')
  ck('Player hull stays readable at full friendly stealth',friendly['ink']>30 and friendly['ratio']>.85,friendly)
  p.evaluate('G.scene.scanAt=.5;G.scene.revealAt=null;G.scene.age=4.2');snap('friendly-counter-scan')
  ck('Authored counter-scan Retina remains active',p.evaluate('(RG4.draws.scan||0)>0'))
  p.evaluate('G.scene.revealAt=4;G.scene.age=4.6;G.cloak=.5;SK19.draws=[]');snap('friendly-reveal')
  ck('Friendly reveal uses the separate out bank on the live formation',p.evaluate('SK19.draws.some(q=>q.key.startsWith("sk19_out_"))'))
  br.close()
finally:stop()
ck('No page/console/draw/asset errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors);(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True);sys.exit(report['failed']>0)
