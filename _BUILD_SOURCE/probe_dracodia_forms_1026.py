"""Native state/damage and pixel fixtures; form selection is isolated from the input-only film."""
from barrage_review_common_1025 import ROOT,boot
from shoot import serve,STEP
from playwright.sync_api import sync_playwright
import json
O=ROOT/'_shots/dracodia_forms_1026/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
def shot(p,name):
 p.evaluate('drawWorld(0)');p.screenshot(path=str(O/(name+'.png')));shots.append(name)
def step(p,n):
 for i in range(0,n,12):p.evaluate(STEP,min(12,n-i));p.wait_for_timeout(1)
port,stop=serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&rd29Ready()&&bi24Warm()}',timeout=180000)
  p.evaluate('()=>{v18Enter(boss,2,0);boss._r30.v18.arenaPhase=2;v18Fight(boss);}')
  initial=p.evaluate('({max:j3State(boss).max,hp:boss.hp,parts:boss.parts.map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed}))})')
  d=p.evaluate('''()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;for(const part of boss.parts){boss._lastPart=part;hitBoss(1e6);}drawWorld(0);const z=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<z.length;i+=4)if(z[i]>240&&z[i+1]>240&&z[i+2]>240&&(a[i]<220||a[i+1]<220||a[i+2]<220))white++;return{white,hp:boss.hp,parts:boss.parts.map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed})),mode:boss._r30.mode,targets:retinaBossTargets(boss).length,shield:bossShieldFrac(boss)};}''')
  ck('Base HP and every piece resist lethal hits while copies remain',d['hp']==initial['hp']and d['parts']==initial['parts'],d)
  ck('Protected base gives actual visible hit feedback and shield state',d['white']>100 and d['shield']==1 and d['targets']==0,d)
  p.evaluate('()=>{r30Break(boss);j3FinalDeath(boss);}')
  ck('Direct defeat routes also preserve the protected final life',p.evaluate("boss._r30.mode==='fight'&&!dr5State(boss).deathStarted&&j3State(boss).hp[0]===boss.maxhp"))
  step(p,30);ck('Protected-base hit flash expires on native clock',p.evaluate('boss.flash<=0&&boss.parts.every(p=>p.flash<=0)'));shot(p,'base-protected')
  for form in [8,1,6,2]:
   p.evaluate('(f)=>{v18Clear(boss);v18Enter(boss,2,f);v18Fight(boss);}',form);step(p,200);shot(p,'form-'+str(form))
   d=p.evaluate('({form:boss._r30.v18.form,mode:boss._r30.mode,hp:boss.hp,parts:boss.parts.length,glows:RD30.glow.size})')
   ck('Native form '+str(form)+' animates and retains its full health',d['form']==form and d['hp']==initial['max'][form]and d['mode']=='fight',d)
  ck('Donor-follow effects expire across helicopter-to-brain switch',not errors,errors[:2])
  p.evaluate("()=>{v18Clear(boss);v18Enter(boss,2,6);v18Fight(boss);nb23Start(boss,'eyeExpansion');}");step(p,36)
  d=p.evaluate('''()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,fn=rd30CombatEffects;rd30CombatEffects=()=>{};try{drawWorld(0);}finally{rd30CombatEffects=fn;}const z=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<z.length;i+=4)if(a[i]!==z[i]||a[i+1]!==z[i+1]||a[i+2]!==z[i+2])n++;drawWorld(0);return n;}''')
  ck('Source-pixel charge and eye muzzle effects visibly alter native pixels',d>100,d);shot(p,'brain-charge')
  p.evaluate("()=>{v18Clear(boss);j3Morph(boss,0);}");trace=[];marks=set()
  for i in range(260):
   p.evaluate(STEP,1)
   d=p.evaluate('({mode:boss._r30.mode,t:boss._r30.t,x:boss.x,y:boss.y,form:boss._r30.v18.form,draw:RD30.last,protected:boss._noHit,hp:boss.hp,pools:j3State(boss).hp})');trace.append(d)
   if d['mode']=='v18formOut'and d['t']>.7 and 'out'not in marks:marks.add('out');shot(p,'fusion-out')
   if d['mode']=='v18formIn':
    for label,t in [('build',.8),('preflash',1.42),('covered',1.7),('reveal',2.4)]:
     if d['t']>=t and label not in marks:marks.add(label);shot(p,'fusion-'+label)
   if d['mode']=='fight':break
   if i%12==0:p.wait_for_timeout(1)
  ck('Code fusion completes through its native clocks',d['mode']=='fight'and d['form']==0 and len(marks)==5,{'mode':d['mode'],'marks':sorted(marks)})
  samples=[q for q in trace if q['mode']=='v18formIn']
  ck('Full copied body appears only under the covering flash',all(not q['draw'].get('complete')or q['draw'].get('white')==16 for q in samples if q['t']<1.85))
  ck('Transform keeps a continuous anchor and intact health pools',max(((a['x']-z['x'])**2+(a['y']-z['y'])**2)**.5 for a,z in zip(trace,trace[1:]))<15 and all(q['pools']==trace[0]['pools']for q in trace))
  p.evaluate("()=>{v18Clear(boss);v19BeginSwipe(boss,'scytheReap');}");frames=set()
  for i in range(170):
   p.evaluate(STEP,1)
   q=p.evaluate('({attack:boss._r30.v18.attack?.type,frame:v18Frame(boss).core.key,x:boss.x,y:boss.y})');frames.add(q['frame'])
   if i in [30,85,120]:shot(p,'scythe-'+str(i))
   if i%12==0:p.wait_for_timeout(1)
  ck('Scythe uses the authored strike bank and finite recovery',len(frames)>14 and p.evaluate('!boss._r30.v18.attack'),len(frames))
  killed=[]
  for form in [8,1,6,2]:
   p.evaluate('(f)=>{v18Clear(boss);v18Enter(boss,2,f);v18Fight(boss);}',form)
   for i in range(600):
    p.evaluate('''()=>{if(boss._r30.mode!=='fight')return;for(const t of retinaBossTargets(boss)){if(!t.dead&&t.hp>0)t._retinaHit(100000);if(boss._r30.mode!=='fight')break;}}''')
    p.evaluate(STEP,1)
    if p.evaluate('(f)=>j3State(boss).hp[f]<=0',form):break
    if i%12==0:p.wait_for_timeout(1)
   killed.append(p.evaluate('(f)=>({form:f,hp:j3State(boss).hp[f],base:j3State(boss).hp[0],mode:boss._r30.mode})',form))
  ck('Four native copy pools exhaust without touching final base life',all(q['hp']==0 and q['base']==initial['hp']for q in killed),killed)
  for i in range(500):
   p.evaluate(STEP,1)
   if p.evaluate("boss._r30.mode==='fight'&&boss._r30.v18.form===0"):break
   if i%12==0:p.wait_for_timeout(1)
  ck('Last copy naturally hands off to a full vulnerable final life',p.evaluate("boss._r30.mode==='fight'&&boss._r30.v18.form===0&&!rd30Locked(boss)&&retinaBossTargets(boss).length>0&&boss.hp===boss.maxhp"));shot(p,'final-life-open')
  d=p.evaluate("()=>{const p=boss.parts.find(p=>p.id==='left');boss._lastPart=p;hitBoss(p.hp+1);return{hp:boss.hp,broken:p.destroyed,shards:S78.debris.filter(q=>q.owner===boss).length,baseAlive:boss.hp>0};}")
  ck('Base arm breaks and shatters only on the final life',d['broken']and d['shards']>0 and d['baseAlive'],d);shot(p,'final-arm-shatter');step(p,30)
  ck('Final-life flash expires with remaining body intact',p.evaluate('boss.flash<=0&&boss.parts.every(p=>p.flash<=0)&&!boss.parts[0].destroyed'))
  p.evaluate('()=>{boss._lastPart=boss.parts[0];hitBoss(1e6);}')
  ck('Exhausted final base enters existing finale once',p.evaluate("dr5State(boss).deathStarted&&RD30.events.filter(e=>e.event==='final-life-unlocked').length===1"))
  ck('New energy rejects offensive interception before first update',p.evaluate("!enemyOrdnanceCanIntercept({_rd30Energy:true,t:0})"))
  ck('No page, update or draw errors',not errors,errors[:3]);events=p.evaluate('RD30.events');br.close()
finally:stop()
(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors,'events':events,'transition':trace,'killed':killed,'shots':shots},indent=2),encoding='utf8')
print(json.dumps({'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks)}))
raise SystemExit(0 if all(q['passed']for q in checks)else 1)
