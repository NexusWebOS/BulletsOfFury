'use strict';
/* Allied escape: a visible foreground flyover into distance, then real edge
   clearance. Existing squad volley, wing HP and native return remain owners. */
const RR66={base:{navigate:s6WingNavigate,draw:s6WingDraw,squad:rebelSquadDraw,load:stageLoadBegin,world:drawWorld,panel:ui20Panel},events:[],hulls:0,shadows:0,duration:1.8,panels:[],painting:false};
for(const a of Object.values(RR66_ART.banks))XART._src[a.key]=a.path;
function rr66Own(q){return rr49Scope()&&q?.hp>0&&!!q._rm49Flight;}
function rr66Model(q){return q.key==='lizzie'&&typeof lizzieSkinOn!=='undefined'&&lizzieSkinOn?'lizzie_b42':q.key;}
function rr66Log(event,q,data={}){RR66.events.push({event,pilot:q.key,time:rg4State()?.age||0,...data});if(RR66.events.length>300)RR66.events.shift();}
function rr66Depth(q){const P=q._rm49Flight;if(!P)return null;const u=P.phase==='out'?clamp(P.t/RR66.duration,0,1):0,ease=v=>v*v*(3-2*v),height=P.phase==='out'?(u<.3?lerp(60,100,ease(u/.3)):lerp(100,16,ease((u-.3)/.7))):60;
 return{i:clamp(Math.round((height-16)/2),0,42),u,offset:P.phase==='out'?8+58*Math.sin(u*Math.PI):18,side:P.phase==='out'?10*Math.sin(u*Math.PI):6};}
function rr66Blit(q,role){const P=q._rm49Flight;if(!rr66Own(q)||!['out','return'].includes(P.phase))return false;const d=rr66Depth(q),a=RR66_ART.banks[rr66Model(q)+'_'+role];if(!a||!XART.rdy(a.key))return false;
 const glow=[0,1,0,2][Math.floor((q.t||0)/.07)%4],f=role==='hull'?d.i*3+glow:d.i,x=q.x+(role==='shadow'?d.side:0),y=q.y+(role==='shadow'?d.offset:0);
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);RR66[role==='hull'?'hulls':'shadows']++;return true;}
stageLoadBegin=function(n,keys){return RR66.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(RR66_ART.banks).map(a=>a.key)]:keys);};
s6WingNavigate=function(q,W,dt){const P=q._rm49Flight;if(!rr66Own(q)||P.phase!=='out')return RR66.base.navigate.apply(this,arguments);dt=clamp(dt,0,.05);
 if(!P.rr66){P.rr66={startY:q.y,startLane:(q.x-camLeftX())/viewW()};rr66Log('overflight-start',q,{x:q.x,y:q.y});}
 const before={x:q.x,y:q.y},u=clamp((P.t+=dt)/RR66.duration,0,1),ease=u*u*(3-2*u),lane=lerp(P.rr66.startLane,clamp(P.rr66.startLane,.13,.87),clamp(u/.3,0,1));
 q.target=null;q._rd21Intercept=null;q.dodgeT=0;q.dodgeMode=null;q.x=camLeftX()+viewW()*lane;q.y=lerp(P.rr66.startY,-120,ease);q.vx=(q.x-before.x)/Math.max(.0001,dt);q.vy=(q.y-before.y)/Math.max(.0001,dt);
 if(!P.rr66.crossed&&q.y<Math.max(...boss._rebels.ships.filter(rd21Live).map(q=>q.y),PLAY.y+120)){P.rr66.crossed=true;rr66Log('overflight-crossing',q,{x:q.x,y:q.y,height:16+rr66Depth(q).i*2});}
 if(u>=1){P.phase='hold';rr66Log('ally-offscreen-after-travel',q,{x:q.x,y:q.y});}return null;
};
// The ground projection is painted before the enemy hulls. The elevated ally
// is painted after the entire native world, including Voss's separate top pass.
rebelSquadDraw=function(b){if(rr49Scope(b))for(const q of s6Wing?.ships||[])rr66Blit(q,'shadow');return RR66.base.squad.apply(this,arguments);};
s6WingDraw=function(){if(!rr49Scope()||!s6Wing)return RR66.base.draw.apply(this,arguments);const W=s6Wing,all=W.ships,fly=all.filter(rr66Own);W.ships=all.filter(q=>!rr66Own(q));
 try{RR66.base.draw.apply(this,arguments);}finally{W.ships=all;}
};
ui20Panel=function(){const r=RR66.base.panel.apply(this,arguments);if(RR66.painting&&r?.cd27&&!RR66.panels.some(p=>p.x===r.x&&p.y===r.y&&p.w===r.w&&p.h===r.h))RR66.panels.push(r);return r;};
drawWorld=function(dt){RR66.panels=[];RR66.painting=true;let r;try{r=RR66.base.world.apply(this,arguments);}finally{RR66.painting=false;}if(!rr49Scope())return r;
 ctx.save();try{const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);
  ctx.beginPath();ctx.rect(camLeftX(),0,viewW(),VH);for(const p of RR66.panels)ctx.rect(camLeftX()+p.x,p.y,p.w,p.h);ctx.clip('evenodd');
  for(const q of s6Wing?.ships||[])rr66Blit(q,'hull');
 }finally{ctx.restore();}return r;
};
globalThis.BOF_RIDERS_ALLIED_OVERFLIGHT_1030=RR66;
