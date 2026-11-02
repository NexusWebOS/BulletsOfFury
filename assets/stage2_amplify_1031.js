"use strict";
/* Stage2 volcanic roster: whole authored hulls, native damage/death/shields,
   measured emitters, committed beams and source-frame flight. */
const V31={base:{spawn:spawnEnemy,volc:volcTick,draw:drawEnemy,entry:enemyEntrySweep,
 turret:modularGroundTurretTick,projectile:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,
 effects:updateEffects,flashes:drawNavalFlashes,ground:groundTargetingDraw,load:stageLoadBegin,element:enemyOrdnanceElement,play:updatePlay,
 aiEnd:ai27End,route:eb11OwnsRoute,begin:beginStage,kill:killEnemy},fx:[],events:[],serial:0,
 models:{ash:'ash',skim:'skimmer',cinderwasp:'wasp',lance:'thunder',firejet1002:'thunder',
 ac10firejet:'interceptor',basaltbomber:'basalt',cruc:'crucible',miner:'minelayer',
 carrier:'carrier',lavasnake:'snake',crawl:'snake',lavamaw:'maw',pod:'pod',disc:'disc'},
 config:{ash:[58,58],skimmer:[88,80],wasp:[66,72],thunder:[112,110],interceptor:[122,118],
 basalt:[94,94],crucible:[108,98],minelayer:[86,86],carrier:[190,156],snake:[148,156],maw:[92,86],pod:[86,86],disc:[104,104],elite:[88,88]}};
for(const a of Object.values(V31_ART.banks))XART._src[a.key]=a.path;
function v31Rank(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function v31Alive(e){return !!e&&!e.dead&&e._dyingT==null&&e.hp>0;}
function v31Log(e,event,extra={}){V31.events.push({id:e?._v31?.id,type:e?.type,event,t:efxClock,...extra});if(V31.events.length>900)V31.events.shift();}
function v31Model(e){return e?._v31&&V31_ART.models[e._v31.model];}
function v31Dir(a,n=32){return((Math.round(s1aAngle(a-Math.PI/2)*n/TAU)%n)+n)%n;}
function v31Blit(B,f,a,x,y,size,tint=null,alpha=1){
 if(!B||!XART.rdy(B.key))return false;const c=B.cell,im=tint?xartTint(B.key,tint,1):XART.get(B.key);
 const d=v31Dir(a,B.dirs),cols=B.cols||B.dirs;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,(d%cols)*c,(clamp(f|0,0,B.frames-1)*(B.dirRows||1)+Math.floor(d/cols))*c,c,c,x-size/2,y-size/2,size,size);ctx.restore();return true;
}
function v31Size(e){const M=v31Model(e);return Math.max(e.w,e.h)*(M.banks.heading?.cell||M.banks.sequence?.cell||M.banks.spin.cell)/M.span;}
function v31Point(e,p,angle=null){const A=e._v31,M=v31Model(e),cell=M.banks.heading?.cell||M.banks.sequence?.cell||192,
 a=angle??A.head,d=TAU*v31Dir(a,M.banks.heading?.dirs||8)/(M.banks.heading?.dirs||8),c=Math.cos(d),s=Math.sin(d),k=v31Size(e)/cell,x=(p[0]-cell/2)*k,y=(p[1]-cell/2)*k;
 return{x:e.x+x*c-y*s,y:e.y+x*s+y*c,angle:Math.PI/2+d};}
function v31Gun(e,i=0){return v31Point(e,v31Model(e).guns[i%v31Model(e).guns.length]);}
function v31Flash(e,p,size=32){V31.fx.push({owner:e,p:{...p},t:0,life:.15,size});if(V31.fx.length>120)V31.fx.shift();}
function v31Shot(e,p,kind='slug',speed=4.2,silent=false){
 const missile=kind==='thunder_missile'||kind==='fire_missile',orb=kind==='orb'||kind==='mine',
 b=eShootT(p.x,p.y,p.angle,speed,missile?'s1jungleMissile':orb?'s2slag':'s2needle',
 {owner:e,noMuzzle:true,silent:true,w:orb?18:missile?10:7,h:orb?18:missile?22:16});
 if(!b||b.dead||b._ai27Held)return b;
 b._v31Owner=e;b._v31Kind=kind;b._noArsenal=true;b._weaponProof=!missile&&!orb;b._shootable=missile||orb;
 b._el=missile&&kind==='thunder_missile'?'lightning':'fire';
 if(missile)b._isPhysicalMissile=true;if(orb){b.hp=kind==='mine'?2:3;b._energyOrdnance=true;}
 e._v31.lastShot=e._v31.age;if(!p.noFlash)v31Flash(e,p,orb?42:34);
 if(!silent){if(missile)enemyShotSfx('s1jungleMissile');else if(orb)Audio.SFX.magmaOrb?.();else Audio.SFX.enemyMachineGunHeavy?.();}
 v31Log(e,'shot',{kind,x:p.x,y:p.y,a:p.angle});return b;
}
function v31Pair(e,kind,speed,aim=null){let any=false;for(let i=0;i<v31Model(e).guns.length;i++){
 const p=v31Gun(e,i);if(aim!=null)p.angle=aim;const b=v31Shot(e,p,kind,speed,i>0);any=any||!!b&&!b.dead;
 }return any;}
