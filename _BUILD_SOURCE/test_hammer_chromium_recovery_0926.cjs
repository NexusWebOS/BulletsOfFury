module.exports=function(vm,ctxv,ok){
  console.log('=== Chromium recovery: earned heal, core interruption and reconstruction (0926) ===');
  const results=JSON.parse(vm.runInContext(`(()=>{
    const save={boss,player,diffKey,DIFF,stage:run.stage,curStage,die:bossDie};const out={};
    function start(hp=350){boss={x:340,y:256,w:158,h:176,hp,maxhp:1000,flash:0,enter:false,dead:false,_noHit:false};hammerBossInit(boss);boss.enter=false;boss._noHit=false;boss.x=340;boss.y=256;boss._hammer.balance0922=true;hammerStormStart(boss);return boss._hammer;}
    try{
      run.stage=5;curStage=STAGES[4];player={x:240,y:410,invuln:999,dead:false};
      for(const d of ['normal','hard','furious']){
        diffKey=d;DIFF=DIFFS[d];let h=start(),R=h.recovery;
        out[d+' pending exactly 25 percent']=R.amount===250&&boss.hp===350&&R.applied===0;
        out[d+' charge hammer Retina target']=hammerWeaponTargetable(boss)&&retinaBossTargets(boss).some(q=>q._retinaId==='hammer');
        hammerBossTick(boss,1.25);out[d+' lightning starts empowerment']=h.empowered&&h.charged&&boss.hp===350;
        hammerBossTick(boss,1);out[d+' heal grows gradually']=boss.hp>350&&boss.hp<400&&R.status==='charging';
        boss.hp-=25;const accrued=R.applied;boss._hammerModuleHit='hammer';const bodyDamage=hammerBossDamage(boss,R.coreHP);
        out[d+' core break revokes all heal']=bodyDamage===0&&Math.abs(boss.hp-325)<1e-7&&R.revoked===accrued&&R.applied===0&&R.status==='cancelled';
        out[d+' immediate stun and no hammer target']=h.state==='storm_stun'&&h.hammerDestroyed&&!hammerWeaponTargetable(boss)&&!retinaBossTargets(boss).some(q=>q._retinaId==='hammer');
        out[d+' stun rewards body damage']=hammerBossDamage(boss,3)===6;
        hammerBossTick(boss,4);out[d+' stun enters visible rebuild']=h.state==='storm_rebuild'&&h.hammerDestroyed&&boss.hp===325;
        hammerBossTick(boss,2.4);out[d+' rebuilt without retrying heal']=h.state==='storm_idle'&&h.empowered&&h.charged&&!h.hammerDestroyed&&h.hammerHP===h.hammerMax&&boss.hp===325&&R.status==='cancelled';
        h=start();R=h.recovery;hammerBossTick(boss,1.25);hammerBossTick(boss,2);boss.hp-=35;hammerBossTick(boss,4);
        out[d+' completion adds only budget less body damage']=R.status==='complete'&&Math.abs(boss.hp-565)<1e-7&&R.applied===250;
        hammerBossTick(boss,.56);out[d+' successful charge resumes storm']=h.state==='storm_idle'&&h.empowerLevel===1&&h.empowered;
      }
      const h=start(950);hammerBossTick(boss,1.25);hammerBossTick(boss,6);out['healing caps at maximum']=boss.hp===1000&&h.recovery.applied===50;
      const low=start(10);hammerBossTick(boss,1.25);hammerBossTick(boss,1);boss.hp-=30;let deaths=0;bossDie=()=>{deaths++;boss.dead=true;};boss._hammerModuleHit='hammer';hammerBossDamage(boss,low.recovery.coreHP);
      out['revoking temporary health can finish boss']=deaths===1&&boss.dead&&boss.hp===0;
      return JSON.stringify(out);
    }finally{boss=save.boss;player=save.player;diffKey=save.diffKey;DIFF=save.DIFF;run.stage=save.stage;curStage=save.curStage;bossDie=save.die;}
  })()`,ctxv));
  for(const [name,value] of Object.entries(results))ok(value,'Chromium recovery: '+name);
};
