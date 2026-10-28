"use strict";
// Jace: dodgeable fire orbs, ranged interceptable helix, deliberate repositioning.
const JR36={attack:rg4Attack,tick:rg4AttackTick,kind:ra4AttackKind,ship:fr27RebelDrawShip,ord:rg4OrdnanceDraw,projectile:drawCombatFinalProjectile,impact:pw5Impact,intercept:enemyOrdnanceCanIntercept,update:updatePlay,helix:ra4Helix,events:[]};
XART._src.jr36_spin='assets/game/levels/stage_06/boss/jace_tactical_1028/spin.png';
PXG_SHEETS.jr36_spin={glow:'assets/game/levels/stage_06/boss/jace_tactical_1028/spin_glow.png',size:[256,256],n:1,st:[6,10]};
for(const kind of ['idle','attack']){const B=AF21_ART.models.jace.banks[kind];PXG_SHEETS[B.key]={glow:'assets/game/levels/stage_06/boss/jace_tactical_1028/'+kind+'_glow.png',size:[128*B.frames,128],n:1,st:[6,10]};}
for(const key of ['jr36_spin','af21_jace_idle','af21_jace_attack']){XART._src['pxg_'+key+'_glow']=PXG_SHEETS[key].glow;XART.rdy(key);XART.rdy('pxg_'+key+'_glow');}
function jr36Orb(x,y,d,t,flash=0,power=.75){if(!XART.rdy('jr36_spin'))return;const f=Math.floor(t*24)%16,im=flash>0?xartTint('jr36_spin','#ffffff',1):XART.get('jr36_spin');
 const step=Math.floor(t*24)%10,pulse=PXG_STEPS[step<6?step:10-step];
 pxgWindow({lights:flash>0?0:power*(.45+.55*pulse),core:0,alpha:1},()=>ctx.drawImage(im,f%4*64,Math.floor(f/4)*64,64,64,x-d/2,y-d/2,d,d),null,[]);
}
function jr36Turret(owner,side){
 const p=rr26AnimatedPose(owner)||rr26Pose(owner),bank=p&&JR36_TURRETS[p.key];if(!bank||owner.dead||owner.evadeT>0)return null;
 const modules=fr27RebelModules(owner),alive=s=>!modules.some(m=>m.id===(s<0?'left':'right')&&m.hp<=0);
 side=side<0?-1:1;if(!alive(side)){side=-side;if(!alive(side))return null;}
 const xy=bank.points[p.f%bank.points.length][side<0?0:1],scale=p._af21?SHIP_DRAW_H*1.5*p.M.referenceRatio/p.M.span:SHIP_DRAW_H*1.5*p.d.referenceRatio/p.m.span;
 return{x:owner.x+(xy[0]-bank.pivot[0])*scale,y:owner.y+(xy[1]-bank.pivot[1])*scale,side,key:p.key,frame:p.f};
}
function rr36Bullet(owner,x,y,a,speed){const T=owner.rg4?._rbal19Gun,side=T?.side??(x<owner.x?-1:x>owner.x?1:(owner.rg4?.gunN||0)%2?-1:1),p=jr36Turret(owner,side);
 if(!p)return{dead:true,x:owner.x,y:owner.y};
 if(T&&Number.isFinite(T.tx+T.ty))a=Math.atan2(T.ty-p.y,T.tx-p.x);
 const z=eShootT(p.x,p.y,a,Math.min(3.2,speed||2.6),'s6orb',{w:16,h:16,silent:true,noMuzzle:true});Object.assign(z,{_jr36Bullet:true,_jr36Side:p.side,_jr36Origin:{...p},_boss:true,_rg4:true,owner});return z;}
