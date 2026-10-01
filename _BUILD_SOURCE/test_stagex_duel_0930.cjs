module.exports=function(vm,ctxv,ok){
 /* 0930 - found filming the v9 trailer's STAGE X shot. Rival24's deploy runs a rival duel on stage 6's neutral
    encounter setup and nulls s6Opening on purpose ("entering the destination stage outright would replay its story
    dialogue and scripted hazards over this optional duel"), and drawLaunch then re-initialised it: the whole stage-6
    opening - the cloaked lock-on with its ~26 s input lock, its radio, its stealth fighters - replayed over the duel,
    and the two radios typing at once re-ticked every visible letter each frame (16,987 letter blips in one 40 s take;
    504 after the fix). Behaviour only: the duel is deployed through Rival24's own map and ally-select input, the way
    the campaign map reaches it (probe_stagex_water_0928.py's sequence). */
 console.log('=== 380. Stage X: a rival duel does not replay the stage-6 opening ===');
 const r=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};
  diffKey='normal';DIFF=DIFFS.normal;coopOn=false;
  /* control: an ordinary stage-6 start still opens on its scripted opening */
  run.mode='arcade';run.pilot='cole';Rival24.reset();
  beginStage(6);s6Opening=null;setState(GS.LAUNCH);drawLaunch(1/60);
  o.control=!!s6Opening&&s6Opening.phase==='cloak';
  o.controlLocked=s6OpeningControlsLocked();
  /* the duel, deployed through the map and the ally select */
  run.mode='campaign';run.pilot='cole';campaign.unlockedMax=8;campaign.rivalScattered=true;
  campaign.rivalDefeated=[false,false,false,false,false];sselBoot=0;stateT=2;Input.clearTaps();
  Input.injectTap('arrowdown');Rival24.mapInput();Input.injectTap('enter');Rival24.mapInput();
  Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('arrowright');Rival24.selectDraw(.1);
  Input.injectTap('enter');Rival24.selectDraw(.1);Input.injectTap('enter');Rival24.selectDraw(.1);
  o.deployed=!!Rival24.active&&run.stage===6&&!!(boss&&boss._rebels);
  o.nulledByDeploy=s6Opening===null;
  /* the vm's stub canvas has no createImageData, so the WORLD draw inside drawLaunch throws on the rival art;
     the s6Opening decision is made before that draw, which is the only thing under test here */
  o.drawThrew=false;try{setState(GS.LAUNCH);drawLaunch(1/60);}catch(e){o.drawThrew=String(e&&e.message||e);}
  o.afterLaunch=s6Opening===null;
  o.unlocked=!s6OpeningControlsLocked();
  for(let i=0;i<30;i++){try{updatePlay(1/60);}catch(e){}}
  o.stillNull=s6Opening===null;
  Rival24.reset();
  return o;
 })())`,ctxv));
 ok(r.control,'control: an ordinary stage-6 launch still starts the scripted opening (cloak phase)');
 ok(r.controlLocked,'control: ... with its cloaked lock-on input lock');
 ok(r.deployed,'the Stage X duel deploys through the map and the ally select (Rival24 active, stage 6, the rebel rig)');
 ok(r.nulledByDeploy,"Rival24's deploy leaves s6Opening null, as it intends");
 ok(r.afterLaunch,'drawLaunch does not re-initialise the stage-6 opening over a live rival duel');
 ok(r.unlocked,'... so the duel does not inherit the opening input lock');
 ok(r.stillNull,'half a second of the duel later, still no stage-6 opening');
};
