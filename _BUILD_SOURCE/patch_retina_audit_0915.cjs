const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
let src=fs.readFileSync(file,'utf8');
if(src.includes('function retinaDynamicPiece(')){
  console.log('Retina audit patch already applied.');
  process.exit(0);
}
if(src.includes('\r'))throw new Error('assets/game.js must remain LF-only');
const start=src.indexOf('function retinaPiece(b,p,kind,pos,w,h){');
const end=src.indexOf('function retinaTargetValid(t)',start);
if(start<0||end<0)throw new Error('retina target block not found');
const old=src.slice(start,end);
if((old.match(/function retinaBossTargets/g)||[]).length!==1)throw new Error('unexpected retina target block');
const next=`function retinaPiece(b,p,kind,pos,w,h){
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
/* Some authored encounters keep their pools in maps rather than part objects. This stable
   wrapper lets the Retina follow those moving plates without copying or replacing their art. */
function retinaDynamicPiece(b,id,kind,state,hit,w,h){
  if(!b._retinaDynamic)b._retinaDynamic=[];
  let t=b._retinaDynamic.find(t=>t._retinaId===id&&t.kind===kind);
  if(!t){
    t={_retinaOwner:b,_retinaId:id,kind:kind,name:kind+' '+id,w:w||44,h:h||44,_retinaState:state,_retinaHit:hit};
    Object.defineProperties(t,{
      x:{get(){const q=this._retinaState();return q.x;}},y:{get(){const q=this._retinaState();return q.y;}},
      hp:{get(){const q=this._retinaState();return q.hp;}},
      dead:{get(){const q=this._retinaState();return !!(b.dead||q.dead||q.hp<=0);}}
    });b._retinaDynamic.push(t);
  }else{t._retinaState=state;t._retinaHit=hit;t.w=w||t.w;t.h=h||t.h;}
  return t;
}
function retinaImpactTarget(b,id,kind,state,w,h){
  return retinaDynamicPiece(b,id,kind,state,function(dmg){
    const q=state();_lastHitX=q.x;_lastHitY=q.y;
    if(typeof boss!=='undefined'&&b===boss)hitBoss(dmg);
    else if(typeof subBoss!=='undefined'&&b===subBoss)hitSubBoss(dmg,q.x,q.y);
  },w,h);
}
function retinaMechPartState(b,id){
  const K=b._mech,M=_mechMeta(K.tag),p=K.parts[id];
  if(!M||!p)return{x:b.x,y:b.y,hp:0,dead:true};
  const bd=M.components[id].bounds,S=(b.w/(M.canvas?M.canvas[0]:384))*(K.scale||1)*(MECH_SCALE[K.tag]||1);
  return{x:b.x+((bd[0]+bd[2])/2-192)*S,y:(b._drawY!=null?b._drawY:b.y)+((bd[1]+bd[3])/2-192)*S,
    w:(bd[2]-bd[0])*S,h:(bd[3]-bd[1])*S,hp:p.hp,dead:p.state==='destroyed'||!p.docked};
}
function retinaBossTargets(b){
  const a=[];if(!b||b.dead||b.enter)return a;
  const S=b._s4war,H=S&&S.shield,M=b._mega,X=b._xenoRig;
  let sectional=false;
  if(H&&H.active)for(const n of H.nodes)if(!n.dead)a.push(retinaPiece(b,n,'electrical node',()=>({x:n.x,y:n.y}),48,48));
  if(S&&S.coreUnlocked)for(const p of S.coreTurrets)if(!p.dead&&p.materialize>=.92)a.push(retinaPiece(b,p,'helper',()=>({x:p.x,y:p.y}),80,80));
  if(M&&M.phase>=1)for(const n of M.nodes)if(!n.dead)a.push(retinaPiece(b,n,'storm node',()=>carrierMegaNodePos(b,n),48,48));
  if(b._bay&&b._bayShield&&!b._bayShield.up)for(const side of ['L','R'])if(b._bay[side]>0){
    if(!b._retinaBays)b._retinaBays={};
    let p=b._retinaBays[side];if(!p){p={side};Object.defineProperty(p,'hp',{get(){return b._bay[side];}});b._retinaBays[side]=p;}
    a.push(retinaPiece(b,p,'missile bay',()=>{const q=carrierBayBox(b,side);return{x:(q.x0+q.x1)/2,y:(q.y0+q.y1)/2};},52,64));
  }
  if(X){if(X.mother&&!X.mother.dead){X.mother._xenoOwner=b;a.push(X.mother);}for(const p of X.helpers)if(!p.dead){p._xenoOwner=b;a.push(p);}}
  if(b._furnace){
    sectional=true;
    if(!(b._mwBarrier&&b._mwBarrier.active))for(const q of furnaceBoxes(b)){
      const id=q.key,state=()=>{const z=furnaceBoxes(b).find(v=>v.key===id);return z?{x:z.x,y:z.y,hp:b._fz.pools[id],dead:false}:{x:b.x,y:b.y,hp:0,dead:true};};
      a.push(retinaImpactTarget(b,id,'furnace '+id,state,q.r*2,q.r*2));
    }
  }else if(b._mech){
    sectional=true;const K=b._mech;
    if(K.phase==='fight')for(const id of _mechOrder(K)){
      const p=K.parts[id];if(!p||p.state==='destroyed'||!p.docked)continue;
      if(id==='torso'&&mechShieldUp(K))continue;if(id==='head'&&mechHeadLocked(K))continue;
      const state=()=>retinaMechPartState(b,id),q=state();
      a.push(retinaImpactTarget(b,id,'mech '+id,state,Math.max(36,q.w||0),Math.max(36,q.h||0)));
    }
  }else if(b._sx){
    sectional=true;const U=SX_UNITS[b._sx.code];
    if(U&&!b._armored&&!b._shielded)for(const id of U.parts)if(!b._sx.dead[id]){
      const state=()=>{const o=sxPartOffset(b._sx.code,id,b);return{x:b.x+o.x,y:b.y+o.y,hp:b._sx.hp[id],dead:b._sx.dead[id]};};
      a.push(retinaImpactTarget(b,id,'section '+id,state,48,48));
    }
  }else if(b._rzb){
    sectional=true;const R=b._rzb,ids=R.state==='guns'?['left','right']:[R.state];
    if(R.state!=='arrival'&&R.trans<=0)for(const id of ids)if(R.pools[id]>0){
      const state=()=>{const q=id==='left'||id==='right'?rzbWorld(b,id==='left'?-57:57,96):{x:b.x,y:b.y};return{x:q.x,y:q.y,hp:R.pools[id],dead:R.pools[id]<=0||R.state!==((id==='left'||id==='right')?'guns':id)||R.trans>0};};
      a.push(retinaImpactTarget(b,id,'razorback '+id,state,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2,(RZB_R[id==='left'||id==='right'?'gun':id]||34)*2));
    }
  }else if(b._tempestDuo){
    sectional=true;
    for(const p of b._tempestDuo.ships)if(!p.dead&&p._tlv.vuln){
      const side=p._tempestGray?'gray':'black';
      for(let i=0;i<4;i++)if(p._tlv.ap[i].hp>0){const id=side+' aperture '+i,state=()=>{const q=tempestPortXY(p,i);return{x:q.x,y:q.y,hp:p._tlv.ap[i].hp,dead:p.dead||!p._tlv.vuln||p._tlv.ap[i].hp<=0};};a.push(retinaImpactTarget(b,id,'aperture',state,30,34));}
      const state=()=>({x:p.x,y:p.y,hp:p._ai&&p._ai.hp!=null?p._ai.hp:1,dead:p.dead||!p._tlv.vuln});
      a.push(retinaImpactTarget(b,side+' hull','tempest hull',state,p.w,p.h));
    }
  }else if(b._tlv){
    sectional=true;const T=b._tlv;
    if(T.vuln){for(let i=0;i<4;i++)if(T.ap[i].hp>0){const state=()=>{const q=tempestPortXY(b,i);return{x:q.x,y:q.y,hp:T.ap[i].hp,dead:!T.vuln||T.ap[i].hp<=0};};a.push(retinaImpactTarget(b,'aperture '+i,'aperture',state,30,34));}
      a.push(retinaImpactTarget(b,'hull','tempest hull',()=>({x:b.x,y:b.y,hp:b.hp,dead:!T.vuln}),b.w,b.h));}
  }else if(b._ql&&!b._qlHullOpen&&(b._qlCan||[]).some(c=>!c.dead)){
    sectional=true;const sc=(b.w||196)/384;
    for(const c of b._qlCan)if(!c.dead&&c.hb){const state=()=>({x:b.x+(c.hb[0]+c.hb[2]/2-192)*sc,y:b.y+(c.hb[1]+c.hb[3]/2-192)*sc,hp:c.hp,dead:c.dead});a.push(retinaImpactTarget(b,c.id,'laser turret',state,c.hb[2]*sc,c.hb[3]*sc));}
  }
  const F=b._s7warden&&b._s7warden.final;
  if(F&&F.phase==='stun'){
    sectional=true;for(const c of F.cores)if(!c.dead){const state=()=>{const q=s7WardenCorePos(b,c.side);return{x:q.x,y:q.y,hp:c.hp,dead:c.dead};};a.push(retinaImpactTarget(b,'core '+c.side,'toxic core',state,54,54));}
  }
  if(b._rapWing){for(const side of ['L','R']){const p=b._rapWing[side];if(!p.dead){const state=()=>({x:b.x+(side==='L'?-1:1)*(b.w||340)*.31,y:b.y,hp:p.hp,dead:p.dead});a.push(retinaImpactTarget(b,'wing '+side,'wing',state,(b.w||340)*.3,b.h*.5));}}}
  if(b.modular&&b.parts){sectional=true;for(const p of b.parts)if(p.dmg&&!p.destroyed)a.push(retinaPiece(b,p,'module',()=>({x:b.x+(p.hx!=null?p.hx:p.dx)*(b._wide||1),y:b.y+(p.hy!=null?p.hy:p.dy)}),p.hw*2,p.hh*2));}
  else if(b._s9fusion&&b._s9fusion.phase==='twins'){sectional=true;for(const p of [b._s9fusion.left,b._s9fusion.right])if(p&&!p.disabled){p._spaceBossOwner=b;a.push(p);}}
  else if(b._s9rift&&b._s9rift.core){sectional=true;const p=b._s9rift.core;if(!p.disabled){p._spaceSubOwner=b;a.push(p);}}
  if(!sectional&&!retinaHullProtected(b))a.push(b);
  return a;
}
`;
src=src.slice(0,start)+next+src.slice(end);
const damageOld=`  if(t._retinaOwner){\n    const b=t._retinaOwner,p=t.part;`;
const damageNew=`  if(t._retinaHit){t._retinaHit(dmg,shot);}\n  else if(t._retinaOwner){\n    const b=t._retinaOwner,p=t.part;`;
if(!src.includes(damageOld))throw new Error('retina damage router not found');
src=src.replace(damageOld,damageNew);
if(src.includes('\r'))throw new Error('patch introduced CR');
fs.writeFileSync(file,src,'utf8');
console.log('Applied complete Retina component audit patch.');
