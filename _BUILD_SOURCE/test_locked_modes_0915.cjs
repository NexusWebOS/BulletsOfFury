const fs=require('fs'),path=require('path');
module.exports=function(vm,ctxv,ok){
  console.log('=== 310. Locked bonus mode presentation and gate ===');
  const roster=JSON.parse(vm.runInContext(`JSON.stringify(MODE_ITEMS.map(x=>({name:x.name,mode:x.mode,pill:x.pill,crop:x.crop||null,requiresFinalClear:!!x.requiresFinalClear})))`,ctxv));
  ok(roster.map(x=>x.name).join('|')==='CAMPAIGN|ARCADE|CO-OP|BOSS RUSH|TIME ATTACK','mode order includes Boss Rush and Time Attack after Co-op');
  ok(roster.slice(3).every(x=>x.requiresFinalClear&&x.crop&&x.crop.join(',')==='0,80,2125,555'),'bonus plates use the checker-free authored source crop');
  for(const file of ['boss_rush.png','time_attack.png','nexus_chains.webp'])ok(fs.existsSync(path.join(__dirname,'..','assets','game','ui','modes_0915',file)),'mode asset exists: '+file);
  const gate=JSON.parse(vm.runInContext(`(function(){
    var save={mode:run.mode,stage:run.stage,unlocked:bonusModesUnlocked,set:localStorage.setItem};var out={};
    try{
      bonusModesUnlocked=false;var writes=[];localStorage.setItem=function(k,v){writes.push([k,v]);};
      out.initialLocked=!modeItemUnlocked(MODE_ITEMS[3])&&!modeItemOpen(MODE_ITEMS[3]);
      run.mode='arcade';run.stage=CAMPAIGN_STAGES;out.arcadeRejected=!bonusModesUnlockFromCampaign()&&!bonusModesUnlocked;
      run.mode='campaign';run.stage=CAMPAIGN_STAGES-1;out.earlyRejected=!bonusModesUnlockFromCampaign()&&!bonusModesUnlocked;
      run.stage=CAMPAIGN_STAGES;out.finalAccepted=bonusModesUnlockFromCampaign()&&bonusModesUnlocked;
      out.persisted=writes.length===1&&writes[0][0]===BONUS_MODE_UNLOCK_KEY&&writes[0][1]==='1';
      out.revealed=modeItemUnlocked(MODE_ITEMS[3])&&!modeItemOpen(MODE_ITEMS[3]);
      out.routesDeferred=BONUS_MODE_PLAYABLE.bossrush===false&&BONUS_MODE_PLAYABLE.timeattack===false;
      return JSON.stringify(out);
    }finally{run.mode=save.mode;run.stage=save.stage;bonusModesUnlocked=save.unlocked;localStorage.setItem=save.set;}
  })()`,ctxv));
  for(const k of Object.keys(gate))ok(gate[k],'bonus mode gate: '+k);
  ok(vm.runInContext(`triggerVictory.toString().includes('bonusModesUnlockFromCampaign()')`,ctxv),'campaign victory path owns the persistent unlock');
  /* 0916: Mike removed the caption under every plate - a permanent label teaches nothing and
     crowds the art - so both refusal strings now live in modeLockedDeny, which arms the big
     typed banner the press actually answers. The lock layer itself is unchanged. */
  ok(vm.runInContext(`drawModeSelect.toString().includes('modeLockDraw(rect)')&&modeLockedDeny.toString().includes('MODE DEVELOPMENT IN PROGRESS')&&modeLockedDeny.toString().includes('CLEAR CAMPAIGN TO UNLOCK')&&drawModeSelect.toString().includes('modeDenyDraw(dt)')`,ctxv),'mode menu draws the exact lock layer and answers a locked press with the typed banner');
  const denial=JSON.parse(vm.runInContext(`(function(){var n=0,save=Audio.SFX.blocked;try{Audio.SFX.blocked=function(){n++;};bonusModesUnlocked=false;modeLockedDeny(MODE_ITEMS[3]);return JSON.stringify({sound:n===1,text:drawModeSelect._deny.text});}finally{Audio.SFX.blocked=save;}})()`,ctxv));
  ok(denial.sound&&denial.text==='CLEAR CAMPAIGN TO UNLOCK','locked confirmation emits an alert and explains the gate');
};
