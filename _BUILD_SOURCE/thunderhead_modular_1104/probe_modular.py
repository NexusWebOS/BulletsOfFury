from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W/'probe';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
port,stop=serve(str(R));errors=[];checks=[];rows=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print('PASS'if ok else'FAIL',name,json.dumps(data)[:300]if data is not None else'',flush=True)
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600])if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{s6WingTick=()=>{};s6WingLaunch=()=>{};allyUpdate=()=>{};const sourceRound=th114Round;window.coreSocketChecks=[];th114Round=function(b,at,a,s,f,p){if(['cyclone','tempest'].includes(f)){const c=th114Core(b);coreSocketChecks.push(Math.hypot(at.x-c.x,at.y-c.y)<.1);}return sourceRound.apply(this,arguments);};window.setupStorm=()=>{EA11.setup(6,'furious');if(s6Wing)s6Wing.ships=[];ally=null;stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;player.invuln=0;run.bombs=40;FB112.events=[];THS114.events=[];TM115.events=[];spawnBoss('warhive');window.B=boss;return{hp:B.hp,kind:B.kind};};}''')
  p.evaluate('''()=>{window.observedPulses=[];const tick=fb112Tick;fb112Tick=function(b,dt){const out=tick.apply(this,arguments);if(tm115Own(b)&&b._fb112.phase==='warn'){const q=b._fb112;observedPulses.push({owner:q.id,seq:q.seq,progress:q.t/q.dur,t:q.t,frame:tm115Pulse(b,4)});}return out;};}''')
  before=p.evaluate('setupStorm');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000)
  saved=set()
  ck('Regenerated hull/core/gun/cannon model is the live native assembly',p.evaluate('()=>B._fb112.M===TM115_ART.model&&B._fb112.scale===1&&TM115.bits.byteLength===TM115_ART.maskBytes'))
  for i in range(240):
   row=p.evaluate('''()=>{for(let i=0;i<15;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);__bofFrames++;drawWorld(1/60);const S=B._th114;return{t:B.t,hp:B.hp,phase:B._fb112.phase,attack:B._fb112.attack,qt:B._fb112.t,weather:S.weather,marks:S.marks.length,impacts:S.impacts.length,fields:S.fields.length,rounds:eBullets.filter(r=>r._th114Owner===B&&!r.dead).length,playerDead:player.dead};}''');rows.append(row)
   key=(row.get('attack')or'')+'-'+row['phase']
   if key not in saved and row.get('attack')and(row['phase']=='warn'and row['qt']>1.1 or row['phase']=='attack'and row['qt']>1):
    saved.add(key);p.screenshot(path=str(O/(key+'.png')))
   if row['phase']=='warn'and row['qt']>2.1 and 'beam-active'not in saved:
    saved.add('beam-active');p.screenshot(path=str(O/'wind-beams-charge.png'))
   if errors:print('NATIVE_ERRORS',errors,flush=True);raise RuntimeError('Native renderer error: '+repr(errors))
  events=p.evaluate('THS114.events');modular=p.evaluate('TM115.events');
  ck('Giant wind beams fire during core charge after1.7seconds warning',any(e['event']=='wind-beam'for e in modular)and all(e['warning']>=1.7 for e in modular if e['event']=='wind-beam'))
  ck('Every surviving modular gun and cannon has a reachable source-pixel target',p.evaluate('()=>B._fb112.parts.every(p=>{const a=fb112PartPoint(B,p);return fb112At(B,a.x,a.y)===p;})'))
  seen={e['attack']for e in events if e['event']=='release'}
  ck('Furious Thunderhead keeps native6348HP and modular identity',before=={'hp':6348,'kind':'thunderhead'},before)
  ck('All4 storm attacks run at untouched healthy HP',len(seen)==4 and all(r['hp']==before['hp']for r in rows),sorted(seen))
  ck('All lightning impacts have at least2seconds of committed ground warning',any(e['event']=='lightning-impact'for e in events)and all(e['warning']>=2 for e in events if e['event']=='lightning-impact'))
  ck('Core has a visible charging stage for every attack',p.evaluate("THS114.events.filter(e=>e.event==='charge').length===THS114.events.filter(e=>e.event==='release').length||THS114.events.filter(e=>e.event==='charge').length===THS114.events.filter(e=>e.event==='release').length+1"))
  ck('No storm pileup beyond concurrency contract',max(r['rounds']for r in rows)<=24 and max(r['marks']for r in rows)<=3 and max(r['impacts']for r in rows)<=4,{'rounds':max(r['rounds']for r in rows),'marks':max(r['marks']for r in rows)})
  ck('Storm weather changes above readable city layers',max(r['weather']for r in rows)>.95 and min(r['weather']for r in rows)<.4)
  ck('Giant storm and twin tornadoes persist as bounded moving hazards',max(r['fields']for r in rows)==2 and any(r['fields']for r in rows if r['attack']=='storm-tempest'and r['qt']>3))
  ck('Tower tornadoes travel inward on the actual warned lanes',all(e['angle']<1.5708 if e.get('part')=='pressure0'else e['angle']>1.5708 for e in events if e['event']=='round'and e.get('family')=='tornado'and e.get('part')))
  ck('Cyclones and giant lightning storm actually leave native core socket',p.evaluate('coreSocketChecks.length>0&&coreSocketChecks.every(Boolean)'))
  ck('Ordinary storm energy cannot be shot down at creation',p.evaluate("()=>{const r=th114Round(B,th114Core(B),Math.PI/2,2,'orb');return r&&!enemyOrdnanceCanIntercept(r)&&!r._shootable;}"))
  ck('Giant storm corridor leaves at least90px on both camera flanks',p.evaluate('()=>{const S=B._th114;return S.stormLane-90-S.camera[0]>=90&&S.camera[1]-S.stormLane-90>=90;}'))
  ck('Beam outlets use both actual cannon bores',len({e['part']for e in modular if e['event']=='wind-beam'})==2)
  ck('Whole body and every component own authored1015 aura frames',all(name in __import__('json').loads((W/'authored/manifest.json').read_text())['banks']for name in ['hull_aura','core_aura','gun_aura','pod0_aura','pod1_aura']))
  ck('Core is invulnerable behind all6 live modules',p.evaluate('()=>{const hp=B.hp;fb112Damage(B,50,null,null,B._fb112.core);return B.hp===hp&&B._fb112.parts.filter(p=>p.hp>0).length===6;}'))
  p.evaluate('setupStorm')
  p.evaluate('''()=>{for(let i=0;i<1200;i++){updatePlay(1/60);if(B._tm115?.beams.length===2&&B._tm115.beams.every(b=>b.age>.3))break;}}''')
  ck('Two live wind beams coexist with the still-charging core',p.evaluate("()=>B._fb112.phase==='warn'&&B._tm115.beams.length===2&&B._fb112.t<B._fb112.dur"))
  ck('Both beam graphics follow their actual moving muzzle sockets',p.evaluate('()=>B._tm115.beams.every(f=>{const m=fb112Bore(B,f.part);return Math.hypot(m.x-f.x,m.y-f.y)<.01;})'))
  ck('Actual charge animation speeds up visibly before release',p.evaluate("""()=>{const seq=observedPulses[0].seq,owner=observedPulses[0].owner,list=observedPulses.filter(p=>p.owner===owner&&p.seq===seq),rate=(lo,hi)=>{const a=list.filter(p=>p.progress>lo&&p.progress<hi);let changes=0;for(let i=1;i<a.length;i++)if(a[i].frame!==a[i-1].frame)changes++;return changes/(a.at(-1).t-a[0].t);};window.pulseRates={early:rate(.05,.25),late:rate(.75,.95)};return pulseRates.late>pulseRates.early*1.5;}"""),p.evaluate('window.pulseRates'))
  ck('Whole armor charge is visible in actual native pixels',p.evaluate('''()=>{const count=f=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);tm115Bank('hull',f,300,300);const a=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>128&&a[i+1]>a[i]+10&&a[i+2]>a[i]+15)n++;return n;};window.chromePixelCheck={idle:count(0),charge:count(14)};return chromePixelCheck.charge>chromePixelCheck.idle+100;}'''),p.evaluate('window.chromePixelCheck'))
  ck('Regenerated gun hit-flash changes actual pixels and expires',p.evaluate('''()=>{const part=B._fb112.parts[0],count=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);fb112Draw(B);const a=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();let n=0;for(let i=0;i<a.length;i+=4)if(a[i]>245&&a[i+1]>245&&a[i+2]>245&&a[i+3]>180)n++;return n;};const before=count();fb112Damage(B,1,null,null,part);const hit=count();for(let i=0;i<18;i++)updatePlay(1/60);const after=count();window.flashPixelCheck={before,hit,after,flash:part.flash};return hit>before+20&&after<hit&&part.flash<=0;}'''),p.evaluate('window.flashPixelCheck'))
  ck('Beam contact invokes native player-hit while GOD prevents death',p.evaluate("()=>{const f=B._tm115.beams[0];player.x=f.x;player.y=f.y+110;player.invuln=0;updatePlay(1/60);return f.hits.has(1)&&!player.dead&&TM115.events.some(e=>e.event==='wind-beam-hit');}"))
  ck('Central escape corridor is outside both actual beam hitboxes',p.evaluate("()=>{const list=B._tm115.beams;player.x=(list[0].x+list[1].x)/2;player.y=Math.max(...list.map(f=>f.y))+110;player.invuln=0;const before=TM115.events.filter(e=>e.event==='wind-beam-hit').length;updatePlay(1/60);return TM115.events.filter(e=>e.event==='wind-beam-hit').length===before;}"))
  ck('Beam animation clocks stay fixed while only rendering paused frames',p.evaluate('()=>{const f=B._tm115.beams[0],age=f.age;for(let i=0;i<10;i++)fb112Draw(B);return f.age===age;}'))
  ck('Destroyed cannon cancels its beam without cancelling the other cannon',p.evaluate("()=>{const f=B._tm115.beams[0];window.brokenBeam=f;for(let i=0;i<3&&f.part.hp>0;i++)fb112Damage(B,f.part.hp+10,null,null,f.part);updatePlay(1/60);return f.part.hp===0&&f.recovery&&B._tm115.beams.some(g=>g!==f&&!g.recovery);}"))
  p.evaluate('()=>{for(let i=0;i<18;i++)updatePlay(1/60);}')
  ck('Cancelled cannon completes finite authored beam recovery',p.evaluate('()=>!B._tm115.beams.includes(brokenBeam)'))
  # Isolated damage fixtures use the actual native damage owner; not the movie.
  p.evaluate('setupStorm');p.evaluate('()=>{for(let i=0;i<240;i++)updatePlay(1/60);}')
  ck('Destroyed pressure tower cancels its own active tornado',p.evaluate("()=>{const p=B._fb112.parts.find(p=>p.type==='pressure'),r=th114Round(B,fb112Bore(B,p),Math.PI/2,1,'tornado',p);for(let i=0;i<3&&p.hp>0;i++)fb112Damage(B,p.hp+10,null,null,p);updatePlay(1/60);return p.hp===0&&r.dead;}"))
  p.evaluate('()=>{for(const p of B._fb112.parts)for(let i=0;i<3&&p.hp>0;i++)fb112Damage(B,p.hp+10,null,null,p);}')
  ck('Destroying all6 modules exposes just the native core and correct HP',p.evaluate('()=>B._fb112.open&&retinaBossTargets(B).length===1&&B.hp===B._fb112.core.hp'))
  for i in range(60):p.evaluate('()=>{for(let j=0;j<15;j++)updatePlay(1/60);}')
  ck('Exposed core immediately prioritizes giant lightning storm',p.evaluate("THS114.events.some(e=>e.event==='release'&&e.attack==='storm-tempest')"))
  ck('Owned marks freeze with paused simulation',p.evaluate("()=>{th114Mark(B,player.x,player.y);const P=B._th114.marks.at(-1),a=P.age;for(let i=0;i<10;i++)fb112Draw(B);return P.age===a;}"))
  p.evaluate('()=>{for(let i=0;i<3&&!B.dead;i++)fb112Damage(B,B.hp+100,null,null,B._fb112.core);for(let i=0;i<210;i++)updatePlay(1/60);}')
  ck('Native defeat occurs once and clears all storm rounds and warnings',p.evaluate("()=>B.dead&&B._tm115.beams.length===0&&B._th114.marks.length===0&&B._th114.impacts.length===0&&eBullets.every(r=>r._th114Owner!==B||r.dead)&&FB112.events.filter(e=>e.event==='defeat').length===1"))
  ck('Death weather relinquishes stage owner',p.evaluate('()=>!th114Weather()'))
  for diff in ['normal','hard']:
   ck(diff+' keeps original encounter',p.evaluate("d=>{EA11.setup(6,'furious');diffKey=d;DIFF=difficultyForRun(run.mode,d);spawnBoss('warhive');return !boss?._fb112;}",diff))
  ck('Stage X and Rough Riders retain original owners',p.evaluate("()=>{EA11.setup(6,'furious');run._gp4StageX='left';spawnBoss('warhive');const x=!th114Own(boss);EA11.setup(6,'furious');spawnBoss('rebelsquad');return x&&!th114Own(boss)&&!!boss._rebels;}"))
  ck('No page/renderer/asset errors',not errors,errors)
  browser.close()
finally:stop()
(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors,'rows':rows,'events':events,'modularEvents':modular},indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
