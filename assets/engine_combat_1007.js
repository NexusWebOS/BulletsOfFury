"use strict";
/* Shared combat presentation: authored warning plates, seat-local gun clocks,
   and swept point-vs-expanded-box collision for ordinary fast projectiles. */
const EC7={frame:0,alerts:new WeakSet(),mountDraws:0,laneDraws:0};
const EC7_BASE={world:drawWorld,pickup:applyPowerup,heat:chaingunHeatTick,warn:combatWarningDraw};
function ec7SegmentBox(x0,y0,x1,y1,cx,cy,hx,hy){
 if(![x0,y0,x1,y1,cx,cy,hx,hy].every(Number.isFinite))return false;
 let lo=0,hi=1;const dx=x1-x0,dy=y1-y0;
 for(const [p,d,c,h] of [[x0,dx,cx,hx],[y0,dy,cy,hy]]){
  if(Math.abs(d)<1e-9){if(Math.abs(p-c)>h)return false;continue;}
  let a=(c-h-p)/d,z=(c+h-p)/d;if(a>z)[a,z]=[z,a];lo=Math.max(lo,a);hi=Math.min(hi,z);if(lo>hi)return false;
 }return true;
}
function ec7SweepRound(b,x0,y0){
 // Existing collision/damage code owns the hit. Only move a fast ordinary
 // round to its first occupied sample, including the boss's live modules.
 if(!['mg','spread','dkshot','iceLance'].includes(b.kind)||b._enemyReflected||b.dead)return;
 const dx=b.x-x0,dy=b.y-y0,n=Math.ceil(Math.hypot(dx,dy)/4);if(n<2)return;
 for(let i=1;i<n;i++){
  const x=x0+dx*i/n,y=y0+dy*i/n;
  let hit=enemies.some(e=>!e.dead&&Math.abs(x-e.x)<((e.w||0)+(b.w||0))/2&&Math.abs(y-e.y)<((e.h||0)+(b.h||0))/2);
  if(!hit&&subBossActive&&subBoss&&!subBoss.dead&&!subBoss.enter){
   const S=subBoss,sw=S._drawW||S.w,sh=S._drawH||S.h,sy=S._drawY??S.y;
   if(Math.abs(x-S.x)<(sw+(b.w||0))/2&&Math.abs(y-sy)<(sh+(b.h||0))/2){const solid=subBossSolidAt(x,y);hit=solid===null||solid===true;}
   if(!hit&&S._ship==='olivewarden')hit=!!stage4MiniDroneAt(S,x,y,Math.max(b.w||0,b.h||0)*.45);
  }
  if(!hit&&bossActive&&boss&&!boss.dead)hit=!!bossHitTest(x,y);
  if(!hit)hit=powerups.some(p=>!p.dead&&spaceShootableContainer(p)&&Math.abs(x-p.x)<((p.w||0)+(b.w||0))/2&&Math.abs(y-p.y)<((p.h||0)+(b.h||0))/2);
  if(hit){b.x=x;b.y=y;return;}
 }
}
function ec7WarmMounts(){
 if(typeof REPAIR30_ART==='undefined')return;
 const pilot=_pilotKey();
 for(const name of ['chaingun_mount_'+pilot+'_left','chaingun_mount_'+pilot+'_right','chaingun_barrel_top']){
  const a=REPAIR30_ART[name];if(!a)continue;
  // A lazy lookup made before a late art registration may have cached null.
  if(XART.img[a.key]===null&&XART._src[a.key])delete XART.img[a.key];XART.rdy(a.key);
 }
}
applyPowerup=function(p){const r=EC7_BASE.pickup.apply(this,arguments);if(run.weapon===7)ec7WarmMounts();return r;};
chaingunHeatTick=function(dt,firing){
 const r=EC7_BASE.heat.apply(this,arguments),step=Number.isFinite(dt)?Math.max(0,dt):0;
 if(run.weapon===7){ec7WarmMounts();player._chainSpinT=(player._chainSpinT||0)+step*(.15+clamp(run._chainRev||0,0,1));}
 player._chainMuzzle=Math.max(0,(player._chainMuzzle||0)-step);return r;
};
chaingunMountsDraw=function(){
 if(!chaingunMountsVisible())return;ec7WarmMounts();
 const pilot=_pilotKey(),points=chaingunMountPoints(),z=.18,barrel=REPAIR30_ART.chaingun_barrel_top,bz=.16;
 for(let i=0;i<2;i++){
  const name='chaingun_mount_'+pilot+'_'+(i?'right':'left'),a=REPAIR30_ART[name];if(!a)continue;
  const p=points[i],socketY=p.y+(18-a.anchor[1])*z;
  const mounted=repair30Cell(name,0,p.x,p.y-(a.anchor[1]-a.size[1]/2)*z,a.size[0]*z,a.size[1]*z,false);
  const rotating=repair30Cell('chaingun_barrel_top',player._chainSpinT||0,p.x,socketY-(barrel.anchor[1]-barrel.size[1]/2)*bz,barrel.size[0]*bz,barrel.size[1]*bz,false);
  if(mounted&&rotating)EC7.mountDraws++;
  if(player._chainMuzzle>0)wm26Draw(ctx,'chaingun',p.x,socketY-12,-Math.PI/2,1-player._chainMuzzle/.10,18,wlvGlow(clamp(run.wlevel||1,1,5)));
 }
};
// A warning never blanks just as it becomes urgent. Brightness pulses, while
// the original authored green/yellow/red silhouette remains readable.
l23WarnSymbolDraw=function(owner,B){
 if(!owner||!B||owner.dead||B.released||B.t>=B.warm||enemyWarningOwner(owner)||EC7.alerts.has(owner))return false;
 const p=clamp(B.t/Math.max(.001,B.warm),0,1),color=l23FovPhase(p),key='bmfx_alert_'+color+'_danger';if(!XART.rdy(key))return false;
 const im=XART.get(key),h=32,w=h*(im.width/im.height),top=(owner._drawY??owner.y)-(owner._drawH??owner.h??30)*.5;
 const x=clamp(Number.isFinite(B.alertX)?B.alertX:owner.x,camLeftX()+w*.5+4,camRightX()-w*.5-4);
 const y=clamp(Number.isFinite(B.alertY)?B.alertY:top-h-10,Math.max(L23_WARN_MINY,viewTopY()+8),VH-h-8);
 const age=B.blinkT??B.t,pulse=.5+.5*Math.sin(age*(color==='red'?22:color==='yellow'?12:5));
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=(color==='green'?.68:.78+.22*pulse)*(B.alpha??1);
 ctx.drawImage(im,Math.round(x-w/2),Math.round(y),w,h);ctx.restore();EC7.alerts.add(owner);return true;
};
combatWarningDraw=function(owner,q){
 if(!owner||owner.dead||!q||q.progress==null)return;
 const k=clamp(q.progress,0,1),dx=q.ex-q.x,dy=q.ey-q.y,len=Number.isFinite(q.len)?q.len:Math.hypot(dx,dy);
 if(q.laneShape==='line'&&!q.alertOnly&&len>0){
  // Slice the authored cone's far interior into a constant-width corridor;
  // its width is the actual collision width plus a small readability margin.
  const key='bmfx_fov_'+l23FovPhase(k)+'_tall';if(XART.rdy(key)){
   const im=XART.get(key),sw=im.width*.40,sx=(im.width-sw)*.5,sy=im.height*.68,sh=im.height*.16,w=Math.max(8,q.width||20);
   ctx.save();ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(dy,dx)-Math.PI/2);ctx.imageSmoothingEnabled=false;
   ctx.globalAlpha*=(q.alpha??1)*(.34+k*.26);ctx.drawImage(im,sx,sy,sw,sh,-w*.5,0,w,len);ctx.restore();EC7.laneDraws++;
  }
 }else if(!q.alertOnly)EC7_BASE.warn(owner,{...q,fieldOnly:true});
 if(!q.fieldOnly)l23WarnSymbolDraw(owner,{t:k,warm:1,released:false,alertX:q.alertX,alertY:q.alertY,alpha:q.alpha,blinkT:owner.t??stateT});
};
drawWorld=function(){EC7.frame++;EC7.alerts=new WeakSet();return EC7_BASE.world.apply(this,arguments);};
