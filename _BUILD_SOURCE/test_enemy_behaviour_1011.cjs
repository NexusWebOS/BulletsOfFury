module.exports=function(vm,c,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof EB11',c)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/enemy_behaviour_1011.js'),'utf8'),c,{filename:'enemy_behaviour_1011.js'});
 console.log('=== Enemy behaviour 1011: visible commitments and difficulty steps ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const out={};
  function setup(stage,diff='normal'){
   ht27Stop();coopOn=false;diffKey=diff;run.mode='arcade';DIFF=difficultyForRun(run.mode,diff);run.pilot='yuri';
   beginStage(stage);setState(GS.PLAY);BOFCinematicDirector.cancel();story=fb2Talk=special=null;player.reset();player.dead=player.out=false;player.alive=true;player.invuln=999;
   player.x=worldWidth()/2;player.y=VH*.82;camX=player.x-VW/2;enemies=[];eBullets=[];pBullets=[];orbBeams=[];
   boss=subBoss=null;bossActive=subBossActive=false;stagePlan=[];aiQueue=[];stageTimer=20;EB11.nextTell=0;EB11.clock=0;
   let seed=1011;Math.random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
  }
  function unit(type,y=130){spawnEnemy(type,worldWidth()/2,y,{inPlace:true});const e=enemies.at(-1);e.y=y;e._entry=0;delete e._esh;return e;}
  function tick(e,fn,n){for(let i=0;i<n;i++){EB11.clock+=1/60;const prev=ai27Begin(e,1/60);e.t+=1/60;fn(e,1/60);ai27End(e,prev);}}
  function warning(e,fn){for(let i=0;i<300;i++){tick(e,fn,1);const q=eb11Queue(e);if(q?._eb11?.started&&!q.fired&&q.t>=.15)return q;}return null;}
  setup(6);let e=unit('s6lancer',-120);e._s6Act={t:0,at:.1,dur:.3,fired:false,release:()=>eShootT(e.x,e.y,Math.PI/2,3,'s6wind')};
  tick(e,(e,dt)=>eb11QueueTick(e,'_s6Act',dt),180);
  out['offscreen releases remain queued without bullets or consumed windup']=eBullets.length===0&&e._s6Act&&!e._s6Act.fired&&e._s6Act.t===0;
  e.y=130;tick(e,(e,dt)=>eb11QueueTick(e,'_s6Act',dt),45);
  out['fresh visible entry still owes a full tell']=eBullets.length===0;
  tick(e,(e,dt)=>eb11QueueTick(e,'_s6Act',dt),45);
  out['a formerly blocked release fires once after its visible warning']=eBullets.length===1;
  setup(6);e=unit('s6lancer');const q=warning(e,s6StormTick),locked=q?._eb11?.target&&{...q._eb11.target};
  out['aim-lock control moves the player before any projectile exists']=!!q&&!q.fired&&eBullets.length===0;player.x+=100;
  tick(e,s6StormTick,60);
  const shots=eBullets.filter(b=>!b.dead);
  out['native lancer releases its complete three-shot pattern']=shots.length===3;
  out['native aimed volley keeps the target fixed through the tell']=!!locked&&shots.some(b=>Math.abs(Math.atan2(b.vy,b.vx)-Math.atan2(locked.y-b.y,locked.x-b.x))<.02);
  setup(6);e=unit('s6lancer');warning(e,s6StormTick);e._stagger=1;
  tick(e,(e,dt)=>eb11QueueTick(e,'_s6Act',dt),100);
  out['stun cannot release a queued attack']=eBullets.length===0;
  e._stagger=0;tick(e,s6StormTick,10);out['stun recovery does not skip the new tell']=eBullets.length===0;
  e.dead=true;tick(e,(e,dt)=>eb11QueueTick(e,'_s6Act',dt),90);out['dead queue owner cannot fire']=eBullets.length===0&&!e._s6Act;
  setup(8);e=unit('s8spread',100);e.x=camLeftX()-130;tick(e,s8MegaTick,600);
  out['side-entry alien spread wing flies into view and fires']=eBullets.length>0&&e._frRealmAI.home>camLeftX();
  setup(6);spawnEnemy('s6dart',worldWidth()/2,-90,{_jetManeuver:'dash'});e=enemies.at(-1);
  tick(e,jetManeuverTick,100);
  out['authored dash route does not fire during its offscreen approach']=e.pattern==='jetmaneuver'&&eBullets.length===0;
  tick(e,jetManeuverTick,300);
  out['authored dash route fires its nose guns before a finite committed dive']=eBullets.length>=4&&e._jetManeuver._eb11.phase==='dive'&&e.dead;
  setup(9);e=unit('gleech',100);e.x=camLeftX()-30;tick(e,s9ChaosTick,540);
  out['rim leech enters the actual camera edge and fires']=eBullets.length>0&&e.x>=camLeftX()+12;
  for(const type of ['pmine','vmanta','tsplit','cbreak']){
   setup(9);e=unit(type,90);e._stagger=.42;tick(e,s9ChaosTick,720);
   out[type+' delayed entry expires and cannot permanently suppress firing']=e._stagger===0&&eBullets.length>0;
  }
  setup(5);e=unit('s5frigate');tick(e,s5SpaceTick,1500);
  out['held space frigate attacks then leaves instead of oscillating forever']=e._eb11.attacks>=3&&e._eb11.leave&&e.dead;
  const metrics={};
  for(const [stage,type,fn] of [[2,'cruc',volcTick],[3,'s3tank',s3IceTick],[4,'s4interceptor',s4ChaseTick],
    [5,'s5frigate',s5SpaceTick],[6,'s6lancer',s6StormTick],[7,'s7tank',s7ToxicTick],[8,'s8interceptor',s8MegaTick],[9,'s9gunship',s9VoidTick]]){
   const row=[];for(const diff of ['normal','hard','furious']){
    setup(stage,diff);e=unit(type);tick(e,fn,720);row.push({shots:eBullets.length,attacks:e._eb11?.attacks||0,cycles:e._frRealmAI?.seq||0});
    out[stage+' '+diff+' native enemy emits actual ordnance']=eBullets.length>0||orbBeams.length>0;
   }metrics[stage]=row;
   out[stage+' Furious increases actual attack output over Normal']=row[2].shots>row[0].shots;
  }
  for(const stage of [2,3]){
   const speeds=[];for(const diff of ['normal','hard','furious']){
    setup(stage,diff);e=unit(stage===2?'ash':'s3interceptor');player.x=2000;e._ac10Ram={phase:'ram',t:0,speed:90,angle:0};
    tick(e,stage===2?volcTick:s3IceTick,100);speeds.push(e._ac10Ram.speed);
    out[stage+' '+diff+' small kamikaze remains unshielded and gunless']=!e._esh&&e.shoots===false&&eBullets.length===0;
   }
   out[stage+' ram speed grows Normal to Hard and further on Furious']=speeds[1]>speeds[0]&&speeds[2]-speeds[1]>speeds[1]-speeds[0];
  }
  const P=EB11.profiles;
  out['larger Furious step in cadence with a retained warning floor']=P.furious.rate-P.hard.rate>P.hard.rate-P.normal.rate&&P.furious.tell>=.45&&P.furious.recovery>=.25;
  out['Normal and Hard keep only two simultaneous native windups']=P.normal.slots===2&&P.hard.slots===2&&P.furious.slots===3;
  out.metrics=metrics;return out;
 })())`,c));
 const metrics=out.metrics;delete out.metrics;for(const [name,value] of Object.entries(out))ok(value,name);
 console.log('Enemy native difficulty measurements: '+JSON.stringify(metrics));
};
