"""All nine actual friendly hulls and a live docked mount during squad cloak."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/stealth-pilots';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];rows=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.FC19={scope:false,calls:[]};const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof im==='object')tags.set(im,k);return im;};ctx.drawImage=function(im){if(FC19.scope){const key=tags.get(im);if(key)FC19.calls.push({key,alpha:this.globalAlpha,matrix:[this.getTransform().a,this.getTransform().d,this.getTransform().e,this.getTransform().f]});}return draw.apply(this,arguments);};
   window.fc19Render=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.setTransform(SS,0,0,SS,-camX*SS,0);FC19.calls=[];FC19.scope=true;drawPlayer();lzMountDraw();FC19.scope=false;const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
  }''')
  def setup(pilot,rescue=True):
   p.evaluate('v=>window.fc19RescueOnSetup=v',rescue)
   p.evaluate('k=>{pilotIndex=PILOTS.findIndex(q=>q.key===k);PILOTMOD={...PILOTS[pilotIndex]};run.pilot=k;}',pilot);p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot=pilot));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&sk19Ready()&&bmfReady("game")}',polling=50)
   p.evaluate('''k=>{pilotIndex=PILOTS.findIndex(q=>q.key===k);PILOTMOD={...PILOTS[pilotIndex]};run.pilot=k;window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;window.G=rg4Init(B);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;fb2Flights=[];s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;for(const q of s6Wing.ships){q.phase='fight';q.fcd=q.specialCd=q.missileCd=999;}G.scene=null;G.rescueDone=false;G.rescueAt=Infinity;G.releaseAt=999;for(const q of R.ships){q.rg4.cd=q.rg4.gunCd=999;q.rg4.act=null;}VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;CP12.stage=6;CP12.lastTimer=0;_adaptiveSpawnT=999999;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;warnT=0;warnKind=null;player.invuln=1e9;player.flash=0;powerups=[];lzMountEnd(true);if(window.fc19RescueOnSetup)rg4RescueStart(B,G);for(const m of (G.members||[]))XART.rdy('ship_'+m.key);}''',pilot)
   if not rescue:p.evaluate('G.scene=null;G.rescueDone=false;G.cloak=0;B._noHit=false;')
   p.wait_for_function('()=>sk19Ready()&&XART.rdy("ship_"+run.pilot)&&(!G.members||G.members.every(m=>XART.rdy("ship_"+m.key)))',polling=50)
  for pilot in p.evaluate('PILOTS.map(q=>q.key)'):
   setup(pilot)
   q=p.evaluate('''()=>{G.scene.age=3.2;G.scene.t=.01;G.scene.castAt=null;G.cloak=0;rg4SceneTick(B,G,0);const a=fc19Render(),normal=FC19.calls.filter(q=>q.key==='ship_'+run.pilot);G.scene.castAt=0;G.cloak=1;SK19.draws=[];const b=fc19Render(),calls=FC19.calls.filter(q=>q.key==='ship_'+run.pilot);let ink=0,visible=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>180){ink++;if(b[i+3]>=120)visible++;}return{pilot:run.pilot,members:G.members.length,normal,calls,ink,visible,ratio:visible/Math.max(1,ink),centered:SK19.draws.some(q=>Math.hypot(q.x-player.x,q.y-player.y)<.01),banks:[...new Set(SK19.draws.map(q=>q.key.split('_')[1]))]};}''');rows.append(q)
   ck(pilot+' native selected hull receives a centered cloak',q['members']==5 and q['centered'] and q['normal'] and q['calls'] and all(abs(c['alpha']-.52)<.001 for c in q['calls']),q)
   ck(pilot+' opaque native hull pixels remain readable',q['ink']>30 and q['ratio']>.85,q)
   if pilot in ['lizzie','maverick','juggernaut']:p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/(pilot+'-cloak.jpg')),type='jpeg',quality=82)
  # A genuine pickup at the rescue start can still be active when the native
  # scene reaches full cloak. Do not extend its life or fast-forward the lines.
  setup('lizzie',False);p.evaluate('lzMountGrant();window.fc19Natural=[];')
  for i in range(4):p.evaluate(shoot.STEP,12);p.wait_for_timeout(5)
  ck('The actual mounted pickup finishes docking before the rescue starts',p.evaluate('lzMountActive()&&lzMount.life>14'))
  p.evaluate('rg4RescueStart(B,G)')
  for i in range(80):
   p.evaluate(shoot.STEP,12);p.wait_for_timeout(5)
   if p.evaluate('G.cloak>.97&&lzMountActive()'):break
  natural=p.evaluate('''()=>{fc19Render();const mounts=FC19.calls.filter(q=>q.key==='nlz_mount'),m=mounts[0];return{age:G.scene?.age,cloak:G.cloak,active:lzMountActive(),life:lzMount?.life,hull:FC19.calls.filter(q=>q.key==='ship_lizzie'),mount:mounts,drift:m?Math.hypot(m.matrix[2]/SS+camX-player.x,m.matrix[3]/SS-(player.y-14)):null,player:{x:player.x,y:player.y},cached:{x:lzMount?.x,y:lzMount?.y}};}''')
  ck('A real fifteen-second mounted pickup overlaps the native full-cloak scene',natural['active'] and natural['cloak']>.97 and natural['life']>0 and natural['age']<15,natural)
  ck('Docked mount and native hull share the actual friendly cloak opacity',natural['hull'] and natural['mount'] and abs(natural['hull'][0]['alpha']-natural['mount'][0]['alpha'])<.02,natural)
  ck('Docked mount stays physically anchored through the native formation movement',natural['drift'] is not None and natural['drift']<.01,natural)
  p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit()');p.screenshot(path=str(O/'lizzie-natural-mounted-cloak.jpg'),type='jpeg',quality=84)
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors);q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');sys.exit(q['failed']>0)
