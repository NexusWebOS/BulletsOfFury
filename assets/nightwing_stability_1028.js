'use strict';
/* Source-locked Nightwing: eased entry, continuous charge headings, larger
   authored wind and own-pixel six-step armor charge. Native attack math stays. */
const NW32={base:{entry:nf29Entry,begin:nf29Begin,charge:nf29Charge,mode:nw28Mode,
 tick:whvAceTick,desperation:whvAceDesperation,body:nw28DrawBody,blit:nw30Blit,projectile:drawCombatFinalProjectile,load:stageLoadBegin},drawing:null,last:null,events:[]};
const NW32_ART={clean_charge:{cw:272,ch:272,frames:18,cols:6},wind_gust:{cw:96,ch:96,frames:512,cols:16},
 wind_rear:{cw:336,ch:336,frames:24,cols:8},wind_front:{cw:336,ch:336,frames:24,cols:8},wind_aura:{cw:272,ch:272,frames:18,cols:6}};
for(const [k,a]of Object.entries(NW32_ART)){a.key='nw32_'+k;XART._src[a.key]='assets/game/levels/stage_06/boss/'+(['wind_rear','wind_front','wind_aura'].includes(k)?'nightwing_teal_charge_1030/':'nightwing_stability_1028/')+k+'.png';}
stageLoadBegin=function(n,keys){return NW32.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(NW32_ART).map(a=>a.key)]:keys);};
function nw32Blit(k,f,x,y,g=ctx){const a=NW32_ART[k];if(!XART.rdy(a.key))return false;f=((f|0)%a.frames+a.frames)%a.frames;
 g.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x)-a.cw/2,Math.round(y)-a.ch/2,a.cw,a.ch);return true;}
function nw32Delta(a,b){return Math.atan2(Math.sin(b-a),Math.cos(b-a));}
nf29Entry=function(b,dt){if(!nw30Own(b))return NW32.base.entry.apply(this,arguments);const A=b._whv.ace,M=A._nw28,mid=camLeftX()+viewW()/2,top=viewTopY(),home=clamp((WHV_ZONE.y0+WHV_ZONE.y1)/2,top+110,VH*.45);
 M.t+=dt;A.t+=dt;A.st='emerge';A.vx=A.vy=0;b._noHit=true;
 const north=M.mode==='north',dur=north?2.1:1.9,u=clamp(M.t/dur,0,1),side=M.corner<mid?-1:1;
 const P=north?[M.from,{x:M.corner,y:VH*.62},{x:mid,y:top+80},{x:mid,y:top-160}]:[M.from,{x:mid+side*85,y:top-70},{x:mid,y:home-85},{x:mid,y:home}];
 const v=north?u:u*u*(3-2*u),p=nf29Curve(P,v);A.x=p.x;A.y=p.y;
 // A single 64-heading family through the curve; no threshold switch between
 // three differently banked silhouettes at8% and90% of entry.
 A._nf29Pose=nf29Heading(p.angle,0);A._nw32Yaw=p.angle;nf29Sync(b);
 if(u>=1){delete A._nf29Pose;nw28Mode(b,north?'north_wait':'settle');nf29Log(b,'stable-entry-'+(north?'north':'return'));}
};
nw28Mode=function(b,mode){const r=NW32.base.mode.apply(this,arguments);if(nw30Own(b)&&mode==='fight'){
 const A=b._whv.ace;A.vx=A.vy=A.pvx=0;A.ppx=player.x;A.rollCd=Math.max(A.rollCd,1.6);A.somerCd=Math.max(A.somerCd,3);A._nw32Yaw=Math.PI/2;}return r;};
nf29Begin=function(b){const A=b._whv.ace,from=A._nw32Yaw??Math.PI/2;const r=NW32.base.begin.apply(this,arguments);A.dash._nw32From=from;return r;};
nf29Charge=function(b,dt){const A=b._whv.ace,D=A.dash,old=D?.st;const r=NW32.base.charge.apply(this,arguments);
 if(!nw30Own(b))return r;
 if(A.dash&&(D.st==='warn'||old==='warn'&&D.st==='go')){const u=clamp(D.t/.95,0,1),e=old==='warn'&&D.st==='go'?1:u*u*(3-2*u),from=D._nw32From??Math.PI/2,yaw=from+nw32Delta(from,D.ang)*e;
  A._nf29Pose=nf29Heading(yaw,0);A._nw32Yaw=yaw;nf29Sync(b);}
 else if(A._nf29Pose)A._nw32Yaw=nw30Pose(b).meta.angle+Math.PI/2;
 if(old==='approach'&&!A.dash){A.vx=A.vy=A.pvx=0;A.ppx=player.x;A._nw32Yaw=Math.PI/2;}
 return r;};
