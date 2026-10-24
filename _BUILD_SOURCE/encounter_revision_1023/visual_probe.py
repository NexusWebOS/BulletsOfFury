from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,time
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W/'visual';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':720});p.set_default_timeout(60000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF);ev=p.evaluate
  ev('''()=>{window.er23Setup=(stage,role,kind)=>{diffKey='furious';debugStartFight({stage,role,kind,name:kind},{pilot:'cole'});if(role==='mini')spawnSubBoss__inner(kind);else spawnBoss(kind);window.B=role==='mini'?subBoss:boss;B.enter=false;B._noHit=false;B.y=B.ty||180;B._drawY=B.y;player.invuln=0;player.dead=false;player.x=worldWidth()/2;player.y=VH-90;state=GS.PLAY;BOFCinematicDirector.cancel();HT23.speech=[];fb2Intro=null;B._fb2IntroSeen=true;return B.name;};window.fixtureHits=[];playerHit=s=>fixtureHits.push(s);window.er23Step=dt=>{updatePlay(dt);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(dt);};window.er23Paint=()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);};}''')
  def snap(name):
   ev('er23Paint()');(O/(name+'.png')).write_bytes(base64.b64decode(ev('cv.toDataURL().split(",")[1]')))
  ev("er23Setup(3,'mini','frostcruiser')")
  p.wait_for_function("[...Object.values(ER23_ART.frost).flatMap(a=>[a.key,a.key+'_hit']),...PT11_ART.ice_parts.map(a=>a.key)].map(k=>XART.rdy(k)).every(Boolean)")
  for i,rot in enumerate([-.8,0,.8]):
   ev('(rot)=>{for(const p of B._mr27.parts)p.rot=rot;}',rot);snap('frost-turn-'+str(i))
  ck('Frost Cruiser authored turn banks ready',ev("Object.values(ER23_ART.frost).every(a=>XART.rdy(a.key))"))
  ev("er23Setup(5,'boss','chromehammer')")
  p.wait_for_function("[...Object.entries(ER23_ART.banks).filter(([n])=>/blue_charge|stun|shield_wall|ball_flash/.test(n)).flatMap(([,a])=>[a.key,a.key+'_hit']),...hf22Keys(5),...hf22Keys(5,true)].map(k=>XART.rdy(k)).every(Boolean)&&ht23Warm()&&hm10Ready()")
  ev("()=>{hammerStormStart(B);B._hammer.t=2.3;B._hammer.recovery.elapsed=2;hm10Data(B).wallAge=1;hm10Data(B).wallOn=true;B._noHit=false;}")
  snap('chronos-charge-shield')
  q=ev("()=>{const q=ha21Blue(B),p=hammerHeadPoint(B);return{kind:q?.kind,head:p,wall:hm10WallActive(B)};}");ck('Charged actor and shield share live counter socket',q['wall']and'charge'in q.get('kind',''),q)
  ev("()=>{B._hammer.recovery=null;B._hammer.state='ball';B._hammer.hammerDestroyed=false;B._hammer._hf22Red=false;B._hammer.er23BallFlash=.16;B.flash=.12;}");snap('chronos-ball-red-response')
  ev("()=>{B._hammer.recovery=null;hammerState(B,'fr_stun');}");snap('chronos-stun')
  ev("()=>{B.dead=true;B.dying=.4;}");snap('chronos-dying-stun')
  ev("()=>{B.dead=false;B._hammer.state='giant_sweep';B._hammer.t=.44;B._hammer.tx=player.x;B._hammer.ty=player.y;B._hammer.giantLeft=1;hammerBossTick(B,1/60);}")
  q=ev("()=>({state:B._hammer.state,combo:!!B._hammer.er23DepthCombo})");ck('Furious distance return schedules second strike and side sweeps',q['combo'],q)
  for name,clock in [('second-down',.9),('left-sweep',1.9),('right-sweep',2.7)]:
   ev('(t)=>{const P=B._hammer.er23DepthCombo;P.clock=t;hj22PairTick(B,P);}',clock);snap('chronos-distance-'+name)
  ev("er23Setup(8,'boss','vileexistence')")
  p.wait_for_function("er23ArtKeys().map(k=>XART.rdy(k)).every(Boolean)&&PXV17_ART.arenas.map(a=>XART.rdy(a.key)).every(Boolean)&&V18_ART.models.infused.frames.flatMap(f=>Object.values(f).map(a=>a.key)).map(k=>XART.rdy(k)).every(Boolean)")
  ev("()=>{v18Fight(B);B.y=220;B._r30.v18.home={x:B.x,y:B.y};}");snap('dracodia-first-form')
  q=ev("""()=>{rb23Budget(B);const values=B.parts.map(p=>({id:p.id,hp:p.hp})),hp=B.hp;B._lastPart=B.parts[0];modularHit(100);return{values,total:B.maxhp,protected:B.hp===hp,eye:rb23Eye(B)};}""");ck('First form has 33.3/33.3/33.4 pools and protected body',q['protected']and abs(sum(r['hp'] for r in q['values'])-q['total'])<.001,q)
  ev("()=>{for(let i=0;i<20;i++)er23Step(1/60);B._r30.v18.rb23Seq=0;v18StartAttack(B);B._r30.v18.attack.t=.9;}");snap('dracodia-red-eye-charge')
  ev("()=>{B._r30.v18.attack.t=1.2;}");snap('dracodia-red-eye-laser')
  q=ev("""()=>{for(const p of B.parts.filter(p=>p.id!=='core')){B._lastPart=p;modularHit(p.hp+1);}for(let i=0;i<90;i++)er23Step(1/60);v18StartAttack(B);return{mode:B._r30.v18.attack?.type,hp:B.hp,core:B.parts[0].hp,arms:rb23Arms(B).length,dead:B.dead};}""");ck('Both arms can break at full part health and expose rolling core',q['arms']==0 and not q['dead'] and q['hp']==q['core']and q['mode']=='rb23-roll',q)
  for n,t in [('fold',.8),('roll-front',1.5),('roll-rear',1.8)]:
   ev('(t)=>{B._r30.v18.attack.t=t;}',t);snap('dracodia-'+n)
  ev("()=>{B._lastPart=B.parts[0];modularHit(B.parts[0].hp+1);}")
  ck('Core death enters protected falling/rebirth sequence',ev("B._r30.mode==='dr5er23rebirth'"))
  for label,target in [('fall',1.3),('question',4.4),('matter-rise',9.3),('heart',12),('fusion',15.5),('lightning',20),('whiteout',25.65),('new-arena',28.4),('monologue',28.6)]:
   ev('(target)=>{for(let i=0;B._r30.t<target&&B._r30.mode==="dr5er23rebirth"&&i<2000;i++)er23Step(Math.min(1/60,target-B._r30.t));}',target);snap('rebirth-'+label)
  q=ev("()=>({mode:B._r30.mode,encounter:j3State(B).encounter,bolts:RB23.events.filter(e=>e.event==='corrupted-lightning').length,arena:B._r30.v18.arenaPhase,dead:B.dead,hp:B.hp,reward:bossDefeated,arenaDraw:VOID17.last,download:AD20.last})")
  ck('Rebirth finishes with exactly 24 lightning beats and final arena/monologue',q['mode']=='dr5Monologue'and q['encounter']==2 and q['bolts']==24 and q['arena']==2 and not q['reward'],q)
  br.close()
finally:
 stop();(W/'visual-probe.json').write_text(json.dumps({'checks':checks,'errors':errors,'pass':all(c['pass']for c in checks)and not errors},indent=2));print('Page errors',errors,flush=True)
