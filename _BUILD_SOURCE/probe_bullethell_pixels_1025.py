"""Explicit native damage/phase fixtures, separate from the observation clips."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from PIL import Image,ImageDraw
import json,http.server

R=Path(__file__).resolve().parents[1];O=R/'_shots/bullethell_1025/pixels';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n,flush=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  def boot(stage,role):
   p=bc.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+json.dumps(m.location))if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof BH25!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("""([s,r])=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(s,r),{pilot:'cole'});if(r==='mini')spawnSubBoss(debugFightFor(s,r).kind);else spawnBoss(debugFightFor(s,r).kind);debugFight.spawned=true;warnT=0;DBGT.god=true;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;BH25.events=[];window.bhActor=r==='mini'?subBoss:boss;}""",[stage,role])
   p.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=180000)
   for i in range(1600):
    p.evaluate(STEP,5)
    if p.evaluate('!!bhActor._bh25'):return p
    if i%12==0:p.wait_for_timeout(1)
   raise RuntimeError('Barrage not reached')
  def shot(p,name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  def damaged(p,code):
   return p.evaluate("""code=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data;eval(code);drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,changed=0;for(let i=0;i<d.length;i+=4){if(d[i]!==a[i]||d[i+1]!==a[i+1]||d[i+2]!==a[i+2])changed++;if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;}return{white,changed};}""",code)
  p=boot(7,'boss');p.evaluate(STEP,10)
  q=damaged(p,"s7mHit(boss,1,undefined,undefined,'frontL')");ck('Warden damage changes actual leg pixels during a barrage',q['white']>20,q);shot(p,'warden-hit')
  p.evaluate(STEP,20);ck('Warden part flash expires during the barrage',p.evaluate("boss._s7mod.parts.find(p=>p.id==='frontL').flash<=0"));shot(p,'warden-expired')
  q=p.evaluate("()=>{const P=boss._bh25,p=bh25Ports(boss)[0],q=bh25Shot(boss,p,Math.PI/2);return{offense:enemyOrdnanceCanIntercept(q),defense:enemyDefensiveProof(q),shootable:q._shootable,beforeFirstUpdate:q.t};}")
  ck('A newly born round cannot be intercepted before its first update',not q['offense']and not q['shootable']and not q['defense'],q)
  ck('Stationary barrage braces the spider legs',p.evaluate('r25Gait(boss).speed===0&&r25Gait(boss).lastDX===0'))
  # Explicit shield-phase damage fixture exercises the retaliatory interlock.
  p.evaluate("()=>{bh25Cancel(boss,'shield-fixture');const M=boss._s7mod;for(const p of M.parts)if(/front|rear/.test(p.id))p.hp=0;M.counter=0;M.counterTell=null;M.shield=200;s7mSet(boss,'bh25');bh25Start(boss,'warden',()=>{s7mSet(boss,'recover');bh25RestoreCounter(boss);});s7mHit(boss,1,boss.x,boss.y,'core');}")
  ck('Shield retaliation is queued behind the committed barrage',p.evaluate('!!boss._s7mod.bh25Counter&&!boss._s7mod.counterTell'))
  for i in range(120):
   p.evaluate(STEP,10)
   if not p.evaluate('!!boss._bh25'):break
  ck('Deferred shield retaliation receives its own full native tell',p.evaluate('boss._s7mod.counterTell?.t<.2&&boss._s7mod.counterTell.warn===1.05'))
  # Density/reaction parameters selected by native difficulty; no new combat stats.
  ranks=p.evaluate("()=>{const out=[];for(const key of ['normal','hard','furious']){bh25Cancel(boss,'difficulty-fixture');diffKey=key;s7mSet(boss,'bh25');bh25Start(boss,'warden',()=>{});const P=boss._bh25;out.push({key,count:P.plan.length,waves:P.waves,warm:P.warm,speed:P.speed});}return out;}")
  ck('Normal and Hard retain fewer, slower waves and longer warnings',ranks[0]['count']<ranks[1]['count']<ranks[2]['count']and ranks[0]['warm']>ranks[1]['warm']>ranks[2]['warm'],ranks)
  p.close()

  p=boot(8,'mini');q=damaged(p,"hd1003Hit(subBoss,1,0,0,'wingL')");ck('Herald wing damage changes visible authored pixels',q['white']>20,q);shot(p,'herald-hit');p.evaluate(STEP,20)
  ck('Herald wing flash expires through native upkeep',p.evaluate("hd1003Part(subBoss,'wingL').flash<=0"));shot(p,'herald-expired')
  p.evaluate(STEP,70)
  q=p.evaluate("()=>{const b=subBoss,p=hd1003Part(b,'wingL');hd1003Hit(b,p.hp,0,0,p.id);bh25Prune();return{dead:p.dead,remaining:eBullets.filter(q=>!q.dead&&q._bh25Owner===b&&q._bh25Part==='wingL').length};}")
  ck('Destroyed Herald wing cancels its released rounds',q['dead']and q['remaining']==0,q);shot(p,'herald-wing-break')
  p.close()

  p=boot(8,'boss');p.evaluate(STEP,47);q=damaged(p,"boss._lastPart=boss.parts.find(p=>p.id==='left');modularHit(1)");ck('Raised claw damage still flashes actual arm pixels',q['white']>50,q);shot(p,'claw-hit');p.evaluate(STEP,20)
  ck('Claw flash expires while the barrage continues',p.evaluate("boss.parts.find(p=>p.id==='left').flash<=0"))
  q=p.evaluate("()=>{const p=boss.parts.find(p=>p.id==='core'),hp=p.hp;boss._lastPart=p;modularHit(20);return{before:hp,after:p.hp,total:boss.parts.reduce((s,p)=>s+p.maxhp,0),budget:boss.maxhp};}")
  ck('Protected 33.4 percent core and total health budget remain native',q['before']==q['after']and q['total']==q['budget'],q)
  p.evaluate(STEP,65);shot(p,'claw-muzzle-release')
  q=p.evaluate("()=>{const b=boss,p=b.parts.find(p=>p.id==='left');b._lastPart=p;modularHit(p.hp);return{dead:p.destroyed,rounds:eBullets.filter(q=>!q.dead&&q._bh25Owner===b&&q._bh25Part==='left').length,shards:S78.debris.length};}")
  ck('Destroyed claw immediately cancels its bullets and breaks into native shards',q['dead']and q['rounds']==0 and q['shards']>0,q);shot(p,'claw-break')
  mark=p.evaluate('BH25.events.length');p.evaluate(STEP,100)
  ck('A destroyed claw never receives a later barrage volley',p.evaluate("i=>!BH25.events.slice(i).some(e=>e.event==='round'&&e.part==='left')",mark))
  p.evaluate("()=>{const p=boss.parts.find(p=>p.id==='right');boss._lastPart=p;modularHit(p.hp);}");p.evaluate(STEP,100)
  ck('Losing both arms restores native ball routes and code bombs',p.evaluate("!boss._bh25&&boss._r30.v18.bi24Rolled&&boss._r30.v18.attack?.type==='rb23-roll'"));shot(p,'native-ball-after-break')
  p.evaluate("()=>{const p=boss.parts.find(p=>p.id==='core');boss._lastPart=p;modularHit(p.hp);}")
  ck('Core exhaustion still enters the protected cinematic once',p.evaluate("boss._r30.mode==='dr5er23rebirth'&&!boss._bh25&&boss.hp===0&&S78.debris.length>=20"));shot(p,'native-rebirth-after-barrage')
  p.close()

  p=boot(8,'boss');p.evaluate("()=>{bh25Cancel(boss,'final-form-fixture');v18Enter(boss,2,0);boss._r30.v18.arenaPhase=2;v18Fight(boss);boss.enter=false;boss._noHit=false;BH25.events=[];}")
  before=p.evaluate('({ledger:[...j3State(boss).hp],attacks:j3State(boss).attacks})')
  for i in range(500):
   p.evaluate(STEP,5)
   if p.evaluate('!!boss._bh25'):break
  ck('Final Dracodia opens with a native barrage before army downloads',p.evaluate("boss._bh25?.kind==='dracodia'&&bh25DrClear(boss)"));shot(p,'final-dracodia-warning')
  for i in range(160):
   p.evaluate(STEP,5)
   if i in [20,40,60]:shot(p,'final-dracodia-'+str(i))
   if not p.evaluate('!!boss._bh25'):break
  after=p.evaluate('({ledger:[...j3State(boss).hp],attacks:j3State(boss).attacks,events:BH25.events})')
  ck('Final barrage preserves all finite form pools and native attack-book progress',before['ledger']==after['ledger']and before['attacks']==after['attacks'],{'before':before,'after':{'ledger':after['ledger'],'attacks':after['attacks']}})
  ck('Final barrage completes through native attack ownership',any(e['event']=='section-complete'for e in after['events']))
  q=p.evaluate("()=>{const b=boss,e=d20Enemy('spear',b.x+130,b.y+80,b,false);v18StartAttack(b);return{spawned:!!e,clear:bh25DrClear(b),barrage:!!b._bh25,attack:b._r30.v18.attack?.type};}")
  ck('Final barrage yields to an active native archive army',q['spawned']and not q['clear']and not q['barrage']and q['attack']!='bh25',q)
  # Cue routes are decoded from the actual shared mixer assets.
  q=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const key of ['bossWeaponCharge',...new Set(Object.values(BH25.cfg).map(c=>c.cue))]){const d=await a.decodeAudioData(await(await fetch(BOFA.sfx[key])).arrayBuffer()),v=d.getChannelData(0);let peak=0;for(const x of v)peak=Math.max(peak,Math.abs(x));out.push({key,peak,duration:d.duration});}return out;}""")
  ck('All barrage launcher cues decode to audible native samples',all(v['peak']>.01 and v['duration']>0 for v in q),q)
  p.evaluate("combatAudio0927(boss,'enemyBossCannon',0)");p.wait_for_timeout(150)
  ck('Launcher audio actually plays through the shared mixer',p.evaluate("Snd.pools.enemyBossCannon.slots.some(s=>s?.el&&!s.el.paused&&s.el.currentTime>0)"))
  ck('No page or console errors in damage and phase fixtures',not errors,errors);p.close();br.close()
finally:
 stop();(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
if shots:
 im=Image.new('RGB',(1280,222*((len(shots)+3)//4)),(5,10,17));d=ImageDraw.Draw(im)
 for i,(f,n)in enumerate(shots):im.paste(Image.open(f).resize((320,200)),((i%4)*320,(i//4)*222));d.text(((i%4)*320+4,(i//4)*222+201),n,fill='white')
 im.save(O/'contact.jpg')
print(json.dumps(dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),errors=errors)),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)and not errors else 1)
