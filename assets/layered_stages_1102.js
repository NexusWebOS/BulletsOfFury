'use strict';
/* LS112: approved Stage2-9/X source layers. Native encounter clocks, rewards,
   waves and special boss arenas stay with their existing owners. Art is authored
   offline: no runtime palette/alpha/rotation/scale/compositing effects. */
const LS112={base:{cfg:_levelCfg,master:drawLevelMaster,begin:beginStage,load:stageLoadBegin,warm:warmStage,
 liquid:_liquidFrames,terrain:drawAnimTerrain,connector:connectorSurface,mask:_buildTankMask,drive:tankDrivable,src:levelSrcY,
 falls:drawLiquidFalls,signs:drawRoadSigns,clean:stage7CleanTerrain,sewer:fr28SewerMaster,
 loop6:bg6LoopDraw,realmLoop:fr27LoopTerrain,objects6:l6ObjsDraw,objects8:l8ObjsDraw,xdraw:stageXArenaDraw,xready:stageXArenaReady,
 highwayDirector:hm17Director,shoulder:hm17Shoulder,transition6:stage6TransitionBackgroundDraw},
 arrays:new Map(),masks:new Map(),draws:{},clock:{},stage:0,roadTravel:0,chaseTravel:0,xTravel:0,last:null};
for(const a of Object.values(LS112_ART.levels))XART._src[a.key]=a.path;
for(const a of Object.values(LS112_ART.banks))XART._src[a.key]=a.path;
for(const a of [LS112_ART.highway,LS112_ART.sewerExit])XART._src[a.key]=a.path;
// November6: Stage5 keeps its original starfield/space parallax, including launch and boss.
function ls112Live(n=run.stage){return Number(n)!==5&&!globalThis.LS112_OFF&&!(typeof tutLive==='function'&&tutLive())&&!!LS112_ART.levels[String(n)];}
function ls112Count(k){LS112.draws[k]=(LS112.draws[k]||0)+1;}
function ls112Keys(n){const a=LS112_ART.levels[String(n)];if(!a)return[];const bed=LS112_ART.materials[a.material];return[a.key,...(bed?[bed.key]:[]),...(n===4?[LS112_ART.tesla.key,LS112_ART.highway.key]:[]),...(n===7?[LS112_ART.sewerExit.key]:[])];}
function ls112Warm(n){for(const k of ls112Keys(n))XART.rdy(k);}
stageLoadBegin=function(n,keys){if(ls112Live(n))keys=[...(keys||[]),...ls112Keys(n)];return LS112.base.load.call(this,n,keys);};
warmStage=function(n){if(ls112Live(n))ls112Warm(n);return LS112.base.warm.apply(this,arguments);};
beginStage=function(n){const result=LS112.base.begin.apply(this,arguments);LS112.stage=n;LS112.roadTravel=LS112.chaseTravel=LS112.xTravel=0;LS112.clock={};LS112.last=null;
 if(ls112Live(n)){ls112Warm(n);_tankMask=null;_tankMaskKey=null;_groundSrcPrev=null;_groundDy=0;delete _wwCache[n];}return result;};
_levelCfg=function(stage=run.stage){const cfg=LS112.base.cfg.apply(this,arguments);if(!cfg||!ls112Live(stage))return cfg;const a=LS112_ART.levels[String(stage)];
 return{...cfg,master:a.key,plateW:a.w,h:a.h,scrollLen:a.nativeRange,liquid:a.material?'ls112:'+a.material:null,tile:1,fps:8,
  props:[],par:null,skipRows:null,staticMaster:false,loopMaster:a.repeat&&stage!==4,continuousBoss:true,lostAirbase1007:false,layered112:true};};
function ls112Frame(a,frame,x,y){if(!XART.rdy(a.key))return false;const f=((Math.floor(frame)%a.frames)+a.frames)%a.frames;
 ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),a.w,a.h);return true;}
