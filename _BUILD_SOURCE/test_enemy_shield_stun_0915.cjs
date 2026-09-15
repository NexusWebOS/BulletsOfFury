module.exports=function(vm,ctxv,ok){
  console.log('=== 304d. shared enemy shield break stun ===');
  const out=JSON.parse(vm.runInContext(`(function(){
    const save={enemies,dmg:_dmgBullet,stage:run.stage,floaters,fx:enemyShieldFx,stats:stageStats};const o={};
    try{
      run.stage=2;floaters=[];enemyShieldFx=[];stageStats={dmgDealt:0,hits:0,mslHits:0,spHits:0,spDmg:0,wpn:{}};
      const src={type:'disc',x:240,y:170,w:48,h:44,hp:100,maxhp:100,dead:false,flash:0,_order:1};
      enemyShieldEquip(src,'bubble_hex',10,{once:true,drawScale:2.55});src._esh.phase='active';src._esh.impactCd=1;
      const ring=[];for(let i=0;i<8;i++)ring.push({type:'eye',x:240+Math.cos(i*TAU/8)*60,y:170+Math.sin(i*TAU/8)*60,w:36,h:36,hp:100,maxhp:100,dead:false,flash:0});
      const far={type:'eye',x:430,y:390,w:36,h:36,hp:100,maxhp:100,dead:false,flash:0};enemies=[src].concat(ring,[far]);
      _dmgBullet={kind:'lzslug',x:src.x,y:src.y,vx:0,vy:-8};hitEnemy(src,10);hitEnemy(src,10);
      o.shieldAbsorbs=src.hp===100&&src._esh.energy===0&&src._esh.phase==='broken';
      o.stunStarts=!!src._eshStun&&!src._frenzy&&src._eshStun.dur===ENEMY_SHIELD_STUN_DUR;
      const hurt=ring.filter(q=>q.hp<100);o.boundedSplash=hurt.length===ENEMY_SHIELD_SPLASH_CAP&&hurt.every(q=>q.hp>=84)&&far.hp===100;
      o.breakFx=enemyShieldFx.length>=4&&floaters.some(f=>f.txt==='SHIELD BREAK!');
      const y0=src.y;enemyShieldStunTick(src,ENEMY_SHIELD_STUN_DUR*.5);
      o.dizzyPose=src.y<y0&&Math.abs(src._eshStun.angle)>2;
      enemyShieldStunTick(src,ENEMY_SHIELD_STUN_DUR*.51);
      o.restore=src.y===y0&&!src._eshStun&&src._frenzy===1;
      const chain={type:'disc',x:100,y:100,w:40,h:40,hp:100,maxhp:100,dead:false,flash:0};enemyShieldEquip(chain,'bubble_hex',2,{once:true});chain._esh.phase='active';
      const witness={type:'eye',x:106,y:100,w:36,h:36,hp:100,maxhp:100,dead:false,flash:0};enemies=[chain,witness];
      _dmgBullet={kind:'shieldbreak',_shieldSplash:true,x:100,y:100,pierce:true};hitEnemy(chain,3);hitEnemy(chain,3);
      o.noChain=chain._esh.phase==='broken'&&!!chain._eshStun&&witness.hp===100;
      o.authoredOrbit=enemyShieldStunDraw.toString().includes("'nes_hit_'");
      return JSON.stringify(o);
    }finally{enemies=save.enemies;_dmgBullet=save.dmg;run.stage=save.stage;floaters=save.floaters;enemyShieldFx=save.fx;stageStats=save.stats;}
  })()`,ctxv));
  for(const k of Object.keys(out))ok(out[k],'Enemy shield break stun: '+k);
  return out;
};
