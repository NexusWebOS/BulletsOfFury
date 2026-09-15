const fs=require('fs'),path=require('path');
const file=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(file,'utf8');
function one(a,b,label){const i=s.indexOf(a);if(i<0||i!==s.lastIndexOf(a))throw new Error(label+' match count is not one');s=s.slice(0,i)+b+s.slice(i+a.length);}

one(
"    coreFormationMode:'home',coreFormationAnchor:null,coreFormationSeen:{advance:false,hold:false,retreat:false},\n    miniHard:null,miniRamCount:0,miniHardLog:[]};",
"    coreFormationMode:'home',coreFormationAnchor:null,coreFormationSeen:{advance:false,hold:false,retreat:false},\n"+
"    coreEnrage:null,coreEnrageCount:0,coreEnrageShots:0,coreEnrageGapWindows:0,\n"+
"    miniHard:null,miniRamCount:0,miniHardLog:[]};",
'enrage state');

one(
`function stage4CoreTurretSpawnMissing(b,threshold){`,
`function stage4CoreEnrageEnd(b){
  const S=b&&b._s4war;if(!S||!S.coreEnrage)return;
  for(const t of S.coreTurrets){
    t.rage=false;t.rageShot=0;t.rageBurst=0;t.state='windup';t.stateT=0;t.windupSfx=false;
    t.heat=0;t.vulnerable=false;t.aimTo=Math.PI/2;
  }
  S.coreEnrage.active=false;S.coreEnrage=null;S.coreFormationT=0;S.coreFormationMix=0;S.coreFormationMode='home';
}
function stage4CoreEnrageStart(b,node){
  const S=b&&b._s4war,D=stage4CoreDifficulty();if(!S||!S.coreUnlocked||!D.hard||S.coreEnrage&&S.coreEnrage.active)return false;
  const live=S.coreTurrets.filter(t=>!t.dead&&t.materialize>=.92);if(!live.length)return false;
  const duration=D.furious?6.8:5.6;
  S.coreEnrage={active:true,t:0,dur:duration,mode:'deploy',sourceSide:node&&node.side||0,shots:0,leftShots:0,rightShots:0,gaps:0};
  S.coreEnrageCount++;
  for(const t of live){t.rage=true;t.rageFrom={x:t.x,y:t.y};t.rageShot=t.side>0?.16:0;t.rageBurst=0;t.state='rage';t.heat=.78;t.vulnerable=false;}
  stage4WarfareSound('bossPhase','enemyLightningChaingun');shake=Math.max(shake,8);return true;
}
function stage4CoreEnrageTick(b,dt,phase){
  const S=b&&b._s4war,R=S&&S.coreEnrage;if(!R||!R.active)return false;
  const D=stage4CoreDifficulty(),live=S.coreTurrets.filter(t=>!t.dead&&t.materialize>=.92);
  if(!live.length){stage4CoreEnrageEnd(b);return false;}
  R.t+=dt;const travel=.62,retreatAt=R.dur-travel;
  R.mode=R.t<travel?'deploy':(R.t<retreatAt?'fire':'retreat');
  const left=camLeftX(),right=camRightX(),sideY=clamp((S.homeY||150)+205,292,VH-230),target=typeof targetShip==='function'?targetShip((left+right)*.5,sideY):player;
  for(const t of live){
    t.flash=Math.max(0,(t.flash||0)-dt);t.deflectFlash=Math.max(0,(t.deflectFlash||0)-dt);t.deflectSfx=Math.max(0,(t.deflectSfx||0)-dt);
    const sideTarget={x:t.side<0?left+48:right-48,y:sideY},home=stage4GeneratorColumn(b,t.side),homeTarget={x:home.x,y:clamp(home.y-123,80,108)};
    let p=sideTarget;
    if(R.mode==='deploy'){const q=clamp(R.t/travel,0,1),e=q*q*(3-2*q),from=t.rageFrom||homeTarget;p={x:lerp(from.x,sideTarget.x,e),y:lerp(from.y,sideTarget.y,e)};}
    else if(R.mode==='retreat'){const q=clamp((R.t-retreatAt)/travel,0,1),e=q*q*(3-2*q);p={x:lerp(sideTarget.x,homeTarget.x,e),y:lerp(sideTarget.y,homeTarget.y,e)};}
    t.x+=(p.x-t.x)*Math.min(1,dt*14);t.y+=(p.y-t.y)*Math.min(1,dt*14);
    const laneY=(target&&target.y!=null?target.y:VH*.72)+t.side*38,laneX=target&&target.x!=null?target.x:(left+right)*.5,
          want=Math.atan2(laneY-t.y,laneX-t.x);
    t.aimTo=want;t.ang=(t.ang==null?Math.PI/2:t.ang)+stage4AngleDelta(t.ang==null?Math.PI/2:t.ang,want)*Math.min(1,dt*12);
    t.reelSpeed=R.mode==='fire'?52:30;t.spin=(t.spin+dt*t.reelSpeed)%8;t.heat=.78+.18*Math.sin(R.t*18+t.side);
    if(R.mode!=='fire')continue;
    t.rageShot-=dt;
    while(t.rageShot<=0){
      if(t.rageBurst>=6){t.rageBurst=0;t.rageShot+=D.furious?.25:.31;R.gaps++;S.coreEnrageGapWindows++;continue;}
      const barrel=t.barrelNext||-1;t.barrelNext=-barrel;const tip=stage4CoreTurretTip(t,barrel),ang=t.ang,
            shot=stage4WarfareShot(b,tip,ang,D.shotSpeed+(D.furious?1.15:.82)+phase*.18,'lightningmg',{accel:.34,max:D.furious?10.8:10.15,szMul:1.20});
      shot._s4CoreSide=t.side;shot._s4CoreRage=true;shot._s4RageLane=t.side;stage4CoreTurretMuzzle(b,t,barrel);
      t.rageBurst++;t.rageShot+=D.furious?.052:.061;R.shots++;S.coreEnrageShots++;if(t.side<0)R.leftShots++;else R.rightShots++;
      if((R.shots%12)===1)stage4WarfareSound('enemyLightningChaingun','enemyMachineGunHeavy');
    }
  }
  if(R.t>=R.dur){stage4CoreEnrageEnd(b);return false;}return true;
}
function stage4CoreTurretSpawnMissing(b,threshold){`,
'enrage director');

