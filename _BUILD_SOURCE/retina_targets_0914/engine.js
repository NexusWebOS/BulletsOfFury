/* Retina eligibility is shared by scanners and seeking weapons; fields remain damageable
   by ordinary fire, but their protected hull is never advertised as a lock target. */
function retinaHullProtected(b){
  if(!b)return false;
  const S=b._s4war,H=S&&S.shield,F=b._bayShield,X=b._xenoRig;
  return !!(b._noHit||b.enter||(H&&(H.active||H.rearming))||(F&&F.up)||
    (b._bay&&(b._bay.L>0||b._bay.R>0))||(X&&X.shield&&X.mother&&!X.mother.dead)||
    (typeof bossShieldFrac==='function'&&bossShieldFrac(b)>0));
}
function retinaPiece(b,p,kind,pos,w,h){
  if(!b._retinaPieces)b._retinaPieces=[];
  let t=b._retinaPieces.find(t=>t.part===p&&t.kind===kind);
  if(!t){
    t={_retinaOwner:b,part:p,kind,w:w||44,h:h||44,name:kind+' '+(p.id||p.side||p.role||''),pos};
    Object.defineProperties(t,{
      x:{get(){return this.pos().x;}},y:{get(){return this.pos().y;}},
      hp:{get(){return p.hp;}},dead:{get(){return !!(b.dead||p.dead||p.destroyed||p.disabled||p.hp<=0);}}
    });b._retinaPieces.push(t);
  }
  return t;
}
function retinaBossTargets(b){
  const a=[];if(!b||b.dead||b.enter)return a;
  const S=b._s4war,H=S&&S.shield,M=b._mega,X=b._xenoRig;
  if(H&&H.active)for(const n of H.nodes)if(!n.dead)a.push(retinaPiece(b,n,'electrical node',()=>({x:n.x,y:n.y}),48,48));
  if(S&&S.coreUnlocked)for(const p of S.coreTurrets)if(!p.dead&&p.materialize>=.92)a.push(retinaPiece(b,p,'helper',()=>({x:p.x,y:p.y}),80,80));
  if(M&&M.phase>=1)for(const n of M.nodes)if(!n.dead)a.push(retinaPiece(b,n,'storm node',()=>carrierMegaNodePos(b,n),48,48));
  if(b._bay&&b._bayShield&&!b._bayShield.up)for(const side of ['L','R'])if(b._bay[side]>0){
    if(!b._retinaBays)b._retinaBays={};
    let p=b._retinaBays[side];if(!p){p={side};Object.defineProperty(p,'hp',{get(){return b._bay[side];}});b._retinaBays[side]=p;}
    a.push(retinaPiece(b,p,'missile bay',()=>{const q=carrierBayBox(b,side);return{x:(q.x0+q.x1)/2,y:(q.y0+q.y1)/2};},52,64));
  }
  if(X){if(X.mother&&!X.mother.dead){X.mother._xenoOwner=b;a.push(X.mother);}for(const p of X.helpers)if(!p.dead){p._xenoOwner=b;a.push(p);}}
  if(b.modular&&b.parts){for(const p of b.parts)if(p.dmg&&!p.destroyed)a.push(retinaPiece(b,p,'module',()=>({x:b.x+(p.hx!=null?p.hx:p.dx)*(b._wide||1),y:b.y+(p.hy!=null?p.hy:p.dy)}),p.hw*2,p.hh*2));}
  else if(b._s9fusion&&b._s9fusion.phase==='twins'){for(const p of [b._s9fusion.left,b._s9fusion.right])if(p&&!p.disabled){p._spaceBossOwner=b;a.push(p);}}
  else if(b._s9rift&&b._s9rift.core){const p=b._s9rift.core;if(!p.disabled){p._spaceSubOwner=b;a.push(p);}}
  else if(!retinaHullProtected(b))a.push(b);
  return a;
}
function retinaTargetValid(t){return !!(t&&!t.dead&&_lockTargets().indexOf(t)>=0);}
function retinaMissileDamage(t,dmg,shot){
  if(!retinaTargetValid(t))return false;
  _lastHitX=t.x;_lastHitY=t.y;
  if(t._retinaOwner){
    const b=t._retinaOwner,p=t.part;
    if(t.kind==='storm node')carrierMegaNodeDamage(b,p,dmg);
    else if(t.kind==='electrical node'){b._s4ShieldHit=p;stage4ShieldAbsorbHit(b,dmg,t.x,t.y);}
    else if(t.kind==='helper')stage4CoreTurretDamage(b,p,dmg);
    else if(t.kind==='missile bay')carrierBayDamage(b,p.side,dmg,t.x,t.y,null);
    else if(t.kind==='module'){b._lastPart=p;hitBoss(dmg);}
  }else if(t._xenoOwner||t._spaceBossOwner||t._spaceSubOwner)spaceDamageTarget(t,dmg,shot);
  else if(t===boss)hitBoss(dmg);
  else if(t===subBoss)hitSubBoss(dmg,t.x,t.y);
  else if(typeof rival!=='undefined'&&t===rival)hitRival(dmg);
  else hitEnemy(t,dmg);
  return true;
}
function _lockTargets(){
  const t=[];
  for(const e of enemies)if(!e.dead&&e.y>PLAY.y-8&&e.y<VH)t.push(e);
  if(typeof subBoss!=='undefined'&&subBossActive)t.push(...retinaBossTargets(subBoss));
  if(bossActive)t.push(...retinaBossTargets(boss));
  if(typeof rival!=='undefined'&&rival&&rival.phase==='fight'&&rival.hp>0&&!rival.dead)t.push(rival);
  return t;
}
