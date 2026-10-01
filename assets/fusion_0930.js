"use strict";
/* Fusion replaces the SPACE slot only. Shadow Orbs remain available to Dark Matter.
   100%=1.55 seconds; 150%=1.5x; 190..199%=2x; 200%=ordinary ship death,
   even through shields, invulnerability, or an active pilot ability (Mike). */
const FUSION30_BASE={tick:spaceBulletTick,bg:drawBG};
const FUSION30_FULL=1.55,FUSION30_LIMIT=3.10;
for(const a of Object.values(FUSION30_ART))XART._src[a.key]=a.path;
function fusion30Warm(){for(const a of Object.values(FUSION30_ART))XART.rdy(a.key);}
function fusion30Cell(name,frame,x,y,w,h,g){
 const a=FUSION30_ART[name];if(!a||!XART.rdy(a.key))return false;
 const r=a.frames[((frame|0)%a.frames.length+a.frames.length)%a.frames.length];g=g||ctx;
 g.save();g.imageSmoothingEnabled=false;const q=a.ink||[0,0,r[2],r[3]];g.drawImage(XART.get(a.key),r[0]+q[0],r[1]+q[1],q[2],q[3],x-w/2,y-h/2,w,h);g.restore();return true;
}
function fusion30Scale(charge){const p=charge/FUSION30_FULL;return p>=1.9?2:p>=1.5?1.5:1;}
function fusion30Overload(){
 if(player.dead)return false;
 spaceShadowCancel();playerHit('fusionOvercharge');return player.dead;
}
spaceShadowRelease=function(charge){
 if(player.dead||(typeof ht27Locked==='function'&&ht27Locked()))return false;
 const held=Math.max(0,charge||0);
 if(held>=FUSION30_LIMIT-1e-8){fusion30Overload();return false;}
 if(held<SPACE_SHADOW_MIN_CHARGE){spaceShadowCancel();return false;}
 const lv=Math.max(1,spaceWeaponLevel()),p=held/FUSION30_FULL,scale=fusion30Scale(held);
 const hp=spaceShipHardpoints(player.x,player.y,SPACE_SHIP_SIZE).nose;
 for(const off of(spaceAkimboActive()?[-19,19]:[0])){
  const w=(30+lv*3)*scale,h=(122+lv*10)*scale;
  pBullets.push({kind:'spaceFusion',x:hp.x+off,y:hp.y-h*.46,w,h,
   vx:0,vy:-(760+lv*30),dmg:(70+lv*25)*(.4+Math.min(p,1.99)*.6),lv,
   charge:p,scale,t:0,life:1.7,_hit:[],seat:typeof _coopSeat==='number'?_coopSeat:1});
 }
 shake=Math.max(shake,Math.min(8,3+p*2));player.fireCd=.38;
 spaceShadowCancel();spaceWeaponCue('spaceShadowRelease','shadowRelease');return true;
};
spaceShadowTick=function(dt,firing){
 if(!spaceWeaponsActive()||run.spaceWeapon!==1||player.dead||
 (specialActive('maverick')||specialActive('yuri')||specialActive('falva')||(run.sonicT||0)>0||(run.dkT||0)>0||
 (typeof lzMountActive==='function'&&lzMountActive()))||(typeof chargePilotActive==='function'&&chargePilotActive())){
  if(run._spaceShadowHeld||(run._spaceShadowCharge||0)>0)spaceShadowCancel();return false;
 }
 if(firing){
  if(!run._spaceShadowHeld){run._spaceShadowHeld=true;run._spaceShadowCharge=0;run._spaceShadowAudio=false;run._fusionWarn=0;fusion30Warm();}
  run._spaceShadowCharge=Math.min(FUSION30_LIMIT,(run._spaceShadowCharge||0)+Math.max(0,dt));
  if(run._spaceShadowCharge>=FUSION30_LIMIT-1e-8){fusion30Overload();return true;}
  if(!run._spaceShadowAudio){try{Snd.loopOn('spaceShadowCharge',.72);}catch(_){spaceWeaponCue('spaceShadowCharge','shadowCharge');}run._spaceShadowAudio=true;}
  if(run._spaceShadowCharge>=FUSION30_FULL*1.5){
   run._fusionWarn=(run._fusionWarn||0)-dt;
   if(run._fusionWarn<=0){run._fusionWarn=run._spaceShadowCharge>FUSION30_FULL*1.85?.10:.25;if(Audio.SFX.retinaCharge)Audio.SFX.retinaCharge();}
  }
  return true;
 }
 if(run._spaceShadowHeld){spaceShadowRelease(run._spaceShadowCharge||0);return true;}return false;
};
spaceShadowIndicatorDraw=function(x,y,size){
 const p=clamp((run._spaceShadowCharge||0)/FUSION30_FULL,0,2),w=112,h=7,left=x-w/2,top=Math.max(PLAY.y+22,y-size*1.45);
 ctx.save();ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#090616';ctx.fillRect(left-2,top-2,w+4,h+4);
 ctx.fillStyle=p>=1.9?'#fff1fe':'#ed55d9';ctx.fillRect(left,top,w*p/2,h);
 ctx.fillStyle='#fff';for(const mark of[.5,.75,.95])ctx.fillRect(left+w*mark,top,1,h);
 const pct=Math.min(199,Math.floor(p*100+1e-6));
 campText('FUSION '+pct+'%',x,top-7,8,'#fff1fe');
 campText(p>=1.9?'RELEASE! 200% = DEATH':p>=1.5?'1.5X POWER - RELEASE':p>=1?'CHARGED - RELEASE':'HOLD TO CHARGE',x,top+18,7,p>=1.5?'#ff98eb':'#e6c6ff');ctx.restore();
};
function fusion30ChargeDraw(x,y,size){
 const p=clamp((run._spaceShadowCharge||0)/FUSION30_FULL,0,2),hp=spaceShipHardpoints(x,y,size).nose,s=size*(.55+p*.4);
 fusion30Cell('charge',efxClock*16,hp.x,hp.y,s,s);spaceShadowIndicatorDraw(x,y,size);
}
drawBG=function(dt){
 const r=FUSION30_BASE.bg(dt);if(spaceWeaponsActive()&&!player.dead&&(run._spaceShadowCharge||0)>0){
  const p=clamp(run._spaceShadowCharge/FUSION30_LIMIT,0,1);
  ctx.save();ctx.globalCompositeOperation='source-over';ctx.fillStyle='rgba(7,0,16,'+(.35*p)+')';ctx.fillRect(camLeftX(),viewTopY(),camRightX()-camLeftX(),VH);
  ctx.fillStyle='rgba(255,30,170,'+(.34*p*p)+')';ctx.fillRect(camLeftX(),viewTopY(),camRightX()-camLeftX(),VH);ctx.restore();
 }return r;
};
function fusion30Impact(b,t){
 const y=spaceTargetY(t),s=Math.min(164,56+b.w*1.2);
 pBullets.push({kind:'spaceFusionFx',x:b.x,y:y,w:s,h:s,t:0,life:.38,_scar:false});
 pBullets.push({kind:'spaceFusionFx',x:b.x,y:y,w:s*.7,h:s*.7,t:0,life:.7,_scar:true});
 if(Audio.SFX.expSmall)Audio.SFX.expSmall();
}
spaceBulletTick=function(b,dt){
 if(b.kind==='spaceFusionFx'){b.t+=dt;if(b.t>=b.life)b.dead=true;return true;}
 if(b.kind!=='spaceFusion')return FUSION30_BASE.tick(b,dt);
 b.t+=dt;b.life-=dt;
 // Sweep the actual moving beam volume; fast shots cannot skip thin modules.
 const steps=Math.max(1,Math.ceil(Math.abs(b.vy*dt)/16)),dy=b.vy*dt/steps;
 for(let i=0;i<steps;i++){
  b.y+=dy;
  const before=b._hit.length;
  spaceBulletHit(b,true);
  for(let j=before;j<b._hit.length;j++)fusion30Impact(b,b._hit[j]);
 }
 if(b.life<=0||b.y+b.h/2<viewTopY()-24)b.dead=true;return true;
};
function fusion30BulletDraw(b){
 if(b.kind!=='spaceFusion'&&b.kind!=='spaceFusionFx')return false;
 if(b.kind==='spaceFusion')fusion30Cell('beam',b.t*18,b.x,b.y,b.w,b.h);
 else{ctx.save();ctx.globalAlpha=1-b.t/b.life;fusion30Cell(b._scar?'scar':'impact',Math.min(3,Math.floor(b.t/b.life*4)),b.x,b.y,b.w,b.h);ctx.restore();}return true;
}
