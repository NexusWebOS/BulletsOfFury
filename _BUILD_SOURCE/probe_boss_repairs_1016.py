"""Native ballistic shots, four-generator shield completion and Hammer budget/charge."""
from pathlib import Path
import ast,json,sys,traceback,hashlib,base64
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_repairs_1016';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  def setup(stage,kind,diff='normal'):
   p.evaluate(SETUP,dict(stage=stage,kind=kind,pilot='cole',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}')
   p.evaluate('()=>{if(B._er26){B._er26.engaged=false;er26Tick(B,0);}B._phaseInvuln=0;B._noHit=false;story=fb2Talk=null;BOFCinematicDirector.cancel();stagePlan=[];VP12.next=CP12.next=EP13.next=9999;player.invuln=1e9;}')
  def frames(n):
   for i in range(0,n,30):p.evaluate('n=>{for(let j=0;j<n;j++)updatePlay(1/60)}',min(30,n-i));p.wait_for_timeout(3)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  # Move the player across each round's flight; the release heading cannot change.
  setup(4,'stormsovereign')
  for kind in ['fireorb','groundup','emissile']:
   row=p.evaluate('''kind=>{eBullets=[];pBullets=[];const q=eShootT(camLeftX()+100,PLAY.y+90,Math.PI/2,2.8,kind,{w:8,h:16,silent:true});
    q.homing=true;q._shootable=true;q.hp=100;q._weaponProof=true;window.ballisticTest=q;
    return {a:Math.atan2(q.vy,q.vx)};}''',kind)
   for side in [-1,1,-1]:
    p.evaluate('side=>{player.x=camLeftX()+viewW()*(side<0?.12:.88);}',side);frames(20)
   q=p.evaluate('({a:Math.atan2(ballisticTest.vy,ballisticTest.vx),committed:ballisticTest._committed,homing:ballisticTest.homing,alive:!ballisticTest.dead})')
   check(kind+' keeps its launch heading while the player crosses',abs(q['a']-row['a'])<.00001 and q['committed'] and not q['homing'],q)
  # Hit all generators through real point routing, including overlapping helpers.
  for diff in ['normal','hard','furious']:
   setup(4,'stormsovereign',diff)
   p.wait_for_function('()=>[...Array(12)].every((_,i)=>XART.rdy("s4w_lightning_shield_"+i))&&XART.rdy(S4REV1006_ART.key)&&XART.rdy("mr27_storm")')
   p.evaluate('''()=>{stage4CoreTurretSpawnMissing(B,.5);sa14CoreTick(B,1);
    window.hitGenerator=function(n){B._noHit=false;B._phaseInvuln=0;_lastHitX=n.x;_lastHitY=n.y;_dmgBullet=null;
     let target=false,node=false,hits=0;while(!n.dead&&hits++<4){target=bossHitTest(n.x,n.y);node=B._s4ShieldHit===n;hitBoss(1e6);}return{target,node,dead:n.dead,hits};};}''')
   cycles=[]
   for cycle in range(3):
    data=p.evaluate('''()=>{const H=B._s4war.shield,nodes=H.nodes,rows=[];
     for(const n of nodes.slice(0,2))rows.push(hitGenerator(n));stage4ShieldTick(B,20);
     return{rows,active:H.active,remaining:H.nodes.filter(n=>!n.dead).length};}''')
    check(diff+' cycle '+str(cycle)+' two surviving cores keep shield up past 18 seconds',data['active'] and data['remaining']==2 and all(q['node'] and q['dead'] for q in data['rows']),data)
    if cycle==0 and diff=='normal':snap('sovereign-two-cores-shield-active')
    data=p.evaluate('''()=>{const H=B._s4war.shield,rows=H.nodes.filter(n=>!n.dead).map(hitGenerator);return{rows,active:H.active,remaining:H.nodes.filter(n=>!n.dead).length};}''')
    check(diff+' cycle '+str(cycle)+' all four real core kills release shield',not data['active'] and data['remaining']==0 and all(q['node'] for q in data['rows']),data)
    data=p.evaluate('''()=>{const S=B._s4war,H=S.shield;let hits=0;while(!H.rearming&&!S._pt11Chase&&!B.dead&&hits++<30){
     B._phaseInvuln=0;B._noHit=false;_dmgBullet=null;const m=mr27Shape(B,'core');_lastHitX=m.x;_lastHitY=m.y;bossHitTest(m.x,m.y);hitBoss(B.maxhp*.18);}
     return{hits,hp:B.hp,max:B.maxhp,rearming:H.rearming,chase:!!S._pt11Chase,index:S.shieldThresholdIndex};}''')
    cycles.append(data)
    if cycle<2:
     check(diff+' threshold '+str(cycle)+' starts generator reconstruction',data['rearming'],data)
     frames(80)
     check(diff+' threshold '+str(cycle)+' rebuilds all four objectives',p.evaluate('B._s4war.shield.active&&!B._s4war.shield.rearming&&B._s4war.shield.nodes.every(n=>!n.dead&&n.hp>0)'))
     if diff=='normal' and cycle==0:snap('sovereign-regenerated-shield')
    else:check(diff+' final quarter enters pursuit without another shield lock',data['chase'] and not data['rearming'],data)
   frames(700)
   finish=p.evaluate('''()=>{let hits=0;while(!B.dead&&hits++<40){B._phaseInvuln=0;_dmgBullet=null;const m=mr27Shape(B,'core');_lastHitX=m.x;_lastHitY=m.y;bossHitTest(m.x,m.y);hitBoss(B.maxhp*.25);}return{dead:B.dead,hp:B.hp,hits,noHit:B._noHit,mode:B._er26.mode};}''')
   check(diff+' native damage can finish the entire encounter',finish['dead'] and finish['hp']<=0,finish)
  # Native shield draw keys must advance and the reassembly layer must be called.
  setup(4,'stormsovereign')
  art=p.evaluate('''()=>{const get=XART.get,clip=s4RevivalClip1006;const keys=new Set();let rebuild=0;
   XART.get=function(k){if(k.startsWith('s4w_lightning_shield_'))keys.add(k);return get.apply(this,arguments)};
   s4RevivalClip1006=function(){rebuild++;return clip.apply(this,arguments)};
   try{for(let i=0;i<16;i++){B._mr27.clock=i*.1;mr27Over(B);}B._s4war.shield.revival1006={t:.6};mr27Over(B);return{keys:[...keys],rebuild};}
   finally{XART.get=get;s4RevivalClip1006=clip;}}''')
  check('authored energy-shield frames animate and reconstruction renders',len(art['keys'])>=8 and art['rebuild']>0,art)
  feedback=p.evaluate('''()=>{const n=B._s4war.shield.nodes[0];n.flash=0;
   function image(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);mr27Over(B);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
   const a=image(),hp=n.hp;B._phaseInvuln=0;B._noHit=false;_lastHitX=n.x;_lastHitY=n.y;_dmgBullet=null;bossHitTest(n.x,n.y);hitBoss(1);const c=image();let pixels=0;
   for(let i=0;i<a.length;i+=4)if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])pixels++;
   const result={pixels,flash:n.flash,hpLost:hp-n.hp};stage4ShieldTick(B,.5);result.expired=n.flash<=0;return result;}''')
  check('Real generator damage visibly flashes the objective plate',feedback['pixels']>10 and feedback['flash']>0 and feedback['hpLost']>0,feedback)
  check('Generator hit flash expires naturally',feedback['expired'],feedback)
  budgets=[]
  for diff in ['easy','normal','hard','furious']:
   setup(5,'chromehammer',diff);budget=p.evaluate('({hp:B.hp,max:B.maxhp})');budgets.append(budget['max'])
   check(diff+' Hammer HP budget is shorter',budget['hp']==budget['max'] and budget['max']=={'easy':1100,'normal':1700,'hard':1950,'furious':2200}[diff],budget)
  check('Hammer HP still increases with difficulty',budgets==sorted(budgets),budgets)
  setup(5,'chromehammer')
  p.wait_for_function('()=>{pxgWarm(5);return pxgKeys(5).every(k=>XART.rdy(k))}')
  p.evaluate('()=>{B.x=worldWidth()/2;B.y=B._drawY=230;B.enter=false;B._noHit=false;B.hp=B.maxhp*.6;fr27BeginArmor(B);B._hammer.frArmor.activated=true;B._noHit=false;fr27Restore(B,.1,false,false);B.flash=0;}')
  frames(110)
  check('Real Hammer recovery enters its authored raised charge',p.evaluate('B._hammer.state==="storm_raise"&&B._hammer.recovery.status==="charging"'))
  charge=p.evaluate('''()=>{const h=B._hammer;h.t=.05;const early=pxgHammerDrive(B);h.t=2.05;const late=pxgHammerDrive(B);return{early,late,head:hammerHeadPoint(B),keys:Object.keys(PXG.log)};}''')
  check('Hammer emissive pixels charge on the same ladder as the core',charge['late']['lights']==charge['late']['core'] and charge['late']['lights']>charge['early']['lights'],charge)
  snap('hammer-core-and-weapon-charge')
  pixel=p.evaluate('''()=>{const drive=pxgHammerDrive,di=ctx.drawImage,rows=[];const head=hammerHeadPoint(B),radius=46;
   function grab(lit){pxgHammerDrive=function(b){const a=drive(b);return{...a,lights:lit?.95:0};};
    ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);hammerBossDraw(B);ctx.restore();
    const x=Math.max(0,Math.round((head.x-camX-radius)*SS)),y=Math.max(0,Math.round((head.y-radius)*SS));return ctx.getImageData(x,y,Math.round(radius*2*SS),Math.round(radius*2*SS)).data;}
   try{const a=grab(false),off=cv.toDataURL().split(',')[1],b=grab(true),on=cv.toDataURL().split(',')[1];let changed=0,light=0;for(let i=0;i<a.length;i+=4)if(a[i]!=b[i]||a[i+1]!=b[i+1]||a[i+2]!=b[i+2]){changed++;light+=b[i]+b[i+1]+b[i+2]-a[i]-a[i+1]-a[i+2];}
    return{changed,light,head,off,on,drawn:Object.keys(PXG.log).filter(k=>k.includes('arch_')||k.includes('pt11_hammer'))};}finally{pxgHammerDrive=drive;ctx.drawImage=di;}}''')
  for name in ['off','on']:(O/('hammer-light-'+name+'.png')).write_bytes(base64.b64decode(pixel.pop(name)))
  check('Actual hammer-region pixels brighten with the weapon charge',pixel['changed']>10 and pixel['light']>0,pixel)
  hurt=p.evaluate('''()=>{B._hammer.frArmor.barrier=0;B._phaseInvuln=0;B._noHit=false;B.flash=0;
   function image(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);hammerBossDraw(B);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
   const a=image(),hp=B.hp,armor=B._hammer.frArmor.hp;_lastHitX=B.x;_lastHitY=B.y;_dmgBullet=null;bossHitTest(B.x,B.y);hitBoss(1);const c=image();let pixels=0;
   for(let i=0;i<a.length;i+=4)if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])pixels++;
   return{pixels,flash:B.flash,hpLost:hp-B.hp+armor-B._hammer.frArmor.hp};}''')
  check('Hammer native damage still flashes charging body pixels',hurt['pixels']>20 and hurt['flash']>0 and hurt['hpLost']>0,hurt)
  frames(30)
  check('Hammer charge hit flash expires naturally',p.evaluate('B.flash<=0'))
  check('No page, console or missing-asset errors',not errors,errors);browser.close()
except Exception as e:errors.append(str(e));print(traceback.format_exc(),flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,
  runtime_sha256={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['assets/game.js','assets/stage34_assault_1014.js','assets/gameplay_repair_1004.js','assets/balance_recovery_1007b.js','assets/pixel_glow_1015.js','assets/pixel_glow_art_1015.js']},
  scope='Native Chromium controlled fixtures, actual collision/damage and pixels; not a full human campaign balance playthrough.')
 (O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}),flush=True)
if errors or report['failed']:sys.exit(1)
