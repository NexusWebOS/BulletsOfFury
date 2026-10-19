"use strict";
/* One defeated pose, a committed core shot, then chromium ignition and breakup.
   Authored armor is fixed until rupture; PixelLab supplies the energy acting. */
const HF17={base:{start:h3EndingStart,tick:h3EndingTick,draw:h3EndingDraw,
 load:stageLoadBegin,begin:beginStage},events:[],draws:{},last:null,earth:null};
for(const bank of Object.values(HF17_ART))for(const a of bank)XART._src[a.key]=a.path;
function hf17Warm(){let ready=true;for(const bank of Object.values(HF17_ART))for(const a of bank)if(!XART.rdy(a.key))ready=false;
 for(const bank of ['nxp_barrage','nxp_dense'])for(let f=0;f<8;f++)if(!XART.rdy(bank+'_'+f))ready=false;return ready;}
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
 if(name==='burst'){F.blasts=[];F.blastCd=0;F.blastSerial=0;F.blastSound=0;Audio.SFX.expBig?.();Audio.SFX.hammerImpact?.();}
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
  for(const f of F.blasts)f.t+=dt;F.blasts=F.blasts.filter(f=>f.t<f.life);F.blastCd-=dt;F.blastSound-=dt;
  if(F.t<4.1&&F.blastCd<=0){F.blastCd=F.t<1.2?.075:.11;
   for(let j=0;j<(F.t<1.2?3:2);j++){
    const i=F.blastSerial++%HF17_ART.fragments.length,p=hf17Fragment(F,i,Math.max(.28,F.t));
    if(p.x<F.camX-50||p.x>F.camX+VW+50||p.y<-50||p.y>VH+50)continue;
    F.blasts.push({x:p.x,y:p.y,t:0,life:.48+(i%3)*.08,size:48+(i%4)*16,bank:i%3?'nxp_barrage':'nxp_dense'});
    HF17.explosions=(HF17.explosions||0)+1;
   }
   if(F.blastSound<=0){F.blastSound=.20;Audio.SFX.expSmall?.();}
  }
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
function hf17Actor(e){const F=e.hf17,p=F.phase,k=240/208;
 if(p==='burst'){
  const age=F.t;
  if(age<.28){hf17Cell('unlit',0,F.anchor.x,F.anchor.y,k,1,e.boss.flash);hf17Cell('engulf',31,F.anchor.x,F.anchor.y,k,1-age/.28);}
  // PixelLab's first seven burst poses are the pre-ignition hold. Ignition
  // has already acted in the preceding clip; join at its first hot core.
  hf17Cell('rupture',7+Math.floor(age*16),F.anchor.x,F.anchor.y,k,age<1.6?1:0);
  if(age>=.28)for(let i=0;i<HF17_ART.fragments.length;i++){
   const q=hf17Fragment(F,i),pad=82*q.k;
   if(q.x+pad<F.camX||q.x-pad>F.camX+VW||q.y+pad<0||q.y-pad>VH)continue;
   hf17Cell('fragments',i,q.x,q.y,q.k,1,0,q.rot);
  }
  for(const f of F.blasts||[]){const key=f.bank+'_'+Math.min(7,Math.floor(f.t/f.life*8));if(!XART.rdy(key))continue;
   const im=XART.get(key);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,f.x-f.size/2,f.y-f.size/2,f.size,f.size);ctx.restore();
   HF17.draws.breakupExplosion=(HF17.draws.breakupExplosion||0)+1;}
 }else{
  hf17Cell('stunned',0,F.anchor.x,F.anchor.y,k,1,e.boss.flash);
  if(p==='drain'){
   const dim=clamp(F.age/5.6,0,1),flicker=.5+.5*Math.sin(F.age*23)**2;
   hf17Cell('unlit',0,F.anchor.x,F.anchor.y,k,dim*(.75+.25*flicker),e.boss.flash);
   hf17Cell('drain',Math.floor(F.age*16)%HF17_ART.drain.length,F.anchor.x,F.anchor.y,k);
  }else{
   hf17Cell('unlit',0,F.anchor.x,F.anchor.y,k,1,e.boss.flash);
   const pulse=p==='pulse'?F.t:p==='lock'?2.1+F.t:3.25+F.t;
   hf17Cell('pulse',Math.min(31,Math.floor(pulse*14)),F.anchor.x,F.anchor.y,k);
   const step=PXG_STEPS[Math.min(5,Math.floor((.55+.45*Math.sin(pulse*11)**2)*5))];
   hf17Cell('coreGlow',0,F.anchor.x,F.anchor.y,k,step);
   if(p==='engulf')hf17Cell('engulf',Math.floor(F.t*16),F.anchor.x,F.anchor.y,k);
  }
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
  const line=SM10_LAST_WORDS[F.line];dlgBox({who:'CHROME HAMMER',portrait:false,portraitKey:'fb1002_hammer_portrait',
   full:line,shown:line.slice(0,F.shown),forceShown:true,screenSpace:false,fade:1,tint:'#96c8ff',pw:VW*.94,ph:VH*.26,x:VW*.03,y:VH*.67});
 }
 ctx.restore();
};
window.BOF_HAMMER_FINALE={state:HF17,warm:hf17Warm,core:hf17Core,earth:hf17EarthDraw};
