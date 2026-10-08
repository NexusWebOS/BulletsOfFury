/* QA only: visible attack geometry and target selection with delayed observations.
   Does not change damage, movement, boss state, stocks, drops or cooldowns. */
const MB7={observe:MV7.observe,decide:MV7.decide,seen:new WeakMap(),lineSeen:new Map()};
MV7.observe=function(){
 const S=MB7.observe(),Q=BAL7.q;
 const velocity=(o,x,y)=>{const prev=MB7.seen.get(o),dt=prev?S.time-prev.t:0;MB7.seen.set(o,{x,y,t:S.time});return {vx:dt>.04?clamp((x-prev.x)/dt,-650,650):0,vy:dt>.04?clamp((y-prev.y)/dt,-650,650):0};};
 const body=(o,x,y,rx,ry)=>S.bodies.push({x,y,rx,ry,...velocity(o,x,y)});
 const line=(L,warn,key)=>{if(![L.x,L.y,L.ex,L.ey].every(Number.isFinite))return;const a=Math.atan2(L.ey-L.y,L.ex-L.x),p=MB7.lineSeen.get(key),dt=p?S.time-p.t:0;const omega=dt>.04&&p.warn===warn?clamp(Math.atan2(Math.sin(a-p.a),Math.cos(a-p.a))/dt,-4,4):0;MB7.lineSeen.set(key,{a,t:S.time,warn});S.lines.push({...L,omega,warn});};
 // Normal rounds damage through their compact ink core; the earlier observer
 // treated half the entire image cell as solid, including transparent padding.
 S.bullets=S.bullets.filter(q=>q.kind==='visible-sonic-ring');
 for(const q of eBullets){if(q.dead||q.x<camLeftX()-70||q.x>camRightX()+70||q.y<PLAY.y-70||q.y>VH+70)continue;
  const v=velocity(q,q.x,q.y),a=Math.atan2(v.vy||q.vy,v.vx||q.vx);let rx=Math.max(2,(q.w||10)*.15),ry=Math.max(2,(q.h||10)*.15);
  if(q._hammerLaser){rx=Math.abs(Math.cos(a))*(q.h||20)/2+Math.abs(Math.sin(a))*(q.w||8)/2;ry=Math.abs(Math.sin(a))*(q.h||20)/2+Math.abs(Math.cos(a))*(q.w||8)/2;}
  if(q._ovSonicWave){rx=q._waveW*.42;ry=q._waveH*.32;}
  S.bullets.push({x:q.x,y:q.y,vx:v.vx||q.vx*60||0,vy:v.vy||q.vy*60||0,rx,ry,kind:q.kind});
 }
 for(const z of zoneCols)if(z.hostile&&z.t<z.warn+z.life)line({x:z.x0+z.w/2,y:PLAY.y,ex:z.x0+z.w/2,ey:VH,width:z.w-8},z.t<z.warn,'zone'+z.x0);
 for(const b of [bossActive?boss:null,subBossActive?subBoss:null].filter(Boolean)){
  const F=b._fz,H=b._hammer,A=b._s4war,J=j3State(b),donor=J?.gp4Donors?.[J.mimic]?.p;
  if(donor?._fz){donor._fz.beams.forEach((q,i)=>line(q,false,'donorbeam'+i));donor._fz.tells.filter(q=>q.kind!=='ring').forEach((q,i)=>line({...q,width:q.width||36},true,'donortell'+i));}
  if(F){
   // Aim at the visible open armor, not at the invulnerable middle of the torso.
   const targets=furnaceBoxes(b);if(targets.length)S.targets=targets.map(t=>({x:t.x,y:t.y,vx:0,important:true,id:t.key}));
   S.bodies=S.bodies.filter(q=>Math.hypot(q.x-b.x,q.y-b.y)>3);
   for(const q of targets)body(F.arm[q.key]||b,q.x,q.y,q.r,q.r);
   F.beams.forEach((q,i)=>line({...q,width:q.width*(q.kind==='flame'?1.25:1)+12*FZT_S},false,'fzbeam'+i));
   F.tells.filter(q=>q.kind!=='ring').forEach((q,i)=>line({...q,width:q.width||36},true,'fztell'+i));
  }
  if(A){
   const shield=A.shield;const nodes=shield?.active?(shield.nodes||[]).filter(n=>!n.dead&&n.hp>0):[];
   const helpers=(A.coreTurrets||[]).filter(n=>!n.dead&&n.materialize>=1);
   if(nodes.length)S.targets=nodes.map((n,i)=>({x:n.x,y:n.y,vx:0,important:true,id:'generator'+i}));
   else if(!shield?.active&&!shield?.rearming)S.targets=[{x:b.x,y:b.y,vx:0,important:true,id:'exposed-hull'}];
   for(const n of [...nodes,...helpers])body(n,n.x,n.y,36,36);
   if(shield&&(shield.active||shield.rearming)){const v=velocity(shield,b.x,b.y);for(const q of S.circles)if(Math.hypot(q.x-b.x,q.y-b.y)<3)Object.assign(q,v);}
  }
  if(H){
   if(!b._noHit){S.bodies=S.bodies.filter(q=>Math.hypot(q.x-b.x,q.y-b.y)>3);body(b,b.x,b.y,H.state==='ball'?54:72,H.state==='ball'?54:72);}
   if(H.throw){const t=H.throw;body(t,t.x,t.y,42,42);}
   if(H.whirl&&['whirlwind','whirl_warn','whirl_turn'].includes(H.state))line({x:H.whirl.l,y:H.whirl.y+36,ex:H.whirl.r,ey:H.whirl.y+36,width:208},H.state!=='whirlwind','whirl');
   if(['warn','leap'].includes(H.state))S.circles.push({x:H.tx,y:H.ty+32,r:74,warn:H.state==='warn'});
   if(['giant_warn','giant_dive','giant_sweep'].includes(H.state))line({x:H.tx-150,y:H.ty,ex:H.tx+150,ey:H.ty,width:156},H.state!=='giant_sweep','giant');
   if(hammerWeaponTargetable(b)&&!b._noHit&&(!H.hammerDestroyed||H.recovery?.status==='charging')){const t=hammerHeadPoint(b);S.targets=[{x:t.x,y:t.y,vx:0,important:true,id:'hammer'}];}
   if(H.state==='mega_beam'||H.state==='mega_charge')line({x:b.x,y:b.y,ex:b.x,ey:VH,width:hammerEradWidth()},H.state==='mega_charge','eradication');
   for(const q of H.stormWaves||[]){const z=hammerStormRedZone(q);if(z)line({x:z.x,y:z.top,ex:z.x,ey:z.y,width:z.width},true,'storm'+z.x);}
  }
  if(J&&r30Live(b)){
   S.bodies=S.bodies.filter(q=>Math.hypot(q.x-b.x,q.y-b.y)>3);
   for(const v of r30Parts(b))if(v.alpha>.5&&!v.p.destroyed)body(v.p,v.x,v.y,Math.abs(Math.cos(v.rot))*v.w*.43+Math.abs(Math.sin(v.rot))*v.h*.44,Math.abs(Math.sin(v.rot))*v.w*.43+Math.abs(Math.cos(v.rot))*v.h*.44);
  }
 }
 return S;
};
// Move the complete shield envelope using its observed velocity, like the body.
// The copy below changes only perception/prediction and charge-button release.
MV7.decide=function(S){
 const Q=BAL7.q;
 const margin=Q.c.margin??12;
 // A learned target stays selected until it disappears, instead of constantly
 // changing arms with the nearest one while dodging.
 if(S.targets.length){let target=S.targets.find(t=>t.id&&t.id===Q.aimId);if(!target)target=S.targets.slice().sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0];Q.aimId=target.id;Q.aimPoint={x:target.x,y:target.y};S.targets=[target];}
 return MB7.decide(S);
};
