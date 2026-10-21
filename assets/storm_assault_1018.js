"use strict";
/* Storm Sovereign: readable overload, live cockpit comms and a south-entry
   lightning wing. Native hull, module HP, Retina and hit-flash owners survive. */
const ST18={events:[],audio:[],draws:{bomb:0,impact:0,glow:0,radio:0},base:{
 load:stageLoadBegin,begin:beginStage,war:er26WarTick,helper:mr27HelperDraw,
 ground:groundTargetingDraw,draw:sa14Draw,rec:debugRecFrame,refresh:SC12.refresh,
 balls:p4EmitBalls,shot:stage4WarfareShot,rev:sa14Rev},lastBoss:null};
for(const bank of Object.values(ST18_ART))for(const a of bank.frames)XART._src[a.key]=a.path;
function st18Keys(){return Object.values(ST18_ART).flatMap(a=>a.frames.map(f=>f.key));}
function st18Log(event,data={}){ST18.events.push({event,...data});if(ST18.events.length>320)ST18.events.shift();}
function st18State(b){return b._st18||(b._st18={age:0,cues:{},said:new Set(),queue:[],radio:null,shield:null,phase:null});}
function st18Cue(b,key,gap=.25,gain=1){const A=st18State(b),last=A.cues[key]??-999;
 if(A.age-last<gap)return;A.cues[key]=A.age;Snd.play(key,gain);
 ST18.audio.push({key,t:A.age});if(ST18.audio.length>400)ST18.audio.shift();}
stageLoadBegin=function(n,keys){if(n===4)Snd.prepare?.(['geyserLightning','element_lightning_hit','chargeDash',
 'enemyLightningChaingun','bossCannon','missileLaunch','bombDrop','bossShieldStatic','gd_tankEngineLoop']);
 return ST18.base.load.call(this,n,n===4?[...(keys||[]),...st18Keys()]:keys);};
beginStage=function(){if(ST18.lastBoss)sa14Stop(ST18.lastBoss);ST18.lastBoss=null;SC12.invalidate();
 return ST18.base.begin.apply(this,arguments);};
function st18Speaker(){const active=seatList().map(s=>withSeat(s,()=>_pilotKey()));
 return !active.includes('decker')?'decker':!active.includes('cole')?'cole':'axel';}
function st18Say(b,id,text,priority=false){const A=st18State(b);if(A.said.has(id))return;
 A.said.add(id);const q={id,text,who:st18Speaker(),t:0,duration:Math.max(5.2,text.length*.075)};
 if(priority){A.queue=[];A.radio=q;}else if(!A.radio)A.radio=q;else A.queue.push(q);
 st18Log('radio',{id,who:q.who,text});SC12.invalidate();Audio.SFX.blip?.();}
function st18RadioTick(b,dt){const A=st18State(b);if(!A.radio)return;
 A.radio.t+=dt;if(A.radio.t>=A.radio.duration){A.radio=A.queue.shift()||null;SC12.invalidate();}}
function st18Wrap(text,width,size){const rows=[];let line='';for(const word of text.split(' ')){
 const next=line?line+' '+word:word;if(line&&bmfMeasure('dialogue',next,size)>width){rows.push(line);line=word;}else line=next;
 }if(line)rows.push(line);return rows;}
