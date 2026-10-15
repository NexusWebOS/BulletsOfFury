"use strict";
/* Approved BOF art in the Stage 8 void transition and homeward portal.
   Encounter owners retain their timing, ship motion and combat boundaries. */
const PL11_GAME={base:{load:stageLoadBegin,reform:pt11ReformDraw,intro:on5IntroDraw,cell:dr5Cell},
  banks:['black_void','blue_rift'],draws:0,last:null};
for(const entry of Object.values(PL11_ART))for(const phase of PL11.phases)
  for(const f of entry[phase].frames)XART._src[f.key]=f.path;
Object.assign(XART._src,PL11.parts);
stageLoadBegin=function(n,keys){return PL11_GAME.base.load.call(this,n,n===8?
  [...(keys||[]),...PL11_GAME.banks.flatMap(bank=>PL11.keys(bank))]:keys);};
function pl11World(bank,pose,x,y,size,alpha=1){
  if(!PL11.ready(bank,XART))return false;
  const drawn=PL11.draw(ctx,pose,x,y,size,key=>XART.get(key),alpha);
  if(drawn){PL11_GAME.draws++;PL11_GAME.last={bank,phase:pose.phase,from:pose.from,to:pose.to,mix:pose.mix,rotation:pose.rotation,x,y,size};}
  return drawn;
}
function pl11VoidWorld(Q,size){return pl11World('black_void',PL11.sequence('black_void',Q.t),Q.x,Q.y,size);}
pt11ReformDraw=function(b){
  const J=j3State(b);if(J?.encounter!==1)return PL11_GAME.base.reform.apply(this,arguments);
  const Q=J.pt11Portal??={x:b.x,y:b.y,t:0,size:340};
  if(!pl11VoidWorld(Q,Q.size))return PL11_GAME.base.reform.apply(this,arguments);
};
on5IntroDraw=function(b){
  const S=b?._r30,J=j3State(b),Q=J?.pt11Portal;
  if(S?.mode!=='voidIntro1005'||!Q||!PL11.ready('black_void',XART))return PL11_GAME.base.intro.apply(this,arguments);
  const t=S.t,u=clamp(t/2.1,0,1),ease=u*u*(3-2*u);
  // Continue Q.t from reformation. Multiplying accumulated time by the new
  // phase's t made the idle animation jump and accelerate at this handoff.
  if(t<2.6)pl11VoidWorld(Q,lerp(Q.size,Math.max(worldWidth(),viewH())*3.3,ease));
  const dark=t<2.1?clamp((t-.9)/1.0,0,1):clamp((3.7-t)/1.6,0,1);
  if(dark>0){ctx.save();ctx.globalAlpha=dark;ctx.fillStyle='#000';ctx.fillRect(-64,viewTopY()-64,worldWidth()+128,viewH()+128);ctx.restore();}
  if(t>=3.9){ctx.save();const k=.25+.75*clamp((t-3.9)/.8,0,1);ctx.translate(b.x,b.y);ctx.scale(k,k);ctx.translate(-b.x,-b.y);j3Body(b,1);ctx.restore();}
};
dr5Cell=function(name,f,x,y,w,h=w,rot=0,alpha=1){
  if(name==='portal'&&boss?._r30){
    const S=boss._r30;
    const timing=S.mode==='dr5Portal'?{form:2,loop:4.2,close:1.4}:
      S.mode==='reunion'&&dr5State(boss).deathStarted?{form:0,loop:.8,close:2}:null;
    if(timing&&pl11World('blue_rift',PL11.sequence('blue_rift',S.t,timing),x,y,w,alpha))return true;
  }
  return PL11_GAME.base.cell.apply(this,arguments);
};
