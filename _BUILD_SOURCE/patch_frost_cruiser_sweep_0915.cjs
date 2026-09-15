const fs=require('fs');const path=require('path');
const root=path.resolve(__dirname,'..'),file=path.join(root,'assets','game.js');let src=fs.readFileSync(file,'utf8');
if(src.includes('\r\n'))throw new Error('assets/game.js must remain LF-only');
function once(from,to,label){const n=src.split(from).length-1;if(n!==1)throw new Error(label+': expected one match, found '+n);src=src.replace(from,to);}

once(
  "const JC_GUN_GAP=0.045, JC_BEAM_CHARGE=1.25, JC_BEAM_HOLD=8.6;\nconst JC_BEAM_SWEEP=Math.PI/6, JC_BEAM_PERIOD=2.55, JC_BEAM_CENTER_SPEED=330;",
  "const JC_GUN_GAP=0.045, JC_BEAM_CHARGE=1.25, JC_BEAM_HOLD=8.6;\nconst JC_BEAM_SWEEP=Math.PI/6, JC_BEAM_PERIOD=2.55, JC_BEAM_CENTER_SPEED=330;\nconst FROST_BEAM_CHARGE=3.0,FROST_BEAM_HOLD=5.2,FROST_BEAM_SWEEP=.78,FROST_BEAM_WIDTH=52.5;",
  'Frost sweep constants');
once(
  "    charge:0,beamActive:false,beamAng:0,beamSound:false,ghost:false,\n    damaged:false,enraged:false,rageQueued:false,blasts:[],blastCd:0.22};",
  "    charge:0,beamActive:false,beamAng:0,beamSound:false,beamDir:1,crackleBeat:-1,ghost:false,\n    damaged:false,enraged:false,rageQueued:false,blasts:[],blastCd:0.22};",
  'Frost sweep state');
once(
  "  if(b._ship==='frostcruiser'&&XART._touch)XART._touch('fllaser_0');",
  "  if(b._ship==='frostcruiser'&&XART._touch){XART._touch('fllaser_0');XART._touch('cfx_stage4_chain_lightning');}",
  'Frost crackle warm');
once(
  "  if(state!=='beamSweep')J.beamActive=false;\n  if(state==='edgeGun'||state==='rageChargeEdge'){",
  "  if(state!=='beamSweep')J.beamActive=false;\n  if(state==='beamCharge'&&b._ship==='frostcruiser'){\n    const W=(typeof worldWidth==='function')?worldWidth():VW;J.beamDir=(player&&player.x<W*.5)?1:-1;\n    J.beamAng=-J.beamDir*FROST_BEAM_SWEEP;J.crackleBeat=-1;\n  }\n  if(state==='edgeGun'||state==='rageChargeEdge'){",
  'Frost committed sweep direction');
once(
  "  const off=Math.abs(px*dy-py*dx),r=(player._hx||9)+12;",
  "  const wide=b._ship==='frostcruiser'?FROST_BEAM_WIDTH:42;\n  const off=Math.abs(px*dy-py*dx),r=(player._hx||9)+wide*(12/42);",
  'Frost beam collision width');
once(
  "      const centre=W*.5,dx=centre-b.x,step=Math.sign(dx)*Math.min(Math.abs(dx),JC_BEAM_CENTER_SPEED*dt);\n      b.x+=step;b.y+=(sy-b.y)*Math.min(1,dt*6);J.charge=clamp(J.t/JC_BEAM_CHARGE,0,1);",
  "      const frost=b._ship==='frostcruiser',chargeDur=frost?FROST_BEAM_CHARGE:JC_BEAM_CHARGE;\n      const centre=W*.5,dx=centre-b.x,step=Math.sign(dx)*Math.min(Math.abs(dx),JC_BEAM_CENTER_SPEED*dt);\n      b.x+=step;b.y+=(sy-b.y)*Math.min(1,dt*6);J.charge=clamp(J.t/chargeDur,0,1);",
  'Frost charge duration');
once(
  "      if(!J.chargeSound){J.chargeSound=true;try{if(Audio&&Audio.SFX&&Audio.SFX.bossWeaponCharge)Audio.SFX.bossWeaponCharge();}catch(_jcc){}}\n      if(J.t>=JC_BEAM_CHARGE&&Math.abs(dx)<2){",
  "      if(!J.chargeSound){J.chargeSound=true;try{if(Audio&&Audio.SFX&&Audio.SFX.bossWeaponCharge)Audio.SFX.bossWeaponCharge();}catch(_jcc){}}\n      if(frost){\n        const beat=Math.floor(J.t/.28);if(beat>J.crackleBeat){J.crackleBeat=beat;try{if(Audio&&Audio.SFX&&(Audio.SFX.crackle||Audio.SFX.enemyElectricBolt))(Audio.SFX.crackle||Audio.SFX.enemyElectricBolt)();}catch(_jccr){}}\n        combatWarningTick(b,'frost-cruiser-sweep',J.t,chargeDur);\n      }\n      if(J.t>=chargeDur&&Math.abs(dx)<2){",
  'Frost crackle and warning');
