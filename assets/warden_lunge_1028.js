"use strict";
/* Rear-leg drive, real claw contact, silent face and denser native portal cookoff. */
const WL39={events:[],cells:new Map(),base:{set:s7mSet,tick:s7mTick,pose:s7mPose,bank:sw28Bank,cell:s7mCell,blit:s7mBlit,warnings:s7mWarnings,shot:s7mShot,orb:sw28Orb,volley:s7mVolley,waves:s7mWaves,barrage:bh25Start,toxic:fr27ToxicExplosion,exit:fr27Exit,load:stageLoadBegin}};
for(const [name,a]of Object.entries(WL39_ART)){const id='wl39_'+name;ER28_ART[id]=a;XART._src[a.key]=a.path;XART.rdy(a.key);}
function wl39Own(b){return run.stage===7&&b?._s7mod&&!b._s7mod.tank;}
function wl39Log(event,data={}){WL39.events.push({event,t:efxClock,...data});if(WL39.events.length>500)WL39.events.shift();}
stageLoadBegin=function(n,keys){return WL39.base.load.call(this,n,[...(keys||[]),...(n===7?Object.values(WL39_ART).map(a=>a.key):[])]);};
s7mSet=function(b,mode){if(wl39Own(b)&&['orbs','er28-core-burst','spore-lob','portal-volley'].includes(mode))mode='er28-mortar';
 const r=WL39.base.set.call(this,b,mode),M=b?._s7mod;if(!wl39Own(b))return r;
 delete M.wl39;if(M.mode.startsWith('swipe')){M.warn=Math.max(.95,M.warn);M.wl39={mode:M.mode,home:{x:b.x,y:b.y},target:{x:player.x,y:player.y},endY:b.y,previous:{},released:false};wl39Log('rear-leg-brace',{mode:M.mode});}return r;};
function wl39Active(b){return wl39Own(b)&&b._s7mod.wl39&&b._s7mod.mode.startsWith('swipe')&&!b._s7mod.frExit;}
function wl39Progress(M){const u=M.t-M.warn;return{u,wind:clamp(M.t/M.warn,0,1),strike:clamp(u/.44,0,1),recover:clamp((u-.52)/.75,0,1)};}
function wl39Front(M,id,end=false){const A=M.wl39,P=wl39Progress(M),side=id.endsWith('L')?-1:1,active=M.mode==='swipeX'||M.mode===(side<0?'swipeL':'swipeR'),bank=R25_ART.legs[id];
 let frame=0,angle=0;if(active){frame=end?7:P.u<0?Math.min(4,Math.floor(P.wind*5)):P.u<.52?4+Math.min(3,Math.floor(P.strike*4)):Math.max(0,7-Math.floor(P.recover*8));
  angle=end?side*.8:P.u<0?-side*.5*P.wind:P.u<.52?side*(-.5+1.3*P.strike):side*.8*(1-P.recover);}
 const row=bank.frames[frame],k=bank.worldScale,c=Math.cos(angle),s=Math.sin(angle),hip={x:side*64,y:-11};
 const point=xy=>({x:hip.x+(xy[0]-bank.pivot[0])*k*c-(xy[1]-bank.pivot[1])*k*s,y:hip.y+(xy[0]-bank.pivot[0])*k*s+(xy[1]-bank.pivot[1])*k*c});
 const center=point([128,128]),toe=point(row.foot),target=point(row.target);return{cell:row.key,frame,a:angle,x:center.x,y:center.y,w:256*k,h:256*k,toe,bm9Tip:toe,target,r25:true};}
s7mPose=function(b){const out=WL39.base.pose.apply(this,arguments);if(!wl39Active(b))return out;const M=b._s7mod,A=M.wl39,P=wl39Progress(M);
 for(let i=0;i<out.length;i++){const p=out[i];if(p.id.startsWith('front'))out[i]={...p,...wl39Front(M,p.id)};
  if(p.id.startsWith('rear')){const a=WL39_ART[p.id],push=Math.max(0,b.y-(A.home.y-10)),f=P.u<0?Math.min(15,Math.floor(P.wind*16)):P.u<.52?16+Math.min(15,Math.round(clamp(push/70,0,1)*15)):32+Math.min(15,Math.floor(P.recover*16)),row=a.poses[f],side=p.id.endsWith('L')?-1:1,hip={x:side*64,y:-50},toe={x:hip.x+row.foot[0]-160,y:hip.y+row.foot[1]-160};
   out[i]={...p,cell:'wl39rear_'+p.id+'_'+f,frame:f,x:hip.x,y:hip.y,w:320,h:320,a:0,r25:true,wl39:true,toe,bm9Tip:toe,target:toe,stance:P.u>=0&&P.u<.52&&push<=70};}}
 return out;};
