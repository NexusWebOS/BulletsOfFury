const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
"function s7WardenMode(b,mode){\n  const S=b._s7warden;S.mode=mode;S.mt=0;S.shot=0;S.event=0;S.noHit=false;S.step++;\n  if(mode==='burst')S.aim=aimPlayer(b.x,b.y+b.h*.22);",
"function s7WardenBurstArm(b){\n  const S=b._s7warden;S.aim=aimPlayer(b.x,b.y+b.h*.22);combatWarningTick(b,'stage7-warden-burst',0,.48,true);\n}\nfunction s7WardenMode(b,mode){\n  const S=b._s7warden;S.mode=mode;S.mt=0;S.shot=0;S.event=0;S.noHit=false;S.step++;\n  if(mode==='burst')s7WardenBurstArm(b);",
'arm burst aim and warning together');
one("if(F.t>=1.34){b._s7FinalNoBar=false;S.mode='burst';S.mt=0;S.noHit=false;s7WardenPhase(b,'fight');}","if(F.t>=1.34){b._s7FinalNoBar=false;S.mode='burst';S.mt=0;S.noHit=false;s7WardenPhase(b,'fight');s7WardenBurstArm(b);}",'arm opening burst after roar');
one("if(F.t>=3.65){S.mode='burst';s7WardenPhase(b,'fight');}","if(F.t>=3.65){S.mode='burst';s7WardenPhase(b,'fight');s7WardenBurstArm(b);}",'arm post-stun burst');
one(
"    if(!isFinite(S.aim)) S.aim=aimPlayer(b.x,b.y+b.h*.22);\n    while(S.shot<10&&S.mt>=.48+S.shot*.105)",
"    if(!isFinite(S.aim)){S.aim=aimPlayer(b.x,b.y+b.h*.22);combatWarningTick(b,'stage7-warden-burst',0,.48,true);}\n    const tell=.48;combatWarningTick(b,'stage7-warden-burst',Math.min(S.mt,tell),tell);\n    while(S.shot<10&&S.mt>=tell+S.shot*.105)",
'tick shared burst warning before unchanged release cadence');
one(
"function s7WardenMineTargets(S){",
"function s7WardenBurstAngles(S){\n  if(!S||!Number.isFinite(S.aim))return [];return [-.05,-.025,0,.025,.05].map(o=>S.aim+o);\n}\nfunction s7WardenBurstWarningDraw(b,front){\n  const S=b&&b._s7warden;if(!S||S.mode!=='burst'||S.shot>0||S.mt>=.48)return false;\n  const p=shipBossMount(b,'C'),k=clamp(S.mt/.48,0,1),angles=s7WardenBurstAngles(S);\n  if(!front)for(const a of angles)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,width:16,fieldOnly:true});\n  else{const a=Number.isFinite(S.aim)?S.aim:Math.PI/2;combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,alertOnly:true});}\n  return true;\n}\nfunction s7WardenMineTargets(S){",
'shared burst warning helpers');
one("  s7WardenRailWarningDraw(b,false);s7WardenMineWarningDraw(b,false);","  s7WardenBurstWarningDraw(b,false);s7WardenRailWarningDraw(b,false);s7WardenMineWarningDraw(b,false);",'burst fields behind hull');
one("  s7WardenRailWarningDraw(b,true);s7WardenMineWarningDraw(b,true);","  s7WardenBurstWarningDraw(b,true);s7WardenRailWarningDraw(b,true);s7WardenMineWarningDraw(b,true);",'burst alert in front of hull');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE7_WARDEN_SHARED_BURST_WARNING_0915');
