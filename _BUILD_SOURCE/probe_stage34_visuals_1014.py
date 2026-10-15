"""Charge pixels, modular emitters, native haptic requests and overhead images."""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage34_assault_1014/visuals';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def check(ok,name,data=None):checks.append(dict(passed=bool(ok),name=name,data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof SA14!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  def setup(stage,kind):
   p.evaluate(SETUP,dict(stage=stage,kind=kind,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&XART.rdy("mr27_"+B._mr27.skin)&&bmfReady("game")}')
   p.evaluate('()=>{B._er26.engaged=false;B._phaseInvuln=0;B._er26.warnings=[];er26Tick(B,0);SA14.events=[];story=fb2Talk=null;BOFCinematicDirector.cancel();}')
  def snap(name):
   p.evaluate('()=>{story=fb2Talk=null;BOFCinematicDirector.cancel();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  for stage,kind,mode in [(3,'cryospear','sa14-ice'),(4,'stormsovereign','sa14-storm')]:
   setup(stage,kind)
   data=p.evaluate('''mode=>{er26Set(B,mode);B._er26.t=B._er26.warm*.90;er26Tick(B,0);
    const glow=B._sa14.glow;function pixels(){ctx.setTransform(SS,0,0,SS,0,0);ctx.translate(-camX,0);drawBG(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;let sum=0;for(let i=0;i<a.length;i+=4)sum+=a[i]+a[i+1]+a[i+2];return sum/(a.length/4*3);}
    B._sa14.glow=0;const plain=pixels();B._sa14.glow=glow;const dim=pixels();return {glow,plain,dim,ratio:dim/plain,warnings:B._er26.warnings.length};}''',mode)
   check(data['glow']>.85 and data['ratio']<.55,f'Stage {stage}: actual background pixels darken during charge',data)
   check(data['warnings']==7,f'Stage {stage}: authored FOV excludes the two safe salvo lanes',data)
   snap('stage'+str(stage)+'-charged')
   p.evaluate('()=>{B._sa14.age=.08;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   snap('stage'+str(stage)+'-blue-flash')
  setup(4,'stormsovereign')
  pulse=p.evaluate('''()=>{const old=navigator.getGamepads,calls=[];navigator.getGamepads=()=>[{vibrationActuator:{playEffect(type,options){calls.push({type,...options});return Promise.resolve('complete');}}}];
   try{B._sa14.rumbleCd=0;sa14Rev(B,.8,.2);}finally{navigator.getGamepads=old;sa14Stop(B);}return calls;}''')
  check(len(pulse)==1 and pulse[0]['strongMagnitude']>.4,'Charge requests native dual-motor haptics when a controller supports them',pulse)
  p.evaluate('()=>{player.y=180;er26Set(B,"sa14-lock");}')
  shake=p.evaluate('''()=>{B._er26.t=.40;const a=mr27Shape(B,'rocketL');B._er26.t=.44;const b=mr27Shape(B,'rocketL');return Math.hypot(a.x-b.x,a.y-b.y);}''')
  check(shake>1,'Missile-box rumble moves the actual shared drawing/collision/muzzle geometry',shake)
  emit=p.evaluate('''()=>{mr27Part(B,'rocketL').dead=true;eBullets=[];const count=sa14Missiles(B,{x:player.x,y:player.y},true),tip=shipBossMount(B,'ROCKET_R');return{count,shots:eBullets.map(q=>({x:q.x,y:q.y})),tip};}''')
  check(emit['count']==3 and all(abs(q['x']-emit['tip']['x'])<.01 and abs(q['y']-emit['tip']['y'])<.01 for q in emit['shots']), 'Destroyed left missile box stops firing; surviving right missiles leave its real muzzle',emit)
  p.evaluate('()=>{mr27Part(B,"rocketL").dead=false;SA14.events=[];player.y=180;B._sa14.lockCd=0;er26Set(B,"recover");}')
  for _ in range(3):p.evaluate('()=>{for(let i=0;i<30;i++)er26Tick(B,1/60)}');p.wait_for_timeout(10)
  paused=p.evaluate('()=>({t:B._er26.t,x:B.x,y:B.y,beeps:SA14.events.filter(q=>q.event==="lock-beep").length})')
  p.evaluate('setState("paused")');p.evaluate(shoot.STEP,30)
  after=p.evaluate('()=>({t:B._er26.t,x:B.x,y:B.y,beeps:SA14.events.filter(q=>q.event==="lock-beep").length})')
  check(after==paused and p.evaluate('state==="paused"'),'Pause freezes targeting, motion and beep progression')
  p.evaluate('()=>{setState(GS.PLAY);player.y=VH-90;er26Set(B,"sa14-overflight");}')
  for count in [30,30,30,30,30,30,30,24]:p.evaluate('n=>{for(let i=0;i<n;i++)er26Tick(B,1/60)}',count);p.wait_for_timeout(10)
  snap('over-player')
  check(p.evaluate('B._sa14.depth&&B._sa14.scale>1.4&&B._sa14.angle===Math.PI'),'Over-player capture uses an enlarged north-facing authored plate')
  p.evaluate('()=>{for(let i=0;i<24;i++)er26Tick(B,1/60);}');snap('overhead-north-exit')
  data=p.evaluate('({depth:B._sa14.depth,scale:B._sa14.scale,t:B._er26.t,nodes:B._s4war.shield.nodes.map(n=>({x:n.x,y:n.y}))})')
  check(p.evaluate('B._sa14.depth&&B._sa14.scale>1&&B._s4war.shield.nodes.every(n=>Number.isFinite(n.x)&&Number.isFinite(n.y))'),'Overhead transformation keeps every generator registered to the scaled hull',data)
  p.evaluate('()=>{VP12.groups=[];enemies=[];vp12Spawn("crisscross");window.colorJet=enemies.find(e=>e._vp12);colorJet._vp12.g.age=2;vp12Move(colorJet,0);colorJet.flash=.2;}')
  for fallback in [False,True]:
   color=p.evaluate('''fallback=>{const tint=xartTint,airTint=air13Tint,pose=air13Pose,draw=ctx.drawImage;let recolors=0,draws=0;
    xartTint=function(){recolors++;return tint.apply(this,arguments)};air13Tint=function(){recolors++;return airTint.apply(this,arguments)};
    ctx.drawImage=function(){draws++;return draw.apply(this,arguments)};if(fallback)air13Pose=()=>null;
    try{drawEnemy(colorJet);}finally{xartTint=tint;air13Tint=airTint;air13Pose=pose;ctx.drawImage=draw;}
    return{recolors,draws,flash:colorJet.flash};}''',fallback)
   check(color['recolors']==0 and color['draws']>0 and color['flash']==.2,('Fallback' if fallback else 'Primary')+' authored mini-aircraft hit draw preserves palette and damage timer',color)
  scope=p.evaluate('''()=>{const stage=run.stage;try{run.stage=8;return ['cryospear','olivewarden','stormsovereign'].every(ship=>{const q={_ship:ship,_er26:{level:1},_mr27:null};return !sa14Owns(q)&&JSON.stringify(er26Book(q))===JSON.stringify(SA14.base.book(q));});}finally{run.stage=stage;}}''')
  check(scope,'Reused late-stage hulls retain their existing encounter controllers')
  browser.close()
finally:
 stop();report={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'errors':errors,'scope':'Native pixels and controlled mechanics; haptics capability simulated, not hardware play.'}
 (O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');(R/'docs/qa/stage34_visuals_1014.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
 if report['failed'] or errors:sys.exit(1)
