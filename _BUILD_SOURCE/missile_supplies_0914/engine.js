/* Mike 0914: authored missile supplies remain available throughout encounters.
 * Stage 1-7: x5/x10/x20. Stage 8: x50/x100.
 * Old x2 packs migrate to x5; tier upgrades require approved SpriteCook art.
 * Fodder alone may scatter one or two collectible missile projectiles.
 */
function bossMissileSupplyTick(dt){
  if(player.dead)return;
  const targets=[];
  if(bossActive&&boss)targets.push(boss);
  if(subBossActive&&subBoss)targets.push(subBoss);
  for(const e of enemies)if(e._amini&&!e.dead)targets.push(e);
  for(const b of targets){
    if(b.dead||b.hp<=0||b.enter||b._dyingT!=null)continue;
    if(b._rzb&&b._rzb.state==='arrival')continue;
    const B=b._missileSupply||(b._missileSupply={t:0,due:7});
    B.t+=dt;
    if(B.t<B.due||powerups.some(p=>!p.dead&&(p.kind==='mcrate'||/^missilepack/.test(p.kind))))continue;
    const bonus=diffKey==='hard'||diffKey==='furious'?1.25:1;
    B.t=0;B.due=18/bonus;
    powerups.push({x:clamp(player.x,camLeftX()+36,camRightX()-36),y:-30,vy:.85,t:0,kind:'mcrate',
      hp:6,flash:0,w:48,h:44,bob:0,_pack:mslPackRoll(),_bossSupply:true});
    if(typeof stageStats!=='undefined')stageStats.pickupsSeen++;
  }
}
function scatterMissilePickups(x,y,n){
  for(let i=0;i<n;i++)powerups.push({x:x+(i-(n-1)/2)*12,y,vy:.80,t:0,kind:'bomb',
    w:26,h:26,bob:i*Math.PI,_looseMissile:true,_scatterVx:n===2?(i?65:-65):0,
    _missileArt:pilotMissileKey(false)});
  if(typeof stageStats!=='undefined')stageStats.pickupsSeen+=n;
}
function enemyMissileDrop(e){
  if(!e||e._ammoDropChecked)return;
  e._ammoDropChecked=true;
  if(e._boss||e._amini||e.mini||e._mini||e._sub||e.sub||e.modular||e._prop||
     e.prop||e._waterRock||e._crate||e._destruct||e.crate||e===boss||e===subBoss||
     enemies.indexOf(e)<0)return;
  const bonus=diffKey==='hard'||diffKey==='furious'?1.25:1;
  if(Math.random()>=.10*bonus)return;
  scatterMissilePickups(e.x,e.y,Math.random()<.25?2:1);
}
function looseMissilePickupDraw(p){
  if(!p._looseMissile)return false;
  const key=p._missileArt||pilotMissileKey(false);
  if(!XART.rdy(key))return true;
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.t*3.2);
  drawMfx(key,0,0,0,18,null,1,null);ctx.restore();return true;
}
