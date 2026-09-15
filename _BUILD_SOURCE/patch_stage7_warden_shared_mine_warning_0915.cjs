const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
"  if(mode==='rail'){S.railAim=aimPlayer(b.x,b.y);S.railSafe=player.x<b.x?-1:1;combatWarningTick(b,'stage7-warden-rail',0,.86,true);}\n  if(mode==='teleport'){",
"  if(mode==='rail'){S.railAim=aimPlayer(b.x,b.y);S.railSafe=player.x<b.x?-1:1;combatWarningTick(b,'stage7-warden-rail',0,.86,true);}\n  if(mode==='minefield'){const cols=7;S.mineGap=clamp(Math.floor(player.x/(worldWidth()/cols)),1,cols-2);combatWarningTick(b,'stage7-warden-minefield',0,.72,true);}\n  if(mode==='teleport'){",
'commit minefield gap at charge start');
one(
"  }else if(S.mode==='minefield'){\n    if(!S.event&&S.mt>.72){S.event=1;const C=shipBossMount(b,'C'),cols=7,gap=clamp(Math.floor(player.x/(worldWidth()/cols)),1,cols-2);",
"  }else if(S.mode==='minefield'){\n    const tell=.72;combatWarningTick(b,'stage7-warden-minefield',Math.min(S.mt,tell),tell);\n    if(!S.event&&S.mt>tell){S.event=1;const C=shipBossMount(b,'C'),cols=7,gap=S.mineGap;",
'shared minefield warning tick and committed release');
one(
"function s7WardenRailAngles(S){",
"function s7WardenMineTargets(S){\n  if(!S||!Number.isFinite(S.mineGap))return [];const cols=7,W=worldWidth();\n  return Array.from({length:cols},(_,i)=>i).filter(i=>i!==S.mineGap).map(i=>({x:(i+.5)*W/cols,y:VH*.58,index:i}));\n}\nfunction s7WardenMineWarningDraw(b,front){\n  const S=b&&b._s7warden;if(!S||S.mode!=='minefield'||S.event||S.mt>=.72)return false;\n  const p=shipBossMount(b,'C'),k=clamp(S.mt/.72,0,1),targets=s7WardenMineTargets(S);\n  if(!front)for(const q of targets)combatWarningDraw(b,{x:p.x,y:p.y,ex:q.x,ey:q.y,progress:k,width:22,fieldOnly:true});\n  else combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x,ey:VH,progress:k,alertOnly:true});\n  return true;\n}\nfunction s7WardenRailAngles(S){",
'shared minefield warning helpers');
one("  s7WardenRailWarningDraw(b,false);\n  const baseY=","  s7WardenRailWarningDraw(b,false);s7WardenMineWarningDraw(b,false);\n  const baseY=",'mine fields behind hull');
one("  s7WardenRailWarningDraw(b,true);\n  return true;","  s7WardenRailWarningDraw(b,true);s7WardenMineWarningDraw(b,true);\n  return true;",'mine alert in front of hull');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE7_WARDEN_SHARED_MINE_WARNING_0915');
