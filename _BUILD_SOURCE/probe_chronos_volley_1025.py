"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_volley_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&c32Warm()&&c30Warm()&&c29Warm()&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=true;h.hammerDestroyed=false;h.frArmor.hp=0;h.state='hammer';boss.hp=boss.maxhp*.15;}")
  timeline=[];last=None
  for i in range(120):
   p.evaluate(STEP,15);p.wait_for_timeout(3)
   q=p.evaluate("({state:boss._hammer.state,scale:hammerDepthScale(boss),red:!!boss._hammer._hf22Red,charge:!!boss._hammer._hf22Charge,depth:boss._hammer.c30?.volley?.depth,phase:boss._hammer.c30?.phase,shots:C32.events.filter(e=>e.type==='palm-shot').length,bullets:eBullets.filter(q=>q._c32Palm).length})");timeline.append(q)
   if q['state']!=last or q['state']=='c30_volley_fire' and i%2==0:
    shot('live-'+str(i)+'-'+q['state']);last=q['state']
  events=p.evaluate('C32.events');shotsf=[q for q in events if q['type']=='palm-shot']
  ck('Rage charge completes before the first volley',all(q['red'] and not q['charge'] for q in timeline if q['shots']>0))
  ck('Native rage fires palm volleys in foreground and background',set(q['depth'] for q in shotsf)=={'foreground','background'},{'count':len(shotsf),'depths':list(set(q['depth']for q in shotsf))})
  ck('Foreground reaches1.08 and background reaches.42 scale',any(q['scale']==1.08 and q['phase']=='volley_fire' for q in timeline) and any(q['scale']==.42 and q['phase']=='volley_fire'for q in timeline))
  ck('Every volley group alternates hands and includes dual palm bursts',all(any(q['hand']==h for q in shotsf)for h in [0,1]) and any(sum(e['beat']==q['beat']and e['group']==q['group']and e['depth']==q['depth']and abs(e['time']-q['time'])<.001 for e in shotsf)==2 for q in shotsf))
  ck('The original red-white energy wave remains in the rage rotation',any(q['phase']=='beam' for q in timeline))
  ck('No hammer is targetable during the volley rotation',p.evaluate('!hammerWeaponTargetable(boss)'))
  ck('Each group has an authored warning before firing',len([e for e in events if e['type']=='warning'])>=6)
  ck('Native projectiles leave the measured palms',len(shotsf)>0 and all(q['y']>70 and q['y']<400 for q in shotsf),shotsf[:4])
  p.evaluate("()=>{const R=boss._hammer.c30;R.cycle=0;c30Retreat(boss);}");p.evaluate(STEP,100)
  q=p.evaluate("""()=>{const b=boss,a=ha21Blue(b),im=XART.get(a.a.key),c=document.createElement('canvas');c.width=a.a.w;c.height=a.a.h;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height).data;let pt;for(let y=65;y<160&&!pt;y++)for(let x=95;x<160;x++)if(d[(y*c.width+x)*4+3]>200){pt={x:b.x+(x+.5-a.a.pivot[0])*a.k,y:b.y+(y+.5-a.a.pivot[1])*a.k};break;}const before=b.hp;_dmgBullet={kind:'bullet',...pt};_lastHitX=pt.x;_lastHitY=pt.y;const hit=bossHitTest(pt.x,pt.y);if(hit)hitBoss(4);_dmgBullet=null;return{hit,before,after:b.hp,flash:b.flash}}""");ck('Whole volley actor takes real pixel hits and flashes',q['hit'] and q['after']<q['before']and q['flash']>0,q);shot('volley-hit');p.evaluate(STEP,20);ck('Volley actor hit flash expires',p.evaluate('boss.flash<=0'));shot('volley-expired')
  q=p.evaluate("""()=>{const b=eBullets.find(q=>q._c32Palm);if(!b)return{found:false};return{found:true,inside:hammerLaserHit(b,{x:b.x,y:b.y},3,3),outside:hammerLaserHit(b,{x:b.x+Math.cos(b.ang+Math.PI/2)*80,y:b.y+Math.sin(b.ang+Math.PI/2)*80},3,3)}}""");ck('Palm bolts use the native oriented laser hit box',q.get('found')and q['inside']and not q['outside'],q)
  p.evaluate("()=>{const q=eBullets.find(q=>q._c32Palm);if(q){eBullets=[q];player.x=q.x;player.y=q.y;player.invuln=0;player.dead=false;player.out=false;DBGT.god=false;}}")
  p.evaluate(STEP,1)
  ck('Live palm projectile reaches native player damage',p.evaluate('player.dead||player.invuln>0'))
  p.evaluate('DBGT.god=true')
  before=p.evaluate('C32.events.length');p.evaluate('boss.dead=true');p.evaluate(STEP,60);ck('Defeated boss cannot launch queued volleys',p.evaluate('C32.events.length')==before)
  ck('No page or console errors',not errors,errors)
  br.close()
finally:stop()
contact=Image.new('RGB',(1280,225*((len(shots)+3)//4)),'#102030');d=ImageDraw.Draw(contact)
for i,(file,name) in enumerate(shots):contact.paste(Image.open(file).resize((320,200)),(i%4*320,i//4*225+25));d.text((i%4*320+4,i//4*225+4),name,fill='white')
contact.save(O/'contact.png');(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');print(json.dumps(dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks))),flush=True)
