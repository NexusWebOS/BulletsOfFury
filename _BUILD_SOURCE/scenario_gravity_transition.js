async () => {
  const s=(run&&run.stage===5)?5:9;
  beginStage(s); player.reset(); player.invuln=1e9;
  player.x=worldWidth()/2; player.y=VH-55; snapCamToPlayer();
  const keys=['ngm_space_atlas'];
  if(s===9)keys.push('nst9_voidwater_master');
  await new Promise(resolve=>{ const until=performance.now()+20000; const poll=()=>{
    if(keys.every(k=>XART.rdy(k))||performance.now()>until)resolve();else setTimeout(poll,50);
  };poll(); });
  setState(GS.LAUNCH); gravityModeReset();
  drawLaunch._phase='settle'; drawLaunch._pt=0.43; drawLaunch._lastT=0;
  drawLaunch._dist=SEG_B3+1800; drawLaunch._spd=LAUNCH_COUNTDOWN_SCROLL;
  drawLaunch._bgScroll=SEG_B3+1800; drawLaunch._mus=true; drawLaunch._go=false; drawLaunch._num=99;
}
