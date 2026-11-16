"use strict";
/* CB112: Current Breaker's authored liquid arsenal. Native HP, damage,
   shared cues, defensive clears, hit flashes and death remain the owners. */
const CB112={base:{plan:buildStagePlan,spawn:spawnEnemy,tick:s911Tick,visual:s911Visual,guns:s911Guns,draw:s911Draw,shot:s911Projectile,
 play:updatePlay,targets:_lockTargets,cancel:s911Cancel,bg:drawBG,load:stageLoadBegin,begin:beginStage,
 intercept:enemyOrdnanceCanIntercept,break:ordnanceBreak1002},balls:[],fx:[],events:[],serial:0};
for(const B of Object.values(CB112_ART.banks))XART._src[B.key]=B.path;
function cb112Own(e){return e?._s911?.model==='current';}
function cb112Live(e){return cb112Own(e)&&s911Live(e);}
function cb112Log(e,event,data={}){CB112.events.push({id:e?._s911?.id,event,t:efxClock,...data});if(CB112.events.length>1800)CB112.events.shift();}
function cb112Set(e,phase){const q=e._cb112;Object.assign(q,{phase,t:0,beat:0,round:0,flightNext:null,from:{x:e.x,y:e.y}});e._s911.phase=phase;e._s911.t=0;e._s911.attack=phase;cb112Log(e,'phase',{phase});}
function cb112Init(e){if(e._cb112)return e._cb112;const q=e._cb112={age:0,t:0,phase:'entry',scale:1,dark:0,human:false,cycleDone:false,home:clamp(e.x,camLeftX()+100,camRightX()-100),baseW:e.w,baseH:e.h,entryY:e.y};
 e._noBodyContact=true;cb112Set(e,'entry');return q;}
function cb112Scale(e){return s911M(e).span/256*(e._cb112?.scale??1);}
function cb112Point(e,p){const k=cb112Scale(e);return{x:e.x+(p[0]-192)*k,y:e.y+(p[1]-192)*k,angle:Math.PI/2};}
function cb112Action(e){const q=e._cb112,t=q.t;if(q.phase==='grenade-charge')return 0;
 if(q.phase==='grenades'){const n=Math.floor(t/q.interval),u=t/q.interval-n;return(n%2?4:0)+(u<.27?0:u<.59?1:u<.8?2:3);}
 if(q.phase==='tidal-charge')return 8+Math.min(3,Math.floor(t/.95*4));
 if(q.phase==='tidal'){const u=t/1.25%1;return 8+Math.min(7,Math.floor(u*8));}
 return 8;
}
function cb112Visual(e){const q=e._cb112,A=e._s911,M=s911M(e),k=cb112Scale(e);let B,f=0,flow=null,view='front';
 if(!q)return CB112.base.visual(e);
 if(q.phase==='entry'||q.phase==='marble'||q.phase==='marble-settle'){B=CB112_ART.banks.orb;f=Math.floor(q.age*(q.phase==='entry'?70:100))%32;flow=CB112_ART.banks.orb_flow;view='orb';}
 else if(q.phase==='transform'||q.phase==='reform'){B=M.morph;f=Math.min(B.frames-1,Math.floor(q.t/(q.phase==='transform'?2.65:1.9)*B.frames));flow=CB112_ART.banks.morph_flow;view='transform';}
 else if(q.phase==='flight-launch'||q.phase==='depth-launch'){B=M.flightLaunch;f=Math.min(7,Math.floor(q.t/.48*8));view='tilt';}
 else if(['flight-exit','flight-warn-n','flight-n','flight-warn-s','flight-s','depth-exit','depth-return-exit','depth-arrive','front-arrive','flight-turn','depth-turn'].includes(q.phase)){B=M.flight;view='overhead';}
 else if(q.phase==='flight-return'||q.phase==='depth-settle'){B=M.flightReturn;f=Math.min(7,Math.floor(q.t/.42*8));view='tilt';}
 else if(q.phase==='depth-spin'||q.phase==='depth-charge'||q.phase==='depth-linger'){B=CB112_ART.banks.yaw;f=q.phase==='depth-charge'?0:Math.floor(q.t*(30+Math.min(26,q.t*8)))%32;flow=CB112_ART.banks.yaw_flow;view='yaw';}
 else{B=CB112_ART.banks.actions;f=cb112Action(e);flow=CB112_ART.banks.actions_flow;}
 return[{B,f,p:e,angle:view==='overhead'?A.head:Math.PI/2,scale:k,flow,view}];
}
s911Visual=function(e){return cb112Own(e)?cb112Visual(e):CB112.base.visual.apply(this,arguments);};
s911Guns=function(e){if(!e?._cb112)return CB112.base.guns.apply(this,arguments);const q=e._cb112,v=cb112Visual(e)[0],M=s911M(e);let p;
 if(v.view==='yaw')p=CB112_ART.yawHands[v.f];
 else if(v.view==='front')p=CB112_ART.hands[v.f];
 else if(v.view==='overhead')p=M.flightPalms[v31Dir(e._s911.head,8)].map(p=>p.map(n=>n+64));
 else if(v.view==='tilt')p=(q.phase==='flight-return'||q.phase==='depth-settle'?M.returnPalms:M.launchPalms)[v.f].map(p=>p.map(n=>n+64));
 else p=[[146,210],[238,210]];
 return p.map((p,i)=>({...cb112Point(e,p),index:i}));};
