const fs=require('fs');const path=require('path');const root=path.resolve(__dirname,'..'),file=path.join(root,'assets','game.js');let s=fs.readFileSync(file,'utf8');
if(/\r\n/.test(s))throw new Error('assets/game.js must remain LF-only');
const backup=path.join(root,'_shots','backups','game_pre_frost_cruiser_furious_charge_0915.js');fs.mkdirSync(path.dirname(backup),{recursive:true});if(!fs.existsSync(backup))fs.writeFileSync(backup,s,'utf8');
function once(from,to,label){const n=s.split(from).length-1;if(n!==1)throw new Error(label+' expected 1 match, got '+n);s=s.replace(from,to);}

once(
"const FROST_ROCKET_CHARGE=1.35,FROST_ROCKET_GAP=.18,FROST_ROCKET_COUNT=6;",
"const FROST_ROCKET_CHARGE=1.35,FROST_ROCKET_GAP=.18,FROST_ROCKET_COUNT=6;\nconst FROST_FURY_TELL=1.20,FROST_FURY_LOCK=.86,FROST_FURY_DASH=760,FROST_FURY_RETURN=260;",
'furious constants');

once(
"  if(state==='frostRocketCharge'&&J.hardVariant){\n    J.charge=0;J.rocketLock=frostCruiserRocketLock(b);\n  }",
"  if((state==='frostRocketCharge'||state==='furyRocketCharge')&&J.hardVariant){\n    J.charge=0;J.rocketLock=frostCruiserRocketLock(b);\n  }\n  if(state==='furyChargeWarn'){\n    const T=targetShip(b.x,b.y);J.furyAimX=T.x;J.furyAimY=T.y;J.furyLocked=false;J.charge=1;\n  }\n  if(state==='furyDash'){\n    const dx=J.furyAimX-b.x,dy=J.furyAimY-b.y,d=Math.hypot(dx,dy)||1;\n    J.furyVX=dx/d*FROST_FURY_DASH;J.furyVY=dy/d*FROST_FURY_DASH;J.rot=Math.atan2(J.furyVY,J.furyVX)-Math.PI/2;\n    J.ghost=false;b._jcGhost=false;J.thrust=1;\n  }",
'furious state setup');

once(
"  if(state==='diveSouth'||state==='riseNorth'||state==='returnTop'){\n    J.ghost=true;b._jcGhost=true;\n  }",
"  if(state==='diveSouth'||state==='riseNorth'||state==='returnTop'||state==='furyReturn'){\n    J.ghost=true;b._jcGhost=true;\n  }",
'furious return ghost');

once(
"    if(J.rageQueued&&!J.ghost&&J.state!=='beamCharge'&&J.state!=='beamSweep'&&J.state.indexOf('rage')!==0){\n      J.rageQueued=false;jungleCruiserSetState(b,'rageMissiles');\n    }",
"    if(J.rageQueued&&!J.ghost&&J.state!=='beamCharge'&&J.state!=='beamSweep'&&J.state.indexOf('rage')!==0&&J.state.indexOf('fury')!==0){\n      J.rageQueued=false;\n      jungleCruiserSetState(b,b._ship==='frostcruiser'&&diffKey==='furious'?'furyRocketCharge':'rageMissiles');\n    }",
'furious rage route');

once(
"    case 'rageMissiles': {\n      jungleCruiserStalk(b,dt);const count=8;",
"    case 'furyRocketCharge': {\n      jungleCruiserStalk(b,dt);J.charge=clamp(J.t/FROST_ROCKET_CHARGE,0,1);\n      if(J.t>=FROST_ROCKET_CHARGE+(FROST_ROCKET_COUNT-1)*FROST_ROCKET_GAP+.32)jungleCruiserSetState(b,'furyChargeWarn');\n      break; }\n    case 'furyChargeWarn': {\n      const T=targetShip(b.x,b.y);\n      if(!J.furyLocked&&J.t<FROST_FURY_LOCK){J.furyAimX=T.x;J.furyAimY=T.y;}\n      if(!J.furyLocked&&J.t>=FROST_FURY_LOCK){J.furyLocked=true;J.furyAimX=T.x;J.furyAimY=T.y;\n        try{if(Audio&&Audio.SFX&&(Audio.SFX.alertLockon||Audio.SFX.dangerAlert))(Audio.SFX.alertLockon||Audio.SFX.dangerAlert)();}catch(_fcfl){}\n      }\n      const a=Math.atan2(J.furyAimY-b.y,J.furyAimX-b.x);J.rot+=(a-Math.PI/2-J.rot)*Math.min(1,dt*7);\n      combatWarningTick(b,'frost-cruiser-furious-charge',J.t,FROST_FURY_TELL,true);\n      if(J.t>=FROST_FURY_TELL)jungleCruiserSetState(b,'furyDash');\n      break; }\n    case 'furyDash':\n      J.thrust=1;b.x+=J.furyVX*dt;b.y+=J.furyVY*dt;\n      if(b.y>VH+b.h*.72||b.x<camLeftX()-b.w||b.x>camRightX()+b.w){\n        const margin=b.w*.52;b.x=clamp(J.furyAimX,camLeftX()+margin,camRightX()-margin);b.y=-b.h*.72;J.rot=0;\n        jungleCruiserSetState(b,'furyReturn');\n      }\n      break;\n    case 'furyReturn':\n      J.ghost=true;b._jcGhost=true;J.thrust=1;J.rot=0;b.y+=FROST_FURY_RETURN*dt;b.x+=(W*.5-b.x)*Math.min(1,dt*1.1);\n      if(b.y>=sy){b.y=sy;J.ghost=false;b._jcGhost=false;J.charge=0;jungleCruiserSetState(b,'recover');}\n      break;\n    case 'rageMissiles': {\n      jungleCruiserStalk(b,dt);const count=8;",
'furious attack states');

once(
"  const frost=b._ship==='frostcruiser',charging=frost&&J.state==='beamCharge',rocketCharging=frost&&J.state==='frostRocketCharge';",
"  const frost=b._ship==='frostcruiser',charging=frost&&J.state==='beamCharge',\n    rocketCharging=frost&&(J.state==='frostRocketCharge'||J.state==='furyRocketCharge'),furyWarning=frost&&J.state==='furyChargeWarn';",
'furious draw state');

once(
"  if(frost&&(charging||J.beamActive)){",
"  if(furyWarning){\n    const C=shipBossMount(b,'C'),e={x:C.x,y:C.y,ex:J.furyAimX,ey:J.furyAimY,progress:clamp(J.t/FROST_FURY_TELL,0,1),width:b.w*.42};\n    combatWarningDraw(b,e);\n  }\n  if(frost&&(charging||J.beamActive)){",
'furious warning draw');

if(/\r\n/.test(s))throw new Error('patch introduced CRLF');fs.writeFileSync(file,s,'utf8');console.log('patched Frost Cruiser Furious volley-charge combo');