enemyOrdnanceCanIntercept=function(p){return p?._jr36Bullet?false:JR36.intercept.apply(this,arguments);};
pw5Impact=function(p){if(p?._jr36Bullet||p?.owner?.key==='jace'&&p.kind==='helix')return null;return JR36.impact.apply(this,arguments);};
drawCombatFinalProjectile=function(p){if(p._jr36Bullet){jr36Orb(p.x,p.y,24,p.t||0);return true;}return JR36.projectile.apply(this,arguments);};
updatePlay=function(dt){for(const p of eBullets)if(p._jr36Bullet&&(p.owner?.dead||fr27RebelModules(p.owner).some(m=>m.id===(p._jr36Side<0?'left':'right')&&m.hp<=0)))p.dead=true;return JR36.update.apply(this,arguments);};
ra4AttackKind=function(q,G){if(q.key==='jace'){q.rg4.serial++;return 'helix';}return JR36.kind.apply(this,arguments);};
rg4Attack=function(q,R,G,forced){if(q.key!=='jace')return JR36.attack.apply(this,arguments);
 if(G.rd21?.fleet||R.ships.some(s=>s!==q&&rbal19Heavy(s))){q.rg4.cd=.6;return;}
 const A=rd21Personal(q,R,G,'jr36helix');A.warm=2.2;A.phase='position';A.from={x:q.x,y:q.y};
 A.perch={x:clamp(q.x,camLeftX()+70,camRightX()-70),y:Math.min(q.y,PLAY.y+130)};q.rg4.trace=[];return A;
};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(A?.kind!=='jr36helix')return JR36.tick.apply(this,arguments);
 if(!rd21Live(q)){q.rg4.act=null;return;}A.t+=Math.min(dt,.05);q.evadeT=0;q.rfHeading=Math.PI/2;q._rd21Scale=1;
 if(A.phase==='position'){const u=clamp(A.t/1.1,0,1),v=u*u*(3-2*u);q.x=lerp(A.from.x,A.perch.x,v);q.y=lerp(A.from.y,A.perch.y,v);if(u===1){A.phase='charge';A.t=0;A.ox=q.x;A.oy=q.y;}return;}
 if(A.phase==='charge'){q.x=A.ox;q.y=A.oy;if(A.t<A.warm*.65){const p=A.target.ref;A.a=Math.atan2(p.y-q.y-42,p.x-q.x);}
  combatWarningTick(A,'jace-fire-helix',Math.min(A.t,A.warm),A.warm);
  if(A.t<A.warm)return;ra4Helix(q,G,A);JR36.events.push({event:'ranged-release',x:q.x,y:q.y});A.phase='recover';A.t=0;A.back={x:q.x,y:q.y};
  const side=q.x>camLeftX()+viewW()/2?-1:1;A.next={x:clamp(q.x+side*65,camLeftX()+70,camRightX()-70),y:A.oy};
 }else if(A.phase==='recover'){const u=clamp(A.t/2,0,1),v=u*u*(3-2*u);q.x=lerp(A.back.x,A.next.x,v);q.y=A.back.y;q.rfHeading=Math.PI/2+Math.sin(u*Math.PI)*.18*Math.sign(A.next.x-A.back.x);if(u===1)rd21Finish(q,G,5.5);}
};
ra4Helix=function(q,G,A){const n=G.ord.length,r=JR36.helix.apply(this,arguments);if(q.key==='jace')for(const o of G.ord.slice(n)){o._jr36Helix=true;o.r=28;o.life=5;o.vx=Math.cos(A.a)*110;o.vy=Math.sin(A.a)*110;}return r;};
const jr36Warning=rg4Warning;
rg4Warning=function(q,A){if(A?.kind==='jr36helix'){if(A.phase==='charge')rd21Fov(A,q.x,q.y+42,A.a,72,A.t/A.warm);return;}return jr36Warning.apply(this,arguments);};
rg4OrdnanceDraw=function(o,G){if(o.kind==='helix'&&o.owner?.key==='jace'){jr36Orb(o.x,o.y,72,o.t,o.flash,.95);return;}return JR36.ord.apply(this,arguments);};
// Attach the companion inside the existing module clips, with the exact native pose rectangle.
const jr36HullDraw=af21Draw;
af21Draw=function(p,x,y,span,alpha=1,flash=null,module=null){const r=jr36HullDraw.apply(this,arguments);
 if(p.id!=='jace'||!JR36.chargeLight||flash||p.rotation)return r;
 const key='pxg_'+p.key+'_glow';if(!XART.rdy(key))return r;const size=span*128/p.M.span,c=p.m.cells[p.f];
 ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha*=alpha*pxgStep(JR36.chargeLight);
 if(module==null)ctx.drawImage(XART.get(key),...c,x-size/2,y-size/2,size,size);
 else{const m=p.m.modules[module];ctx.drawImage(XART.get(key),c[0]+m[0],c[1]+m[1],m[2],m[3],x+(m[0]-64)*size/128,y+(m[1]-64)*size/128,m[2]*size/128,m[3]*size/128);}
 ctx.restore();JR36.hullGlowDraws=(JR36.hullGlowDraws||0)+1;return r;
};
fr27RebelDrawShip=function(q){
 if(q.key!=='jace'||q.dead||rr33Protected()||rg4State()?.rd21?.fleet)return JR36.ship.apply(this,arguments);
 const A=q.rg4?.act,charge=A?.kind==='jr36helix'&&A.phase==='charge',power=charge?clamp(A.t/A.warm,0,1):0;
 const step=Math.floor((A?.t||0)*18)%10,light=PXG_STEPS[step<6?step:10-step],previous=JR36.chargeLight;
 JR36.chargeLight=charge&&q.flash<=0?(.2+.75*power)*light:0;
 let r;try{r=air13DrawRebel(q);}finally{JR36.chargeLight=previous;}
 if(A)rg4Warning(q,A);
 if(charge){const p=rr26Socket(q);jr36Orb(p.x,p.y,24+48*power,A.t,0,.3+.65*power);}
 const T=q.rg4?._rbal19Gun,p=T&&jr36Turret(q,T.side);if(p)jr36Orb(p.x,p.y,12+8*clamp(T.t/T.warm,0,1),T.t,0,.65);
 return r;
};
