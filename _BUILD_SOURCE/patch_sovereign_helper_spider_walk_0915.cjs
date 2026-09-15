const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(file,'utf8');
function one(a,b,label){const i=s.indexOf(a);if(i<0||i!==s.lastIndexOf(a))throw new Error(label+' match count is not one');s=s.slice(0,i)+b+s.slice(i+a.length);}
one(
"  S.coreEnrage={active:true,t:0,dur:duration,mode:'deploy',sourceSide:node&&node.side||0,shots:0,leftShots:0,rightShots:0,gaps:0};",
"  S.coreEnrage={active:true,t:0,dur:duration,mode:'deploy',sourceSide:node&&node.side||0,shots:0,leftShots:0,rightShots:0,gaps:0,\n"+
"    walkActive:false,walkT:0,walkOffset:0,walkDepth:D.furious?72:58,walkDuration:D.furious?3.15:3.45,reacts:0,walkSeenUp:false,walkSeenBack:false};",
'walk state');
one(
`function stage4CoreEnrageTick(b,dt,phase){`,
`function stage4CoreEnrageReact(b,node){
  const S=b&&b._s4war,R=S&&S.coreEnrage;if(!R||!R.active||R.mode==='retreat')return false;
  R.reacts++;if(!R.walkActive){R.walkActive=true;R.walkT=0;R.walkOffset=0;R.walkSeenUp=false;R.walkSeenBack=false;
    stage4WarfareSound('bossShieldStatic','enemyElectricBolt');}
  return true;
}
function stage4CoreEnrageWalkTick(R,dt){
  if(!R||!R.walkActive)return 0;R.walkT+=dt;const q=clamp(R.walkT/Math.max(.1,R.walkDuration),0,1),turn=.52;
  if(q<=turn){const u=q/turn,e=u*u*(3-2*u);R.walkOffset=-R.walkDepth*e;if(u>.20)R.walkSeenUp=true;}
  else{const u=(q-turn)/(1-turn),e=u*u*(3-2*u);R.walkOffset=-R.walkDepth*(1-e);if(u>.20)R.walkSeenBack=true;}
  if(q>=1){R.walkActive=false;R.walkOffset=0;}return R.walkOffset;
}
function stage4CoreEnrageTick(b,dt,phase){`,
'walk helpers');
one(
"  R.mode=R.t<travel?'deploy':(R.t<retreatAt?'fire':'retreat');\n  const left=camLeftX(),right=camRightX(),sideY=clamp((S.homeY||150)+205,292,VH-230),target=typeof targetShip==='function'?targetShip((left+right)*.5,sideY):player;",
"  R.mode=R.t<travel?'deploy':(R.t<retreatAt?'fire':'retreat');\n  const left=camLeftX(),right=camRightX(),baseSideY=clamp((S.homeY||150)+205,292,VH-230),\n        sideY=baseSideY+stage4CoreEnrageWalkTick(R,dt),target=typeof targetShip==='function'?targetShip((left+right)*.5,sideY):player;",
'walk movement');
one(
"    if(!n._coreRageTriggered&&stage4CoreEnrageStart(b,n))n._coreRageTriggered=true;\n    if(_dmgBullet&&(_dmgBullet.kind==='beam'||_dmgBullet._stage4WideBeam))n.hp-=Math.max(1,dmg||1);",
"    if(!n._coreRageTriggered){\n      if(stage4CoreEnrageStart(b,n))n._coreRageTriggered=true;\n      else if(b._s4war.coreEnrage&&b._s4war.coreEnrage.active){n._coreRageTriggered=true;stage4CoreEnrageReact(b,n);}\n    }else stage4CoreEnrageReact(b,n);\n    if(_dmgBullet&&(_dmgBullet.kind==='beam'||_dmgBullet._stage4WideBeam))n.hp-=Math.max(1,dmg||1);",
'generator reaction');
if(s.includes('\r\n'))throw new Error('game.js line endings changed');fs.writeFileSync(file,s,'utf8');console.log('PATCHED_SOVEREIGN_HELPER_SPIDER_WALK_0915');