function st18RadioDraw(){const b=boss,A=b?._st18,q=A?.radio;if(!sa14Storm(b)||!bossActive||b.dead||!q||!SC12.active()||!bmfReady('dialogue'))return;
 // Reuse the existing pilot well in the approved housing; no combat overlay,
 // input capture, story state or pause is involved in a radio transmission.
 if(SC12.mode!=='sides')return st18CompactRadio(q);
 const g=SC12.panels[0].getContext('2d'),r=SC12_ART.wells.pilot,source=XART.get(SC12_ART.key);
 if(!source)return;g.save();g.imageSmoothingEnabled=false;
 for(let row=0;row<seatList().length;row++){
  g.save();g.translate(0,row*1536);g.clearRect(...r);g.drawImage(source,...r,...r);
  g.beginPath();g.rect(r[0]+3,r[1]+3,r[2]-6,r[3]-6);g.clip();
  const key=commPortrait(q.who,'talk'),im=XART.rdy(key)?XART.get(key):null;
  if(im){const k=Math.min(58/im.width,58/im.height);g.drawImage(im,r[0]+9,r[1]+4,im.width*k,im.height*k);}
  bmfDrawOn(g,'dialogue',q.who.toUpperCase(),r[0]+80,r[1]+20,29,'left');
  bmfDrawOn(g,'dialogue','FURY COMMS',r[0]+80,r[1]+47,20,'left');
  const lines=st18Wrap(q.text,r[2]-20,24);for(let i=0;i<lines.length;i++)bmfDrawOn(g,'dialogue',lines[i],r[0]+10,r[1]+78+i*28,24,'left');
  g.restore();
 }g.restore();ST18.draws.radio++;
}
function st18CompactRadio(q){
 // Narrow displays have no portrait well. A short page occupies the score
 // compartment only; life, missile, dodge and lock controls remain visible.
 const g=SC12.compact.getContext('2d');g.save();g.imageSmoothingEnabled=false;
 for(let row=0;row<seatList().length;row++){
  const x=13,y=row*SC12_ART.compactHeight*2+10,w=372,h=132;
  g.clearRect(x,y,w,h);g.fillStyle='#031421';g.fillRect(x,y,w,h);
  bmfDrawOn(g,'dialogue',q.who.toUpperCase(),x+8,y+7,23,'left');
  const lines=st18Wrap(q.text,w-16,22),page=Math.min(Math.floor(q.t/3),Math.max(0,Math.ceil(lines.length/3)-1));
  for(let i=0;i<3;i++)if(lines[page*3+i])bmfDrawOn(g,'dialogue',lines[page*3+i],x+8,y+39+i*27,22,'left');
 }g.restore();ST18.draws.radio++;
}
debugRecFrame=function(){const r=ST18.base.rec.apply(this,arguments);st18RadioDraw();return r;};
SC12.refresh=function(){const r=ST18.base.refresh.apply(this,arguments);st18RadioDraw();return r;};
sa14Rev=function(b,progress,dt){const r=ST18.base.rev.apply(this,arguments);if(sa14Storm(b)){
 const v=window.BOF_CHIP_PASS?.sound(sa14State(b).engine,'gd_tankEngineLoop',{loop:true,gain:3.8});
 if(v)v.el.playbackRate=(.78+progress*1.15)*clamp(timeScale,.5,2);
 }return r;};
function st18Phase(b,dt){const A=st18State(b),P=b._p4Final,R=b._er26;
 if(P){
  const target={panic:710,ram:1180,away:1080,overhead:1080,rear:960}[P.phase]||480;
  P.roadSpeed=lerp(P.roadSpeed||480,target,Math.min(1,dt*4.5));
  if(A.phase!==P.phase){A.phase=P.phase;st18Log('phase',{phase:P.phase,t:P.t,y:b.y,scale:b._sa14.scale});
   if(P.phase==='panic'){st18Say(b,'overload',"HULL OVERLOAD! DODGE THE RAM. IT'S ABOUT TO FLEE NORTH!",true);st18Cue(b,'bossShieldStatic',0,1.6);}
   if(P.phase==='ram'){st18Cue(b,'chargeDash',0,1.3);st18Cue(b,'bossCannon',0,1.15);}
   if(P.phase==='overhead'){st18Cue(b,'chargeDash',0,1.2);st18Cue(b,'geyserLightning',0,1.1);}
   if(P.phase==='rear'){st18Say(b,'chase','CHASE ITS EXPOSED REAR CORE! HITS PROVOKE MORE LIGHTNING.',true);st18Cue(b,'element_lightning_hit',0,1.3);}
  }
  if(P.phase==='panic'){st18Cue(b,'geyserLightning',.48,1.1);st18Cue(b,'element_lightning_hit',.28,.85);}
  if(['away','overhead','rear'].includes(P.phase)){
   const v=window.BOF_CHIP_PASS?.sound(sa14State(b).engine,'gd_tankEngineLoop',{loop:true,gain:P.phase==='overhead'?3.5:2.7});
   if(v)v.el.playbackRate=clamp(timeScale,.5,2)*(P.phase==='overhead'?1.65:1.3);
  }
 }else if(R?.mode==='sa14-storm'&&b._sa14.glow>.1)st18Cue(b,'element_lightning_hit',.45,1.1);
 if(A.shield!==b._s4war.shield.active){const wasShield=A.shield;A.shield=b._s4war.shield.active;
  if(A.shield)st18Say(b,'generators','FOUR SPINNING GENERATORS. TAG WITH MULTI-RETINA, THEN FIRE MISSILES.');
  else if(wasShield===true&&!P)st18Say(b,'weakspots','SHIELD DOWN! THE CENTRE CORE AND WEAPON PODS ARE EXPOSED.',true);
 }
}
er26WarTick=function(b,dt){const r=ST18.base.war.apply(this,arguments);if(!sa14Storm(b)||b.enter||b.dead||b.hp<=0)return r;
 const A=st18State(b);ST18.lastBoss=b;A.age+=dt;st18RadioTick(b,dt);st18Phase(b,dt);return r;};
