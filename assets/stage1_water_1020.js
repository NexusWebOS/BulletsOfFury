'use strict';
/* Bright Stage1 ocean. Keep the native frame-array contract for transition and
   shared-water callers; replace only the final Stage1 water blit. No runtime
   recoloring, per-frame canvas allocation, mask changes or collision changes. */
const S1W20={base:{frames:_liquidFrames,terrain:drawAnimTerrain,connector:connectorSurface,
 load:stageLoadBegin,warm:warmStage},arrays:new WeakSet(),draws:0,frame:0};
function s1w20Live(){return run.stage===1&&!tutLive();}
function s1w20Water(key){return key==='nlq2_water'||key==='nwl_water';}
function s1w20Clock(){return Math.max(0,efxClock);}
function s1w20Draw(scroll,speed,width,top){
 const A=S1W20_ART;if(!XART.rdy(A.key))return false;
 const im=XART.get(A.key),f=Math.floor(s1w20Clock()*A.fps)%A.frames,c=A.cells[f];
 const w=width||VW,yTop=top==null?viewTopY():top;
 const sy=Math.round(((scroll*speed)%A.height+A.height)%A.height);
 let y0=sy-A.height;while(y0>yTop-A.height)y0-=A.height;
 ctx.save();ctx.imageSmoothingEnabled=false;
 for(let y=y0;y<VH;y+=A.height)for(let x=0;x<w;x+=A.width)
  ctx.drawImage(im,...c,x,y,A.width,A.height);
 ctx.restore();S1W20.frame=f;S1W20.draws++;return true;
}
_liquidFrames=function(key){const a=S1W20.base.frames.apply(this,arguments);
 if(s1w20Live()&&s1w20Water(key)&&a)S1W20.arrays.add(a);return a;};
drawAnimTerrain=function(frames,scroll,speed,scale,fps,width){
 if(s1w20Live()&&frames&&S1W20.arrays.has(frames)&&s1w20Draw(scroll,speed,width))return true;
 return S1W20.base.terrain.apply(this,arguments);
};
connectorSurface=function(stage,joinY,width){
 if(s1w20Live()&&stage===1&&s1w20Water(entryConnCfg(stage).bed)&&
    s1w20Draw(joinY,1,Math.max(width,VW),0))return true;
 return S1W20.base.connector.apply(this,arguments);
};
stageLoadBegin=function(stage,keys){
 if(stage===1&&!tutLive())keys=[S1W20_ART.key,...(keys||[])];
 return S1W20.base.load.call(this,stage,keys);
};
warmStage=function(stage){if(stage===1&&!tutLive())XART.rdy(S1W20_ART.key);
 return S1W20.base.warm.apply(this,arguments);};
window.BOFSTAGE1WATER={get live(){return s1w20Live();},get phase(){return S1W20.frame;},
 get draws(){return S1W20.draws;},get ready(){return XART.rdy(S1W20_ART.key);},key:S1W20_ART.key};
