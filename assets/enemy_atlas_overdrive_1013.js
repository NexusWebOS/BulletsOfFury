/* The guide reuses the real Overdrive mission, unit, boss and projectile owners.
   Only loaded by expansion/topdown/index.html?enemyAtlas=1, after the save guard. */
(()=>{'use strict';
 const clock=window.BOF_ATLAS_CLOCK,TD=window.TD;
 if(!clock||!TD||new URLSearchParams(location.search).get('enemyAtlas')!=='1')return;
 const G=TD.game,M=TD.M,W=TD.World,Cam=TD.Cam;
 const A={entry:null,actor:null,error:null,seen:new Map(),serial:0,elapsed:0,started:0,cycle:0,muted:true,difficulty:'normal',manualTarget:null};
 const input=TD.Input.update,follow=Cam.follow,hurt=TD.hurtPlayer;
 const missionGuards=new Map(TD.MISSIONS.map(m=>[m,{canSpawnBoss:m.canSpawnBoss,canReinforce:m.canReinforce}]));
 TD.Input.update=function(){input.call(this);if(A.entry){this.state={};this.last={};this.pointer.buttons={};this.pointer.active=false;}};
 TD.hurtPlayer=function(){if(A.entry)return false;return hurt.apply(this,arguments);};
 Cam.follow=function(tx,ty,k){
  if(A.entry&&A.actor&&!G.convoy){const b=A.actor,p=G.player,actors=b.tanks?b.tanks.filter(q=>!q.dead):[b];
   let xs=[p.x-24,p.x+24],ys=[p.y-40,p.y+35];
   if(b.bounds){const q=b.bounds();xs.push(q.left,q.right);ys.push(q.top,q.bottom);}
   else for(const q of actors){const margin=b.tanks?100:b.type?65:115;xs.push(q.x-margin,q.x+margin);ys.push(q.y-margin,q.y+margin);}
   const l=Math.min(...xs),r=Math.max(...xs),t=Math.min(...ys),bot=Math.max(...ys);
   this.zoom=Math.min(1,TD.VW/(r-l+80),TD.VH/(bot-t+75));tx=(l+r)/2;ty=(t+bot)/2;k=1;
   // The guide camera can revisit a specimen; museum campaign push-scroll does
   // not pin an isolated moving boss underneath the bottom of the preview.
   this.minY=0;this.maxY=W.h;if(G.pushY!=null)G.pushY=W.h;
  }return follow.call(this,tx,ty,k);
 };
 function mute(on){A.muted=!!on;TD.Audio.master=A.muted?0:.65;
  if(A.muted){TD.Audio.stopEffects();TD.Audio.stopMusic();TD.Frontend.stopVoice();}
  else{TD.Audio.unlock();TD.Audio.playMusic(G.boss?'boss2':'level2');}
 }
 function protectTarget(){const p=G.player;p.inv=0;p.dead=false;p.flash=0;
  Object.defineProperty(p,'hp',{configurable:true,enumerable:true,get(){return this.max;},set(){}});
  // The native truck driver normally owns its position; a guide drag temporarily
  // supplies that position without changing enemy steering or projectile owners.
  if(G.convoy)for(const axis of ['x','y']){let value=p[axis];Object.defineProperty(p,axis,{configurable:true,enumerable:true,get(){return A.manualTarget?.[axis]??value;},set(v){value=v;}});}
 }
 function unitPlace(type){
  const d=TD.ET[type],range=d.prefer?Math.min(225,(d.prefer[0]+d.prefer[1])*.5):170;
  for(const y of [280,350,450,600,800])for(const x of [400,340,460,280,520]){
   if(y+range>=W.h-65)continue;
   if(!W.solidAt(x,y)&&!W.solidAt(x,y+range)&&!W.rayBlock(x,y,x,y+range))return{x,y,px:x,py:y+range};
  }return{x:W.w/2,y:W.h/2-100,px:W.w/2,py:W.h/2+100};
 }
 function spawnUnit(s){
  let u;
  if(/^convoy/.test(s.type)){
   const kind={convoyJet:'jet',convoyTruck:'truck',convoyRunner:'runner',convoyElite:'elite'}[s.type];
   G.convoy.phase='pursuit';G.convoy.age=8;G.convoy.combat=2;G.convoy.nextWave=1e6;
   u=TD.Convoy.spawn(G,kind,kind==='jet'?320:180,kind==='jet'?55:kind==='truck'?440:480,0);
  }else{
   const p=unitPlace(s.type);G.player.x=p.px;G.player.y=p.py;G.cp={x:p.px,y:p.py};
   u=TD.makeUnit(s.type,p.x,p.y,{a:0,mode:'alert',aware:1,sees:true,fireCd:.25,goal:{x:p.px,y:p.py}});
   G.units.push(u);TD.Stealth.phase='ALERT';TD.Stealth.timer=999;
  }
  A.actor=u;A.cycle=G.time;return u;
 }
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 async function start(entry,difficulty='normal'){
  const serial=++A.serial;A.entry=null;A.actor=null;A.error=null;A.manualTarget=null;A.seen.clear();A.elapsed=0;clock.paused=false;
  try{
   const s=entry.spawn||{};if(!['overdrive-unit','overdrive-boss'].includes(s.method))throw new Error('Unsupported Overdrive spawn method '+s.method);
   if(s.method==='overdrive-unit'&&!TD.ET[s.type])throw new Error('Unknown Overdrive enemy '+s.type);
   let stage=/^convoy/.test(s.type||'')?6:s.kind==='gosfer'?3:(s.stage||entry.stages?.[0]||2);
   for(const [m,guard]of missionGuards)Object.assign(m,guard);
   G.sel=TD.MISSIONS.findIndex(m=>m.id===stage);if(G.sel<0)throw new Error('Unknown Overdrive mission '+stage);
   TD.pilot=TD.MISSIONS[G.sel].mode==='foot'?'yuri':'cole';TD.difficulty=TD.DIFFICULTIES[difficulty]?difficulty:'normal';
   TDGAME.start();A.difficulty=TD.difficulty;A.entry=entry;A.started=G.time;A.lastTime=G.time;
   const mission=TD.MISSIONS[G.sel];mission.canSpawnBoss=()=>false;mission.canReinforce=()=>false;
   G.units=[];G.shots=[];G.eshots=[];G.props=[];G.structures=[];G.pickups=[];G.wrecks=[];G.grenades=[];G.msgs=[];G.ally=null;G.boss=null;G.bossIntro=null;G.bossDeadT=null;G.reinfT=1e6;
   TD.FX.list=[];TD.Achievements.queue=[];TD.Input.combatLatch.clear();W.load(mission.map.w,mission.map.h,mission.map.rects);
   protectTarget();mute(A.muted);
   if(s.method==='overdrive-unit')spawnUnit(s);
   else{
    const factories={warrior:'makeWarrior',fortress:'makeFortress',machinists:'makeMachinists',exhibit:'makeExhibit',gosfer:'makeGosfer'},factory=factories[s.kind];
    if(!factory||typeof TD[factory]!=='function')throw new Error('Unknown Overdrive boss '+s.kind);
    const at=mission.data.boss||{x:400,y:195};A.actor=G.boss=TD[factory](G,at.x,at.y);
    G.player.x=400;G.player.y=s.kind==='gosfer'?428:s.kind==='warrior'?635:s.kind==='exhibit'?395:570;G.player.a=G.player.aim=Math.PI;
    if(s.kind==='fortress')for(const [x,y]of [[340,225],[470,225],[400,185]])G.units.push(TD.makeUnit('robotHeavy',x,y,{a:0,role:'sentry',mode:'alert',aware:1,sees:true}));
    if(s.kind==='machinists'&&s.member)for(const q of A.actor.tanks)if(q.crew!==s.member){q.dead=true;for(const k in q.parts)q.parts[k]=0;}
    if(s.kind==='exhibit'&&s.phase>1){const b=A.actor;b.state='recover';b.cool=.5;b.gauge=1;
     for(const key of s.phase>=3?['podL','podR','turret']:['podL','podR']){const p=b.partPos[key]();b.hit(p.x,p.y,1,10000);}
    }
   }
   const keys=[mission.map.key,...(entry.artKeys||[])].filter(k=>ART.has(k));ART.warm(keys);
   for(let n=0;n<200&&keys.some(k=>!ART.get(k));n++){await wait(25);if(serial!==A.serial)return;}
   if(serial!==A.serial)return;
   TDGAME.resize();Cam.follow(G.player.x,G.player.y,1);TDGAME.render();return snapshot();
  }catch(e){A.error=String(e.message||e);return snapshot();}
 }
 function actorHealth(b){if(!b)return null;if(typeof b.hpFrac==='function')return b.hpFrac();return b.max?b.hp/b.max:1;}
 function snapshot(){const b=A.actor;return{ready:!!window.TDGAME,game:'overdrive',entry:A.entry?.id,error:A.error,elapsed:A.elapsed,frames:clock.frames,paused:clock.paused,speed:clock.speed,stage:G.mission,difficulty:A.difficulty,
  actor:b?{type:b.type||A.entry?.spawn.kind,hp:typeof b.hp==='number'?b.hp:actorHealth(b)*100,maxhp:typeof b.max==='number'?b.max:100,dead:!!b.dead,x:b.x,y:b.y,phase:b.form||b.phase||b.state,pattern:b.mode||b.state,health:actorHealth(b)}:null,
  projectiles:[...A.seen.keys()],liveProjectiles:G.eshots.length,unitCount:G.units.filter(u=>!u.dead).length,target:{x:G.player?.x,y:G.player?.y},protectedTarget:true};}
 function after(){if(!A.entry||A.error)return;A.elapsed+=Math.max(0,G.time-(A.lastTime||0));A.lastTime=G.time;G.reinfT=1e6;G.bossDeadT=null;
  G.player.inv=0;G.player.flash=0;G.ally=null;
  for(const s of G.eshots)if(!s.dead&&!A.seen.has(s.k))A.seen.set(s.k,{...s});
  if(G.convoy){G.convoy.nextWave=1e6;G.convoy.combat=Math.min(G.convoy.combat,10);}
  if(A.entry.spawn.method==='overdrive-unit'){
   G.units=G.units.filter(u=>u===A.actor&&!u.dead);
   if(A.actor.dead||!G.units.length||G.time-A.cycle>22){G.units=[];G.eshots=[];spawnUnit(A.entry.spawn);}
  }
 }
 clock.after=after;
 function image(key,target){const g=ART.get(key);if(!g)return false;const c=target.getContext('2d'),z=Math.min(target.width/g.sw,target.height/g.sh);c.clearRect(0,0,target.width,target.height);c.imageSmoothingEnabled=false;c.drawImage(g.im,g.sx,g.sy,g.sw,g.sh,(target.width-g.sw*z)/2,(target.height-g.sh*z)/2,g.sw*z,g.sh*z);return true;}
 function projectiles(tiles){for(const tile of tiles||[]){const kind=tile.kind==='pellet'?'mg':tile.kind,c=tile.canvas.getContext('2d'),w=tile.canvas.width,h=tile.canvas.height;
  c.clearRect(0,0,w,h);c.imageSmoothingEnabled=false;const sample=A.seen.get(kind)||{k:kind,a:0,r:5,life:100};
  const s={...sample,x:w/2,y:h/2,t:G.t||0,drawLift:0};TD.drawShot(c,s,true);
 }}
 function hp(ratio){const b=A.actor;if(!b)return;const q=M.clamp(+ratio||.01,.01,1);
  if(b.tanks){for(const u of b.tanks)if(!u.dead){for(const k in u.parts)u.parts[k]=u.initial[k]*q;u.hp=u.max*q;}}
  else if(b.parts&&typeof b.max==='object'){for(const k in b.parts)b.parts[k]=b.max[k]*q;}
  else if(typeof b.max==='number')b.hp=b.max*q;
  TDGAME.render();
 }
 window.BOF_ENEMY_ATLAS={start,snapshot,image,projectiles,mute,hp,patterns:[],pattern(){return false;},
  pause(on){clock.paused=!!on;},speed(n){clock.speed=M.clamp(+n||1,.1,2);},step(){clock.paused=true;TDGAME.step(1);clock.frames++;after();},
  target(x,y){if(!G.player)return;const p={x:Cam.x+M.clamp(+x,0,1)*TD.VW/Cam.zoom,y:Cam.y+M.clamp(+y,0,1)*TD.VH/Cam.zoom};G.player.x=p.x;G.player.y=p.y;if(G.convoy)A.manualTarget=p;TDGAME.render();},
  get ready(){return !!window.TDGAME&&G.state!=='load';},get entry(){return A.entry;}
 };mute(true);
})();