p4EmitBalls=function(b){const n=ST18.base.balls.apply(this,arguments);if(sa14Storm(b)&&n)st18Cue(b,'enemyLightningChaingun',.32,1.2);return n;};
stage4WarfareShot=function(b,p,a,speed,role){const q=ST18.base.shot.apply(this,arguments);
 if(sa14Storm(b)&&!q.dead){if(role==='lightning')st18Cue(b,'geyserLightning',.30,1.05);
  else if(role==='rocket')st18Cue(b,'missileLaunch',.18,1.05);
  else if(role==='lightningmg')st18Cue(b,'enemyLightningChaingun',.22,.85);
 }return q;};

// Same two authored aircraft and module HP. Flight and gun clocks are separate,
// so moving into a crossing pass never silently disables the wing's guns.
function st18Centre(b){const station=b._target17Station||{x:er26Station(b,0),y:b._er26.home};
 return{x:clamp(b._sa14.depth?station.x:b.x,camLeftX()+140,camRightX()-140),y:clamp(b._sa14.depth?station.y:b.y,PLAY.y+125,PLAY.y+210)};}
function st18Orbit(b,d,C){const o=st18Centre(b),a=C.age*.72+(d.side>0?Math.PI:0);
 return{x:o.x+Math.cos(a)*Math.min(viewW()*.31,205),y:o.y+Math.sin(a)*88};}