function ls112Bed(name,width=worldWidth(),top=viewTopY(),height=viewH()){
 const a=LS112_ART.materials[name];if(!a||!XART.rdy(a.key))return false;
 const t=Math.max(0,efxClock),f=Math.floor(t*a.fps)%a.frames,x0=Math.floor((camLeftX()*.68)%a.w)-a.w,
  y0=Math.floor(top+(t*(name==='space'?5:12))%a.h)-a.h;
 for(let y=y0;y<top+height;y+=a.h)for(let x=x0;x<width;x+=a.w)ls112Frame(a,f,x,y);
 LS112.clock.bed={name,time:t,frame:f,x:x0,y:y0};ls112Count('bed-'+name);return true;
}
_liquidFrames=function(key){if(typeof key==='string'&&key.startsWith('ls112:')){if(!LS112.arrays.has(key))LS112.arrays.set(key,Object.assign([null],{ls112:key.slice(6)}));return LS112.arrays.get(key);}return LS112.base.liquid.apply(this,arguments);};
drawAnimTerrain=function(frames){if(frames?.ls112)return ls112Bed(frames.ls112,arguments[5]||worldWidth());return LS112.base.terrain.apply(this,arguments);};
connectorSurface=function(stage,joinY,width){if(ls112Live(stage)){const a=LS112_ART.levels[String(stage)];if(a.material&&ls112Bed(a.material,Math.max(width||0,VW),0,VH))return true;}return LS112.base.connector.apply(this,arguments);};
function ls112Window(a,source,top=viewTopY(),height=viewH(),repeat=false){
 if(!XART.rdy(a.key))return false;const im=XART.get(a.key),H=a.h;let sy=Math.floor(source),dy=Math.round(top),left=Math.ceil(height);
 if(!repeat){if(sy<0){const n=Math.min(left,-sy);sy+=n;dy+=n;left-=n;}left=Math.min(left,H-sy);if(left>0)ctx.drawImage(im,0,sy,a.w,left,0,dy,a.w,left);return true;}
 sy=((sy%H)+H)%H;
 while(left>0){const n=Math.min(left,H-sy);ctx.drawImage(im,0,sy,a.w,n,0,dy,a.w,n);dy+=n;left-=n;sy=0;}
 return true;
}
function ls112Power(source,top=viewTopY()){
 const a=LS112_ART.tesla,y=Math.round(a.y-source+top);if(y+a.h<viewTopY()||y>VH)return;
 const f=Math.floor(Math.max(0,efxClock)*a.fps)%a.frames;if(ls112Frame(a,f,a.x,y)){LS112.clock.tesla={frame:f,y,source,sockets:a.sockets.map(([x,Y])=>({x,y:Math.round(Y-source+top)}))};ls112Count('tesla');}
}
function ls112Road(dt){
 const a=LS112_ART.levels['4'];if(!ls112Keys(4).every(k=>XART.rdy(k)))return false;
 dt=Number.isFinite(dt)?Math.max(0,Math.min(dt,.1)):0;
 const held=!!(bossActive&&boss&&!boss.dead)||!!(subBossActive&&subBoss&&!subBoss.dead&&!SUBBOSS_NO_HOLD[4]);
 if(held)_bossHold=Math.min(1,(_bossHold||0)+dt*1.6);else _bossHold=Math.max(0,(_bossHold||0)-dt*1.6);
 const before=mapScroll;mapScroll=Math.min(a.nativeRange,mapScroll+dt*40*(1-_bossHold));_lastScrollDy=mapScroll-_prevMapScroll;_prevMapScroll=mapScroll;
 const chase=!!(boss&&((bossActive&&!boss.dead)||(boss._cinDeath&&boss.dying<9.8))),height=viewH(),top=viewTopY();
 if(chase){const mode=boss?._s4war?.mode,spd=boss?._p4Final?.roadSpeed||(mode==='flyaway'?620:mode==='swerve'?560:480);LS112.chaseTravel+=dt*spd;_stage4BossRoadScroll=LS112.chaseTravel;}
 else _stage4BossRoadScroll=0;
 const source=Math.max(0,a.h-height)*(1-clamp(mapScroll/a.nativeRange,0,1))-LS112.chaseTravel;
 ctx.save();ctx.imageSmoothingEnabled=false;
 if(source<0){const road=LS112_ART.highway;ls112Window(road,road.h+source,top,Math.min(height,-source),true);}
 ls112Window(a,source,top,height,false);ls112Power(source,top);ctx.restore();
 _masterSrcY=source-top;_groundPublish(source);LS112.roadTravel=a.h-height-source;LA1007.scroll=LS112.roadTravel;LA1007.mapPrev=mapScroll;
 for(const e of enemies)if(e._hm17?.phase==='loaded'&&!e.dead){e.x=hm17Shoulder(e._hm17.side);e.y=e._hm17.anchor+LA1007.scroll-46;}
 for(const p of HM17.empty)hm17Blit('pad',p.x,p.anchor+LA1007.scroll);
 LS112.clock.terrain={stage:4,source,travel:LS112.roadTravel,chase};ls112Count('stage-4');return true;
}
drawLevelMaster=function(dt){
 if(!ls112Live())return LS112.base.master.apply(this,arguments);
 if(run.stage===4)return ls112Road(dt);
 const result=LS112.base.master.apply(this,arguments);if(!result)return result;
 const n=run.stage,a=LS112_ART.levels[String(n)];
 if([5,8,9].includes(n)){
  const t=Number.isFinite(dt)?Math.max(0,Math.min(dt,.1)):0;let travel;
  if(n===5)travel=_stage5SpaceScroll*.34;else if(n===9)travel=_stage9SpaceScroll*.32;
  else travel=(LS112.clock.realmTravel||0)+t*85;
  if(n===8)LS112.clock.realmTravel=travel;
  ls112Bed(a.material);const source=a.h-viewH()-travel;ls112Window(a,source,viewTopY(),viewH(),true);
  _masterSrcY=((source%a.h)+a.h)%a.h-viewTopY();_groundPublish(-travel);LS112.clock.terrain={stage:n,source,travel};
 }else if(n!==4)LS112.clock.terrain={stage:n,source:_masterSrcY+viewTopY(),mapScroll};
 ls112Count('stage-'+n);return result;
};
bg6LoopDraw=function(img,key,scroll,width,height,top){if(!ls112Live(6)||key!==LS112_ART.levels['6'].key)return LS112.base.loop6.apply(this,arguments);
 const a=LS112_ART.levels['6'],source=a.h-height-scroll;ls112Window(a,source,top,height,true);_masterSrcY=((source%a.h)+a.h)%a.h-top;_groundPublish(-scroll);LS112.clock.terrain={stage:6,source,travel:scroll};ls112Count('city');};
