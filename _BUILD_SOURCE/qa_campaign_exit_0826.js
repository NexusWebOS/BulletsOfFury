() => {
  run.mode='campaign';
  run.pilot='maverick';
  campaign.unlockedMax=8;
  openStageSelect(6,{boot:true});
  stateT=1;
  sselUnlockCine=null;
  s9MapCine=null;
  window.sselCommitted=false;

  Input.injectTap('k');
  campaignMenuInputTick();
  const escaped=menuBackTick();
  if(escaped || state!==GS.STAGESEL) throw new Error('campaign back escaped the booting map');

  Input.injectTap('enter');
  campaignMenuInputTick();
  if(campPause) throw new Error('campaign menu opened before map boot completed');

  sselBoot=0;
  Input.injectTap('enter');
  campaignMenuInputTick();
  if(!campPause || CAMP_PAUSE_BTN.map(b=>b.act).join(',')!=='save,load,exit')
    throw new Error('live campaign map did not open the three-action menu');

  const music=[];
  const oldStart=Audio.startMusic;
  Audio.startMusic=n=>music.push(n);
  campPause.sel=2;
  campPause.t=1;
  Input.injectTap('enter');
  campPauseDraw(1/60);
  Audio.startMusic=oldStart;

  if(state!==GS.TITLE || run.mode!=='arcade')
    throw new Error('Exit Game did not return directly to the main screen');
  if(!music.includes('title'))
    throw new Error('Exit Game did not restore the main-menu music');
  window.__qaCampaignExit={state,mode:run.mode,music,passed:true};
}
