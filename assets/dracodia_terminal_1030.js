'use strict';
/* RD84: terminal lightning/arena-download shatter. Native victory is still the
   sole reward owner. Every displayed effect is an authored, unrotated frame. */
const RD84={base:{final:j3FinalDeath,tick:r30Tick,death:dr5DeathTick,draw:r30DrawBoss,bg:drawBG,player:drawPlayer,arena:v17ArenaDraw,begin:beginStage,state:setState,visible:bossHealthVisible,load:stageLoadBegin,keys:v18Keys,warm:v18Warm},events:[],draws:{},reducedMotion:typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches};
for(const [key,a]of Object.entries(RD84_ART.pages))XART._src[key]=a.path;
for(const a of [...RD84_ART.stages,...RD84_ART.reunion,...RD84_ART.flash])XART._src[a.key]=a.path;
function rd84Keys(){return[...Object.keys(RD84_ART.pages),...RD84_ART.stages.map(a=>a.key),...RD84_ART.reunion.map(a=>a.key),...RD84_ART.flash.map(a=>a.key),'cf50_scenery_dim'];}
v18Keys=function(){return[...RD84.base.keys(),...rd84Keys()];};
v18Warm=function(){const prior=RD84.base.warm();return rd84Keys().map(k=>XART.rdy(k)).every(Boolean)&&prior;};
stageLoadBegin=function(n,keys){if(n===8){rd27ThunderReady();Snd.prepare(['rd27Lightning','rd71ScreamA','rd71ScreamB','bossWeaponCharge','warpGate','teleportIn','expBig','combatModule0927']);}return RD84.base.load.call(this,n,n===8?[...(keys||[]),...rd84Keys()]:keys);};
function rd84Own(b){return v18Owned(b)&&dr5State(b)?.deathStarted&&!!dr5State(b).rd84&&['dr5Death','dr5Portal','reunion'].includes(b._r30.mode);}
function rd84Log(b,event,more={}){RD84.events.push({event,mode:b._r30.mode,t:b._r30.t,...more});if(RD84.events.length>400)RD84.events.shift();}
function rd84Stop(){for(const k of ['rd27Lightning','rd71ScreamA','rd71ScreamB','bossWeaponCharge'])Snd.stopCue(k);}
function rd84Cue(b,k,gain=1){const played=Snd.play(k,gain);rd84Log(b,'sound',{key:k,played});}
j3FinalDeath=function(b){if(!v18Owned(b))return RD84.base.final.apply(this,arguments);if(dr5State(b).deathStarted)return;
 // The retired final-death wrapper constructs runtime snapshot shards. Prevent
 // that one side effect while preserving every native defeat/progression hook.
 const snapshot=r25BodySnapshot;let r;try{r25BodySnapshot=()=>null;r=RD84.base.final.apply(this,arguments);}finally{r25BodySnapshot=snapshot;}
 const D=dr5State(b);D.rd84={age:0,phase:'tremble',beat:-1,fx:[],nextBurst:6,bursts:0,stage:-1,poses:0,posePhase:0,flash:0,dim:0,origin:{x:b.x,y:b.y},events:new Set()};D.bodyGone=false;D.fx=[];D.bits=[];b._fv21Final=null;S78.debris=S78.debris.filter(q=>q.owner!==b);FV21.fx=FV21.fx.filter(q=>q.owner!==b);b._r30.v18.shards=[];for(const q of powerups)q.dead=true;whiteBlast=0;Snd.stopCue('dracodiaShriek');rd84Log(b,'terminal-start',{hp:b.hp,pools:{...j3State(b).hp}});rd84Cue(b,'rd71ScreamA',.9);return r;
};
function rd84Emit(b,bank,dx,dy){const Q=dr5State(b).rd84;Q.fx.push({bank,dx,dy,x:b.x+dx,y:b.y+dy,t:0,life:RD84_ART.banks[bank].length/24,anchor:b._r30.t<13.2});if(Q.fx.length>12)Q.fx.shift();rd84Log(b,'electric-burst',{bank,dx,dy});}
const RD84_DOWNLOADS=[.52,.46,.42,.38,.34,.30,.28,.26,.24,.22];
function rd84Download(t){let q=t-9.2;for(let i=0;i<RD84_DOWNLOADS.length;i++){if(q<RD84_DOWNLOADS[i])return{index:i,age:q,duration:RD84_DOWNLOADS[i]};q-=RD84_DOWNLOADS[i];}return{index:10,age:q,duration:.58};}
function rd84Death(b,dt){dr5Protect(b,dt);const S=b._r30,D=dr5State(b),Q=D.rd84,t=S.t;Q.age+=dt;Q.flash=0;Q.dim=t<9.2?Math.min(8,Math.floor(t*1.2)):0;b._fv21Final=null;
 for(const f of Q.fx)f.t+=dt;Q.fx=Q.fx.filter(f=>f.t<f.life);b.x=camLeftX()+viewW()/2;b.y=viewTopY()+203;
 const amp=(RD84.reducedMotion?.35:1)*Math.min(12,2+t*.9);Q.dx=Math.round(Math.sin(t*73)*amp);Q.dy=Math.round(Math.sin(t*89)*amp*.45);
 const beat=Math.min(23,Math.floor(2*Math.min(t,6)+Math.min(t,6)**2/3));if(t<=6&&beat!==Q.beat){Q.beat=beat;Q.strikeT=0;Q.lane=[4,1,7,3,6,0,8,2,5][beat%9];rd84Cue(b,'rd27Lightning',.85);rd84Log(b,'lightning-strike',{beat,lane:Q.lane});}Q.strikeT=(Q.strikeT||0)+dt;
 if(t>=3)D.radio=null;
 for(const [tag,at,key]of[['rising-shriek',2.3,'rd71ScreamB'],['peak-shriek',4.5,'rd71ScreamA'],['core-charge',5,'bossWeaponCharge']])if(t>=at&&!Q.events.has(tag)){Q.events.add(tag);rd84Cue(b,key,.9);}
 if(t<6){Q.phase='tremble';Q.posePhase+=dt*(2+t*1.7);Q.roar=Math.floor(Q.posePhase)%2===1;Q.pose=Q.roar?Math.min(13,Math.floor(3+t*1.7)):(Math.floor(t*14)%16);Q.white=Q.strikeT<.065?5:Math.floor(t*9)%3===0?2:0;Q.flash=Q.strikeT<.045?3:0;}
 else if(t<9.2){Q.phase='electric-overload';Q.posePhase+=dt*(12+(t-6)*3);Q.roar=Math.floor(Q.posePhase)%2===1;Q.pose=Q.roar?12:Math.floor(t*16)%16;Q.white=Math.floor(t*22)%3===0?5:1;
  if(t>=Q.nextBurst&&Q.bursts<20){const n=Q.bursts++;Q.nextBurst=t+Math.max(.10,.31-n*.011);const a=n*2.39996;rd84Emit(b,n%3?'electric_small':'electric_medium',Math.round(Math.cos(a)*(65+n%3*20)),Math.round(Math.sin(a)*(85+n%4*18)));rd84Cue(b,n%3?'combatModule0927':'expBig',.7);if(n%2===0)rd84Cue(b,'rd27Lightning',.7);}
  if(!Q.events.has('overload')){Q.events.add('overload');rd84Cue(b,'rd71ScreamB',1);}
 }else if(t<13.2){Q.phase='arena-downloads';Q.roar=true;Q.pose=12;Q.white=3;const x=rd84Download(t);Q.download=x;if(x.index!==Q.stage){Q.stage=x.index;rd84Cue(b,'warpGate',.8);rd84Log(b,'arena-download',{level:x.index<10?x.index+1:8});}Q.flash=x.age<.04?5:0;
 }else if(t<16.4){Q.phase='shatter';Q.white=0;D.bodyGone=true;if(!Q.events.has('shatter')){Q.events.add('shatter');Q.shatterAt={x:b.x,y:b.y};rd84Cue(b,'rd71ScreamB',.9);rd84Cue(b,'expBig',1);rd84Emit(b,'electric_final',0,0);rd84Log(b,'whole-body-shatter',{pieces:RD84_ART.shatterPieces});}Q.flash=t<13.3?6:0;
  const n=Math.floor((t-13.2)*4);if(n!==Q.chain&&n<9){Q.chain=n;rd84Emit(b,'electric_medium',Math.round(Math.sin(n*2.4)*150),Math.round(Math.cos(n*2.4)*140));if(n%2===0)rd84Cue(b,'expBig',.65);}
 }else{Q.phase='aftermath';Q.flash=t<16.55?4:0;}
 if(t>=18.4){S.mode='dr5Portal';S.t=0;D.radio=null;D.fx=[];D.bits=[];D.events.clear();dr5Ships(b);Q.fx=[];Q.phase='portal-form';Q.flash=0;rd84Stop();dr5Say(b,run.pilot.toUpperCase(),'The code is gone. Fury flight, I am coming home.');rd84Cue(b,'teleportIn');rd84Log(b,'blue-gated-portal');}
 if(RD84.reducedMotion){Q.white=Math.min(2,Q.white||0);Q.flash=Math.min(1,Q.flash);}
}
dr5DeathTick=function(b,dt){if(rd84Own(b))return rd84Death(b,dt);return RD84.base.death.apply(this,arguments);};
r30Tick=function(b,dt){if(!rd84Own(b))return RD84.base.tick.apply(this,arguments);const S=b._r30,D=dr5State(b),Q=D.rd84;dt=Math.min(.05,Math.max(0,dt||0));if(S.mode==='dr5Death')return rd84Death(b,dt);
 if(S.mode==='dr5Portal'){dr5Protect(b,dt);Q.age+=dt;const t=S.t,u=clamp((t-2)/2.8,0,1);Q.phase=t<.8?'portal-form':t<5?'portal-entry':'portal-close';Q.flash=t>6.1?6:0;for(const [i,s]of(D.ships||[]).entries())withSeat(s.seat,()=>{player.x=lerp(s.x,worldWidth()/2+(i?14:-14),u);player.y=lerp(s.y,viewTopY()+165,u);});if(t>=6.25){S.mode='reunion';S.t=0;D.radio=null;D.events.clear();Q.flash=0;Q.phase='reunion';run._realmReturned=true;dr5Ships(b);rd84Cue(b,'teleportIn',.8);Audio.startMusic('realm8');rd84Log(b,'above-ground-reunion');}return;}
 const out=RD84.base.tick.apply(this,arguments);if(S.mode==='reunion'&&state===GS.PLAY){Q.age+=dt;Q.flash=0;for(const [i,s]of(D.ships||[]).entries())withSeat(s.seat,()=>{player.x=worldWidth()/2+(D.ships.length>1?(i?18:-18):0);player.y=lerp(viewTopY()+150,viewTopY()+410,clamp(S.t/2.3,0,1));});}else{rd84Stop();rd84Log(b,'native-victory-handoff',{rewarded:S.rewarded,state});}return out;
};
function rd84Blit(a,x,y){if(!a||!XART.rdy(a.key))return false;ctx.drawImage(XART.get(a.key),...a.rect,Math.round(x+a.offset[0]),Math.round(y+a.offset[1]),a.w,a.h);return true;}
function rd84Bank(name,f,x,y){const q=RD84_ART.banks[name];if(!q)return false;RD84.draws[name]=(RD84.draws[name]||0)+1;return rd84Blit(q[clamp(Math.floor(f),0,q.length-1)],x,y);}
function rd84Gate(t,x,y,phase){if(phase==='form')return rd84Bank('gate_form',t/.8*12,x,y);if(phase==='close')return rd84Bank('gate_close',t/1.2*12,x,y);return rd84Bank('gate_loop',Math.floor(t*20)%16,x,y);}
r30DrawBoss=function(b){if(!rd84Own(b))return RD84.base.draw.apply(this,arguments);const S=b._r30,Q=dr5State(b).rd84,t=S.t;
 if(S.mode==='dr5Death'){
  const x=b.x+Q.dx,y=b.y+Q.dy;if(t<13.2){if(Q.phase==='arena-downloads'&&Q.download.index<10)rd84Bank('download_erase',Q.download.age/Q.download.duration*15,x,y);else rd84Bank((Q.roar?'roar':'idle')+'_'+(Q.white||0),Q.pose||0,x,y);}
  if(t<6&&Q.strikeT<.22){const col=camLeftX()+viewW()*(.08+(Q.lane||0)*.105);for(const px of [col,b.x])rd84Bank(Q.strikeT<.1?'lightning_strong':'lightning_tail',Math.floor(Q.strikeT*44)%8,px,viewTopY()+256);}
  for(const f of Q.fx)rd84Bank(f.bank,f.t*24,f.anchor?x+f.dx:f.x,f.anchor?y+f.dy:f.y);
  if(t>=13.2&&t<16.4)rd84Bank('body_shatter',(t-13.2)*20,Q.shatterAt.x,Q.shatterAt.y);
  return;
 }
 if(S.mode==='dr5Portal'){if(t<.8)rd84Gate(t,worldWidth()/2,viewTopY()+165,'form');else if(t<5)rd84Gate(t,worldWidth()/2,viewTopY()+165,'loop');else rd84Gate(t-5,worldWidth()/2,viewTopY()+165,'close');return;}
 const selected=seatList().map(s=>withSeat(s,()=>run.pilot));Q.squad=RD84_ART.pilots.filter(pk=>!selected.includes(pk));const positions=[[190,295],[245,300],[435,300],[490,295],[190,390],[245,398],[435,398],[490,390]];
 for(const [i,pk]of Q.squad.entries()){const [x,y]=positions[i];rd84Bank('shadow_'+pk,0,x+7,y+15);rd84Bank('ship_north_'+pk,31,x,y+Math.sin(Q.age*1.4+i)*1.5);}
 if(t<.8)rd84Gate(t,worldWidth()/2,viewTopY()+145,'loop');else if(t<2)rd84Gate(t-.8,worldWidth()/2,viewTopY()+145,'close');
};
drawBG=function(){if(!rd84Own(boss))return RD84.base.bg.apply(this,arguments);const S=boss._r30,Q=dr5State(boss).rd84;if(S.mode==='reunion'){const a=RD84_ART.reunion[Math.floor(Q.age*8)%8],near=RD84_ART.reunion[0],farX=Math.round(camLeftX()*.08);if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),0,0,680,208,farX,0,680,208);if(XART.rdy(near.key))ctx.drawImage(XART.get(near.key),0,208,680,304,0,208,680,304);RD84.parallax={farX,nearX:0,waterFrame:Math.floor(Q.age*8)%8};RD84.draws.riverfront=(RD84.draws.riverfront||0)+1;return;}
 if(S.mode==='dr5Death'&&Q.phase==='arena-downloads'&&Q.download.index<10){const a=RD84_ART.stages[Q.download.index];if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),Math.round(camLeftX()),viewTopY());return;}
 const r=RD84.base.bg.apply(this,arguments);if(Q.dim&&S.mode==='dr5Death')cf50DimDraw(Q.dim);return r;
};
v17ArenaDraw=function(){if(rd84Own(boss))return true;return RD84.base.arena.apply(this,arguments);};
drawPlayer=function(){if(!rd84Own(boss))return RD84.base.player.apply(this,arguments);const S=boss._r30,t=S.t;let f=31,name='ship_north_';if(S.mode==='dr5Portal'){if(t>=4.9)return;f=Math.round((1-clamp((t-2)/2.8,0,1))*31);}else if(S.mode==='reunion'){f=Math.min(31,Math.floor(t/1.6*31));name='ship_south_';}rd84Bank(name+run.pilot,f,player.x,player.y);};
const rd84World=drawWorld;drawWorld=function(){const out=rd84World.apply(this,arguments);if(rd84Own(boss)){const f=dr5State(boss).rd84.flash;if(f){const a=RD84_ART.flash[clamp(f|0,0,6)];if(XART.rdy(a.key)){ctx.save();ctx.translate(-camLeftX(),0);ctx.drawImage(XART.get(a.key),Math.round(camLeftX()),viewTopY());ctx.restore();}}}return out;};
bossHealthVisible=function(b){if(rd84Own(b))return false;return RD84.base.visible.apply(this,arguments);};
const rd84Update=updatePlay;updatePlay=function(){const out=rd84Update.apply(this,arguments);if(rd84Own(boss))for(const q of powerups)q.dead=true;return out;};
beginStage=function(){rd84Stop();RD84.events=[];return RD84.base.begin.apply(this,arguments);};
setState=function(s){if(s!==GS.PLAY&&rd84Own(boss))rd84Stop();return RD84.base.state.apply(this,arguments);};
globalThis.BOF_DRACODIA_TERMINAL_1030=RD84;