sw28Bank=function(b,p){if(p.wl39)return{name:'wl39_'+p.id,f:p.frame};return WL39.base.bank.apply(this,arguments);};
s7mCell=function(name,i,trim){if(typeof i!=='string'||!i.startsWith('wl39rear_'))return WL39.base.cell.apply(this,arguments);const [,id,n]=i.split('_'),a=WL39_ART[id],f=+n;let c=WL39.cells.get(i);if(!c&&XART.rdy(a.key)){c=document.createElement('canvas');c.width=c.height=320;c.getContext('2d').drawImage(XART.get(a.key),f%a.cols*320,Math.floor(f/a.cols)*320,320,320,0,0,320,320);WL39.cells.set(i,c);}return c||null;};
s7mBlit=function(name,i,x,y,w,h,rot,alpha,flash){if(typeof i==='string'&&i.startsWith('wl39rear_')){const [,id,f]=i.split('_');return er28Blit('wl39_'+id,+f,x,y,flash>0);}return WL39.base.blit.apply(this,arguments);};
s7mTick=function(b,dt){if(!wl39Active(b)){const r=WL39.base.tick.apply(this,arguments),M=b?._s7mod;
 if(wl39Own(b)&&missionIntro(b)&&M._mission29Intro?.t>3.3){const I=M._mission29Intro;I.wl39CD=(I.wl39CD||0)-dt;if(I.wl39CD<=0){I.wl39CD+=.10;wl39PortalBurst(b,worldWidth()/2,149,I.serial++);}}return r;}
 const M=b._s7mod,A=M.wl39,ids=s7mLive(M,'front').filter(p=>M.mode==='swipeX'||M.mode===(p.id==='frontL'?'swipeL':'swipeR')).map(p=>p.id);if(!ids.length){s7mSet(b,'recover');return true;}
 bm9S7Common(b,dt);for(const c of M.er28Canisters||[])c.flash=Math.max(0,c.flash-dt);M.lean=0;M.height=0;
 const P=wl39Progress(M);if(P.u<0){if(P.wind<.65)A.target={x:player.x,y:player.y};const rear=s7mLive(M,'rear').length;
  const reach=clamp(A.target.y-97-A.home.y,40,145)*(rear===2?1:rear===1?.62:0);A.endY=Math.min(VH-130,A.home.y+reach);b.y=A.home.y-10*P.wind;combatWarningTick(b,'warden-rear-drive',M.t,M.warn);}
 else if(P.u<.52){const v=P.strike*P.strike*(3-2*P.strike);b.y=lerp(A.home.y-10,A.endY,v);if(!A.released){A.released=true;s7mSound('hammerThrow');s7WardenMechSound('foot');wl39Log('rear-leg-thrust',{from:A.home.y,to:A.endY});}}
 else b.y=lerp(A.endY,A.home.y,P.recover*P.recover*(3-2*P.recover));b.x=A.home.x;b._drawY=b.y+M.drop;
 const gait=r25Gait(b);gait.yaw=0;gait.speed=0;gait.floorRate=0;gait.lastDX=gait.lastDY=0;
 for(const p of s7mPose(b).filter(p=>ids.includes(p.id))){const tip=s7mWorld(b,p.toe);if(P.u>=0&&P.u<.52)bm9HitPath(A.previous[p.id]||tip,tip,26,'Warden rear-driven claw');A.previous[p.id]=tip;}
 if(P.recover>=1){b.y=A.home.y;const next=M.mode==='swipeL'&&s7mLive(M,'front').some(p=>p.id==='frontR')?'swipeR':M.mode==='swipeR'?'swipeX':'recover';s7mSet(b,next);}return true;
};
s7mWarnings=function(front){if(!wl39Active(boss))return WL39.base.warnings.apply(this,arguments);const b=boss,M=b._s7mod,A=M.wl39;if(M.t>=M.warn)return;
 for(const p of s7mPose(b).filter(p=>p.id.startsWith('front')&&s7mLive(M,'front').some(q=>q.id===p.id)&&(M.mode==='swipeX'||M.mode===(p.id==='frontL'?'swipeL':'swipeR')))){
  const start=s7mWorld(b,p.toe),end=wl39Front(M,p.id,true).toe,z={x:A.home.x+end.x,y:A.endY+M.drop+end.y};
  combatWarningDraw(b,{x:start.x,y:start.y,ex:z.x,ey:z.y,width:52,progress:M.t/M.warn,laneShape:'line',fieldOnly:!front,alertOnly:false});}
};
// The face has no ordinary launcher. Existing live turrets and dorsal mortars own ordnance.
s7mShot=function(b,x,y,a,speed,kind){if(wl39Own(b)&&!['gun','laser'].includes(kind))return{dead:true,x,y,vx:0,vy:0};return WL39.base.shot.apply(this,arguments);};
s7mVolley=function(b){if(wl39Own(b))return;return WL39.base.volley.apply(this,arguments);};
s7mWaves=function(b){if(wl39Own(b))return;return WL39.base.waves.apply(this,arguments);};
bh25Start=function(b,kind){if(wl39Own(b)&&kind==='warden')return false;return WL39.base.barrage.apply(this,arguments);};
sw28Orb=function(b){if(wl39Own(b)&&['orbs','er28-core-burst','bh25'].includes(b._s7mod.mode))return null;return WL39.base.orb.apply(this,arguments);};
fr27ToxicExplosion=function(){const first=explosions.length,r=WL39.base.toxic.apply(this,arguments);if(run.stage===7)for(const e of explosions.slice(first)){e.dur=Math.max(.16,e.dur*.62);e._wl39Toxic=true;}return r;};
function wl39PortalBurst(b,x,y,serial){if(!Number.isFinite(x+y))return;if(explosions.filter(e=>e._wl39Toxic).length>=64)return;const a=serial*2.39996,rx=105+(serial%3)*13,ry=76+(serial%2)*23;fr27ToxicExplosion(x+Math.cos(a)*rx,y+Math.sin(a)*ry,105+serial%3*18,serial);}
fr27Exit=function(b,dt){const r=WL39.base.exit.apply(this,arguments),E=b._s7mod.frExit;if(!E||b.dead)return r;
 const current=!!E.k1001,near=current?E.portalOn&&(!E.closeT||E.t<E.closeT+S7P.CLOSE):E.t>=13.5&&E.t<18.6;
 if(current?E.t<.35:E.t<8)return r;
 E.wl39CD=(E.wl39CD||0)-dt;if(E.wl39CD<=0){E.wl39CD+=near?.045:.07;
  if(near){const y=current?E.portalYNow:E.portalY;wl39PortalBurst(b,E.portalX,y,E.serial++);wl39PortalBurst(b,E.portalX,y,E.serial++);}
  else if(explosions.filter(e=>e._wl39Toxic).length<64)fr27ToxicExplosion(camLeftX()+((E.serial++*.381966)%1)*viewW(),viewTopY()+40+((E.serial*.618034)%1)*(viewH()-80),115+E.serial%4*20,E.serial);
  combatAudio0927(b,near?'expBig':'expSmall',near?.14:.22);}
 return r;};