function cb112Cue(e,key,gap=.16){combatAudio0927(e,key,gap);}
function cb112Grenade(e,p,angle=null){const q=e._cb112,T=targetShip(e.x,e.y),aim=angle==null?{x:clamp(T.x+(p.index?30:-30),camLeftX()+35,camRightX()-35),y:clamp(T.y,PLAY.y+100,VH-40)}:{x:p.x+Math.cos(angle)*190,y:p.y+Math.sin(angle)*190},b=s911Shot(e,{...p,angle:Math.atan2(aim.y-p.y,aim.x-p.x)},'grenade',1,true);
 if(!b)return;const flight=1.4;b._cb112Grenade=true;b._s911Hazard={kind:'grenade',target:aim,age:0,flight};b.vx=(aim.x-p.x)/flight/60;b.vy=(aim.y-p.y)/flight/60;S911.hazards.add(b);cb112Log(e,'grenade',{hand:p.index,x:p.x,y:p.y,radial:angle!=null});}
function cb112Wave(e,p,angle,side=false){const b=s911Shot(e,{...p,angle},'wave',side?3.7:2.6,true);if(!b)return;
 b._cb112Wave={born:efxClock,side,w:side?32:145,h:side?82:40};b.w=b._cb112Wave.w*.25;b.h=b._cb112Wave.h*.25;b._weaponProof=true;b._shootable=false;cb112Log(e,'wave',{side,index:p.index,x:p.x,y:p.y,angle,phase:e._cb112.phase,pose:cb112Visual(e)[0].f});}
function cb112Roller(e,p){const T=targetShip(e.x,e.y),a=Math.atan2(T.y-p.y,T.x-p.x),b=s911Shot(e,{...p,angle:a},'laser-orb',2.9,true);if(!b)return;
 const F={id:++CB112.serial,e,q:b,t:0,size:12,done:false,returning:null};b._cb112Roller=F;b._weaponProof=true;b._shootable=false;b.homing=false;CB112.balls.push(F);cb112Log(e,'roller',{id:F.id,hand:p.index});}
function cb112Splash(e,x,y,size=100){CB112.fx.push({e,x,y,t:0,life:.65,size});if(CB112.fx.length>64)CB112.fx.shift();cb112Cue(e,'cfComboWater',.12);}
function cb112Weapon(F,shot){if(F.done||F.returning||!F.q||F.q.dead||!shot||shot.dead)return false;const missile=['gmiss','missile','nukem','retinaMissile'].includes(shot.kind)||/missile|rocket|warhead/i.test(shot.kind||'');
 const b=F.q;b.dead=true;F.q=null;if(missile){F.returning={x:b.x,y:b.y,size:F.size,t:0,seat:shot.seat||1};cb112Cue(F.e,'missileHit',.1);cb112Log(F.e,'roller-reflected',{id:F.id});}
 else{F.done=true;cb112Splash(F.e,b.x,b.y,120);cb112Log(F.e,'roller-safe-splash',{id:F.id});}
 if(!shot.pierce&&shot.kind!=='beam')shot.dead=true;return true;}