function st18Flight(b,d,C,dt){C.moveT+=dt;const old={x:d.x,y:d.y},o=st18Orbit(b,d,C);
 if(C.move==='entry'){
  const wait=.85+(d.side>0?.22:0),u=clamp((C.moveT-wait)/1.55,0,1),ease=p4Ease(u);
  d.x=lerp(C.from.x,o.x,ease);d.y=lerp(VH+190,o.y,ease);d._sg17Scale=lerp(2.25,1,ease);
  d._noHit=true;d.materialize=0;d.ang=-Math.PI/2;
  if(C.moveT<wait){const x=clamp(C.from.x,camLeftX()+55,camRightX()-55);b._er26.warnings.push({x,y:VH-12,angle:-Math.PI/2,width:78,progress:C.moveT/wait,helper:d});}
  if(u>=1){C.move='orbit';C.moveT=0;d._noHit=false;d.materialize=1;C.nextRaid=[10,9,8,7][p4Rank()];st18Log('helper-on-plane',{side:d.side,age:C.age});}
 }else if(C.move==='orbit'){
  d.x+=clamp(o.x-d.x,-230*dt,230*dt);d.y+=clamp(o.y-d.y,-180*dt,180*dt);C.nextRaid-=dt;
  if(C.nextRaid<=0){C.move='scatter';C.moveT=0;C.from={x:d.x,y:d.y};C.raid++;C.bombs=0;
   C.out={x:camLeftX()+viewW()*(d.side<0?.08:.92),y:PLAY.y+100+(C.raid%2)*40};
   st18Log('helper-scatter',{side:d.side,raid:C.raid});}
 }else if(C.move==='scatter'){
  const u=p4Ease(C.moveT/.9);d.x=lerp(C.from.x,C.out.x,u);d.y=lerp(C.from.y,C.out.y,u);
  if(C.moveT>=.9){C.move='cross';C.moveT=0;C.from={x:d.x,y:d.y};
   C.to={x:camLeftX()+viewW()*(d.side<0?.88:.12),y:VH-(d.side<0?180:115)};
   st18Log('helper-cross',{side:d.side,raid:C.raid,from:{...C.from},to:{...C.to}});}
 }else if(C.move==='cross'){
  const u=clamp(C.moveT/2.2,0,1);d.x=lerp(C.from.x,C.to.x,u);d.y=lerp(C.from.y,C.to.y,u)-Math.sin(u*Math.PI)*45;
  if(C.bombs<2&&C.moveT>=.40+C.bombs*.75){st18Bomb(b,d,C.bombs);C.bombs++;}
  if(u>=1){C.move='return';C.moveT=0;C.from={x:d.x,y:d.y};}
 }else{
  const u=p4Ease(C.moveT/1.3);d.x=lerp(C.from.x,o.x,u);d.y=lerp(C.from.y,o.y,u);
  if(u>=1){C.move='orbit';C.moveT=0;C.nextRaid=[12,10,8.5,7][p4Rank()];st18Log('helper-orbit',{side:d.side,raid:C.raid});}
 }
 if(C.move!=='entry'){
  d._sg17Scale=1;d._noHit=false;d.materialize=1;
  const moved=Math.hypot(d.x-old.x,d.y-old.y),heading=moved>.15?Math.atan2(d.y-old.y,d.x-old.x):Math.PI/2;
  // Rigid authored aircraft orientation; no skewing or per-frame fitting.
  const angle=C.phase==='tell'||C.phase==='fire'?C.angle:heading;
  d.ang+=stage4AngleDelta(d.ang,angle)*Math.min(1,dt*9);
 }
}
sg17Wing=function(b,d,dt){const rank=p4Rank(),S=b._s4war;
 const C=d._sg17||(d._sg17={age:0,phase:'recover',t:0,shot:0,cycle:0,delay:d.side>0?.32:0,
  move:'entry',moveT:0,raid:0,from:{x:clamp(er26Station(b,0)+d.side*viewW()*.23,camLeftX()+70,camRightX()-70),y:VH+190}});
 // Existing live actors can acquire this owner without healing or respawning.
 if(!C.move){C.move='orbit';C.moveT=0;C.raid=0;C.nextRaid=7;C.bombs=0;}
 C.age+=dt;d._mrOwner=b;d.size=116;d.spawnT+=dt;
 d.flash=Math.max(0,d.flash-dt);d.deflectFlash=Math.max(0,(d.deflectFlash||0)-dt);d.deflectSfx=Math.max(0,(d.deflectSfx||0)-dt);
 const g=mr27HelperState(d);g.flash=Math.max(0,g.flash-dt);
 if(!C.announced){C.announced=true;st18Say(b,'helpers-'+S.coreGeneration,'LIGHTNING HELPERS, SOUTH! WATCH THEIR CROSSING RUNS AND BOMB RETINAS.',true);
  st18Cue(b,'bossShieldTeleport',.45,1.2);st18Log('helper-entry',{side:d.side,from:{...C.from}});}
 st18Flight(b,d,C,dt);if(C.move==='entry'){d.state='overheat';return;}
 if(b.dead||g.dead){C.phase='recover';C.t=0;d.state='overheat';return;}
 C.t+=dt;const warm=[1.05,.92,.82,.72][rank],rest=[1.35,1.05,.80,.62][rank];
 if(C.phase==='recover'){
  d.state='overheat';d.vulnerable=true;
  if(C.t>=rest+C.delay){const p=targetShip(d.x,d.y);C.aim={x:p.x,y:p.y};C.angle=Math.atan2(p.y-d.y,p.x-d.x);C.phase='tell';C.t=0;C.shot=0;C.round=0;C.cycle++;C.missile=C.cycle%2===0;st18Cue(b,'bossShieldStatic',.35,1);}
 }else if(C.phase==='tell'){
  d.state='windup';d.vulnerable=true;combatWarningTick(d,'storm-jet-'+C.cycle,C.t,warm);
  const p=stage4CoreTurretTip(d,1);for(const off of C.missile?[-.09,.09]:[0])b._er26.warnings.push({...p,angle:C.angle+off,width:C.missile?24:20,progress:C.t/warm,helper:d});
  if(C.t>=warm){C.phase='fire';C.t=0;}
 }else{
  d.state='fire';C.shot-=dt;
  if(C.shot<=0&&C.round<(C.missile?[2,2,3,4][rank]:[6,8,10,12][rank])){
   const side=C.round++%2?1:-1,p=stage4CoreTurretTip(d,side),angle=C.angle+(C.missile?(C.round%2?.09:-.09):0);
   const q=stage4WarfareShot(b,p,angle,C.missile?2.8+rank*.2:3.7+rank*.3,C.missile?'rocket':'lightningmg',{szMul:.70});
   Object.assign(q,{_sa14CoreShot:true,_sg17JetShot:true,_weaponProof:!C.missile,_shootable:C.missile,homing:false,
    _er26Source:'core',_air17Element:'lightning',_air17Missile:!!C.missile});
   if(C.missile){q.kind='emissile';q.hp=rank>=2?3:2;q.w=10;q.h=24;q._s4Accel=1.1;q._s4Max=5.8;}
   sg17Protect(q); // Lightning cannot be intercepted, including this missile-shaped reel.
   S.coreShots++;S.coreBarrelShots[side]++;b._er26.helperShots++;SG17.shots++;stage4CoreTurretMuzzle(b,d,side);
   C.shot=C.missile?.23:[.18,.15,.12,.10][rank];
  }
  if(C.t>1.6){C.phase='recover';C.t=0;}
 }
};
mr27HelperDraw=function(b,d){if(!sa14Storm(b)||!d._sg17)return ST18.base.helper.apply(this,arguments);
 const scale=d._sg17Scale||1,g=mr27HelperState(d);
 if(d._noHit){d._bodShadow=true;drawUnitShadow(d.x+12,d.y+32,116*scale*.8,74*scale,.30,d);}
 a17Blit('stormJet',b.t*18,d.x,d.y,116*scale,Math.max(d.flash||0,g.flash||0,d.deflectFlash||0),d.ang-Math.PI/2);
};
function st18Bomb(b,d,pass){if(groundTargetingFx.filter(q=>q._st18Bomb&&!q.dead).length>=6)return null;
 const rank=p4Rank(),p=targetShip(d.x,d.y),x=clamp(p.x+d.side*(pass?50:20),camLeftX()+35,camRightX()-35),y=clamp(p.y+(pass?28:-28),PLAY.y+100,VH-35);
 const q=groundTargetingSpawn({kind:'missile',x,y,owner:b,track:false,lane:false,warn:[1.85,1.65,1.45,1.30][rank],
  active:.80,radius:30,size:90,shake:4,sound:'geyserLightning',onImpact:g=>{st18Cue(b,'element_lightning_hit',.1,1.15);st18Log('bomb-impact',{x:g.x,y:g.y,t:g.t});}});
 q._jetBomb={x:d.x,y:d.y};q._st18Bomb=true;q._late27=true;
 st18Cue(b,'bombDrop',.18,1.15);st18Log('lightning-bomb',{side:d.side,x,y,from:{...q._jetBomb},warn:q.warn});return q;
}
function st18Blit(name,frame,x,y,size){const bank=ST18_ART[name],a=bank.frames[clamp(Math.floor(frame),0,bank.frames.length-1)];
 if(!XART.rdy(a.key))return false;const k=size/bank.h;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),x-bank.pivot[0]*k,y-bank.pivot[1]*k,bank.w*k,bank.h*k);ctx.restore();ST18.draws[name]++;return true;}
