"""Native Event Horizon observation and labelled damage/clear fixtures."""
from barrage_review_common_1025 import ROOT,boot,advance
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from pathlib import Path
import json,base64

O=ROOT/'_shots/horizon_assault_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];runs=[]
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
def shot(p,name):
 p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  for diff in ['normal','hard','furious']:
   p=boot(bc,port,9,errors)
   if diff!='furious':
    p.evaluate("""d=>{diffKey=d;debugStartFight(debugFightFor(9,'mini'),{pilot:'cole'});spawnSubBoss(debugFightFor(9,'mini').kind);debugFight.spawned=true;warnT=0;DBGT.god=true;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;window.reviewActor=subBoss;}""",diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s5924Ready("black_spin")&&XART.rdy("bf22_water_orb")}',timeout=180000)
   p.evaluate('EH25.events=[];BH25.events=[];S5924.shots=[]');initial=p.evaluate('({hp:reviewActor.hp,maxhp:reviewActor.maxhp})');states=[];seen=set();birthproof=True
   for i in range(1100):
    p.evaluate(STEP,3)
    q=p.evaluate("""()=>{const b=reviewActor,H=b._eh25,Q=b._s9rift.s5924;return{x:b.x,y:b.y,eye:s5924Eye(b),mode:Q.mode,t:Q.t,enter:b.enter,spin:H.spin,spinning:H.spinning,rps:H.rps,frame:H.frame,bomb:H.bomb?.phase,bombT:H.bomb?.t,rounds:eBullets.filter(q=>q._eh25Owner===b&&!q.dead).length,hp:b.hp,complete:EH25.events.filter(e=>e.event==='bomb-complete').length};}""");states.append(q)
    if q['rounds']:birthproof=birthproof and p.evaluate("eBullets.filter(q=>q._eh25Owner&&!q.dead).every(q=>!enemyOrdnanceCanIntercept(q)&&!q._shootable&&!enemyDefensiveProof(q))")
    if diff=='furious':
     name='bomb-'+str(q.get('bomb'))
     if q.get('bomb')=='charge':name+='-'+('peak'if q.get('bombT',0)>1.2 else'early')
     if q.get('bomb')and name not in seen:seen.add(name);shot(p,diff+'-'+name)
     if q['spinning']and 'spin'not in seen:seen.add('spin');shot(p,'furious-fast-spin')
     if q['y']>295 and 'low'not in seen:seen.add('low');shot(p,'furious-low-pass')
     if q['y']<180 and not q['enter']and 'high'not in seen:seen.add('high');shot(p,'furious-high-pass')
    if q['complete']>=2:break
    if i%12==0:p.wait_for_timeout(1)
   active=[s for s in states if not s['enter']];ev=p.evaluate('EH25.events');natives=p.evaluate('S5924.shots');runs.append(dict(difficulty=diff,initial=initial,states=states,events=ev))
   ck(diff+' completes two charged energy bomb turns naturally',sum(e['event']=='bomb-complete'for e in ev)>=2)
   ck(diff+' flies up and down across a substantial vertical range',max(s['y']for s in active)-min(s['y']for s in active)>95,{'min':min(s['y']for s in active),'max':max(s['y']for s in active)})
   ck(diff+' physical core, eye and drawn hull stay aligned',all(abs(s['y']-s['eye']['y'])<.01 for s in active))
   ck(diff+' fast spin clock is independent of the barrage duration',any(s['spinning']for s in active)and max(s['rps']for s in active)>1.5,max(s['rps']for s in active))
   ck(diff+' native renderer cycles at least eight authored spin poses in half a second',any(all(v['spinning']for v in active[i:i+11])and len({v.get('frame',{}).get('frame')for v in active[i:i+11]})>=8 for i in range(max(0,len(active)-10))))
   ck(diff+' preserves the native complete HP pool while fire is withheld',all(s['hp']==initial['hp']for s in states),initial)
   ck(diff+' energy bombs reject offensive interception and allow defensive clears',birthproof and any(s['rounds']for s in active))
   ck(diff+' bomb aim locks with a visible reaction window before launch',any(e['event']=='bomb-aim-locked'and e['remaining']>.9 for e in ev))
   ck(diff+' bomb releases from the current eye and reaches its committed impact',any(e['event']=='bomb-release'for e in ev)and any(e['event']=='bomb-impact'for e in ev),ev[:4])
   if diff!='furious':p.close();continue
   # Explicit native damage fixture; compare real pixels and native expiry.
   advance(p,'!reviewActor._eh25.bomb',100,3)
   d=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,b=reviewActor,eye=s5924Eye(b),hp=b.hp;s9VoidHorizonHit(b,1,eye.x,eye.y);drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<z.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,damage:hp-b.hp,flash:b._s9rift.core.flash};}""")
   ck('Fast-spinning native hull visibly flashes when actually damaged',d['white']>30 and d['damage']==1,d);shot(p,'native-hit-flash')
   p.evaluate(STEP,18);ck('Native hull flash expires during the new manoeuvres',p.evaluate('reviewActor._s9rift.core.flash<=0'));shot(p,'native-hit-expired')
   # A defence may clear the in-flight ordinary bomb without its landing blast.
   advance(p,"reviewActor._eh25.bomb?.phase==='flight'",400,3)
   p.evaluate("()=>{window.clearJob=reviewActor._eh25.bomb.job;clearJob.ball.dead=true;window.impactCount=EH25.events.filter(e=>e.event==='bomb-impact').length;}");p.evaluate(STEP,10)
   ck('Defensive bomb removal cancels its splash rather than detonating',p.evaluate("clearJob.dead&&!clearJob.arrived&&EH25.events.filter(e=>e.event==='bomb-impact').length===impactCount"))
   # Pending charge is cancelled immediately by the actual native defeat owner.
   advance(p,"reviewActor._eh25.bomb?.phase==='charge'",400,3)
   p.evaluate("()=>{window.deadJob=reviewActor._eh25.bomb.job;const at=s5924Eye(reviewActor);s9VoidHorizonHit(reviewActor,reviewActor.hp,at.x,at.y);}")
   ck('Native defeat exhausts the existing core and cancels its pending bomb',p.evaluate('reviewActor.dead&&reviewActor.hp===0&&reviewActor._s9rift.core.disabled&&deadJob.dead&&!reviewActor._eh25.bomb'))
   p.evaluate(STEP,90);ck('Destroyed Event Horizon cannot emit delayed energy bombs',p.evaluate('!eBullets.some(q=>q._eh25Owner===reviewActor&&!q.dead)&&!tb28List.some(q=>q.owner===reviewActor&&!q.dead)'))
   audio=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const key of EH25.cues){const b=await a.decodeAudioData(await(await fetch(BOFA.sfx[key])).arrayBuffer());let peak=0;for(const v of b.getChannelData(0))peak=Math.max(peak,Math.abs(v));out.push({key,peak,duration:b.duration});}return out;}""")
   ck('Charge, launch and energy impact cues decode to audible native audio',all(v['peak']>.01 and v['duration']>0 for v in audio),audio)
   p.close()
  br.close()
finally:stop()
ck('Horizon native tests report no page or console errors',not errors,errors)
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,runs=runs),indent=2),encoding='utf8')
if shots:
 im=Image.new('RGB',(1280,((len(shots)+3)//4)*220),(5,10,17));g=ImageDraw.Draw(im)
 for i,(f,n)in enumerate(shots):im.paste(Image.open(f).resize((320,200)),((i%4)*320,(i//4)*220));g.text(((i%4)*320+3,(i//4)*220+202),n,fill='white')
 im.save(O/'contact.jpg')
print(json.dumps(dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),errors=errors)),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)and not errors else 1)
