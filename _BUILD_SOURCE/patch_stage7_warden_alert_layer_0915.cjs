const fs=require('fs'),path=require('path'),p=path.resolve(__dirname,'..','assets','game.js');let s=fs.readFileSync(p,'utf8');if(s.includes('\r'))throw new Error('game.js must remain LF-only');
function one(a,b,label){const n=s.split(a).length-1;if(n!==1)throw new Error(label+' expected once, found '+n);s=s.replace(a,b);}
one(
"function s7WardenRailWarningDraw(b){\n  const S=b&&b._s7warden;if(!S||S.mode!=='rail'||S.event||S.mt>=.86)return false;\n  const p=shipBossMount(b,'C'),k=clamp(S.mt/.86,0,1),angles=s7WardenRailAngles(S);\n  for(const a of angles)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,width:20,fieldOnly:true});\n  const a=Number.isFinite(S.railAim)?S.railAim:Math.PI/2;combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,alertOnly:true});return true;\n}",
"function s7WardenRailWarningDraw(b,front){\n  const S=b&&b._s7warden;if(!S||S.mode!=='rail'||S.event||S.mt>=.86)return false;\n  const p=shipBossMount(b,'C'),k=clamp(S.mt/.86,0,1),angles=s7WardenRailAngles(S);\n  if(!front)for(const a of angles)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,width:20,fieldOnly:true});\n  else{const a=Number.isFinite(S.railAim)?S.railAim:Math.PI/2;combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*650,ey:p.y+Math.sin(a)*650,progress:k,alertOnly:true});}\n  return true;\n}",
'split field and alert layers');
one("  s7WardenRailWarningDraw(b);\n  const baseY=","  s7WardenRailWarningDraw(b,false);\n  const baseY=",'field behind hull');
one(
"  return true;\n}\n/* ============================================================\n   STAGE 9's TWO SHIP BOSSES FIRE AUTHORED ORDNANCE NOW",
"  s7WardenRailWarningDraw(b,true);\n  return true;\n}\n/* ============================================================\n   STAGE 9's TWO SHIP BOSSES FIRE AUTHORED ORDNANCE NOW",
'alert in front of hull');
fs.writeFileSync(p,s,'utf8');console.log('PATCHED_STAGE7_WARDEN_ALERT_LAYER_0915');
