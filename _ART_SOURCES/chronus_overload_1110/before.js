"use strict";
/* One defeated pose, a committed core shot, then chromium ignition and breakup.
   Authored armor is fixed until rupture; PixelLab supplies the energy acting. */
const HF17={base:{start:h3EndingStart,tick:h3EndingTick,draw:h3EndingDraw,
 load:stageLoadBegin,begin:beginStage},events:[],draws:{},last:null,earth:null};
for(const bank of Object.values(HF17_ART))for(const a of bank)XART._src[a.key]=a.path;

// CE110: actual core-pixel 1015 steps, preserved PixelLab discharge and source-piece breakup.
const CE110={keys:["body-0-0", "body-0-1", "body-1-0", "body-1-1", "body-2-0", "body-2-1", "body-3-0", "body-3-1", "body-4-0", "body-4-1", "body-5-0", "body-5-1", "aura", "boss-heavy", "boss-heavy-large", "dracodia-surge", "dracodia-surge-large", "stage5-core", "stage5-core-large", "piece-00", "piece-01", "piece-02", "piece-03", "piece-04", "piece-05", "piece-06", "piece-07", "piece-08", "piece-09", "piece-10", "piece-11", "piece-12", "piece-13", "piece-14", "piece-15", "piece-16", "piece-17"],stats:{white:0,normal:0,aura:{},fx:[0,0,0],pieces:0,maxFx:0},families:['boss-heavy','dracodia-surge','stage5-core']};
for(const key of CE110.keys)XART._src['ce110_'+key]='assets/game/levels/stage_05/boss/'+(key==='aura'||key.startsWith('body-')?'chronus_core_loop_1110/':'chronus_electric_1110/')+key+'.png';
function ce110Warm(){let ready=true;for(const k of CE110.keys)if(!XART.rdy('ce110_'+k))ready=false;return ready;}
function ce110Blit(key,frame,size,x,y){const k='ce110_'+key;if(!XART.rdy(k))return;const im=XART.get(k);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,frame*size,0,size,size,Math.round(x-size/2),Math.round(y-size/2),size,size);ctx.restore();}
function ce110Offset(F){const a=[[2,0],[-2,1],[1,-2],[-1,2],[3,-1],[-3,0],[1,2],[-2,-1]];return a[Math.floor(F.age*24)%a.length];}
// Integrated frame clock: 8fps rising continuously to40fps, without phase resets.
function ce110Loop(age){const t=Math.min(10,age);return 8*t+1.6*t*t+Math.max(0,age-10)*40;}
function ce110Body(e){const F=e.hf17,q=ce110Offset(F),clock=ce110Loop(F.age),frame=Math.floor(clock)%32;
 const floor=Math.min(3,Math.floor(F.age/2)),level=Math.min(5,floor+Math.floor((Math.sin(clock/32*Math.PI*2)*.5+.5)*(5-floor)+.001)),white=e.boss.flash>0||Math.floor(F.age*16)%3===0?1:0;
 const im=XART.get('ce110_body-'+level+'-'+white);if(im)ctx.drawImage(im,Math.round(F.anchor.x+q[0]-148),Math.round(F.anchor.y+q[1]-148));
 CE110.stats[white?'white':'normal']++;ce110Blit('aura',frame,320,F.anchor.x+q[0],F.anchor.y+q[1]);
 CE110.stats.aura[frame]=(CE110.stats.aura[frame]||0)+1;CE110.stats.coreLevels||={};CE110.stats.coreLevels[level]=(CE110.stats.coreLevels[level]||0)+1;CE110.stats.loopFps=8+3.2*Math.min(10,F.age);
}
function ce110Emit(F,x,y,large=false){if(F.blasts.length>=20)return;const family=F.blastSerial++%3;F.blasts.push({x,y,t:0,life:.78,family,large});CE110.stats.fx[family]++;CE110.stats.maxFx=Math.max(CE110.stats.maxFx,F.blasts.length);}

