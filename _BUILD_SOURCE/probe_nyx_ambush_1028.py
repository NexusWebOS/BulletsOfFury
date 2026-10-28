from pathlib import Path
import ast,json
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/nyx_1028/probe';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
port,stop=shoot.serve(str(R));errors=[];checks={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.stage=6;stageLoadBegin(6);}')
  p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',diff='normal',pilot='cole'))
  p.evaluate("""()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=B._noHit=false;window.G=rg4Init(B);H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;
  s6WingInit();s6WingLaunch(4,true);s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='right';s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;for(const q of s6Wing.ships)q.phase='fight';
  G.gang=true;G.scene=null;G.rescueDone=false;G.rescueAt=999;G.releaseAt=999;G.rd21.next=999;
  VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;warnT=0;warnKind=null;
  player.invuln=999999;player.fireCd=999999;powerups=[];eBullets=[];pBullets=[];for(const q of R.ships){q.rg4.cd=999;q.mode='fight';q.warp=0;q.x=camLeftX()+viewW()/2+(q.i-2)*76;q.y=PLAY.y+95+(q.i%2)*45;}SC12.refresh();__bofFit();}""")
  p.wait_for_function("()=>{stageLoadTick();rr26Warm();return stageLoadReady(6)&&XART.rdy('rr26_wall')&&XART.rdy('rr26_box')&&XART.rdy('pxg_rr26_wall_glow')&&REBEL_KEYS.every(k=>XART.rdy(AM13_ART[k].heading.key));}")
  def snap(name):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  checks['box_no_scene']=p.evaluate("()=>{rg4RescueStart(B,G);return !G.scene&&s6Wing.boxes.some(o=>o._rr26Wall)&&!B._noHit;}")
  snap('box')
  checks['decker_shoots_box']=p.evaluate("()=>{const o=s6Wing.boxes.find(o=>o._rr26Wall);pBullets=[{kind:'mg',_wingKey:'decker',ally:true,x:o.x,y:o.y,w:8,h:16,dmg:5}];s6SupplyTick(s6Wing,.016);return !!G.rr26.wall&&!s6Wing.boxes.includes(o);}")
  checks['wall_cast_duration']=p.evaluate("()=>{const W=G.rr26.wall;return W.cast===1.4&&W.hold===10&&Math.abs(W.dur-W.cast-W.build-W.fade-10)<.001&&W.caster.key==='decker';}")
  p.evaluate("()=>G.rr26.wall.t=.75");snap('wall-cast')
  p.evaluate("()=>G.rr26.wall.t=1.7");snap('wall-build')
  checks['centered']=p.evaluate('()=>{const r=rr26WallRect();return Math.abs(r.y+r.h/2-viewH()/2)<.01&&r.h<70;}')
  checks['reflect_multi']=p.evaluate("()=>{G.rr26.wall.t=2.3;const r=rr26WallRect();for(let i=0;i<5;i++)eShootT(r.x+30+i*50,r.y+20,Math.PI/2,3,'s6tracer');rr26WallTick(G,.016);return G.rr26.returns.length===5&&new Set(G.rr26.returns.map(o=>o.target.key)).size===5;}")
  snap('wall')
  checks['ship_block']=p.evaluate("""()=>{const r=rr26WallRect();player.y=r.y+r.h+50;rr26BlockShips(G);player.y=r.y-100;rr26BlockShips(G);const friendly=player.y>r.y+r.h;const q=R.ships[0];q.y=r.y-100;rr26BlockShips(G);q.y=r.y+r.h+100;rr26BlockShips(G);return friendly&&q.y<r.y;}""")
  checks['friendly_reflection']=p.evaluate("""()=>{const r=rr26WallRect(),o={kind:'mg',x:r.x+r.w/2,y:r.y+r.h+15,vx:0,vy:-12,w:8,h:12,dmg:3};pBullets=[o];rr26WallContact(G,.05);return o.dead&&eBullets.some(q=>q._rr26FriendlyReturn&&q.vy>0&&!enemyOrdnanceCanIntercept(q));}""")
  checks['beam_stopped']=p.evaluate("()=>{const r=rr26WallRect(),a=playerBeamRange({kind:'beam',x:r.x+r.w/2,y:r.y+r.h+100,top:PLAY.y,bot:r.y+r.h+100,w:16,h:400});return a.top>=r.y+r.h;}")
  checks['pixel_glow']=p.evaluate("""()=>{const n=PXG.log.pxg_rr26_wall_glow||0;G.rr26.wall.t=2.4;drawWorld(0);return (PXG.log.pxg_rr26_wall_glow||0)>n;}""")
  checks['return_damage']=p.evaluate("()=>{const hp=B.hp;for(let i=0;i<150;i++)rr26WallTick(G,1/60);return B.hp<hp;}")
  checks['helix_counter']=p.evaluate("()=>{const q=R.ships.find(q=>q.key==='jace');ra4Helix(q,G,{a:Math.PI/2});const o=G.ord[G.ord.length-1];o.x=R.ships[2].x;o.y=R.ships[2].y;const hp=B.hp;pBullets=[{kind:'mg',x:o.x,y:o.y,w:8,h:16,dmg:20,t:0,vx:0,vy:0}];rg4OrdnanceTick(B,G,.00001);return o.dead&&B.hp<hp&&RR26.events.some(e=>e.kind==='helix-counterburst'&&e.hit>0);}")
  checks['energy_instead_of_bullet']=p.evaluate("()=>{const q=R.ships[0],n=eBullets.length;q._rr26RoundAt=0;const z=rg4Round(q,Math.PI/2,4,'s6tracer');return eBullets.length===n&&G.ord.includes(z)&&z.hp>0;}")
  p.evaluate("()=>{for(const q of R.ships)q.flash=0;const q=R.ships.find(q=>q.key==='nyx');q._rr26Fade=1;q._rd21Cloak=true;}");snap('cloak')
  checks['heading_frames']=p.evaluate("()=>{const q=R.ships[0],frames=new Set();for(let i=0;i<8;i++){q.rfHeading=Math.PI/2+i*TAU/8;air13DrawRebel(q);frames.add(q._air13Frame);}return frames.size===8;}")
  p.evaluate("()=>{G.rr26.wall=null;G.rr26.returns=[];rd21FleetStart(B,G,G.rd21);}")
  for i in range(600):
   p.evaluate('()=>{rebelSquadTick(B,1/60);}')
   if i in [150,300,390]:snap('flight-'+str(i))
   if i==150:
    checks['distributed_retinas']=p.evaluate("()=>{const L=R.ships.filter(q=>q._rd21Volley);return L.length===5&&new Set(L.map(q=>q._rd21Volley.target.ref)).size===5;}")
   if i==285:
    checks['missile_volley']=p.evaluate("()=>eBullets.filter(q=>q._ra4Rocket).length>=15")
  checks['missile_retina_no_fov']=p.evaluate("""()=>{const q=R.ships[0],A={t:.6,warm:1.35,locked:true,target:{ref:player},a:Math.PI/2,shot:0};q._rd21Volley=A;let lanes=0,retinas=0;const f=combatWarningDraw,l=ra4LockWarning;combatWarningDraw=function(){lanes++;};ra4LockWarning=function(){retinas++;return l.apply(this,arguments);};try{q.rg4.act=null;q.rg4._rbal19Gun=null;fr27RebelDrawShip(q);return lanes===0&&retinas>0;}finally{combatWarningDraw=f;ra4LockWarning=l;q._rd21Volley=null;}}""")
  p.evaluate("()=>{const q=R.ships[0];q._rd21Volley={t:.6,warm:1.35,locked:true,target:{ref:player},a:Math.PI/2,shot:0};}");snap('missile-retina')
  checks['lock_beep']=p.evaluate("()=>{const n=RR26.events.filter(e=>e.kind==='missile-lock-beep').length;rebelSquadTick(B,.016);R.ships[0]._rd21Volley=null;return RR26.events.filter(e=>e.kind==='missile-lock-beep').length>n;}")
  checks['north_south']=p.evaluate("()=>RR26.events.some(e=>e.kind==='north-south-return')")
  checks['visible_hit_and_expiry']=p.evaluate("""()=>{const q=R.ships.find(q=>q.key==='voss');q.rfHeading=Math.PI/2;q.flash=0;const x=q.x,y=q.y;
   function pixels(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.restore();air13DrawRebel(q);const a=ctx.getTransform(),d=ctx.getImageData(Math.max(0,Math.floor(a.a*(q.x-70)+a.e)),Math.max(0,Math.floor(a.d*(q.y-70)+a.f)),Math.floor(140*a.a),Math.floor(140*a.d)).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>235&&d[i+1]>235&&d[i+2]>235&&d[i+3]>100)n++;return n;}
   const base=pixels();rr26Damage(q,1);const hit=pixels();for(let i=0;i<12;i++)rebelSquadTick(B,1/60);q.x=x;q.y=y;q.rfHeading=Math.PI/2;const end=pixels();return hit>base+50&&q.flash<=0&&end<hit;}""")
  p.wait_for_function("()=>[0,1,2,3].every(i=>XART.rdy('nfrb_'+i))")
  checks['kaia_burst']=p.evaluate("""()=>{G.ord=[];G.rd21.fleet=null;for(const q of R.ships)q.rg4.act=null;const q=R.ships.find(q=>q.key==='kaia');q.x=camLeftX()+viewW()/2;q.y=PLAY.y+110;rg4Attack(q,R,G,'rockets');if(q.rg4.act?.kind!=='rr26roller')return false;for(let i=0;i<215;i++)rg4AttackTick(q,R,G,1/60);return G.ord.filter(o=>o._rr26KaiaRoller).length===10&&q.rg4.act.phase==='recover';}""")
  p.evaluate("()=>{G.rr26.wall=null;G.rr26.radio=null;G.ord.forEach((o,i)=>{o.y+=40+i*24;});}");snap('kaia-rollers')
  p.wait_for_function("()=>XART.rdy('rr35_roller')&&XART.rdy('pxg_rr35_roller_glow')")
  checks['kaia_animated_glow_pixels']=p.evaluate("""()=>{const frames=new Set(),glowBefore=PXG.log.pxg_rr35_roller_glow||0;
   function pixels(t,flash){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,128,128);rr35RollerDraw(64,64,64,t,flash,.95);const data=ctx.getImageData(0,0,128,128).data;let hash=0,white=0;for(let i=0;i<data.length;i+=4){hash=(Math.imul(hash,31)+data[i]+data[i+1]*3+data[i+2]*7)|0;if(data[i]>235&&data[i+1]>235&&data[i+2]>235&&data[i+3]>100)white++;}ctx.restore();return {hash,white};}
   for(let i=0;i<16;i++)frames.add(pixels(i/24,0).hash);const base=pixels(0,0),hit=pixels(0,.1),end=pixels(0,0);return frames.size===16&&hit.white>base.white+100&&base.hash===end.hash&&(PXG.log.pxg_rr35_roller_glow||0)>glowBefore;}""")
  checks['kaia_straight']=p.evaluate("()=>{const a=G.ord.filter(o=>o._rr26KaiaRoller);return a.length===10&&new Set(a.map(o=>o.vx+','+o.vy)).size===1&&new Set(a.map(o=>o.x)).size===1&&a.every(o=>pw5Impact(o,player,1)===null);}")
  checks['kaia_shootable']=p.evaluate("()=>{const o=G.ord.find(o=>o._rr26KaiaRoller);rg4OrdnanceHit(G,o,1);const flashed=o.flash>0;rg4OrdnanceHit(G,o,4);return flashed&&o.dead;}")
  checks['rook_chain']=p.evaluate("""()=>{for(const q of R.ships)q.rg4.act=null;G.rd21.fleet=null;G.rr26.wall=null;eBullets=[];const q=R.ships.find(q=>q.key==='rook');q.x=camLeftX()+viewW()/2;q.y=PLAY.y+95;rg4Attack(q,R,G,'slug');const A=q.rg4.act;if(A?.kind!=='rr26chain')return false;A.target={ref:player};const x=q.x,y=q.y;for(let i=0;i<100;i++)rg4AttackTick(q,R,G,1/60);return q.x===x&&q.y===y&&eBullets.some(z=>z._rr26Rook&&z._rr26Track===player&&!enemyOrdnanceCanIntercept(z));}""")
  p.evaluate("()=>{G.ord=[];const q=R.ships.find(q=>q.key==='rook');q.rg4.act.phase='charge';q.rg4.act.t=1.4;}");snap('rook-chain')
  p.evaluate("()=>{R.ships.find(q=>q.key==='rook').rg4.act=null;}")
  checks['voss_turbo_return']=p.evaluate("""()=>{for(const q of R.ships)q.rg4.act=null;const q=R.ships.find(q=>q.key==='voss');q.x=camLeftX()+viewW()/2;q.y=PLAY.y+100;const home={x:q.x,y:q.y};rg4Attack(q,R,G,'turbo');if(q.rg4.act?.kind!=='turbo'||!q.rg4.act._vs41)return false;let off=false,north=false,safe=false;for(let i=0;i<1800&&q.rg4.act;i++){rg4AttackTick(q,R,G,1/60);off ||=q.y>VH;north ||=q.rg4.act?.phase==='north'&&q.y<PLAY.y;safe ||=vs41Safe(q);}return off&&north&&safe&&!q.rg4.act&&Math.hypot(q.x-home.x,q.y-home.y)<1&&q._rd21Scale===1;}""")
  p.evaluate("()=>{const q=R.ships.find(q=>q.key==='voss');rg4Attack(q,R,G,'fusion');q.rg4.act.t=1.25;}");snap('voss-charge')
  p.evaluate("()=>{R.ships.find(q=>q.key==='voss').rg4.act=null;}")
  checks['voss_cruise']=p.evaluate("()=>{const q=R.ships.find(q=>q.key==='voss');rg4Attack(q,R,G,'turbo');return q.rg4.act?.kind==='turbo';}")
  p.wait_for_function("()=>['jr36_spin','pxg_jr36_spin_glow','pxg_af21_jace_attack_glow'].every(k=>XART.rdy(k))")
  checks['jace_bullets_dodge_only']=p.evaluate("""()=>{G.ord=[];G.scene=null;G.rd21.fleet=null;G.rr26.wall=null;for(const q of R.ships)q.rg4.act=null;const q=R.ships.find(q=>q.key==='jace');q._rr26RoundAt=0;const z=rg4Round(q,Math.PI/2,3,'s6orb',{owner:q});return z._jr36Bullet&&!z._shootable&&!enemyOrdnanceCanIntercept(z)&&pw5Impact(z,player)===null&&!G.ord.includes(z)&&eBullets.includes(z);}""")
  checks['jace_no_dash']=p.evaluate("()=>{const q=R.ships.find(q=>q.key==='jace');const kinds=new Set();for(let i=0;i<9;i++)kinds.add(ra4AttackKind(q,G));rg4Attack(q,R,G,'ram');return kinds.size===1&&kinds.has('helix')&&q.rg4.act.kind==='jr36helix';}")
  p.evaluate("()=>{const q=R.ships.find(q=>q.key==='jace');q.rg4.act=null;q.x=camLeftX()+viewW()*.7;q.y=PLAY.y+100;rg4Attack(q,R,G,'helix');for(let i=0;i<140;i++)rg4AttackTick(q,R,G,1/60);}");snap('jace-charge')
  print('JACE RENDER',p.evaluate("()=>{const q=R.ships.find(q=>q.key==='jace');return {key:q._air13RenderedKey,frame:q._rr34Frame,pose:rr26AnimatedPose(q)?.key,fade:q._rr26Fade,glow:JR36.hullGlowDraws,charge:q.rg4.act.phase,ready:XART.rdy('af21_jace_attack')};}"))
  checks['jace_hull_glow']=p.evaluate("()=>{const n=JR36.hullGlowDraws||0;const q=R.ships.find(q=>q.key==='jace');q.flash=0;for(let i=0;i<12;i++){q.rg4.act.t+=1/60;fr27RebelDrawShip(q);}return (JR36.hullGlowDraws||0)>n;}")
  checks['jace_ranged_release']=p.evaluate("""()=>{const q=R.ships.find(q=>q.key==='jace'),x=q.x,y=q.y;let maxY=y;for(let i=0;i<90;i++){rg4AttackTick(q,R,G,1/60);maxY=Math.max(maxY,q.y);}const o=G.ord.find(o=>o._jr36Helix);return !!o&&o.hp===6&&o.r===28&&maxY<=y+.01&&Math.abs(o.x-x)<1&&o.y<PLAY.y+180&&q.rg4.act.phase==='recover';}""")
  checks['jace_spin_pixels']=p.evaluate("""()=>{const seen=new Set();for(let i=0;i<16;i++){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,100,100);jr36Orb(50,50,64,i/24);const a=ctx.getImageData(0,0,100,100).data;let h=0;for(let j=0;j<a.length;j+=4)h=(Math.imul(h,31)+a[j]+a[j+1]*3+a[j+2]*7)|0;seen.add(h);ctx.restore();}return seen.size===16&&(PXG.log.pxg_jr36_spin_glow||0)>0;}""")
  checks['jace_player_intercepts_counterblast']=p.evaluate("""()=>{const o=G.ord.find(o=>o._jr36Helix),before=B.hp;o.t=.1;pBullets=[{kind:'mg',x:o.x,y:o.y,w:8,h:16,dmg:10,t:0,vx:0,vy:0}];rg4OrdnanceTick(B,G,.00001);return o.dead&&B.hp<before&&RR26.events.some(e=>e.kind==='helix-counterburst'&&e.hit>0);}""")
  checks['jace_native_hit_flash_expiry']=p.evaluate("""()=>{const q=R.ships.find(q=>q.key==='jace');q.rg4.act=null;q.rfHeading=Math.PI/2;q.flash=0;const x=q.x,y=q.y;
   function pixels(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.restore();fr27RebelDrawShip(q);const a=ctx.getTransform(),d=ctx.getImageData(Math.max(0,Math.floor(a.a*(q.x-70)+a.e)),Math.max(0,Math.floor(a.d*(q.y-70)+a.f)),Math.floor(140*a.a),Math.floor(140*a.d)).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>235&&d[i+1]>235&&d[i+2]>235&&d[i+3]>100)n++;return n;}
   const base=pixels();rr26Damage(q,1);const hit=pixels();for(let i=0;i<12;i++)rebelSquadTick(B,1/60);q.x=x;q.y=y;q.rfHeading=Math.PI/2;const end=pixels();return hit>base+50&&q.flash<=0&&end<hit;}""")
  p.wait_for_function("()=>['nx37_lasers','ngm_shock_7',...Array.from({length:4},(_,i)=>'ndr_furymine_idle_'+i)].every(k=>XART.rdy(k))")
  checks['nyx_close_reveal_mine']=p.evaluate("""()=>{for(const q of R.ships)q.rg4.act=null;G.rd21.fleet=null;G.scene=null;G.nx37={mines:[],waves:[]};window.N=R.ships.find(q=>q.key==='nyx');N._rd21Cloak=true;N.x=camLeftX()+100;N.y=PLAY.y+90;rg4Attack(N,R,G);const A=N.rg4.act;if(A?.kind!=='nx37ambush')return false;for(let i=0;i<175;i++)rg4AttackTick(N,R,G,1/60);return G.nx37.mines.length===1&&!N._rd21Cloak&&A.phase==='retreat';}""")
  checks['nyx_two_turret_warnings']=p.evaluate("""()=>{for(let i=0;i<120;i++)rg4AttackTick(N,R,G,1/60);let lanes=[];const old=rd21Fov;rd21Fov=(a,x,y)=>lanes.push([x,y]);try{rg4Warning(N,N.rg4.act);}finally{rd21Fov=old;}return N.rg4.act.phase==='charge'&&lanes.length===2&&Math.hypot(lanes[0][0]-lanes[1][0],lanes[0][1]-lanes[1][1])>30;}""")
  p.evaluate("()=>{N._rr26Fade=0;}");snap('nyx-laser-charge')
  checks['nyx_twin_lasers']=p.evaluate("""()=>{eBullets=[];for(let i=0;i<250;i++)rg4AttackTick(N,R,G,1/60);const shots=eBullets.filter(z=>z._nx37Laser);return shots.length>=20&&shots.length%2===0&&shots.every(z=>!enemyOrdnanceCanIntercept(z)&&pw5Impact(z,player)===null);}""")
  checks['nyx_exit_return_cloak']=p.evaluate("()=>{for(let i=0;i<280;i++)if(N.rg4.act)rg4AttackTick(N,R,G,1/60);return !N.rg4.act&&N._rd21Cloak&&NX37.events.some(e=>e.event==='recloaked');}")
  checks['nyx_mine_proximity']=p.evaluate("""()=>{const S=G.nx37;S.waves=[];S.mines=[{x:player.x,y:player.y-70,t:0,phase:'arming',owner:N,beep:0}];nx37Hazards(G,.5);const safe=S.waves.length===0;for(let i=0;i<110;i++)nx37Hazards(G,1/60);return safe&&S.waves.length===1&&S.mines.length===0;}""")
  snap('nyx-blast-wave')
  checks['nyx_wave_dodge_and_finite_reach']=p.evaluate("""()=>{let hits=0;const old=playerHit;playerHit=()=>hits++;const S=G.nx37;const create=()=>({x:player.x,y:player.y-70,t:.15,r:39,max:150,owner:N,hit:new Set()});try{S.waves=[create()];player.roll={t:0};nx37Hazards(G,.1);const roll=hits===0;player.roll=null;player.somer={t:0};S.waves=[create()];nx37Hazards(G,.1);const somer=hits===0;player.somer=null;S.waves=[create()];nx37Hazards(G,.1);const hurt=hits===1;for(let i=0;i<60;i++)nx37Hazards(G,1/60);return roll&&somer&&hurt&&S.waves.length===0;}finally{playerHit=old;player.roll=player.somer=null;}}""")
  checks['nyx_native_hit_flash_expiry']=p.evaluate("""()=>{const q=R.ships.find(q=>q.key==='nyx');q._rd21Cloak=false;q._rd21Visible=99;q._rr26Fade=0;q.frCloak=0;q.rg4.cd=999;q.rg4.act=null;q.rfHeading=Math.PI/2;q.flash=0;const x=q.x,y=q.y;
   function pixels(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.restore();fr27RebelDrawShip(q);const a=ctx.getTransform(),d=ctx.getImageData(Math.max(0,Math.floor(a.a*(q.x-70)+a.e)),Math.max(0,Math.floor(a.d*(q.y-70)+a.f)),Math.floor(140*a.a),Math.floor(140*a.d)).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>235&&d[i+1]>235&&d[i+2]>235&&d[i+3]>100)n++;return n;}
   const base=pixels();rr26Damage(q,1);const hit=pixels();for(let i=0;i<12;i++)rebelSquadTick(B,1/60);q.x=x;q.y=y;q.rfHeading=Math.PI/2;const end=pixels();return hit>base+50&&q.flash<=0&&end<hit;}""")
  checks['returned_shot_hurts_player']=p.evaluate("""()=>{G.rr26.wall={t:1,dur:8,hits:0};G.shield=0;const r=rr26WallRect();pBullets=[{kind:'mg',x:r.x+r.w/2,y:r.y+r.h+2,vy:-5,vx:0,w:8,h:16}];rr26WallContact(G,.016);const q=eBullets.find(q=>!q.dead&&q._rr26FriendlyReturn);if(!q)return false;player.dead=player.out=false;player.invuln=0;player.roll=player.somer=null;run.shield=0;run.dkT=run.sonicT=0;special=null;q.x=player.x=r.x+r.w/2;q.y=player.y=r.y+r.h+70;const lives=run.lives;updatePlay(.00001);return !!player.dead||run.lives<lives;}""")
  checks['no_errors']=not errors
  (O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,events=p.evaluate('RR26.events')),indent=2));print(checks,errors)
  br.close()
finally:stop()
assert all(checks.values())
