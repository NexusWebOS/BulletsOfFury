'use strict';
/* Molten Stage2 lava. Keep the native frame-array contract for transition and
   shared-water callers; replace only the final Stage2 water blit. No runtime
   recoloring, per-frame canvas allocation, mask changes or collision changes. */
const S2L20={base:{frames:_liquidFrames,terrain:drawAnimTerrain,connector:connectorSurface,
 load:stageLoadBegin,warm:warmStage},arrays:new WeakSet(),draws:0,frame:0};
function s2l20Live(){return run.stage===2&&!tutLive();}
function s2l20Water(key){return key==='nlq3_lava'||key==='nlq2_lava'||key==='nwl_lava';}
function s2l20Clock(){return Math.max(0,efxClock);}
function s2l20Draw(scroll,speed,width,top){
 const A=S2L20_ART;if(!XART.rdy(A.key))return false;
 const im=XART.get(A.key),f=Math.floor(s2l20Clock()*A.fps)%A.frames,c=A.cells[f];
 const w=width||VW,yTop=top==null?viewTopY():top;
 const sy=Math.round(((scroll*speed)%A.height+A.height)%A.height);
 let y0=sy-A.height;while(y0>yTop-A.height)y0-=A.height;
 ctx.save();ctx.imageSmoothingEnabled=false;
 for(let y=y0;y<VH;y+=A.height)for(let x=0;x<w;x+=A.width)
  ctx.drawImage(im,...c,x,y,A.width,A.height);
 ctx.restore();S2L20.frame=f;S2L20.draws++;return true;
}
_liquidFrames=function(key){const a=S2L20.base.frames.apply(this,arguments);
 if(s2l20Live()&&s2l20Water(key)&&a)S2L20.arrays.add(a);return a;};
drawAnimTerrain=function(frames,scroll,speed,scale,fps,width){
 if(s2l20Live()&&frames&&S2L20.arrays.has(frames)&&s2l20Draw(scroll,speed,width))return true;
 return S2L20.base.terrain.apply(this,arguments);
};
connectorSurface=function(stage,joinY,width){
 if(s2l20Live()&&stage===2&&s2l20Water(entryConnCfg(stage).bed)&&
    s2l20Draw(joinY,1,Math.max(width,VW),0))return true;
 return S2L20.base.connector.apply(this,arguments);
};
stageLoadBegin=function(stage,keys){
 if(stage===2&&!tutLive())keys=[S2L20_ART.key,...(keys||[])];
 return S2L20.base.load.call(this,stage,keys);
};
warmStage=function(stage){if(stage===2&&!tutLive())XART.rdy(S2L20_ART.key);
 return S2L20.base.warm.apply(this,arguments);};
window.BOFSTAGE2LAVA={get live(){return s2l20Live();},get phase(){return S2L20.frame;},
 get draws(){return S2L20.draws;},get ready(){return XART.rdy(S2L20_ART.key);},key:S2L20_ART.key};
