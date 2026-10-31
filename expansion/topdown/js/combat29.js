/* Arcade movement/aims. All poses resolve authored whole-body plates. */
(function(root){
 'use strict';
 const TD=root.TD,I=TD.Input,M=TD.M,W=TD.World,A=TD.Audio,pack=root.TD_ESCAPE29_ART,art=TD.AssaultArt;
 const api=TD.Combat29={stats:{vaults:0,rollLandings:0,crouchLandings:0,aimDraws:0}};
 api.frame=(name,t=0,loop=true)=>{const q=pack.sequences['e29_'+name];return q?.frames[loop?Math.floor(t*(q.fps||16))%q.frames.length:Math.min(q.frames.length-1,Math.max(0,Math.floor(t*(q.fps||16))))];};
 api.aimKey=function(p,angle=p.aim){const f=M.fwd(angle);if(Math.abs(f[0])>.08)p.sideFacing29=f[0]>0?'east':'west';const side=p.sideFacing29||'east',elevation=Math.atan2(-f[1],Math.abs(f[0]))*180/Math.PI,index=M.clamp(Math.round((elevation+90)/15),0,12);return pack.sequences['e29_aim_'+side]?.frames[index];};
 const make=TD.makeFootPlayer;TD.makeFootPlayer=function(...args){const p=make(...args);if([3,7].includes(TD.game?.mission))Object.assign(p,{hp:1,max:1,oneHit29:true});return p;};
 const pose=TD.footPose;TD.footPose=function(p){
  if(p.vault29&&!p.dead){const v=p.vault29,side=v.tx<v.x?'west':'east',key=Math.abs(v.tx-v.x)>Math.abs(v.ty-v.y)?api.frame('vault_'+side,v.t/.72*.85,false):art.frame('yuri_north_jump',v.t/.72*.6,false);if(key)return{key,scale:root.TD_ASSAULT_ART.assets[key]?.drawScale??1,angle:0,action:'vault',dir:side};}
  if(p.pilot==='yuri'&&p.modernFoot&&!p.pseudo3D&&!p.dead&&!p.moving&&!p.action&&p.stance==='stand'&&!(p.stanceTransition?.t<.46)&&!p.prone&&!p.cover&&!p.roll&&!p.jump&&!p.scripted){const key=api.aimKey(p);if(key&&ART.get(key)){api.stats.aimDraws++;return{key,scale:1,angle:0,action:'vertical_aim',dir:p.sideFacing29};}}
  return pose(p);
 };
 function vaultTarget(p,G){const [dx,dy]=I.dir();if(!dx&&!dy)return null;const f=Math.abs(dx)>Math.abs(dy)?[Math.sign(dx),0]:[0,Math.sign(dy)];
  for(const s of G.structures){if(s.dead||!['od_barrier','od_bunker','od_bosswall','od_crate','od_wood'].includes(s.kind))continue;const r=s.rect,x=p.x+f[0]*34,y=p.y+f[1]*34;if(x<r.x0-10||x>r.x1+10||y<r.y0-10||y>r.y1+10)continue;
   const tx=f[0]?f[0]>0?r.x1+16:r.x0-16:p.x,ty=f[1]?f[1]>0?r.y1+16:r.y0-16:p.y;if(W.rects.some(q=>q!==r&&q.t==='b'&&tx>q.x0-10&&tx<q.x1+10&&ty>q.y0-10&&ty<q.y1+10))continue;
   return{x:p.x,y:p.y,tx,ty,t:0,wall:s,roll:false,prone:false};
  }return null;
 }
 const tick=TD.footTick;TD.footTick=function(p,G,dt){
  if(!p.dead&&!p.scripted&&!p.pseudo3D&&p.modernFoot){if(!p.vault29&&p.roll<=0&&p.jump<=0&&(I.tap('jump')||I.tap('reload')||I.tap('B')&&!I.state.directionalFire)){p.vault29=vaultTarget(p,G);if(p.vault29){p.cover=null;p.prone=false;p.action=null;p.firing=0;api.stats.vaults++;A.play('stylishDodge',.55);}}
   if(p.vault29){const v=p.vault29;v.t+=dt;p.inv=Math.max(0,p.inv-1);p.flash=Math.max(0,p.flash-dt);p.rollCd=Math.max(0,p.rollCd-dt);if(I.tap('X')&&p.rollCd<=0)v.roll=true;if(I.tap('prone'))v.prone=!v.prone;
    const u=M.clamp(v.t/.72,0,1),e=u*u*(3-2*u);p.x=M.lerp(v.x,v.tx,e);p.y=M.lerp(v.y,v.ty,e);p.jump=.65*(1-u);p.jumpZ=Math.sin(u*Math.PI)*48;p.moving=false;p.vx=p.vy=0;
    if(u===1){p.vault29=null;p.jump=p.jumpZ=0;p.prone=v.prone;p.stance=v.prone?'prone':I.down('cover')||I.down('C')?'crouch':'stand';if(p.stance==='crouch')api.stats.crouchLandings++;if(v.roll){p.roll=.5;p.rollCd=5;p.rollAim=M.angTo(v.x,v.y,v.tx,v.ty);p.rollProne=v.prone||I.down('prone');api.stats.rollLandings++;}p.poseT=0;}return;
   }
  }return tick(p,G,dt);
 };
 api.drawCover=function(ctx,s){
  if(!s.assault)return false;let key,scl=1;
  if(['od_barrier','od_bunker','od_bosswall','od_wood'].includes(s.kind)){key='e29_barrier';scl=s.type.hw*2/pack.assets[key].bodyWidth;}
  else if(s.kind==='od_wall'){key='e29_wall';scl=s.type.hh*2/pack.assets[key].bodyHeight;}
  else if(s.kind==='od_relay'){key='e29_relay';scl=.45;}
  else if(s.kind==='od_crate'){key='e29_crate';scl=.65;}
  else if(s.kind==='od_barrel'){key='e29_barrel';scl=.44;}
  else if(s.kind==='od_server'){key='e29_crate';scl=.45;}
  if(!key||!ART.get(key))return false;
  if(s.dead){art.draw(ctx,'pb19_cover_7',s.x,s.y+s.type.hh,{s:s.type.hw*2/152});return true;}
  art.draw(ctx,key,s.x,s.y+s.type.hh,{s:scl,flash:s.flash>0?s.flash/.12:0});
  return true;
 };
 const status=TD.CornerHUD26.status;TD.CornerHUD26.status=function(G,pseudo){if(G.player.vault29)return G.player.vault29.roll?'VAULT + ROLL':'VAULTING';if(G.escape29?.phase==='chute')return 'SLIDING';if(G.player.sideCover29)return G.player.peekExposed?'PEEK FIRE':'IN COVER';return status(G,pseudo);};
 const impact=TD.structureImpact;TD.structureImpact=function(G,s,...args){const result=impact(G,s,...args);if(result&&G.mission===3&&G.eshots.includes(s)){const p=G.player;if(Math.hypot(s.x-p.x,s.y-p.y)<125)TD.Cam.kick(2.2);A.play('impactMetal',.45);}return result;};
})(window);
