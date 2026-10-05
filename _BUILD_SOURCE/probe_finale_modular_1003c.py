"""Real Chromium rig/weapon/gauge checks; authored pixels through the game ctx."""
from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/finale_modular_1003c';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'forms':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n):
 for i in range(0,n,15):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(15,n-i));p.wait_for_timeout(8)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.add_init_script('(()=>{const d=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(){if(window.fmcCalls&&window.fmcKey&&typeof ctx!=="undefined"&&this===ctx)fmcCalls.push(fmcKey);return d.apply(this,arguments);};})()')
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate('()=>{r30Warm();window.fmcCalls=[];window.fmcKey=null;const c=fmcCell,r=r30Blit;fmcCell=function(s,k){fmcKey="fmc_"+s+":"+k;try{return c.apply(this,arguments);}finally{fmcKey=null;}};r30Blit=function(k){fmcKey="r30_"+k;try{return r.apply(this,arguments);}finally{fmcKey=null;}};}')
  p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))&&Object.keys(REALM30_ART).every(k=>XART.rdy("r30_"+k))',timeout=120000,polling=60)
  ck(p.evaluate('()=>Object.values(FMC_ART).every(a=>{const im=XART.get(a.key);return im.width===a.size[0]&&im.height===a.size[1];})'),'ten component/effect sources decode through XART')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{window.realFmcHit=playerHit;playerHit=function(){};window.fmcSounds={};const s=r30Sound;r30Sound=function(k){fmcSounds[k]=(fmcSounds[k]||0)+1;return s.apply(this,arguments);};}')
  for i in range(8):
   p.evaluate('(i)=>{B._r30.mode="takeover";B._r30.t=.30+i*.5+.20;}',i);shot(p,f'fill-{i+1}')
  ck(p.evaluate('()=>{const colors=[];for(let i=0;i<8;i++){B._r30.t=.30+i*.5+.20;const g=fmcGauge(B);if(Math.abs(g.frac-.5)>.001)return false;colors.push(g.color);}return new Set(colors).size===8;}'),'one gauge refills eight times in eight colors')
  ck(p.evaluate('()=>{B._r30.shield=0;let frames=0;const get=XART.get;XART.get=function(k){if(k==="bmbar_frame_boss")frames++;return get.apply(this,arguments);};try{drawHealthBarV2("boss",1,240,45,340,false,"test");}finally{XART.get=get;}return frames===1;}'),'exactly one boss gauge housing per draw')
  for form in range(8):
   p.evaluate('(n)=>{r30Clear(B);r30Form(B,n);B._r30.mode="fight";B._r30.cd=99;B.enter=false;player.x=worldWidth()/2;player.y=VH-110;camX=player.x-VW/2;player.invuln=0;powerups=[];}',form)
   shot(p,f'form-{form+1}-idle')
   data=p.evaluate('()=>({id:f1003bDef(B).id,parts:r30Parts(B).map(v=>({id:v.p.id,x:v.x,y:v.y,w:v.w,h:v.h,rot:v.rot})),book:f1003bDef(B).book})');report['forms'].append(data)
   ck(len(data['parts'])>=3,f'form {form+1} has independently positioned components')
   ck(p.evaluate('()=>{B.hp=B.maxhp*.37;const g=fmcGauge(B);B.hp=B.maxhp;return Math.abs(g.frac-.37)<1e-8&&g.color===f1003bDef(B).color;}'),f'form {form+1} gauge reads its own health and color')
   p.evaluate('()=>{const v=r30Parts(B).find(v=>v.p.id!=="core"&&v.p.id!=="rotor");window.component=v.p;window.componentBefore=v.p.hp;window.hpBefore=B.hp;pBullets.push({kind:"mg",_chaingun:true,x:v.x,y:v.y,vx:0,vy:0,w:6,h:10,dmg:12,t:0});}');frames(p,1)
   ck(p.evaluate('()=>component.hp<componentBefore&&B.hp<hpBefore'),f'form {form+1} real chaingun collision damages a component')
   p.evaluate('()=>{B._lastPart=component;modularHit(component.hp+1);}');shot(p,f'form-{form+1}-broken')
   ck(p.evaluate('()=>component.destroyed&&!r30Parts(B).some(v=>v.p===component)&&B.hp>0'),f'form {form+1} destroyed component disappears independently')
   p.evaluate('(n)=>{r30Form(B,n);B._r30.mode="fight";B.enter=false;}',form)
   for idx,attack in enumerate(data['book']):
    p.evaluate('(i)=>{r30Clear(B);B._r30.seq=i;r30Attack(B);window.attackFmc=B._r30.attack;window.peakFmc=0;window.movingFmc=false;window.startFmc=r30Parts(B).map(v=>[v.p.id,v.rot]);}',idx)
    taken=False
    for j in range(190):
     frames(p,5)
     q=p.evaluate('()=>{const P=B._r30.attack;peakFmc=Math.max(peakFmc,eBullets.filter(q=>q._finale1003b).length+S81003.beams.length+groundTargetingFx.filter(q=>!q.dead).length);movingFmc=movingFmc||r30Parts(B).some(v=>Math.abs(v.rot-(startFmc.find(a=>a[0]===v.p.id)?.[1]||0))>.02);return {active:P===attackFmc,t:P?.t||0,tell:P?.tell||0,phase:P?.k1003?.phase};}')
     if not taken and ((q['phase'] if 'phase' in q else None)=='slashTell' or (attack!='knight' and q['t']>.65*q['tell'] and q['t']<q['tell'])):
      shot(p,f'form-{form+1}-{attack}-charge');taken=True
     if not q['active']:break
    result=p.evaluate('()=>({done:B._r30.attack!==attackFmc,recovery:B._r30.cd,peak:peakFmc,moving:movingFmc,finite:r30Parts(B).every(v=>Number.isFinite(v.x+v.y+v.rot))})')
    ck(result['done'] and result['recovery']>0 and result['finite'],f'form {form+1} {attack} completes with recovery and finite rig')
    if attack not in ['talons','ram','stomp','knight']:ck(result['peak']>0,f'form {form+1} {attack} produces real hazards')
   # Destroy a laser weapon during its warning. It may neither fire nor retain a beam.
   if form in [0,2,3,4,6,7]:
    laser={0:'code',2:'furnaceBeam',3:'iceLance',4:'lightning',6:'carrierLance',7:'code'}[form]
    p.evaluate('(c)=>{r30Clear(B);r30Form(B,c.form);B._r30.mode="fight";B.enter=false;B._r30.seq=f1003bDef(B).book.indexOf(c.type);r30Attack(B);window.boundModule=B._r30.attack.lanes[0].module;B._lastPart=B.parts.find(p=>p.id===boundModule);modularHit(B._lastPart.hp+1);}',{'form':form,'type':laser})
    frames(p,110)
    ck(p.evaluate('()=>!B._r30.attack?.lanes.some(q=>q.module===boundModule)&&!S81003.beams.some(q=>q.owner===B&&q.module===boundModule)'),f'form {form+1} broken emitter cancels warning and beam')
  # Pixel-backed sword attachment, charge and actual blade collision.
  p.evaluate('()=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;r30Attack(B);s81003KnightEnter(B,"slashTell");B._r30.attack.k1003.age=.45;}');shot(p,'knight-head-and-powered-sword')
  ck(p.evaluate('()=>{const r=fmcRig(B),arm=r.find(v=>v.p.id==="swordArm"),sword=r.find(v=>v.p.id==="sword");return !!arm&&!!sword&&fmcCharge(B).frame>=3&&fmcCalls.includes("fmc_head:head")&&fmcCalls.some(k=>k.startsWith("fmc_sword_fx:"));}'),'separate head and power-up art draw with the moving sword')
  p.evaluate('()=>{s81003KnightEnter(B,"sweep");B._r30.attack.k1003.age=.10;const L=fmcBlade(B);player.x=(L.x+L.ex)/2;player.y=(L.y+L.ey)/2;window.swordHits=0;playerHit=()=>swordHits++;fmcBladeHit(B);}');ck(p.evaluate('()=>swordHits===1'),'powered sword damages on the actual moving blade')
  p.evaluate('()=>{B._r30.attack.k1003.hitSeats.clear();B._r30.attack.k1003.previousBlade=null;player.x=B.x+500;player.y=B.y+500;fmcBladeHit(B);}');ck(p.evaluate('()=>swordHits===1'),'sword does not use a remote target-circle hitbox')
  for phase in ['slash','jump','sweep']:
   result=p.evaluate('(phase)=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;r30Attack(B);const P=B._r30.attack,K=P.k1003;player.x=B.x;player.y=VH-120;K.target={x:player.x,y:player.y};K.from={x:B.x,y:B.y};K.x=B.x;K.y=phase==="sweep"?player.y-142:B.y;P.kSteps=[phase,"recover"];P.kIndex=0;s81003KnightEnter(B,phase);let hits=0;playerHit=(s)=>{if(s.startsWith("powered alien sword"))hits++;};for(let i=0;i<48&&K.phase===phase;i++)f1003bKnightTick(B,1/120);if(phase==="jump")for(let i=0;i<48&&K.phase===phase;i++)f1003bKnightTick(B,1/120);return hits;}',phase)
   ck(result>0,phase+' blade crosses the warned stationary target')
  p.evaluate('()=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;r30Attack(B);B._r30.shield=0;}')
  p.evaluate('()=>{B._lastPart=B.parts.find(p=>p.id==="swordArm");modularHit(B._lastPart.hp+1);}');shot(p,'knight-sword-arm-broken');ck(p.evaluate('()=>!fmcAlive(B,"sword")&&!B._r30.attack&&B._r30.cd>0'),'breaking sword arm removes sword and cancels its combo')
  # Ensure all lives, transformed rigs and final reward still progress once.
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'});p.evaluate('()=>{playerHit=function(){};B._r30.mode="fight";B.enter=false;window.startScoreFmc=run.score;}')
  for form in range(8):
   ck(p.evaluate('(n)=>B._r30.form===n&&r30Live(B)&&B.parts.every(p=>p.hp>0&&!p.destroyed)',form),f'progression enters intact modular form {form+1}')
   p.evaluate('()=>{B._lastPart=B.parts[0];modularHit(B.hp+1);}');frames(p,180 if form<7 else 950)
   if form<7:ck(p.evaluate('()=>run.score===startScoreFmc&&!bossDefeated'),f'no early reward after form {form+1}')
  ck(p.evaluate('()=>B._r30.rewarded&&B._r30.mode==="done"&&run._trueFinaleCleared&&state===GS.STAGECLEAR'),'one final portal/reunion reward after all eight lives')
  report['artCalls']=p.evaluate('()=>[...new Set(fmcCalls)]');report['sounds']=p.evaluate('()=>fmcSounds');report['errors']=errors;ck(not errors,'no page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}),flush=True);browser.close()
finally:stop()
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
