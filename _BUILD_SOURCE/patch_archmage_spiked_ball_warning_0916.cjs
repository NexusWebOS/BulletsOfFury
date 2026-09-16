const fs=require('fs'),path=require('path');
const gamePath=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(gamePath);
function lastOnce(old,replacement,label){const a=Buffer.from(old,'utf8'),b=Buffer.from(replacement,'utf8'),at=s.lastIndexOf(a);if(at<0)throw new Error(label+' anchor missing');s=Buffer.concat([s.subarray(0,at),b,s.subarray(at+a.length)]);}
lastOnce("function hammerState(b,state){const h=b._hammer;h.state=state;h.t=0;h.ox=b.x;h.oy=b.y;}","function hammerState(b,state){const h=b._hammer;if(h.state==='curl'&&state!=='curl'&&h.ballWarn){combatWarningTick(b,'archmage-spiked-ball',HAMMER_BALL_WARN,HAMMER_BALL_WARN,true);h.ballWarn=false;}h.state=state;h.t=0;h.ox=b.x;h.oy=b.y;}",'active hammer state cleanup');
lastOnce("function hammerHard(){return diffKey==='hard'||diffKey==='furious';}\nfunction hammerFurious(){return diffKey==='furious';}\nfunction hammerGripPoint(b){return{x:b.x-48,y:b.y-10};}",`function hammerHard(){return diffKey==='hard'||diffKey==='furious';}
function hammerFurious(){return diffKey==='furious';}
const HAMMER_BALL_WARN=1.25;
function hammerBallLaunchPath(b){
  const h=b&&b._hammer,rad=54,dir=h&&h.ballDir<0?-1:1,vx=150*dir,vy=165,l=camLeftX()+rad,r=camRightX()-rad,bt=PLAY.y+PLAY.h-rad;
  const sideT=(dir<0?(l-b.x)/vx:(r-b.x)/vx),bottomT=(bt-b.y)/vy,t=Math.max(0,Math.min(sideT>0?sideT:Infinity,bottomT>0?bottomT:Infinity));
  return{x:b.x,y:b.y,ex:b.x+vx*t,ey:b.y+vy*t,dir:dir};
}
function hammerBallArm(b){
  const h=b._hammer;h.ballDir=Math.random()<.5?-1:1;h.ballWarn=true;combatWarningTick(b,'archmage-spiked-ball',0,HAMMER_BALL_WARN,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();
}
function hammerGripPoint(b){return{x:b.x-48,y:b.y-10};}`,'spiked-ball warning helpers');
lastOnce("  else if(h.state==='shield'){if(h.t>1.0)hammerState(b,'curl');}\n  else if(h.state==='curl'){if(h.t>1.25){h.rage=0;h.vx=150*(Math.random()<.5?-1:1);h.vy=165;h.shotCd=.7;hammerState(b,'ball');}}",`  else if(h.state==='shield'){if(h.t>1.0){hammerBallArm(b);hammerState(b,'curl');}}
  else if(h.state==='curl'){combatWarningTick(b,'archmage-spiked-ball',Math.min(h.t,HAMMER_BALL_WARN),HAMMER_BALL_WARN);if(h.t>HAMMER_BALL_WARN){h.rage=0;h.vx=150*(h.ballDir<0?-1:1);h.vy=165;h.shotCd=.7;hammerState(b,'ball');}}`,'spiked-ball launch flow');
lastOnce("function hammerBossDraw(b){\n  const h=b._hammer;hammerBossAtmosphereDraw(b);",`function hammerBossDraw(b){
  const h=b._hammer;hammerBossAtmosphereDraw(b);
  if(h.state==='curl'&&h.ballWarn){const p=hammerBallLaunchPath(b),k=clamp(h.t/HAMMER_BALL_WARN,0,1);combatWarningDraw(b,{x:p.x,y:p.y,ex:p.ex,ey:p.ey,progress:k,width:112,alertX:b.x-p.dir*86,alertY:b.y-76});}`,'spiked-ball warning draw');
if(s.includes(13))throw new Error('assets/game.js line endings changed');fs.writeFileSync(gamePath,s);console.log('PATCHED_ARCHMAGE_SPIKED_BALL_WARNING_0916');
