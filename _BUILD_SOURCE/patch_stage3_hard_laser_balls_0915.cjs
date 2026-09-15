const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const file=path.join(root,'assets','game.js');
const backup=path.join(root,'_shots','backups','game_pre_stage3_hard_laser_balls_0915.js');
let s=fs.readFileSync(file,'utf8');
if(s.includes('\r'))throw new Error('assets/game.js line-ending drift');
fs.mkdirSync(path.dirname(backup),{recursive:true});
if(!fs.existsSync(backup))fs.copyFileSync(file,backup);
function once(from,to,label){
  const n=s.split(from).length-1;
  if(n!==1)throw new Error(label+' expected once, found '+n);
  s=s.replace(from,to);
}
once(
"  if(b._s3boss.role==='wall'){\n    q._s3StaticSpin=true;q._shootable=false;q.hp=undefined;\n  }else if(opt.shootable){q._shootable=true;q.hp=opt.hp||1;}",
"  if(b._s3boss.role==='wall'&&!opt.homingBall){\n    q._s3StaticSpin=true;q._shootable=false;q.hp=undefined;\n  }else if(opt.shootable){q._shootable=true;q.hp=opt.hp||1;}\n  if(opt.homingBall){q._s3StaticSpin=true;q._s3LaserBall=true;}",
'allow only the Hard Retina balls through the wall shootable gate');
once(
"function stage3BossQueueVolley(b,events,duration){\n  if(!b||!b._s3boss)return;\n  b._s3boss.volley={t:0,i:0,events:events||[],duration:duration||1};\n}\n",
"function stage3BossQueueVolley(b,events,duration){\n  if(!b||!b._s3boss)return;\n  b._s3boss.volley={t:0,i:0,events:events||[],duration:duration||1};\n}\n/* Hard/Furious Rime Wall pressure below half health: two independently shootable laser balls\n   share one Retina. The lock grants their steering, so a new roll/somersault breaks both at\n   once and the rounds keep their last vector until they leave the world. Inside the shared\n   commit radius they also freeze normally, preserving the last-second dodge. */\nfunction stage3BossHardLaserPair(b){\n  const S=b&&b._s3boss,hard=(typeof diffKey!=='undefined'&&(diffKey==='hard'||diffKey==='furious'));\n  if(!S||S.role!=='wall'||!hard||b.hp>b.maxhp*.5||typeof enemyLockOn!=='function')return false;\n  const pid=S.hardLaserPid=(S.hardLaserPid||0)+1,slots=['L','R'];\n  for(let i=0;i<slots.length;i++){\n    const slot=slots[i];\n    enemyLockOn(b,.58+i*.24,{fire:function(){\n      if(!b||b.dead||!b._s3boss||b._s3boss.hardLaserPid!==pid)return;\n      const p=shipBossMount(b,slot),a=aimPlayer(p.x,p.y);\n      const q=stage3BossShot(b,slot,a,2.35,'s3mortar',{w:34,h:34,szMul:1.28,\n        accel:.78,max:5.25,shootable:true,hp:2,homingBall:true,silent:i>0});\n      q._threatBullet=1.06;stage3BossMuzzle(b,slot,'s3mortar',1.05,.20);\n    }});\n  }\n  return true;\n}\n",
'insert Hard Retina laser pair');
once(
"  }else if(pat==='s3wallhalo'){\n    /* The old phase was one slow orb and then empty time.",
"  }else if(pat==='s3wallhalo'){\n    stage3BossHardLaserPair(b);\n    /* The old phase was one slow orb and then empty time.",
'add pair to below-half halo');
once(
"  }else if(pat==='s3walloverdrive'){\n    /* Final form: three locked beams establish the corridors, a gated halo closes the idle lanes,",
"  }else if(pat==='s3walloverdrive'){\n    stage3BossHardLaserPair(b);\n    /* Final form: three locked beams establish the corridors, a gated halo closes the idle lanes,",
'add pair to critical overdrive');
fs.writeFileSync(file,s,'utf8');
if(fs.readFileSync(file,'utf8').includes('\r'))throw new Error('wrote CRLF to assets/game.js');
console.log('patched Stage-3 Hard Retina laser pair');
