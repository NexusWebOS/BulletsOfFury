// ===== 305. DIRECTIONAL RETINA SCAN, 0914 =====
console.log('=== 305. directional Retina scan ===');
{
 var rs305=JSON.parse(vm.runInContext(`(function(){
  const save={boss,subBoss,bossActive,subBossActive,enemies,retina,player,run:{...run},pBullets,powerups,special,camX,curStage};const o={};
  try{
   boss=null;subBoss=null;bossActive=false;subBossActive=false;special=null;player={x:240,y:400,dead:false};pBullets=[];powerups=[];retina={target:null};run.retinaScan=true;run.bombs=8;run.stage=2;camX=0;curStage=STAGES[1];
   const make=(x,y)=>({x,y,w:30,h:30,hp:100,maxhp:100,dead:false});enemies=[make(130,200),make(230,150),make(350,190),make(240,80),make(240,460)];
   retinaScanDirection(0,-1);retinaScanDirection(0,-1);retinaScanDirection(0,-1);retinaScanDirection(0,-1);
   o.direction=retinaScanState().marks.length===4&&!retinaScanState().marks.some(m=>m.target===enemies[4]);
   const first=retinaScanState().marks[0].target;retinaScanDirection(0,-1);o.capUnique=retinaScanState().marks.length===4&&new Set(retinaScanState().marks.map(m=>m.target)).size===4;
   retinaScanTick(.44);o.acquire=retinaScanState().marks.every(m=>m.phase==='seek');retinaScanTick(.02);o.locks=retinaScanState().marks.every(m=>m.phase==='locked'&&m.lockT===5);
   retinaScanFire();retinaScanTick(.001);o.first=pBullets.length===1&&run.bombs===7&&pBullets[0].tgt===first;
   retinaScanTick(.02);o.delay=pBullets.length===1;retinaScanTick(.03);o.second=pBullets.length===2&&run.bombs===6;
   for(let i=0;i<2;i++)retinaScanTick(.051);o.sequence=pBullets.length===4&&run.bombs===4&&!retinaScanState().queue&&!retinaScanState().marks.length;
   retinaScanAdd(enemies[0]);retinaScanTick(.5);retinaScanTick(3.81);o.flash=retinaScanState().marks.some(m=>m.lockT<1.2);retinaScanTick(1.2);o.expire=retinaScanState().marks.length===0&&!retinaScanFire();
   retinaScanAdd(enemies[0]);retinaScanAdd(enemies[1]);retinaScanTick(.5);retinaScanFire();enemies[0].dead=true;const ammo=run.bombs;retinaScanTick(.001);o.invalidFree=run.bombs===ammo;retinaScanTick(.051);o.liveFires=run.bombs===ammo-1;
   retinaScanAdd(enemies[1]);retinaScanAdd(enemies[2]);retinaScanTick(.5);run.bombs=1;retinaScanFire();retinaScanTick(.001);retinaScanTick(.051);o.ammoFloor=run.bombs===0&&!retinaScanState().queue;
   run.bombs=3;retinaScanAdd(enemies[1]);player.dead=true;retinaScanTick(.01);o.deathClears=!player._retinaScan;
   player.dead=false;run.retinaScan=false;retinaScanSupply({kind:'mcrate',x:240,y:200});retinaScanSupply({kind:'mcrate',x:240,y:200});o.onePickup=powerups.filter(p=>p.kind==='retinascan').length===1;applyPowerup(powerups[0]);o.grant=run.retinaScan===true&&campSnapshot().retinaScan===true;
   return JSON.stringify(o);
  }finally{boss=save.boss;subBoss=save.subBoss;bossActive=save.bossActive;subBossActive=save.subBossActive;enemies=save.enemies;retina=save.retina;player=save.player;camX=save.camX;curStage=save.curStage;Object.assign(run,save.run);pBullets=save.pBullets;powerups=save.powerups;special=save.special;}
 })()`,ctxv));
 for(const k of Object.keys(rs305))ok(rs305[k],'Directional Retina scan: '+k);
}
