'use strict';
/* October 9: the campaign map flies with the pilot.

   Mike: zoom in toward the levels. On a new campaign the jet leaves Fury HQ for Stage 1 with the
   camera practically on Stage 1, jet and flag both in view. After a clear the camera stays zoomed
   in and follows the jet to the next stage.

   - The jet starts at Fury HQ until a stage has been cleared, then it starts at the cursor's flag.
     It never flies in from off the left edge any more.
   - During an unlock cinematic the jet flies to the new flag first. The cinematic holds in 'wait'
     until the jet arrives, so the ding and unfurl happen in view with the jet beside the flag.
   - The camera follows the jet, leading toward its destination, at a close zoom.
   - The boot sequence, Stage X / Rebel framing, the bonus stage, the rift return and the
     progression-bar overview keep their existing cameras. */
const CF9={base:{cam:cmap2CameraTick,ship:sselShipUpdate,reset:cmap2Reset},
 lead:.35,                      // camera leads from the jet toward its destination
 zoom:()=>Math.min(.62,(CM2_BAND_BOT-CM2_BAND_TOP)/(cmap2Size(1)*.66)),
 cineHold:0};

function cf9Fresh(){const r=campaign.rank||{};
 return !Object.keys(r).some(k=>r[k]&&r[k]!=='incomplete');}
// Where the jet is heading now: the new flag during an unlock cinematic, else the cursor's flag.
function cf9Dest(){const cine=sselUnlockCine;
 return cine&&!cine.done?sselFlagXY(cine.stage):sselFlagXY(sselCursor);}
function cf9Standard(){
 return !(sselBoot>0||s9MapCine||riftReturn||Rival24.flying||Rival24.mapFocused||MAP4E.xPreview||
  cmap2.focus==='bar'||sselCursor===9||(typeof map4hXFocused==='function'&&map4hXFocused())||
  Rival24.mapAvailable&&[6,7].includes(sselCursor)&&!sselUnlockCine);
}

sselShipUpdate=function(dt){
 if(sselBoot>0||!cf9Standard())return CF9.base.ship.apply(this,arguments);
 const cine=sselUnlockCine,dest=cf9Dest();if(!dest)return CF9.base.ship.apply(this,arguments);
 if(!sselShip){
  const hq=cf9Fresh()?cmap2World('hq'):null,from=hq?{x:hq.x,y:hq.y+40}:dest;
  sselShip={x:from.x,y:from.y,tx:dest.x,ty:dest.y,t:0,phase:hq?'flyin':'idle',bank:0,trail:0,
   cur:cine?cine.stage:sselCursor,head:map4eShipHeading(null,1,dest.x-from.x),face:1,cf9:true};
 }
 const sh=sselShip,target=cine?cine.stage:sselCursor;sh.t+=dt;
 if(sh.cur!==target){sh.head=map4eShipHeading(sh.cur,target,dest.x-sh.x);
  if(sh.cur!=null&&Audio.SFX.mapMove)Audio.SFX.mapMove();sh.cur=target;}
 if(!Number.isFinite(sh.head))sh.head=Math.PI/2;
 sh.face=sh.head<0?-1:1;sh.tx=dest.x;sh.ty=dest.y;
 // A slower glide than menu hops so the flight reads as travel, not a cursor jump.
 const dx=dest.x-sh.x,dy=dest.y-sh.y,d=Math.hypot(dx,dy),k=sh.phase==='flyin'||cine?.035:.07;
 sh.x+=dx*Math.min(1,dt*60*k);sh.y+=dy*Math.min(1,dt*60*k);sh.bank=0;
 if(sh.phase==='flyin'&&d<4)sh.phase='idle';sh.moving=d>3;sh.trail-=dt;
 if(sh.moving&&sh.trail<=0){sh.trail=.03;const ux=Math.sin(sh.head),uy=-Math.cos(sh.head);
  particles.push({x:sh.x-ux*17,y:sh.y-uy*17,vx:-ux*.35+rnd(-.2,.2),vy:-uy*.35+rnd(-.2,.2),
   life:rnd(.18,.36),t:0,r:rnd(1,2.2),color:d>90?'#ffd27a':'#8fd0ff'});}
 // Hold the unlock cinematic until the jet has reached the new flag.
 if(cine&&(cine.phase==null||cine.phase==='wait')&&d>8)cine.t=0;
};

cmap2CameraTick=function(dt,cine,selected){
 if(!cf9Standard()||!sselShip)return CF9.base.cam.apply(this,arguments);
 map4eWarm();
 const sh=sselShip,dest=cf9Dest()||sh,z=CF9.zoom();
 const t=cmap2Clamp({x:lerp(sh.x,dest.x,CF9.lead),y:lerp(sh.y,dest.y,CF9.lead)-12/z},z),c=cmap2.cam;
 const kp=1-Math.exp(-Math.max(0,dt)*4.2),kz=1-Math.exp(-Math.max(0,dt)*2.2);
 c.x+=(t.x-c.x)*kp;c.y+=(t.y-c.y)*kp;c.z+=(z-c.z)*kz;
};

// Returning from a stage opens already zoomed in on the cursor's flag, where the jet will be.
cmap2Reset=function(opts){const r=CF9.base.reset.apply(this,arguments);
 if(!opts?.boot&&cf9Standard()){const p=sselFlagXY(sselCursor),z=CF9.zoom();
  if(p){const t=cmap2Clamp({x:p.x,y:p.y-12/z},z);Object.assign(cmap2.cam,{x:t.x,y:t.y,z});}}
 return r;};