function hf17Warm(){return ce110Warm();}
stageLoadBegin=function(n,keys){return HF17.base.load.call(this,n,[...(keys||[]),...(n===5?Object.values(HF17_ART).flat().map(a=>a.key):[])]);};
beginStage=function(n){const r=HF17.base.begin.apply(this,arguments);HF17.events=[];HF17.last=HF17.earth=null;if(n===5)hf17Warm();return r;};
function hf17Log(event,data={}){HF17.events.push({event,...data});if(HF17.events.length>160)HF17.events.shift();}
function hf17Core(F){const a=HF17_ART.stunned[0],k=240/208;return{x:F.anchor.x+(127-a.pivot[0])*k,y:F.anchor.y+(145-a.pivot[1])*k};}
function hf17Phase(e,name){const F=e.hf17;F.phase=name;F.t=0;e.sm10.phase=name;hf17Log(name,{age:F.age});
 if(name==='pulse')Audio.SFX.bossWeaponCharge?.();
 if(name==='lock'){F.beep=-1;Audio.SFX.retinaCharge?.();}
 if(name==='missile'){
  F.from=spaceShipHardpoints(F.ship.x,F.ship.y,SPACE_SHIP_SIZE*1.5).nose;
  F.flight=clamp(Math.hypot(F.core.x-F.from.x,F.core.y-F.from.y)/620,.45,.85);
  Audio.SFX.missile?.();hf17Log('shot-fired',{from:F.from,to:F.core});
 }
 if(name==='engulf'){
  F.impacts++;e.boss.dying=0;markHit(e.boss);Audio.SFX.impactMetal?.();Audio.SFX.expBig?.();
  sm10Log('hammer-core-impact',F.core);hf17Log('core-impact',{count:F.impacts,...F.core});
 }
 if(name==='burst'){F.blasts=[];F.blastCd=0;F.blastSerial=0;F.blastSound=0;F.centerCd=0;Audio.SFX.expBig?.();Audio.SFX.hammerImpact?.();}
}
h3EndingStart=function(b){
 HF17.base.start.apply(this,arguments);const e=H3.ending;
 if(!e||!fb1002NormalHammer(b))return;
 const F=e.hf17={phase:'drain',t:0,age:0,line:0,shown:0,impacts:0,crackle:0,camX,
  anchor:{x:b.x,y:b.y},ship:{x:player.x,y:Math.min(player.y,VH*.78)}};
 F.core=hf17Core(F);e.phase='hammerFinale';e.sm10.phase='drain';
 HF17.events=[];HF17.earth=null;hf17Log('stunned',{...F.anchor,core:F.core});
 hf17Warm();XART.rdy('nbret_'+_pilotKey());XART.rdy(pilotMissileKey(true));
};
h3EndingTick=function(dt){const e=H3.ending,F=e?.hf17;if(!F)return HF17.base.tick.apply(this,arguments);
 if(F.phase==='after')return HF17.base.tick.apply(this,arguments);
 if(!hf17Warm()||!furyShipReady()||!XART.rdy('fb1002_hammer_portrait')){stageEnding=0;return;}
 F.t+=dt;F.age+=dt;stageEnding=0;whiteBlast=0;shake=0;camX=F.camX;
 e.boss.x=F.anchor.x;e.boss.y=F.anchor.y;e.boss.flash=Math.max(0,(e.boss.flash||0)-dt);
 _stage5SpaceScroll+=dt*10;efxTick(dt);
 if(F.phase==='drain'){
  const crackle=Math.floor(F.age/1.1);if(crackle>F.crackle){F.crackle=crackle;Audio.SFX.bossShieldStatic?.();}
  const line=SM10_LAST_WORDS[F.line],n=Math.min(line.length,Math.floor(F.t*32));
  dialogueLetterTicks(line,F.shown,n);F.shown=n;
  if(F.t>=line.length/32+2){if(F.line===0){F.line=1;F.t=0;F.shown=0;}else hf17Phase(e,'pulse');}
 }else if(F.phase==='pulse'&&F.t>=2.1)hf17Phase(e,'lock');
 else if(F.phase==='lock'){
  const beat=Math.min(5,Math.floor(F.t/.19));if(beat>F.beep){F.beep=beat;Audio.SFX.retinaLockBeep?.();}
  if(F.t>=1.15)hf17Phase(e,'missile');
 }else if(F.phase==='missile'&&F.t>=F.flight)hf17Phase(e,'engulf');
 else if(F.phase==='engulf'){
  e.boss.dying=F.t;shake=2+F.t*2;
  if(F.t>=2)hf17Phase(e,'burst');
 }else if(F.phase==='burst'){
  e.boss.dying=2+F.t;shake=F.t<.55?14*(1-F.t/.55):0;
  if(F.t>=.28&&!F.released){F.released=true;hf17Log('armor-release');}
  for(const f of F.blasts)f.t+=dt;F.blasts=F.blasts.filter(f=>f.t<f.life);F.blastCd-=dt;F.centerCd-=dt;F.blastSound-=dt;
  if(F.t<4.1&&F.blastCd<=0){F.blastCd=.11;
   for(let j=0;j<2;j++){const i=F.blastSerial%HF17_ART.fragments.length,p=hf17Fragment(F,i,Math.max(.28,F.t));
    if(p.x>=F.camX-40&&p.x<=F.camX+VW+40&&p.y>=-40&&p.y<=VH+40)ce110Emit(F,p.x,p.y,false);else F.blastSerial++;}
   if(F.blastSound<=0){F.blastSound=.20;Audio.SFX.expSmall?.();}}
  if(F.t<4.1&&F.centerCd<=0){F.centerCd=.20;const n=F.blastSerial,angle=n*2.39996;
   ce110Emit(F,F.core.x+Math.cos(angle)*58,F.core.y+Math.sin(angle)*66,n%3===0);}
  if(F.t>=5.1){F.phase='after';e.sm10.phase='death';delete e.engineDeath;e.t=0;e.phase='overhead';whiteBlast=shake=0;hf17Log('cutaway');}
 }
};
function hf17Cell(name,index,x,y,k=240/208,alpha=1,flash=0,rot=0){
 const a=HF17_ART[name]?.[Math.max(0,Math.min(HF17_ART[name].length-1,index|0))];if(!a||!XART.rdy(a.key)||alpha<=0)return false;
 const im=flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);
 ctx.save();ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 HF17.draws[name]=(HF17.draws[name]||0)+1;return true;
}
function hf17Fragment(F,i,age=F.t){const a=HF17_ART.fragments[i],k=240/208,t=Math.max(0,age-.28),dx=a.origin[0]-127,dy=a.origin[1]-145,
 angle=Math.atan2(dy,dx)+(i%2?-.17:.17),v=150+(i%5)*24;
 return{x:F.anchor.x+(a.origin[0]-128)*k+Math.cos(angle)*v*t,
  y:F.anchor.y+(a.origin[1]-128)*k+Math.sin(angle)*v*t,k,rot:(i%2?1:-1)*t*(1.5+i%4)};
}
function hf17Actor(e){const F=e.hf17,p=F.phase;
 if(p!=='burst')ce110Body(e);
 else{
  if(F.t<.28)ce110Body(e);
  if(F.t>=.28)for(let i=0;i<HF17_ART.fragments.length;i++){
   const q=hf17Fragment(F,i),size=160;if(q.x+80<F.camX||q.x-80>F.camX+VW||q.y+80<0||q.y-80>VH)continue;
   const frame=((Math.round(q.rot/(Math.PI*2)*16)%16)+16)%16;ce110Blit('piece-'+String(i).padStart(2,'0'),frame,size,q.x,q.y);CE110.stats.pieces++;}
  for(const f of F.blasts){const size=f.large?320:176,name=CE110.families[f.family]+(f.large?'-large':'');ce110Blit(name,Math.min(13,Math.floor(f.t/.055)),size,f.x,f.y);}
 }
 HF17.last={phase:p,age:F.age,t:F.t,anchor:{...F.anchor},core:{...F.core},impacts:F.impacts};
}
function hf17Missile(F){
 const u=clamp(F.t/F.flight,0,1),x=lerp(F.from.x,F.core.x,u),y=lerp(F.from.y,F.core.y,u),angle=Math.atan2(F.core.y-F.from.y,F.core.x-F.from.x),
  key=pilotMissileKey(true),size=manualMissileSpec(run.missileTier).size;
 if(drawMfx(key,x,y,angle,14*size,null,1,'#ffb04a'))return;
 ctx.save();ctx.translate(x,y);ctx.rotate(angle+Math.PI/2);
 spaceAtlasDraw(ctx,'volley_3_trail_'+(Math.floor(F.t*16)%4),0,18,20,36,true,null);
 spaceAtlasDraw(ctx,'volley_3_missile_0',0,0,22,36,true,null);ctx.restore();
}
function hf17EarthDraw(e){
 ctx.save();worldXformEscape();ctx.fillStyle='#040713';ctx.fillRect(0,0,VW,VH);
 // The existing star plate moves behind a separate destination. No scenery
 // actor, stage camera, mapScroll or sky-scroll value can translate Earth.
 if(XART.rdy('bg_stage05_loop_0923')){
  const im=XART.get('bg_stage05_loop_0923'),sw=im.width,sh=sw*VH/VW,travel=(e.homeAge||0)*21,
   sy=(im.height-sh-travel%Math.max(1,im.height-sh));
  ctx.imageSmoothingEnabled=false;ctx.drawImage(im,0,sy,sw,sh,0,0,VW,VH);
 }
 const u=clamp(e.descent/8,0,1),s=u*u*(3-2*u),center={x:VW*.5,y:VH*.35},size=VW*lerp(.30,.82,s),
  ship={x:center.x,y:lerp(VH*.78,center.y,s),size:lerp(SPACE_SHIP_SIZE*1.5,3,s)};
 if(XART.rdy('h3_earth')){const im=XART.get('h3_earth'),height=size*im.height/im.width;ctx.drawImage(im,center.x-size/2,center.y-height/2,size,height);}
 furyShipDrawFlight(ship.x,ship.y,ship.size,_pilotKey(),{key:'base'},e.t);
 if(e.phase==='welcome'&&e.cheer<H3_CHEERS.length){const [who,line]=h3Cheer(e);h3Radio(who,line,e.shown,VH*.75);}
 const fade=Math.max(1-clamp((e.homeAge||0)/1.2,0,1),clamp((e.descent-8)/1.6,0,1));
 if(fade>0){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,VW,VH);}
 HF17.earth={phase:e.phase,center,size,ship,u,fade};ctx.restore();
}
h3EndingDraw=function(){const e=H3.ending,F=e?.hf17;if(!F)return HF17.base.draw.apply(this,arguments);
 if(F.phase==='after'){
  if(['welcome','descent'].includes(e.phase))return hf17EarthDraw(e);
  return HF17.base.draw.apply(this,arguments);
 }
 ctx.save();worldXformEscape();ctx.save();ctx.translate(-F.camX,0);drawBG(0);
 hf17Actor(e);furyShipDrawFlight(F.ship.x,F.ship.y,SPACE_SHIP_SIZE*1.5,_pilotKey(),{key:'base'},F.age);
 if(['lock','missile'].includes(F.phase))drawBossRetina(e.boss,F.core.x,F.core.y,F.phase==='lock'?(1-clamp(F.t/1.15,0,1))*TAU:0,1);
 if(F.phase==='missile')hf17Missile(F);ctx.restore();
 if(F.phase==='drain'){
  const line=SM10_LAST_WORDS[F.line];dlgBox({who:'CHRONOS',portrait:false,portraitKey:'fb1002_hammer_portrait',
   full:line,shown:line.slice(0,F.shown),forceShown:true,screenSpace:false,fade:1,tint:'#96c8ff',pw:VW*.94,ph:VH*.26,x:VW*.03,y:VH*.67});
 }
 ctx.restore();
};
window.BOF_HAMMER_FINALE={state:HF17,warm:hf17Warm,core:hf17Core,earth:hf17EarthDraw};
