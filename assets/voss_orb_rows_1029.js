'use strict';
/* Voss twin cannon: parallel rows, faster travel and authored spin/1015 light. */
const OR44={base:{release:vs41Release,warning:rg4Warning,ord:rg4OrdnanceDraw,load:stageLoadBegin},events:[],serial:0,rows:0,rounds:0};
XART._src.or44_orbs='assets/game/levels/stage_06/boss/voss_orb_rows_1029/orb_rows.png';
stageLoadBegin=function(n,keys){return OR44.base.load.call(this,n,n===6?[...(keys||[]),'or44_orbs']:keys);};
function or44Own(q){return q?.key==='voss'&&run.stage===6&&!run._gp4StageX&&boss?._rebels&&!boss._rebels.frStageX&&boss._rebels.ships.includes(q);}
function or44Angle(){return Math.PI/2;}
function or44Log(event,data={}){OR44.events.push({event,time:efxClock,...data});if(OR44.events.length>500)OR44.events.shift();}
vs41Release=function(q,G,A){if(!or44Own(q))return OR44.base.release.apply(this,arguments);
 const row=++OR44.serial,a=or44Angle(q,A),vx=0,vy=240;let count=0;
 for(const side of[-1,1]){const p=vs41Cannon(q,side);if(!p)continue;
  const o=rr26Energy(q,G,a,false,p.x,p.y);Object.assign(o,{_vs41Side:side,_or44:true,_or44Row:row,_or44Side:side,
   _or44Origin:{x:p.x,y:p.y},_or44Velocity:{x:vx,y:vy},r:13,vx,vy,life:4.5});
  wm26Emit(q,p.x,p.y,a,'orb','#ff5039',{size:30,life:.11,follow:()=>vs41Active(q)?vs41Cannon(q,side):null});
  count++;OR44.rounds++;or44Log('orb',{row,side,x:p.x,y:p.y,vx,vy});
 }
 if(count){OR44.rows++;combatAudio0927(q,'enemyBossCannon',.18);}vs41Log('twin-cannon',{count,round:A.round});
};
rg4Warning=function(q,A){if(!or44Own(q)||!A?._vs41||A.phase!=='charge')return OR44.base.warning.apply(this,arguments);
 const a=or44Angle(q,A);for(const side of[-1,1]){const p=vs41Cannon(q,side);if(p)rd21Fov(A,p.x,p.y,a,26,A.t/A.warm);}
};
rg4OrdnanceDraw=function(o,G){if(!o?._or44)return OR44.base.ord.apply(this,arguments);if(!XART.rdy('or44_orbs'))return;
 const f=Math.floor((o.t||0)*24)%32+(o.flash>0?32:0);ctx.drawImage(XART.get('or44_orbs'),f%8*48,Math.floor(f/8)*48,48,48,Math.round(o.x)-24,Math.round(o.y)-24,48,48);
};
globalThis.BOF_ORB_ROWS_1029=OR44;
