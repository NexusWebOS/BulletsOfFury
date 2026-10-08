'use strict';
/* finale_forms_1008.js - Mike, 2026-10-08: "The sword knight and hammer forms he has, are very very underwhelming
   compared to the actual hammer boss. Also, he was stuck on the knight form after i destroyed all other forms and
   unbeatable."

   Loaded last. Four changes to Dracodia's copied knight (pool 5) and Code Hammer (pool 8):

   1. PRESENCE. Both rigs were drawn at 0.68 / 0.76 of their authored cells - about half the real Stage 5 Hammer on
      screen. The whole rig (and therefore every hit box, blade line and muzzle read off it) is scaled up about the
      boss's own centre, so pictures and collision stay one thing.
   2. HIT FLASH. Under steady fire every hit re-armed the white silhouette, so both forms spent most of a fight as a
      white shape (measured on the native contact sheets). The white still lands on every hit - as a flicker capped
      below full white, so the armour and the art stay readable.
   3. THE KNIGHT HITS LIKE THE HAMMER. Shorter recovery between moves, a radial code shockwave wherever a leap or a
      shield smite lands, and a new warned BLADE TEMPEST: a committed horizontal lane, a sweep across the whole arena
      with the sword spinning, code rounds spilling off it.
   4. NO UNBEATABLE LAST FORM. Measured on the live game: the Code Hammer took 0 damage in 38 s of continuous Normal
      fire (its chromium armour equals its whole pool and the source Hammer's recovery heals it), and every copy
      rotates home on a 38/44 s timer. When it is the last pool alive the fight could only loop back into it. Now the
      copy's armour is a share of its pool, a copied form may heal once per fight, and the last pool alive neither
      rotates away nor heals. */

const FF8={scale:{5:1.42,8:1.38},log:[]};
const FF8_BASE={rig:fmcRig,white:fmcWhiteBlit,cell:fmcCell,knight:hk5KnightTick,donor:gd4Tick,draw:r30DrawBoss};
function ff8Diff(){return diffKey==='furious'||diffKey==='insanity'?3:diffKey==='hard'?2:1;}
function ff8Mimic(b){const J=b&&typeof j3State==='function'?j3State(b):null;return J&&J.encounter===2?J.mimic:null;}
function ff8Last(J){return J.hp.filter(h=>h>0).length<=1;}

/* ---- 1. presence: one scale for picture and collision ---- */
fmcRig=function(b){
 const rig=FF8_BASE.rig.apply(this,arguments),k=FF8.scale[ff8Mimic(b)];if(!k||!rig)return rig;
 const T=b._r30&&b._r30.ff8Tempest,spin=T&&T.phase==='sweep'?T.t*14*T.dir:0,c=Math.cos(spin),s=Math.sin(spin);
 return rig.map(v=>{const o=Object.assign({},v);
  for(const [kx,ky] of [['x','y'],['ax','ay']]){if(!Number.isFinite(o[kx]))continue;
   let dx=(o[kx]-b.x)*k,dy=(o[ky]-b.y)*k;if(spin){const rx=dx*c-dy*s;dy=dx*s+dy*c;dx=rx;}o[kx]=b.x+dx;o[ky]=b.y+dy;}
  if(Number.isFinite(o.w))o.w*=k;if(Number.isFinite(o.h))o.h*=k;if(spin)o.rot=(o.rot||0)+spin;return o;});
};

/* ---- 2. the hit flash is a flicker, not a silhouette ---- */
fmcWhiteBlit=function(key,x,y,w,h,rot=0,alpha=1){
 if(!ff8Third())return FF8_BASE.white.apply(this,arguments);
 const t=typeof stateT!=='undefined'?stateT:0;if(Math.floor(t*30)%3===2)return;   // two frames on, one off
 return FF8_BASE.white.call(this,key,x,y,w,h,rot,Math.min(alpha,.58));
};

