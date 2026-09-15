module.exports=function(vm,ctxv,ok){
  console.log('=== 304i. shared no-one-shot enemy pools ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={enemies,boss,subBoss,bossActive,subBossActive,dmg:_dmgBullet,src:_dmgSrc,stats:stageStats,stage:run.stage,curStage};const o={};
    try{
      run.stage=1;curStage=STAGES[0];enemies=[];boss=null;subBoss=null;bossActive=false;subBossActive=false;
      stageStats={dmgDealt:0,hits:0,mslHits:0,spHits:0,spDmg:0,kills:0,wpn:{}};
      function foe(hp){return{x:210,y:160,w:28,h:28,hp:hp,maxhp:hp,dead:false,score:0,dropOk:false,type:'scout',flash:0};}

      let e=foe(1);enemies=[e];_dmgSrc='missile';_dmgBullet={kind:'gmiss',x:e.x,y:e.y};hitEnemy(e,999);
      o.onePointPromoted=e.hp===1&&e.maxhp===2&&!e.dead&&stageStats.dmgDealt===1;
      hitEnemy(e,999);o.secondImpactKills=!!e.dead&&e.hp===0&&stageStats.dmgDealt===2;

      e=foe(10);enemies=[e];stageStats.dmgDealt=0;_dmgBullet={kind:'beam',pierce:true,x:e.x,y:e.y};hitEnemy(e,999);
      o.beamFirstTick=e.hp===1&&!e.dead&&stageStats.dmgDealt===9;
      hitEnemy(e,999);o.beamLaterTick=!!e.dead&&stageStats.dmgDealt===10;

      e=foe(10);enemies=[e];stageStats.dmgDealt=0;_dmgBullet={kind:'mg',x:e.x,y:e.y};hitEnemy(e,3);hitEnemy(e,999);
      o.nonlethalFirstDoesNotGrantExtraLife=!!e.dead&&stageStats.dmgDealt===10;

      const a=foe(6),b=foe(6);enemies=[a,b];_dmgBullet={kind:'gmiss',x:a.x,y:a.y};hitEnemy(a,50);_dmgBullet.x=b.x;_dmgBullet.y=b.y;hitEnemy(b,50);
      o.perTarget=a.hp===1&&b.hp===1&&!a.dead&&!b.dead;

      e=foe(10);enemyShieldEquip(e,'bubble_hex',4,{once:true});e._esh.phase='active';enemies=[e];_dmgBullet={kind:'gmiss',x:e.x,y:e.y};hitEnemy(e,99);
      o.shieldFirst=e._esh.energy===1&&e._esh.phase==='active'&&e.hp===10;
      hitEnemy(e,99);o.shieldSecond=e._esh.energy===0&&e._esh.phase==='broken'&&e.hp===10;
      hitEnemy(e,99);o.hullBehindShield=e.hp===1&&!e.dead;

      const part={x:200,y:120,role:'helper',hp:1,maxhp:1,dead:false,flash:0,anim:0};xenoRegentPartDamage(part,500,null,true);
      o.componentFirst=part.hp===1&&part.maxhp===2&&!part.dead;
      xenoRegentPartDamage(part,500,null,true);o.componentSecond=part.dead&&part.hp===0;

      boss={x:240,y:120,w:120,h:100,hp:10,maxhp:10,dead:false,modular:true,_lastPart:null,
        parts:[{dmg:true,destroyed:false,hp:5,maxhp:5,dx:-20,dy:0,hw:20,hh:20},{dmg:true,destroyed:false,hp:5,maxhp:5,dx:20,dy:0,hw:20,hh:20}]};
      boss._lastPart=boss.parts[0];modularHit(500);o.modularFirst=boss.parts[0].hp===1&&!boss.parts[0].destroyed;
      modularHit(500);o.modularSecond=boss.parts[0].destroyed&&boss.parts[1].hp===5;

      e=foe(12);e._s3ice=true;enemies=[e];_dmgBullet={kind:'flame',_el:'fire',x:e.x,y:e.y};hitEnemy(e,8);
      o.elementalHighDamage=e.hp===1&&!e.dead;
      return JSON.stringify(o);
    }finally{enemies=save.enemies;boss=save.boss;subBoss=save.subBoss;bossActive=save.bossActive;subBossActive=save.subBossActive;_dmgBullet=save.dmg;_dmgSrc=save.src;stageStats=save.stats;run.stage=save.stage;curStage=save.curStage;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'No-one-shot rule: '+k);
  return out;
};
