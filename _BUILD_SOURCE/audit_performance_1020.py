from pathlib import Path
import ast,json,sys,http.server,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/performance_finish_1020/audit';O.mkdir(exist_ok=True,parents=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
roster=[(1,'razorback',True),(1,'damkeeper',False),(2,'magmaward',True),(2,'infernoreaver',False),(3,'frostcruiser',True),(3,'cryospear',False),(4,'olivewarden',True),(4,'stormsovereign',False),(5,'siegebomber',True),(6,'siegefortress17',True),(6,'warhive',False),(6,'rebelsquad',False),(7,'dualscoopdredger',True),(7,'sludgeemperor',False),(8,'heralddeath',True),(9,'voidhorizon',True),(9,'tidalfusion',False)]
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));rows=[];errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.PA20={keys:{},phase:[],clock:0};const get=XART.get,draw=ctx.drawImage,tags=new WeakMap();XART.get=function(k){const im=get.apply(this,arguments);if(im)tags.set(im,k);return im;};ctx.drawImage=function(im,...a){const k=tags.get(im);if(PA20.capture&&k){const q=PA20.keys[k]||(PA20.keys[k]={n:0,w:im.naturalWidth||im.width,h:im.naturalHeight||im.height});q.n++;}return draw.call(this,im,...a);};const db=drawBoss,ds=drawSubBoss;drawBoss=function(){const old=PA20.capture;PA20.capture=true;try{return db.apply(this,arguments);}finally{PA20.capture=old;}};drawSubBoss=function(){const old=PA20.capture;PA20.capture=true;try{return ds.apply(this,arguments);}finally{PA20.capture=old;}};window.pa20Paint=()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);};}''')
  for stage,kind,mini in roster:
   print('AUDIT '+kind,flush=True);p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,diff='normal',pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=80)
   p.evaluate('''()=>{VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;spawnClock=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;subBossDone=true;warnT=0;warnKind=null;bossWarned=false;bossDefeated=false;stageTimer=0;BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;run._megaShield=false;run.spaceMode=[5,9].includes(run.stage);player.fireCd=999999;powerups=[];eBullets=[];pBullets=[];PA20={keys:{},phase:[],clock:0};}''')
   shots=[]
   for sec in range(36):
    p.evaluate('''()=>{for(let i=0;i<60;i++){PA20.clock+=1/60;player.invuln=1e9;Input.keys={};Input.mouse.down=false;if(!player._ra7Caught&&!player._ra7Thrown){player.x=worldWidth()/2+Math.sin(PA20.clock*.65)*95;player.y=VH-100;}updatePlay(1/60);if(i%10===0)pa20Paint();}const phase=B._er26?.state||B._er26?.mode||B.state||B.phase;PA20.phase.push({time:PA20.clock,phase,ship:B._ship});}''')
    if sec==17:p.evaluate('B.hp=B.maxhp*.42')
    if sec%4==3:
     p.evaluate('shake=0;pa20Paint()');f=O/f'{stage}-{kind}-{sec+1:02}.png';f.write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')));shots.append(f)
    if sec%6==0:p.wait_for_timeout(10)
   row=p.evaluate('({keys:PA20.keys,phases:PA20.phase,state:{ship:B._ship,type:B.type,w:B.w,h:B.h,x:B.x,y:B.y,er:B._er26?{mode:B._er26.mode,state:B._er26.state}:null}})');row.update(stage=stage,kind=kind,mini=mini);rows.append(row)
   contact=Image.new('RGB',(480*3,534*3),'#0a1421');g=ImageDraw.Draw(contact)
   for i,f in enumerate(shots):
    im=Image.open(f).convert('RGB');im.thumbnail((480,512));x=i%3*480;y=i//3*534;contact.paste(im,(x,y));g.text((x+8,y+514),f.stem,fill='white')
   contact.save(O/(kind+'-contact.jpg'),quality=88)
   (O/'report.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2),encoding='utf-8')
  # Current terminal effects, from their actual native draw owner.
  p.evaluate(SETUP,dict(stage=1,pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&dr21Warm();}')
  for kind,source in [('laser','laser beam'),('ice','cryo ice shard'),('shadow','Dracodia shadow eradication')]:
   p.evaluate('s=>{player.dead=false;player.invuln=0;player.roll=player.somer=null;run.shield=0;playerHit(s);}',source)
   for i,t in enumerate([.1,.35,.65,.95,1.25]):
    p.evaluate('t=>{player._dr21Death.t=t;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);ctx.fillStyle="#081422";ctx.fillRect(0,0,VW,VH);drawDeathSpin();}',t)
    (O/f'death-{kind}-{i}.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  br.close()
finally:stop()
print(json.dumps({'encounters':len(rows),'errors':errors}),flush=True);raise SystemExit(bool(errors))
