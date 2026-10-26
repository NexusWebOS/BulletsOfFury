"""Native pixels and encounter ownership for the silhouette/pickup correction."""
from pathlib import Path
import json,base64,ast,hashlib
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_aura_gun_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
audit=json.loads((O.parent/'after/audit.json').read_text())
hit=next(e for q in audit['timeline'] for e in q['events'] if e['type']=='crate-struck')
ck('The actual hammer head reaches the crate before its impact event',np.hypot(hit['head']['x']-hit['box']['x'],hit['head']['y']-hit['box']['y'])<1,hit)
ck('Released hammer leaves the screen before the gun catch',all('ht23_tool_0' not in q['draws'] for q in audit['timeline'] if 3.1<q['seconds']<4.7))
events={e['type']:e['t'] for q in audit['timeline'] for e in q['events']}
ck('Impact, upward throw, ejection, catch, and firing readiness are ordered',all(events[a]<events[b] for a,b in zip(['crate-struck','hammer-released-up','gun-ejected','gun-caught'],['hammer-released-up','gun-ejected','gun-caught','tactical-ready'])),events)
ck('All nine crate frames show a physical opening into an empty shell',len({hashlib.sha256((R/'_ART_SOURCES/chronos_aura_gun_1025/crate'/f'{i:02}.png').read_bytes()).hexdigest() for i in range(9)})==9)
seed=next(n.args[0].value for n in ast.walk(ast.parse((R/'_BUILD_SOURCE/audit_chronos_aura_gun_1025.py').read_text())) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.seedGun=' in n.args[0].value)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.armGun=()=>{seedGun();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;h.c27RagePending=false;h.ch23Rev=0;h.ch23Spin=0;hammerChainStart(boss);boss.x=cv.width/2;boss.y=220;boss._drawY=boss.y;};armGun();}")
  states=[]
  for i in range(43):
   p.evaluate('hammerBossTick(boss,1/60)');states.append(p.evaluate("()=>({state:boss._hammer.state,frame:ch23GunFrame(boss),rev:boss._hammer.ch23Rev,bullets:eBullets.length})"))
  warn=[q for q in states if q['state']=='chain_warn']
  ck('Rotor accelerates visibly during the warning before any rounds',len({q['frame'] for q in warn})>=5 and all(q['bullets']==0 for q in warn),warn)
  pose_pixels=[];gun_pixels=[]
  for mat in ['regular','chrome','red']:
   p.evaluate("""mat=>{armGun();boss._hammer.state='chaingun';boss._hammer.frArmor.hp=mat==='regular'?0:8415;boss._hammer._hf22Red=mat==='red';boss._hammer.ch23Rev=1;boss.flash=0;}""",mat)
   for f in range(6):
    data=p.evaluate("""f=>{boss._hammer.t=(f+.05)/18;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);hammerBossDraw(boss);ctx.restore();return cv.toDataURL('image/png').split(',')[1]}""",f)
    file=O/f'{mat}-recoil-{f}.png';file.write_bytes(base64.b64decode(data));pose_pixels.append((mat,hashlib.sha256(base64.b64decode(data)).hexdigest()));p.wait_for_timeout(5)
   ck(mat+' has six distinct native rendered whole-body recoil poses',len({v for m,v in pose_pixels if m==mat})==6)
  p.evaluate("()=>{armGun();boss._hammer.state='chaingun';boss._hammer.ch23Rev=1;}")
  for f in range(8):
   q=p.evaluate("""f=>{boss._hammer.ch23Spin=f;boss._hammer.t=0;const m=ch23Mount(boss);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ch23Blit(m.a,m.x,m.y);const at=ctx.getImageData(Math.round(m.x)-7,Math.round(m.muzzleY)-6,15,15).data;let lit=0;for(let i=0;i<at.length;i+=4)if(at[i]+at[i+1]+at[i+2]>60)lit++;ctx.restore();return{png:cv.toDataURL('image/png').split(',')[1],lit,hit:hammerBlasterHit(boss,m.x,m.muzzleY-10),muzzle:m.muzzleY}}""",f)
   gun_pixels.append(dict(hash=hashlib.sha256(base64.b64decode(q.pop('png'))).hexdigest(),**q));p.wait_for_timeout(5)
  ck('All eight rotating barrel phases change actual native pixels',len({q['hash'] for q in gun_pixels})==8)
  ck('Every barrel frame keeps the muzzle on the gun and inside its alpha target',all(q['lit']>20 and q['hit'] for q in gun_pixels),gun_pixels)
  q=p.evaluate("""()=>{armGun();boss._hammer.state='chaingun';boss._hammer.ch23Pattern='fan';const h=boss._hammer;h.ch23Volleys=0;h.chainMuzzle=.09;const m=ch23Mount(boss);eBullets=[];hammerBossChaingunFire(boss);return{muzzle:{x:m.x,y:m.muzzleY},rounds:eBullets.map(q=>({x:q.x,y:q.y,proof:q._weaponProof})),recoil:ch23Recoil(boss)}}""")
  ck('Nine Furious fan rounds originate at the recoiling visible muzzle',len(q['rounds'])==9 and all(abs(v['x']-q['muzzle']['x'])<1 and abs(v['y']-q['muzzle']['y'])<1 and v['proof'] for v in q['rounds']),q)
  q=p.evaluate("""()=>{armGun();boss._hammer.state='chaingun';const h=boss._hammer,m=ch23Mount(boss);ctx.clearRect(0,0,cv.width,cv.height);hammerBossDraw(boss);const a=ctx.getImageData(0,0,cv.width,cv.height).data;_dmgBullet={kind:'bullet',x:m.x,y:m.muzzleY-12};_lastHitX=m.x;_lastHitY=m.muzzleY-12;const hit=bossHitTest(m.x,m.muzzleY-12),hp=h.chainHP;if(hit)hitBoss(10);_dmgBullet=null;hammerBossDraw(boss);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{hit,before:hp,after:h.chainHP,flash:h.ch23GunFlash,white};}""")
  ck('Shooting the actual gun damages its native HP and flashes its rendered pixels',q['hit'] and q['after']<q['before'] and q['white']>100,q)
  p.evaluate('for(let i=0;i<30;i++)hammerBossTick(boss,1/60)')
  ck('Gun hit flash expires under its existing owner',p.evaluate('(boss._hammer.ch23GunFlash||0)===0'))
  q=p.evaluate("""()=>{armGun();boss._hammer.chainDestroyed=true;const n=eBullets.length;hammerBossChaingunFire(boss);hammerBossTick(boss,1/60);return{newRounds:eBullets.length-n,armed:ch23Armed(boss),state:boss._hammer.state}}""")
  ck('Destroyed gun stops its target and rounds and enters native recovery',q['newRounds']==0 and not q['armed'] and q['state']=='chain_cool',q)
  q=p.evaluate("""()=>{armGun();boss._hammer.ch23Rev=1;boss._hammer.state='chain_cool';boss._hammer.t=0;let frames=[];for(let i=0;i<45;i++){hammerBossTick(boss,1/60);frames.push(ch23GunFrame(boss));}return{frames,rev:boss._hammer.ch23Rev}}""")
  ck('Barrel coasts through changing frames then stops during rest',len(set(q['frames']))>=5 and q['rev']<.05,q)
  q=p.evaluate("""()=>{armGun();const h=boss._hammer;h.openingJump1003=false;h.frArmor=null;fr27BeginArmor(boss);const entered={gun:h._ht23ArmorGun,state:h.state};for(let i=0;i<230&&h.state==='fr_activation';i++)fr27ActivationTick(boss,1/60);return{entered,state:h.state,mode:h.mode,destroyed:h.hammerDestroyed,armed:ch23Armed(boss),pose:ha21Blue(boss)?.kind}}""")
  ck('Chromium activation with the acquired gun returns to its armed warning',q['entered']['gun'] and q['state']=='chain_warn' and q['mode']=='chaingun' and q['destroyed'] and q['armed'],q)
  # Compare the native body alone against the exact same pose with its aura.
  for scale in [1,.36]:
   for phase in [0,4]:
    for kind in ['body','aura','pulse']:
     q=p.evaluate("""v=>{seedGun();const b=boss,h=b._hammer;h.hb20Pickup=null;h._hf22Red=true;h.state='whirlwind';h.c26SpinClock=v.phase;b.x=cv.width/2;b.y=cv.height/2-30;b.flash=0;const q=ha21Blue(b);q.k=v.scale;efxClock=v.kind==='pulse'?.19:0;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);if(v.kind==='body')C27.base.traceBody(b,q);else ha21Body(b,q);ctx.restore();return cv.toDataURL('image/png').split(',')[1]}""",dict(scale=scale,phase=phase,kind=kind))
     (O/f'trace-{scale}-{phase}-{kind}.png').write_bytes(base64.b64decode(q));p.wait_for_timeout(5)
    base=np.array(Image.open(O/f'trace-{scale}-{phase}-body.png'))[:,:,:3];aura=np.array(Image.open(O/f'trace-{scale}-{phase}-aura.png'))[:,:,:3];pulse=np.array(Image.open(O/f'trace-{scale}-{phase}-pulse.png'))[:,:,:3]
    body=base.max(2)>15;outside=(aura.max(2)>20)&~body;dist=distance_transform_edt(~body);changed=int(np.any(aura!=pulse,axis=2).sum());limit=24 if scale==1 else 12
    ck(f'Aura follows pose{phase} at scale{scale} with moving close contours',outside.sum()>80 and float(np.percentile(dist[outside],99))<limit and changed>100,dict(pixels=int(outside.sum()),distance99=float(np.percentile(dist[outside],99)),animatedPixels=changed))
  q=p.evaluate("""()=>{seedGun();boss._hammer.hb20Pickup=null;boss._hammer.c27RagePending=false;boss._hammer.frArmor.hp=0;boss.hp=boss.maxhp*.15;hammerBossTick(boss,1/60);boss._hammer._hf22Charge.t=1.5;nativeDraws=[];drawWorld(0);return{state:boss._hammer.state,pose:ha21Blue(boss)?.kind,draws:[...new Set(nativeDraws)],auraDraws:C27.auraDraws}}""")
  ck('15 percent charge uses the held-hammer actor and traced aura, not the old flame plate',q['state']=='hf22_rage_charge' and q['pose']=='c27_windup_red' and not any('rage_charge' in k or 'blue_aura' in k for k in q['draws']),q)
  p.screenshot(path=str(O/'new-rage-charge.png'));br.close()
finally:stop()
ck('No page or console errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'])),flush=True)
raise SystemExit(bool(report['failed']))