enemyOrdnanceCanIntercept=function(b){return b?._v31Kind?['orb','mine','thunder_missile','fire_missile'].includes(b._v31Kind):V31.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(b){if(b?._v31Kind)return['orb','mine'].includes(b._v31Kind)?'fire':null;return V31.base.element.apply(this,arguments);};
function v31GroundLegal(e,x,y){const size=Math.max(e.w||50,e._drawW||0)*.54,sy=levelSrcY()+y;
 return[-1,0,1].every(i=>[-1,0,1].every(j=>tankDrivable(x+i*size,sy+j*size,false)));}
function v31PlaceTurret(e,prefer){const born=e.y;for(let row=0;row<=768;row+=16){e.y=born-row;for(let d=0;d<worldWidth();d+=8)for(const side of d?[-1,1]:[1]){
 const x=clamp(prefer+d*side,40,worldWidth()-40);if(v31GroundLegal(e,x,e.y)){e.x=x;e._fixedX=x;e._lvlY=levelSrcY()+e.y;return true;}}}
 e.y=born;
 return false;}
function v31Init(e,model,options={}){
 const cfg=V31.config[model],oldHp=e.hp;e.w=cfg[0];e.h=cfg[1];e._drawW=e.w;e._drawH=e.h;
 const A=e._v31={id:++V31.serial,model,age:0,head:Math.PI/2,phase:'entry',phaseT:0,cd:.85,round:0,cycles:0,
 homeX:e.x,homeY:Math.max(PLAY.y+95,e.y),side:e.x<worldWidth()/2?1:-1,spin:0,pose:0,beams:[],fast:model==='minelayer'?Math.random()<.8:false,role:options._v31Role||'guns'};
 // The native spawn already applied difficulty/thermal HP once. Preserve it.
 e.hp=oldHp;e.maxhp=e._maxhp=e.maxhp||e._maxhp||oldHp;e.shoots=false;e.armed=false;e.fk=null;e.fireCd=999;
 e.pattern='volc';e._volc=e._volc||e.type;e._noSep=true;e.spin=0;e._frFlight=false;
 for(const k of ['_dr','_cn','_ai','_af10Jet','_ac10Ram','_fireJet1002','_jetManeuver','_entry','_s2Act','_biomePlate'])delete e[k];
 if(model==='crucible'){delete e._esh;enemyShieldEquip(e,'bubble_fire',Math.max(8,Math.ceil(oldHp*.7)),{once:true,drawScale:1.35});}
 else if(['ash','disc','skimmer','thunder','interceptor','wasp','minelayer','carrier','snake','elite'].includes(model))delete e._esh;
 if(model==='carrier'&&!options.inPlace){A.side=e.x<worldWidth()/2?1:-1;e.x=A.side>0?camLeftX()-120:camRightX()+120;e.y=PLAY.y+145;A.head=A.side>0?0:Math.PI;A.homeX=(camLeftX()+camRightX())/2;}
 if(model==='snake'){e._noBodyContact=true;A.side=e.x<worldWidth()/2?1:-1;e.x=A.side>0?camLeftX()+35:camRightX()-35;e.y=VH*.72;A.phase='erupt';A.homeY=e.y;A.cross=0;}
 v31Log(e,'spawn',{model,hp:oldHp});return A;
}
spawnEnemy=function(type,x,y,options={}){
 if(['eye','magmaeye','magmaorb'].includes(type)){v31Log(null,'retired-spawn-rejected',{type});return null;}
 const elite=type.startsWith('v31elite_'),snake=type==='lavasnake',e=V31.base.spawn.call(this,elite?'cruc':snake?'crawl':type,x,y,options);
 if(!e||run.stage!==2)return e;
 if(e._modTurret){e._v31Turret=true;e._drawW=e._drawH=e.w*1.27;if(!v31PlaceTurret(e,e.x+(e._modTurret.weapon==='laser'?14:0))){e.dead=true;e.dropOk=false;return null;}return e;}
 const model=elite?'elite':V31.models[type]||V31.models[e.type];if(!model)return e;
 if(elite)e.type=type;if(type==='crawl'||snake)e.type='lavasnake';v31Init(e,model,options);return e;
};
enemyEntrySweep=function(e){if(e?._v31)return;return V31.base.entry.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._v31||V31.base.route.apply(this,arguments);};
ai27End=function(e,previous){if(e?._v31&&e._ai27)e._ai27.dx=0;return V31.base.aiEnd.apply(this,arguments);};
function v31Mode(e,phase){const A=e._v31;A.phase=phase;A.phaseT=0;A.round=0;A.cd=0;v31Log(e,phase);}
function v31Fly(e,tx,ty,speed,turn,dt){const A=e._v31,a=Math.atan2(ty-e.y,tx-e.x);A.head+=clamp(s1aAngle(a-A.head),-turn*dt,turn*dt);
 const x=e.x,y=e.y;e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;e.vx=(e.x-x)/Math.max(dt,.001)/60;e.vy=(e.y-y)/Math.max(dt,.001)/60;}
function v31Tell(e,duration=.9){const A=e._v31;if(A.phase!=='tell'){v31Mode(e,'tell');A.dur=duration;A.target={...targetShip(e.x,e.y)};Audio.SFX.bossWeaponCharge?.();}
 combatWarningTick(e,'v31',A.phaseT,A.dur);return A.phaseT>=A.dur;}
function v31Beam(e,p,life=.65,width=12,length=900){const A=e._v31;A.beams.push({p:{...p},t:0,life,width,length});v31Flash(e,p,46);v31Log(e,'beam',{x:p.x,y:p.y,a:p.angle});}
function v31BeamTick(e,dt){const A=e._v31;for(const b of A.beams){b.t+=dt;if(b.t>b.life)continue;
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out)return;const dx=player.x-b.p.x,dy=player.y-b.p.y,c=Math.cos(b.p.angle),s=Math.sin(b.p.angle),along=dx*c+dy*s,across=Math.abs(-dx*s+dy*c);
  if(along>0&&along<b.length&&across<(b.flame?(10+along*.16):b.width/2)+(player._hx||8))playerHit(b.flame?'Volcanic flamethrower':'Fire-infused laser');});}
 A.beams=A.beams.filter(b=>b.t<b.life);}
