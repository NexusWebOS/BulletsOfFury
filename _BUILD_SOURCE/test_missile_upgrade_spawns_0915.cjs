const fs=require('fs'),path=require('path'),Module=require('module');
const ROOT=path.resolve(__dirname,'..');
const harness=fs.readFileSync(path.join(ROOT,'_BUILD_SOURCE/test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const test=`
const result=vm.runInContext(\`(()=>{
 const checks=[];const check=(v,n)=>{checks.push({name:n,ok:!!v});if(!v)throw Error(n);};
 powerups.length=0;run.missileTier='standard';run.missileUpgrade=null;run._missileWaveSerial=1;run.bombs=80;
 manualMissileObserveWave();
 check(run._missileWaveSerial===2,'authored wave advances the missile gate');
 check(powerups.length===1&&powerups[0].kind==='missileupbox_super','second ordinary wave offers the authored Super box');
 const superBox=powerups[0];applyPowerup(superBox);
 check(run.missileTier==='super'&&run.bombs===50,'Super box grants Super and enforces its ammo cap');
 check(run.missileUpgrade&&run.missileUpgrade.next==='ultra'&&!run.missileUpgrade.ready,'Ultra locks after Super acquisition');
 powerups.length=0;manualMissileObserveWave();
 check(run.missileUpgrade.ready&&powerups.length===1&&powerups[0].kind==='missileupbox_ultra','next survived wave unlocks and offers Ultra');
 const n=powerups.length;manualMissileSpawnWaveOffers();check(powerups.length===n,'an active tier box blocks duplicates');
 applyPowerup(powerups[0]);check(run.missileTier==='ultra'&&run.missileUpgrade.next==='uber'&&!run.missileUpgrade.ready,'Ultra grants and locks Uber');
 powerups.length=0;manualMissileObserveWave();check(powerups[0].kind==='missileupbox_uber','following survived wave offers Uber');
 applyPowerup(powerups[0]);check(run.missileTier==='uber'&&run.missileUpgrade===null,'Uber completes the tier chain');
 powerups.length=0;manualMissileSpawnWaveOffers();check(powerups.length===0,'max tier produces no extra upgrade box');
 manualMissileResetOnDeath(run);check(run.missileTier==='standard'&&run.missileUpgrade===null,'death resets upgrade progression');
 check(/p\._missileSeat&&p\._missileSeat!==_s/.test(updatePlay.toString()),'co-op tier boxes are seat-bound at collection');
 return {passed:checks.length,failed:0,checks};
})()\`,ctxv);console.log(JSON.stringify(result,null,2));`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;m._compile(boot+test,__filename);
