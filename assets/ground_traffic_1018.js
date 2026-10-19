"use strict";
/* Full authored hulls reserve ground traffic space at birth and after movement.
   Crowded vehicles wait upstream; their weapons keep their native clocks. */
const GT18={serial:0,gap:12,resolving:false,stats:{reserved:0,queued:0,blocked:0},base:{
 spawn:spawnEnemy,separate:enemySeparate,drive:tankDriveStep,play:updatePlay,begin:beginStage}};
function groundTrafficVehicle(e){return !!e&&!e.dead&&e._dyingT==null&&!e.prop&&!e._prop&&!e._boss&&!e._amini&&!e._modTurret&&
 !!(e._tank||e._modTank||e._vkind==='tank'||/tank|crawler|halftrack|apc/i.test(e.type||''));}
function groundTrafficFootprint(e){
 if(e._modTank===4){const w=e.w*1.26;return{w:Math.max(e.w,w*1.04),h:Math.max(e.h,w*144/128)};}
 return{w:Math.max(e.w||24,e._drawW||0),h:Math.max(e.h||24,e._drawH||0)};
}
function groundTrafficTouch(a,b,ax=a.x,ay=a.y){const A=groundTrafficFootprint(a),B=groundTrafficFootprint(b);
 return Math.abs(ax-b.x)<(A.w+B.w)/2+GT18.gap-.01&&Math.abs(ay-b.y)<(A.h+B.h)/2+GT18.gap-.01;}
function groundTrafficLegal(e,x,y){const W=worldWidth(),F=groundTrafficFootprint(e);
 if(x<F.w*.35+6||x>W-F.w*.35-6)return false;
 if(typeof tankDrivable!=='function')return true;
 const sy=levelSrcY()+y,open=run.stage===4;
 if(!tankDrivable(x,sy,open))return false;
 return run.stage!==4||[-1,1].every(s=>tankDrivable(x+s*F.w*.35,sy,open));
}
function groundTrafficSet(e,x,y){const dx=x-e.x,dy=y-e.y;e.x=x;e.y=y;
 if(e._lvlY!=null)e._lvlY+=dy;else e._lvlY=levelSrcY()+y;
 for(const key of ['_tankLane','_fixedX','_lane','_apX0','_apX1'])if(e[key]!=null)e[key]+=dx;
 if(y<viewTopY())e._tankQueueY=Math.min(e._tankQueueY??Infinity,y-groundTrafficFootprint(e).h);
}
function groundTrafficCanPlace(x,y,w,h,self){const candidate={x,y,w,h};
 return !enemies.some(e=>e!==self&&groundTrafficVehicle(e)&&groundTrafficTouch(candidate,e));}
function groundTrafficReserve(e,settled){const F=groundTrafficFootprint(e);let y=e.y;
 for(let pass=0;pass<settled.length+2;pass++){
  const contacts=settled.filter(o=>groundTrafficTouch(e,o,e.x,y));if(!contacts.length)break;
  y=Math.min(...contacts.map(o=>o.y-(F.h+groundTrafficFootprint(o).h)/2-GT18.gap-.25));
 }
 if(Math.abs(y-e.y)<.01)return;
 let legal=null;
 for(let n=0;n<=1536;n+=8){const yy=y-n;
  if(groundTrafficLegal(e,e.x,yy)&&!settled.some(o=>groundTrafficTouch(e,o,e.x,yy))){legal=yy;break;}}
 if(legal==null)legal=Math.min(y,viewTopY()-F.h-80);
 groundTrafficSet(e,e.x,legal);GT18.stats.queued++;
}
function groundTrafficResolve(){if(GT18.resolving||window.__sepOff)return;
 GT18.resolving=true;try{
  const list=enemies.filter(groundTrafficVehicle);
  for(const e of list)if(e._traffic18==null)e._traffic18=++GT18.serial;
  list.sort((a,b)=>b.y-a.y||a._traffic18-b._traffic18);
  const settled=[];for(const e of list){groundTrafficReserve(e,settled);settled.push(e);}
 }finally{GT18.resolving=false;}}
spawnEnemy=function(){const start=enemies.length,r=GT18.base.spawn.apply(this,arguments);
 const newcomers=enemies.slice(start).filter(groundTrafficVehicle);
 for(const e of newcomers){e._traffic18=++GT18.serial;GT18.stats.reserved++;
  groundTrafficReserve(e,enemies.filter(o=>o!==e&&groundTrafficVehicle(o)&&!newcomers.includes(o)));
 }groundTrafficResolve();return r;};
tankDriveStep=function(e){if(!groundTrafficVehicle(e))return GT18.base.drive.apply(this,arguments);
 const before={x:e.x,y:e.y,row:e._lvlY},clear=!enemies.some(o=>o!==e&&groundTrafficVehicle(o)&&groundTrafficTouch(e,o));
 const result=GT18.base.drive.apply(this,arguments);
 if(clear&&enemies.some(o=>o!==e&&groundTrafficVehicle(o)&&groundTrafficTouch(e,o))){
  e.x=before.x;e.y=before.y;e._lvlY=before.row;e.vx=0;e._trafficBusy=true;
  if(e._phase==='drive')e._phase='brake';GT18.stats.blocked++;return false;
 }e._trafficBusy=false;return result;};
enemySeparate=function(){const r=GT18.base.separate.apply(this,arguments);groundTrafficResolve();return r;};
updatePlay=function(){const r=GT18.base.play.apply(this,arguments);if(state===GS.PLAY)groundTrafficResolve();return r;};
beginStage=function(){GT18.serial=0;GT18.stats={reserved:0,queued:0,blocked:0};return GT18.base.begin.apply(this,arguments);};
window.BOF_GROUND_TRAFFIC={vehicle:groundTrafficVehicle,footprint:groundTrafficFootprint,
 overlap:groundTrafficTouch,canPlace:groundTrafficCanPlace,resolve:groundTrafficResolve,state:GT18};
