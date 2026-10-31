/* Authored slide twists, complete shoulder roll, and front-facing floor fire. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,pack=root.TD_YURI31_ART,api=TD.Yuri31={build:'overdrive1015-yuri31-r1'};
 const pick=(name,u)=>{const q=pack.sequences[name];return q?.frames[Math.min(q.frames.length-1,Math.max(0,Math.floor(u*q.frames.length)))];};
 api.rollKey=function(p,side){return pick('y31_roll_'+(p.rollProne?'prone_':'')+side,M.clamp((.5-p.roll)/.5,0,1));};
 api.downKey=p=>p.firing>0?pick('y31_down_fire',Math.min(.999,(p.shotAge||0)/.12)):'y31_down_idle';
 api.update=function(G,dt){const e=G.escape29,p=G.player;if(!e)return;
  if(e.phase==='chute'||e.phase==='hinge'){
   const dx=e.cursor.x-p.x,dy=e.cursor.y-(p.y-45);e.slideFacing31??=0;
   // Hysteresis keeps the shoulders from flickering at the left/right threshold.
   if(dx<-44)e.slideFacing31=1;else if(dx>-18)e.slideFacing31=0;
   const at=e.slideTurn31||0,step=dt/.34;e.slideTurn31=M.clamp(at+Math.sign(e.slideFacing31-at)*Math.min(step,Math.abs(e.slideFacing31-at)),0,1);
  }else{e.slideTurn31=0;e.slideFacing31=0;}
 };
 TD.Escape29.slidePose=function(G){const e=G.escape29,p=G.player;
  if((e.slideTurn31||0)>0)return pick('y31_slide_turn_east',Math.min(.999,e.slideTurn31));
  const dx=e.cursor.x-p.x,dy=e.cursor.y-(p.y-45);
  if(dy>25)return'e29_slide_down';if(Math.abs(dx)<60)return'e29_slide_up';
  return pick('y31_slide_turn_east',0);
 };
 const oldAim=TD.Combat29.aimKey;
 TD.Combat29.aimKey=function(p,angle=p.aim){const f=M.fwd(angle);if(f[1]>.96)return api.downKey(p);return oldAim(p,angle);};
 const oldPose=TD.Escape29.pose;
 TD.Escape29.pose=function(G){const p=G.player,e=G.escape29;if(!p.dead){
  if(p.roll>0)return api.rollKey(p,(p.rollDir||0)<0?'west':(p.rollDir||0)>0?'east':p.sideFacing29||'east');
  if(p.prone&&['corridor','escape'].includes(e.phase)){
   // The lowering transition is not a crawl loop: retain only its grounded tail.
   const q=root.TD_ESCAPE29_ART.sequences['e29_prone_'+(p.sideFacing29||'east')];
   return q.frames[p.moving?11+Math.floor((p.sideGait29||0)*20)%5:15];
  }
  if(e.phase==='hatch'&&p.freeAim)return api.downKey(p);
 }return oldPose(G);};
 const foot=TD.footPose;
 TD.footPose=function(p){if(p.pilot==='yuri'&&p.modernFoot&&!p.pseudo3D&&!p.dead&&p.roll>0&&Math.abs(Math.sin(p.rollAim||0))>.5){const side=Math.sin(p.rollAim)>0?'west':'east',key=api.rollKey(p,side);return{key,scale:1,angle:0,action:'complete_roll',dir:side};}return foot(p);};
})(window);
