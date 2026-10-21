"""Native spin, both escape edges, and every actual wireframe transformation."""
from pathlib import Path
from PIL import Image,ImageDraw
from io import BytesIO
import ast,base64,http.server,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_download_1019';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
BOOT=next(n.args[0].value for n in ast.walk(ast.parse((R/'_BUILD_SOURCE/probe_dracodia_demon_1019.py').read_text(encoding='utf-8'))) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.demonSetup=' in n.args[0].value)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&dr21Warm();}',polling=80);p.evaluate(BOOT)
  def setup(phase=2,diff='normal',kind='shadowAscension'):return p.evaluate('([a,b,c])=>demonSetup(a,b,c)',[phase,diff,kind])
  def tick(n):p.evaluate('demonTick',n)
  def shot(name=None):
   p.evaluate('()=>{shake=whiteBlast=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   raw=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
   if name:(O/(name+'.png')).write_bytes(raw)
   im=Image.open(BytesIO(raw)).convert('RGB');im.thumbnail((840,1000));return im
  def movie(name,film):film[0].save(O/(name+'.webp'),save_all=True,append_images=film[1:],duration=100,loop=0,quality=88)
  for diff in ['easy','normal','hard','furious']:
   for side in [-1,1]:
    for initial in ['center','edge']:
     setup(2,diff);p.evaluate('([side,initial])=>{run.speed=0;player.x=initial==="edge"?(side<0?camLeftX()+24:camRightX()-24):worldWidth()/2;}',[side,initial])
     row=p.evaluate('''side=>{let minimum=9999,locked=null,spins=[];for(let i=0;i<460;i++){if(P.locked){player.x=clamp(player.x+side*playerBaseSpeed(),camLeftX()+24,camRightX()-24);}demonTick(1);if(P.locked&&!locked)locked={...P.target};const u=P.t-P.tell;if(u>P.travel*.94&&u<P.travel+.16)minimum=Math.min(minimum,Math.hypot(player.x-P.x,player.y-P.y));if(i%60===0)spins.push(P.spin);}return{alive:!player.dead,invuln:player.invuln,hits:P.hit.size,minimum,locked,left:camLeftX(),right:camRightX(),radius:P.radius,spins};}''',side)
     check(diff+' '+('left' if side<0 else 'right')+' escape from '+initial+' with base speed / no iframes',row['alive'] and row['invuln']==0 and row['hits']==0 and row['minimum']>row['radius'],row)
     check(diff+' '+initial+' commit preserves both edge corridors',row['locked'] and row['locked']['x']>=row['left']+110 and row['locked']['x']<=row['right']-110,row)
   setup(2,diff);tick(450);check(diff+' staying in the central core is still lethal',p.evaluate('player.dead&&player._dr21Death?.kind==="shadow"'))
  setup();tick(30);p.evaluate('()=>{window.spinSamples=[];window.spinRead=()=>{const old=ctx.rotate;ctx.rotate=function(a){spinSamples.push(a);return old.call(this,a);};try{dr21DrawAttack(B);}finally{ctx.rotate=old;}};spinRead();}');tick(74);p.evaluate('spinRead()');row=p.evaluate('({rotations:spinSamples,t:P.t,spin:P.spin})');check('Charge completes a continuous 360-degree revolution',len(row['rotations'])==2 and abs((row['rotations'][1]-row['rotations'][0])-6.28318530718)<.4,row)
  p.evaluate('P.t=P.tell+.1');tick(1);p.evaluate('spinRead()');p.evaluate('P.t=P.tell+P.travel*.8');tick(1);p.evaluate('spinRead()');row=p.evaluate('spinSamples');check('Release and approaching ball keep the same forward spin clock',len(row)==4 and all(row[i+1]>row[i] for i in range(3)),row)
  # Capture the actual native canvas at eight quarter/half poses of one full
  # turn, holding the authored flame frame fixed to isolate rotation.
  row=p.evaluate('''()=>{const save=ctx.rotate,angles=[];ctx.rotate=function(a){angles.push(a);return save.call(this,a);};try{for(let i=0;i<=8;i++)dr21Art('ball',.35,240,240,180,1,false,i*TAU/8);}finally{ctx.rotate=save;}return angles;}''');check('Native renderer receives every angle including a full 2pi turn',len(row)==9 and abs(row[-1]-6.28318530718)<.00001,row)
  setup();film=[]
  for i in range(112):
   p.evaluate('()=>{for(let i=0;i<4;i++){if(!P.locked)player.x=worldWidth()/2+Math.sin(P.t*1.3)*90;else player.x=clamp(player.x-playerBaseSpeed(),camLeftX()+24,camRightX()-24);demonTick(1);}}');im=shot('ball-spin-'+str(i) if i in [10,20,30,42,70,80,88,93] else None);film.append(im)
  movie('rotating-ball',film);check('Filmed rotating ball permits a real left-edge dodge',p.evaluate('!player.dead&&player.invuln===0'))
  setup();p.evaluate('v18Clear(B);dr5State(B).radio=null;B._r30.cd=999');film=[];keyframes=[]
  for form,name in [(8,'hammer'),(1,'helicopter'),(6,'harrier'),(2,'volcano'),(0,'colossus')]:
   p.evaluate('form=>{j3State(B).attacks=D20.book.length;j3Morph(B,form);}',form)
   for i in range(32):
    tick(6);im=shot(name+'-'+str(i) if i in [4,9,17,21,26,30] else None);film.append(im)
    if i in [9,21,30]:keyframes.append((name+' '+str(i),im.copy()))
   row=p.evaluate('({mode:B._r30.mode,form:B._r30.v18.form,hidden:B._noHit,enter:B.enter,protectionOwned:B._r30.v18.form!==8||B._noHit===!!gd4Create(B,8).p._noHit,draws:DR21.draws,transition:DR21.transition})');check(name+' naturally downloads then returns to its live fight',row['mode']=='fight' and row['form']==form and not row['enter'] and row['protectionOwned'] and row['draws'].get('wire_'+name,0)>0,row)
   check(name+' all native module sockets remain finite',p.evaluate('v18Rig(B).every(v=>Number.isFinite(v.x)&&Number.isFinite(v.y)&&v.w>0&&v.h>0)'))
  movie('form-downloads',film)
  film=[]
  for phase in [1,2]:
   setup(phase-1,kind='codeAegis');p.evaluate('phase=>{v18Clear(B);B._r30.v18.transition={to:phase,switched:false};v18SetMode(B,"v18phaseFade");dr5State(B).introSeen=true;}',phase)
   for i in range(51):
    tick(6);im=shot('phase-'+str(phase+1)+'-'+str(i) if i in [19,26,34,42,49] else None);film.append(im)
   row=p.evaluate('({phase:j3State(B).encounter,mode:B._r30.mode,draws:DR21.draws})');check('Phase '+str(phase+1)+' arrives through its own wireframe body',row['phase']==phase and row['draws'].get('wire_'+('ghost' if phase==1 else 'colossus'),0)>0,row)
  movie('phase-downloads',film)
  setup(0,kind='codeAegis');p.evaluate('()=>{v18Clear(B);v18SetMode(B,"v18conversion");B._r30.t=2.9;}');shot('infused-download');check('Infused host also downloads its actual wireframe',p.evaluate('DR21.draws.wire_infused>0'))
  # Every sheet/frame blits through the production renderer with stable
  # anchors and no leaked canvas state, using actual stage dimensions.
  for phase,form,name in [(0,0,'infused'),(1,0,'ghost'),(2,0,'colossus'),(2,8,'hammer'),(2,1,'helicopter'),(2,6,'harrier'),(2,2,'volcano')]:
   setup(phase,kind='codeAegis');p.evaluate('form=>{v18Clear(B);v18Enter(B,j3State(B).encounter,form);v18Fight(B);}',form)
   row=p.evaluate('''()=>{const before=ctx.getTransform(),alpha=ctx.globalAlpha,composite=ctx.globalCompositeOperation;for(let i=0;i<16;i++)dr21Download(B,i*.07,1.6,true);const after=ctx.getTransform();return{same:['a','b','c','d','e','f'].every(k=>before[k]===after[k]),alpha:alpha===ctx.globalAlpha,composite:composite===ctx.globalCompositeOperation};}''');check(name+' all sixteen wire frames restore canvas state',all(row.values()),row)
   row=p.evaluate('''()=>{dr21Download(B,.6,1.6,true);const a=DR22_ART.forms[v18Model(B)],k=v18Size(B)/(a.captureSize*a.captureScale);return{top:B.y+(a.bounds[1]-a.pivot[1])*k+DR21.transition.offsetY,limit:viewTopY()+72};}''');check(name+' whole wireframe clears the protected HUD',row['top']>=row['limit']-.1,row)
  setup();row=p.evaluate('''()=>{v18Clear(B);j3State(B).attacks=D20.book.length;const old=Snd.play,seen=[];Snd.play=function(k){seen.push(k);return old.apply(this,arguments);};try{v18Enter(B,2,8);v18SetMode(B,'v18formIn');const before=seen.length;for(let i=0;i<5;i++)r30DrawBoss(B);return{cue:seen.includes('teleportIn'),repeat:seen.length-before};}finally{Snd.play=old;}}''');check('Download cue fires on entry and never repeats per draw',row['cue'] and row['repeat']==0,row)
  setup();tick(450);row=p.evaluate('({time:player._dr21Death?.ballTime,spin:P.spin})');check('Lethal foreground preserves the incoming rotation phase',row['time'] and row['time']>5,row)
  check('No page, console, asset or draw errors',not errors,errors);br.close()
finally:stop()
sheet=Image.new('RGB',(3*420,len(keyframes)//3*520),'#0d1018');d=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(keyframes):
 im.thumbnail((420,490));x=i%3*420;y=i//3*520;sheet.paste(im,(x,y));d.text((x+8,y+495),label,fill='white')
sheet.save(O/'native-transitions-sheet.png')
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors)),flush=True);raise SystemExit(0 if all(q['passed'] for q in checks) and not errors else 1)
