"use strict";
/* Roadside atomic missiles: shoot the standing rocket or its ascent. A missile
   which fully clears the top commits one warned return; the landing never homes. */
const HM17={base:{begin:beginStage,load:stageLoadBegin,update:updatePlay,enemy:drawEnemy,
 kill:killEnemy,terrain:drawLevelMaster,ground:groundTargetingDraw,targets:_lockTargets},events:[],empty:[],serial:0,
 next:100,side:-1,draws:{},cfg:[
  {gap:380,warm:4.4,hp:14,return:3.4,radius:52},
  {gap:300,warm:3.8,hp:18,return:3.2,radius:58},
  {gap:230,warm:3.3,hp:22,return:3.0,radius:64},
  {gap:180,warm:2.9,hp:26,return:2.8,radius:70},
  {gap:150,warm:2.7,hp:28,return:2.7,radius:72}]};
for(const a of Object.values(HM17_ART))XART._src[a.key]=a.path;
function hm17Config(){return HM17.cfg[target17Rank()];}
function hm17Log(event,data={}){HM17.events.push({event,...data});if(HM17.events.length>180)HM17.events.shift();}
function hm17Warm(){let ready=true;for(const a of Object.values(HM17_ART))if(!XART.rdy(a.key))ready=false;
 for(const a of P2_ART.atom)if(!XART.rdy(a.key))ready=false;if(!XART.rdy('s3thermo_nuclear_retina'))ready=false;wm26Warm();return ready;}
stageLoadBegin=function(n,keys){return HM17.base.load.call(this,n,[...(keys||[]),...(n===4?[...Object.values(HM17_ART).map(a=>a.key),'s3thermo_nuclear_retina']:[])]);};
beginStage=function(n){const r=HM17.base.begin.apply(this,arguments);HM17.events=[];HM17.empty=[];HM17.serial=0;HM17.next=100;HM17.side=-1;
 if(n===4)hm17Warm();return r;};