function ff8Third(){return typeof boss!=='undefined'&&boss&&boss._r30&&typeof j3State==='function'&&j3State(boss)&&j3State(boss).encounter===2;}
// the authored-cell rigs (knight, Code Hammer, copied forms) flash through fmcCell with a white tint - same flicker
fmcCell=function(sheet,part,x,y,w,h,rot,alpha,tint){
 if(tint!=='#ffffff'||!ff8Third())return FF8_BASE.cell.apply(this,arguments);
 const t=typeof stateT!=='undefined'?stateT:0;if(Math.floor(t*30)%3===2)return false;
 return FF8_BASE.cell.call(this,sheet,part,x,y,w,h,rot,Math.min(alpha==null?1:alpha,.58),tint);
};

/* ---- 3. the knight ---- */
function ff8Ring(b,x,y,n,spd,gap){
 // a radial code shockwave with a deliberate gap facing away from the player's current side, so it reads and dodges
 const away=Math.atan2(y-player.y,x-player.x),half=gap/2;
 for(let i=0;i<n;i++){const a=i/n*Math.PI*2;let d=Math.atan2(Math.sin(a-away),Math.cos(a-away));if(Math.abs(d)<half)continue;
  const q=eShootT(x,y,a,spd,'eglaser',{w:20,h:22});if(q){q._hkCodeFire=true;q._hkOwner=b;q.t=0;q.w=q.h=20;(b._r30.hkShots??=[]).push(q);}}
 r30Sound('expBig');shake=Math.max(shake||0,5);
}
function ff8TempestStart(b){
 const S=b._r30,d=ff8Diff(),left=camLeftX()+70,right=camRightX()-70,fromLeft=b.x>(left+right)/2?false:true;
 const lane=clamp(player.y-10,PLAY.y+170,hammerWarningFloorY()-30);
 S.ff8Tempest={phase:'tell',t:0,ox:b.x,oy:b.y,sx:fromLeft?left:right,ex:fromLeft?right:left,dir:fromLeft?1:-1,lane,
  tell:d===3?.95:d===2?1.05:1.2,sweep:d===3?1.05:d===2?1.2:1.35,shot:0,hit:new Set()};
 FF8.log.push({event:'tempest',lane,diff:diffKey});
}
function ff8TempestTick(b,D,dt){
 const S=b._r30,T=S.ff8Tempest,d=ff8Diff();T.t+=dt;
 if(!fmcAlive(b,'sword')&&T.phase!=='recover'){T.phase='recover';T.t=0;}
 if(T.phase==='tell'){
  // glide to the lane's start while the lane is warned; the lane is committed and does not follow the player
  const u=clamp(T.t/T.tell,0,1);b.x=lerp(T.ox,T.sx,Math.min(1,u*1.6));b.y=lerp(T.oy,T.lane,Math.min(1,u*1.6));
  combatWarningTick(b,'ff8-tempest',T.t,T.tell);if(T.t>=T.tell){T.phase='sweep';T.t=0;r30Sound('combatAlien0927');}
 }else if(T.phase==='sweep'){
  const u=clamp(T.t/T.sweep,0,1),e=u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;b.x=lerp(T.sx,T.ex,e);b.y=T.lane+Math.sin(u*Math.PI*3)*6;
  for(const seat of seatList())withSeat(seat,()=>{if(T.hit.has(seat)||player.dead)return;
   if(Math.abs(player.x-b.x)<62&&Math.abs(player.y-b.y)<44){playerHit('alien blade tempest');T.hit.add(seat);}});
  T.shot-=dt;if(T.shot<=0){T.shot=d===3?.10:d===2?.13:.18;
   const spin=T.t*9;for(const off of d>=2?[0,Math.PI]:[0]){const q=eShootT(b.x,b.y,Math.PI/2+Math.sin(spin+off)*.9,d===3?3.2:2.7,'eglaser',{w:18,h:20});
    if(q){q._hkCodeFire=true;q._hkOwner=b;q.t=0;q.w=q.h=18;(S.hkShots??=[]).push(q);}}}
  if(T.t>=T.sweep){T.phase='recover';T.t=0;ff8Ring(b,b.x,b.y,d===3?16:12,2.4,1.1);}
 }else{
  b.x=lerp(b.x,T.ox,Math.min(1,dt*4));b.y=lerp(b.y,T.oy,Math.min(1,dt*4));
  if(T.t>=.7){S.ff8Tempest=null;S.hkKnightCd=d===3?.45:d===2?.6:.8;}
 }
 D.p.x=b.x;D.p.y=b.y;
}
hk5KnightTick=function(b,D,dt){
 const S=b._r30;
 if(S.ff8Tempest)return ff8TempestTick(b,D,dt);
 // every third move is the tempest, once the knight has his sword
 if(!S.hkKnight&&(S.hkKnightCd??1.2)-dt<=0&&fmcAlive(b,'sword')&&((S.ff8N=(S.ff8N||0)+1)%3===0)){ff8TempestStart(b);return ff8TempestTick(b,D,0);}
 const K0=S.hkKnight,was=K0&&K0.phase,kind=K0&&K0.kind;
 const r=FF8_BASE.knight.apply(this,arguments);
 const K=S.hkKnight,d=ff8Diff();
 // a landing leap and a finished shield smite both throw the code shockwave
 if(K&&kind==='leapSlash'&&was==='jump'&&K.phase==='land')ff8Ring(b,K.tx,K.ty,d===3?18:d===2?14:12,2.6,1.0);
 if(kind==='shieldSmite'&&was==='active'&&(!K||K.phase==='recover'))ff8Ring(b,b.x,b.y+30,d===3?12:10,2.3,1.2);
 if(!S.hkKnight&&S.hkKnightCd>0)S.hkKnightCd=Math.min(S.hkKnightCd,d===3?.45:d===2?.6:.8);
 return r;
};