// A ground projection of the actual core alpha stays beneath the airborne chassis.
function wl39AirShadowPose(b){const M=b?._s7mod;if(!wl39Own(b)||b.dead||M.frExit||!(M.height>0)||!['er28-bounce','jump','stomp','bounce'].includes(M.mode))return null;
 const high=clamp(M.height/150,0,1),scale=.96-.22*high;
 return{x:b.x,y:b.y+M.drop+22,scale,alpha:.52-.22*high,frame:Math.floor(M.clock*20)%16};}
function wl39AirShadow(b){const p=wl39AirShadowPose(b),a=WL39_ART.coreShadow;if(!p||!XART.rdy(a.key))return false;
 ctx.save();ctx.globalAlpha*=p.alpha;ctx.drawImage(XART.get(a.key),p.frame%a.cols*a.cw,Math.floor(p.frame/a.cols)*a.ch,a.cw,a.ch,p.x-a.pivot[0]*p.scale,p.y-a.pivot[1]*p.scale,a.cw*p.scale,a.ch*p.scale);ctx.restore();return true;}
WL39.shadowBase=s7mDraw;
s7mDraw=function(b){const M=b?._s7mod;wl39AirShadow(b);
 // The native high jump hides the body and used to draw a separate ellipse.
 if(wl39Own(b)&&!b.dead&&!M.frExit&&M.mode==='jump'&&M.height>330)return true;
 return WL39.shadowBase.apply(this,arguments);};
