"""Native visual audit of pickup, firing and pose-bound rage."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1]
O=R/'_shots/chronos_aura_gun_1025'/('after' if '--after' in sys.argv else 'before');O.mkdir(parents=True,exist_ok=True)
errors=[];shots=[];timeline=[]
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&ch23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000)
  p.evaluate("""()=>{window.seedGun=()=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp*.49;b.x=340;b.y=220;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='hammer';h.t=0;h.mode='hammer';h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=h.c26Return=h.throw=h.whirl=null;h.c27Combo=null;h._hf22Charge=h._hj22Pair=h._hf22StormPair=null;h.hammerDestroyed=h.hb20PickupDone=h.chainDestroyed=h._hf22Red=false;h.frArmor={hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[.75,.5,.35]};debugUnlocked=true;DBGT.god=true;player.invuln=0;player.x=340;player.y=480;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedGun();window.nativeDraws=[];const get=XART.get;XART.get=function(k){const im=get.apply(this,arguments);if(im)HA21.tags.set(im,k);return im;};const draw=ctx.drawImage;ctx.drawImage=function(im,...args){const k=HA21.tags.get(im);if(k&&/^(c2[567]|ht23|ch23|hf22|ha21|hb20|arch_)/.test(k))nativeDraws.push(k);return draw.call(this,im,...args);};hammerPhaseTwoStart(boss);}""")
  last=0
  for t in [0,.6,1.2,1.65,1.78,2.0,2.3,2.75,2.95,3.15,3.45,3.9,4.4,4.65,4.95,5.3,5.6,6,7,8,9,10,11,12]:
   for _ in range(round((t-last)*60)):
    p.evaluate(STEP,1)
   p.wait_for_timeout(20);last=t
   q=p.evaluate("""()=>{nativeDraws=[];drawWorld(0);const b=boss,h=b._hammer;return{state:h.state,t:h.t,pickup:h.hb20Pickup,pose:ha21Blue(b)?.kind,head:hammerHeadPoint(b),barrel:ch23GunFrame(b),rev:h.ch23Rev,spin:h.ch23Spin,armed:ch23Armed(b),draws:[...new Set(nativeDraws)],x:b.x,y:b.y,bullets:eBullets.length,events:HT23.events.slice(-6)}}""");q['seconds']=t;timeline.append(q)
   file=O/('gun-%04d.png'%round(t*100));p.screenshot(path=str(file));shots.append((file,f"{t:.2f}s {q['state']}"))
  p.evaluate("()=>{seedGun();boss.hp=boss.maxhp*.14;boss._hammer._hf22Red=true;boss._hammer.hammerDestroyed=false;boss._hammer.c27RagePending=false;hammerWhirlStart(boss);boss._hammer.state='whirlwind';boss.x=340;boss.y=260;boss._drawY=boss.y;}")
  for f in [0,2,4,6]:
   p.evaluate('f=>{boss._hammer.c26SpinClock=f;drawWorld(0)}',f);file=O/f'rage-{f}.png';p.screenshot(path=str(file));shots.append((file,f'Rage original spin {f}'))
  report=dict(timeline=timeline,errors=errors,gunEvents=p.evaluate('CH23.events'));(O/'audit.json').write_text(json.dumps(report,indent=2),encoding='utf8');br.close()
finally:stop()
out=Image.new('RGB',(1280,225*((len(shots)+3)//4)),'#101d2a');d=ImageDraw.Draw(out)
for i,(file,title) in enumerate(shots):
 im=Image.open(file).resize((320,200));x=i%4*320;y=i//4*225;out.paste(im,(x,y+25));d.text((x+6,y+5),title,fill='white')
out.save(O/'contact.png');print(json.dumps(dict(errors=errors,output=str(O))),flush=True)
