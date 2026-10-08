// QA-only perception for authored, visible stage hazards. Does not change gameplay.
const WORLD7_BASE=MV7.observe;
MV7.observe=function(){
 const S=WORLD7_BASE(),Q=BAL7.q;
 for(const d of fireDebris)if(!d.dead&&d.delay<=0&&d.y>=PLAY.y-35&&d.y<=VH+35)S.bullets.push({x:d.x,y:d.y,vx:d.vx*60,vy:d.vy*60,ay:DEBRIS_G*3600,rx:d.r,ry:d.r,kind:'volcanic-debris'});
 for(const g of geysers)if(g.hostile&&g.t<g.life)S.bodies.push({x:g.x,y:g.y-g.h/2,vx:0,vy:0,rx:geyserLane(g)*.75,ry:g.h/2});
 for(const v of s2Vents)if(!v.done)S.lines.push({x:v.x,y:v.y,ex:v.x,ey:v.y-GEYSER_H,width:geyserLane({kind:'fire'})*1.5,warn:true});
 const f=wfx?.fseq,w=f?.wave;
 if(w&&w.y>=PLAY.y-170){const r=150*w.sc*.34;S.bodies.push({x:w.x,y:w.y,vx:0,vy:(VH+300)/FIRE_CROSS,rx:r+9,ry:r+9});}
 const b=subBossActive?subBoss:null;
 if(b&&!b.enter&&!b._noHit&&!b._jcGhost&&!b._tempestDuo&&!b._rzbPair&&!b._hd1003&&(!b._harrier||b._chCollision)){
  const q=S.bodies.find(q=>Math.hypot(q.x-b.x,q.y-b.y)<3);
  if(q){q.y=b._drawY||b.y;q.rx=b.w/2+1;q.ry=b.h/2+1;q.vx=clamp(q.vx,-600,600);q.vy=clamp(q.vy,-600,600);}
 }
 return S;
};
