/* Yuri's authored upward fire, flat-ground slide and reversible cover poses. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,pack=root.TD_YURI32_ART,api=TD.Yuri32={build:'overdrive1015-yuri32-r1'};
 const pick=(name,u)=>{const q=pack.sequences['y32_'+name];return q?.frames[Math.min(q.frames.length-1,Math.max(0,Math.floor(u*q.frames.length)))];};
 api.upKey=p=>p.firing>0?pick('up_fire',Math.min(.999,(p.shotAge||0)/.12)):'y32_up_idle';
 const aim=TD.Combat29.aimKey;TD.Combat29.aimKey=function(p,angle=p.aim){return M.fwd(angle)[1]<-.96?api.upKey(p):aim(p,angle);};
 const step=TD.Escape29.step;TD.Escape29.step=function(G,dt){const p=G.player,was=p.slide29||0,moving=p.moving,low=p.stance==='crouch';
  if(!was&&TD.Input.tap('X')&&p.rollCd<=0)p.slideEntry32=moving&&!low?'run':'walk';
  step(G,dt);
  if(!was&&p.slide29>0)p.slideEntry32=moving&&!low?'run':'walk';
 };
 api.slideKey=function(p,e){const side=p.rollDir<0?'west':'east',t=Math.max(0,.65-(p.slide29||0));
  if(e.phase==='doorSlide')return pick('slide_hold_'+side,0);
  if(t<.34)return pick((p.slideEntry32==='run'?'run':'walk')+'_slide_'+side,t/.34);
  if(t<.43)return pick('slide_hold_'+side,0);
  return pick('slide_exit_'+side,(t-.43)/.22);
 };
 const pose=TD.Escape29.pose;TD.Escape29.pose=function(G){const p=G.player,e=G.escape29;
  if(!p.dead&&['corridor','escape','doorSlide'].includes(e.phase)&&!p.vault29&&!p.roll){
   if(p.slide29>0)return api.slideKey(p,e);
   if(p.sideCover29&&!p.prone){const side=p.sideFacing29||'east',backAgainst=side==='east'?p.sideCover29.x<p.x:p.sideCover29.x>p.x;
    // Back-contact poses apply when the object is behind the torso. Preserve
    // forward cover's existing over-the-top pose when the object is ahead.
    if(backAgainst){const bank=p.sideCover29.h>=76?'cover_peek_':'crouch_peek_';return pick(bank+side,M.clamp(p.peek29||0,0,.999));}
   }
  }
  return pose(G);
 };
})(window);
