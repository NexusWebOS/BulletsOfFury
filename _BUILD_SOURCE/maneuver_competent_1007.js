/* QA-only addition: perceive authored ring arcs, duo hulls and shield perimeter. */
const MVC7={observe:MV7.observe};
MV7.observe=function(){
 const S=MVC7.observe();
 for(const b of [bossActive?boss:null,subBossActive?subBoss:null].filter(Boolean)){
  if(b._s4war?.shield&&(b._s4war.shield.active||b._s4war.shield.rearming))S.circles.push({x:b.x,y:b._drawY??b.y,r:b.w*.67,warn:false});
  for(const q of b._rzbPair?.actors||[]){if(q.dead||q._rzbGone)continue;const R=q._rzb,sc=rzbScale(q),last=BAL7.q.lastSeen.get(q),dt=last?BAL7.q.t-last.t:0;S.bodies.push({x:q.x,y:q.y,vx:dt>.04?(q.x-last.x)/dt:0,vy:dt>.04?(q.y-last.y)/dt:0,rx:105*sc,ry:105*sc});BAL7.q.lastSeen.set(q,{x:q.x,y:q.y,t:BAL7.q.t});
   for(const w of R.waves){if(w.fade<=.28||w.life<=0)continue;for(let rel=-w.arc;rel<=w.arc;rel+=Math.max(.02,12/Math.max(12,w.r))){if(!rzbWaveAngleHit(w,rel))continue;const a=w.a+rel+Math.PI/2;S.bullets.push({x:w.x+Math.cos(a)*w.r,y:w.y+Math.sin(a)*w.r,vx:Math.cos(a)*w.speed,vy:Math.sin(a)*w.speed,rx:w.width+7*sc,ry:w.width+7*sc,kind:'visible-sonic-ring'});}}
  }
 }
 return S;
};
