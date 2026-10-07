"use strict";
/* Combat components remain opaque through disassembly and reassembly.
   The established transition controller still owns clocks, protection, saved
   modules, nine health pools, dialogue and the single campaign reward. */
const FT7={draws:0,last:null};
const FT7_BASE={morph:j3Morph,draw:r30DrawBoss};
function ft7CombatPose(b,draw){
 const S=b._r30,mode=S.mode,attack=S.attack,returning=S.returning,hidden=S.ghostHidden;
 // Some legacy pose functions select a different body outside fight mode.
 // Query the same idle combat rig without running any combat controller.
 S.mode='fight';S.attack=null;S.returning=null;
 try{return draw();}finally{S.mode=mode;S.attack=attack;S.returning=returning;S.ghostHidden=hidden;}
}
function ft7Nodes(b){return ft7CombatPose(b,()=>{
 const J=j3State(b),copied=J.mimic!=null&&J.mimic>0,rig=copied?fmcRig(b):r30Parts(b);
 return rig.filter(v=>!v.spec?.hidden&&!(v.p?.destroyed&&v.p.id!=='core')).map((v,i)=>{
  const cell=copied&&!v.spec?.legacy,sheet=cell?(v.spec?.sheet||f1003bDef(b).id):null;
  return{id:v.p?.id||String(i),kind:cell?'cell':'blit',key:cell?sheet:(v.spec?.legacy?v.spec.art:v.key),part:cell?v.spec?.art:null,
   x:v.x-b.x,y:v.y-b.y,w:v.w,h:v.h,rot:v.rot||0,z:v.z||0};
 }).sort((a,c)=>a.z-c.z);
});}
j3Morph=function(b,to){
 const J=j3State(b),pieces=J?.encounter===2?ft7Nodes(b):null,origin={x:b.x,y:b.y};
 const r=FT7_BASE.morph.apply(this,arguments);
 if(pieces&&b._r30.mode==='transform1003j')J.ft7={out:pieces,origin,destination:J.destination};
 return r;
};
function ft7Ease(v){v=clamp(v,0,1);return v*v*(3-2*v);}
function ft7PiecePose(v,index,u,out){
 const phase=out?ft7Ease((u-index*.012)/.88):ft7Ease((u-index*.014)/(.90-index*.014));
 const joined=out?1-phase:phase,angle=(out?1:-1)*(1-joined)*Math.PI*(v.id==='core'?.80:1.45),c=Math.cos(angle),s=Math.sin(angle);
 const bend=Math.sin(phase*Math.PI)*(out?26:18),side=Math.sign(v.x)||(index%2?1:-1);
 // Real modules first unlock, then corkscrew into a compact solid cluster.
 // On return the torso seats first, followed by limbs and independent tools.
 return{x:(v.x*c-v.y*s)*joined+side*bend,y:(v.x*s+v.y*c)*joined-Math.sin(phase*Math.PI)*(v.id==='core'?15:30),
  w:v.w*(.16+.84*joined),h:v.h*(.16+.84*joined),rot:v.rot+angle+side*Math.sin(phase*Math.PI)*.24};
}
function ft7PieceDraw(v,p,x,y){
 if(v.kind==='cell')return fmcCell(v.key,v.part,x+p.x,y+p.y,p.w,p.h,p.rot,1);
 return r30Blit(v.key,x+p.x,y+p.y,p.w,p.h,p.rot,1);
}
function ft7TransformDraw(b){
 const S=b._r30,J=j3State(b),out=S.mode==='transform1003j',u=clamp(S.t/(out?1.25:1.15),0,1),saved=J.ft7;
 const pieces=out?(saved?.out||ft7Nodes(b)):ft7Nodes(b),origin=saved?.origin||b;
 const travel=out?0:ft7Ease(u),x=lerp(origin.x,b.x,travel),y=lerp(origin.y,b.y,travel),envelope=Math.sin(Math.PI*(out?u*.5:.5+u*.5)),energy=ft7Ease(out?u/.15:(1-u)/.20);
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';
 ctx.save();ctx.globalAlpha=energy;
 if(typeof hc7HelixDraw==='function')hc7HelixDraw(b,x,y,270+envelope*100,310+envelope*75,false);
 if(typeof hc7VoidDraw==='function')hc7VoidDraw(b,x,y,85+envelope*140,.92);
 ctx.restore();
 const rendered=[];
 for(const [i,v]of pieces.entries()){
  const p=ft7PiecePose(v,i,u,out);ft7PieceDraw(v,p,x,y);
  rendered.push({id:v.id,key:v.key,part:v.part,x:x+p.x,y:y+p.y,w:p.w,h:p.h,rot:p.rot,alpha:1});
 }
 ctx.save();ctx.globalAlpha=energy;
 if(typeof hc7HelixDraw==='function')hc7HelixDraw(b,x,y,270+envelope*100,310+envelope*75,true);
 ctx.restore();
 ctx.restore();FT7.draws++;FT7.last={mode:S.mode,u,pieces:rendered};
}
r30DrawBoss=function(b){
 const J=j3State(b),S=b?._r30;
 if(J?.encounter===2&&['transform1003j','reveal1003j'].includes(S.mode))return ft7TransformDraw(b);
 if(J?.encounter===2&&S.mode==='dr5Monologue'){
  // Exactly the combat body, including its live articulated idle arms. The
  // existing world layer still owns the portrait, mouth, words and audio.
  ctx.save();ctx.globalAlpha=1;ft7CombatPose(b,()=>j3Body(b,1));ctx.restore();
  dr5EffectsDraw(b);FT7.draws++;FT7.last={mode:S.mode,combatBody:true};return;
 }
 return FT7_BASE.draw.apply(this,arguments);
};
