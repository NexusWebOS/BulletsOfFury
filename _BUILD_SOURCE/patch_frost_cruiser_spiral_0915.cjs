const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
let s=fs.readFileSync(file,'utf8');
if(/\r\n/.test(s))throw new Error('assets/game.js must remain LF-only');
const backup=path.join(root,'_shots','backups','game_pre_frost_cruiser_spiral_0915.js');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.writeFileSync(backup,s,'utf8');
function once(from,to,label){
  const n=s.split(from).length-1;
  if(n!==1)throw new Error(label+' expected 1 match, got '+n);
  s=s.replace(from,to);
}

once(
"const FROST_BEAM_CHARGE=3.0,FROST_BEAM_HOLD=5.2,FROST_BEAM_SWEEP=.78,FROST_BEAM_WIDTH=52.5;",
"const FROST_BEAM_CHARGE=3.0,FROST_BEAM_HOLD=5.2,FROST_BEAM_SWEEP=.78,FROST_BEAM_WIDTH=52.5;\nconst FROST_ROCKET_CHARGE=1.35,FROST_ROCKET_GAP=.18,FROST_ROCKET_COUNT=6;",
'rocket constants');

once(
"  if(J.state==='beamSweep'&&state!=='beamSweep')jungleCruiserBeamAudio(b,false);\n  J.state=state;J.t=0;J.shot=0;J.gunClock=0;J.sample=0;J.thrust=0;",
"  if(J.state==='beamSweep'&&state!=='beamSweep')jungleCruiserBeamAudio(b,false);\n  if(J.state==='frostRocketCharge'&&state!=='frostRocketCharge')J.charge=0;\n  J.state=state;J.t=0;J.shot=0;J.gunClock=0;J.sample=0;J.thrust=0;",
'state exit reset');

once(
"  if(state==='beamCharge'&&b._ship==='frostcruiser'){\n    const W=(typeof worldWidth==='function')?worldWidth():VW;J.beamDir=(player&&player.x<W*.5)?1:-1;\n    J.beamAng=-J.beamDir*FROST_BEAM_SWEEP;J.crackleBeat=-1;\n  }",
"  if(state==='beamCharge'&&b._ship==='frostcruiser'){\n    const W=(typeof worldWidth==='function')?worldWidth():VW;J.beamDir=(player&&player.x<W*.5)?1:-1;\n    J.beamAng=-J.beamDir*FROST_BEAM_SWEEP;J.crackleBeat=-1;\n  }\n  if(state==='frostRocketCharge'&&J.hardVariant){\n    J.charge=0;J.rocketLock=frostCruiserRocketLock(b);\n  }",
'state entry queue');

once(
"function jungleCruiserLoopMissiles(b){\n  for(const item of [['L',-1],['R',1]]){",
"function frostCruiserSpiralRocket(b,slot,index){\n  if(!b||b.dead)return null;\n  const m=shipBossMount(b,slot),side=slot==='L'?-1:1,t=targetShip(m.x,m.y);\n  const a=eAimDown(Math.atan2(t.y-m.y,t.x-m.x)+side*.075),spd=2.70;\n  const q={x:m.x,y:m.y,vx:Math.cos(a)*spd,vy:Math.sin(a)*spd,ang:a,spd:spd,w:14,h:24,dmg:1,t:0,\n    kind:'emissile',hp:1,_shootable:true,_boss:true,_noArsenal:true,_jcRocket:true,_frostSpiral:true,\n    _frostSlot:slot,_frostIndex:index,_swirl:true,_swPh:index*TAU/FROST_ROCKET_COUNT,_swAmp:.82,\n    homing:false,_accel:.032,_maxspd:5.65};\n  eBullets.push(q);jungleCruiserFlash(b,slot,BPFX_MUZZLE_MISSILE,1.05,62,.20);\n  try{if(Audio&&Audio.SFX&&(Audio.SFX.missile||Audio.SFX.enemyBossCannon))(Audio.SFX.missile||Audio.SFX.enemyBossCannon)();}catch(_fcrm){}\n  shake=Math.max(shake,3);return q;\n}\nfunction frostCruiserRocketLock(b){\n  if(typeof enemyLockOn!=='function'||!b||b.dead)return null;\n  let lock=null;\n  for(let i=0;i<FROST_ROCKET_COUNT;i++){\n    const slot=(i&1)?'R':'L';\n    lock=enemyLockOn(b,FROST_ROCKET_CHARGE+i*FROST_ROCKET_GAP,{fire:function(){frostCruiserSpiralRocket(b,slot,i);}})||lock;\n  }\n  return lock;\n}\nfunction jungleCruiserLoopMissiles(b){\n  for(const item of [['L',-1],['R',1]]){",
'rocket functions');

once(
"      if(J.t>=(b._ship==='frostcruiser'?.90:1.35))jungleCruiserSetState(b,'missiles');",
"      if(J.t>=(b._ship==='frostcruiser'?.90:1.35))jungleCruiserSetState(b,J.hardVariant?'frostRocketCharge':'missiles');",
'hard entry route');

once(
"    case 'missiles': {\n      jungleCruiserStalk(b,dt);const gap=J.damaged?0.145:JC_POD_GAP,count=4;",
"    case 'frostRocketCharge': {\n      jungleCruiserStalk(b,dt);J.charge=clamp(J.t/FROST_ROCKET_CHARGE,0,1);\n      if(J.t>=FROST_ROCKET_CHARGE+(FROST_ROCKET_COUNT-1)*FROST_ROCKET_GAP+.38){\n        J.charge=0;jungleCruiserSetState(b,'edgeGun');\n      }\n      break; }\n    case 'missiles': {\n      jungleCruiserStalk(b,dt);const gap=J.damaged?0.145:JC_POD_GAP,count=4;",
'hard charge state');

once(
"      if(J.t>=0.82)jungleCruiserSetState(b,J.enraged?'rageMissiles':'missiles');",
"      if(J.t>=0.82)jungleCruiserSetState(b,J.enraged?'rageMissiles':(J.hardVariant?'frostRocketCharge':'missiles'));",
'hard recovery route');

once(
"  const frost=b._ship==='frostcruiser',charging=frost&&J.state==='beamCharge';\n  if(frost&&(charging||J.beamActive))",
"  const frost=b._ship==='frostcruiser',charging=frost&&J.state==='beamCharge',rocketCharging=frost&&J.state==='frostRocketCharge';\n  if(rocketCharging&&typeof combatAtlasDraw==='function'){\n    const fi=Math.floor(J.t*22)%8;\n    for(const slot of ['L','R']){const m=shipBossMount(b,slot),side=slot==='L'?-1:1;\n      combatAtlasDraw('cfx_stage4_chain_lightning',4,2,fi,m.x,m.y,24+18*J.charge,54+28*J.charge,{angle:side*.34,alpha:.28+.48*J.charge,blend:'lighter'});\n    }\n  }\n  if(frost&&(charging||J.beamActive))",
'rocket charge draw');

if(/\r\n/.test(s))throw new Error('patch introduced CRLF');
fs.writeFileSync(file,s,'utf8');
console.log('patched Frost Cruiser Retina spiral volley');
