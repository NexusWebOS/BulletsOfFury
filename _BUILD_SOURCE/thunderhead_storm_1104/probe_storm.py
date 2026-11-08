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
  p.evaluate('''()=>{s6WingTick=()=>{};s6WingLaunch=()=>{};allyUpdate=()=>{};window.setupStorm=()=>{EA11.setup(6,'furious');if(s6Wing)s6Wing.ships=[];ally=null;stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;player.invuln=0;run.bombs=40;FB112.events=[];THS114.events=[];spawnBoss('warhive');window.B=boss;return{hp:B.hp,kind:B.kind};};}''')
  before=p.evaluate('setupStorm');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000)
  saved=set()
  for i in range(190):
   row=p.evaluate('''()=>{for(let i=0;i<15;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);__bofFrames++;drawWorld(1/60);const S=B._th114;return{t:B.t,hp:B.hp,phase:B._fb112.phase,attack:B._fb112.attack,qt:B._fb112.t,weather:S.weather,marks:S.marks.length,impacts:S.impacts.length,fields:S.fields.length,rounds:eBullets.filter(r=>r._th114Owner===B&&!r.dead).length,playerDead:player.dead};}''');rows.append(row)
   key=(row.get('attack')or'')+'-'+row['phase']
   if key not in saved and row.get('attack')and(row['phase']=='warn'and row['qt']>1.1 or row['phase']=='attack'and row['qt']>1):
    saved.add(key);p.screenshot(path=str(O/(key+'.png')))
   if errors:break
  events=p.evaluate('THS114.events');seen={e['attack']for e in events if e['event']=='release'}
  ck('Furious Thunderhead keeps native6348HP and modular identity',before=={'hp':6348,'kind':'thunderhead'},before)
  ck('All4 storm attacks run at untouched healthy HP',len(seen)==4 and all(r['hp']==before['hp']for r in rows),sorted(seen))
  ck('All lightning impacts have at least2seconds of committed ground warning',any(e['event']=='lightning-impact'for e in events)and all(e['warning']>=2 for e in events if e['event']=='lightning-impact'))
  ck('Core has a visible charging stage for every attack',p.evaluate("THS114.events.filter(e=>e.event==='charge').length===THS114.events.filter(e=>e.event==='release').length||THS114.events.filter(e=>e.event==='charge').length===THS114.events.filter(e=>e.event==='release').length+1"))
  ck('No storm pileup beyond concurrency contract',max(r['rounds']for r in rows)<=24 and max(r['marks']for r in rows)<=3 and max(r['impacts']for r in rows)<=4,{'rounds':max(r['rounds']for r in rows),'marks':max(r['marks']for r in rows)})
  ck('Storm weather changes above readable city layers',max(r['weather']for r in rows)>.95 and min(r['weather']for r in rows)<.4)
  ck('Giant storm and twin tornadoes persist as bounded moving hazards',max(r['fields']for r in rows)==2 and any(r['fields']for r in rows if r['attack']=='storm-tempest'and r['qt']>3))
  ck('Tower tornadoes travel inward on the actual warned lanes',all(e['angle']<1.5708 if e.get('part')=='pressure0'else e['angle']>1.5708 for e in events if e['event']=='round'and e.get('family')=='tornado'and e.get('part')))
  ck('Cyclones and giant lightning storm actually leave native core socket',p.evaluate("()=>THS114.events.filter(e=>e.event==='round'&&['cyclone','tempest'].includes(e.family)).every(e=>Math.abs(e.x-worldWidth()/2)<20&&e.y>180&&e.y<220)"))
  ck('Ordinary storm energy cannot be shot down at creation',p.evaluate("()=>{const r=th114Round(B,th114Core(B),Math.PI/2,2,'orb');return r&&!enemyOrdnanceCanIntercept(r)&&!r._shootable;}"))
  ck('Giant storm corridor leaves at least90px on both camera flanks',p.evaluate('()=>{const S=B._th114;return S.stormLane-90-S.camera[0]>=90&&S.camera[1]-S.stormLane-90>=90;}'))
  ck('Core is invulnerable behind all6 live modules',p.evaluate('()=>{const hp=B.hp;fb112Damage(B,50,null,null,B._fb112.core);return B.hp===hp&&B._fb112.parts.filter(p=>p.hp>0).length===6;}'))
  # Isolated damage fixtures use the actual native damage owner; not the movie.
  p.evaluate('setupStorm');p.evaluate('()=>{for(let i=0;i<240;i++)updatePlay(1/60);}')
  ck('Destroyed pressure tower cancels its own active tornado',p.evaluate("()=>{const p=B._fb112.parts.find(p=>p.type==='pressure'),r=th114Round(B,fb112Bore(B,p),Math.PI/2,1,'tornado',p);for(let i=0;i<3&&p.hp>0;i++)fb112Damage(B,p.hp+10,null,null,p);updatePlay(1/60);return p.hp===0&&r.dead;}"))
  p.evaluate('()=>{for(const p of B._fb112.parts)for(let i=0;i<3&&p.hp>0;i++)fb112Damage(B,p.hp+10,null,null,p);}')
  ck('Destroying all6 modules exposes just the native core and correct HP',p.evaluate('()=>B._fb112.open&&retinaBossTargets(B).length===1&&B.hp===B._fb112.core.hp'))
  for i in range(60):p.evaluate('()=>{for(let j=0;j<15;j++)updatePlay(1/60);}')
  ck('Exposed core immediately prioritizes giant lightning storm',p.evaluate("THS114.events.some(e=>e.event==='release'&&e.attack==='storm-tempest')"))
  ck('Owned marks freeze with paused simulation',p.evaluate("()=>{th114Mark(B,player.x,player.y);const P=B._th114.marks.at(-1),a=P.age;for(let i=0;i<10;i++)fb112Draw(B);return P.age===a;}"))
  p.evaluate('()=>{for(let i=0;i<3&&!B.dead;i++)fb112Damage(B,B.hp+100,null,null,B._fb112.core);for(let i=0;i<210;i++)updatePlay(1/60);}')
  ck('Native defeat occurs once and clears all storm rounds and warnings',p.evaluate("()=>B.dead&&B._th114.marks.length===0&&B._th114.impacts.length===0&&eBullets.every(r=>r._th114Owner!==B||r.dead)&&FB112.events.filter(e=>e.event==='defeat').length===1"))
  ck('Death weather relinquishes stage owner',p.evaluate('()=>!th114Weather()'))
  for diff in ['normal','hard']:
   ck(diff+' keeps original encounter',p.evaluate("d=>{EA11.setup(6,'furious');diffKey=d;DIFF=difficultyForRun(run.mode,d);spawnBoss('warhive');return !boss?._fb112;}",diff))
  ck('Stage X and Rough Riders retain original owners',p.evaluate("()=>{EA11.setup(6,'furious');run._gp4StageX='left';spawnBoss('warhive');const x=!th114Own(boss);EA11.setup(6,'furious');spawnBoss('rebelsquad');return x&&!th114Own(boss)&&!!boss._rebels;}"))
  ck('No page/renderer/asset errors',not errors,errors)
  browser.close()
finally:stop()
(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors,'rows':rows,'events':events},indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
