"""Native flight observation; damage and destroyed-claw fixtures are labelled."""
from barrage_review_common_1025 import ROOT,boot,advance
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json

O=ROOT/'_shots/herald_speed_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];runs=[];shots=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
def shot(p,name):
 p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  for diff in ['furious','hard','normal']:
   p=boot(bc,port,8,errors)
   if diff!='furious':
    p.evaluate("""d=>{diffKey=d;debugStartFight(debugFightFor(8,'mini'),{pilot:'cole'});spawnSubBoss(debugFightFor(8,'mini').kind);debugFight.spawned=true;warnT=0;DBGT.god=true;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;window.reviewActor=subBoss;}""",diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&XART.rdy(HB25_ART.key)}',timeout=180000)
   p.evaluate("""()=>{HB25.events=[];window.birthAudit=[];const release=hb25BombDrop;hb25BombDrop=function(b,Q,P){const m=hd1003Muzzle(b,P.id),before=eBullets.length;const r=release.apply(this,arguments);if(eBullets.length>before){const q=eBullets.at(-1);birthAudit.push({id:P.id,time:efxClock,pass:Q.pass,phase:Q.phase,x:q.x,y:q.y,vx:q.vx,vy:q.vy,bottomX:q.x+q.vx*(VH-38-q.y)/q.vy,error:Math.hypot(q.x-m.x,q.y-m.y),proof:!enemyOrdnanceCanIntercept(q)&&!q._shootable&&!enemyDefensiveProof(q),target:P.target,burst:P.burst});}return r;};}""")
   initial=p.evaluate('reviewActor.hp')
   ck(diff+' reaches its bomber through the native attack book',advance(p,"reviewActor._hd1003._hb25?.kind==='bomber'&&reviewActor._hd1003._hb25.phase==='tell'",900,3))
   plan=p.evaluate("""()=>{const Q=reviewActor._hd1003._hb25;return{duration:Q.duration,interval:Q.interval,warm:Q.warm,escapeX:Q.escapeX,plan:Q.plan};}""")
   ck(diff+' warns the committed drop carpet before any release',plan['warm']>=1.05 and not p.evaluate('birthAudit.length'))
   ck(diff+' plans rapid drops from both living claws',len(plan['plan'])>=8 and set(q['id']for q in plan['plan'])=={'gunL','gunR'},plan)
   ck(diff+' keeps a committed opening through the falling carpet',all(q['burst']or abs(q['target']['x']-plan['escapeX'])>=52 for q in plan['plan']))
   seen=set();peak=0;trace=[]
   if diff=='furious':shot(p,'furious-complete-pass-warning')
   for i in range(800):
    p.evaluate(STEP,1)
    q=p.evaluate("""()=>{const Q=reviewActor._hd1003._hb25;return{time:efxClock,phase:Q?.phase,pass:Q?.pass,x:reviewActor.x,y:reviewActor.y,visible:reviewActor.x>camLeftX()+viewW()*.3&&reviewActor.x<camLeftX()+viewW()*.7,live:eBullets.filter(q=>q._hb25Chaos&&!q.dead).length,births:birthAudit.length,done:HB25.events.some(e=>e.event==='flight-complete'&&e.kind==='bomber')};}""")
    peak=max(peak,q['live']);trace.append(q)
    label='pass-'+str(q.get('pass'))
    if diff=='furious'and q.get('phase')=='strike'and q['visible']and label not in seen:seen.add(label);shot(p,'furious-'+label+'-rapid-drops')
    if diff=='furious'and p.evaluate("HB25.events.some(e=>e.event==='bomb-burst')")and'burst'not in seen:seen.add('burst');shot(p,'furious-red-bomb-bursts')
    if q['done']:break
    if i%12==0:p.wait_for_timeout(1)
   ev=p.evaluate('HB25.events');births=p.evaluate('birthAudit')
   strikes=[e for e in ev if e['event']=='flight-phase'and e.get('phase')=='strike']
   swoop=next(e for e in strikes if e.get('kind')=='swoop');bombers=[e for e in strikes if e.get('kind')=='bomber']
   ck(diff+' bomber matches the actual corner-flight speed',bool(bombers)and all(abs(e['speed']-swoop['speed'])<.001 for e in bombers),{'swoop':swoop,'bombers':bombers})
   ck(diff+' completes every fast pass and returns to native combat',q['done']and len(bombers)==(1 if diff=='normal'else 2))
   ck(diff+' releases at least eight red projectiles per pass',bool(births)and all(sum(q['pass']==i for q in births)>=8 for i in range(len(bombers))),{'counts':[sum(q['pass']==i for q in births)for i in range(len(bombers))]})
   ck(diff+' rapid releases stay on the actual claw apertures',bool(births)and all(q['error']<.001 and q['phase']=='strike'for q in births))
   ck(diff+' falling streams keep the escape opening at player height',all(q['burst']or q['vy']>0 and abs(q['vx'])<.00001 and abs(q['bottomX']-plan['escapeX'])>=44 for q in births))
   ck(diff+' drop and burst rounds remain bounded and unshootable',0<peak<=128 and all(q['proof']for q in births),peak)
   ck(diff+' bombs visibly burst while retaining the committed escape sector',any(e['event']=='bomb-burst'and e['half']>=.32 for e in ev))
   ck(diff+' observation preserves the complete native HP pool',p.evaluate('reviewActor.hp')==initial,initial)
   runs.append({'difficulty':diff,'plan':plan,'events':ev,'births':births,'peakLive':peak,'trace':trace})
   if diff=='furious':
    # Explicit native-damage fixture on a fast moving claw, separate from observation.
    p.evaluate("hb25Flight(reviewActor,'bomber')")
    advance(p,"reviewActor._hd1003._hb25?.phase==='strike'&&reviewActor.x>camLeftX()+viewW()*.35&&reviewActor.x<camLeftX()+viewW()*.65",350,1)
    d=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;hd1003Hit(reviewActor,1,0,0,'gunL');drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<z.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return white;}""")
    ck('Fast moving Herald claw still renders white damaged pixels',d>4,d);shot(p,'furious-native-claw-hit')
    p.evaluate(STEP,20);ck('Fast flight preserves native hit-flash expiry',p.evaluate("hd1003Part(reviewActor,'gunL').flash<=0"))
    p.evaluate("window.brokenAt=efxClock;hd1003Hit(reviewActor,hd1003Part(reviewActor,'gunL').hp+2,0,0,'gunL')")
    p.evaluate(STEP,240)
    ck('A broken claw cancels its planned drops and surviving projectiles',p.evaluate("!birthAudit.some(q=>q.id==='gunL'&&q.time>brokenAt)&&!eBullets.some(q=>q._hb25Chaos&&!q.dead&&q._heraldPart1003==='gunL')"))
    d=p.evaluate("""async()=>{const c=Snd._audioCtx();await c.resume();const out=[];for(const key of ['bossfireVileexistence','combatOrb0927','jetDash','bossWeaponCharge']){const b=await c.decodeAudioData(await(await fetch(BOFA.sfx[key])).arrayBuffer());let peak=0;for(const v of b.getChannelData(0))peak=Math.max(peak,Math.abs(v));out.push({key,peak,duration:b.duration});}return out;}""")
    ck('Rapid launch, burst, flight and charge sound routes decode audibly',all(x['peak']>.01 and x['duration']>0 for x in d),d)
   p.close()
  br.close()
finally:stop()
ck('Native Chromium has no page or console errors',not errors,errors)
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,runs=runs),indent=2),encoding='utf8')
if shots:
 im=Image.new('RGB',(1280,((len(shots)+2)//3)*285),(5,10,17));g=ImageDraw.Draw(im)
 for i,(f,n)in enumerate(shots):im.paste(Image.open(f).convert('RGB').resize((426,266)),((i%3)*426,(i//3)*285));g.text(((i%3)*426+3,(i//3)*285+266),n,fill='white')
 im.save(O/'contact.jpg')
print(json.dumps({'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)}),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
