const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');
function once(old,replacement,label){const n=s.split(old).length-1;if(n!==1)throw new Error(label+' anchor count '+n);s=s.replace(old,replacement);}
once(
"  if(b._s7Flood){b.fireCd=Math.max(b.fireCd||0,.22);return false;}",
"  if(b._s7Flood){b.fireCd=Math.max(b.fireCd||0,.22);return false;}\n  if(b._s7DredgerMine){b.fireCd=Math.max(b.fireCd||0,.22);return false;}",
'queue guard');
once(
"  if(b._s7Flood)sludgeFloodTick(b,dt);\n  if(b._s7Rosette)sludgeRosetteTick(b,dt);",
"  if(b._s7Flood)sludgeFloodTick(b,dt);\n  if(b._s7Rosette)sludgeRosetteTick(b,dt);\n  if(b._s7DredgerMine)s7DredgerMineTick(b,dt);",
'per-frame tick');
once(
"function s7DredgerAttack(b,step){\n  const ph=shipBossPhase(b),L=shipBossMount(b,'L'),R=shipBossMount(b,'R'),C=shipBossMount(b,'C');\n  b._sbPat=ph>=2?'s7portalmines':(ph?'s7spore':'s7dredge');\n  if(ph>=2&&step%4===0){const cols=6,gap=clamp(Math.floor(player.x/(worldWidth()/cols)),0,cols-1);\n    for(let i=0;i<cols;i++){if(i===gap)continue;const tx=(i+.5)*worldWidth()/cols,a=Math.atan2(VH*.60-C.y,tx-C.x);\n      s7WardenShot(b,'C',a,1.08,'mine',{silent:i>0});}\n    shipBossMuzzleStart(b,['C'],{fam:'nfx_toxicleviathan_mflash',n:6,life:.26,hpx:68});b.fireCd=1.42;\n  }else if(!ph)",
`const S7_DREDGER_MINE_WARN=.86;
function s7DredgerMineTargets(M){
  if(!M||!Number.isFinite(M.gap))return [];
  return Array.from({length:M.cols},(_,i)=>i).filter(i=>i!==M.gap).map(i=>({x:(i+.5)*M.width/M.cols,y:VH*.60,index:i}));
}
function s7DredgerMineStart(b){
  if(!b||b._s7DredgerMine)return false;
  const cols=6,W=worldWidth(),gap=clamp(Math.floor(player.x/(W/cols)),0,cols-1);
  b._s7DredgerMine={t:0,warn:S7_DREDGER_MINE_WARN,cols:cols,gap:gap,width:W,released:false,finish:0};
  b.fireCd=Math.max(b.fireCd||0,S7_DREDGER_MINE_WARN+.58);
  combatWarningTick(b,'stage7-dredger-minefield',0,S7_DREDGER_MINE_WARN,true);
  return true;
}
function s7DredgerMineTick(b,dt){
  const M=b&&b._s7DredgerMine;if(!M)return false;M.t+=dt;
  combatWarningTick(b,'stage7-dredger-minefield',Math.min(M.t,M.warn),M.warn);
  if(!M.released&&M.t>=M.warn){
    M.released=true;M.finish=M.t+.45;const C=shipBossMount(b,'C'),targets=s7DredgerMineTargets(M);
    for(let i=0;i<targets.length;i++){const q=targets[i],a=Math.atan2(q.y-C.y,q.x-C.x);s7WardenShot(b,'C',a,1.08,'mine',{silent:i>0});}
    shipBossMuzzleStart(b,['C'],{fam:'nfx_toxicleviathan_mflash',n:6,life:.26,hpx:68});
    shake=Math.max(shake,6);
  }
  if(M.released&&M.t>=M.finish){b._s7DredgerMine=null;b.fireCd=.56;return false;}
  return true;
}
function s7DredgerMineDraw(b,front){
  const M=b&&b._s7DredgerMine;if(!M||M.released)return false;
  const C=shipBossMount(b,'C'),k=clamp(M.t/M.warn,0,1),targets=s7DredgerMineTargets(M);
  if(!front)for(const q of targets)combatWarningDraw(b,{x:C.x,y:C.y,ex:q.x,ey:q.y,progress:k,width:22,fieldOnly:true});
  else combatWarningDraw(b,{x:C.x,y:C.y,ex:C.x,ey:VH,progress:k,alertOnly:true,alertX:b.x,alertY:52});
  return true;
}
function s7DredgerAttack(b,step){
  const ph=shipBossPhase(b),L=shipBossMount(b,'L'),R=shipBossMount(b,'R'),C=shipBossMount(b,'C');
  b._sbPat=ph&&step%4===0?'s7portalmines':(ph?'s7spore':'s7dredge');
  if(b._s7DredgerMine){b.fireCd=.24;return;}
  if(ph&&step%4===0){s7DredgerMineStart(b);return;
  }else if(!ph)`,
'Dredger mine controller');
once(
"  if(typeof XART==='undefined' || !XART.rdy(D.key)){\n    /* ⚠ NEVER FALL THROUGH TO NOTHING.",
"  if(typeof XART==='undefined' || !XART.rdy(D.key)){\n    if(b._s7DredgerMine)s7DredgerMineDraw(b,false);\n    /* ⚠ NEVER FALL THROUGH TO NOTHING.",
'fallback under warning');
once(
"    shipBossMuzzleDraw(b);\n    if(b._s9Cascade)tidalCascadeDraw(b,true);",
"    shipBossMuzzleDraw(b);\n    if(b._s7DredgerMine)s7DredgerMineDraw(b,true);\n    if(b._s9Cascade)tidalCascadeDraw(b,true);",
'fallback front warning');
once(
"  if(b._s7Flood)sludgeFloodDraw(b);\n  if(b._s7Rosette)sludgeRosetteDraw(b);\n  if(b._s9Cascade)tidalCascadeDraw(b,false);",
"  if(b._s7Flood)sludgeFloodDraw(b);\n  if(b._s7Rosette)sludgeRosetteDraw(b);\n  if(b._s7DredgerMine)s7DredgerMineDraw(b,false);\n  if(b._s9Cascade)tidalCascadeDraw(b,false);",
'normal under warning');
once(
"  shipBossMuzzleDraw(b);\n  if(b._s9Cascade)tidalCascadeDraw(b,true);\n  return true;",
"  shipBossMuzzleDraw(b);\n  if(b._s7DredgerMine)s7DredgerMineDraw(b,true);\n  if(b._s9Cascade)tidalCascadeDraw(b,true);\n  return true;",
'normal front warning');
if(s.includes('\r'))throw new Error('assets/game.js line endings changed');fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE7_DREDGER_MINE_WARNING_0916');
