(()=>{
const checks=[];function check(v,n){checks.push({name:n,ok:!!v});if(!v)throw Error(n);}
run.stage=5;diffKey='normal';curStage=STAGES[4];spawnBoss('xenoregent');
check(!!boss._hammer,'Normal stage 5 routes to new boss');
check(boss.y>VH&&boss.enter&&!bossHitTest(boss.x,boss.y),'harmless bottom entrance');
const max=boss.hp;hitBoss(20);check(boss.hp===max,'entrance rejects direct damage');
let states=new Set();for(let i=0;i<700;i++){updateBoss(1/60);states.add(boss._hammer.state);}
check(states.has('return')&&states.has('unfold')&&states.has('warn')&&states.has('leap'),'entrance, transformation and hammer cycle run');
hammerState(boss,'warn');hammerTarget(boss);const x=boss._hammer.tx;player.x+=100;updateBoss(.2);check(boss._hammer.tx===x,'reticle commits before leap');
hammerState(boss,'ball');boss._hammer.vx=130;boss._hammer.vy=150;
boss.x=camRightX()-46;boss.y=PLAY.y+PLAY.h-46;updateBoss(.05);
check(boss._hammer.vx<0&&boss._hammer.vy<0,'ball reflects at bottom and right bounds');
boss.x=camLeftX()+46;boss.y=PLAY.y+46;updateBoss(.05);
check(boss._hammer.vx>0&&boss._hammer.vy>0,'ball reflects at top and left bounds');
_dmgBullet={kind:'missile',_auto:true,x:boss.x,y:boss.y+20};hitBoss(10);check(boss._hammer.rage>0,'passive homing fire enrages');
const before=eBullets.length;for(let i=0;i<120;i++){hitBoss(.01);updateBoss(1/60);}check(eBullets.length>before,'sustained weapon fire does not suppress rage laser release');
_dmgBullet={kind:'gmiss',x:boss.x,y:boss.y+20};hitBoss(10);check(boss._hammer.rage===0&&boss._hammer.vy<0,'manual missile knocks away without rage');
_dmgBullet=null;
check(Array.from({length:100},()=>mslPackRoll()).every(k=>k==='missilepack10'||k==='missilepack20'),'fight supply rolls only x10 and x20');
powerups.push({kind:'mcrate',_pack:'missilepack'},{kind:'missilepack'});updateBoss(.01);check(powerups.every(p=>p.kind!=='missilepack'&&p._pack!=='missilepack'),'existing x5 pickups upgrade');
hammerState(boss,'ball');for(let i=0;i<899;i++)updateBoss(1/60);check(boss._hammer.state==='ball','ball lasts full 15 seconds');updateBoss(.03);check(boss._hammer.state==='uncurl','ball exits into authored uncurl');
diffKey='hard';spawnBoss('xenoregent');check(!boss._hammer&&boss._ship==='xenoregent','Hard retains Xenoregent');
run.stage=4;curStage=STAGES[3];spawnBoss('stormsovereign');boss.y=150;boss.hp=0;bossDie();
check(!!boss._cinDeath,'stage 4 cinematic death hook');
for(let i=0;i<30;i++)updateBoss(1/60);check(_smokeRings.filter(r=>r.front).length===4,'four crossing front rings');
for(let i=0;i<180;i++)updateBoss(1/60);check(boss.y>190&&boss._cinDeath.explosions>=8,'fall and accelerating cookoff');
for(let i=0;i<210;i++)updateBoss(1/60);check(whiteBlast>.99,'white hides ship removal at seven seconds');
for(let i=0;i<120;i++)updateBoss(1/60);check(whiteBlast===0&&boss.dying>8.9,'normal scene returns after flash');
return {passed:checks.length,failed:0,checks};
})()
