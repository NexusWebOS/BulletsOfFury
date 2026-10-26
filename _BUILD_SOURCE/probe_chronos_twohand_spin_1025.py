"""Whole original spin pixels, native contact/recoil and password owner checks."""
from pathlib import Path
import json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_twohand_spin_1025';O.mkdir(exist_ok=True);checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok: print(json.dumps(data),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();c27Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000)
  p.evaluate("()=>{window.seedMotion=(chrome=true)=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp=11220;b.x=340;b.y=260;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='hammer';h.t=0;h.mode='hammer';h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=h.c26Return=h.throw=h.whirl=null;h.c27Combo=null;h._hf22Charge=h._hj22Pair=h._hf22StormPair=null;h.hammerDestroyed=false;h._hf22Red=false;h.frArmor=chrome?{hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]}:null;debugUnlocked=true;DBGT.god=true;player.invuln=0;player.x=320;player.y=430;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedMotion();}")
  contact=Image.new('RGB',(1280,420*2),'#0b1421');d=ImageDraw.Draw(contact)
  for mi,mat in enumerate(['regular','chrome']):
   p.evaluate("""mat=>{seedMotion(mat!=='regular');boss._hammer._hf22Red=mat==='red';boss._hammer.c27RagePending=false;hammerWhirlStart(boss);boss._hammer.state='whirlwind';boss.x=340;boss.y=220;boss._drawY=boss.y;player.x=340;player.y=500;}""",mat)
   stats=[]
   for f in range(8):
    q=p.evaluate("""f=>{const b=boss,h=b._hammer;h.c26SpinClock=f;b.flash=0;b._gp4FlashNext=0;const ox=b.x,oy=b.y;b.x=cv.width/2;b.y=cv.height/2-40;const q=ha21Blue(b);ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ha21Body(b,q);let pixels=0;const data=ctx.getImageData(0,0,cv.width,cv.height).data;for(let i=0;i<data.length;i+=4)if(data[i]+data[i+1]+data[i+2]>45)pixels++;const tip=hammerHeadPoint(b);const a=ctx.getImageData(Math.round(tip.x)-5,Math.round(tip.y)-5,11,11).data;let atHead=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>90)atHead++;ctx.restore();b.x=ox;b.y=oy;drawWorld(0);return{pixels,atHead,key:q.a.key,tip,whole:q.a.wholeAuthored,hands:q.a.gripHands,frame:q.a.frame}}""",f)
    stats.append(q)
    if f in [0,2,4,6]:
     p.screenshot(path=str(O/(mat+'-whole-'+str(f)+'.png')))
     im=Image.open(O/(mat+'-whole-'+str(f)+'.png')).resize((320,200));contact.paste(im,(f//2*320,mi*420+24));d.text((f//2*320+10,mi*420+5),mat+' original frame '+str(f+1),fill='white')
    p.wait_for_timeout(5)
   ck(mat+' uses all eight complete original two-handed frames',all(q['pixels']>7000 and q['whole'] and q['hands']==2 for q in stats) and len({q['key'] for q in stats})==8,stats)
   ck(mat+' measured head is on real rendered hammer pixels',all(q['atHead']>20 for q in stats),[q['atHead'] for q in stats])
   q=p.evaluate("""()=>{const b=boss;b.flash=0;drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;markHit(b);drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,flash:b.flash}}""")
   ck(mat+' whole body and held hammer retain real hit flash',q['white']>100,q)
  contact.save(O/'native-whole-contact.png')
  p.evaluate("()=>{seedMotion();hammerWhirlStart(boss);boss._hammer.state='whirlwind';boss.x=340;boss.y=240;boss._hammer.whirl.y=240;boss._hammer.c26SpinClock=0;}")
  q=p.evaluate("""()=>{const b=boss,h=b._hammer,at=hammerHeadPoint(b),before=h.c26SpinClock;_dmgBullet={kind:'bullet',x:at.x,y:at.y};const hit=bossHitTest(at.x,at.y);if(hit){_lastHitX=at.x;_lastHitY=at.y;hitBoss(3)}_dmgBullet=null;return{hit,spinBefore:before,spinAfter:h.c26SpinClock,back:h.c26Backspin,state:h.state,destroyed:h.hammerDestroyed,knock:!!h.c25Knock,throw:!!h.throw}}""")
  ck('Shooting held hammer recoils the whole two-handed turn without detaching or stunning',q['hit'] and q['back']>0 and q['spinAfter']<q['spinBefore'] and not q['destroyed'] and not q['knock'] and not q['throw'] and q['state']=='whirlwind',q)
  for _ in range(6):p.evaluate(STEP,5);p.wait_for_timeout(3)
  ck('Hit flash expires during the native moving spin',p.evaluate('boss.flash<=0'))
  q=p.evaluate("""()=>{seedMotion();hammerWhirlStart(boss);const h=boss._hammer;h.state='whirlwind';h.t=.2;h.hitCd=0;h.c26SpinClock=0;boss.x=340;boss.y=h.whirl.y=230;boss._drawY=boss.y;const at=hammerHeadPoint(boss);DBGT.god=false;player.dead=false;player.invuln=0;run.shield=3;player.x=at.x;player.y=at.y;B20.events.length=0;hammerCombatTick(boss,1/60);return{shield:run.shield,events:B20.events,head:hammerHeadPoint(boss),player:{x:player.x,y:player.y}}}""")
  ck('Actual original hammer path damages the ship on contact',q['shield']<3,q)
  q=p.evaluate("""()=>{seedMotion();hammerWhirlStart(boss);const h=boss._hammer;h.state='whirlwind';h.t=.2;h.hitCd=0;h.c26SpinClock=0;boss.x=340;boss.y=h.whirl.y=230;DBGT.god=false;player.dead=false;player.invuln=0;run.shield=3;player.x=340;player.y=500;hammerCombatTick(boss,1/60);return run.shield}""")
  ck('Moving away from the hammer path avoids spin contact',q==3,q)
  q=p.evaluate("""()=>{seedMotion();boss._hammerTime={mode:'dance'};const dance=ha21Blue(boss);boss._hammerTime.mode='intro';const intro=ha21Blue(boss);delete boss._hammerTime;return{dance, intro}}""")
  ck('HAMMER entrance and dance keep their original owner',q['dance'] is None and q['intro'] is None,q)
  q=p.evaluate("""()=>{seedMotion();hammerWhirlStart(boss);boss._hammer.state='whirlwind';boss.x=340;boss.y=220;boss._drawY=boss.y;const trace=[],old=ctx.drawImage;ctx.drawImage=function(im,...args){const key=HA21.tags.get(im);if(key)trace.push(key);return old.call(this,im,...args)};try{drawWorld(0)}finally{ctx.drawImage=old}return trace.filter(k=>/c27_spin|blue_tool|arch_hammer$|arch_hammer_spin$|hammer_boomerang_hammer/.test(k))}""")
  ck('Native spin draws one intact actor and zero detached-tool overlays',len(q)==1 and q[0].startswith('c27_spin_'),q)
  p.evaluate("()=>{seedMotion();boss._hammer._hf22Red=true;c30Start(boss);}")
  ck('Permanent red rage remains unarmed',p.evaluate('c30Own(boss)&&boss._hammer.hammerDestroyed'))
  ck('No page or console errors',not errors,errors)
  br.close()
finally:stop()
result=dict(checks=checks,errors=errors,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks));(O/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps({'passed':result['passed'],'failed':result['failed']}));raise SystemExit(bool(result['failed']))