function hm17Blit(name,x,y,flash=0,angle=0,scale){const a=HM17_ART[name];if(!a||!XART.rdy(a.key))return false;
 const k=scale??a.scale,im=XART.get(a.key);ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(angle);
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);
 if(flash>0){const tint=xartTint(a.key,'#ffffff',1);if(tint){ctx.globalAlpha*=Math.min(1,flash*8);ctx.drawImage(tint,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);}}
 ctx.restore();HM17.draws[name]=(HM17.draws[name]||0)+1;return true;
}
function hm17Shoulder(side){
 // The authored Lost Airbase spine occupies source x334..690 on a1024px
 // master. A66px-wide pad sits immediately OUTSIDE it; tanks retain the road.
 const k=LA1007.worldW/LA1007.sourceW;
 return side<0?334*k-34:690*k+34;
}
function hm17Spawn(side,y=viewTopY()-36){if(run.stage!==4||!hm17Warm())return null;
 const C=hm17Config(),hp=C.hp*(coopActive()?1.5:1),e={type:'highway_missile17',x:hm17Shoulder(side),y:y-46,
  vx:0,vy:0,w:56,h:136,hp,maxhp:hp,_maxhp:hp,t:0,flash:0,dead:false,score:650,dropOk:true,
  pattern:'ballistic17',shoots:false,fireCd:999,fireRate:999,amp:0,ground:true,prop:true,_prop:true,
  _vkind:'tank',_noSep:true,_esw:null,_hm17:{id:++HM17.serial,side,phase:'loaded',t:0,
   anchor:y-LA1007.scroll,warm:C.warm,return:C.return,radius:C.radius,velocity:24}};
 enemies.push(e);if(typeof stageStats!=='undefined')stageStats.spawned++;
 if(typeof stageScoreOffer==='function')stageScoreOffer(e.score);
 hm17Log('pad-spawn',{id:e._hm17.id,side,x:e.x,y,scroll:LA1007.scroll,hp});return e;
}
function hm17LeavePad(e){const A=e._hm17;if(A.leftPad)return;A.leftPad=true;
 HM17.empty.push({x:e.x,anchor:A.anchor});
}
function hm17Escape(e){const A=e._hm17;if(A.escaped||e.dead||e.hp<=0)return;
 A.escaped=true;A.phase='escaped';e.dead=true;
 const T=targetShip(e.x,VH*.6),r=A.radius;
 const q=groundTargetingSpawn({kind:'missile',owner:null,track:false,lane:false,
  x:clamp(T.x,camLeftX()+r+12,camRightX()-r-12),y:clamp(T.y,viewTopY()+r+55,VH-r-16),
  warn:A.return,radius:r,size:r*2.4,active:.62,sound:'atomicDetonate',shake:14,
  onImpact:g=>{s67AtomicImpact(g);const cloud=s67Nukes[s67Nukes.length-1];
   if(cloud){cloud.w=300;cloud.dur=1.8;}hm17Log('atomic-impact',{id:A.id,x:g.x,y:g.y,radius:g.radius});}});
 q._hm17Return={id:A.id};
 Audio.SFX.alertDanger?.();hm17Log('escaped-return-locked',{id:A.id,x:q.x,y:q.y,warn:q.warn,radius:r});
}
function hm17Tick(e,dt){const A=e._hm17;if(e.dead||e._dyingT!=null)return;
 if(A.phase==='loaded'){
  const base=A.anchor+LA1007.scroll;e.x=hm17Shoulder(A.side);e.y=base-46;
  if(base>VH+85){e.dead=true;return;}
  // Show the entire tall rocket before starting its launch countdown.
  if(base<viewTopY()+126||e.x<camLeftX()+30||e.x>camRightX()-30)return;
  if(bossActive||subBossActive||warnT>0||bossDefeated){e.dead=true;hm17LeavePad(e);return;}
  if(e._frozen||e._mercuryLock>0||e._stagger>0)return;
  A.t+=dt;combatWarningTick(e,'hm17-launch',A.t,A.warm);
  if(A.t>=A.warm){hm17LeavePad(e);A.phase='boost';A.t=0;e.y-=8;e.w=34;e.h=120;
   Audio.SFX.nuclearLaunch?.();shake=Math.max(shake,3);hm17Log('launch',{id:A.id,x:e.x,y:e.y,hp:e.hp});}
 }else if(A.phase==='boost'){
  // One fixed ascent lane: freezing/chromium can delay an interceptable rocket.
  if(e._frozen||e._mercuryLock>0)return;
  A.t+=dt;A.velocity=Math.min(350,A.velocity+145*dt);e.y-=A.velocity*dt;
  if(e.y+60<viewTopY()-8)hm17Escape(e);
 }
}
function hm17Director(){if(run.stage!==4||!XART.rdy(LA1007.key)||bossActive||subBossActive||bossDefeated||warnT>0||stageEnding||stageTimer<3)return;
 if(stageTimer>=curStage.length-14)return; // Let the authored boss crowd gate clear.
 if(LA1007.scroll<HM17.next)return;
 if(enemies.filter(e=>e._hm17&&!e.dead).length>=(target17Rank()===0?2:target17Rank()===1?3:4))return;
 if(hm17Spawn(HM17.side)){HM17.side*=-1;HM17.next=LA1007.scroll+hm17Config().gap;}
}
updatePlay=function(dt){const r=HM17.base.update.apply(this,arguments);
 if(state!==GS.PLAY||run.stage!==4||story||fb2Talk)return r;
 const step=Math.min(.1,Math.max(0,dt));for(const e of enemies)if(e._hm17)hm17Tick(e,step);
 for(const q of groundTargetingFx)if(q._hm17Return&&!q.dead&&!q.impact)combatWarningTick(q,'hm17-return',q.t,q.warn);
 HM17.empty=HM17.empty.filter(p=>p.anchor+LA1007.scroll<VH+100);enemies=enemies.filter(e=>!e.dead);
 hm17Director();return r;
};
killEnemy=function(e){if(!e?._hm17)return HM17.base.kill.apply(this,arguments);
 if(e.dead||e._dyingT!=null)return;const A=e._hm17;hm17LeavePad(e);
 hm17Log('intercepted',{id:A.id,phase:A.phase,x:e.x,y:e.y});A.phase='destroyed';
 return HM17.base.kill.apply(this,arguments);
};
_lockTargets=function(){const all=HM17.base.targets.apply(this,arguments);
 // The ordinary list uses a unit's centre. Keep this tall rocket's lock until
 // its visible tail clears the field, rather than dropping it halfway out.
 if(run.stage===4)for(const e of enemies)if(e._hm17?.phase==='boost'&&!e.dead&&e.hp>0&&
  e.y+e.h/2>viewTopY()&&e.y-e.h/2<VH&&!all.includes(e))all.push(e);
 return all;
};
drawLevelMaster=function(dt){const r=HM17.base.terrain.apply(this,arguments);
 if(run.stage===4){
  // This terrain owner publishes travel during drawing. Register the standing
  // bodies to that SAME publication, including the very first reflected seam.
  for(const e of enemies)if(e._hm17?.phase==='loaded'&&!e.dead){e.x=hm17Shoulder(e._hm17.side);e.y=e._hm17.anchor+LA1007.scroll-46;}
  for(const p of HM17.empty)hm17Blit('pad',p.x,p.anchor+LA1007.scroll);
 }return r;};
