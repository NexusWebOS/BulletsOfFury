() => {
  run.mode='campaign';
  run.pilot='maverick';
  campaign.unlockedMax=8;
  openStageSelect(6,{boot:false});
  stateT=1;
  sselCursor=6;
  sselFlagsShown=9;
  sselBoot=0;
  sselUnlockCine=null;
  s9MapCine=null;
  window.sselCommitted=false;
  const p=sselFlagXY(6);
  sselShip={x:p.x,y:p.y,tx:p.x,ty:p.y,t:0,phase:'idle',bank:0,trail:0,head:0,moving:false};
  if(Audio&&Audio.SFX) Object.keys(Audio.SFX).forEach(k=>Audio.SFX[k]=()=>{});
  Input.injectTap('enter');
  campaignMenuInputTick();
  window.__qaCampaignMenu={
    state,
    boot:sselBoot,
    open:!!campPause,
    actions:CAMP_PAUSE_BTN.map(b=>b.act)
  };
}