function v31Drop(e,p,tx,ty,warn=1.5){
 const q=groundTargetingSpawn({kind:'missile',x:tx,y:ty,owner:e,track:false,lane:false,warn,radius:23,size:58,active:.38,
 sound:'magmaOrb',shake:3,onImpact:g=>explode(g.x,g.y,55,'red','fireball')});
 const b=v31Shot(e,{...p,noFlash:true},'orb',0,true);if(b){b.vx=b.vy=b.spd=0;b.homing=false;b.life=warn+.3;b._v31Arc=q;}
 q._v31Drop={p:{...p},bullet:b};if(efxClock-(e._v31.lastDropFlash??-9)>.08){v31Flash(e,p,38);e._v31.lastDropFlash=efxClock;}
 Audio.SFX.bombDrop?.();v31Log(e,'volcano-orb',{x:p.x,y:p.y,tx,ty});return q;}
function v31Aircraft(e,dt){const A=e._v31,K=A.model,r=v31Rank(),T=targetShip(e.x,e.y),left=camLeftX(),right=camRightX();
 if(K==='ash'){
  if(A.phase==='entry'){v31Fly(e,clamp(T.x+A.side*145,left+80,right-80),T.y-180,150,2.2,dt);if(e.y>PLAY.y+80)v31Mode(e,'spiral');}
  else if(A.phase==='spiral'){const radius=Math.max(65,200-A.phaseT*24),a=A.phaseT*2.1+A.id*.9;v31Fly(e,clamp(T.x+Math.cos(a)*radius,left+30,right-30),clamp(T.y-65+Math.sin(a)*radius*.65,PLAY.y+70,VH-55),185,3.5,dt);A.spin+=dt*1.1;if(A.phaseT>5.6){v31Mode(e,'kamikaze');A.commit={x:T.x,y:T.y+35};Audio.SFX.jetDash?.();}}
  else if(A.phase==='kamikaze'){v31Fly(e,A.commit.x,A.commit.y,330,3.1,dt);if(A.phaseT>1.5)v31Mode(e,'exit');}
  else v31Fly(e,e.x+A.side*250,VH+180,260,2.2,dt);
  A.cd-=dt;if(A.cd<=0&&A.phase!=='exit'&&e.y>PLAY.y+30&&Math.hypot(T.x-e.x,T.y-e.y)>80){v31Pair(e,'slug',4.5,aimPlayer(e.x,e.y));A.cd=turretInterval15(.42,[.42,.30,.22][r]);}
 }else if(K==='skimmer'||K==='wasp'||K==='basalt'||K==='elite'){
  const duration=K==='elite'?13:K==='wasp'?10:9;
  if(A.phase==='entry'&&e.y>PLAY.y+70)v31Mode(e,'curve');
  if(A.age>duration&&A.phase!=='exit')v31Mode(e,'exit');
  const a=A.phaseT*(K==='wasp'?1.7:.9)+A.id*.9,tx=A.phase==='entry'?clamp(A.homeX,left+65,right-65):A.phase==='exit'?(A.side>0?right+180:left-180):clamp((left+right)/2+Math.sin(a)*(right-left)*.31,left+60,right-60),
   ty=A.phase==='exit'?VH+130:A.phase==='entry'?PLAY.y+140:PLAY.y+145+Math.cos(a*.8)*75;
  v31Fly(e,tx,ty,K==='wasp'?158:K==='basalt'?115:140,2.4,dt);
  A.cd-=dt;if(A.cd<=0&&A.phase!=='exit'&&e.y>PLAY.y+45){
   if(K==='basalt'){for(const side of [-1,1]){const p=v31Gun(e,side<0?0:1);v31Drop(e,p,clamp(e.x+side*64,left+35,right-35),clamp(T.y-45+side*45,PLAY.y+160,VH-40),1.65);}A.cd=turretInterval15(2.1,[2.1,1.6,1.2][r]);}
   else if(K==='elite'&&['wall','flame'].includes(A.role)){
    if(!A.heavy){A.heavy={t:0,p:v31Gun(e)};Audio.SFX.bossWeaponCharge?.();}A.cd=.05;
   }else{const kind=K==='elite'&&A.role==='balls'?'orb':'slug',speed=4.4;
    v31Pair(e,kind,speed,aimPlayer(e.x,e.y));A.round++;A.cd=K==='elite'&&A.role==='flame'?.13:A.round%5?[.17,.13,.10][r]:[1.1,.8,.6][r];}
  }
  if(A.heavy){const H=A.heavy;H.t+=dt;combatWarningTick(e,'v31-heavy',H.t,.9);if(H.t>=.9){
   if(A.role==='flame'){for(let i=0;i<2;i++){const p=v31Gun(e,i);v31Beam(e,p,.8,30,160);A.beams.at(-1).flame=true;}(Audio.SFX.flameThrowerStart||Audio.SFX.enemyFlameBolt)?.();}
   else{const p=v31Gun(e),b=v31Shot(e,{...p,angle:Math.PI/2},'slug',2.3);if(b){b._v31Kind='wall';b.w=138;b.h=22;b._weaponProof=true;b._shootable=false;}Audio.SFX.enemyFlameBolt?.();}
   A.heavy=null;A.cd=2.2;}}
 }else if(K==='thunder'||K==='interceptor'||K==='crucible'){
  if(A.phase==='entry'){v31Fly(e,clamp(A.homeX,left+85,right-85),PLAY.y+145,100,2,dt);if(e.y>PLAY.y+110){v31Mode(e,'wait');A.cd=.6;}}
  else if(A.phase==='exit')v31Fly(e,A.side>0?right+170:left-170,PLAY.y-160,170,2,dt);
  else{
   if(A.phase==='wait'){const tx=clamp(A.homeX+Math.sin(A.age*.8)*100,left+85,right-85);v31Fly(e,tx,PLAY.y+145+Math.sin(A.age*.5)*55,55,1.6,dt);A.cd-=dt;if(A.cd<=0){v31Mode(e,'tell');A.dur=[.85,.72,.62][r];A.target={x:T.x,y:T.y};A.head=aimPlayer(e.x,e.y);}}
   else if(A.phase==='tell'){combatWarningTick(e,'v31',A.phaseT,A.dur);if(A.phaseT>=A.dur){v31Mode(e,'burst');A.cd=0;}}
   else if(A.phase==='burst'){A.cd-=dt;if(A.cd<=0){const kind=K==='thunder'?'thunder_slug':K==='crucible'?'orb':'slug';v31Pair(e,kind,K==='crucible'?2.8:5.1);A.round++;A.cd=turretInterval15(.18,[.18,.14,.10][r]);if(A.round>=(K==='interceptor'?7:K==='thunder'?5:3)){
     if(K==='thunder'&&A.cycles%2===0){enemyLockOn(e,.75,{fire:()=>{if(v31Alive(e))v31Pair(e,'thunder_missile',2.8);}});}
     A.cycles++;v31Mode(e,'wait');A.cd=turretInterval15(1.4,[1.4,1.05,.75][r]);}}
   }
  }
  if(A.age>22&&A.phase!=='exit')v31Mode(e,'exit');
 }
 if(A.phase==='exit'&&(e.x<left-130||e.x>right+130||e.y>VH+110||e.y<PLAY.y-130))e.dead=true;
}
function v31Minelayer(e,dt){const A=e._v31,r=v31Rank(),L=camLeftX(),R=camRightX();
 if(A.phase==='entry'){v31Fly(e,clamp(A.homeX,L+70,R-70),PLAY.y+185,130,2.5,dt);if(e.y>PLAY.y+125){v31Mode(e,'lay');A.cd=0;}}
 else if(A.phase==='lay'){
  v31Fly(e,clamp(A.homeX+A.side*140,L+60,R-60),PLAY.y+235,100,2.5,dt);A.cd-=dt;
  if(A.cd<=0){const p=v31Gun(e);p.angle=Math.PI/2;const b=v31Shot(e,p,'mine',.22);if(b){b.life=9;b._v31Mine=true;b._wardenAnchor={x:p.x,y:p.y+8,life:9};b._wardenAnchored=true;}A.cd=.48;A.round++;}
  if(A.phaseT>(A.fast?2:5)){v31Mode(e,'boost');Audio.SFX.jetDash?.();}
 }else{v31Fly(e,A.side>0?R+180:L-180,PLAY.y-160,330+50*r,3,dt);if(e.x<L-100||e.x>R+100||e.y<PLAY.y-100)e.dead=true;}
}
function v31Carrier(e,dt){const A=e._v31,L=camLeftX(),R=camRightX();
 if(A.phase==='entry'){v31Fly(e,A.homeX,PLAY.y+145,115,1.4,dt);if(Math.hypot(e.x-A.homeX,e.y-(PLAY.y+145))<55){v31Mode(e,'open');A.head=Math.PI/2;}}
 else if(A.phase==='open'){A.door=Math.min(3,Math.floor(A.phaseT/.24));if(A.phaseT>1.05){v31Mode(e,'deploy');A.cd=0;}}
 else if(A.phase==='deploy'){A.door=3;A.cd-=dt;if(A.cd<=0&&A.round<4){const roles=['flame','balls','guns','wall'],role=roles[A.round],p=v31Gun(e),jet=spawnEnemy('v31elite_'+role,p.x,p.y+8,{inPlace:true,_v31Role:role});
   if(jet){jet._v31.homeX=clamp(p.x+(A.round-1.5)*75,L+60,R-60);jet._v31Carrier=e;v31Log(e,'deploy-jet',{role,child:jet._v31.id});Audio.SFX.jetDash?.();}A.round++;A.cd=1.0;
  }if(A.phaseT>4.3)v31Mode(e,'close');}
 else if(A.phase==='close'){A.door=Math.max(0,3-Math.floor(A.phaseT/.24));if(A.phaseT>1)v31Mode(e,'exit');}
 else{v31Fly(e,A.side>0?R+220:L-220,PLAY.y-160,160,1.6,dt);if(e.x<L-150||e.x>R+150||e.y<PLAY.y-150)e.dead=true;}
}
function v31Snake(e,dt){const A=e._v31,L=camLeftX()+35,R=camRightX()-35,r=v31Rank();
 if(A.phase==='erupt'){
  A.pose=Math.min(3,Math.floor(A.phaseT*5));if(!A.eruption){A.eruption=true;groundTargetingSpawn({kind:'lava',x:e.x,y:e.y,owner:e,track:false,lane:false,warn:.9,radius:36,size:92,active:.5,sound:'expBig',onImpact:g=>{explode(g.x,g.y,98,'red','fireball');}});}
  if(A.phaseT>1.2){A.start={x:e.x,y:e.y};v31Mode(e,'cross');Audio.SFX.jetDash?.();}
 }else if(A.phase==='cross'){
  const u=clamp(A.phaseT/1.8,0,1),x=A.side>0?L:R,xx=A.side>0?R:L;
  e.x=lerp(x,xx,u);e.y=A.homeY-Math.sin(u*Math.PI)*200+Math.sin(u*TAU)*23;A.pose=(A.side>0?0:4)+Math.min(3,Math.floor(u*4));
  if(u>=1){A.side*=-1;A.cross++;A.eruption=false;v31Mode(e,A.cross>=3?'bite-tell':'erupt');}
 }else if(A.phase==='bite-tell'){
  if(!A.target){const T=targetShip(e.x,e.y);A.target={x:T.x,y:T.y};A.from={x:e.x,y:e.y};Audio.SFX.bossWeaponCharge?.();}
  A.pose=8+Math.min(3,Math.floor(A.phaseT*4));combatWarningTick(e,'v31',A.phaseT,.95);
  if(A.phaseT>.95){v31Mode(e,'bite');Audio.SFX.jetDash?.();}
 }else if(A.phase==='bite'){
  const u=clamp(A.phaseT/.48,0,1);e.x=lerp(A.from.x,A.target.x,u);e.y=lerp(A.from.y,A.target.y-38,u);A.pose=12;
  for(const s of seatList())withSeat(s,()=>{if(!player.dead&&Math.hypot(player.x-e.x,player.y-(e.y+40))<27)playerHit('Mechanical serpent bite');});
  if(u>=1){A.from={x:e.x,y:e.y};v31Mode(e,'recover');}
 }else{
  const u=clamp(A.phaseT/1.2,0,1);e.x=lerp(A.from.x,A.side>0?L:R,u);e.y=lerp(A.from.y,A.homeY,u);A.pose=13+Math.min(2,Math.floor(u*3));
  if(u>=1){A.cross=0;A.target=null;A.eruption=false;v31Mode(e,A.age>29?'exit':'erupt');}
 }
 if(A.phase==='exit')e.dead=true;
}
function v31Volcano(e,dt){const A=e._v31,r=v31Rank(),T=targetShip(e.x,e.y);e.y+=emplaceStep(e,dt);A.cd-=dt;
 if(A.phase==='entry')v31Mode(e,'wait');
 if(A.phase==='wait'&&A.cd<=0&&e.y>PLAY.y+45&&e.y<VH-100){v31Mode(e,'tell');A.dur=[1.1,.85,.7][r];A.target={x:T.x,y:T.y};Audio.SFX.bossWeaponCharge?.();}
 if(A.phase==='tell'&&A.phaseT>=A.dur){
  const M=v31Model(e),p=v31Point(e,M.guns[0],Math.PI/2),n=A.model==='maw'?6:8,rad=A.model==='maw'?100:130;
  for(let k=0;k<n;k++){const a=k*TAU/n;v31Drop(e,p,clamp(A.target.x+Math.cos(a)*rad,camLeftX()+28,camRightX()-28),clamp(A.target.y+Math.sin(a)*rad*.5,PLAY.y+100,VH-30),[1.7,1.45,1.25][r]);}
  v31Mode(e,'erupt');Audio.SFX.expSmall?.();
 }
 if(A.phase==='erupt'&&A.phaseT>.65){v31Mode(e,'wait');A.cd=turretInterval15(2.3,[2.3,1.5,1.0][r]);}
 A.pose=A.phase==='tell'?4+Math.min(3,Math.floor(A.phaseT/A.dur*4)):A.phase==='erupt'?8+Math.min(7,Math.floor(A.phaseT/.65*8)):Math.floor(A.age*5)%4;
 if(e.y>VH+100)e.dead=true;
}
function v31Disc(e,dt){const A=e._v31,r=v31Rank();
 if(A.phase==='entry'){e.y+=80*dt;A.spin+=dt*.7;if(e.y>PLAY.y+155){v31Mode(e,'wait');A.cd=1.0;}}
 else if(A.phase==='wait'){A.spin+=dt*(.8+.2*r);A.cd-=dt;if(A.cd<=0){v31Mode(e,'tell');A.dur=[1.2,1.05,.95][r];A.spinFrame=Math.floor(A.spin*32)%32;A.lanes=V31_ART.models.disc.spikes[A.spinFrame].map(p=>v31Point(e,p,Math.PI/2));
   A.lanes.forEach((p,i)=>p.angle=V31_ART.models.disc.spikes[A.spinFrame][i][2]);Audio.SFX.bossWeaponCharge?.();}}
 else if(A.phase==='tell'){combatWarningTick(e,'v31',A.phaseT,A.dur);if(A.phaseT>=A.dur){for(const p of A.lanes)v31Beam(e,p,.66,10);Audio.SFX.enemyHeavyLaser?.();v31Mode(e,'fire');}}
 else if(A.phase==='fire'&&A.phaseT>.9){A.cycles++;v31Mode(e,'wait');A.cd=turretInterval15(2.2,[2.2,1.7,1.3][r]);}
 if(A.age>24&&!A.beams.length){e.y-=120*dt;if(e.y<PLAY.y-100)e.dead=true;}
}
volcTick=function(e,dt){if(!e?._v31)return V31.base.volc.apply(this,arguments);if(!v31Alive(e)||e._frozen||e._mercuryLock>0)return;
 const A=e._v31;if(e._stagger>0)return;A.age+=dt;A.phaseT+=dt;e.spin=0;v31BeamTick(e,dt);
 if(A.model==='minelayer')v31Minelayer(e,dt);else if(A.model==='carrier')v31Carrier(e,dt);else if(A.model==='snake')v31Snake(e,dt);else if(A.model==='maw'||A.model==='pod')v31Volcano(e,dt);else if(A.model==='disc')v31Disc(e,dt);else v31Aircraft(e,dt);
};
function v31TurretGun(e,i=0){const T=e._modTurret,a=Math.PI/2+v31Dir(T.angle,64)*TAU/64,k=e.w*.96/256,c=Math.cos(a-Math.PI/2),s=Math.sin(a-Math.PI/2),x=(T.weapon==='laser'?0:i?54:-54)*k,y=(T.weapon==='missile'?68:90)*k;
 return{x:e.x+x*c-y*s,y:e.y+x*s+y*c,angle:a};}
