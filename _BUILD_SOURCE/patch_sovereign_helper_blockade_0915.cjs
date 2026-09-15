const fs=require('fs');
const path=require('path');
const file=path.resolve(__dirname,'..','assets','game.js');
let s=fs.readFileSync(file,'utf8');
function one(oldText,newText,label){
  const first=s.indexOf(oldText),last=s.lastIndexOf(oldText);
  if(first<0||first!==last)throw new Error(label+' match count is not one');
  s=s.slice(0,first)+newText+s.slice(first+oldText.length);
}

one(
"    coreSpreadShots:0,coreSpreadLast:null,miniHard:null,miniRamCount:0,miniHardLog:[]};",
"    coreSpreadShots:0,coreSpreadLast:null,coreFormationT:0,coreFormationMix:0,\n"+
"    coreFormationMode:'home',coreFormationAnchor:null,coreFormationSeen:{advance:false,hold:false,retreat:false},\n"+
"    miniHard:null,miniRamCount:0,miniHardLog:[]};",
'formation state');

one(
"const S4H_SCALE=.40, S4H_SIZE=132*S4H_SCALE, S4H_HALF=S4H_SIZE/2;\n"+
"function stage4CoreTurretTarget(b,side){const p=stage4GeneratorColumn(b,side);return {x:p.x,y:clamp(p.y-123,80,108)};}",
`const S4H_SCALE=.40, S4H_SIZE=132*S4H_SCALE, S4H_HALF=S4H_SIZE/2;
function stage4CoreDifficulty(){
  const key=typeof diffKey==='undefined'?'normal':diffKey,furious=key==='furious',hard=furious||key==='hard';
  return {hard:hard,furious:furious,shieldMul:hard?1.5:1,windup:furious?.94:(hard?1.08:1.35),
    straightBeat:furious?.022:(hard?.026:null),diagBeat:furious?.037:(hard?.043:.055),
    diagGap:furious?.21:(hard?.25:.32),shotSpeed:furious?8.05:(hard?7.62:7.10),
    aimGain:furious?9.5:(hard?8:6),hold:furious?3.0:2.55};
}
function stage4CoreFormationTick(b,dt){
  const S=b&&b._s4war,D=stage4CoreDifficulty();if(!S||!S.coreUnlocked)return;
  const live=S.coreTurrets.filter(t=>!t.dead&&t.materialize>=.92);
  if(!D.hard||live.length<2){S.coreFormationMode='home';S.coreFormationMix=0;S.coreFormationT=0;return;}
  S.coreFormationT=(S.coreFormationT||0)+dt;
  const home=2.20,travel=.72,hold=D.hold,cycle=home+travel+hold+travel+1.45,u=S.coreFormationT%cycle;
  let mode='home',mix=0;
  if(u>=home&&u<home+travel){mode='advance';const q=(u-home)/travel;mix=q*q*(3-2*q);}
  else if(u<home+travel+hold){mode='hold';mix=1;}
  else if(u<home+travel+hold+travel){mode='retreat';const q=(u-home-travel-hold)/travel;mix=1-q*q*(3-2*q);}
  S.coreFormationMode=mode;S.coreFormationMix=mix;
  if(S.coreFormationSeen&&mode!=='home')S.coreFormationSeen[mode]=true;
  const left=camLeftX(),right=camRightX(),mid=(left+right)*.5,target=typeof targetShip==='function'?targetShip(mid,315):player;
  const desired=clamp(target&&target.x!=null?target.x:mid,left+105,right-105);
  if(S.coreFormationAnchor==null)S.coreFormationAnchor=desired;
  S.coreFormationAnchor+=(desired-S.coreFormationAnchor)*Math.min(1,dt*(D.furious?6.8:5.8));
}
function stage4CoreTurretTarget(b,side){
  const S=b._s4war,p=stage4GeneratorColumn(b,side),home={x:p.x,y:clamp(p.y-123,80,108)},mix=S.coreFormationMix||0;
  if(mix<=0)return home;
  const left=camLeftX(),right=camRightX(),anchor=clamp(S.coreFormationAnchor==null?(left+right)*.5:S.coreFormationAnchor,left+105,right-105),
        row={x:anchor+side*58,y:clamp((S.homeY||150)+176,286,350)};
  return {x:lerp(home.x,row.x,mix),y:lerp(home.y,row.y,mix)};
}`,
'difficulty and formation helpers');

one(
"  const S=b&&b._s4war;if(!S||S.mini)return 0;S.coreUnlocked=true;S.coreGeneration++;\n  let spawned=0;",
"  const S=b&&b._s4war;if(!S||S.mini)return 0;S.coreUnlocked=true;S.coreGeneration++;\n  const D=stage4CoreDifficulty();\n  let spawned=0;",
'spawn difficulty');
one(
"    const p=stage4CoreTurretTarget(b,side),hp=170+S.coreGeneration*20,shield=90+S.coreGeneration*12,",
"    const p=stage4CoreTurretTarget(b,side),hp=170+S.coreGeneration*20,shield=Math.ceil((90+S.coreGeneration*12)*D.shieldMul),",
'shield multiplier');
one(
"  const S=b&&b._s4war;if(!S||!S.coreUnlocked)return;\n  for(const t of S.coreTurrets){",
"  const S=b&&b._s4war;if(!S||!S.coreUnlocked)return;const D=stage4CoreDifficulty();stage4CoreFormationTick(b,dt);\n  for(const t of S.coreTurrets){",
'tick difficulty');
one(
"stage4AngleDelta(t.ang==null?Math.PI/2:t.ang,t.aimTo)*Math.min(1,dt*6);",
"stage4AngleDelta(t.ang==null?Math.PI/2:t.ang,t.aimTo)*Math.min(1,dt*D.aimGain);",
'aim speed');
one("      const q=clamp(t.stateT/1.35,0,1);","      const q=clamp(t.stateT/D.windup,0,1);",'windup progress');
one("      if(t.stateT>=1.35){t.state='fire';","      if(t.stateT>=D.windup){t.state='fire';",'windup release');
one(
"          if(t.burstLeft>1){t.burstLeft--;t.fireShot+=.055;}\n          else{t.burstLeft=4;t.fireShot+=.32;}\n        } else t.fireShot+=(phase>=3?.028:.034);",
"          if(t.burstLeft>1){t.burstLeft--;t.fireShot+=D.diagBeat;}\n          else{t.burstLeft=4;t.fireShot+=D.diagGap;}\n        } else t.fireShot+=D.straightBeat||(phase>=3?.028:.034);",
'shot cadence');
one(
"          b,tip,ang,7.10+phase*.20,'lightningmg',{accel:.22,max:8.70,szMul:1.20});",
"          b,tip,ang,D.shotSpeed+phase*.20,'lightningmg',{accel:D.hard?.30:.22,max:(D.furious?10.1:(D.hard?9.55:8.70)),szMul:1.20});",
'shot velocity');

if(s.includes('\r\n'))throw new Error('game.js line endings changed before write');
fs.writeFileSync(file,s,'utf8');
console.log('PATCHED_SOVEREIGN_HELPER_BLOCKADE_0915');