// The native low-health criss-cross path has its own flight owner. Its stale
// cruise velocity cannot describe the pass: select authored headings from the
// exact path tangent, including the five-wave vertical displacement.
whvAceDesperation=function(b,A,dt){
 const r=NW32.base.desperation.apply(this,arguments);
 if(!nw30Own(b))return r;
 const P=A.desp;
 if(P&&P.st!=='done'){
  let yaw=Math.PI/2;
  if(P.st==='cross'){
   const u=clamp((P.t-P.lead)/P.dur,0,1),dx=(P.x1-P.x0)/P.dur,
    dy=(P.y1-P.y0)/P.dur+Math.cos(u*Math.PI*5)*Math.PI*5*34/P.dur;
   yaw=Math.atan2(dy,dx);
  }
  A._nf29Pose=nf29Heading(yaw,0);A._nw32Yaw=yaw;A._nw32SidePose=true;
  nf29Sync(b);
 }else if(A._nw32SidePose){
  delete A._nf29Pose;delete A._nw32SidePose;A._nw32Yaw=Math.PI/2;
 }
 return r;
};
function nw32WindGlow(b){return !b.dead&&b?._nw30?.action?.kind==='wind'?nw32Glow(b):0;}
function nw32Glow(b){const C=b?._nw30?.action;if(!C)return 0;
 if(C.phase==='fire'&&C.t<.18)return 5;if(C.phase!=='warn'&&C.phase!=='charge')return 0;
 const u=clamp(C.t/(C.kind==='wind'?2.1:C.warn),0,1),level=1+Math.floor(u*4);
 // The1015 palette ladder lives in the exported armor pixels; the renderer
 // selects a frame. Modest late pulsing preserves the blue cockpit and metal.
 return Math.min(5,level+(u>.6&&Math.floor(C.t*6)%2?1:0));}
nw30Blit=function(name,f,x,y,g=ctx){const b=NW32.drawing;
 if(b&&name==='wind_charge')return;
 if(b&&name==='clean'&&nw32Glow(b)>0){const level=nw32Glow(b);NW32.last={glow:level,frame:f,body:'clean_charge'};return nw32Blit('clean_charge',level*3+(f===16?2:f>=8?1:0),x,y,g);}
 return NW32.base.blit.apply(this,arguments);};
nw28DrawBody=function(b){if(!nw30Own(b))return NW32.base.body.apply(this,arguments);const C=b._nw30?.action,wind=!b.dead&&C?.kind==='wind'&&C.phase==='charge',A=b._whv.ace,frame=wind?Math.floor(C.t*18)%24:0;
 if(wind)nw32Blit('wind_rear',frame,A.x,A.y);NW32.drawing=b;
 try{const r=NW32.base.body.apply(this,arguments),glow=nw32WindGlow(b);NW32.auraLast=null;
  if(glow&&nw30Modular(b)){const pose=A.inverted?2:b.hp<b.maxhp*.5?1:0;nw32Blit('wind_aura',glow*3+pose,A.x,A.y);NW32.auraLast={glow,pose,x:A.x,y:A.y,hit:b.flash>0};}
  if(wind)nw32Blit('wind_front',frame,A.x,A.y);return r;}finally{NW32.drawing=null;}
};
whvAceTick=function(b,dt){if(nw30Own(b)&&b._nw30?.action){const A=b._whv.ace;A.ppx=player.x;A.pvx=0;}
 return NW32.base.tick.apply(this,arguments);};
drawCombatFinalProjectile=function(q){if(q?._nw30Owner&&q._nw30Wind){const angle=Math.atan2(q.vy,q.vx),dir=((Math.round((angle-Math.PI/2)*32/TAU)%32)+32)%32;
  nw32Blit('wind_gust',dir*16+Math.floor((q.t||0)*24)%16,q.x,q.y);return true;}return NW32.base.projectile.apply(this,arguments);};
globalThis.BOF_NIGHTWING_STABILITY_1028=NW32;
