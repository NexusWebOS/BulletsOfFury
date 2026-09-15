module.exports=function(vm,ctxv,ok){
  console.log('=== 304j. manual missile tier progression ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={bombs:run.bombs,tier:run.missileTier,upgrade:run.missileUpgrade,serial:run._missileWaveSerial,ml:run.missileLevel,dead:player.dead,stats:stageStats,special,coopOn,
      p2tier:run2.missileTier,p2upgrade:run2.missileUpgrade,p2serial:run2._missileWaveSerial,p2bombs:run2.bombs};
    const old=pBullets.slice(),o={};
    try{
      const specs=MANUAL_MISSILE_TIERS.map(q=>({id:q.id,damage:q.damage,size:q.size}));
      o.names=specs.map(q=>q.id).join(',')==='standard,super,ultra,uber';
      o.damage=specs.map(q=>q.damage).join(',')==='1,1.25,1.5625,1.953125';
      o.size=specs.map(q=>q.size).join(',')==='1,1.25,1.5625,1.953125';
      o.safeFallback=manualMissileSpec('unknown').id==='standard'&&manualMissileSpec(-20).id==='standard'&&manualMissileSpec(99).id==='uber';

      player.dead=false;retina.target=null;retina.phase=null;stageStats={missiles:0};
      const fired=[];
      for(const q of specs){pBullets.length=0;run.bombs=2;run.missileTier=q.id;useBomb(null);const b=pBullets[0];fired.push({kind:b.kind,dmg:b.dmg,w:b.w,h:b.h,tier:b.missileTier,scale:b._missileScale,auto:!!b._auto});}
      o.launches=fired.every((b,i)=>b.kind==='gmiss'&&b.tier===specs[i].id&&!b.auto);
      o.launchDamage=fired.every((b,i)=>b.dmg===24*specs[i].damage);
      o.launchSize=fired.every((b,i)=>b.w===10*specs[i].size&&b.h===18*specs[i].size&&b.scale===specs[i].size);
      o.ammo=fired.length===4&&run.bombs===1&&stageStats.missiles===4;

      pBullets.length=0;run.missileTier='uber';run.missileLevel=2;autoFireMissiles();
      o.passiveSeparate=pBullets.length===2&&pBullets.every(b=>b.kind==='missile'&&b._auto&&b.dmg===4&&b.w===10&&b.h===22&&b.missileTier===undefined);
      o.coopState=run2.missileTier==='standard'&&SEAT_RUN_FIELDS.includes('missileTier');
      o.renderScale=drawBullets.toString().includes("14*_gms")&&drawBullets.toString().includes("42*_gms")&&drawBullets.toString().includes("22*(b._missileScale||1)");

      o.caps=manualMissileAmmoCap('standard')===999&&manualMissileAmmoCap('super')===50&&manualMissileAmmoCap('ultra')===35&&manualMissileAmmoCap('uber')===20;
      const capped=[];for(const q of ['standard','super','ultra','uber']){run.missileTier=q;run.bombs=0;addManualMissiles(1000);capped.push(run.bombs);}
      o.pickupClamp=capped.join(',')==='999,50,35,20';
      run.missileTier='uber';run.bombs=999;pBullets.length=0;useBomb(null);o.fireClamp=run.bombs===19&&pBullets[0].missileTier==='uber';
      const ap=applyPowerup.toString();o.allPickupRoutes=ap.split('addManualMissiles(').length-1===5&&!ap.includes('run.bombs + _c.n');
      o.saveClamp=campSnapshot.toString().includes('bombs:clampManualMissiles(run.bombs)')&&campSnapshot.toString().includes('missileTier:manualMissileSpec(run.missileTier).id');
      o.loadClamp=campApply.toString().includes('run.missileTier=manualMissileSpec(s.missileTier).id')&&campApply.toString().includes('run.bombs=clampManualMissiles');
      o.rushClamp=startMissileRush.toString().includes('prevBombs:clampManualMissiles')&&updateMissileRush.toString().includes('run.bombs=clampManualMissiles');

      special=null;run.missileTier='standard';run.missileUpgrade=null;run._missileWaveSerial=10;run.bombs=80;
      applyPowerup({kind:'missileup_super',x:200,y:200});
      o.superPickup=run.missileTier==='super'&&run.bombs===50&&run.missileUpgrade.next==='ultra'&&!run.missileUpgrade.ready&&run.missileUpgrade.readyAfter===11;
      o.ultraBlocked=!manualMissileUpgradeCanSpawn('ultra')&&!manualMissileApplyUpgrade('ultra');
      coopOn=false;manualMissileObserveWave();o.ultraReady=run._missileWaveSerial===11&&manualMissileUpgradeCanSpawn('ultra');
      o.ultraPickup=manualMissileApplyUpgrade('ultra')&&run.missileTier==='ultra'&&run.bombs===35&&run.missileUpgrade.next==='uber'&&!run.missileUpgrade.ready;
      manualMissileObserveWave();o.uberReady=manualMissileUpgradeCanSpawn('uber');
      o.uberPickup=manualMissileApplyUpgrade('uber')&&run.missileTier==='uber'&&run.bombs===20&&run.missileUpgrade===null;
      o.noDuplicate=!manualMissileApplyUpgrade('uber')&&!manualMissileApplyUpgrade('super');
      manualMissileResetOnDeath();o.deathReset=run.missileTier==='standard'&&run.missileUpgrade===null&&run.bombs===20;

      run.missileTier='super';run.missileUpgrade={next:'ultra',ready:false,readyAfter:31};run._missileWaveSerial=30;
      run2.missileTier='ultra';run2.missileUpgrade={next:'uber',ready:false,readyAfter:8};run2._missileWaveSerial=7;coopOn=true;manualMissileObserveWave();
      o.coopWave=run._missileWaveSerial===31&&run.missileUpgrade.ready&&run2._missileWaveSerial===8&&run2.missileUpgrade.ready;
      o.schedulerHook=updatePlay.toString().includes("manualMissileObserveWave()");
      const cs=campSnapshot.toString(),ca=campApply.toString();o.lifecycleSave=cs.includes('missileUpgrade:')&&cs.includes('missileWaveSerial:')&&ca.includes('s.missileUpgrade')&&ca.includes('s.missileWaveSerial');
      return JSON.stringify(o);
    }finally{
      run.bombs=save.bombs;run.missileTier=save.tier;run.missileUpgrade=save.upgrade;run._missileWaveSerial=save.serial;run.missileLevel=save.ml;player.dead=save.dead;stageStats=save.stats;special=save.special;coopOn=save.coopOn;
      run2.missileTier=save.p2tier;run2.missileUpgrade=save.p2upgrade;run2._missileWaveSerial=save.p2serial;run2.bombs=save.p2bombs;
      pBullets.length=0;for(const b of old)pBullets.push(b);
    }
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Manual missile tiers: '+k);
  const src=require('fs').readFileSync(require('path').join(__dirname,'..','assets','game.js'),'utf8');
  ok(src.includes('run.power=0;manualMissileResetOnDeath(run);'),'Manual missile tiers: real death path resets the tier');
  return out;
};
