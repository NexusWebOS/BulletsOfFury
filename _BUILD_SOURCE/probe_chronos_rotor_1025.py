"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_rotor_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=true;h.state='hammer';h.hammerDestroyed=false;h.frArmor.hp=0;boss.hp=boss.maxhp*.15;}")
  for i in range(15):
   p.evaluate(STEP,20);p.wait_for_timeout(10);shot('live-charge-'+str(i))
  ck('Live clock completes charge, latches red and discards hammer',p.evaluate('boss._hammer._hf22Red&&!boss._hammer._hf22Charge&&boss._hammer.hammerDestroyed'))
  p.evaluate(STEP,70)
  q=p.evaluate("""()=>{const b=boss,a=ha21Blue(b),im=XART.get(a.a.key),c=document.createElement('canvas');c.width=a.a.w;c.height=a.a.h;const g=c.getContext('2d');g.drawImage(im,0,0);const data=g.getImageData(0,0,c.width,c.height).data;let point;for(let y=65;y<150&&!point;y++)for(let x=95;x<160;x++)if(data[(y*c.width+x)*4+3]>200){point={x:b.x+(x+.5-a.a.pivot[0])*a.k,y:b.y+(y+.5-a.a.pivot[1])*a.k};break;}const old=b.hp;_dmgBullet={kind:'bullet',...point};_lastHitX=point.x;_lastHitY=point.y;const hit=bossHitTest(point.x,point.y);if(hit)hitBoss(8);_dmgBullet=null;return{hit,before:old,after:b.hp,flash:b.flash,point,weapon:hammerWeaponTargetable(b)}}""")
  ck('Scaled red actor takes real pixel hits and flashes without ghost hammer',q['hit'] and q['after']<q['before'] and q['flash']>0 and not q['weapon'],q);shot('red-hit')
  p.evaluate(STEP,20);ck('Red hit flash expires',p.evaluate('boss.flash<=0'));shot('red-expired')
  p.evaluate("()=>{const h=boss._hammer;h.c30.phase='beam';h.c30.t=.35;h.c30.lock={x:player.x,y:player.y};h.c30.hit=new Set();DBGT.god=false;player.invuln=0;window.beforeBeamHP=player.hp;hammerBossTick(boss,1/60);}")
  q=p.evaluate('({before:beforeBeamHP,after:player.hp,invuln:player.invuln,hit:boss._hammer.c30.hit.size,dead:player.dead})');ck('Committed energy wave reaches native player damage',q['hit']>0 and (q['invuln']>0 or q['dead']),q)
  p.evaluate('DBGT.god=true;fresh();boss._hammer.hb20Pickup=null;boss._hammer.hb20PickupDone=true;hammerState(boss,"giant_idle")')
  land=[]
  for i in range(20):
   p.evaluate(STEP,20);p.wait_for_timeout(5)
   q=p.evaluate('({state:boss._hammer.state,warn:C30.lastLanding})');land.append(q)
   if q['state'] in ['giant_warn','giant_dive']:shot('landing-'+str(i))
  ck('Native background jump restores landing FOV before impact',any(q['state']=='giant_warn' and q['warn']for q in land),land)
  p.evaluate('armGun();boss._hammer.ch23Rev=1')
  q=p.evaluate("""()=>{const hashes=[];for(let i=1;i<=16;i++){const a=c30Row('rotor',i),im=XART.get(a.key),c=document.createElement('canvas');c.width=104;c.height=208;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(28,150,48,50).data;let h=2166136261;for(const v of d)h=Math.imul(h^v,16777619);hashes.push(h)}return new Set(hashes).size}""");ck('All sixteen muzzle faces contain different rotational pixels',q==16,q)
  p.evaluate(STEP,200);shot('gun-live')
  q=p.evaluate("""()=>{const b=eBullets.find(q=>q._c30Slug);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='black';ctx.fillRect(0,0,80,80);ch23BulletDraw({...b,x:40,y:40});const a=ctx.getImageData(0,0,80,80).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>60)n++;ctx.restore();return n}""");ck('Slug renderer draws visible authored projectile pixels',q>60,q)
  p.evaluate('armGun();c31Warm();boss._hammer.ch23Rev=1')
  for i in range(0,36,3):
   p.evaluate('i=>{boss._hammer.c31Angle=i*Math.PI/18;boss._hammer.chainMuzzle=0;}',i);shot('rotation-'+str(i))
  q=p.evaluate("""()=>{const source=C31.get.call(XART,'c30_rotor_0'),a=C31Texture.rotor(source,0),b=C31Texture.rotor(source,Math.PI*2),data=c=>c.getContext('2d').getImageData(0,0,104,208).data;const x=data(a),y=data(b);let n=0;for(let i=0;i<x.length;i++)if(x[i]!==y[i])n++;return n}""");ck('Full 360-degree rotation returns to the same authored pixels',q==0,q)
  p.evaluate("boss._hammer.state='chaingun';boss._hammer.chainMuzzle=.065");shot('golden-muzzle')
  ck('Native firing draws the larger muzzle flash at the bore plane',p.evaluate('!!C31.lastMuzzle&&Math.abs(C31.lastMuzzle.y-ch23Mount(boss).muzzleY)<1'))
  q=p.evaluate("""()=>{const im=XART.get('c30_wave_3'),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const a=g.getImageData(0,0,c.width,c.height).data;let red=0,blue=0,white=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>50){if(a[i]>a[i+2]+40)red++;if(a[i+2]>a[i]+40)blue++;if(a[i]>210&&a[i+1]>200&&a[i+2]>200)white++;}return{red,blue,white}}""");ck('Wave has red energy and a white core, with no blue energy pixels',q['red']>1000 and q['blue']==0 and q['white']>100,q)
  ck('No page or console errors',not errors,errors)
  br.close()
finally:stop()
contact=Image.new('RGB',(1280,225*((len(shots)+3)//4)),'#102030');d=ImageDraw.Draw(contact)
for i,(file,name) in enumerate(shots):contact.paste(Image.open(file).resize((320,200)),(i%4*320,i//4*225+25));d.text((i%4*320+4,i//4*225+4),name,fill='white')
contact.save(O/'contact.png');(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');print(json.dumps(dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks))),flush=True)