modularGroundTurretTick=function(e,dt){if(!e?._v31Turret)return V31.base.turret.apply(this,arguments);
 const T=e._modTurret,A=e._v31Ground||(e._v31Ground={phase:'wait',t:0,cd:.7,round:0,beams:[]}),r=v31Rank(),target=targetShip(e.x,e.y);
 if(!v31Alive(e)||e.y<30||e.y>VH-60||bossActive||subBossActive)return;
 A.t+=dt;A.cd-=dt;
 if(A.phase==='wait'){const want=Math.atan2(target.y-e.y,target.x-e.x);T.angle+=clamp(s1aAngle(want-T.angle),-dt*turretSpeed15(2.3),dt*turretSpeed15(2.3));if(A.cd<=0){A.phase='tell';A.t=0;A.target={x:target.x,y:target.y};
  if(T.weapon==='missile'){enemyLockOn(e,.8,{fire:()=>{if(v31Alive(e)){A.phase='fire';A.t=0;A.cd=0;A.round=0;}}});}else Audio.SFX.bossWeaponCharge?.();}}
 else if(A.phase==='tell'&&T.weapon!=='missile'){combatWarningTick(e,'v31-turret',A.t,.8);if(A.t>=.8){A.phase='fire';A.t=0;A.cd=0;A.round=0;}}
 else if(A.phase==='fire'&&A.cd<=0){
  for(let i=0;i<(T.weapon==='laser'?1:2);i++){
   const p=v31TurretGun(e,i),b=eShootT(p.x,p.y,p.angle,T.weapon==='missile'?3.0:T.weapon==='mg'?4.8:6,T.weapon==='missile'?'s1jungleMissile':'s2needle',{owner:e,noMuzzle:true,silent:true,w:7,h:T.weapon==='laser'?32:18});
   if(b&&!b.dead){b._v31Owner=e;b._v31Kind=T.weapon==='missile'?'fire_missile':T.weapon==='laser'?'laser':'slug';b._weaponProof=T.weapon!=='missile';b._shootable=T.weapon==='missile';b._noArsenal=true;v31Flash(e,p,34);v31Log(e,'turret-shot',{kind:b._v31Kind,x:p.x,y:p.y});}
  }
  (T.weapon==='missile'?Audio.SFX.enemyMissile:T.weapon==='laser'?Audio.SFX.enemyHeavyLaser:Audio.SFX.enemyMachineGunHeavy)?.();
  A.round++;A.cd=turretInterval15(T.weapon==='laser'?.22:T.weapon==='mg'?.12:.22,T.weapon==='laser'?[.22,.13,.065][r]:T.weapon==='mg'?.12:.22);
  // Hard/Furious rotate the laser between releases after its committed tell.
  if(T.weapon==='laser'&&r>0)T.angle+=.07*(r===2?1.2:1);
  if(A.round>=(T.weapon==='laser'?[2,5,9][r]:T.weapon==='missile'?2:6)){A.phase='wait';A.cd=turretInterval15(2.2,[2.2,1.45,.85][r]);A.t=0;}
 }
 T.mode=A.phase==='tell'?'tell':'wait';
};
function v31DrawBeams(e){for(const b of e._v31.beams){
 if(b.flame){v31Blit(V31_ART.banks.flamethrower,Math.floor(b.t*20)%4,b.p.angle,b.p.x+Math.cos(b.p.angle)*77,b.p.y+Math.sin(b.p.angle)*77,182);continue;}
 const size=b.width*4,step=size*.72;
 for(let d=step/2;d<b.length;d+=step){const x=b.p.x+Math.cos(b.p.angle)*d,y=b.p.y+Math.sin(b.p.angle)*d;if(x<camLeftX()-40||x>camRightX()+40||y<PLAY.y-40||y>VH+40)continue;
  v31Blit(V31_ART.banks.laser,Math.floor(b.t*24)%4,b.p.angle,x,y,size);}
 }}