stage6TransitionBackgroundDraw=function(scroll){if(!ls112Live(6)||stageXArenaActive())return LS112.base.transition6.apply(this,arguments);
 const a=LS112_ART.levels['6'];ls112Warm(6);if(!XART.rdy(a.key)||!XART.rdy(LS112_ART.materials[a.material].key))return true;
 ctx.save();ctx.translate(-camLeftX(),0);ls112Bed(a.material,680,0,VH);ls112Window(a,a.h-VH-(scroll||0),0,VH,true);ctx.restore();
 bg6WeatherGrade(0,0,VW,VH);ls112Count('city-transition');return true;};
fr27LoopTerrain=function(key,scroll){if(ls112Live(8)&&run.stage===8&&key==='fr27_realm_terrain'){
 const a=LS112_ART.levels['8'],source=a.h-viewH()-scroll;ls112Bed(a.material);if(!ls112Window(a,source,viewTopY(),viewH(),true))return false;
 _masterSrcY=((source%a.h)+a.h)%a.h-viewTopY();_groundPublish(-scroll);LS112.clock.terrain={stage:8,source,travel:scroll};ls112Count('stage-8');return true;
 }return LS112.base.realmLoop.apply(this,arguments);};
// Placement follows visual travel, but the director still uses its original
// logical distance/gaps. New scenery must not silently add missile waves.
hm17Director=function(){if(!ls112Live(4)||run.stage!==4)return LS112.base.highwayDirector.apply(this,arguments);
 const visual=LA1007.scroll,logical=mapScroll,serial=HM17.serial;LA1007.scroll=logical;
 try{return LS112.base.highwayDirector.apply(this,arguments);}finally{
  for(const e of enemies)if(e._hm17&&e._hm17.id>serial)e._hm17.anchor+=logical-visual;
  LA1007.scroll=visual;
 }};
