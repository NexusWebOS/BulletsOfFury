/* QA-only wave telemetry (never shipped). Load after wave_review_1101.js.
   Runs a stage's regular waves on their native schedule (bosses/minibosses suppressed, ambient and
   adaptive reinforcements ON; see WT.start) on a
   chosen difficulty, with a dodge bot in place of the review pilot, and measures what the player
   actually faces each second: bullets, fire rate, speeds, aimed share, enemies, safe space, nearby
   threats, and would-be hits (playerHit calls while invulnerable; the game is one-hit-death). */
globalThis.WT={F:null,hitsRaw:0,lastHit:-9,hits:0,hitLog:[],vp:4.2};
(function(){
 const base=playerHit;
 playerHit=function(){
  /* count only hits that land: DA13 (difficulty_assist_1103) may refuse a firewall/debris graze */
  const S=globalThis.DA13&&DA13.state.stat,r0=S?S.wallRefused+S.debrisRefused:0,src=WT.on?WT.cause():null;
  const out=base.apply(this,arguments);
  if(WT.on&&!(S&&S.wallRefused+S.debrisRefused>r0)){WT.hitsRaw++;if(WT.F.clock-WT.lastHit>1.2){WT.hits++;WT.hitLog.push({t:+WT.F.clock.toFixed(2),src});}WT.lastHit=WT.F.clock;}
  return out;
 };
})();
WT.cause=function(){let best=null,bd=1e9;for(const b of eBullets){if(b.dead)continue;const d=Math.hypot(b.x-player.x,b.y-player.y);if(d<bd){bd=d;best=b;}}
 if(best&&bd<40)return 'bullet:'+best.kind;let be=null,ed=1e9;for(const e of enemies){if(e.dead)continue;const d=Math.hypot(e.x-player.x,e.y-player.y);if(d<ed){ed=d;be=e;}}
 if(be&&ed<90)return 'body:'+be.type;
 /* not a nearby round or hull: name the game function that called playerHit (beam, wave, hazard...) */
 const st=String(new Error().stack).split(String.fromCharCode(10)).map(l=>l.trim()).filter(l=>l.startsWith('at ')&&!/WT\.|playerHit|wave_telemetry/.test(l));
 const top=(st[0]||'').replace(/^at /,'').replace(/\(.*\/assets\//,'(').replace(/\?[^:)]*/,'');
 return 'other:'+top.slice(0,70)+(be?' near '+be.type+'@'+Math.round(ed):'');};
WT.BOTS={
 novice:{every:15,horizon:15,sight:150,home:.06,aim:.004,label:'novice: 250 ms reactions, sees 150 px, plans 0.25 s'},
 skilled:{every:5,horizon:30,sight:9999,home:.03,aim:.012,label:'skilled: 85 ms reactions, sees all, plans 0.5 s'},
 still:{every:1e9,horizon:1,sight:0,home:0,aim:0,label:'stationary bottom-centre (raw pressure)'},
};
WT.start=function(stage,diff,route,bot,wlevel){
 WT.seeHazards=!!globalThis.WT_SEE_HAZARDS;
 let r;
 if(typeof WO16!=='undefined'){
  /* today's observer fixture (wave_followup_1103/wave_observe_1102.js): ambient, onslaught and adaptive
     reinforcement owners stay ON, as in real play. It hard-codes Furious; run a copy with the chosen
     difficulty substituted before beginStage builds the wave book. */
  /* NATURAL PACING. The fixture file overrides WO16.start/input further down with a paced inspection
     mode (one wave at a time, next wave held until the last is cleared or ~60 s, adaptive off).
     That is for filming, not play: use the ORIGINAL setup (wo16Start: native schedule, ambient and
     adaptive owners on) and the ORIGINAL input (wo16Input). */
  globalThis.WT_DIFF=diff;const base=typeof wo16Start==='function'?wo16Start:WO16.start;
  const src=base.toString().replace(/'furious'/g,'WT_DIFF');
  r=(0,eval)('('+src+')').call(WO16,stage,route||'left');WT.F=WO16;
  if(typeof wo16Input==='function')WO16.input=wo16Input;
 }else{
  const setup=EA11.setup;EA11.setup=function(st){return setup.call(this,st,diff);};
  try{r=WR15.start(stage,route||'left');}finally{EA11.setup=setup;}WT.F=WR15;
 }
 diffKey=diff;DIFF=difficultyForRun(run.mode,diff);
 run.wlevel=wlevel||3;run.wlevels=WEAPONS.map(()=>wlevel||3);run.shield=0;
 Object.assign(WT,{on:true,stage,diff,bot,B:WT.BOTS[bot],frame:0,hitsRaw:0,hits:0,lastHit:-9,hitLog:[],seen:new WeakSet(),eSeen:new WeakSet(),
  sec:[],cur:null,fired:0,speeds:[],aimed:0,shots:0,kinds:{},dir:[0,0],lastX:player.x,enemyKinds:{},spawnT:[]});
 WT.newSec();return r;
};
WT.newSec=function(){WT.cur={nB:0,nBmax:0,nE:0,nEmax:0,fired:0,near:0,safe:[],hits:0,frames:0};};
WT.hazards=function(sight){
 const P=player,H=[];
 for(const b of eBullets){if(!b||b.dead||b._friendly)continue;if(Math.abs(b.x-P.x)>sight||Math.abs(b.y-P.y)>sight)continue;
  H.push([b.x,b.y,b.vx||0,b.vy||0,Math.max(4,Math.min(b.w||8,b.h||8)*.5)]);}
 for(const e of enemies){if(!e||e.dead||e._dyingT!=null||e.prop||e._prop||e.y<PLAY.y)continue;if(Math.abs(e.x-P.x)>sight||Math.abs(e.y-P.y)>sight)continue;
  H.push([e.x,e.y,e.vx||0,e.vy||0,Math.max(10,Math.min(e.w||30,e.h||30)*.32)]);}
 if(WT.seeHazards){
  /* stage hazards outside eBullets: Stage 2 fire debris (ballistic, r 9 + ship 8) and the falling
     firewall (its catch box is +-0.34*150*sc, sc growing 0.9 -> 2.15 over FIRE_CROSS) */
  if(typeof fireDebris!=='undefined')for(const d of fireDebris){if(d.dead||d.delay>0)continue;if(Math.abs(d.x-P.x)>sight||Math.abs(d.y-P.y)>sight)continue;H.push([d.x,d.y,d.vx||0,d.vy||0,d.r||9]);}
  const W=typeof wfx!=='undefined'&&wfx&&wfx.fseq&&wfx.fseq.wave;
  if(W){const sc=Math.min(2.15,(W.sc||.9)+.3),half=150*sc*.34,vy=(VH+300)/FIRE_CROSS/60;
   for(let k=-2;k<=2;k++)H.push([W.x+k*half/2.5,W.y,0,vy,half*.55]);}
 }
 return H;
};
WT.botInput=function(){
 const K=Input.keys,B=WT.B,P=player;
 K.j=true;K.c=false;
 if(WT.frame%B.every===0){
  const H=WT.hazards(B.sight),L=camLeftX()+14,R=camRightX()-14,T=PLAY.y+60,Bo=VH-28,homeY=VH-90;
  const tgt=enemies.filter(e=>!e.dead&&e._dyingT==null&&e.y>PLAY.y&&e.y<P.y-40).sort((a,b)=>b.y-a.y)[0];
  let best=[0,0],bs=-1e9;
  for(const dx of [-1,0,1])for(const dy of [-1,0,1]){
   let clear=60;const n=Math.hypot(dx,dy)||1;
   for(let t=3;t<=B.horizon;t+=3){
    const x=clamp(P.x+dx/n*WT.vp*t,L,R),y=clamp(P.y+dy/n*WT.vp*t,T,Bo);
    for(const h of H){const d=Math.hypot(h[0]+h[2]*t-x,h[1]+h[3]*t-y)-h[4]-9;if(d<clear)clear=d;}
   }
   const fx=clamp(P.x+dx*WT.vp*B.every,L,R),fy=clamp(P.y+dy*WT.vp*B.every,T,Bo);
   const s=Math.min(clear,40)-B.home*Math.abs(fy-homeY)-(tgt?B.aim*Math.abs(fx-tgt.x):0)-(dx||dy?.5:0);
   if(s>bs){bs=s;best=[dx,dy];}
  }
  WT.dir=best;
 }
 K.a=WT.dir[0]<0;K.d=WT.dir[0]>0;K.w=WT.dir[1]<0;K.s=WT.dir[1]>0;
};
WT.safeFrac=function(){
 const L=camLeftX()+14,R=camRightX()-14,T=VH*.45,Bo=VH-28,cols=12,rows=7;let safe=0;
 const bs=eBullets.filter(b=>b&&!b.dead&&!b._friendly);
 for(let i=0;i<cols;i++)for(let j=0;j<rows;j++){
  const x=L+(R-L)*(i+.5)/cols,y=T+(Bo-T)*(j+.5)/rows;let ok=true;
  for(const b of bs){for(const t of [0,10,20,30]){if(Math.hypot(b.x+(b.vx||0)*t-x,b.y+(b.vy||0)*t-y)<16+Math.min(b.w||8,b.h||8)*.5){ok=false;break;}}if(!ok)break;}
  if(ok)safe++;
 }
 return safe/(cols*rows);
};
WT.sample=function(){
 const c=WT.cur,P=player;c.frames++;
 const bs=eBullets.filter(b=>b&&!b.dead&&!b._friendly&&b.y>PLAY.y-10&&b.y<VH+10);
 c.nB+=bs.length;c.nBmax=Math.max(c.nBmax,bs.length);
 const es=enemies.filter(e=>e&&!e.dead&&e._dyingT==null&&!e.prop&&!e._prop&&e.y>PLAY.y-20&&e.y<VH);
 c.nE+=es.length;c.nEmax=Math.max(c.nEmax,es.length);
 for(const e of es)if(!WT.eSeen.has(e)){WT.eSeen.add(e);WT.enemyKinds[e.type]=(WT.enemyKinds[e.type]||0)+1;WT.spawnT.push(+WT.F.clock.toFixed(1));}
 for(const b of bs){
  if(Math.hypot(b.x-P.x,b.y-P.y)<100)c.near++;
  if(WT.seen.has(b))continue;WT.seen.add(b);c.fired++;WT.shots++;
  const sp=Math.hypot(b.vx||0,b.vy||0)*60;WT.speeds.push(Math.round(sp));
  const a1=Math.atan2(b.vy||0,b.vx||0),a2=Math.atan2(P.y-b.y,P.x-b.x);let d=Math.abs(a1-a2)%(Math.PI*2);if(d>Math.PI)d=Math.PI*2-d;
  if(d<.14&&sp>1)WT.aimed++;
  WT.kinds[b.kind]=(WT.kinds[b.kind]||0)+1;
 }
 if(WT.frame%6===0)c.safe.push(WT.safeFrac());
 const dx=Math.abs(P.x-WT.lastX);if(dx>WT.vp&&dx<12)WT.vp=dx;WT.lastX=P.x;
 if(c.frames>=60){WT.sec.push({nB:+(c.nB/c.frames).toFixed(1),nBmax:c.nBmax,nE:+(c.nE/c.frames).toFixed(1),nEmax:c.nEmax,fired:c.fired,near:+(c.near/c.frames).toFixed(2),
   safe:c.safe.length?+Math.min(...c.safe).toFixed(2):1,safeAvg:c.safe.length?+(c.safe.reduce((a,b)=>a+b,0)/c.safe.length).toFixed(2):1,hits:WT.hits});WT.newSec();}
};
WT.steps=function(n){
 for(let i=0;i<n;i++){
  if(state!==GS.PLAY||WT.F.done)break;
  stageLoadTick();WT.F.input(1/60);WT.botInput();stateT+=1/60;run.shield=0;
  updatePlay(1/60);WT.frame++;WT.sample();
  /* the scenery clock (mapScroll, terrain rows that ground waves wait for) advances inside the
     background draw, exactly as in the wave recorder: one drawWorld per three simulation steps */
  if(WT.frame%3===0){ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;drawWorld(3/60);}
 }
 return {clock:WT.F.clock,done:WT.F.done,state,events:WT.F.events.length,expected:WT.F.expected,hits:WT.hits};
};
WT.result=function(){
 const sp=WT.speeds.slice().sort((a,b)=>a-b),q=p=>sp.length?sp[Math.min(sp.length-1,Math.floor(p*sp.length))]:0;
 const mins=WT.sec.length/60;
 return {stage:WT.stage,diff:WT.diff,bot:WT.bot,seconds:WT.sec.length,hits:WT.hits,hitsRaw:WT.hitsRaw,hitsPerMin:mins?+(WT.hits/mins).toFixed(2):0,hitLog:WT.hitLog,
  shots:WT.shots,shotsPerSec:mins?+(WT.shots/WT.sec.length).toFixed(2):0,aimedShare:WT.shots?+(WT.aimed/WT.shots).toFixed(2):0,
  speed:{p10:q(.1),p50:q(.5),p90:q(.9)},kinds:WT.kinds,enemyKinds:WT.enemyKinds,spawnT:WT.spawnT,vp:WT.vp,waves:WT.F.events.map(e=>({i:e.i,clock:+e.clock.toFixed(1),types:e.types})),sec:WT.sec};
};