function v31DrawHull(e){const A=e._v31,M=v31Model(e),size=v31Size(e);let B=M.banks.heading,f=0,a=A.head;
 if(A.model==='snake'||A.model==='maw'||A.model==='pod'){B=M.banks.sequence;f=A.pose;a=Math.PI/2;}
 else if(A.model==='disc'){B=M.banks.spin;f=['tell','fire'].includes(A.phase)?A.spinFrame:Math.floor(A.spin*32)%32;a=Math.PI/2;}
 else if(A.model==='carrier'&&['open','deploy','close'].includes(A.phase)){B=M.banks.charge;f=A.door||0;a=Math.PI/2;}
 else if(A.model==='ash'&&A.phase==='spiral'){B=M.banks.roll;f=Math.floor(A.spin*B.frames)%B.frames;}
 else if(A.phase==='tell'){B=M.banks.charge||M.banks.attack;f=Math.min(B.frames-1,Math.floor(A.phaseT/(A.dur||1)*B.frames));}
 else if(A.age-(A.lastShot??-99)<.25){B=M.banks.attack;f=Math.floor((A.age-A.lastShot)/.25*B.frames)%B.frames;}
 if(e._dyingT!=null){B=M.banks.roll||M.banks.sequence||M.banks.spin;f=Math.floor(e._dyingT*12)%B.frames;a=A.head+(e.spin||0);}
 v31Blit(B,f,a,e.x+8,e.y+15,size,'#000000',.23);
 if(M.tails?.length&&e._dyingT==null)for(const p of M.tails){const t=v31Point(e,p);v31Blit(V31_ART.banks.thruster,Math.floor(A.age*24)%4,t.angle,t.x,t.y,30*(A.phase==='boost'?1.6:1));}
 v31Blit(B,f,a,e.x,e.y,size,e.flash>0?hitFlashColor(e):null);e._v31Rendered={key:B.key,frame:f,angle:a,size};
 if(A.phase==='tell'&&A.target&&A.model!=='maw'&&A.model!=='pod'&&A.model!=='disc'){
  const ps=A.model==='snake'?[{x:e.x,y:e.y}]:M.guns.map((_,i)=>v31Gun(e,i));for(const p of ps)combatWarningDraw(e,{...p,ex:A.target.x,ey:A.target.y,progress:A.phaseT/(A.dur||.95),width:A.model==='snake'?48:16,fieldOnly:true});}
 if(A.heavy){const p=v31Gun(e);combatWarningDraw(e,{...p,ex:p.x,ey:p.y+200,progress:A.heavy.t/.9,width:A.role==='wall'?145:70,fieldOnly:true});}
 if(A.model==='disc'&&A.phase==='tell')for(const p of A.lanes)combatWarningDraw(e,{...p,ex:p.x+Math.cos(p.angle)*900,ey:p.y+Math.sin(p.angle)*900,progress:A.phaseT/A.dur,width:14,fieldOnly:true});
 // Native drawEnemyShieldBack/Front already surround this hull renderer.
 v31DrawBeams(e);
}
drawEnemy=function(e){
 if(e?._v31&&!e.dead)return v31DrawHull(e);
 if(e?._v31Turret&&!e.dead){const bk='overhaul_ground_base_2',s=e.w*1.27,im=e.flash>0?xartTint(bk,hitFlashColor(e),1):XART.get(bk);if(im)ctx.drawImage(im,e.x-s/2,e.y-s/2,s,s);
  v31Blit(V31_ART.banks['turret_'+e._modTurret.weapon],0,e._modTurret.angle,e.x,e.y,e.w*.96,e.flash>0?hitFlashColor(e):null);
  const A=e._v31Ground;if(A?.phase==='tell'&&e._modTurret.weapon!=='missile'){const p=v31TurretGun(e);combatWarningDraw(e,{...p,ex:A.target.x,ey:A.target.y,progress:A.t/.8,width:24,fieldOnly:true});}return;
 }
 return V31.base.draw.apply(this,arguments);
};
drawCombatFinalProjectile=function(b){if(!b?._v31Kind)return V31.base.projectile.apply(this,arguments);
 const kind=b._v31Kind,B=V31_ART.banks[kind];
 if(kind==='wall'){for(let i=-3;i<=3;i++)v31Blit(V31_ART.banks.flamethrower,Math.floor((b.t||0)*22+i+100)%4,Math.PI/2,b.x+i*20,b.y,54);return true;}
 if(!B)return false;
 const size=kind==='orb'?32:kind==='mine'?38:kind.includes('missile')?48:kind==='laser'?40:26;
 return v31Blit(B,Math.floor((b.t||0)*24)%4,Math.atan2(b.vy,b.vx),b.x,b.y,size);
};
updateEffects=function(dt){const r=V31.base.effects.apply(this,arguments);for(const q of V31.fx)q.t+=dt;V31.fx=V31.fx.filter(q=>q.t<q.life&&v31Alive(q.owner));return r;};
drawNavalFlashes=function(){const r=V31.base.flashes.apply(this,arguments);for(const q of V31.fx)v31Blit(V31_ART.banks.muzzle,Math.floor(q.t/q.life*4),q.p.angle,q.p.x,q.p.y,q.size);return r;};
groundTargetingDraw=function(){const r=V31.base.ground.apply(this,arguments);for(const q of groundTargetingFx){if(!q._v31Drop||q._v31Drop.bullet||q.impact||q.delay>0)continue;
 const u=clamp(q.t/q.warn,0,1),p=q._v31Drop.p,x=lerp(p.x,q.x,u),y=lerp(p.y,q.y,u)-Math.sin(u*Math.PI)*95;v31Blit(V31_ART.banks.orb,Math.floor(q.t*22)%4,Math.PI/2,x,y,28);}return r;};
