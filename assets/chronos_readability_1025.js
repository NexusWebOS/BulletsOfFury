"use strict";
// Native authored dialogue plate and FOV owners; no combat pause or extra reticles.
const C34={base:{world:drawWorld,draw:hammerBossDraw},radio:null,warnings:0};
function c34Radio(){const q=ui20Radio();C34.radio=null;if(run.stage!==5||!q||(/CHRONOS/i.test(q.who)&&!fb2IntroActive()))return;
 const w=VW*.9,h=94,x=(VW-w)/2,y=VH-h-12;
 dlgBox({who:/^DECKER/i.test(q.who)?'DECKER':q.who,full:q.text,shown:q.text,pw:w,ph:h,fixedHeight:true,x,y,portraitKey:/^(CHRONOS|\?\?\?)$/i.test(q.who)?'fb1002_hammer_portrait':undefined,portrait:/^DECKER/i.test(q.who)?'decker':q.who.toLowerCase(),maxBottom:VH-8});
 C34.radio={...q,x,y,w,h};}
drawWorld=function(dt){const r=C34.base.world.apply(this,arguments);if(state===GS.PLAY)c34Radio();return r;};
hammerBossDraw=function(b){const r=C34.base.draw.apply(this,arguments);if(!c25Own(b)||b.dead||c30Own(b))return r;
 const h=b._hammer,P=h.c27Combo;C34.warnings=0;
 // C27 owns this combo outright, so the old pair renderer is never called.
 if(P){if(P.furiousMelee24)C25.base.pair(b,P);else if(P.clock<1.2){const at=hammerHeadPoint(b);C25.base.warning(P,{x:at.x,y:at.y,ex:P.target.x,ey:P.target.y,width:124,progress:clamp(P.clock/.85,0,1),fieldOnly:true});}C34.warnings++;}
 if(['whirl_warn','spin','revenge_charge'].includes(h.state)){
  const at=hammerHeadPoint(b),p=targetShip(b.x,b.y),dur=h.state==='whirl_warn'?1.1:h.state==='spin'?HAMMER_SPIN_TIME:2;
  C25.base.warning(b,{x:at.x,y:at.y,ex:p.x,ey:p.y,width:h.state==='whirl_warn'?150:90,progress:clamp(h.t/dur,0,1),fieldOnly:true});C34.warnings++;}
 return r;};