function cb112Segment(px,py,x1,y1,x2,y2,r){const dx=x2-x1,dy=y2-y1,d=dx*dx+dy*dy,u=d?clamp(((px-x1)*dx+(py-y1)*dy)/d,0,1):0;return Math.hypot(px-x1-u*dx,py-y1-u*dy)<=r;}
function cb112Intercept(dt){for(const b of eBullets)if(!b.dead&&b._cb112Wave){const q=b._cb112Wave,g=Math.min(1,.25+Math.max(0,efxClock-q.born)*2.5);b.w=q.w*g;b.h=q.h*g;}for(const F of CB112.balls){if(F.done||F.returning||!F.q||F.q.dead)continue;const b=F.q,r=F.size*.36;
 for(const p of pBullets){if(p.dead)continue;let hit=false;if(p.kind==='beam')hit=Math.abs(p.x-b.x)<r+(p.w||12)/2&&b.y+r>=(p.top??PLAY.y)&&b.y-r<=(p.bot??player.y);
 else if(p.kind==='flame')hit=flameHit(p,b.x,b.y,r*2,r*2);
 else if(p.kind==='firewhip'&&p.reach&&p.duration)hit=fireWhipTouches(p,b,(p.t||0)/p.duration,(p.t||0)/p.duration);
 else hit=cb112Segment(b.x,b.y,p.x,p.y,p.x+(p.vx||0)*dt*60-b.vx*dt*60,p.y+(p.vy??-(p.spd||0))*dt*60-b.vy*dt*60,r+Math.max(p.w||4,p.h||8)*.4);
 if(hit&&cb112Weapon(F,p))break;
 }}}
function cb112Effects(dt){for(const f of CB112.fx)f.t+=dt;CB112.fx=CB112.fx.filter(f=>f.t<f.life);
 for(const F of CB112.balls){if(F.done)continue;if(!cb112Live(F.e)){F.done=true;if(F.q)F.q.dead=true;continue;}F.t+=dt;
 if(F.returning){const r=F.returning;r.t+=dt;const u=clamp(r.t/.72,0,1);F.x=lerp(r.x,F.e.x,u);F.y=lerp(r.y,F.e.y,u);F.size=lerp(r.size,12,u);if(u>=1){F.done=true;const before=F.e.hp,save=_dmgBullet,src=_dmgSrc,seat=_shooter;_dmgBullet=null;_dmgSrc='missile';shooterSet(r.seat);try{hitEnemy(F.e,22);}finally{_dmgBullet=save;_dmgSrc=src;shooterSet(seat);}cb112Splash(F.e,F.e.x,F.e.y,82);cb112Log(F.e,'roller-counter-hit',{id:F.id,damage:before-F.e.hp});}}
 else if(F.q){F.size=Math.min(58,12+F.t*24);F.q.w=F.q.h=F.size*.65;F.x=F.q.x;F.y=F.q.y;if(F.q.dead||!eBullets.includes(F.q)){F.done=true;cb112Splash(F.e,F.x,F.y,85);}}
 }CB112.balls=CB112.balls.filter(F=>!F.done);}
