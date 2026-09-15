module.exports=function(vm,ctxv,ok){
  console.log('=== 315. Furnace Tyrant accelerating rollerball ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    var save={boss:boss,bossActive:bossActive,run:{stage:run.stage},curStage:curStage,diffKey:diffKey,DIFF:DIFF,
      warn:combatWarningTick,sfx:fztSfx,hit:playerHit,px:player.x,py:player.y,pdead:player.dead,pinv:player.invuln};var o={};
    try{
      run.stage=2;curStage=STAGES[1];diffKey='normal';DIFF=DIFFS.normal;player.x=130;player.y=390;player.dead=false;player.invuln=0;
      var warns=0,sounds=[],hits=0;combatWarningTick=function(owner,id,elapsed,dur){if(id==='furnace-rollerball'&&dur===1.45)warns++;};
      fztSfx=function(n){sounds.push(n);};playerHit=function(){if(player.invuln>0)return;hits++;player.invuln=60;};
      spawnBoss('infernoreaver');furnaceSync(boss);var F=boss._fz;
      F.phase='core';F.trans=0;F.attack='rollerball';F.idx=2;F.at=0;F.startX=boss.x;F.rollY=null;F.rollLeg=-1;boss.enter=false;boss.dead=false;
      var dt=1/120,lastX=boss.x,lastA=F.a,peaks=[0,0,0,0,0,0],spinEarly=0,spinLate=0,lockedY=null,range=[1e9,-1e9],guard=0;
      while(guard++<1300&&F.attack==='rollerball'){
        if(F.at>1.5&&hits===0){player.x=boss.x;player.y=boss.y;player.invuln=0;}else if(F.at<1.3){player.y=260;}
        var prevLeg=F.rollLeg;furnaceTick(boss,dt);range[0]=Math.min(range[0],boss.x);range[1]=Math.max(range[1],boss.x);
        if(lockedY==null&&F.rollY!=null)lockedY=F.rollY;
        if(F.rollLive&&F.rollLeg>=0){var v=Math.abs(boss.x-lastX)/dt,spin=Math.abs(F.a-lastA)/dt;peaks[F.rollLeg]=Math.max(peaks[F.rollLeg],v);if(F.rollLeg===0)spinEarly=Math.max(spinEarly,spin);if(F.rollLeg===5)spinLate=Math.max(spinLate,spin);}
        lastX=boss.x;lastA=F.a;
      }
      o.warning=warns>100&&lockedY!=null;
      o.laneLocks=Math.abs(lockedY-260)<1&&Math.abs(F.rollY||0)<1;
      o.sixPasses=F.rollLeg===-1&&sounds.filter(function(n){return n==='whip';}).length===6;
      o.travelAccelerates=peaks.every(function(v){return v>0;})&&peaks[5]>peaks[0]*2.4&&peaks[3]>peaks[1]*1.25;
      o.spinAccelerates=spinLate>spinEarly*2;
      o.fullWidth=range[0]<120&&range[1]>360;
      o.contactHurts=hits===1;
      o.handsOff=F.attack==='rotor'&&Math.abs(F.a)<.001&&guard<1300;
      o.sound=sounds[0]==='bossWeaponCharge'&&sounds.indexOf('whip')>=0;
      return JSON.stringify(o);
    }finally{boss=save.boss;bossActive=save.bossActive;run.stage=save.run.stage;curStage=save.curStage;diffKey=save.diffKey;DIFF=save.DIFF;
      combatWarningTick=save.warn;fztSfx=save.sfx;playerHit=save.hit;player.x=save.px;player.y=save.py;player.dead=save.pdead;player.invuln=save.pinv;}
  })()`,ctxv));
  for(const k of Object.keys(q))ok(q[k],'Furnace rollerball: '+k);
  ok(vm.runInContext(`FZT_ATTACKS.core.indexOf('rollerball')===2&&furnaceCombat.toString().includes("F.rollLive=true")`,ctxv),'rollerball is a live Furnace core attack with a bounded danger phase');
};
