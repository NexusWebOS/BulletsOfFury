"use strict";
/* Committed native attacks, active space formations and readable Normal skies. */
const AP10_FLEET={space:s5SpaceTick,sky:s6OnslaughtTick,wing:s6WingTick,
 cannon:whvCannonTick,carrier:whvDrawCarrier,shield:drawShield,play:updatePlay,events:[]};
updatePlay=function(dt){
 if(run.stage===6&&!fb2TalkActive()&&!h3RebelIntro()&&!s6OpeningActive())H3.release=false;
 return AP10_FLEET.play.apply(this,arguments);};
s5SpaceTick=function(e,dt){
 const prev=e._s5Act,r=AP10_FLEET.space.apply(this,arguments),K=e._s5space;
 if(e.dead||e._dyingT!=null)return r;
 if(['s5frigate','s5gravity','s5station','s5satellite','s5minelayer'].includes(K)&&e.y>=VH*.17){
  const Q=e._ap10Flight||(e._ap10Flight={x:clamp(e.x,camLeftX()+90,camRightX()-90),t:0});Q.t+=dt;
  const amp=K==='s5station'?90:K==='s5frigate'?62:45;
  e.x=clamp(Q.x+Math.sin(Q.t*1.1+(e.phase||0))*amp,camLeftX()+e.w/2+10,camRightX()-e.w/2-10);
  e.y=VH*.24+Math.sin(Q.t*1.45+(e.phase||0))*34;
 }
 if(!prev&&e._s5Act){AP10_FLEET.events.push({event:'space-attack',type:K});
  if(AP10_FLEET.events.length>160)AP10_FLEET.events.shift();
  e._fcd=Math.max(.85,(e._fcd||1)*(diffKey==='easy'?1:diffKey==='normal'?.82:.74));}
 return r;
};
s6OnslaughtTick=function(W,dt){
 W.combatTime=(W.combatTime||0)+dt;
 if(bossActive||subBossActive||s6OpeningActive()||W.choice||W.fake||run._gp4StageX)return;
 W.reinforce=(W.reinforce||0)-dt;const n=diffKey==='furious'?2:diffKey==='hard'?1:0;
 const cap=diffKey==='easy'?2:[3,4,5][n],live=enemies.filter(e=>!e.dead&&e._dyingT==null&&!e.prop&&!e._prop).length;
 if(W.reinforce<=0&&live<cap){W.reinforce=diffKey==='easy'?8:[5.5,4.7,4][n];
  const i=W.reinforceSerial=(W.reinforceSerial||0)+1;
  spawnEnemy(i%3===0?'s6bomber':'s6dart',camLeftX()+45+((i*.618)%1)*(viewW()-90),-75,{});
 }
};
s6WingTick=function(dt){const r=AP10_FLEET.wing.apply(this,arguments),W=s6Wing;
 if(W&&!W._ap10EarlyWing&&stageTimer>=14&&!subBossActive&&!bossActive&&!s6OpeningActive()&&!run._gp4StageX){
  // The native random launch draws from nine pilots before GP4 keeps its five-
  // ship roster. Launch the authored roster, then filter, so no ally is lost.
  W._ap10EarlyWing=true;s6WingLaunch(4,true);
 }return r;};
const AP10_FLEET_JET=jetTick;
jetTick=function(e,dt){const y=e.y,r=AP10_FLEET_JET.apply(this,arguments);
 if(run.stage===6&&!s6OpeningActive()&&AP10_AIR_TYPES.has(e.type)&&!e._mission29&&!e._fb2Stealth&&!e.dead&&e.y>y)
  e.y+=(e.y-y)*(diffKey==='easy'?.08:diffKey==='normal'?.18:.12);
 return r;};
whvCannonTick=function(b,dt){const W=b._whv,normal=!W.hard;
 const before=W.can?.seq,beam=W.beam;let r;
 if(normal){W.hard=true;try{r=AP10_FLEET.cannon.call(this,b,dt*.80);}finally{W.hard=false;}}
 else r=AP10_FLEET.cannon.apply(this,arguments);
 if(!before&&W.can?.seq){const S=W.can.seq;S.ap10Warm=.70;
  for(const s of S.shots)s.at+=S.ap10Warm;
 }
 if(W.can?.seq){const S=W.can.seq;combatWarningTick(b,'ap10-harrier-'+S.side,Math.min(S.t,.7),.7);}
 if(normal&&!beam&&W.beam){W.beam.w=VW/6;W.beam.warn=1.65;W.beam.fire=1.05;}
 return r;
};
whvDrawCarrier=function(b){const r=AP10_FLEET.carrier.apply(this,arguments),S=b._whv?.can?.seq;
 if(S?.ap10Warm&&S.t<S.ap10Warm){const q=whvPartPos(b,S.side);
  combatWarningDraw(b,{x:q.x,y:q.y+14,ex:player.x,ey:player.y,width:54,progress:S.t/S.ap10Warm});
 }return r;};
// Match the personal shield to the current hull, including the space hull.
drawShield=function(x,y){if(!(run.shield>0))return;
 const space=spaceShipActive(),im=space?furyShipCanvas('base',_pilotKey()):XART.rdy('ship_'+_pilotKey())?XART.get('ship_'+_pilotKey()):null;
 if(!im)return AP10_FLEET.shield.apply(this,arguments);
 const h=space?SPACE_SHIP_SIZE:SHIP_DRAW_H,w=h*im.width/im.height;
 ctx.save();ctx.globalAlpha=.62+.06*Math.min(5,run.shield);
 repair30Cell('shield',efxClock,x,y,w*1.08,h*1.10,true);ctx.restore();
};
