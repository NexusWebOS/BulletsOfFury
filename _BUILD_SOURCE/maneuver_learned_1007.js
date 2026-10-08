/* QA profile: recognizes the rendered warning lanes and beam silhouettes. */
const MV7_LEARNED={warn:combatWarningDraw,beam:av3Beam,draw:drawWorld,observe:MV7.observe};
MV7.visibleWarnings=[];MV7.visibleBeams=[];
combatWarningDraw=function(owner,q){
 if(MV7.recording&&q&&[q.x,q.y,q.ex,q.ey].every(Number.isFinite)&&q.progress!=null){const a=Math.atan2(q.ey-q.y,q.ex-q.x),len=q.len||Math.max(120,Math.sin(a)>.25?(VH-q.y)/Math.sin(a):Math.max(VW,VH)*1.25);MV7.visibleWarnings.push({x:q.x,y:q.y,ex:q.x+Math.cos(a)*len,ey:q.y+Math.sin(a)*len,width:q.width||20,warn:true});}
 return MV7_LEARNED.warn.apply(this,arguments);
};
av3Beam=function(g,x,y,a,len,width,color,t,alpha){if(MV7.recording&&(alpha==null||alpha>.1))MV7.visibleBeams.push({x,y,ex:x+Math.cos(a)*len,ey:y+Math.sin(a)*len,width,warn:false});return MV7_LEARNED.beam.apply(this,arguments);};
drawWorld=function(){MV7.visibleWarnings=[];MV7.visibleBeams=[];MV7.recording=true;try{return MV7_LEARNED.draw.apply(this,arguments);}finally{MV7.recording=false;}};
MV7.observe=function(){const S=MV7_LEARNED.observe();S.lines.push(...MV7.visibleWarnings,...MV7.visibleBeams);
 for(const b of [bossActive?boss:null,subBossActive?subBoss:null].filter(Boolean)){
  if(b._chargeTell){const T=b._chargeTell;S.lines.push({x:T.lane,y:PLAY.y,ex:T.lane,ey:VH,width:(b.w||150)*.75,warn:true});}
  if(b._chg&&b._ovState==='chargeOff')S.lines.push({x:b._chg.lane,y:PLAY.y,ex:b._chg.lane,ey:VH,width:(b.w||150)*.75,warn:false});
  for(const q of b._rzbPair?.tanks||b._rzbPair?.ships||[]){if(q&&!q.dead)S.bodies.push({x:q.x,y:q.y,vx:0,vy:0,rx:105*rzbScale(q),ry:105*rzbScale(q)});}
 }
 return S;
};
