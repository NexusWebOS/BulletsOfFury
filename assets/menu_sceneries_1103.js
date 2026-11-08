"use strict";
// MS113: authored menu environments. Only source clipping and native translation.
const MS113={enabled:new URLSearchParams(location.search).get('menubg')!=='classic',epoch:performance.now(),draws:{},last:null,
 scenes:{orbit:{front:'orbit_front',rate:.012,near:.021,phase:-.7},command:{front:'industrial_front',rate:.009,near:.015,phase:-.8},hangar:{front:'industrial_front',rate:.008,near:.014,phase:0},forge:{front:'industrial_front',rate:.008,near:.014,phase:-1},hq:{front:'coastal_front',rate:.007,near:.012,phase:.65},vault:{front:'industrial_front',rate:.008,near:.014,phase:-.7}},
 states:{title:'orbit',modesel:'command',diff:'command',password:'vault',credits:'orbit',options:'vault',help:'vault',achievements:'vault',vault:'vault',armory:'forge',forge:'forge',forging:'forge',forged:'forge',loadout:'forge',supplies:'forge',powers:'forge',camphub:'hq'},
 base:{canon:drawCanonBackdrop,boot:drawBootBackdrop,title:drawTitleBackdrop,pilot:drawPilotBG,space:scrollSpaceBG,arsenal:arsenalBackdrop,pauseOpen:sm22Open,pauseClose:sm22Close}};
for(const key of [...Object.keys(MS113.scenes),'industrial_front','orbit_front','coastal_front'])XART._src['ms113_'+key]='assets/game/shared/ui/menu_sceneries_1103/'+key+'.png';
for(const key of Object.keys(MS113.scenes))XART._src['ms113_'+key+'_portrait']='assets/game/shared/ui/menu_sceneries_1103/'+key+'_portrait.png';
function ms113Warm(scene,portrait=false){const q=MS113.scenes[scene];if(!q)return;for(const k of [scene,q.front,...(portrait?[scene+'_portrait']:[])])XART.rdy('ms113_'+k);}
function ms113Scene(){return MS113.states[state]||null;}
function menuScenery113(scene=ms113Scene(),W=VW,H=VH){
 if(!MS113.enabled||!MS113.states[state]||!MS113.scenes[scene])return false;
 const q=MS113.scenes[scene],portrait=H>512,key='ms113_'+scene+(portrait?'_portrait':''),front='ms113_'+q.front;ms113Warm(scene,portrait);
 if(!XART.rdy(key)||!XART.rdy(front))return false;if(H>(portrait?1280:512))return false;
 const a=XART.get(key),b=XART.get(front),aw=a.naturalWidth||a.width,ah=a.naturalHeight||a.height,bw=b.naturalWidth||b.width,bh=b.naturalHeight||b.height,t=(performance.now()-MS113.epoch)/1000,
  range=Math.max(0,aw-W),nearRange=Math.max(0,bw-W),x=-Math.round(range*(.5+.5*Math.sin(t*q.rate+(q.phase||0)))),nx=-Math.round(nearRange*(.5+.5*Math.sin(t*q.near+(q.phase||0)+.4))),sy=Math.max(0,Math.floor((ah-H)*.58));
 ctx.save();ctx.imageSmoothingEnabled=false;
 // Copy authored pixels at 1:1. A larger viewport repeats complete source tiles.
 for(let px=x;px<W;px+=aw)ctx.drawImage(a,0,sy,aw,Math.min(H,ah-sy),px,0,aw,Math.min(H,ah-sy));
 // Keep near-camera ceiling and lower edges at their native authored height.
 for(let px=nx;px<W;px+=bw){ctx.drawImage(b,0,0,bw,bh/2,px,0,bw,bh/2);ctx.drawImage(b,0,bh/2,bw,bh/2,px,H-bh/2,bw,bh/2);}
 ctx.restore();MS113.draws[scene]=(MS113.draws[scene]||0)+1;MS113.last={state,scene,W,H,key,front,x,nx,sy,time:t,portrait};return true;
}
drawCanonBackdrop=function(){if(menuScenery113())return true;return MS113.base.canon.apply(this,arguments);};
drawBootBackdrop=function(){if(menuScenery113())return true;return MS113.base.boot.apply(this,arguments);};
scrollSpaceBG=function(){if(menuScenery113())return true;return MS113.base.space.apply(this,arguments);};
drawTitleBackdrop=function(){if(!menuScenery113('orbit'))return MS113.base.title.apply(this,arguments);drawLogo(VW/2,60,.34);};
drawPilotBG=function(){return MS113.base.pilot.apply(this,arguments);};
arsenalBackdrop=function(W,H,bays){
 if(!MS113.enabled||!MS113.states[state])return MS113.base.arsenal.apply(this,arguments);ms113Warm('forge');if(!XART.rdy('ms113_forge')||!XART.rdy('ms113_industrial_front'))return MS113.base.arsenal.apply(this,arguments);
 const result=MS113.base.arsenal.call(this,W,H,false);if(!result)return result;
 // The original authored frame/header/footer remain intact around their aperture.
 ctx.save();ctx.beginPath();ctx.rect(W*.069,H*.216,W*.862,H*.586);ctx.clip();menuScenery113('forge',W,H);ctx.restore();
 const old=XART.rdy('forge_loadout_0918')?XART.get('forge_loadout_0918'):null;
 if(bays&&old){const P=LOADOUT_PLATE;for(let i=0;i<6;i++)ctx.drawImage(old,old.width*(.080+i*.143),old.height*.288,old.width*.126,old.height*.23,P.bayX[i]*W-2,P.bayY*H-2,P.bayW*W+4,P.bayH*H+4);ctx.drawImage(old,old.width*.070,old.height*.644,old.width*.86,old.height*.142,P.pool[0]*W,P.pool[1]*H,P.pool[2]*W,P.pool[3]*H);}
 return true;
};
sm22Open=function(){MS113.pauseAt=performance.now();return MS113.base.pauseOpen.apply(this,arguments);};
sm22Close=function(){if(MS113.pauseAt!=null){MS113.epoch+=performance.now()-MS113.pauseAt;MS113.pauseAt=null;}return MS113.base.pauseClose.apply(this,arguments);};
ms113Warm('orbit');
globalThis.BOF_MENU_SCENERIES_1103=MS113;