function cb112Warn(e,x,y,angle,progress,width=80,len=900){combatWarningDraw(e,{x,y,ex:x+Math.cos(angle)*len,ey:y+Math.sin(angle)*len,width,progress:clamp(progress,0,1),fieldOnly:true});}
function cb112Tick(e,dt){if(!cb112Live(e))return;const q=cb112Init(e),A=e._s911;q.age+=dt;q.t+=dt;q.beat-=dt;A.age=q.age;A.t=q.t;A.head=A.head??Math.PI/2;e.shoots=e.armed=false;
 const dark=['grenade-charge','grenades'].includes(q.phase)?.61:0;q.dark+=clamp(dark-q.dark,-dt*1.7,dt*1.7);
 if(bossActive||subBossActive||bossDefeated||q.age>64){if(q.phase!=='retreat'){s911Cancel(e);cb112Set(e,'retreat');}}
 const cx=(camLeftX()+camRightX())/2,homeY=PLAY.y+150;
 if(q.phase==='entry'){A.head=Math.PI/2;q.entryY+=170*dt;const taper=clamp((homeY-q.entryY)/65,0,1);e.x=q.home+Math.sin(q.age*8)*22*taper;e.y=q.entryY+Math.cos(q.age*8)*11*taper;if(q.entryY>=homeY){e.y=homeY;if(!s911Live(S911.heavy)||S911.heavy===e){S911.heavy=e;cb112Set(e,'transform');cb112Cue(e,'cfComboWater',.5);}}}
 else if(q.phase==='transform'||q.phase==='reform'){if(q.t>(q.phase==='transform'?2.65:1.9)){q.human=A.human=true;cb112Set(e,q.phase==='transform'?'grenade-charge':'tidal-charge');}}
 else if(q.phase==='grenade-charge'){q.interval=turretInterval15(.44);if(q.t>.95){cb112Set(e,'grenades');q.next=q.interval*.60;}}
 else if(q.phase==='grenades'){if(q.t>=q.next){const n=q.round,index=n%2?0:1,p=s911Guns(e)[index];cb112Grenade(e,p);cb112Cue(e,'cfComboWater',.15);q.round++;q.next+=q.interval;}if(q.t>5.2)cb112Set(e,'flight-launch');}
 else if(q.phase==='flight-launch'){if(q.t>.48){A.head=Math.PI/2;cb112Set(e,'flight-turn');}}
 else if(q.phase==='flight-turn'||q.phase==='depth-turn'){A.head=Math.PI/2+Math.PI*clamp(q.t/.32,0,1);if(q.t>.32){cb112Set(e,q.phase==='flight-turn'?'flight-exit':'depth-exit');cb112Cue(e,'jetDash',.5);}}
 else if(q.phase==='flight-exit'){e.y-=600*dt;if(e.y<viewTopY()-160){q.lane=clamp(targetShip(e.x,e.y).x+85,camLeftX()+95,camRightX()-95);e.x=q.lane;e.y=VH+160;A.head=-Math.PI/2;cb112Set(e,'flight-warn-n');cb112Cue(e,'bossWeaponCharge',.6);}}
 else if(q.phase==='flight-warn-n'||q.phase==='flight-warn-s'){combatWarningTick(e,'cb112-flight',q.t,.85);if(q.t>.85){cb112Set(e,q.phase==='flight-warn-n'?'flight-n':'flight-s');cb112Cue(e,'jetDash',.5);}}
 else if(q.phase==='flight-n'||q.phase==='flight-s'){const north=q.phase==='flight-n';A.head=north?-Math.PI/2:Math.PI/2;e.y+=(north?-1:1)*610*dt;e.x=q.lane+Math.sin(q.t*7)*4;
  if(e.y>PLAY.y+40&&e.y<VH-40){if(q.flightNext==null)q.flightNext=q.t;if(q.t+1e-8>=q.flightNext){s911Guns(e).forEach((p,i)=>{if(p.y>PLAY.y+15&&p.y<VH-15)cb112Wave(e,p,i?0:Math.PI,true);});q.flightNext+=turretInterval15(.30);cb112Cue(e,'cfComboWater',.18);}}
  if(north&&e.y<viewTopY()-160){q.lane=clamp(targetShip(e.x,e.y).x-85,camLeftX()+95,camRightX()-95);e.x=q.lane;e.y=viewTopY()-160;A.head=Math.PI/2;cb112Set(e,'flight-warn-s');cb112Cue(e,'bossWeaponCharge',.6);}
  else if(!north&&e.y>VH+160){q.human=A.human=false;cb112Set(e,'marble');}}
 else if(q.phase==='marble'){const u=clamp(q.t/.6,0,1),ease=u*u*(3-2*u),a=Math.PI/2+q.t*TAU*.73; e.x=lerp(q.from.x,cx+Math.cos(a)*(viewW()/2-78),ease);e.y=lerp(q.from.y,VH*.49+Math.sin(a)*(VH*.5-78),ease);
  if(q.t>.65&&q.beat<=0){for(let i=0;i<9;i++)cb112Grenade(e,{x:e.x,y:e.y,index:i},q.t*.9+i*TAU/9);q.beat=.95;cb112Cue(e,'cfComboWater',.22);cb112Log(e,'nine-grenade-pulse');}
  if(q.t>4.35)cb112Set(e,'marble-settle');}
 else if(q.phase==='marble-settle'){const u=clamp(q.t/.65,0,1);e.x=lerp(q.from.x,worldWidth()/2,u);e.y=lerp(q.from.y,homeY,u);if(u>=1)cb112Set(e,'reform');}
 else if(q.phase==='tidal-charge'){if(q.t>.95){cb112Set(e,'tidal');q.next=.65;}}
 else if(q.phase==='tidal'){if(q.t>=q.next){const ports=s911Guns(e);ports.forEach(p=>cb112Wave(e,p,Math.PI/2));q.next+=1.25;q.round++;cb112Cue(e,'cfComboWater',.30);}if(q.t>3.75)cb112Set(e,'depth-launch');}
 else if(q.phase==='depth-launch'){if(q.t>.48){A.head=Math.PI/2;cb112Set(e,'depth-turn');}}
 else if(q.phase==='depth-exit'){e.y-=420*dt;q.scale=Math.max(.34,q.scale-dt*.7);if(e.y<viewTopY()-165){q.scale=.34;e.y=viewTopY()-90;e.x=cx;A.head=Math.PI/2;cb112Set(e,'depth-arrive');}}
 else if(q.phase==='depth-arrive'){e.y+=210*dt;if(e.y>PLAY.y+85){e.y=PLAY.y+85;cb112Set(e,'depth-settle');}}
 else if(q.phase==='depth-settle'){if(q.t>.42)cb112Set(e,'depth-charge');}
 else if(q.phase==='depth-charge'){if(q.t>1.15){cb112Set(e,'depth-spin');q.next=.1;cb112Cue(e,'cfComboWater',.4);}}
 else if(q.phase==='depth-spin'){e.x=cx+Math.sin(q.t*1.4)*65;e.y=PLAY.y+85+Math.sin(q.t*2)*9;
  if(q.t>=q.next){const ports=s911Guns(e),p=ports[q.round%2];cb112Roller(e,p);q.round++;q.next+=turretInterval15(.52);cb112Cue(e,'cfComboWater',.18);}if(q.t>6.1)cb112Set(e,'depth-linger');}
 else if(q.phase==='depth-linger'){if(q.t>2.2){A.head=-Math.PI/2;cb112Set(e,'depth-return-exit');}}
 else if(q.phase==='depth-return-exit'){e.y-=310*dt;if(e.y<viewTopY()-120){e.y=viewTopY()-180;e.x=cx;A.head=Math.PI/2;cb112Set(e,'front-arrive');}}
 else if(q.phase==='front-arrive'){q.scale=Math.min(1,q.scale+dt*.65);e.y+=250*dt;if(e.y>=homeY){e.y=homeY;q.scale=1;cb112Set(e,'flight-return');}}
 else if(q.phase==='flight-return'){if(q.t>.42){q.cycleDone=true;s911Cancel(e);cb112Set(e,'retreat');cb112Log(e,'arsenal-complete');}}
 else if(q.phase==='retreat'){q.dark=Math.max(0,q.dark-dt*2);e.y-=200*dt;if(e.y<viewTopY()-190)e.dead=true;}
 if(!['entry','transform','reform','marble','marble-settle'].includes(q.phase))q.human=A.human=true;
 if(['transform','reform','grenade-charge','grenades','tidal-charge','tidal','depth-charge'].includes(q.phase)){e.x+=Math.sin(q.age*1.7)*9*dt;e.y+=Math.cos(q.age*2.1)*4*dt;}
 e.w=q.baseW*q.scale;e.h=q.baseH*q.scale;A.phase=q.phase;A.t=q.t;
}
s911Tick=function(e,dt){return cb112Own(e)?cb112Tick(e,dt):CB112.base.tick.apply(this,arguments);};
function currentBreakerPending112(){return run.stage===9&&!run._gp4StageX&&(warnKind==='sub'||CB112.planned&&!CB112.dispatched&&stageTimer>=11.9||enemies.some(e=>cb112Live(e)&&e._cb112&&e._cb112.age<64));}
function cb112Flow(B,f,x,y,size,t){if(!B)return;ctx.save();ctx.globalCompositeOperation='lighter';v31Blit(B,f,Math.PI/2+Math.floor(t*24)%4*TAU/4,x,y,size,null,.45+.4*pxgStep(.5+.5*Math.sin(t*8)));ctx.restore();}
function cb112FlightWarnings(e){const q=e._cb112,north=q.phase==='flight-warn-n',M=s911M(e),k=cb112Scale(e),ports=M.flightPalms[north?4:0],origin=north?VH+160:viewTopY()-160,dy=610/60*(north?-1:1),edge=north?VH-40:PLAY.y+40,first=Math.floor((edge-origin)/dy)+1,interval=turretInterval15(.30);q.warnLanes=[];
 cb112Warn(e,q.lane,north?VH:PLAY.y,north?-Math.PI/2:Math.PI/2,q.t/.85,65);
 // Forecast the same fixed60 Hz release ticks, including the offscreen entry
 // distance. This prevents accumulated half-frame errors in the side lanes.
 for(let n=0;n<5;n++){const tick=first+Math.ceil(n*interval*60-1e-7),y=origin+dy*tick,x0=q.lane+Math.sin(tick/60*7)*4;if(y<PLAY.y+40||y>VH-40)continue;ports.forEach((p,i)=>{const x=x0+(p[0]-128)*k,yy=y+(p[1]-128)*k;if(yy<PLAY.y+15||yy>VH-15)return;const angle=i?0:Math.PI,len=i?camRightX()-x+30:x-camLeftX()+30;cb112Warn(e,x,yy,angle,q.t/.85,110,len);q.warnLanes.push({x,y:yy,angle,width:110});});}
}
s911Draw=function(e){if(!cb112Own(e))return CB112.base.draw.apply(this,arguments);const q=e._cb112;if(!q)return CB112.base.draw(e);const v=cb112Visual(e)[0],hit=e.flash>0?hitFlashColor(e):null,dying=e._dyingT!=null;
 v31Blit(v.B,v.f,v.angle,e.x,e.y,v.B.cell*v.scale,hit);if(!hit&&!dying)cb112Flow(v.flow,v.f,e.x,e.y,v.B.cell*v.scale,q.age);
 const ports=s911Guns(e);if(!dying&&['grenade-charge','grenades','tidal-charge','tidal','depth-charge'].includes(q.phase)){
  const both=/tidal|depth/.test(q.phase),n=Math.floor(q.t/(q.interval||.44)),chosen=n%2?0:1;
  ports.forEach((p,i)=>{if(!both&&i!==chosen)return;const cycle=q.t/1.25%1,u=q.phase==='grenades'?q.t/q.interval%1:q.phase==='tidal'?clamp(cycle/.5,0,1):clamp(q.t/.8,0,1);if(q.phase==='grenades'&&u>.65||q.phase==='tidal'&&cycle>.62)return;const size=(10+22*(q.phase==='grenades'?Math.min(1,u/.55):u))*q.scale;v31Blit(S911_ART.banks.water_grenade,0,Math.PI/2+q.age*TAU*1.5,p.x,p.y,size);});
 }
 if(!dying){if(q.phase==='flight-warn-n'||q.phase==='flight-warn-s')cb112FlightWarnings(e);
 if(q.phase==='tidal-charge')ports.forEach(p=>cb112Warn(e,p.x,p.y,Math.PI/2,q.t/.95,150));}
 e._s911Rendered={model:'current',phase:q.phase,pose:v.f,view:v.view,dir:v31Dir(v.angle,v.B.dirs),heading:e._s911.head,parts:1,depth:q.scale,key:v.B.key};
};
s911Projectile=function(b){if(b?._cb112Roller){const F=b._cb112Roller;v31Blit(CB112_ART.banks.roller,Math.floor(F.t*32)%16,Math.PI/2,b.x,b.y,F.size,b.flash>0?'#fff':null);cb112Flow(CB112_ART.banks.roller_flow,Math.floor(F.t*32)%16,b.x,b.y,F.size,F.t);return true;}
 if(b?._cb112Wave){const t=efxClock-b._cb112Wave.born,size=b._cb112Wave.side?105:180;return v31Blit(CB112_ART.banks.wave,Math.floor(t*32)%32,Math.atan2(b.vy,b.vx),b.x,b.y,size*Math.min(1,.25+t*2.5));}
 return CB112.base.shot.apply(this,arguments);};
