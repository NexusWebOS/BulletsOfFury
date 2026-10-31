/* Yuri cover continuity. Uses the approved body banks and their muzzle roots. */
(function(root){
 'use strict';
 const TD=root.TD,M=TD.M,I=TD.Input,P=root.TD_ASSAULT_ART;
 const Y=TD.Yuri36={build:'overdrive1016-cover36-r1',stats:{crawlFrames:0,coverFrames:0,transitions:0}};
 const active=p=>p.pilot==='yuri'&&p.modernFoot&&!p.pseudo3D&&!p.sideScroll&&!p.dead&&!p.scripted;
 const blocked=p=>p.action||p.roll>0||p.jump>0||p.vault29;
 const wrapped=n=>(n%1+1)%1;
 const pose=(bank,index,action,dir)=>{const q=P.sequences[bank];if(!q)return null;const n=M.clamp(index,0,q.frames.length-1),key=q.frames[n];if(!ART.get(key))return null;return{key,scale:P.assets[key]?.drawScale??1,angle:0,action,dir,bank,index:n};};
 function lateral(p){
  const s=Math.sin(p.aim),side=s<0?'east':'west';
  return Math.abs(s)>.78?side:p.lowSide36&&Math.abs(s)>.60?p.lowSide36:null;
 }
 Y.coverSpec=function(p){
  const c=p.cover;if(!c||c.dead||!c.rect||p.prone||p.blindfire)return null;
  const r=c.rect,sy=p.y>=r.y0-12&&p.y<=r.y1+12,side=sy&&p.x>=r.x1?'east':sy&&p.x<=r.x0?'west':null;
  const f=M.fwd(p.aim),outward=side&&f[0]*(side==='east'?1:-1)>.72;
  // The side banks press the back into the actual contacted edge. Their guns
  // point away from that edge; retain directional banks for other aim angles.
  if(side&&((p.peek||0)===0&&!p.peekExposed||outward)){
   const column=c.kind==='od_column36',bank='y32_'+(column?'cover_peek_':'crouch_peek_')+side;
   return{bank,dir:side,out:column?.475:.36,back:column?.475:.32,column};
  }
  // Low north-facing wall: the held/extended pose stays in the same bank.
  // Switching to generic fire at full exposure used to change body and root.
  if(c.kind!=='od_column36'&&f[1]<-.72)return{bank:'yuri_north_peek',dir:'north',out:.36,back:.32,column:false};
  return null;
 };
 const tick=TD.footTick;
 TD.footTick=function(p,G,dt){
  if(active(p)&&!blocked(p)){
   p.lowSide36=lateral(p);
   const spec=Y.coverSpec(p);
   if(spec){
    const expose=I.down('A')&&!I.down('retina');
    p.coverReturn36=!expose;
    // Infantry owns cover eligibility, shots and exposure. Adjust its clock
    // before that owner runs, so bullets cannot precede the authored pop-out.
    const target=M.clamp((p.peek||0)+dt*(expose?.24/spec.out:-.24/spec.back),0,.24);
    p.peek=target-(expose?dt:-dt*1.5);
   }
  }
  const result=tick(p,G,dt);
  if(active(p))p.lowSide36=lateral(p);
  return result;
 };
 const previous=TD.footPose;
 TD.footPose=function(p){
  if(!active(p)||blocked(p))return previous(p);
  const side=lateral(p),transition=p.stanceTransition;
  if(side&&transition&&transition.t<.46){
   // e29_prone's first twelve frames lower the body; they are a transition,
   // not locomotion. Reverse the same drawings when standing back up.
   let n=Math.min(11,Math.floor(transition.t/.46*12));
   if(transition.to==='stand')n=11-n;
   const z=pose('e29_prone_'+side,n,'prone_transition',side);
   if(z){Y.stats.transitions++;return z;}
  }
  if(side&&p.stance==='prone'&&!p.peekExposed&&!p.blindfire){
   // Only these grounded frames are a crawl. Previously the full 0..15 bank
   // replayed stand -> kneel -> prone every stride, visibly inflating Yuri.
   const n=p.moving?11+Math.floor(wrapped(p.gaitPhase||0)*5):15;
   const z=pose('e29_prone_'+side,n,p.moving?'crawl':'prone_hold',side);
   if(z){Y.stats.crawlFrames++;return z;}
  }
  const spec=Y.coverSpec(p);
  if(spec&&!(transition?.t<.46)){
   const q=P.sequences[spec.bank],u=M.clamp((p.peek||0)/.24,0,1);
   let z;
   if(spec.dir==='north'&&u===0&&p.moving){
    const phase=wrapped((p.gaitPhase||0)*(p.vx<0?-1:1));
    z=pose('yuri_north_crouch_sidestep',Math.floor(phase*8),'cover_sidestep','north');
   }else if(spec.dir!=='north'&&u===0&&p.moving){
    const bank=spec.column?'y28_'+spec.dir+'_up_step':'e29_crouch_'+spec.dir,q=P.sequences[bank];
    if(q){const phase=wrapped((p.gaitPhase||0)*(spec.column&&p.vy>0?-1:1));z=pose(bank,Math.floor(phase*q.frames.length+1e-8),'cover_sidestep',spec.dir);}
   }else if(q){
    let n=Math.min(q.frames.length-1,Math.floor(u*q.frames.length+1e-8));
    if(spec.bank.startsWith('y32_crouch_peek_')){
     // The authored last four drawings are withdrawal, not full exposure.
     // Finish them before returning through the matching tucked-rifle poses.
     const back=[13,14,15,16,4,3,2,1,0];
     n=u===0?0:p.coverReturn36?back[Math.min(back.length-1,Math.floor((1-u)*back.length))]:Math.min(12,Math.floor(u*13+1e-8));
    }
    z=pose(spec.bank,n,spec.column?'back_cover':u>0?'cover_peek':'cover_hold',spec.dir);
   }
   if(z){Y.stats.coverFrames++;return z;}
  }
  return previous(p);
 };
 // Existing drawFoot and footVisualSocket both ask footPose for this same key:
 // no silhouette shadow, per-frame resizing, synthetic limbs or muzzle offset.
})(window);
