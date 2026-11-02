"use strict";
/* 1101 (Mike: "stage 9, begin balancing and fixing the fov's and direction of firing"). Late layer over S911
   (stage9_amplify_1101.js); that owner keeps every actor, attack book, beam, hazard, HP and death.
   Measured before this layer (probe_s9_fov_1101.py, Furious): gun attacks - bursts, water fans, gravity orbs, radial
   and nine-orb volleys - ran their tell with no FOV lane at all (S911 only draws lanes for beams and dashes); flying
   types kept re-aiming during the volley so rounds left away from the committed direction; the Gravity Leech fired
   12 rounds while never on screen; the Comet fired on its first visible frame; the Gate Turret's four-port water fan
   put out 13 rounds/s, double anything else on the stage. */
const S9F={events:[],base:{tick:s911Tick,shot:s911Shot,mounts:s911Mounts,draw:drawEnemy}};
const S9F_GUN=new Set(['burst','water-fan','gravity-orbs']),S9F_RADIAL=new Set(['radial','nine-orbs']);
// Densest fodder (measured 7.9 / 7.6 rounds/s on Furious): their volley beat is stretched.
const S9F_CADENCE={skimmer:1.3,manta:1.3};
function s9fLog(e,event,data={}){S9F.events.push({type:e?.type,model:e?._s911?.model,event,t:efxClock,...data});if(S9F.events.length>1200)S9F.events.shift();}
function s9fOnScreen(e){const y=e._drawY??e.y;return e.x>camLeftX()+6&&e.x<camRightX()-6&&y>viewTopY()+6&&y<VH-6;}
// The lanes a gun attack will fire along: each gun mouth, three per mouth for the water fan, spokes for radial books.
function s9fLanes(e){const A=e._s911,M=s911M(e),atk=A.attack;
 if(S9F_RADIAL.has(atk)){const p=s911Point(e,M.core),n=atk==='nine-orbs'?9:Math.max(6,s911Guns(e).length);return Array.from({length:n},(_,i)=>({x:p.x,y:p.y,angle:A.head+i*TAU/n,width:12,len:170}));}
 const out=[];for(const p of s911Guns(e))for(const o of atk==='water-fan'?[-.19,0,.19]:[0])out.push({x:p.x,y:p.y,angle:p.angle+o,width:atk==='water-fan'?14:18,len:1000});return out;}
s911Tick=function(e,dt){const A=e?._s911;if(!A)return S9F.base.tick.apply(this,arguments);
 // A tell never runs out while the unit is off-screen, so nothing attacks from where the player cannot see it.
 if(A.phase==='tell'&&!s9fOnScreen(e)&&A.t>A.warm*.3){A.t=A.warm*.3;if(!A.s9fHeld){A.s9fHeld=1;s9fLog(e,'tell-held-offscreen');}}
 if(A.phase==='pass'&&s9fOnScreen(e))A.s9fPass=(A.s9fPass||0)+dt;
 const was=A.committed,beat0=A.beat,r=S9F.base.tick.apply(this,arguments);
 if((A.phase==='fire'||A.phase==='dash')&&S9F_CADENCE[A.model]&&A.beat>beat0+1e-6)A.beat*=S9F_CADENCE[A.model];
 if(A.phase==='tell'&&!was&&A.committed&&S9F_GUN.has(A.attack)){A.s9fLock=A.angles.slice();A.s9fHead=A.head;s9fLog(e,'lock',{attack:A.attack});}
 if(A.phase!=='tell'&&A.phase!=='fire')A.s9fLock=A.s9fHead=null;
 return r;};
// Rounds leave along the committed lanes: the guns keep the angles they held when the warning committed.
// During a dash the guns face along the dash itself (the lane its warning drew), instead of keeping a stale angle.
s911Mounts=function(e,dt,track){const r=S9F.base.mounts.apply(this,arguments),A=e?._s911;
 if(A&&A.phase==='fire'&&A.s9fLock&&S9F_GUN.has(A.attack))A.angles=A.s9fLock.slice();
 else if(A&&A.phase==='dash'&&Array.isArray(A.angles))A.angles=A.angles.map(()=>A.head);
 return r;};
s911Shot=function(e,p){const A=e?._s911;
 if(A&&s911Live(e)){
  if(!s9fOnScreen(e)){s9fLog(e,'refused-offscreen');return null;}
  if(A.phase==='pass'&&(A.s9fPass||0)<.55)return null;
  // Gate Turret water fan: its four corner guns alternate in pairs (was four ports x three rounds every beat).
  if(A.model==='gate'&&A.phase==='fire'&&A.attack==='water-fan'&&((p?.index|0)%2)!==(A.round%2))return null;
 }
 // Fixed-gun hulls (no articulated modules) fire along their nose; while they weave during the volley the round keeps
 // its offset from the nose but uses the heading committed with the warning.
 if(A&&A.phase==='fire'&&A.s9fHead!=null&&S9F_GUN.has(A.attack)&&!s911M(e).modules.length&&p&&Number.isFinite(p.angle)){
  const args=[...arguments];args[1]={...p,angle:A.s9fHead+s1aAngle(p.angle-A.head)};return S9F.base.shot.apply(this,args);}
 return S9F.base.shot.apply(this,arguments);};
drawEnemy=function(e){const r=S9F.base.draw.apply(this,arguments),A=e?._s911;
 if(A&&!e.dead&&e._dyingT==null&&!A.cancelled){
  let lanes=null,progress=0;
  if(A.phase==='tell'&&(S9F_GUN.has(A.attack)||S9F_RADIAL.has(A.attack))){lanes=s9fLanes(e);progress=clamp(A.t/A.warm,0,1);}
  // Spinners keep turning between radial volleys: faint spokes show where the NEXT volley will leave.
  else if(A.phase==='fire'&&S9F_RADIAL.has(A.attack)&&A.beat>0){const spin=S911.defs[A.model]?.spin?1.9*A.beat:0,h0=A.head;A.head=h0+spin;try{lanes=s9fLanes(e).map(p=>({...p,width:8,len:140}));}finally{A.head=h0;}progress=clamp(1-A.beat/.6,0,1)*.7;}
  else if(A.phase==='pass'&&(A.s9fPass||0)<.55&&s9fOnScreen(e)){lanes=s911Guns(e).map(p=>({...p,width:16,len:1000}));progress=clamp((A.s9fPass||0)/.55,0,1);}
  if(lanes)for(const p of lanes)combatWarningDraw(e,{x:p.x,y:p.y,ex:p.x+Math.cos(p.angle)*p.len,ey:p.y+Math.sin(p.angle)*p.len,width:p.width,progress,fieldOnly:true});
 }
 return r;};
globalThis.BOF_STAGE9_FOV=S9F;