hm17Shoulder=function(side){return ls112Live(4)&&run.stage===4?(side<0?248:432):LS112.base.shoulder.apply(this,arguments);};
// Retired scenery overlays cannot re-cover approved transparent terrain.
drawLiquidFalls=function(){if(ls112Live())return;return LS112.base.falls.apply(this,arguments);};
drawRoadSigns=function(){if(ls112Live())return;return LS112.base.signs.apply(this,arguments);};
l6ObjsDraw=function(){if(ls112Live(6)&&run.stage===6)return;return LS112.base.objects6.apply(this,arguments);};
l8ObjsDraw=function(){if(ls112Live(8)&&run.stage===8)return;return LS112.base.objects8.apply(this,arguments);};
stage7CleanTerrain=function(img,key){if(ls112Live(7)&&key===LS112_ART.levels['7'].key)return img;return LS112.base.clean.apply(this,arguments);};
fr28SewerMaster=function(){if(ls112Live(7)&&run.stage===7){const exit=boss?._s7mod?.frExit;if(!exit)return null;const a=exit.sc86?.sr93?LS112_ART.sewerExit:LS112_ART.levels['7'];if(XART.rdy(a.key))return XART.get(a.key);}return LS112.base.sewer.apply(this,arguments);};
_buildTankMask=function(){const n=String(run.stage),a=LS112_ART.masks[n];if(!ls112Live()||!a)return LS112.base.mask.apply(this,arguments);
 if(!LS112.masks.has(n)){const bytes=atob(a.bits),bits=new Uint8Array(a.gw*a.gh);for(let i=0;i<bits.length;i++)bits[i]=(bytes.charCodeAt(i>>3)>>(7-(i&7)))&1;LS112.masks.set(n,{cell:a.cell,gw:a.gw,gh:a.gh,bits});}
 _tankMask=LS112.masks.get(n);_tankMaskKey=LS112_ART.levels[n].key;return _tankMask;};
tankDrivable=function(x,y,failOpen){if(ls112Live()&&LS112_ART.masks[String(run.stage)]){if(run.stage===4&&y<0)return x>=285&&x<=395;const m=_buildTankMask(),gx=Math.floor(x/m.cell),gy=Math.floor(y/m.cell);return gx>=0&&gy>=0&&gx<m.gw&&gy<m.gh&&!!m.bits[gy*m.gw+gx];}return LS112.base.drive.apply(this,arguments);};
levelSrcY=function(){if(ls112Live()&&Number.isFinite(_masterSrcY))return _masterSrcY;return LS112.base.src.apply(this,arguments);};
stageXArenaReady=function(){if(!globalThis.LS112_OFF){ls112Warm('X');return ls112Keys('X').every(k=>XART.rdy(k));}return LS112.base.xready.apply(this,arguments);};
stageXArenaDraw=function(dt){if(globalThis.LS112_OFF||!stageXArenaReady())return LS112.base.xdraw.apply(this,arguments);
 const a=LS112_ART.levels.X;LS112.xTravel+=Math.max(0,Number.isFinite(dt)?dt:0)*36;const source=a.h-viewH()-LS112.xTravel;
 ls112Bed(a.material);ls112Window(a,source,viewTopY(),viewH(),true);_masterSrcY=((source%a.h)+a.h)%a.h-viewTopY();_groundPublish(-LS112.xTravel);LS112.clock.terrain={stage:'X',source,travel:LS112.xTravel};ls112Count('stage-X');return true;};
globalThis.BOF_LAYERED_STAGES={state:LS112,art:LS112_ART,live:ls112Live,warm:ls112Warm,bed:ls112Bed,road:ls112Road,
 info(){return{stage:run.stage,clock:LS112.clock,draws:LS112.draws,source:_masterSrcY,groundDelta:_groundDy,worldWidth:worldWidth(),mapScroll,nativeRange:levelScrollRange()};}};