groundTargetingDraw=function(){const own=groundTargetingFx.filter(q=>q._st18Bomb&&!q.dead),all=groundTargetingFx;
 try{groundTargetingFx=all.filter(q=>!q._st18Bomb);ST18.base.ground.apply(this,arguments);}finally{groundTargetingFx=all;}
 for(const q of own){if(q.delay>0)continue;if(!q.impact){const u=clamp(q.t/q.warn,0,1),t=u*u;
   groundTargetReticleDraw(q.x,q.y,q.size,u,.9);
   st18Blit('bomb',Math.floor(q.t*ST18_ART.bomb.fps)%16,lerp(q._jetBomb.x,q.x,t),lerp(q._jetBomb.y,q.y,t)-Math.sin(u*Math.PI)*35,44);
  }else st18Blit('impact',(q.t-q.warn)/q.active*16,q.x,q.y,124);
 }
};
sa14Draw=function(b){const r=ST18.base.draw.apply(this,arguments);if(!sa14Storm(b)||b.dead||!b._p4Final)return r;
 const A=b._sa14,P=b._p4Final;if(P.phase==='panic'||P.phase==='ram'){
  const clock=b._er26.clock,glow=P.phase==='panic'?A.glow:.7;
  // Authored lightning banks crawl across the whole plate and wing roots.
  for(const side of [-1,1])for(const y of [-.23,.06,.28])sa14BlueArc(b.x+side*b.w*.25,b.y+b.h*y,
   clock*1.8+side*.7,50+glow*58,clock+side+y,.55+glow*.35);
  ST18.draws.glow++;
 }return r;};
const ST18_UPDATE=updatePlay;
updatePlay=function(dt){const r=ST18_UPDATE.apply(this,arguments),b=ST18.lastBoss;
 if(b&&(!bossActive||boss!==b||b.dead||b.hp<=0)){sa14Stop(b);if(b._st18)b._st18.radio=null;ST18.lastBoss=null;SC12.invalidate();}
 return r;};
window.BOF_STORM_ASSAULT={state:ST18,speaker:st18Speaker,bomb:st18Bomb,radio:st18Say};
