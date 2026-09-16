const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
function once(a,b,n){const i=s.indexOf(a);if(i<0)throw new Error(n+' anchor missing');if(s.indexOf(a,i+a.length)>=0)throw new Error(n+' anchor repeated');s=s.slice(0,i)+b+s.slice(i+a.length);}
once(`function hammerBallLaunchPath(b){
  const h=b&&b._hammer,rad=54,dir=h&&h.ballDir<0?-1:1,vx=150*dir,vy=165,l=camLeftX()+rad,r=camRightX()-rad,bt=PLAY.y+PLAY.h-rad;
  const sideT=(dir<0?(l-b.x)/vx:(r-b.x)/vx),bottomT=(bt-b.y)/vy,t=Math.max(0,Math.min(sideT>0?sideT:Infinity,bottomT>0?bottomT:Infinity));
  return{x:b.x,y:b.y,ex:b.x+vx*t,ey:b.y+vy*t,dir:dir};
}
function hammerBallArm(b){
  const h=b._hammer;h.ballDir=Math.random()<.5?-1:1;h.ballWarn=true;combatWarningTick(b,'archmage-spiked-ball',0,HAMMER_BALL_WARN,true);
  if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();
}` ,`function hammerBallRay(b,dir){
  const rad=54,vx=150*dir,vy=165,l=camLeftX()+rad,r=camRightX()-rad,bt=PLAY.y+PLAY.h-rad;
  const sideT=(dir<0?(l-b.x)/vx:(r-b.x)/vx),bottomT=(bt-b.y)/vy,t=Math.max(0,Math.min(sideT>0?sideT:Infinity,bottomT>0?bottomT:Infinity));
  return{x:b.x,y:b.y,ex:b.x+vx*t,ey:b.y+vy*t,dir:dir,bounds:{l:l,r:r,bt:bt}};
}
function hammerBallLaunchPath(b){
  const h=b&&b._hammer,p=h&&h.ballPath?h.ballPath:hammerBallRay(b,h&&h.ballDir<0?-1:1);return{x:p.x,y:p.y,ex:p.ex,ey:p.ey,dir:p.dir};
}
function hammerBallArm(b){
  const h=b._hammer;h.ballDir=Math.random()<.5?-1:1;const p=hammerBallRay(b,h.ballDir);h.ballPath={x:p.x,y:p.y,ex:p.ex,ey:p.ey,dir:p.dir};h.ballBounds=p.bounds;h.ballWarn=true;
  combatWarningTick(b,'archmage-spiked-ball',0,HAMMER_BALL_WARN,true);if(Audio.SFX&&(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle))(Audio.SFX.bossWeaponCharge||Audio.SFX.crackle)();
}`,'committed ray');
once("  else if(h.state==='curl'){combatWarningTick(b,'archmage-spiked-ball',Math.min(h.t,HAMMER_BALL_WARN),HAMMER_BALL_WARN);if(h.t>HAMMER_BALL_WARN){h.rage=0;h.vx=150*(h.ballDir<0?-1:1);h.vy=165;h.shotCd=.7;hammerState(b,'ball');}}\n  else if(h.state==='ball'){const sp=h.rage>0?2.25:1,rad=54;b.x+=h.vx*dt*sp;b.y+=h.vy*dt*sp;h.angle+=dt*(h.rage>0?16:8);const l=camLeftX()+rad,r=camRightX()-rad,t=PLAY.y+rad,bt=PLAY.y+PLAY.h-rad;if(b.x<l){b.x=l;h.vx=Math.abs(h.vx);}if(b.x>r){b.x=r;h.vx=-Math.abs(h.vx);}if(b.y<t){b.y=t;h.vy=Math.abs(h.vy);}if(b.y>bt){b.y=bt;h.vy=-Math.abs(h.vy);}if(h.rage>0&&h.shotCd<=0){h.shotCd=.62;for(let i=0;i<8;i++)hammerEnergyBomb(b.x,b.y,TAU*i/8,4.5);}if(h.t>=15)hammerState(b,'uncurl');}",`  else if(h.state==='curl'){combatWarningTick(b,'archmage-spiked-ball',Math.min(h.t,HAMMER_BALL_WARN),HAMMER_BALL_WARN);if(h.t>HAMMER_BALL_WARN){h.rage=0;h.vx=150*(h.ballDir<0?-1:1);h.vy=165;h.shotCd=.7;h.ballFirst=true;hammerState(b,'ball');}}
  else if(h.state==='ball'){
    const sp=h.rage>0?2.25:1,rad=54;b.x+=h.vx*dt*sp;b.y+=h.vy*dt*sp;h.angle+=dt*(h.rage>0?16:8);
    const fixed=h.ballFirst&&h.ballBounds,l=fixed?fixed.l:camLeftX()+rad,r=fixed?fixed.r:camRightX()-rad,t=PLAY.y+rad,bt=fixed?fixed.bt:PLAY.y+PLAY.h-rad;let bounced=false;
    if(b.x<l){b.x=l;h.vx=Math.abs(h.vx);bounced=true;}if(b.x>r){b.x=r;h.vx=-Math.abs(h.vx);bounced=true;}if(b.y<t){b.y=t;h.vy=Math.abs(h.vy);bounced=true;}if(b.y>bt){b.y=bt;h.vy=-Math.abs(h.vy);bounced=true;}if(bounced)h.ballFirst=false;
    if(h.rage>0&&h.shotCd<=0){h.shotCd=.62;for(let i=0;i<8;i++)hammerEnergyBomb(b.x,b.y,TAU*i/8,4.5);}if(h.t>=15)hammerState(b,'uncurl');
  }`,'committed first bounce');
if(/\r/.test(s))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s,'utf8');console.log('PATCHED_ARCHMAGE_SPIKED_BALL_COMMIT_0916');
