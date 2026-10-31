/* Contra34: approved exported enemy art; camera and input share an inverse transform. */
(function(root){
 'use strict';
 const TD=root.TD,P=root.TD_CONTRA34_ART,E=TD.Escape29,I=TD.Input,M=TD.M,art=TD.AssaultArt;
 const api=TD.Contra34={build:P.build,stats:{side:0,front:0,boss:0,drone:0}};
 const roles={rifle:'machine_gunner',heavy:'minigunner',laser:'sniper',rocket:'rocket_launcher'};
 const clip=(tag,role,action,side)=>P.sequences[['c34',tag,role,action,side].filter(Boolean).join('_')];
 function frame(q,t,loop=q?.loop){if(!q)return null;const n=Math.max(0,Math.floor(t*q.fps));return q.frames[loop?n%q.frames.length:Math.min(n,q.frames.length-1)];}
 api.clip=clip;
 api.role=u=>u.contraRole||roles[u.kind]||'machine_gunner';
 api.sidePose=function(u,G){const role=api.role(u),side=u.x<G.player.x?'east':'west',action=u.phase==='enter'?'walk':u.firing>0?'fire':'idle',time=action==='walk'?u.walk:action==='fire'?u.fireAge34||0:0,q=clip('side',role,action,side);return {key:frame(q,time,true),s:P.roles[role].sideScale,side,action};};
 api.sideSocket=function(u,G){const z=api.sidePose(u,G),m=P.assets[z.key];return{x:u.x+(m.muzzle[0]-m.anchor[0])*z.s,y:u.y+(m.muzzle[1]-m.anchor[1])*z.s};};
 api.sideBody=function(u,G){const z=api.sidePose(u,G),m=P.assets[z.key],h=(m.anchor[1]-m.bounds[1])*z.s;return{x:u.x,y:u.y-h/2,rx:u.kind==='heavy'?29:22,ry:Math.max(28,h*.47)};};
 api.drawSide=function(ctx,u,G){if(u.dead&&u.deadT>.10)return;const z=api.sidePose(u,G);art.draw(ctx,z.key,u.x,u.y,{s:z.s,flash:u.flash>0||u.dead?1:0});api.stats.side++;};
 api.dronePose=function(u,G){const side=u.x<G.player.x?'east':'west';return{key:frame(clip('side','flying_alien',u.firing>0?'fly_fire':'fly',side),u.age,true),s:.95};};
 api.droneSocket=function(u,G){const z=api.dronePose(u,G),m=P.assets[z.key];return{x:u.x+(m.muzzle[0]-m.anchor[0])*z.s,y:u.y+28+(m.muzzle[1]-m.anchor[1])*z.s};};
 api.droneBody=function(u,G){const z=api.dronePose(u,G),m=P.assets[z.key],b=m.bounds;return{x:u.x,y:u.y+28+((b[1]+b[3])/2-m.anchor[1])*z.s,rx:23,ry:(b[3]-b[1])*z.s*.44};};
 api.drawDrone=function(ctx,u,G){if(u.dead&&u.deadT>.1)return;const z=api.dronePose(u,G);art.draw(ctx,z.key,u.x,u.y+28,{s:z.s,flash:u.flash>0||u.dead?1:0});api.stats.drone++;};
 api.frontPose=function(u){
  if(!roles[u.kind])return null;const role=api.role(u),moving=['enter','rush','vault'].includes(u.phase),side=(u.toX??u.homeX??320)<320?'west':'east';
  if(moving){const action=u.phase==='vault'?'jump':u.phase==='rush'?'run':'walk',q=clip('side',role,action,side);return frame(q,u.phase==='vault'?u.vaultT:(u.gait||0)*.7,u.phase!=='vault');}
  if(u.phase==='flank'){return frame(clip('side',role,u.firing>0?'fire':'idle',u.x<320?'east':'west'),u.fireT||0,true);}
  const firing=u.firing>0,q=clip('front',role,firing?'fire_forward':'draw_forward');
  return frame(q,firing?(u.fireT||0):u.warn>0?(.22-u.warn)/.22*q.frames.length/q.fps:0,firing);
 };
 api.heliosPose=function(b){let action=b.dead?'overload_death':b.state==='run'?'run':b.state==='return'?'walk':b.state==='volley'?'prism_volley':b.state==='lightning'?'prism_lightning':b.state==='jump'?'ground_slam':'idle',tag=action==='prism_volley'?'front':'motion',q=clip(tag,'fire_prism',action),t=b.dead?(TD.game.bastion.clearT||0):['run','walk'].includes(action)?(b.gait||0):b.t||0;api.stats.boss++;return{key:frame(q,t,!b.dead&&action!=='ground_slam'),flip:['run','walk'].includes(action)&&b.toX<b.x,action};};
 api.turretPose=t=>frame(clip('front','wall_turret_'+t.kind,t.attackT!=null&&t.attackT<.3?'fire':t.kind==='laser'?'charge':'deploy'),t.attackT!=null&&t.attackT<.3?t.attackT*2:t.age||0,true);
 api.corePose=c=>frame(clip('front','door_core','power_pulse'),c.age,true);
 api.frontShot=function(ctx,e){if(e.t<0)return true;const id=e.kind==='rocket'?'rocket_front':e.kind==='laser'?'sniper_front':e.kind==='orb'?'prism_front':'bullet_front',q=clip('fx',id,'flight');if(!q)return false;const progress=M.clamp(e.t/e.duration,0,1),k=q.frames[Math.min(q.frames.length-1,Math.floor(progress*q.frames.length))],m=P.assets[k],size=(e.kind==='orb'?20:10)+progress*(e.kind==='orb'?24:10),s=size/Math.max(m.bounds[2]-m.bounds[0],m.bounds[3]-m.bounds[1]);art.draw(ctx,k,e.x,e.y,{s});return true;};
 api.view=function(G){const e=G.escape29;if(e&&!e.finished){const side=['corridor','escape','doorSlide','drop'].includes(e.phase);return{z:1.25,x:side?0:64,y:side?82:e.phase==='chute'?32:96,worldX:side?e.camX:0};}return{z:1.15,x:M.clamp(G.player.x-320/1.15,0,640-640/1.15),y:54,worldX:0};};
 api.toWorld=function(G,x,y){const v=api.view(G);return{x:v.worldX+v.x+x/v.z,y:v.y+y/v.z};};
 api.toScreen=function(G,x,y){const v=api.view(G);return{x:(x-v.worldX-v.x)*v.z,y:(y-v.y)*v.z};};
 api.limitCursor=function(G,c){const a=api.toWorld(G,10,90),b=api.toWorld(G,630,465);c.x=M.clamp(c.x,a.x,b.x);c.y=M.clamp(c.y,a.y,b.y);};
 const canvas=document.createElement('canvas');canvas.width=640;canvas.height=480;const scene=canvas.getContext('2d');
 function closeView(draw,ctx,G){scene.setTransform(1,0,0,1,0,0);scene.clearRect(0,0,640,480);draw(scene,G);const v=api.view(G);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(canvas,v.x,v.y,640/v.z,480/v.z,0,0,640,480);ctx.restore();}
 const oldDraw=E.draw;api.drawEscapeScene=oldDraw;E.draw=(ctx,G)=>closeView(oldDraw,ctx,G);
 const m=TD.MISSIONS.find(m=>m.id===7),baseDraw=m.drawWorld;m.drawWorld=(ctx,G)=>closeView(baseDraw,ctx,G);TD.Bastion.draw=m.drawWorld;
 // Prepare the complete new banks before starting either authored section.
 const warm=()=>ART.warm(Object.keys(P.assets));warm();
})(window);
