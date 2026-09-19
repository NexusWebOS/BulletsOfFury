module.exports=function(vm,ctxv,ok){
  console.log('=== 304c. shared elemental damage rules ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={boss,subBoss,bossActive,subBossActive,enemies,dmg:_dmgBullet,src:_dmgSrc,stage:run.stage,timer:stageTimer,floaters,stats:stageStats};const o={};
    try{
      boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];floaters=[];stageStats={dmgDealt:0,hits:0,mslHits:0,spHits:0,spDmg:0,wpn:{}};_dmgSrc=null;
      run.stage=2;stageTimer=10;_dmgBullet={kind:'flame',_el:'fire'};
      let e={x:100,y:100,w:40,h:40,hp:100,maxhp:100,dead:false,_volc:true};hitEnemy(e,20);
      o.fireHalf=e.hp===90&&stageStats.dmgDealt===10;
      o.fireText=floaters.length===1&&floaters[0].txt==='FIRE DMG ABSORBED!';
      hitEnemy(e,20);o.throttle=floaters.length===1&&e.hp===80;
      stageTimer+=.56;hitEnemy(e,20);o.repeat=floaters.length===2&&e.hp===70;

      run.stage=3;stageTimer=20;floaters=[];_dmgBullet={kind:'iceorb',_el:'ice'};
      e={x:120,y:120,w:40,h:40,hp:100,maxhp:100,dead:false,_s3ice:true};hitEnemy(e,18);
      o.iceHalf=e.hp===91;o.iceText=floaters.length===1&&floaters[0].txt==='ICE DMG ABSORBED!';

      run.stage=2;floaters=[];_dmgBullet={kind:'iceorb',_el:'ice'};
      e={x:140,y:120,w:40,h:40,hp:100,maxhp:100,dead:false,_volc:true};hitEnemy(e,20);
      o.iceOnFireDouble=e.hp===70&&e._hitFlashColor==='#83d9ff'&&floaters.length===0;

      run.stage=3;_dmgBullet={kind:'flame',_el:'fire'};
      e={x:145,y:120,w:40,h:40,hp:100,maxhp:100,dead:false,_s3ice:true};hitEnemy(e,20);
      o.fireOnIceDouble=e.hp===70&&e._hitFlashColor==='#ff3b30'&&floaters.length===0;

      run.stage=2;_dmgBullet={kind:'iceorb',_el:'ice',x:160,y:120};
      e={x:160,y:120,w:40,h:40,hp:100,maxhp:100,dead:false,_volc:true,
        _esh:{family:'bubble_hex',kind:'bubble',once:false,energy:100,max:100,drawScale:2.5,breakDelay:1.4,regen:.07,phase:'active',animT:0,hitT:0,sinceHit:99,breakT:0,impactCd:1}};
      hitEnemy(e,20);o.shieldDouble=e.hp===100&&e._esh.energy===70;

      const oldPilot=run.pilot;run.pilot='freezer';_dmgBullet={kind:'flame',_el:'ice'};
      e={x:150,y:120,w:40,h:40,hp:100,maxhp:100,dead:false,_volc:true};hitEnemy(e,40);
      o.freezerNoQuad=e.hp===60;run.pilot=oldPilot;

      _dmgBullet={kind:'flame',_el:'fire'};boss={x:240,y:140,w:100,h:100,hp:200,maxhp:200,dead:false,enter:false,_volc:true};bossActive=true;_lastHitX=boss.x;_lastHitY=boss.y;hitBoss(20);
      o.bossHalf=boss.hp===190;
      boss=null;bossActive=false;subBoss={x:240,y:140,w:100,h:100,hp:200,maxhp:200,dead:false,enter:false,_volc:true};subBossActive=true;hitSubBoss(20,subBoss.x,subBoss.y);
      o.subBossHalf=subBoss.hp===190;

      run.stage=8;boss=subBoss;subBoss=null;subBossActive=false;bossActive=true;boss.hp=200;boss.dead=false;_lastHitX=boss.x;_lastHitY=boss.y;hitBoss(20);
      o.stage8Exempt=boss.hp===180;
      return JSON.stringify(o);
    }finally{boss=save.boss;subBoss=save.subBoss;bossActive=save.bossActive;subBossActive=save.subBossActive;enemies=save.enemies;_dmgBullet=save.dmg;_dmgSrc=save.src;run.stage=save.stage;stageTimer=save.timer;floaters=save.floaters;stageStats=save.stats;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Shared elemental damage: '+k);
  return out;
};
