/* Upward cross-step locomotion while independently aiming left/right. */
(function(root){
 'use strict';
 const TD=root.TD,pack=root.TD_YURI28_ART,oldPose=TD.footPose;
 const api=TD.Yuri28={selected:0};
 api.bank=function(p){
  if(p.pilot!=='yuri'||!p.modernFoot||p.pseudo3D||p.dead||p.action||p.cover||p.roll>0||p.jump>0||p.stance!=='stand'||p.stanceTransition?.t<.46||!p.moving)return null;
  if(p.vy>=-.05||Math.abs(p.vy)<Math.abs(p.vx)*1.2||Math.abs(Math.sin(p.aim))<.90)return null;
  const dir=Math.sin(p.aim)<0?'east':'west';return'y28_'+dir+'_'+(p.firing>0?'up_fire':'up_step');
 };
 TD.footPose=function(p){const bank=api.bank(p),q=bank&&pack.sequences[bank];
  if(!q)return oldPose(p);const phase=((p.gaitPhase||0)%1+1)%1,index=Math.floor(phase*q.frames.length)%q.frames.length,key=q.frames[index];
  if(!ART.get(key))return oldPose(p);api.selected++;return{key,angle:0,scale:1,action:q.action,dir:q.direction,phase,index,bank};
 };
})(window);
