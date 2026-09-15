const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
"  if(mode==='burst')S.aim=aimPlayer(b.x,b.y+b.h*.22);\n  if(mode==='teleport'){",
"  if(mode==='burst')S.aim=aimPlayer(b.x,b.y+b.h*.22);\n  if(mode==='rail'){S.railAim=aimPlayer(b.x,b.y);S.railSafe=player.x<b.x?-1:1;combatWarningTick(b,'stage7-warden-rail',0,.86,true);}\n  if(mode==='teleport'){",
'commit rail target at charge start');
one(
"  }else if(S.mode==='rail'){\n    if(!S.event&&S.mt>.86){S.event=1;const base=aimPlayer(b.x,b.y),safe=(player.x<b.x)?-1:1;\n      for(const o of [-.44,-.30,-.16,0,.16,.30,.44]){if(Math.sign(o)===safe&&Math.abs(o)>.28)continue;",
"  }else if(S.mode==='rail'){\n    const tell=.86;combatWarningTick(b,'stage7-warden-rail',Math.min(S.mt,tell),tell);\n    if(!S.event&&S.mt>tell){S.event=1;const base=S.railAim,safe=S.railSafe;\n      for(const o of [-.44,-.30,-.16,0,.16,.30,.44]){if(Math.sign(o)===safe&&Math.abs(o)>.28)continue;",
'shared rail warning tick and committed release');
one(
"function s7WardenDraw(b){\n  const S=b&&b._s7warden;if(!S)return false;const F=S.final,phase=F&&F.phase;\n  if(phase==='portalClose'||(F&&F.bossHidden))return true;",
"function s7WardenRailAngles(S){\n  if(!S||!Number.isFinite(S.railAim))return [];const safe=S.railSafe;\n  return [-.44,-.30,-.16,0,.16,.30,.44].filter(o=>!(Math.sign(o)===safe&&Math.abs(o)>.28)).map(o=>S.railAim+o);\n}\nfunction s7WardenRailWarningDraw(b){\n  const S=b&&b._s7warden;if(!S||S.mode!=='rail'||S.event||S.mt>=.86)return false;\n  const p=shipBossMount(b,'C'),k=clamp(S.mt/.86,0,1),angles=s7WardenRailAngles(S);\n  for(const a of angles)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,width:20,fieldOnly:true});\n  const a=Number.isFinite(S.railAim)?S.railAim:Math.PI/2;combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,alertOnly:true});return true;\n}\nfunction s7WardenDraw(b){\n  const S=b&&b._s7warden;if(!S)return false;const F=S.final,phase=F&&F.phase;\n  if(phase==='portalClose'||(F&&F.bossHidden))return true;\n  s7WardenRailWarningDraw(b);",
'shared rail warning draw');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE7_WARDEN_SHARED_RAIL_WARNING_0915');
