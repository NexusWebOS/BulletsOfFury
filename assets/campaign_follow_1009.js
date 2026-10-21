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
   - The boot sequence now stays close for the HQ approach. Stage X / Rebel
     cinematics, rift return and progression-bar overview keep their cameras. */
const CF9={base:{cam:cmap2CameraTick,ship:sselShipUpdate,reset:cmap2Reset},
 lead:.35,                      // camera leads from the jet toward its destination
 zoom:()=>Math.min(1.65,(CM2_BAND_BOT-CM2_BAND_TOP)/(cmap2Size(sselUnlockCine?.stage||sselCursor)*.25)),
 detail:0,cineHold:0};

// Markers used to cancel out camera zoom entirely. Give the selected flag
// enough pixels for its Roman numeral while the actual pilot hull stays clear.
function cf9FlagHeight(st){return 28+(st===(sselUnlockCine?.stage||sselCursor)?44*CF9.detail:0);}
function cf9ShipSize(){return 40+28*CF9.detail;}

function cf9Fresh(){const r=campaign.rank||{};
 return !Object.keys(r).some(k=>r[k]&&r[k]!=='incomplete');}
// Where the jet is heading now: the new flag during an unlock cinematic, else the cursor's flag.
function cf9Dest(){const cine=sselUnlockCine;
 return cine&&!cine.done?sselFlagXY(cine.stage):sselFlagXY(sselCursor);}
function cf9Standard(){
 return !(s9MapCine||riftReturn||Rival24.flying||Rival24.mapFocused||MAP4E.xPreview||
  cmap2.focus==='bar'||(typeof map4hXFocused==='function'&&map4hXFocused()));
}

function cf9ShipTick(dt){
 if(!cf9Standard())return CF9.base.ship.apply(this,arguments);
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
}
sselShipUpdate=function(dt){
 if(CF9.shipEarly){CF9.shipEarly=false;return;}
 return cf9ShipTick(dt);
};

cmap2CameraTick=function(dt,cine,selected){
 const close=cf9Standard();CF9.detail+=((close?1:0)-CF9.detail)*(1-Math.exp(-Math.max(0,dt)*6));
 // Native map drawing updates the jet after applying its camera. Step it
 // once before the camera instead, so both use the same visible position.
 CF9.shipEarly=false;if(close){cf9ShipTick(dt);CF9.shipEarly=true;}
 if(!close||!sselShip)return CF9.base.cam.apply(this,arguments);
 map4eWarm();
 const sh=sselShip,dest=cf9Dest()||sh,z=CF9.zoom();
 const leadX=clamp((dest.x-sh.x)*CF9.lead,-VW*.22/z,VW*.22/z),
  leadY=clamp((dest.y-sh.y)*CF9.lead,-(CM2_BAND_BOT-CM2_BAND_TOP)*.30/z,(CM2_BAND_BOT-CM2_BAND_TOP)*.30/z);
 const t=cmap2Clamp({x:sh.x+leadX,y:sh.y+leadY-12/z},z),c=cmap2.cam;
 const kp=1-Math.exp(-Math.max(0,dt)*(sh.moving?12:10)),kz=1-Math.exp(-Math.max(0,dt)*4);
 c.x+=(t.x-c.x)*kp;c.y+=(t.y-c.y)*kp;c.z+=(z-c.z)*kz;
 // A close camera cannot lag a fast north/south hop behind the briefing or
 // top bar. Bound the full visible hull after easing, while retaining lead.
 const pad=cf9ShipSize()/2+4;
 c.y=clamp(c.y,sh.y-(CM2_BAND_BOT-pad-CM2_VCY)/c.z,sh.y-(CM2_BAND_TOP+pad-CM2_VCY)/c.z);
 c.x=clamp(c.x,sh.x-(VW+campaignViewOffset()-pad-CM2_VCX)/c.z,
  sh.x-(-campaignViewOffset()+pad-CM2_VCX)/c.z);
};

// Returning from a stage opens already zoomed in on the cursor's flag, where the jet will be.
cmap2Reset=function(opts){const r=CF9.base.reset.apply(this,arguments);
 CF9.detail=cf9Standard()?1:0;
 if(cf9Standard()){const p=opts?.boot&&cf9Fresh()?cmap2World('hq'):sselFlagXY(sselCursor),z=CF9.zoom();
  if(p){const t=cmap2Clamp({x:p.x,y:p.y-12/z},z);Object.assign(cmap2.cam,{x:t.x,y:t.y,z});}}
 return r;};