drawEnemy=function(e){if(!e?._hm17)return HM17.base.enemy.apply(this,arguments);
 if(e.dead||e._dyingT!=null)return;const A=e._hm17,loaded=A.phase==='loaded',base=e.y+46;
 if(loaded){hm17Blit('pad',e.x,base,e.flash);
  if(A.t>0){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.3+.7*Math.abs(Math.sin(A.t*(A.t/A.warm>.72?22:9)));
   hm17Blit('lamps',e.x,base);ctx.restore();
   combatWarningDraw(e,{x:e.x,y:e.y-70,ex:e.x,ey:e.y-80,progress:A.t/A.warm,alertOnly:true,alertX:e.x,alertY:e.y-78});}
 }else if(A.phase==='boost')wm26Draw(ctx,'missile',e.x,e.y+57,Math.PI/2,(A.t*14)%1,48);
 hm17Blit('missile',e.x,e.y-(loaded?8:0),e.flash);
 e._drawW=loaded?72:41;e._drawH=loaded?136:123;return true;
};
groundTargetingDraw=function(){const all=groundTargetingFx,own=all.filter(q=>q._hm17Return&&!q.dead);
 // The normal floor marker is a perspective ellipse. This atomic attack has
 // a circular damage radius, so its authored nuclear Retina marks that circle.
 groundTargetingFx=all.filter(q=>!q._hm17Return);let r;
 try{r=HM17.base.ground.apply(this,arguments);}finally{groundTargetingFx=all;}
 for(const q of own){if(q.impact)continue;
  if(XART.rdy('s3thermo_nuclear_retina')){
   ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=.65+.3*Math.abs(Math.sin(q.t*(q.t/q.warn>.78?22:7)));
   const key='s3thermo_nuclear_retina',progress=q.t/q.warn,tint=progress<.5?'#85ec62':progress<.78?'#ffdc64':'#ff4840';
   ctx.drawImage(xartTint(key,tint,1)||XART.get(key),q.x-q.radius,q.y-q.radius,q.radius*2,q.radius*2);ctx.restore();
   HM17.draws.returnRetina=(HM17.draws.returnRetina||0)+1;
  }
  const fall=.95,u=clamp((q.t-(q.warn-fall))/fall,0,1);if(u<=0)continue;
  // Pointed nose reaches the committed floor mark at impact. No collision
  // before that point, and no second Retina chase after the launch escaped.
  const a=HM17_ART.missile,k=.50,cy=lerp(viewTopY()-110,q.y-(a.pivot[1]-4)*k,u*u);
  wm26Draw(ctx,'missile',q.x,cy-43,-Math.PI/2,(q.t*14)%1,34);
  hm17Blit('missile',q.x,cy,0,Math.PI,k);
 }return r;
};
window.BOF_HIGHWAY_MISSILES={state:HM17,spawn:hm17Spawn,shoulder:hm17Shoulder};
