/* Pixel25: PixelLab-native troops and UI for Overdrive stages 3 and 7. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,pack=root.TD_PIXEL25_ART;
 const seq=(kind,action,dir='south')=>pack.sequences['px25_'+kind+'_'+action+'_'+dir];
 function at(q,n){return q?.frames[Math.max(0,Math.min(q.frames.length-1,n))];}
 const api=TD.Pixel25={stats:{stage3:0,stage7:0,corpses:0},corpses:[],seq};
 api.pose=function(u){
  const kind=u.kind;if(!['rifle','heavy','rocket','laser'].includes(kind))return null;
  const locomotion=u.phase==='enter'&&seq(kind,'strafe')&&Math.abs((u.homeX||320)-320)>Math.abs((u.targetY||338)-250)*1.2?'strafe':'walk';
  const action=u.dead?'death':u.phase==='vault'?'vault':u.duck>.05?'crouch':u.firing>0||u.warn>0?'fire':['enter','rush'].includes(u.phase)||Math.abs(u.velocity)>9?locomotion:'idle';
  const q=seq(kind,action)||seq(kind,action==='vault'?'walk':'idle');if(!q)return null;
  let n=u.dead?Math.floor(u.deathT*15):action==='vault'?Math.floor(M.clamp(u.vaultT/.84,0,.999)*q.frames.length):action==='crouch'?Math.round(u.duck*(q.frames.length-1)):['walk','strafe'].includes(action)?Math.floor((u.gait||0)*q.frames.length)%q.frames.length:action==='fire'?(u.warn>0&&u.firing<=0?Math.floor((.22-u.warn)/.22*4):Math.floor((u.fireT||0)*q.fps)):0;
  const key=at(q,n);if(!ART.get(key))return null;api.stats.stage7++;return key;
 };
 const oldTick=TD.unitTick,oldDraw=TD.drawAssaultRobot,oldHit=TD.hitUnit;
 api.stage3Pose=function(u,elite){const kind=elite?'heavy':'rifle',side=Math.abs(Math.sin(u.a))>.72,dir=side?(Math.sin(u.a)>0?'west':'east'):Math.cos(u.a)<0?'north':'south',moving=Math.hypot(u.vx||0,u.vy||0)>.12,action=moving?(u.strafe&&dir==='south'&&seq(kind,'strafe')?'strafe':'walk'):u.pxFire>0?'fire':'idle',q=seq(kind,action,dir)||seq(kind,'idle',dir),n=moving?Math.floor((u.walkT||0)*q.frames.length)%q.frames.length:action==='fire'?Math.floor((u.pxFireAge||0)*q.fps):0;return {key:at(q,n),scale:elite?.84:.72};};
 api.stage3Socket=function(u,elite){const z=api.stage3Pose(u,elite),m=pack.assets[z.key],q=m.muzzle||[m.anchor[0],m.anchor[1]-50];return{x:u.x+(q[0]-m.anchor[0])*z.scale,y:u.y+(q[1]-m.anchor[1])*z.scale};};
 TD.unitTick=function(u,G,dt){const cd=u.fireCd,shots=G.eshots.length,fx=TD.FX.list.length;u.pxFire=Math.max(0,(u.pxFire||0)-dt);const result=oldTick(u,G,dt);if(G.mission===3&&['odRobot','odElite'].includes(u.type)&&u.fireCd>cd+.1){u.pxFire=.65;u.pxFireAge=0;const elite=u.type==='odElite',socket=api.stage3Socket(u,elite);for(const s of G.eshots.slice(shots)){const delta=M.wrap(s.a-u.look),angle=M.angTo(socket.x,u.y,G.player.x,G.player.y)+delta,v=M.fwd(angle),speed=Math.hypot(s.vx,s.vy);Object.assign(s,{x:socket.x,y:u.y,drawLift:u.y-socket.y,a:angle,vx:v[0]*speed,vy:v[1]*speed});}TD.FX.list.splice(fx);TD.FX.attachedFlash(u,()=>api.stage3Socket(u,elite),u.look,.13);}else u.pxFireAge=(u.pxFireAge||0)+dt;return result;};
 TD.drawAssaultRobot=function(ctx,u,elite){
  if(TD.game?.mission!==3)return oldDraw(ctx,u,elite);
  const pose=api.stage3Pose(u,elite),key=pose.key;
  if(!key||!ART.get(key))return oldDraw(ctx,u,elite);
  const s=elite?.84:.72;TD.AssaultArt.draw(ctx,key,u.x+2,u.y+3,{s,tint:'#000',alpha:.28});TD.AssaultArt.draw(ctx,key,u.x,u.y,{s,flash:u.flash>0?.7:0});api.stats.stage3++;
 };
 TD.hitUnit=function(G,u,...args){const was=u.dead,result=oldHit(G,u,...args);if(G.mission===3&&!was&&u.dead&&['odRobot','odElite'].includes(u.type)){api.corpses.push({x:u.x,y:u.y,kind:u.type==='odElite'?'heavy':'rifle',at:G.time});if(api.corpses.length>24)api.corpses.shift();}return result;};
 const mission=TD.MISSIONS.find(m=>m.id===3),floor=mission.drawFloor,setup=mission.setup;
 mission.setup=function(...args){api.corpses=[];return setup.apply(this,args);};
 mission.drawFloor=function(ctx,G){floor(ctx,G);api.corpses=api.corpses.filter(c=>G.time-c.at<3);for(const c of api.corpses){const age=G.time-c.at,q=seq(c.kind,'death'),key=at(q,Math.floor(age*15));if(key){TD.AssaultArt.draw(ctx,key,c.x,c.y,{s:c.kind==='heavy'?.84:.72,alpha:age<2?1:3-age});api.stats.corpses++;}}};
})(window);
