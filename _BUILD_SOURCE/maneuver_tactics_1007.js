
const MT7={observe:MV7.observe,rotors:new WeakMap()};
MV7.observe=function(){const S=MT7.observe();
 for(const b of [bossActive?boss:null,subBossActive?subBoss:null].filter(Boolean)){
  const H=b._s4war?.shield;
  if(H&&(H.active||H.rearming)){S.targets=H.nodes.filter(n=>!n.dead&&n.hp>0).map(n=>({x:n.x,y:n.y,vx:0,important:true}));}
  const C=hc1007CrossState(b);if(C){const previous=MT7.rotors.get(b),dt=previous?S.time-previous.time:0,omega=dt>.04?Math.atan2(Math.sin(C.angle-previous.angle),Math.cos(C.angle-previous.angle))/dt:0;MT7.rotors.set(b,{angle:C.angle,time:S.time});for(const L of S.lines)if(C.rays.some(r=>Math.hypot(r.x-L.x,r.y-L.y)<2))L.omega=omega;}
  // Single-tank sonic waves use the same visibly expanding arcs as the hard-mode pair.
  if(b._rzb){const R=b._rzb,sc=rzbScale(b);for(const w of R.waves){if(w.fade<=.28||w.life<=0)continue;for(let rel=-w.arc;rel<=w.arc;rel+=Math.max(.02,12/Math.max(12,w.r))){if(!rzbWaveAngleHit(w,rel))continue;const a=w.a+rel+Math.PI/2;S.bullets.push({x:w.x+Math.cos(a)*w.r,y:w.y+Math.sin(a)*w.r,vx:Math.cos(a)*w.speed,vy:Math.sin(a)*w.speed,rx:w.width+7*sc,ry:w.width+7*sc,kind:'visible-sonic-ring'});}}}
 }
 return S;
};
