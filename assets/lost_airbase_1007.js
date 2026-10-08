"use strict";
/* Authored abandoned desert airbase. One native PNG powers the entire stage and
   continuous pursuit; alternating vertical reflections join identical edge rows.
   This replaces the terrain renderer only. Wave/spawn progression stays mapScroll. */
const LA1007={key:'la1007_airbase',path:'assets/game/levels/stage_04/stage/hardcorps_1007/stage4_airbase.png',
 sourceW:1024,sourceH:1536,worldW:680,scrollLen:3568,scroll:0,mapPrev:null,draws:0,tiles:[]};
XART._src[LA1007.key]=LA1007.path;
// Register the loose master for data-only tools as well as runtime XART.
BOFX.img[LA1007.key]=LA1007.path;
const LA1007_BASE={cfg:_levelCfg,draw:drawLevelMaster,begin:beginStage,src:levelSrcY,drive:tankDrivable};
_levelCfg=function(){const c=LA1007_BASE.cfg.apply(this,arguments);if(run.stage!==4||!c)return c;
 return{...c,master:LA1007.key,plateW:LA1007.worldW,scrollLen:LA1007.scrollLen,liquid:null,
  continuousBoss:true,loopMaster:false,props:[],fill:'#a86b28',lostAirbase1007:true};
};
beginStage=function(n){if(n===4){LA1007.scroll=0;LA1007.mapPrev=null;LA1007.tiles=[];_groundSrcPrev=null;_groundDy=0;XART.rdy(LA1007.key);}
 return LA1007_BASE.begin.apply(this,arguments);
};
function la1007TileHeight(){return LA1007.sourceH*LA1007.worldW/LA1007.sourceW;}
function la1007Chase(){return !!(boss&&((bossActive&&!boss.dead)||(boss._cinDeath&&boss.dying<9.8)));}
function la1007TileAt(y){const h=la1007TileHeight(),mapY=y-LA1007.scroll,n=Math.floor(mapY/h),u=mapY-n*h;return{n,flip:Math.abs(n%2)===1,row:Math.abs(n%2)===1?(h-u)*LA1007.sourceH/h:u*LA1007.sourceH/h};}
drawLevelMaster=function(dt){
 if(run.stage!==4)return LA1007_BASE.draw.apply(this,arguments);
 if(!XART.rdy(LA1007.key))return LA1007_BASE.draw.apply(this,arguments);
 dt=Number.isFinite(dt)&&dt>=0?Math.min(dt,.1):0;
 const mini=!!(subBossActive&&subBoss&&!subBoss.dead&&!SUBBOSS_NO_HOLD[4]);
 const real=!!(bossActive&&boss&&!boss.dead),held=real||mini;
 if(held)_bossHold=Math.min(1,(_bossHold||0)+dt*1.6);else _bossHold=Math.max(0,(_bossHold||0)-dt*1.6);
 const before=mapScroll;mapScroll=Math.min(LA1007.scrollLen,mapScroll+dt*40*(1-_bossHold));
 _lastScrollDy=mapScroll-_prevMapScroll;_prevMapScroll=mapScroll;
 if(LA1007.mapPrev==null){LA1007.scroll=before;LA1007.mapPrev=before;}
 // Keep visual continuity at engagement and after death. The chase moves faster
 // without consuming waves, ground spawn positions, or the campaign exit gate.
 if(la1007Chase()){
  const mode=boss?._s4war?.mode,spd=mode==='flyaway'?620:mode==='swerve'?560:480;
  LA1007.scroll+=dt*spd;_stage4BossRoadScroll=LA1007.scroll;
 }else{LA1007.scroll+=mapScroll-LA1007.mapPrev;_stage4BossRoadScroll=0;}
 LA1007.mapPrev=mapScroll;
 const im=XART.get(LA1007.key),h=la1007TileHeight(),top=viewTopY(),height=viewH(),first=Math.floor((top-LA1007.scroll)/h),last=Math.ceil((top+height-LA1007.scroll)/h);
 LA1007.tiles=[];ctx.save();ctx.imageSmoothingEnabled=false;ctx.beginPath();ctx.rect(0,top,LA1007.worldW,height);ctx.clip();
 for(let n=first;n<last;n++){
  const y=n*h+LA1007.scroll,flip=Math.abs(n%2)===1;ctx.save();ctx.translate(0,y);
  if(flip){ctx.translate(0,h);ctx.scale(1,-1);}ctx.drawImage(im,0,0,LA1007.worldW,h);ctx.restore();
  LA1007.tiles.push({n,y,h,flip});LA1007.draws++;
 }
 ctx.restore();
 // Publish unwrapped world travel. Modulo source rows would fling ground decals
 // at every tile seam, although the image itself looked continuous.
 _masterSrcY=-LA1007.scroll;_groundPublish(-LA1007.scroll);return true;
};
levelSrcY=function(){return run.stage===4?-LA1007.scroll:LA1007_BASE.src.apply(this,arguments);};
tankDrivable=function(wx,levelY,failOpen){
 if(run.stage!==4)return LA1007_BASE.drive.apply(this,arguments);
 // Measured clear paved spine in the generated source: x=334..690. A 20px
 // source inset avoids sand shoulders and static wreckage on service aprons.
 const x=wx*LA1007.sourceW/LA1007.worldW;return Number.isFinite(x+levelY)&&x>=354&&x<=670;
};
