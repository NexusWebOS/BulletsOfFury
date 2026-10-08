/* Test-only native browser instrumentation. Never loaded by index.html. */
window.BAL7={initial:JSON.parse(JSON.stringify(run)),originalHit:playerHit,events:[],q:null};
playerHit=function(source){
 const Q=BAL7.q,alive=!player.dead,shield=run.shield,seat=_seat,weapon=run.weapon,level=run.wlevel;
 const r=BAL7.originalHit.apply(this,arguments);
 if(Q&&alive&&(player.dead||run.shield<shield))Q.hits.push({t:+Q.t.toFixed(3),seat,source:source||'unspecified',dead:!!player.dead,x:Math.round(player.x),y:Math.round(player.y),stack:new Error().stack.split('\n').slice(2,6).join('\n'),pattern:BAL7.pattern(),weapon,level});
 return r;
};
if(window.BOFOnline)window.BOFOnline.submitScore=()=>{};
BAL7.seed=function(n){let s=n>>>0;Math.random=()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};};
BAL7.meta=()=>({pilots:PILOTS.map(p=>({key:p.key,speed:p.spd,fire:p.fire})),weapons:WEAPONS.map((v,i)=>({i,name:v.name||v})),diffs:DIFFS,arcade:ARCADE_STOCK,coop:{count:COOP_COUNT_MUL,enemyHP:COOP_EHP_MUL,bossHP:COOP_BOSS_MUL},bindings:keybindFor(1),canvas:{w:VW,h:VH,play:PLAY}});
BAL7.setup=function(c){
 BAL7.q=null;BAL7.seed(c.seed||1007);ht27Stop();debugFight=null;coopOn=false;
 for(const k of Object.keys(run))delete run[k];Object.assign(run,JSON.parse(JSON.stringify(BAL7.initial)));
 diffKey=c.diff;run.mode=c.mode||'arcade';DIFF=difficultyForRun(run.mode,diffKey);run.pilot=c.pilot||'yuri';pilotIndex=PILOTS.findIndex(p=>p.key===run.pilot);PILOTMOD={...PILOTS[pilotIndex]};
 run.lives=DIFF.startLives;run.contUsed=0;run.contBonus=0;run.bombs=DIFF.startBombs;run.shield=0;run.forge={};run.wvars=[];run.forgeForms={};run.infusion=null;run._megaShield=false;
 if(c.coop){coopOn=true;Object.assign(run2,JSON.parse(JSON.stringify(run)),{pilot:'falva'});p2Index=PILOTS.findIndex(p=>p.key===run2.pilot);PILOTMOD2={...PILOTS[p2Index]};}
 beginStage(c.stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;fb2Talk=null;special=null;thunderStorm=null;s6Opening=null;s6Wing=null;
 stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;bossDefeated=false;subBossDone=true;subBossTriggered=true;groundTargetingReset();tb28Reset();polishLanes=[];stageTimer=0;
 if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);window.B=c.mini?subBoss:boss;
 B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=B._er26?.home||B.ty||160;B._drawY=B.y;
 if(c.form!=null){j3Encounter(B,['host','sequence'].includes(c.form)?0:c.form==='ghost'?1:2);if(!['host','ghost','home','sequence'].includes(c.form))j3Mimic(B,+c.form);on5FightStart(B);const D=dr5State(B);D.introWanted=false;D.introSeen=true;B.x=worldWidth()/2;B.y=205;B._drawY=B.y;const J=j3State(B);if(J.mimic>0){const donor=gd4Create(B,J.mimic);donor.p.x=B.x;donor.p.y=B.y;}}
 if(B._rebels){const R=B._rebels;rf28Init(B,R);R.frIntro={done:true};const G=rg4Init(B);G.scene=null;G.rescueDone=true;G.releaseAt=G.age+999;H3.release=false;for(const q of R.ships){q.mode='fight';q.x=worldWidth()/2+(q.i-2)*65;q.y=170+(q.i%2)*45;}rg4Warm();XART.rdy(RA7.sheet);}
 if(c.ace){whvAceSpawn(B);B._whv.mode='ace';const A=B._whv.ace;A.st='fight';A.x=worldWidth()/2;A.y=180;}
 BOFCinematicDirector.cancel();story=null;fb2Talk=null;thaw=null;B._noHit=false;B.enter=false;
 const lv=c.level??3;run.weapon=c.weapon??0;run.wlevel=lv;run.wlevels=WEAPONS.map(()=>lv);run.spaceWeapon=c.spaceWeapon??0;run.spaceLevels=[lv,lv,lv];run.missileLevel=c.missileLevel??1;run.speed=c.speed??0;run.speedLevel=run.speed;run._lifeCombatT=0;run._lifeThreat=0;run._threatBuild=0;
 player.x=worldWidth()/2;player.y=VH-110;camX=clamp(player.x-VW/2,0,worldWidth()-VW);player.invuln=0;player.dead=false;player.out=false;player._spin=null;player._voidDeath=null;player.roll=player.somer=null;player.fireCd=0;run.shield=c.shield||0;timeScale=1;
 if(c.coop){Object.assign(run2,{weapon:run.weapon,wlevel:lv,wlevels:run.wlevels.slice(),spaceWeapon:run.spaceWeapon,spaceLevels:run.spaceLevels.slice(),missileLevel:run.missileLevel,speed:run.speed,shield:0});player2.reset();player2.x=player.x+55;player.x-=55;player2.y=player.y;player2.dead=false;player2.out=false;player2.invuln=0;}
 for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps?.();
 HC1007.history=[];HF7.events=[];HC7.events=[];RA7.events=[];
 BAL7.q={c,t:0,frames:0,hits:[],samples:[],patterns:{},commands:[0,0],queue:[],observe:0,decision:0,shots:0,seenShots:new WeakSet(),peakBullets:0,moves:0,rolls:0,bombsUsed:0,initialStock:run.lives,initialHP:BAL7.health(),initialParts:BAL7.parts(),partDamage:0,previousParts:BAL7.parts(),startForm:c.form,done:false,outcome:null,finite:true,attackClock:0};
 hc1007Warm();if(c.stage===8){hc7Warm();aa5Warm();}drawWorld(0);
 if(c.recovery)playerHit('balance: intentional recovery death');
 return{hp:BAL7.q.initialHP,stock:run.lives,playerSpeed:playerBaseSpeed(),pilot:run.pilot,level:run.wlevel,boss:B.kind||B._ship,world:worldWidth()};
};
BAL7.health=function(){if(!window.B)return 0;if(B._rebels)return B._rebels.ships.reduce((n,q)=>n+Math.max(0,q.hp||0),0);return Math.max(0,B.hp||0);};
BAL7.pools=function(){const J=B?._r30&&j3State(B);if(!J)return null;const hp=J.hp.slice();if(J.encounter===2)hp[J.active]=B.hp;return{hp,max:J.max.slice(),encounter:J.encounter,mimic:J.mimic,active:J.active};};
BAL7.parts=function(){const ps=B?.parts||B?._mr27?.parts||B?._bomber?.parts||B?._hd1003?.parts||[];return Object.fromEntries(ps.map((p,i)=>[p.id||p.name||i,{hp:Math.max(0,p.hp||0),dead:!!(p.destroyed||p.dead),max:p.maxhp||p.max||0}]));};
BAL7.pattern=function(){return [B?._hc1007?.mode,B?._hc1007?.cross?'cross':null,B?._bomber?.mode,B?._er26?.mode,B?._s4war?.mode,B?._hd1003?.attack,B?._r30?.mode,B?._r30?.hf7?.sig?.def?.name,B?._r30?.hc7Rift?.phase,B?._whv?.mode,B?._whv?.ace?.st,...(B?._rebels?.ships||[]).map(q=>q.rg4?.act?.kind)].filter(Boolean).join('|');};
BAL7.observe=function(){
 const bullets=eBullets.filter(q=>!q.dead&&q.x>=camLeftX()-15&&q.x<=camRightX()+15&&q.y>=PLAY.y&&q.y<=VH).map(q=>({x:q.x,y:q.y,vx:(q.vx||0)*60,vy:(q.vy||0)*60,r:Math.max(5,Math.min(20,(q.w||8)/2))}));
 const lines=[];let circle=null;
 const C=hc1007CrossState(B);if(C&&!['gap','done','dissolve'].includes(C.mode))for(const L of C.rays)lines.push({...L,warn:C.mode==='tell'});
 if(B._hc1007&&!B._hc1007.cross)for(const L of B._hc1007.lines||[])lines.push({...L,warn:!L.fire});
 if(B._r30){const H=hf7Sample(B);if(H&&!['recover','gap','dissolve'].includes(H.phase))for(const L of H.lines)lines.push({...L,warn:H.phase==='tell'});const V=B._r30.hc7Rift;if(V&&V.phase!=='recover'){circle={x:V.x,y:V.y,r:V.radius+22};for(const L of V.lanes)lines.push({...L,warn:L.phase==='tell'});}}
 for(const q of B._rebels?.ships||[]){const A=q.rg4?.act;if(A?.kind==='rookhook'&&['charge','cast'].includes(A.phase))lines.push({x:q.x,y:q.y+25,ex:q.x+Math.cos(A.a)*A.range,ey:q.y+25+Math.sin(A.a)*A.range,width:24,warn:A.phase==='charge'});}
 const targets=_lockTargets().filter(t=>!t.dead&&t.x>=camLeftX()&&t.x<=camRightX()&&t.y>=PLAY.y&&t.y<player.y-35);
 const target=targets.sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0];
 const bodies=(B._rebels?B._rebels.ships:B._whv?.mode==='ace'?[B._whv.ace]:[B]).filter(t=>t&&!t.dead&&!t.enter).map(t=>({x:t.x,y:t.y,w:t.w||60,h:t.h||70}));
 return{time:BAL7.q.t,bullets,lines,circle,target:target?{x:target.x,y:target.y}:null,bodies};
};
BAL7.decide=function(S){
 const Q=BAL7.q,spd=playerBaseSpeed()*60,left=camLeftX()+18,right=camRightX()-18,top=PLAY.y+45,bottom=VH-35;
 let best=Infinity,choice=[0,0],danger=0;
 for(const dy of [-1,0,1])for(const dx of [-1,0,1]){
  const norm=dx&&dy?Math.SQRT1_2:1;let cost=0;
  for(const t of [.12,.30,.5]){
   const x=clamp(player.x+dx*norm*spd*t,left,right),y=clamp(player.y+dy*norm*spd*t,top,bottom);
   for(const b of S.bullets){const d=Math.hypot(x-b.x-b.vx*t,y-b.y-b.vy*t);cost+=Math.max(0,26+b.r-d)*4;}
   for(const L of S.lines){const d=s81003Distance(x,y,L);cost+=Math.max(0,(L.width||16)/2+20-d)*(L.warn?4:10);}
   if(S.circle)cost+=Math.max(0,S.circle.r-Math.hypot(x-S.circle.x,y-S.circle.y))*2;
   for(const b of S.bodies){const overlap=Math.min(b.w/2+20-Math.abs(x-b.x),b.h/2+20-Math.abs(y-b.y));if(overlap>0)cost+=overlap*5;}
  }
  if(!dx&&!dy)danger=cost;
  const fx=clamp(player.x+dx*spd*.4,left,right),fy=clamp(player.y+dy*spd*.4,top,bottom);
  const preferredY=Q.c.rangeAware&&S.target?clamp(S.target.y+(run.weapon===4?flameReach(run.wlevel)*.72:160),PLAY.y+100,VH-70):VH-120;
  cost+=(S.target?Math.abs(fx-S.target.x):Math.abs(fx-worldWidth()/2))*.10+Math.abs(fy-preferredY)*(Q.c.rangeAware?.14:.055)+(dx||dy?1:0);
  if(cost<best){best=cost;choice=[dx,dy];}
 }
 Q.commands=Q.c.controller==='stationary'?[0,0]:choice;
 if(Q.c.evasion&&danger>65&&!player.roll&&!player.somer&&!(player._rollCool>0)){startRoll(choice[0]||1);if(player.roll)Q.rolls++;}
};
BAL7.step=function(n){
 const Q=BAL7.q,dt=1/(Q.c.fps||60);
 for(let i=0;i<n&&!Q.done;i++){
  if(state!==GS.PLAY){Q.done=true;Q.outcome=state;break;}
  Q.t+=dt;Q.frames++;for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps?.();
  const hold=a=>(keybindFor(1)[a]||[]).filter(k=>!k.startsWith('pad_')).forEach(k=>Input.keys[k]=true);
  if(!player.dead){
   if(Q.t>=Q.observe){Q.queue.push(BAL7.observe());Q.observe=Q.t+.1;}
   while(Q.queue.length&&Q.queue[0].time<=Q.t-(Q.c.reaction??.25)){const S=Q.queue.shift();BAL7.decide(S);}
   const [dx,dy]=Q.commands;if(dx<0)hold('left');if(dx>0)hold('right');if(dy<0)hold('up');if(dy>0)hold('down');if(Q.c.fire!==false)hold('fire');
  }
  if(Q.c.coop&&!player2.dead&&!player2.out){
   const keys=keybindFor(2);if(Q.c.fire!==false)for(const k of keys.fire||[])if(!k.startsWith('pad_'))Input.keys[k]=true;
   if(Q.c.p2Controller==='mirror'){const [x,y]=Q.commands;for(const a of [x<0?'right':x>0?'left':null,y<0?'up':y>0?'down':null].filter(Boolean))for(const k of keys[a]||[])if(!k.startsWith('pad_'))Input.keys[k]=true;}
  }
  const x=player.x,y=player.y;updatePlay(dt);if(Q.frames%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(dt*6);}Q.moves+=Math.hypot(player.x-x,player.y-y);
  if(Q.frames===1)Q.effectiveLoadout={weapon:run.weapon,level:run.wlevel,spaceWeapon:run.spaceWeapon,spaceLevel:run.spaceLevels?.[run.spaceWeapon]};
  const parts=BAL7.parts();for(const [k,p] of Object.entries(parts)){const old=Q.previousParts[k];if(old)Q.partDamage+=Math.max(0,old.hp-p.hp);}Q.previousParts=parts;
  for(const b of pBullets)if(!Q.seenShots.has(b)){Q.seenShots.add(b);Q.shots++;}Q.peakBullets=Math.max(Q.peakBullets,eBullets.length);
  const pattern=BAL7.pattern();Q.patterns[pattern]=(Q.patterns[pattern]||0)+dt;
  if(Q.frames%Math.round(5/dt)===0)Q.samples.push({t:Math.round(Q.t),hp:BAL7.health(),lives:run.lives,dead:player.dead,weapon:run.weapon,level:run.wlevel,supplies:powerups.map(p=>p.kind),threat:run._lifeThreat||0});
  if(!Number.isFinite(player.x+player.y+B.x+B.y)){Q.finite=false;Q.done=true;Q.outcome='nonfinite';}
  if(Q.c.firstLife&&player.dead){Q.done=true;Q.outcome='death';}
  if(B.dead||bossDefeated||(Q.c.mini&&!subBossActive&&subBossDone)||(B.hp<=0&&Q.c.form!=='sequence')){Q.done=true;Q.outcome=Q.c.form!=null?'phase-depleted':'encounter-defeated';}
  if(Q.c.form!=null&&Q.c.form!=='sequence'&&B._r30){const J=j3State(B),id=J.encounter===0?'host':J.encounter===1?'ghost':J.mimic==null?'home':String(J.mimic);if(id!==String(Q.c.form)){Q.done=true;Q.outcome='form-transition';}}
  if(Q.t>=Q.c.seconds){Q.done=true;Q.outcome='time-limit';}
 }
 return{t:Q.t,done:Q.done,outcome:Q.outcome,hp:BAL7.health(),deaths:Q.hits.filter(h=>h.dead).length};
};
BAL7.result=function(){const Q=BAL7.q,pools=BAL7.pools(),startHP=Q.c.form!=null&&/^\d$/.test(Q.c.form)?pools?.hp[+Q.c.form]:BAL7.health();return{...Q,seenShots:undefined,queue:undefined,commands:undefined,previousParts:undefined,attackOwner:undefined,health:BAL7.health(),hpRatio:startHP/Math.max(1,Q.initialHP),phasePools:pools,finalParts:BAL7.parts(),finalLives:run.lives,finalBombs:run.bombs,finalWeapon:run.weapon,finalLevel:run.wlevel,state,frameSize:[cv.width,cv.height],events:{encounter:HC1007.history,finale:HF7.events,rift:HC7.events,rebels:RA7.events}};};