/* ---- 4. no unbeatable last form, and a Code Hammer that can be worn down ---- */
gd4Tick=function(b,dt){
 const J=j3State(b),i=J&&J.encounter===2?J.mimic:null;
 const D=i!=null&&J.gp4Donors?J.gp4Donors[i]:null,before=b.hp;
 const r=FF8_BASE.donor.apply(this,arguments);
 if(i==null||!J)return r;
 const last=ff8Last(J),D2=D||(J.gp4Donors&&J.gp4Donors[i]);
 // the last pool alive stays: no timer sends it home and back into itself
 if(last&&D2&&b._r30.mode==='fight')D2.age=0;
 if(i===8&&D2){const h=D2.p._hammer,A=h&&h.frArmor;
  if(A&&!A.ff8){const cap=Math.round(J.max[8]*(ff8Diff()===3?.45:ff8Diff()===2?.40:.35));A.max=cap;A.hp=Math.min(A.hp,cap);A.ff8=true;}
 }
 // a copied form heals at most once per fight, and never while it is the last pool alive
 if(b.hp>before+1&&b._r30.mode==='fight'&&J.mimic===i){
  J.ff8Healed=J.ff8Healed||{};
  if(last||J.ff8Healed[i]){b.hp=before;j3Health(b,b.hp,b.maxhp);J.hp[i]=Math.min(J.hp[i],b.hp);if(D2)D2.p.hp=b.hp;}
  else J.ff8Healed[i]=true;
 }
 return r;
};

/* ---- the tempest's lane warning, drawn with the boss ---- */
r30DrawBoss=function(b){
 const T=b&&b._r30&&b._r30.ff8Tempest;
 if(T&&T.phase==='tell'){const u=T.t/T.tell,flash=(Math.floor(T.t*(u>.66?14:8))%2)===0,col=u<.33?'90,255,120':u<.66?'255,214,60':'255,60,60';
  ctx.save();ctx.fillStyle='rgba('+col+','+(flash?.30:.16)+')';ctx.fillRect(camLeftX(),T.lane-34,camRightX()-camLeftX(),68);
  ctx.fillStyle='rgba('+col+',.85)';ctx.fillRect(camLeftX(),T.lane-35,camRightX()-camLeftX(),2);ctx.fillRect(camLeftX(),T.lane+33,camRightX()-camLeftX(),2);ctx.restore();}
 return FF8_BASE.draw.apply(this,arguments);
};
window.BOFFinaleForms=FF8;