once(
  "        b.x=centre;J.rot=0;J.charge=1;J.chargeSound=false;jungleCruiserSetState(b,'beamSweep');J.beamActive=true;\n        jungleCruiserFlash",
  "        b.x=centre;J.rot=0;J.charge=1;J.chargeSound=false;jungleCruiserSetState(b,'beamSweep');J.beamActive=true;\n        if(frost)J.beamAng=-J.beamDir*FROST_BEAM_SWEEP;\n        jungleCruiserFlash",
  'Frost sweep start');
once(
  "    case 'beamSweep':\n      /* Centre lock plus a full +/-30 degree sweep gives both edges a readable escape lane on\n         alternating beats.  The beam never samples player.x; survival is movement and timing,\n         not the boss cheating by following the player. */\n      J.beamActive=true;J.beamAng=Math.sin(J.t*(Math.PI*2/JC_BEAM_PERIOD))*JC_BEAM_SWEEP;J.rot=J.beamAng*0.18;\n      b.x=W*.5;b.y=sy;jungleCruiserBeamHit(b);\n      if(J.t>=JC_BEAM_HOLD){J.beamActive=false;J.charge=0;J.rot=0;jungleCruiserSetState(b,'recover');}\n      break;",
  "    case 'beamSweep': {\n      /* Frost makes one predictable edge-to-edge sweep, starting opposite the sampled player.\n         The older Jungle encounter keeps its cyclic green beam untouched. */\n      const frost=b._ship==='frostcruiser',hold=frost?FROST_BEAM_HOLD:JC_BEAM_HOLD;\n      J.beamActive=true;\n      if(frost){const u=fztSmooth(clamp(J.t/hold,0,1));J.beamAng=fztMix(-J.beamDir*FROST_BEAM_SWEEP,J.beamDir*FROST_BEAM_SWEEP,u);}\n      else J.beamAng=Math.sin(J.t*(Math.PI*2/JC_BEAM_PERIOD))*JC_BEAM_SWEEP;\n      J.rot=J.beamAng*0.18;b.x=W*.5;b.y=sy;jungleCruiserBeamHit(b);\n      if(J.t>=hold){J.beamActive=false;J.charge=0;J.rot=0;jungleCruiserSetState(b,'recover');}\n      break; }",
  'Frost linear sweep');
once(
  "function jungleCruiserDrawUnder(b){\n  const J=b&&b._jc;if(!J||!J.beamActive||typeof XART==='undefined')return;\n  const C=shipBossMount(b,'C'),a=Math.PI/2+(J.beamAng||0),len=VH*1.55,bw=42;",
  "function jungleCruiserDrawUnder(b){\n  const J=b&&b._jc;if(!J||typeof XART==='undefined')return;\n  const frost=b._ship==='frostcruiser',charging=frost&&J.state==='beamCharge';\n  if(frost&&(charging||J.beamActive)){\n    const alpha=charging?.10+.42*clamp(J.charge,0,1):.48;ctx.save();ctx.fillStyle='rgba(1,5,13,'+alpha+')';\n    ctx.fillRect(camLeftX()-8,viewTopY()-8,viewW()+16,viewH()+16);ctx.restore();\n    if(charging&&typeof combatAtlasDraw==='function'){const fi=Math.floor(J.t*22)%8,r=b.w*.48;\n      for(let i=0;i<4;i++){const a=i*TAU/4+J.t*.9,x=b.x+Math.cos(a)*r,y=(b._drawY!=null?b._drawY:b.y)+Math.sin(a)*r*.72;\n        combatAtlasDraw('cfx_stage4_chain_lightning',4,2,fi,x,y,30,68,{angle:a-Math.PI/2,alpha:.42+.42*J.charge,blend:'lighter'});}}\n    if(charging){const C=shipBossMount(b,'C'),a=Math.PI/2+(J.beamAng||0),e={x:C.x,y:C.y,ex:C.x+Math.cos(a)*VH*1.55,ey:C.y+Math.sin(a)*VH*1.55,progress:J.charge,width:FROST_BEAM_WIDTH};combatWarningDraw(b,e);}\n  }\n  if(!J.beamActive)return;\n  const C=shipBossMount(b,'C'),a=Math.PI/2+(J.beamAng||0),len=VH*1.55,bw=frost?FROST_BEAM_WIDTH:42;",
  'Frost darkness crackle warning and width');
const backupDir=path.join(root,'_shots','backups');fs.mkdirSync(backupDir,{recursive:true});fs.copyFileSync(file,path.join(backupDir,'game_pre_frost_cruiser_sweep_0915.js'));
fs.writeFileSync(file,src,'utf8');console.log('PATCHED_FROST_CRUISER_SWEEP_0915');