drawNavalFlashes=(()=>{const base=drawNavalFlashes;return function(){const r=base.apply(this,arguments);for(const f of CB112.fx)v31Blit(S911_ART.banks.water_splash,Math.min(7,Math.floor(f.t/f.life*8)),Math.PI/2,f.x,f.y,f.size);
 for(const F of CB112.balls)if(F.returning&&!F.done){v31Blit(CB112_ART.banks.roller,Math.floor(F.t*32)%16,Math.PI/2,F.x,F.y,F.size);cb112Flow(CB112_ART.banks.roller_flow,Math.floor(F.t*32)%16,F.x,F.y,F.size,F.t);}return r;};})();
drawBG=function(){const r=CB112.base.bg.apply(this,arguments);const dark=Math.max(0,...enemies.filter(cb112Live).map(e=>e._cb112?.dark||0));if(dark>0){ctx.save();ctx.fillStyle='rgba(0,3,13,'+dark+')';ctx.fillRect(camLeftX(),viewTopY(),viewW(),VH-viewTopY());ctx.restore();}return r;};
enemyOrdnanceCanIntercept=function(b){return b?._cb112Roller?false:CB112.base.intercept.apply(this,arguments);};
ordnanceBreak1002=function(b){if(b?._cb112Roller){const F=b._cb112Roller;if(!F.done&&!F.returning){F.done=true;cb112Splash(F.e,b.x,b.y,100);}return;}return CB112.base.break.apply(this,arguments);};
_lockTargets=function(){const list=CB112.base.targets.apply(this,arguments);for(const F of CB112.balls)if(!F.done&&!F.returning&&F.q&&!F.q.dead){const b=F.q;F.target=F.target||retinaDynamicPiece(b,'cb112-roller-'+F.id,'Counterable water roller',()=>({x:b.x,y:b.y,hp:1,dead:F.done||!!F.returning||b.dead}),(d,shot)=>cb112Weapon(F,shot),58,58);F.target.w=F.target.h=F.size*.8;list.push(F.target);}return list;};
s911Cancel=function(e){const r=CB112.base.cancel.apply(this,arguments);if(cb112Own(e)){for(const b of eBullets)if(b._s911Owner===e)b.dead=true;for(const F of CB112.balls)if(F.e===e){F.done=true;if(F.q)F.q.dead=true;}}return r;};
updatePlay=function(dt){const at=stageTimer,hold=run.stage===9&&!run._gp4StageX&&!subBossDone&&!subBossTriggered&&!subBossActive&&warnT<=0&&stageTimer>=curStage.length*(SUBBOSS[9]?.at||.45)&&currentBreakerPending112();cb112Intercept(dt);const r=CB112.base.play.apply(this,arguments);if(hold&&stageTimer>at)stageTimer=at;cb112Effects(dt);return r;};
stageLoadBegin=function(n,keys){return CB112.base.load.call(this,n,n===9?[...(keys||[]),...Object.values(CB112_ART.banks).map(b=>b.key)]:keys);};
beginStage=function(){CB112.balls=[];CB112.fx=[];CB112.events=[];CB112.planned=CB112.dispatched=false;return CB112.base.begin.apply(this,arguments);};
spawnEnemy=function(){const e=CB112.base.spawn.apply(this,arguments);if(cb112Live(e)){CB112.dispatched=true;cb112Init(e);}return e;};
buildStagePlan=function(stage){const plan=CB112.base.plan.apply(this,arguments);if(stage!==9||run._gp4StageX)return plan;
 const wave=plan.find(w=>Math.abs(w.t-12.05)<.001&&String(w.fn).includes('cbreak'));if(wave){CB112.planned=true;wave._currentBreaker112=true;const native=wave.fn;wave.fn=function(){const r=native.apply(this,arguments);if(!CB112.dispatched){if(waveIdx>0)waveIdx--;_waveGap=.25;}return r;};}return plan;};
globalThis.BOF_CURRENT_BREAKER_1102={state:CB112,art:CB112_ART,weapon:cb112Weapon,pending:currentBreakerPending112};
