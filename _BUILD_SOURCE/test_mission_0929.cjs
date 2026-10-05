module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof MISSION29_ART',ctxv)==='undefined')for(const f of ['mission_art_0929.js','mission_repair_0929.js'])
  vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== September 29: campaign ownership, comms, live jet gates, portal and authored laser reels ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};ht27Stop();debugFight=null;coopOn=false;diffKey='normal';DIFF=DIFFS.normal;
 const owned=achievementState.owned;achievementState.owned={forge_element_fire_E:{at:1},forge_element_ice_E:{at:1},forge_dark_3_C:{at:1}};
 run.mode='campaign';run.pilot='cole';run.infusion={elem:'ice',lv:4};run.forgeElems={fire:1,ice:1};run.forge={3:{elem:'ice',lv:1}};run.forgeForms={3:{ice:{elem:'ice',lv:1}}};run._chainSeeded=true;run._stageElements=['dark'];run.ngplus=true;chaingunUnlocked=true;laserMistUnlocked=true;
 yuriLightningOrbUnlocked=true;pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(1);
 o['fresh campaign imports no elements, recipes, aura, rewards, NG+ or weapon seed']=forgeDiscovered().length===0&&Object.keys(ensureForgeForms()).length===0&&!run.infusion&&!run._stageElements.length&&!run.ngplus&&!run._chainSeeded;
 o['profile unlocks cannot activate campaign combinations, mist, chaingun or Yuri orb']=!forgeComboOwned('dark',3)&&!laserMistIsUnlocked()&&!chaingunIsUnlocked()&&!yuriLightningOrbIsUnlocked()&&run._chainLightningLevel===1;
 o['an unearned combination cannot be crafted or selected']=forgeCombine(3,'ice')==='locked'&&forgeSelect(3,'ice')==='locked';
 forgeComboGrant('kinetic',0);run.forgeCombos=2;o['only a collected element enters the fresh campaign Forge']=forgeDiscovered().join()==='kinetic'&&forgeCombine(3,'kinetic')==='ok';
 chaingunUnlock();laserMistUnlock();const saved=campSnapshot();run.forgeElems={fire:1};run._earnedUnlocks={};campApply(saved);
 o['save restores campaign-earned elements, form and weapon unlocks']=forgeDiscovered().join()==='kinetic'&&!!forgeFormsFor(3).kinetic&&chaingunIsUnlocked()&&laserMistIsUnlocked();
 const legacy={...saved};delete legacy.earnedUnlocks;legacy.rank={};campApply(legacy);
 o['legacy slot with no completed stages cannot inherit global weapon unlocks']=!chaingunIsUnlocked()&&!laserMistIsUnlocked();
 run.pilot='yuri';yuriLightningOrbGrantStage4();o['Yuri must earn his Stage 4 orb again in this campaign']=yuriLightningOrbIsUnlocked()&&run._earnedUnlocks.lightningOrb;
 run.pilot='cole';run._earnedUnlocks={};coopOn=true;run2.pilot='yuri';run2._earnedUnlocks={};yuriLightningOrbGrantStage4();let p2Orb=false;withSeat(2,()=>{p2Orb=yuriLightningOrbIsUnlocked();});o['Yuri in co-op seat 2 retains the campaign-earned orb gate']=p2Orb;coopOn=false;
 run.mode='arcade';run.forgeElems={};run.forge={};run.forgeForms={};run.ngplus=true;
 o['arcade preserves purchased recipes without importing all prior-run elements']=!forgeDiscovered().includes('fire')&&!!forgeFormsFor(3).dark;achievementState.owned=owned;
 run.pilot='cole';o['Cole solo warning comes from Decker']=missionRadioWho('DECKER')==='DECKER'&&missionRadioWho('COLE')==='DECKER';
 run.pilot='decker';o['Decker solo warning comes from Cole']=missionRadioWho('DECKER')==='COLE';
 run.pilot='maverick';o['Maverick solo does not make Decker ask himself about cloaking']=missionRadioWho('MAVERICK')==='COLE';run.pilot='decker';
 coopOn=true;run2.pilot='cole';o['Decker and Cole co-op may both speak']=missionRadioWho('DECKER')==='DECKER'&&missionRadioWho('COLE')==='COLE';coopOn=false;
 for(const diff of ['normal','hard','furious']){
  diffKey=diff;DIFF=DIFFS[diff];beginStage(6);setState(GS.PLAY);story=null;enemies=[];eBullets=[];groundTargetingReset();
  const O=missionAssaultStart(),n=O.n,side=O.events.filter(q=>q.kind==='lane'&&q.direction!=='south'),bomb=O.events.filter(q=>q.kind==='bomb'),south=O.events.filter(q=>q.direction==='south');
  o[diff+' side gates start right then left and leave a safe row']=side[0].direction==='west'&&side.some(q=>q.direction==='east')&&side.filter(q=>q.direction==='west').length===(n===0?3:4);
  o[diff+' bombing passes begin on the left and have no zone entries']=bomb[0].direction==='east'&&bomb.some(q=>q.direction==='west')&&bomb.every(q=>q.kind==='bomb');
  o[diff+' descending gates scale simultaneous pressure and weapons']=south.length===[3,8,15][n]&&south.every(q=>n===2||q.attack===null);
  const e=missionJetSpawn(south[0],O);e.x=worldWidth()/2;e.y=viewTopY()+85;const sx=e.x,sy=e.y;s6StrikeTick(e,.1);
  o[diff+' jets use straight committed movement at the intended speed']=e.x===sx&&Math.abs(e.y-sy-[350,455,570][n]*.1)<.001;
  if(n<2)o[diff+' southbound gate jets remain gun-free']=eBullets.length===0&&groundTargetingFx.length===0;
  const crossing=missionJetSpawn(side[0],O);crossing.x=worldWidth()/2;crossing.y=VH*.4;s6StrikeTick(crossing,.1);
  o[diff+' sideways gates now drop warned bombs']=groundTargetingFx.some(q=>q._mission29&&!q.track);
  const jet=missionJetSpawn(bomb[0],O);jet.x=worldWidth()/2;jet.y=VH*.5;s6StrikeTick(jet,.1);
  o[diff+' bomber commits a dodgeable retina with the shared explosion owner']=groundTargetingFx.some(q=>q._mission29&&!q.track&&!q.lane&&q.warn>=1.35&&typeof q.onImpact==='function');
  enemies=[];groundTargetingReset();O.index=O.events.length;O.t=O.finish;O.lanes=[];missionAssaultTick(O,.01);
  o[diff+' assault exits cleanly and lets the normal mission advance']=s6Opening===null&&run._mission29OpeningDone;
 }
 diffKey='furious';DIFF=DIFFS.furious;beginStage(7);setState(GS.PLAY);story=null;spawnBoss('sludgeemperor');bossActive=true;const b=boss,M=s7mInit(b);
 s7mTick(b,1.1);o['anomaly intro is invulnerable and radios from another pilot']=missionIntro(b)&&b._s7warden.noHit&&b._s7warden.final.radio.who!=='DECKER';
 o['anomaly uses authored toxic explosions']=explosions.some(q=>q._frToxic);
 s7mTick(b,6);o['anomaly finishes into the original portal entry']=M._mission29IntroDone&&M.mode==='portal'&&M.t===0;
 s7mTick(b,1.5);o['Warden emerges into its real walk-in after the cinematic']=M.mode==='entry';
 M.mode='dead';fr27Exit(b,.1);const E=M.frExit;fr27Exit(b,9);o['wreck world anchor advances with sewer source, never player chase']=b.y===E.groundY+E.travel&&M.height===0&&M.drop===0;
 o['all nine elemental laser reels have four authored registered frames']=Object.keys(INFUSIONS).every(e=>MISSION29_ART['beam_'+e]?.frames.length===4&&XART._src[MISSION29_ART['beam_'+e].key]===MISSION29_ART['beam_'+e].path);
 let draws=0;const draw=ctx.drawImage;ctx.drawImage=function(){draws++;return draw.apply(this,arguments);};
 for(const e of Object.keys(INFUSIONS)){const before=draws;o[e+' beam uses the authored animated renderer']=missionBeamDraw({_inf:e,top:20,bot:300,w:26,x:240})&&draws>before;}
 ctx.drawImage=draw;return o;
 })())`,ctxv));
 for(const [label,passed]of Object.entries(out))ok(passed,label);
};
