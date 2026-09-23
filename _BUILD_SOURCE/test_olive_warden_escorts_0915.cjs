module.exports=function(vm,ctxv,ok){
  console.log('=== 323. Olive Warden difficulty escorts ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={sub:subBoss,active:subBossActive,runStage:run.stage,curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      bullets:eBullets,pb:pBullets,en:enemies,plan:stagePlan,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    function spawn(k){run.stage=4;curStage=STAGES[3];diffKey=k;DIFF=DIFFS[k];stagePlan=[];enemies=[];pBullets=[];eBullets=[];
      player.x=worldWidth()*.42;player.y=610;player.dead=false;player.invuln=999;spawnSubBoss('olivewarden');var b=subBoss;
      b.enter=false;b.x=worldWidth()/2;b.y=b._s4war.homeY;b._drawY=b.y;b.fireCd=999;subBossActive=true;return b;}
    try{
      var b=spawn('normal'),S=b._s4war;for(var i=0;i<90;i++)stage4MiniDirector(b,1/60);o.normalSolo=S.drones.length===0&&!S.summoned;
      b=spawn('hard');S=b._s4war;var maxProtectTravel=0;for(i=0;i<210;i++){if(i===105)player.x=worldWidth()*.70;stage4MiniDirector(b,1/60);
        var liveProtect=S.drones.find(d=>d.role==='protector');if(liveProtect)maxProtectTravel=Math.max(maxProtectTravel,Math.abs(liveProtect.x-liveProtect.stationX));}
      var roles=S.drones.map(d=>d.role),gun=S.drones.find(d=>d.role==='gunner'),protect=S.drones.find(d=>d.role==='protector');
      o.hardPair=S.drones.length===2&&roles.filter(x=>x==='gunner').length===1&&roles.filter(x=>x==='protector').length===1;
      o.authored=S.drones.every(d=>['s4w_warden_gunner_0919','s4w_warden_rocketeer_0919'].includes(d.art)&&d.active>=.99);
      o.noShieldEffects=S.drones.every(d=>d.shield===0&&d.maxShield===0&&d.hp===d.maxhp);
      o.mountedGunner=eBullets.some(x=>x._s4EscortRole==='gunner'&&x._s4wKind==='machine')&&gun.shots>=5;
      o.missileProtector=eBullets.some(x=>x._s4EscortRole==='protector'&&x._shootable&&x._s4wKind==='rocket')&&protect.shots>=1;
      o.evasiveProtector=maxProtectTravel>30&&stage4MiniDroneAt(b,protect.x,protect.y,2)===protect;
      o.exposedGunner=Math.abs(gun.x-b.x)>(b.w+gun.size)*.4||Math.abs(gun.y-b.y)>(b.h+gun.size)*.4;
      var hp=gun.hp;stage4MiniDroneDamage(b,gun,5);o.hullTakesDamage=gun.hp<hp&&gun.shield===0;
      o.hittable=stage4MiniDroneAt(b,gun.x,gun.y,2)===gun;
      o.planContinues=/^hard/.test(S.mode)||S.miniHard||['burst','center','rockets'].includes(S.mode);
      b=spawn('furious');S=b._s4war;for(i=0;i<170;i++)stage4MiniDirector(b,1/60);
      o.furiousPair=S.drones.length===2&&S.drones.filter(d=>d.role==='gunner').length===1&&S.drones.filter(d=>d.role==='protector').length===1&&S.summoned;
      o.furiousPressure=S.drones.every(d=>d.shots>0);
      o.noPostStageHoming=eBullets.filter(x=>x._s4EscortRole==='protector').every(x=>!x.homing);
      return JSON.stringify(o);
    }finally{subBoss=save.sub;subBossActive=save.active;run.stage=save.runStage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      eBullets=save.bullets;pBullets=save.pb;enemies=save.en;stagePlan=save.plan;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Olive Warden escorts: '+k);
};
