"use strict";
/* A coastal entrance followed by continuous northward city travel. Fixed
   authored streets in world coordinates; animated water has its own scroll. */
const CC21={base:{bg:stageXArenaDraw,ready:stageXArenaReady,src:stageXArenaSrcY,
 begin:beginStage,update:updatePlay,world:drawWorld},t:0,card:0,owner:null,draws:0};
XART._src[CC21_ART.key]=CC21_ART.path;
XART._src.cc21_card=CC21_ART.card;XART._src.r24_card=CC21_ART.card;
function cc21Live(){return typeof stageXArenaActive==='function'&&stageXArenaActive();}
stageXArenaReady=function(){return cc21Live()?XART.rdy(CC21_ART.key)&&XART.rdy(S1W20_ART.key):CC21.base.ready.apply(this,arguments);};
function cc21Water(W,top,h){const A=S1W20_ART;if(!XART.rdy(A.key))return;const f=Math.floor(CC21.t*12)%A.frames,c=A.cells[f],im=XART.get(A.key),size=224,phase=(CC21.t*15)%size;
 for(let y=top-phase-size;y<top+h;y+=size)for(let x=0;x<W;x+=size)ctx.drawImage(im,...c,x,y,size,size);}
function cc21Strip(im,v,rows,x,y,w,scale){let n=rows,at=v,out=y;const A=CC21_ART;
 while(n>.001){if(at>=0){const take=Math.min(n,A.h-at);if(take<=0)break;ctx.drawImage(im,0,at,A.w,take,x,out,w,take*scale);at+=take;out+=take*scale;n-=take;}
  else{const district=Math.floor(at/A.urban),local=((at%A.urban)+A.urban)%A.urban,flip=((district%2)+2)%2===1;
   const take=Math.min(n,A.urban-local,-at);if(take<=.001)break;
   if(flip){ctx.save();ctx.translate(x,out+take*scale);ctx.scale(1,-1);ctx.drawImage(im,0,A.urban-local-take,A.w,take,0,0,w,take*scale);ctx.restore();}
   else ctx.drawImage(im,0,local,A.w,take,x,out,w,take*scale);
   at+=take;out+=take*scale;n-=take;
  }
 }
}
stageXArenaSrcY=function(img){if(!cc21Live())return CC21.base.src.apply(this,arguments);const scale=worldWidth()/CC21_ART.w;return CC21_ART.h-viewH()/scale-CC21.t*CC21_ART.scroll;};
stageXArenaDraw=function(dt){if(!cc21Live())return CC21.base.bg.apply(this,arguments);if(!stageXArenaReady())return false;
 CC21.t+=Math.max(0,dt||0);const A=CC21_ART,W=worldWidth(),top=viewTopY(),h=viewH(),scale=W/A.w,sy=stageXArenaSrcY();
 ctx.save();ctx.imageSmoothingEnabled=false;cc21Water(W,top,h);cc21Strip(XART.get(A.key),sy,h/scale,0,top,W,scale);ctx.restore();_masterSrcY=sy*scale-top;CC21.draws++;return true;};
beginStage=function(){CC21.t=0;CC21.card=0;CC21.owner=null;return CC21.base.begin.apply(this,arguments);};
// The campaign's alternate Stage6 route lacks Rival24's dedicated entrance
// state. Give it a short protected card before its existing radio sequence.
updatePlay=function(dt){if(cc21Live()&&!Rival24.active&&run._gp4StageX){const owner=run._gp4StageX;
 if(CC21.owner!==owner){CC21.owner=owner;CC21.card=0;XART.rdy('cc21_card');Audio.SFX.alertBossIncoming?.();}
 if(CC21.card<3){CC21.card+=Math.min(.05,dt);return;}}
 return CC21.base.update.apply(this,arguments);};
function cc21Card(){const u=CC21.card;if(!(u>0&&u<3))return;const fade=Math.min(1,u/.25,(3-u)/.35),w=Math.min(viewW()*.92,600),h=w*.5,x=VW/2,y=PLAY.y+viewH()*.38;
 if(XART.rdy('cc21_card')){ctx.save();ctx.globalAlpha*=fade;ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get('cc21_card'),x-w/2,y-h/2,w,h);ctx.restore();return;}
 ctx.save();ctx.globalAlpha*=fade;ctx.fillStyle='rgba(1,5,12,.94)';ctx.fillRect(x-w/2-6,y-h/2-6,w+12,h+12);
 if(XART.rdy('r24_panel')){const im=XART.get('r24_panel');ctx.drawImage(im,x-w/2,y-h/2,w,h);}
 const text=(s,dy,size,color)=>{const f=window.BOF_UI_FACE||'game';bmfDrawOn(ctx,f,s,x,y+dy,size,'center',color);};
 text('STAGE X',-h*.27,Math.min(22,w*.046),'#79e5ff');text('SEABREAK CITY',-h*.02,Math.min(26,w*.055),'#ffffff');text('COASTAL FRONT',h*.23,Math.min(13,w*.027),'#ffcb73');ctx.restore();}
drawWorld=function(dt){const r=CC21.base.world.apply(this,arguments);if(cc21Live()&&!Rival24.active){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);cc21Card();ctx.restore();}return r;};
globalThis.BOF_COASTAL_CITY=CC21;
