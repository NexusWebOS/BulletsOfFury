const fs=require('fs'),path=require('path'),file=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(file,'utf8');
function one(a,b,label){const i=s.indexOf(a);if(i<0||i!==s.lastIndexOf(a))throw new Error(label+' match count is not one');s=s.slice(0,i)+b+s.slice(i+a.length);}
one(
"    coreEnrage:null,coreEnrageCount:0,coreEnrageShots:0,coreEnrageGapWindows:0,\n    miniHard:null,miniRamCount:0,miniHardLog:[]};",
"    coreEnrage:null,coreEnrageCount:0,coreEnrageShots:0,coreEnrageGapWindows:0,\n"+
"    chainBolts:0,chainOrbs:0,chainLastAngles:[],chainCycles:0,\n"+
"    miniHard:null,miniRamCount:0,miniHardLog:[]};",
'chain state');
one(
`function stage4WarfareMiniTick(b,dt){return stage4MiniDirector(b,dt);}`,
`function stage4SovereignChainProfile(){
  const key=typeof diffKey==='undefined'?'normal':diffKey,furious=key==='furious',hard=furious||key==='hard';
  return furious?{hard:true,furious:true,beats:[.82,1.18,1.62],end:3.34,orbTimes:[2.02,2.40,2.78],speed:1.14,
      outer:[-.46,-.22,.22,.46],inner:[.10,.38,-.38,-.10]}:
    hard?{hard:true,furious:false,beats:[1.12,1.68,2.28],end:4.12,orbTimes:[2.92],speed:1.06,
      outer:[-.38,-.18,.18,.38],inner:[.10,.32,-.32,-.10]}:
      {hard:false,furious:false,beats:[1.12,1.68,2.28],end:4.12,orbTimes:[2.92],speed:1,
      outer:[-.24,.24],inner:[.18,-.18]};
}
function stage4SovereignChainVolley(b,P,inner){
  const S=b._s4war,angles=inner?P.inner:P.outer,shots=[];
  for(let i=0;i<angles.length;i++){
    const slot=i<angles.length/2?'EL':'ER',ang=Math.PI/2+angles[i],q=stage4WarfareShot(b,slot,ang,(inner?5.45:5.15)*P.speed,'lightning',
      {accel:(inner?1.2:1.1)*P.speed,max:(inner?7.5:7.2)*P.speed,szMul:P.furious?1.78:(P.hard?1.66:(inner?1.58:1.52))});
    q._s4ChainBolt=true;q._s4ChainGroup=inner?1:0;q._s4ChainAngle=angles[i];shots.push(q);stage4WarfareMuzzle(b,slot,'lightning',1.12,.24);
  }
  S.chainBolts+=shots.length;S.chainLastAngles=angles.slice();return shots;
}
function stage4SovereignChainOrb(b,P,index){
  const S=b._s4war,multi=P.orbTimes.length>1,slot=multi?(index&1?'ORB_R':'ORB_L'):'C',side=multi?(index&1?1:-1):0,
        q=stage4WarfareShot(b,slot,Math.PI/2,multi?1.58:1.38,'orb',{lift:multi?.25:.30,launchSpeed:multi?2.7:2.45,
          launchAccel:multi?2.18:2.0,max:multi?7.45:7.0,side:side,shootable:true,hp:P.furious?3:4,szMul:P.furious?.86:.92});
  q._s4ChainOrb=true;q._s4ChainOrbIndex=index;S.chainOrbs++;stage4WarfareMuzzle(b,slot,'orb',1.48,.28);
  stage4WarfareSound('enemyElectricBolt','enemyBossCannon');return q;
}
function stage4WarfareMiniTick(b,dt){return stage4MiniDirector(b,dt);}`,
'chain helpers');
const old=`  }else{
    b.x+=(mid-b.x)*Math.min(1,dt*5.8);b.y+=(sy-b.y)*Math.min(1,dt*5.8);
    if(S.event===0&&S.t>=1.12){
      for(const e of [['EL',-.24],['ER',.24]]){stage4WarfareShot(b,e[0],Math.PI/2+e[1],5.15,'lightning',{accel:1.1,max:7.2,szMul:1.52});stage4WarfareMuzzle(b,e[0],'lightning',1.12,.24);}
      stage4WarfareSound('enemyHeavyLaser','enemyElectricBolt');shake=Math.max(shake,6);S.event=1;
    }
    if(S.event===1&&S.t>=1.68){
      for(const e of [['EL',.18],['ER',-.18]]){stage4WarfareShot(b,e[0],Math.PI/2+e[1],5.45,'lightning',{accel:1.2,max:7.5,szMul:1.58});stage4WarfareMuzzle(b,e[0],'lightning',1.12,.24);}
      stage4WarfareSound('enemyElectricBolt','enemyBossCannon');S.event=2;
    }
    if(S.event===2&&S.t>=2.28){
      stage4WarfareShot(b,'C',Math.PI/2,4.10,'lightning',{w:23,h:54,accel:1.55,max:8.0,szMul:2.05});
      stage4WarfareMuzzle(b,'C','lightning',1.55,.30);stage4WarfareSound('enemyHeavyLaser','laserCannon');shake=Math.max(shake,10);S.event=3;
    }
    if(S.event===3&&S.t>=2.92){
      stage4WarfareShot(b,'C',Math.PI/2,1.38,'orb',{lift:.30,launchSpeed:2.45,launchAccel:2.0,max:7.0,shootable:true,hp:4,szMul:.92});
      stage4WarfareMuzzle(b,'C','orb',1.48,.28);stage4WarfareSound('enemyElectricBolt','enemyBossCannon');S.event=4;
    }
    if(S.t>=4.12)stage4WarfareSetMode(b,'burst');
  }`;
const neu=`  }else{
    b.x+=(mid-b.x)*Math.min(1,dt*5.8);b.y+=(sy-b.y)*Math.min(1,dt*5.8);const P=stage4SovereignChainProfile();
    if(S.event===0&&S.t>=P.beats[0]){stage4SovereignChainVolley(b,P,false);stage4WarfareSound('enemyHeavyLaser','enemyElectricBolt');shake=Math.max(shake,P.hard?8:6);S.event=1;S.chainCycles++;}
    if(S.event===1&&S.t>=P.beats[1]){stage4SovereignChainVolley(b,P,true);stage4WarfareSound('enemyElectricBolt','enemyBossCannon');S.event=2;}
    if(S.event===2&&S.t>=P.beats[2]){
      const q=stage4WarfareShot(b,'C',Math.PI/2,4.10*P.speed,'lightning',{w:P.hard?27:23,h:P.hard?62:54,accel:1.55*P.speed,max:8.0*P.speed,szMul:P.furious?2.28:(P.hard?2.16:2.05)});
      q._s4ChainBolt=true;q._s4ChainGroup=2;q._s4ChainAngle=0;S.chainBolts++;stage4WarfareMuzzle(b,'C','lightning',1.55,.30);stage4WarfareSound('enemyHeavyLaser','laserCannon');shake=Math.max(shake,P.hard?12:10);S.event=3;
    }
    const oi=S.event-3;if(oi>=0&&oi<P.orbTimes.length&&S.t>=P.orbTimes[oi]){stage4SovereignChainOrb(b,P,oi);S.event++;}
    if(S.t>=P.end)stage4WarfareSetMode(b,'burst');
  }`;
one(old,neu,'lightning director');
if(s.includes('\r\n'))throw new Error('game.js line endings changed');fs.writeFileSync(file,s,'utf8');console.log('PATCHED_SOVEREIGN_CHAIN_LIGHTNING_0915');
