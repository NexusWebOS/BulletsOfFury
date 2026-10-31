'use strict';
/* RD71 / RD94: actual PixelLab metal gates, infector return, data-bomb possession and whole shoulders. */
const RD71={base:{tick:r30Tick,draw:r30DrawBoss,body:bi24Draw,at:r30At,rupture:v18Rupture,update:updatePlay,load:stageLoadBegin},events:[],breaks:[],last:null};
for(const a of [...Object.values(RD71_ART),...Object.values(RD94_ART)])XART._src[a.key]=a.path;
function rd71Pool(key,file){const slots=[],list=[];for(let i=0;i<2;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri:file,attached:false,used:0};return Snd._touchVoice(slots[i]);}});Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:1,native:true,min:.65};}
rd71Pool('rd71ScreamA','assets/game/levels/stage_08/audio/possession_1030/scream_a.mp3');rd71Pool('rd71ScreamB','assets/game/levels/stage_08/audio/possession_1030/scream_b.mp3');
stageLoadBegin=function(n,keys){RD71.breaks=[];if(n===8)Snd.prepare(['rd71ScreamA','rd71ScreamB','warpGate','bossWeaponCharge','combatAlien0927','timedBombBlast']);return RD71.base.load.call(this,n,n===8?[...(keys||[]),...[...Object.values(RD71_ART),...Object.values(RD94_ART)].map(a=>a.key)]:keys);};
function rd71Blit(n,f,x,y,hit=false){const a=RD71_ART[n+(hit?'_hit':'')]||RD71_ART[n];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
function rd71Time(b){const S=b._r30;return S.mode==='dr5er23entry'?S.t:S.mode==='v18arrival'?7.2+S.t:9.6+S.t;}
function rd71Log(b,event,data={}){RD71.events.push({event,time:rd71Time(b),clock:b._r30.clock,...data});if(RD71.events.length>600)RD71.events.shift();}
function rd71Cue(b,id,t,key,gain){const R=rd29Init(b);R.rd71Flags??={};if(rd71Time(b)<t||R.rd71Flags[id])return;R.rd71Flags[id]=true;Snd.play(key,gain);rd71Log(b,id,{cue:key,gain});}
function rd71Ufo(b){const R=rd29Init(b),t=rd71Time(b),home=R.home,gx=clamp(home.x+82,camLeftX()+125,camRightX()-125),gy=Math.max(viewTopY()+125,home.y-105),u=clamp((t-9.7)/.9,0,1),exit=clamp((t-12.9)/1.1,0,1),k=exit*exit*(3-2*exit);
 const hx=gx+(36+Math.sin(t*2.3)*10)*u,hy=gy+(70+Math.sin(t*3)*5)*u;
 return{x:lerp(hx,gx,k),y:lerp(hy,gy,k),gx,gy,u,exit};}
function rd94GatePose(color,t,form,loop,close){if(t<0||t>=form+loop+close)return null;const phase=t<form?'form':t<form+loop?'loop':'close',a=RD94_ART[color+'_'+phase];
 const f=phase==='form'?Math.min(a.frames-1,Math.floor(t/form*a.frames)):phase==='loop'?Math.floor((t-form)*a.fps)%a.frames:Math.min(a.frames-1,Math.floor((t-form-loop)/close*a.frames));return{color,phase,f,a};}
function rd94GateBlit(q,x,y){if(!q||!XART.rdy(q.a.key))return false;const a=q.a,f=q.f;ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
rd29White=function(t){if(t<8.5)return 0;if(t<9.05)return Math.floor((t-8.5)/.55*16);if(t<9.4)return 16;return 16-Math.floor(clamp((t-9.4)/1.6,0,1)*16);};
r30Tick=function(b,dt){if(!rd29Own(b))return RD71.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);const S=b._r30,N=S.v18,R=rd29Init(b);dr5Protect(b,dt);b._noHit=true;N.attack=null;
 if(!R.ships)R.ships=seatList().map(seat=>withSeat(seat,()=>({seat,x:player.x,y:player.y})));for(const q of R.ships)withSeat(q.seat,()=>{player.x=q.x;player.y=q.y;});
 const total=rd71Time(b);R.time=total;
 if(S.mode==='dr5er23entry'){
  rd71Cue(b,'background-warp',0,'combatEnergy0927',.45);if(S.t>=3.4&&!R.flags.arena){R.flags.arena=true;N.arenaPhase=0;rd71Log(b,'arena-handoff');}
  rd71Cue(b,'purple-toxic-gate',5.4,'warpGate',.85);if(S.t>=7.2){b.x=R.home.x;b.y=R.home.y;v18SetMode(b,'v18arrival');rd71Log(b,'neutral-drone-emerges');}
 }else if(S.mode==='v18arrival'){
  b.x=R.home.x;b.y=R.home.y+Math.sin(S.t*2)*3;rd71Cue(b,'drone-ready',8.2,'combatModule0927',.5);rd71Cue(b,'red-toxic-gate',9.2,'warpGate',.95);
  if(S.t>=2.4){v18SetMode(b,'v18conversion');rd71Log(b,'infector-arrival');}
 }else{
  const t=S.t,power=clamp((t-3.05)/5.4,0,1);b.x=R.home.x+Math.sin(t*78)*power*7;b.y=R.home.y+Math.sin(t*91)*power*4;shake=Math.max(shake,power*3.5);
  rd71Cue(b,'red-toxic-gate',9.2,'warpGate',.95);rd71Cue(b,'ufo-hover',9.7,'combatAlien0927',.7);rd71Cue(b,'data-bomb-charge',10.75,'bossWeaponCharge',.8);
  if(total>=10.75&&total<12.1)combatWarningTick(b,'rd71-data-bomb',total-10.75,1.35);
  rd71Cue(b,'data-bomb-release',12.1,'combatOrb0927',.8);
  rd71Cue(b,'infector-returns-through-red-gate',12.9,'combatModule0927',.45);rd71Cue(b,'red-gate-closes-after-return',14.06,'warpGate',.65);
  if(t>=3.05&&!R.rd71Impact){R.rd71Impact=true;R.rd71BombAt={x:R.home.x,y:R.home.y};explode(b.x,b.y,78,'purple');rd71Log(b,'data-bomb-impact');dr5Say(b,run.pilot.toUpperCase(),'The drone... something is taking it over!');}
  rd71Cue(b,'robotic-scream-first',12.7,'rd71ScreamA',.98);rd71Cue(b,'robotic-scream-rising',15.2,'rd71ScreamB',1);rd71Cue(b,'robotic-scream-violent',17.25,'rd71ScreamA',1);
  if(t>=8.45)dr5State(b).radio=null;rd71Cue(b,'covering-white-impact',18.65,'expBig',1);rd71Cue(b,'robotic-host-reveal',19.05,'rd71ScreamB',1);
  if(t>=9.05){b.x=R.home.x+Math.sin(S.clock*.65)*Math.min(24,viewW()*.04);b.y=R.home.y+Math.sin(S.clock*.9)*5;}
  if(t>=11.4){dr5State(b).radio=null;rd71Log(b,'native-phase1-fight');v18Fight(b);}
 }
};
function rd71GateFrame(t,form,loop,close){if(t<0||t>=form+loop+close)return null;if(t<form)return Math.min(3,Math.floor(t/form*4));if(t<form+loop)return 4+Math.floor((t-form)*12)%8;return 12+Math.min(11,Math.floor((t-form-loop)/close*12));}
r30DrawBoss=function(b){if(!rd29Own(b))return RD71.base.draw.apply(this,arguments);const S=b._r30,R=rd29Init(b),total=rd71Time(b),primary=rd94GatePose('purple',total-5.4,1.1,2.2,.7),secondary=rd94GatePose('red',total-9.2,.7,4.16,.8),ufo=rd71Ufo(b),t=S.t;
 if(primary)rd94GateBlit(primary,R.home.x,R.home.y-10);if(secondary)rd94GateBlit(secondary,ufo.gx,ufo.gy);
 if(total>=9.7&&total<14){const retract=ufo.exit>.45,emerging=total<10.6,name=emerging||retract?'ufo_emerge':'ufo',f=retract?Math.round((1-clamp((ufo.exit-.45)/.55,0,1))*15):emerging?Math.floor(ufo.u*15):total>=10.75&&total<12.1?8+Math.floor((total-10.75)/1.35*4):Math.floor(total*12)%16;rd71Blit(name,f,ufo.x,ufo.y);}

 const possessed=S.mode==='v18conversion'&&t>=3.05&&t<9.05,codeAge=t-3.05,codeFrame=Math.floor(Math.max(0,codeAge)*24)%48;
 if(possessed)rd71Blit(codeAge<1/3?'helix_in_back':'helix_back',codeAge<1/3?Math.floor(codeAge*24):codeFrame,b.x,b.y);
 if(S.mode==='v18arrival')rd71Blit(t<1.0?'drone_emerge':'drone_ready',t<1?Math.floor(t*24):Math.min(15,Math.floor((t-1)/1.1*16)),b.x,b.y);
 if(S.mode==='v18conversion'){
  if(t<9.05)rd71Blit(t<3.05?'drone_ready':'drone_charge',t<3.05?15:Math.min(63,Math.floor((t-3.05)/5.4*64)),b.x,b.y);
  else bi24Draw(bi24Sample('dracodia_wind',1-clamp((t-10.4)/1,0,1)),b,360);
 }
 if(possessed)rd71Blit(codeAge<1/3?'helix_in_front':'helix_front',codeAge<1/3?Math.floor(codeAge*24):codeFrame,b.x,b.y);
 if(total>=10.75&&total<12.1)combatWarningDraw(b,{x:ufo.x,y:ufo.y+24,ex:R.home.x,ey:R.home.y,width:30,progress:(total-10.75)/1.35,laneShape:'line'});
 if(total>=12.1&&total<12.65){const u=(total-12.1)/.55,p=rd71Ufo(b);rd71Blit('bomb_charge',Math.floor(u*16),lerp(p.x,R.home.x,u),lerp(p.y+24,R.home.y,u));}
 if(total>=12.65&&total<13.05)rd71Blit('bomb_burst',Math.floor((total-12.65)/.4*RD71_ART.bomb_burst.frames),R.home.x,R.home.y);
 RD71.last={time:total,mode:S.mode,primary:primary?.f??null,primaryPhase:primary?.phase??null,secondary:secondary?.f??null,secondaryPhase:secondary?.phase??null,ufo:total>=9.7&&total<14,ufoReturning:ufo.exit>0&&total<14,ufoAt:{x:ufo.x,y:ufo.y},redGateAt:{x:ufo.gx,y:ufo.gy},gated:true,possessed,codeFrame,white:S.mode==='v18conversion'?rd29White(t):0,host:S.mode==='v18conversion'&&t>=9.05,protected:b._noHit};RD29.last=RD71.last;
};
function rd71HostName(q){return q?.a?.key?.replace('nca_bi24_','');}
bi24Draw=function(q,b,size,rot=0){const name=rd71HostName(q);if(!rb23Host(b)||!RD71_ART['host_'+name+'_core']||rot)return RD71.base.body.apply(this,arguments);
 for(const id of ['left','right','core']){const p=b.parts.find(p=>p.id===id);if(!p||p.destroyed||p.hp<=0&&id!=='core')continue;rd71Blit('host_'+name+'_'+id,q.f,b.x,b.y,Math.max(p.flash||0,id==='core'?b.flash||0:0)>0);}
 BI24.current.set(b,{...q,size:360,k:360/512,rot:0,x:b.x,y:b.y,key:q.a.key});return true;
};
function rd71At(a,f,x,y){const xx=Math.floor(x+a.pivot[0]),yy=Math.floor(y+a.pivot[1]);if(xx<0||xx>=a.cw||yy<0||yy>=a.ch)return false;const row=a.spans[f][yy];for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;}
r30At=function(b,x,y){if(!rb23Host(b)||b._r30.mode!=='fight'||b._r30.v18.bi24Rolled)return RD71.base.at.apply(this,arguments);if(!r30Live(b)||b._noHit)return null;const q=r25HostSample(b);
 for(const id of ['left','right','core']){const p=b.parts.find(p=>p.id===id),a=RD71_ART['host_'+q.name+'_'+id];if(p&&!p.destroyed&&p.hp>0&&a&&rd71At(a,q.f,x-b.x,y-b.y))return p;}return null;
};
v18Rupture=function(b,p){if(!rb23Host(b)||!['left','right'].includes(p.id))return RD71.base.rupture.apply(this,arguments);const q=r25HostSample(b),a=RD71_ART['host_'+q.name+'_'+p.id];if(!a)return RD71.base.rupture.apply(this,arguments);
 const points=a.blasts[q.f];RD71.breaks.push({b,origin:{x:b.x,y:b.y},points,t:0,next:0,side:p.id});if(RD71.breaks.length>2)RD71.breaks.shift();r30Sound('expBig');shake=Math.max(shake,8);rd71Log(b,'whole-shoulder-arm-break',{part:p.id,points});
};
updatePlay=function(dt){const out=RD71.base.update.apply(this,arguments);for(const F of RD71.breaks){F.t+=dt;if(F.b!==boss||run.stage!==8||F.b.dead){F.done=true;continue;}while(F.next<F.points.length&&F.t>=F.next*.075){const p=F.points[F.next++];explode(F.origin.x+p[0],F.origin.y+p[1],F.next<3?92:76,'purple',null,null,null,null,true);}if(F.t>.85)F.done=true;}RD71.breaks=RD71.breaks.filter(f=>!f.done);return out;};
globalThis.BOF_DRACODIA_POSSESSION_1030={state:RD71};
