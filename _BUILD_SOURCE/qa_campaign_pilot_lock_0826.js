() => {
  run.mode='campaign';
  pilotIndex=0;
  pilotFrom=0;
  pilotRot=0;
  pilotPending=null;
  pilotComm=null;
  Input.mouse.x=VW/2;
  Input.mouse.y=VH*0.45;
  Input.mouse.down=true;
  drawPilot._entered=false;
  setState(GS.PILOT);

  drawPilot(1/60);
  stateT=0.6;
  Input.injectTap('enter');
  drawPilot(1/60);
  if(pilotInputArmed || pilotPending!=null || pilotRot>0)
    throw new Error('held Campaign input changed or launched the pilot');

  Input.mouse.down=false;
  drawPilot(1/60);                       // release arms, but does not act
  if(!pilotInputArmed || pilotPending!=null || pilotRot>0)
    throw new Error('release-to-arm did not settle cleanly');

  drawPilot(1/60);
  Input.injectTap('pad_right');
  drawPilot(1/60);
  if(pilotRot<=0 || pilotIndex!==1)
    throw new Error('fresh directional input was not accepted after release');

  pilotRot=0;
  pilotFrom=pilotIndex;
  drawPilot(1/60);                       // initialize the newly selected pilot's own card
  if(typeof pcSkip==='function') pcSkip();
  Input.injectTap('enter');
  drawPilot(1/60);
  if(pilotPending!==pilotIndex)
    throw new Error('fresh confirm was not accepted after release');
  if(SPECIAL_INFO.decker.name!=='CLOAKING SYSTEM' || PC_SPECIAL.decker.name!==SPECIAL_INFO.decker.name)
    throw new Error('Decker pilot metadata does not match his live cloaking special');

  window.__qaCampaignPilotLock={passed:true,index:pilotIndex};
  pilotPending=null;
  pilotSlide=0;
  pilotComm=null;
  pilotRot=0;
  stateT=1;
}