one(
"  const S=b&&b._s4war;if(!S||!S.coreUnlocked)return;const D=stage4CoreDifficulty();stage4CoreFormationTick(b,dt);",
"  const S=b&&b._s4war;if(!S||!S.coreUnlocked)return;const D=stage4CoreDifficulty();if(stage4CoreEnrageTick(b,dt,phase))return;stage4CoreFormationTick(b,dt);",
'enrage tick route');

one(
"  stage4ShieldTick(b,dt);\n  stage4FinalChaingunTick(b,dt,phase);\n  stage4CoreTurretTick(b,dt,phase);\n  /* Helper chainguns replace the carrier spread once unlocked; do not layer both attacks. */",
"  stage4ShieldTick(b,dt);\n  const coreRageActive=!!(S.coreEnrage&&S.coreEnrage.active);\n  if(!coreRageActive)stage4FinalChaingunTick(b,dt,phase);\n  stage4CoreTurretTick(b,dt,phase);\n  if(coreRageActive){\n    const rageMid=(camLeftX()+camRightX())*.5;b.x+=(rageMid-b.x)*Math.min(1,dt*6);b.y+=(S.homeY-b.y)*Math.min(1,dt*6);\n    S.poseRot=0;S.scale=1;b._animKey='s4w_boss_energized_'+(Math.floor((b.t||0)*11)%12);return true;\n  }\n  /* Helper chainguns replace the carrier spread once unlocked; do not layer both attacks. */",
'dedicated rage phase');

one(
"    const n=H.nodes[i];n.dead=false;n.hp=n.maxhp=hp;n.flash=0;n.materialize=0;",
"    const n=H.nodes[i];n.dead=false;n.hp=n.maxhp=hp;n.flash=0;n.materialize=0;n._coreRageTriggered=false;",
'node reset');

one(
"    if(_dmgBullet&&(_dmgBullet.kind==='beam'||_dmgBullet._stage4WideBeam))n.hp-=Math.max(1,dmg||1);",
"    if(!n._coreRageTriggered&&stage4CoreEnrageStart(b,n))n._coreRageTriggered=true;\n    if(_dmgBullet&&(_dmgBullet.kind==='beam'||_dmgBullet._stage4WideBeam))n.hp-=Math.max(1,dmg||1);",
'generator trigger');

one(
"    if(XART.rdy(dual))ctx.drawImage(XART.get(dual),-S4H_HALF,-S4H_HALF,S4H_SIZE,S4H_SIZE);",
"    const ragePlate=t.rage&&typeof xartEnraged==='function'?xartEnraged(dual):null;\n    if(ragePlate)ctx.drawImage(ragePlate,-S4H_HALF,-S4H_HALF,S4H_SIZE,S4H_SIZE);\n    else if(XART.rdy(dual))ctx.drawImage(XART.get(dual),-S4H_HALF,-S4H_HALF,S4H_SIZE,S4H_SIZE);",
'red palette draw');

one(
"    ctx.restore();\n    if(alpha>=.92){",
"    ctx.restore();\n    if(t.rage){\n      ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='bold 25px \"BOFmil\", monospace';\n      ctx.shadowColor='#ff321f';ctx.shadowBlur=12;ctx.lineWidth=4;ctx.strokeStyle='#250006';ctx.fillStyle='#ff5444';\n      ctx.strokeText('*',t.x,t.y-S4H_HALF-16);ctx.fillText('*',t.x,t.y-S4H_HALF-16);ctx.restore();\n    }\n    if(alpha>=.92){",
'asterisk draw');

if(s.includes('\r\n'))throw new Error('game.js line endings changed');
fs.writeFileSync(file,s,'utf8');console.log('PATCHED_SOVEREIGN_HELPER_ENRAGE_0915');
