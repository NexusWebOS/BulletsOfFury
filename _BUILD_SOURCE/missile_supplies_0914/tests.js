// ===== 301. MISSILE SUPPLIES DURING ENCOUNTERS, 0914 =====
console.log('=== 301. missile supplies during encounters ===');
{
 var supplies301=JSON.parse(vm.runInContext(`(function(){
   var r=Math.random,o={};Math.random=function(){return .9;};
   for(var st=1;st<=9;st++){run.stage=st;o[st]=mslPackRoll();}
   Math.random=function(){return .1;};run.stage=8;o.low8=mslPackRoll();
   Math.random=r;run.bombs=0;applyPowerup({kind:'missilepack',x:0,y:0});o.five=run.bombs;
   run.bombs=0;applyPowerup({kind:'missilepack2',x:0,y:0});o.oldTwo=run.bombs;
   return JSON.stringify(o);
 })()`,ctxv));
 ok([1,2,3,4,5,6,7].every(i=>supplies301[i]==='missilepack20'),'every stage 1-7 can roll the authored x20 supply');
 ok(supplies301[8]==='missilepack100'&&supplies301.low8==='missilepack50','stage 8 rolls both x50 and x100 ammo');
 ok(supplies301[9]==='missilepack10','unspecified stage 9 retains small supplies without an x2 roll');
 ok(supplies301.five===5&&supplies301.oldTwo===5,'x5 graphics grant five rounds and old x2 pickups migrate to five');
 var bossSupply301=JSON.parse(vm.runInContext(`(function(){
   var oldB=boss,oldS=subBoss,oldA=bossActive,oldSA=subBossActive;boss={hp:100,x:240,y:100};bossActive=true;
   subBoss={hp:100,x:220,y:100};subBossActive=true;enemies=[];powerups=[];player.dead=false;player.x=240;run.stage=1;diffKey='normal';
   bossMissileSupplyTick(6.9);var pre=powerups.length;bossMissileSupplyTick(.2);var first=powerups.length;
   bossMissileSupplyTick(40);var cap=powerups.length;powerups=[];bossMissileSupplyTick(.01);var again=powerups.length;
   powerups=[];boss._missileSupply={t:0,due:18};subBossActive=false;diffKey='hard';bossMissileSupplyTick(18);
   var hardDue=boss._missileSupply.due;var deadT=boss._missileSupply.t;player.dead=true;bossMissileSupplyTick(99);
   var deadAfter=boss._missileSupply.t;player.dead=false;
   boss=oldB;subBoss=oldS;bossActive=oldA;subBossActive=oldSA;diffKey='normal';powerups=[];
   return JSON.stringify({pre,first,cap,again,hardDue,deadT,deadAfter});
 })()`,ctxv));
 ok(bossSupply301.pre===0&&bossSupply301.first===1,'a boss/miniboss supply arrives after a seven-second entrance allowance');
 ok(bossSupply301.cap===1&&bossSupply301.again===1,'overlapping encounters share one live supply and restock after its removal');
 ok(bossSupply301.hardDue===18/1.25,'hard boss missile restock frequency increases exactly 25 percent');
 ok(bossSupply301.deadT===bossSupply301.deadAfter,'dead players cannot advance the missile supply clock');
 var loose301=JSON.parse(vm.runInContext(`(function(){
   var r=Math.random;Math.random=function(){return 0;};powerups=[];
   var e={x:240,y:200,type:'s1jetdelta'};enemies=[e];enemyMissileDrop(e);var n=powerups.length;
   enemyMissileDrop(e);var twice=powerups.length;
   var spread=powerups.map(p=>p._scatterVx),kinds=powerups.map(p=>p.kind);
   for(var k of ['_boss','_amini','mini','_mini','_sub','sub','modular','_prop','_waterRock']){
     var q={x:240,y:200};q[k]=true;enemies=[q];enemyMissileDrop(q);
   }
   var protectedN=powerups.length;Math.random=function(){return .9;};var q={x:20,y:200};enemies=[q];enemyMissileDrop(q);
   var noDrop=powerups.length;Math.random=r;enemies=[];powerups=[];
   return JSON.stringify({n,twice,spread,kinds,protectedN,noDrop});
 })()`,ctxv));
 ok(loose301.n===2&&loose301.spread[0]<0&&loose301.spread[1]>0,'a successful double fodder drop scatters two actual collectible missiles apart');
 ok(loose301.twice===2,'repeated death handling cannot grant another ammo drop');
 ok(loose301.protectedN===2,'bosses, minibosses and destructible props never receive the loose missile RNG');
 ok(loose301.noDrop===2&&loose301.kinds.every(k=>k==='bomb'),'failed RNG grants nothing; accepted missile drops use the actual one-round collect case');
}
