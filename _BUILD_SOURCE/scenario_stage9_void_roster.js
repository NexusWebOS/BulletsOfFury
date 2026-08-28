async () => {
  beginStage(9); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  player.x=worldWidth()/2; player.y=VH-55; snapCamToPlayer(); gravityModeStart(); gravityMode.phase='active';
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  stagePlan=[]; waveIdx=999; subBossTriggered=true; subBossDone=true; bossWarned=true;
  const rows=[
    ['horizon',worldWidth()*0.25,105],['pmine',worldWidth()*0.50,105],['dreadv',worldWidth()*0.75,118],
    ['riftrock',worldWidth()*0.25,285],['vmanta',worldWidth()*0.50,275],['riftrocksm',worldWidth()*0.75,290]
  ];
  rows.forEach((r,i)=>{ const e=spawnEnemy(r[0],r[1],r[2],{}); if(e){e.x=r[1];e.y=r[2];e._s9x0=r[1];e._s9y0=r[2];e._s9fire=0.9+i*0.1;} });
  const keys=['nst9_voidwater_master','ngm_space_atlas','ns9x_horizon_0','ns9x_dreadv','ns9fx_water_3',
    'nes_violet_b_3','nes_violet_f_3','nes_prism_3'];
  await new Promise(resolve=>{ const until=performance.now()+20000; const poll=()=>{
    if(keys.every(k=>XART.rdy(k))||performance.now()>until)resolve();else setTimeout(poll,50);
  };poll(); });
}
