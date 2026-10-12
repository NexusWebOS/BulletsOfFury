"use strict";
/* Homecoming: original static pilot aircraft, selected pilot,
   physical walk into HQ. The camera never turns a top-down sprite upright. */
const HL10={base:{restoration:victoryRestoration,keys:victoryEndingKeys,load:stageLoadBegin,viewport:_setCinematicViewport,
 dish:victoryDish,card:victoryFinalCard},
 pilots:['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut'],
 times:{earth:3,coast:6,pad:9.4,exit:13.6,walk:16.6,entered:24,end:26.4},events:[],draws:{},last:null,transition:null,
 // Time, uniform zoom, focus X/Y in the authored scene. Follow the actual
 // cockpit/ladder/walking route, then hold the threshold while the doors close.
 cameraTrack:[[9.4,1,.5,.5],[11.08,1.15,.5,.60],[13.6,1.32,.52,.65],
  [16.6,1.56,.59,.71],[18.38,1.78,.625,.66],[20.60,2.18,.57,.565],
  [22.52,2.70,.50,.525],[24,3,.50,.49],[26.4,3,.50,.49]]};
for(const bank of Object.values(HL10_ART))for(const a of bank)XART._src[a.key]=a.path;
function hl10Pilot(pk){return HL10.pilots.includes(pk)?pk:'axel';}
function hl10Assets(pk=run.pilot){
 pk=hl10Pilot(pk);
 return [...HL10_ART.background,...hc10FlightAssets(pk),...HL10_ART.shadow,...HL10_ART.downwash,...HL10_ART.door,
  ...HL10_ART[pk+'_exit'],...HL10_ART[pk+'_walk']];
}
function hl10Warm(pk=run.pilot){
 let ready=true;for(const a of hl10Assets(pk))if(!XART.rdy(a.key))ready=false;
 return ready;
}
victoryEndingKeys=function(){return [...HL10.base.keys.apply(this,arguments),...hl10Assets().map(a=>a.key)];};
stageLoadBegin=function(n,keys){return HL10.base.load.call(this,n,[...(keys||[]),...(n>=7?hl10Assets().map(a=>a.key):[])]);};
_setCinematicViewport=function(on){
 const r=HL10.base.viewport.apply(this,arguments);
 if(on&&state===GS.VICTORY){
  CINEMA_VW=Math.max(1,Math.round(VH*window.innerWidth/Math.max(1,window.innerHeight)));
  if(cv.width!==CINEMA_VW*SS||cv.height!==VH*SS){cv.width=CINEMA_VW*SS;cv.height=VH*SS;}
  ctx.imageSmoothingEnabled=false;if(window.__bofFit)window.__bofFit();
 }return r;
};
function hl10Record(event,data={}){HL10.events.push({event,...data});if(HL10.events.length>180)HL10.events.shift();}
function hl10Sound(cue){
 const name={approach:'thruster',gear:'furyPartArrival',touchdown:'gravityLock',hatch:'furyPartArrival',door:'select',welcome:'blip'}[cue],fn=Audio.SFX?.[name];
 if(fn)fn(cue==='hatch'?1:0);hl10Record('sound',{cue,name,available:!!fn});
}
function hl10Cues(t,pk){
 let s=drawVictory._hl10;
 if(!s||s.pilot!==pk||t+1e-5<s.time)s=drawVictory._hl10={pilot:pk,time:-1,cues:new Set()};
 const schedule={approach:6.02,gear:9.48,touchdown:11.08,hatch:12.46,door:20.0,welcome:24.05};
 if(t>s.time)for(const [cue,at] of Object.entries(schedule))if(t>=at&&!s.cues.has(cue)){
  s.cues.add(cue);if(s.time>=0&&s.time<at&&t-s.time<.75)hl10Sound(cue);
 }
 s.time=t;
}
function hl10Ease(q){q=clamp(q,0,1);return q*q*(3-2*q);}
function hl10Camera(t){
 const keys=HL10.cameraTrack;
 let i=0;while(i<keys.length-2&&t>keys[i+1][0])i++;
 const a=keys[i],b=keys[i+1],span=b[0]-a[0],u=clamp((t-a[0])/span,0,1),v=u*u,w=v*u;
 // Monotone cubic tangents keep camera speed continuous between cues and
 // prevent overshoot or a reversal during the push toward the doorway.
 const slope=(j,k)=>{
  if(j===0||j===keys.length-1)return 0;
  const left=keys[j][0]-keys[j-1][0],right=keys[j+1][0]-keys[j][0],
   dl=(keys[j][k]-keys[j-1][k])/left,dr=(keys[j+1][k]-keys[j][k])/right;
  if(dl*dr<=0)return 0;
  const wl=2*right+left,wr=right+2*left;return (wl+wr)/(wl/dl+wr/dr);
 };
 const sample=k=>(2*w-3*v+1)*a[k]+(w-2*v+u)*span*slope(i,k)+
  (-2*w+3*v)*b[k]+(w-v)*span*slope(i+1,k);
 const zoom=sample(1),margin=.5/zoom;
 return {zoom,x:clamp(sample(2),margin,1-margin),y:clamp(sample(3),margin,1-margin)};
}
function hl10Fade(alpha,W,H){
 if(alpha<=0)return;
 ctx.save();ctx.globalAlpha=clamp(alpha,0,1);ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);ctx.restore();
}
function hl10Sample(t,pk='axel'){
 pk=hl10Pilot(pk);const T=HL10.times;
 const s={pilot:pk,t,phase:t<T.earth?'escape':t<T.coast?'earth':t<T.pad?'approach':t<T.exit?'landing':t<T.walk?'exit':t<T.entered?'walk':'inside',
  background:t<T.coast?Math.floor(t/T.earth):t<T.pad?0:1,shipFrame:0,actorFrame:null,actorClip:null,grounded:t>=T.pad+1.68,entered:t>=T.entered,doorFrame:0};
 if(s.phase==='exit'){s.actorClip='exit';s.actorFrame=Math.min(7,Math.floor((t-T.exit)/3*8));}
 if(s.phase==='walk'){s.actorClip='walk';s.actorFrame=Math.floor((t-T.walk)*12)%8;}
 if(t>=20&&t<24.55)s.doorFrame=Math.min(15,Math.floor((t-20)/1.1*16));
 else if(t>=24.55)s.doorFrame=Math.max(0,15-Math.floor((t-24.55)/1.1*16));
 return s;
}
function hl10Cell(bank,f,x,y,w){
 const list=HL10_ART[bank],a=list?.[clamp(f|0,0,list.length-1)];
 if(!a||!XART.rdy(a.key))return false;
 const k=w/a.w;ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 HL10.draws[a.key]=(HL10.draws[a.key]||0)+1;return true;
}
function hl10EnvironmentRect(bank,f,W,H){
 const a=HL10_ART[bank][f],k=Math.min(W/a.w,H*.72/a.h),R={x:(W-a.w*k)/2,y:8,w:a.w*k,h:a.h*k};
 return R;
}
function hl10BodyGeometry(pk){
 const cells=HL10_ART[pk+'_walk'];
 const median=values=>values.sort((a,b)=>a-b)[values.length>>1];
 return {height:median(cells.map(a=>a.opaque_bounds[3]-a.opaque_bounds[1])),foot:median(cells.map(a=>a.opaque_bounds[3]-a.pivot[1]))};
}
function hl10Actor(s,R){
 if(!s.actorClip||s.entered)return null;
 const T=HL10.times,q=s.phase==='exit'?(s.t-T.exit)/3:(s.t-T.walk)/(T.entered-T.walk),body=hl10BodyGeometry(s.pilot);
 let x,y,height,inside=false;
 if(s.phase==='exit'){
  // The upper cockpit and starboard ladder define the root trajectory. Art
  // supplies crouch/hand/foot articulation without a per-frame size fit.
  const d=hl10Ease(q);x=lerp(.570,.622,d);y=lerp(.780,.882,d);height=.080;
 }else{
  if(q<.24){const d=q/.24;x=lerp(.622,.659,d);y=lerp(.882,.655,d);height=lerp(.080,.071,d);}
  else if(q<.54){const d=(q-.24)/.30;x=lerp(.659,.590,d);y=lerp(.655,.562,d);height=lerp(.071,.061,d);}
  else if(q<.80){const d=(q-.54)/.26;x=lerp(.590,.500,d);y=lerp(.562,.551,d);height=lerp(.061,.055,d);}
  else{const d=(q-.80)/.20;inside=true;x=.500;y=lerp(.551,.505,d);height=lerp(.055,.012,d);}
 }
 const scale=height*R.h/body.height,foot={x:R.x+x*R.w,y:R.y+y*R.h};
 if(inside){ctx.save();ctx.beginPath();ctx.rect(R.x+R.w*.475,R.y+R.h*.425,R.w*.061,R.h*.138);ctx.clip();}
 hl10Cell(s.pilot+'_'+s.actorClip,s.actorFrame,foot.x,foot.y-body.foot*scale,HL10_ART[s.pilot+'_'+s.actorClip][0].w*scale);
 if(inside)ctx.restore();
 return {foot,height:height*R.h,inside,q};
}
function hl10Draw(t,W,H,pk){
 pk=hl10Pilot(pk);const s=hl10Sample(t,pk),T=HL10.times;
 const bank=t<T.coast?(t<T.earth?'space':'earth'):'background',
  R=t<T.coast?hc10Rect(bank,W,H):hl10EnvironmentRect(bank,s.background,W,H),camera=hl10Camera(t);
 ctx.save();ctx.beginPath();ctx.rect(R.x,R.y,R.w,R.h);ctx.clip();
 // Only the scene moves. Aircraft, actor, shadows and doorway share the same
 // world transform; captions and their layout stay outside the camera.
 ctx.translate(R.x+R.w/2,R.y+R.h/2);ctx.scale(camera.zoom,camera.zoom);
 ctx.translate(-R.x-camera.x*R.w,-R.y-camera.y*R.h);
 if(t<T.coast)hc10Plate(bank,R);else hl10Cell(bank,s.background,R.x+R.w/2,R.y+R.h/2,R.w);
 if(t<T.coast){
  s.flight=hc10Flight(t,pk,R);
 }else if(t<T.pad){
  s.flight=hc10Flight(t,pk,R);
 }else{
  const landing=hc10ShipGeometry(pk,'rear'),q=Math.max(0,t-T.pad),d=hl10Ease(q/1.68),
   // Continue the exact approach image and width without a pose/position pop.
   // Only rigid translation and the shared camera move the static airframe.
   scale=.20*R.w/landing.w,x=R.x+R.w*.500,footY=R.y+R.h*.875,
   y=lerp(R.y+R.h*.58,footY-landing.h*scale/2,d);
  hl10Cell('shadow',Math.min(3,Math.floor(d*4)),x+scale*16,footY,R.w*lerp(.27,.35,d));
  hl10Cell('door',s.doorFrame,R.x+R.w*.500,R.y+R.h*.563,HL10_ART.door[0].w*R.w/840*.50);
  if(q>=1.60&&q<3.28)hl10Cell('downwash',Math.min(15,Math.floor((q-1.60)/1.68*16)),x,footY,R.w*.37);
  // The same fully grounded root remains through disembark and the walk.
  const actorBehind=s.phase==='walk'&&(t-T.walk)/(T.entered-T.walk)>.24;
  let actor=null;if(actorBehind)actor=hl10Actor(s,R);
  hc10StaticShip(pk,'rear',x,y,landing.w*scale);
  if(!actorBehind)actor=hl10Actor(s,R);
  s.ship={x,y,footY,scale,bank:landing.key,frame:0};s.actor=actor;
 }
 ctx.restore();
 const E=VICTORY_PILOT_ENDINGS[pk];
 const captions=t<T.earth?[pk.toUpperCase(),'FURY FLIGHT, CAN ANYONE HEAR ME?']:
  t<T.coast?['FURY FLIGHT','WE HAVE YOU. HOLD THAT CHANNEL. WE ARE BRINGING YOU HOME.']:
  t<T.pad?[pk.toUpperCase(),'FURY HQ IN SIGHT. IT IS GOOD TO BE HOME.']:
  t<T.exit?['FURY HQ','WELCOME HOME. THE LANDING PAD IS CLEAR.']:
  t<T.walk?[pk.toUpperCase(),'ENGINES OFF. BACK ON SOLID GROUND.']:[E.head,E.body];
 victoryCaption(captions[0],captions[1],W,H,1);
 const fade=hl10Ease((t-(T.end-.70))/.70);
 hl10Fade(fade,W,H);
 HL10.last={...s,rect:R,camera,fade};HL10.transition={phase:'homecoming',t,fade};hl10Cues(t,pk);
}
victoryRestoration=function(t,W,H,pk){
 // The original ending's parked aircraft are retired from this shot. Even
 // the bounded loading fallback only draws cells from this new homecoming.
 hl10Warm(pk);
 return hl10Draw(t,W,H,pk);
};
victoryDish=function(t,W,H,S){
 const out=HL10.base.dish.apply(this,arguments),fade=1-hl10Ease((t-VICTORY_DISH_AT)/.65);
 hl10Fade(fade,W,H);HL10.transition={phase:'survivor',t,fade};return out;
};
victoryFinalCard=function(t,W,H){
 const out=HL10.base.card.apply(this,arguments);
 if(run.mode!=='arcade'&&!drawVictory._trueEnding){
  const fade=1-hl10Ease((t-VICTORY_CARD_AT)/.65);
  hl10Fade(fade,W,H);HL10.transition={phase:'card',t,fade};
 }return out;
};
