/* QA only. Delayed visible geometry, eight-way input, actual movement and damage. */
const MV7_BASE_SETUP=BAL7.setup;
window.MV7={};
MV7.setup=function(c){
 const cfg={...c,mini:c.role==='mini'||c.role==='alt',kind:c.kind||STAGES[c.stage-1].boss};
 if(c.code){const E=ON5_CODES[c.code];cfg.kind=E.kind||debugFightFor(E.stage,E.role==='boss'?'boss':'mini').kind;cfg.mini=E.role!=='boss';if(E.phase!=null)cfg.form=E.phase===0?'host':E.phase===1?'ghost':E.mimic!=null?String(E.mimic):'home';}
 const entry=MV7_BASE_SETUP(cfg);const Q=BAL7.q;if(c.code){window.B=on5LaunchEncounter({...ON5_CODES[c.code],code:c.code});Q.initialHP=BAL7.health();Q.initialParts=BAL7.parts();}Q.c={...cfg,seconds:c.seconds||180};Q.lastSeen=new WeakMap();Q.targetSeen=new Map();Q.previousTime=0;Q.safeChoices=[];Q.dangerDecisions=0;Q.minClearance=999;Q.collects=0;Q.startLives=run.lives;Q.trace=[];Q.evasionAt=-99;Q.stopT=null;Q.actor=B;
 if(c.stageWaves){beginStage(c.stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;player.invuln=0;player.dead=false;run.weapon=c.weapon||0;run.wlevel=c.level??3;run.spaceWeapon=0;run.spaceLevels=[c.level??3,c.level??3,c.level??3];run._lifeThreat=0;window.B=null;}
 player.x=worldWidth()*(c.position||.5);player.y=VH-100;player.fireCd=0;player._rollCool=0;player._somerCool=0;
 return {...entry,scenario:cfg.code||cfg.key};
};
MV7.observe=function(){
 const Q=BAL7.q,now=Q.t;window.B=Q.c.stageWaves?(bossActive?boss:subBossActive?subBoss:null):Q.actor;
 const S={time:now,bullets:[],lines:[],circles:[],bodies:[],targets:[],pickups:[]};
 const visible=q=>q&&!q.dead&&q.x>=camLeftX()-60&&q.x<=camRightX()+60&&q.y>=PLAY.y-60&&q.y<=VH+30;
 for(const q of eBullets.filter(visible)){
  const prev=Q.lastSeen.get(q),delta=prev?now-prev.t:0;let vx=(q.vx||0)*60,vy=(q.vy||0)*60;
  if(delta>.04){vx=(q.x-prev.x)/delta;vy=(q.y-prev.y)/delta;}
  Q.lastSeen.set(q,{x:q.x,y:q.y,t:now});
  S.bullets.push({x:q.x,y:q.y,vx,vy,rx:q._ovSonicWave?q._waveW*.42:Math.max(4,Math.min(65,(q.r||q.radius||q.w||10)*.5)),ry:q._ovSonicWave?q._waveH*.32:Math.max(4,Math.min(65,(q.r||q.radius||q.h||12)*.5)),kind:q.kind});
 }
 const line=(L,warn=false)=>{if(L&&[L.x,L.y,L.ex,L.ey].every(Number.isFinite))S.lines.push({x:L.x,y:L.y,ex:L.ex,ey:L.ey,width:L.width||18,warn});};
 for(const g of groundTargetingFx){if(g.dead||g.delay>0||g.t<.05)continue;if(g.kind==='missile')S.circles.push({x:g.x,y:g.y,r:g.radius+9,warn:g.t<g.warn});else line({x:g.x,y:PLAY.y,ex:g.x,ey:VH,width:g.radius*2},g.t<g.warn);}
 for(const owner of [bossActive?boss:null,subBossActive?subBoss:null].filter(Boolean)){
  const C=hc1007CrossState(owner);if(C&&!['gap','done','dissolve'].includes(C.mode))for(const L of C.rays)line(L,C.mode==='tell');
  if(owner._hc1007&&!C)for(const L of owner._hc1007.lines||[])if(!L.fire||L.liveAge==null||L.liveAge<.76)line(L,!L.fire);
  if(owner._r30){const H=hf7Sample(owner);if(H&&!['recover','gap','dissolve'].includes(H.phase))for(const L of H.lines)line(L,H.phase==='tell');const V=owner._r30.hc7Rift;if(V&&V.phase!=='recover'){S.circles.push({x:V.x,y:V.y,r:V.radius+24});for(const L of V.lanes)line(L,L.phase==='tell');}}
  for(const q of owner._rebels?.ships||[]){const A=q.rg4?.act;if(A?.kind==='rookhook'&&['charge','cast'].includes(A.phase))line({x:q.x,y:q.y+25,ex:q.x+Math.cos(A.a)*A.range,ey:q.y+25+Math.sin(A.a)*A.range,width:24},A.phase==='charge');}
  for(const q of owner._tempestDuo?.ships||[])for(const beam of q._tlv?.beams||[])line({x:beam.x,y:beam.y,ex:beam.x+Math.cos(beam.ang)*VH*2,ey:beam.y+Math.sin(beam.ang)*VH*2,width:26},!beam.active);
 }
 const bodies=[...enemies,...[bossActive?boss:null,subBossActive?subBoss:null].flatMap(b=>!b?[]:b._rebels?b._rebels.ships:b._whv?.mode==='ace'?[b._whv.ace]:b._tempestDuo?b._tempestDuo.ships:[b])];
 for(const b of bodies.filter(visible)){if(b.enter||b._noHit||b._dyingT!=null)continue;const prev=Q.lastSeen.get(b),d=prev?now-prev.t:0;S.bodies.push({x:b.x,y:b.y,vx:d>.04?(b.x-prev.x)/d:0,vy:d>.04?(b.y-prev.y)/d:0,rx:Math.min(150,(b._drawW||b.w||48)*.40),ry:Math.min(130,(b._drawH||b.h||50)*.36)});Q.lastSeen.set(b,{x:b.x,y:b.y,t:now});}
 S.targets=_lockTargets().filter(t=>!t.dead&&t.y>=PLAY.y-25&&t.y<player.y-45&&t.x>=camLeftX()&&t.x<=camRightX()).map((t,i)=>{const k=t.id||t.key||t.name||i,old=Q.targetSeen.get(k),dt=old?now-old.t:0,vx=dt>.04?clamp((t.x-old.x)/dt,-400,400):0;Q.targetSeen.set(k,{x:t.x,t:now});return{x:t.x,y:t.y,vx,important:!!(t._bossModule||t._retinaOwner||t._boss)};});
 S.pickups=powerups.filter(visible).map(t=>({x:t.x,y:t.y,kind:t.kind}));return S;
};
MV7.decide=function(S){
 const Q=BAL7.q,delay=Q.t-S.time,speed=playerBaseSpeed()*60*1.35,left=camLeftX()+16,right=camRightX()-16,top=PLAY.y+25,bottom=VH-29,margin=Q.c.margin??12;
 const seg=(x,y,L)=>{const vx=L.ex-L.x,vy=L.ey-L.y,t=clamp(((x-L.x)*vx+(y-L.y)*vy)/(vx*vx+vy*vy||1),0,1);return Math.hypot(x-L.x-t*vx,y-L.y-t*vy);};
 const target=S.targets.sort((a,b)=>(Math.abs(a.x-player.x)+(a.important?0:25))-(Math.abs(b.x-player.x)+(b.important?0:25)))[0];
 const targetX=target?clamp(target.x+(target.vx||0)*(delay+Math.max(0,player.y-target.y)/650),left,right):worldWidth()/2;let best=Infinity,bestHazard=0,choice=[0,0],safe=0,stationary=0;
 for(const dy of [-1,0,1])for(const dx of [-1,0,1]){
  let risk=0,clearance=999;const norm=dx&&dy?Math.SQRT1_2:1;
  for(const lead of [.10,.24,.42,.64]){
   const x=clamp(player.x+dx*norm*speed*lead,left,right),y=clamp(player.y+dy*norm*speed*lead,top,bottom),t=delay+lead;
   for(const b of S.bullets){const bx=b.x+b.vx*t,by=b.y+b.vy*t,d=Math.hypot((x-bx)/(b.rx+margin),(y-by)/(b.ry+margin));if(d<2.2)risk+=(2.2-d)*85;clearance=Math.min(clearance,(d-1)*Math.min(b.rx+margin,b.ry+margin));}
   for(const L of S.lines){const d=seg(x,y,L)-L.width*.5-margin;clearance=Math.min(clearance,d);risk+=Math.max(0,30-d)*(L.warn?3:8);}
   for(const b of S.bodies){const overlap=Math.min(b.rx+margin-Math.abs(x-b.x-b.vx*t),b.ry+margin-Math.abs(y-b.y-b.vy*t));risk+=Math.max(0,overlap)*9;clearance=Math.min(clearance,-overlap);}
   for(const g of S.circles){const d=Math.hypot(x-g.x,y-g.y)-g.r-margin;risk+=Math.max(0,25-d)*(g.warn?3:6);clearance=Math.min(clearance,d);}
  }
  if(clearance>0)safe++;if(!dx&&!dy)stationary=risk;
  const fx=clamp(player.x+dx*norm*speed*.45,left,right),fy=clamp(player.y+dy*norm*speed*.45,top,bottom);
  let cost=risk+(target?Math.abs(fx-targetX):Math.abs(fx-worldWidth()/2))*.11+Math.abs(fy-(VH-100))*.12;
  if(fx<=left+10||fx>=right-10)cost+=9;if(dx!==Q.commands[0]||dy!==Q.commands[1])cost+=2;
  const pickup=S.pickups.filter(p=>Math.hypot(p.x-player.x,p.y-player.y)<160).sort((a,b)=>Math.hypot(a.x-fx,a.y-fy)-Math.hypot(b.x-fx,b.y-fy))[0];if(pickup&&risk<80)cost+=Math.hypot(fx-pickup.x,fy-pickup.y)*.18;
  if(cost<best){best=cost;choice=[dx,dy];bestHazard=risk;}
 }
 Q.safeChoices.push(safe);if(safe===0)Q.dangerDecisions++;
 Q.commands=Q.c.stationary?[0,0]:choice;
 if(!Q.c.stationary&&Q.c.evasion!==false&&stationary>145&&Q.t-Q.evasionAt>.7&&!player.roll&&!player.somer){
  if(!(player._rollCool>0)){startRoll(choice[0]||(player.x<worldWidth()/2?1:-1));if(player.roll){Q.rolls++;Q.evasionAt=Q.t;}}
  else if(!(player._somerCool>0)){startSomersault();if(player.somer){Q.flips=(Q.flips||0)+1;Q.evasionAt=Q.t;}}
  else if(bestHazard>180&&run.bombs>0){Input.injectTap((keybindFor(1).bomb||['k'])[0]);Q.bombsUsed++;Q.evasionAt=Q.t;}
 }
};
MV7.step=function(n){const Q=BAL7.q,dt=1/(Q.c.fps||60);
 for(let i=0;i<n&&!Q.done;i++){
  if(state!==GS.PLAY){Q.done=true;Q.outcome=state;break;}
  Q.t+=dt;Q.frames++;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps?.();
  const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
  if(!player.dead){if(Q.t>=Q.observe){Q.queue.push(MV7.observe());Q.observe=Q.t+(Q.c.decision||.125);}while(Q.queue.length&&Q.queue[0].time<=Q.t-(Q.c.reaction??.25))MV7.decide(Q.queue.shift());const [x,y]=Q.commands;if(x<0)hold('left');if(x>0)hold('right');if(y<0)hold('up');if(y>0)hold('down');if(Q.c.fire!==false&&!H3.release&&!h3Locked()&&!BOFCinematicDirector.live)hold('fire');}
  if(run.stage===6&&s6Wing?.choice&&!s6Wing.route&&!s6Wing.autoRoute&&(s6Wing.frChoice?.t||0)>.6)Input.injectTap(' ');
  stateT+=dt;updatePlay(dt);if(Q.frames%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawScene(dt*6);}
  Q.peakBullets=Math.max(Q.peakBullets,eBullets.length);const pattern=BAL7.pattern();Q.patterns[pattern]=(Q.patterns[pattern]||0)+dt;
  if(Q.frames%60===0)Q.trace.push({t:+Q.t.toFixed(1),x:Math.round(player.x),y:Math.round(player.y),hp:BAL7.health(),lives:run.lives,bullets:eBullets.length,pattern,level:run.wlevel});
  if(Q.c.firstLife&&player.dead){Q.done=true;Q.outcome='death';}
  if(Q.c.stageWaves){if(bossActive&&!Q.c.fullStage){Q.done=true;Q.outcome='wave-phase-complete';}}
  else if(B&&(B.dead||bossDefeated||(Q.c.mini&&!subBossActive&&subBossDone)||(!Q.c.sequence&&B.hp<=0))){Q.done=true;Q.outcome=Q.c.form!=null?'phase-depleted':'encounter-defeated';}
  if(Q.c.form!=null&&B?._r30){const J=j3State(B),id=J.encounter===0?'host':J.encounter===1?'ghost':J.mimic==null?'home':String(J.mimic);if(!Q.c.sequence&&id!==String(Q.c.form)){Q.done=true;Q.outcome='form-transition';}}
  if(!Number.isFinite(player.x+player.y)){Q.done=true;Q.outcome='nonfinite';}
  if(!Q.done&&Q.t>=Q.c.seconds){Q.done=true;Q.outcome='time-limit';}
 }
 return {t:Q.t,done:Q.done,outcome:Q.outcome};
};
MV7.result=function(){const Q=BAL7.q;return {c:Q.c,t:Q.t,outcome:Q.outcome,hits:Q.hits,deaths:Q.hits.filter(h=>h.dead).length,initialHP:Q.initialHP,remainingHP:BAL7.health(),pools:BAL7.pools(),lives:run.lives,bombs:run.bombs,rolls:Q.rolls,flips:Q.flips||0,peakBullets:Q.peakBullets,patterns:Q.patterns,zeroSafeDecisions:Q.dangerDecisions,decisions:Q.safeChoices.length,trace:Q.trace,stageTimer,stageLength:curStage.length,diagnostics:{state,cinematic:BOFCinematicDirector.current?.id,live:BOFCinematicDirector.live,release:H3.release,opening:s6Opening?.phase,talk:fb2Talk?{done:fb2Talk.done,i:fb2Talk.i,age:fb2Talk.age,beat:fb2Talk.beats?.[fb2Talk.i]?.kind}:null,wing:s6Wing?{route:s6Wing.route,fake:s6Wing.fake,choice:s6Wing.choice,story:s6Wing.frStory}:null}};};