updatePlay=function(dt){
 for(const q of groundTargetingFx){const d=q._v31Drop,b=d?.bullet;if(!b||b.dead||q.impact||q.dead)continue;
  const u=clamp((q.t+dt)/q.warn,0,1);b.x=lerp(d.p.x,q.x,u);b.y=lerp(d.p.y,q.y,u)-Math.sin(u*Math.PI)*95;b.vx=b.vy=0;}
 const r=V31.base.play.apply(this,arguments);
 for(const q of groundTargetingFx){const b=q._v31Drop?.bullet;if(!b)continue;
  if(q.impact||q.dead){b.dead=true;b._v31Detonated=true;}
  else if(b.dead||!eBullets.includes(b)){q.dead=true;v31Log(q.owner,'magma-arc-intercepted',{x:b.x,y:b.y});}}
 groundTargetingFx=groundTargetingFx.filter(q=>!q.dead);return r;
};
stageLoadBegin=function(n,keys){if(n===2)keys=[...(keys||[]),...Object.values(V31_ART.banks).map(a=>a.key),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return V31.base.load.call(this,n,keys);};
beginStage=function(){V31.fx=[];V31.events=[];return V31.base.begin.apply(this,arguments);};
killEnemy=function(e){if(e?._v31){e._v31.beams=[];e._v31.heavy=null;e._v31.lanes=[];e._v31.phase='destroyed';V31.fx=V31.fx.filter(q=>q.owner!==e);v31Log(e,'destroyed');}return V31.base.kill.apply(this,arguments);};
globalThis.BOF_VOLCANIC_REFIT={state:V31,art:V31_ART};
