"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_beam_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
src=ast.parse((R/'_BUILD_SOURCE/audit_chronos_aura_gun_1025.py').read_text(encoding='utf8'))
seed=next(n.args[0].value for n in ast.walk(src) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.seedGun=' in n.args[0].value)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c30Warm();c29Warm();bi24Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&c30Warm()&&c29Warm()&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p.evaluate('armGun()')
  samples=[]
  for sec in range(16):
   p.evaluate('for(let i=0;i<60;i++)hammerBossTick(boss,1/60)');p.wait_for_timeout(5)
   samples.append(p.evaluate('({state:boss._hammer.state,rate:boss._hammer.shotCd,gunTime:boss._hammer.c29GunTime,hp:boss._hammer.chainHP})'))
   if sec in [0,5,14]:shot('gun-'+str(sec))
  ck('Intact gun stays firing for 16 seconds without casting or cooldown',all(v['state']=='chaingun' for v in samples),samples)
  q=p.evaluate('C29.events.filter(e=>e.type==="gun-shot").map(e=>e.interval)')
  ck('Minigun accelerates from .18 toward .045 seconds between shots',len(q)>100 and q[-1]<.05 and q[0]>.16,dict(first=q[:3],last=q[-3:],shots=len(q)))
  ck('Health bar is positioned above the actual gun',p.evaluate('C29.bar.y<ch23Mount(boss).top&&C29.bar.hp===boss._hammer.chainHP'))
  q=p.evaluate("""()=>{const b=boss,h=b._hammer,t=retinaBossTargets(b).find(t=>t._retinaId==='chaingun'),before=h.chainHP;if(t)retinaMissileDamage(t,30,{kind:'retinaMissile',x:t.x,y:t.y});return{target:!!t,valid:t&&retinaTargetValid(t),before,after:h.chainHP}}""")
  ck('Retina acquires the gun and its missile damages gun HP',q['target'] and q['valid'] and q['after']<q['before'],q)
  q=p.evaluate("""()=>{const b=boss,h=b._hammer,m=ch23Mount(b);_dmgBullet={kind:'bullet',x:m.x,y:m.muzzleY-12};_lastHitX=m.x;_lastHitY=m.muzzleY-12;const hit=bossHitTest(m.x,m.muzzleY-12);if(hit)hitBoss(2000);_dmgBullet=null;return{hit,state:h.state,dead:h.chainDestroyed,reason:h.c29Break?.reason,armed:ch23Armed(b),hp:h.chainHP}}""")
  ck('Actual gun hit destroys only its module and enters gun-break stun',q['hit'] and q['dead'] and q['reason']=='gun' and not q['armed'],q)
  ck('Destroyed gun is immediately removed from Retina targets',p.evaluate('!retinaBossTargets(boss).some(t=>t._retinaId==="chaingun"&&!t.dead)'))
  p.evaluate(STEP,20)
  ck('Gun-break damage flash expires in the live game clock',p.evaluate('boss.flash<=0'))
  for t in [.2,.8,2.5,3.7,4.2]:
   p.evaluate('t=>{boss._hammer.c29Break.t=t;boss._hammer.t=t;}',t);shot('gun-break-'+str(t))
  p.evaluate('hammerBossTick(boss,.3)')
  ck('Gun break recovers to held hammer, not casting',p.evaluate('!boss._hammer.c29Break&&!boss._hammer.hammerDestroyed&&boss._hammer.state==="hammer"'))
  p.evaluate("()=>{fresh();const h=boss._hammer;h.frArmor.hp=1;h.hb20Pickup=null;h.hb20PickupDone=true;h.hammerDestroyed=false;h.state='hammer';h.mode='hammer';b20Cue('shieldUp');_dmgBullet={kind:'bullet'};boss._hammerModuleHit=null;window.armorDamage=hammerBossDamage(boss,200);_dmgBullet=null;}")
  q=p.evaluate('({hp:boss._hammer.frArmor.hp,state:boss._hammer.state,reason:boss._hammer.c29Break?.reason,damage:armorDamage})');ck('Chromium depletion enters an energy-break stun',q['hp']==0 and q['reason']=='armor',q)
  for t in [.1,.6,2,3.9]:
   p.evaluate('t=>{boss._hammer.c29Break.t=t;boss._hammer.t=t;}',t);shot('armor-break-'+str(t))
  p.evaluate('hammerBossTick(boss,.6)');ck('Armor break recovery remains regular armor',p.evaluate('!boss._hammer.c29Break&&c27Material(boss)==="regular"'))
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=true;h.state='hammer';h.hammerDestroyed=false;fr27Restore(boss,.1,false,false);}")
  p.evaluate('for(let i=0;i<90;i++)hammerBossTick(boss,1/60)');shot('shield-charge')
  q=p.evaluate('({state:boss._hammer.state,pose:ha21Blue(boss)?.kind,head:hammerHeadPoint(boss),top:viewTopY()})');ck('Shield uses original two-handed overhead pose with visible hammer',q['pose'].startswith('c29_hold') and q['head']['y']>q['top']+55,q)
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=true;h.hammerDestroyed=false;h.frArmor.hp=0;h.state='hammer';boss.hp=boss.maxhp*.15;hammerBossTick(boss,1/60);}")
  keys=[]
  for i in range(10):
   p.evaluate('for(let i=0;i<28;i++)hammerBossTick(boss,1/60)');keys.append(p.evaluate('ha21Blue(boss)?.a.key'));shot('rage-'+str(i))
  ck('Transformation plays distinct body acting before permanent red armor',len(set(keys))>=7,keys)
  p.evaluate('for(let i=0;i<30;i++)hammerBossTick(boss,1/60)');ck('Red armor latches only after full charge',p.evaluate('boss._hammer._hf22Red&&!boss._hammer._hf22Charge'))
  q=p.evaluate("({state:boss._hammer.state,hammer:boss._hammer.hammerDestroyed,scale:hammerDepthScale(boss),pose:ha21Blue(boss).kind})")
  ck('Rage permanently discards hammer and retreats into depth',q['hammer'] and q['state'].startswith('c30_'),q)
  states=[]
  for i in range(36):
   p.evaluate(STEP,20);p.wait_for_timeout(5)
   q=p.evaluate("({state:boss._hammer.state,scale:hammerDepthScale(boss),key:ha21Blue(boss).a.key,weapon:hammerWeaponTargetable(boss),beam:C30.lastBeam})");states.append(q)
   if i%3==0:shot('wave-'+str(i))
  ck('Rage uses whole unarmed gather, thrust, wave and recovery',all(not q['weapon'] for q in states) and len(set(q['state'] for q in states))>=4,states)
  ck('Background casting reaches .42 scale and renders a committed wave',any(q['scale']==.42 and q['beam'] for q in states))
  p.evaluate('armGun()');p.evaluate(STEP,240);shot('visible-slugs')
  q=p.evaluate("({fixed:ch23BodyFrame(boss),frames:C30_ART.banks.rotor.length,slugs:eBullets.filter(q=>q._c30Slug).map(q=>({w:q.w,h:q.h,x:q.x,y:q.y}))})")
  ck('Fixed hand pose and 16 physical rotating barrel phases',q['fixed']==0 and q['frames']==17,q)
  ck('Native minigun emits visible slug-sized projectiles',len(q['slugs'])>0 and all(b['w']==10 and b['h']==24 for b in q['slugs']),q)
  ck('No page or console errors',not errors,errors)
  br.close()
finally:stop()
contact=Image.new('RGB',(1280,225*((len(shots)+3)//4)),'#102030');d=ImageDraw.Draw(contact)
for i,(file,name) in enumerate(shots):contact.paste(Image.open(file).resize((320,200)),(i%4*320,i//4*225+25));d.text((i%4*320+4,i//4*225+4),name,fill='white')
contact.save(O/'contact.png');(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');print(json.dumps(dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks))),flush=True)
