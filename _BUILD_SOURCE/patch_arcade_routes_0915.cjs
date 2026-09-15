/* Guarded reconstruction of the Arcade route/isolation changes on main 7635330b. */
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),file=path.join(root,'assets/game.js');
let source=fs.readFileSync(file,'utf8'),changes=0;
function once(before,after,label){
  const count=source.split(before).length-1;
  if(count!==1)throw new Error(label+': expected one source match, got '+count);
  source=source.replace(before,after);changes++;
}
once(
`function s7WardenSay(b,text,dur,who){
  const F=b&&b._s7warden&&b._s7warden.final;if(!F)return;
  F.radio=`,
`function s7WardenSay(b,text,dur,who){
  const F=b&&b._s7warden&&b._s7warden.final;if(!F)return;
  if(run.mode==='arcade'){F.radio=null;return;}
  F.radio=`,'Warden radio');
once(
`  const S=b&&b._s7warden,F=S&&S.final;if(!F||F.phase==='defeat'||F.phase==='escape')return true;`,
`  const S=b&&b._s7warden,F=S&&S.final;if(!F||F.finished||F.phase==='defeat'||F.phase==='escape')return true;`,'Warden score guard');
once(
`  }else{
    run._l78Entry=1;beginStage(8);
  }
}
function s7WardenFinalTick`,
`  }else{
    // Arcade must pay both seats through the ordinary results handler before Stage 8.
    F.radio=null;F.shipHidden=false;run._l78Entry=0;
    drawStageClear._init=false;drawStageClear._res=null;setState(GS.STAGECLEAR);
  }
}
function s7WardenFinalTick`,'Warden results');
once(`    if(F.t>=2.75){s7WardenPhase(b,'escape');`,`    if(F.t>=(run.mode==='arcade'?.65:2.75)){s7WardenPhase(b,'escape');`,'Warden hold');
once(
`    S.noHit=true;F.portalOpen=clamp(F.t/.72,0,1);mapScroll=Math.min(levelScrollRange(),mapScroll+dt*230);
    if(!F.beat){F.beat=1;if(Audio.SFX&&(Audio.SFX.helixCharge||Audio.SFX.warpGate))(Audio.SFX.helixCharge||Audio.SFX.warpGate)();}`,
`    const arcade=run.mode==='arcade';
    S.noHit=true;F.portalOpen=arcade?0:clamp(F.t/.72,0,1);
    if(!arcade)mapScroll=Math.min(levelScrollRange(),mapScroll+dt*230);
    if(!F.beat){F.beat=1;if(!arcade&&Audio.SFX&&(Audio.SFX.helixCharge||Audio.SFX.warpGate))(Audio.SFX.helixCharge||Audio.SFX.warpGate)();}`,'Warden portal');
once(`    if(F.t>=1.55){const q=clamp((F.t-1.55)/1.58,0,1)`,`    if(!arcade&&F.t>=1.55){const q=clamp((F.t-1.55)/1.58,0,1)`,'Warden forced flight');
once(
`    if(F.t>=3.06&&!F.bigBoom){F.bigBoom=true;F.bossHidden=true;for(let i=0;i<9;i++)explode(b.x+rnd(-b.w*.55,b.w*.55),b.y+rnd(-b.h*.45,b.h*.45),rnd(72,132),'red');if(typeof fxBurst==='function')fxBurst(b.x,b.y,230,{color:'#ff7134',rings:4,chunks:44,sparks:72});}
    if(F.t>=3.72){F.engulf=`,
`    if(F.t>=3.06&&!F.bigBoom){F.bigBoom=true;F.bossHidden=true;for(let i=0;i<9;i++)explode(b.x+rnd(-b.w*.55,b.w*.55),b.y+rnd(-b.h*.45,b.h*.45),rnd(72,132),'red');if(typeof fxBurst==='function')fxBurst(b.x,b.y,230,{color:'#ff7134',rings:4,chunks:44,sparks:72});}
    // Keep the authored wreck and blast, then show results without the story's portal flight.
    if(arcade&&F.t>=3.72){s7WardenFinishCampaign(b);return true;}
    if(F.t>=3.72){F.engulf=`,'Warden Arcade finish');
once(
`  run.contUsed=0;   // continue counter resets per RUN, not per stage (drop 0805b)`,
`  run.contUsed=0;   // continue counter resets per RUN, not per stage (drop 0805b)
  run._s5Resume=null;run._s5ResumeArm=0;run._s5GateOut=0;run._s9taken=0;run._l78Entry=0;`,'fresh run latches');
once(`  if(num===9 && typeof campaign!=='undefined') campaign.bonusUnlocked=0;`,`  if(num===9 && run.mode==='campaign' && typeof campaign!=='undefined') campaign.bonusUnlocked=0;`,'bonus ownership');
once(
`  const _l78Pending=(num===8)&&!!(run._l78Entry||(typeof campaign!=='undefined'&&campaign._l78Pending));`,
`  // Campaign owns the map-to-rift handoff; a saved campaign latch cannot redirect Arcade.
  const _l78Pending=run.mode==='campaign'&&(num===8)&&!!(run._l78Entry||(typeof campaign!=='undefined'&&campaign._l78Pending));
  if(run.mode==='arcade') storySkip();`,'Stage 8 latch');
once(
`  const _wantOpening = (typeof DBG!=='undefined' && DBG.opening)`,
`  const _wantOpening = run.mode==='campaign' && (typeof DBG!=='undefined' && DBG.opening)`,'opening');
once(
`  drawVictory._ready=false;
  if(typeof victoryEndingWarm==='function')victoryEndingWarm();
  setState(GS.VICTORY); Audio.stopMusic(); Audio.startMusic('cinematics'); Audio.SFX.victory();`,
`  drawVictory._ready=run.mode==='arcade';
  if(run.mode!=='arcade'&&typeof victoryEndingWarm==='function')victoryEndingWarm();
  setState(GS.VICTORY); Audio.stopMusic(); Audio.startMusic(run.mode==='arcade'?'stageclear':'cinematics'); Audio.SFX.victory();`,'Arcade final setup');
once(`function storyPlay(stage, scene){
`,`function storyPlay(stage, scene){
  if(run.mode==='arcade') return false;
`,'story guard');
once(
`      /* hand over to the map, which flashes the bonus node and unlocks it */
      if(typeof openStageSelect==='function') openStageSelect(5, {bonusUnlock:true});`,
`      // Arcade earns the same secret encounter without selecting it on the campaign map.
      if(run.mode==='arcade') beginStage(9);
      else if(typeof openStageSelect==='function') openStageSelect(5, {bonusUnlock:true});`,'secret entry');
once(
`  run._l78Entry=0; try{ if(typeof campaign!=='undefined'&&campaign) campaign._l78Pending=0; }catch(_e){}`,
`  run._l78Entry=0;   // debug runs use Arcade; the saved campaign owns its pending arrival`,'debug isolation');
once(`    else if(F.phase==='escape'){
      const q=`,`    else if(F.phase==='escape'&&run.mode!=='arcade'){
      const q=`,'Warden portal draw');
once(
`        if(typeof openStageSelect==='function') openStageSelect(clamp(campaign.unlockedMax||1,1,8), {});
        else beginStage(6);`,
`        if(run.mode==='arcade'){
          // Resume the earned Stage-5 detour; password entry has no suspended level.
          if(run._s5Resume){run._s9taken=1;run._s5ResumeArm=1;run._s5GateOut=1;beginStage(5);}
          else beginStage(6);
        }else if(typeof openStageSelect==='function') openStageSelect(clamp(campaign.unlockedMax||1,1,8), {});
        else beginStage(6);`,'secret return');
once(`         continues directly while preserving the same Stage 8 entrance cinematic. */`,`         continues directly to the ordinary Stage 8 card and launch. */`,'Stage 8 comment');
once(
`      else if(run.mode==='arcade'){
        if(typeof outboundStart==='function'){ outboundStart(run.stage); setState(GS.OUTBOUND); }
        else beginStage(run.stage+1);
      }`,
`      else if(run.mode==='arcade'){
        beginStage(run.stage+1);
      }`,'direct stage results');
once(
`  victoryEndingWarm();ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);`,
`  // Arcade keeps its score/end card, with no pilot-ending cinematic or art-loading wait.
  if(run.mode==='arcade'){
    drawVictory._t=(drawVictory._t||0)+dt;
    victoryFinalCard(VICTORY_CARD_AT+drawVictory._t,W,H);
    const click=!!Input.mouse.down&&!drawVictory._md;drawVictory._md=!!Input.mouse.down;
    if(drawVictory._t>5&&(Input.menuConfirm()||click)){
      drawVictory._t=0;drawVictory._ready=false;setState(GS.TITLE);menuIndex=0;Audio.startMusic('title');
    }
    return;
  }
  victoryEndingWarm();ctx.fillStyle='#000';ctx.fillRect(0,0,W,H);`,'Arcade final draw');
once(
`  gravityMode={phase:'drift',t:0,age:0,dialogueT:0,dialogueDelay:0.42,dialogueDone:false,
    line:`,
`  const arcade=run.mode==='arcade';
  gravityMode={phase:'drift',t:0,age:0,dialogueT:0,dialogueDelay:0.42,dialogueDone:arcade,
    narrative:!arcade,
    line:`,'Stage 5 narrative state');
once(
`  if(gravityMode.phase==='drift'){
    gravityMode.dialogueT=(gravityMode.dialogueT||0)+dt;
    const chars=Math.max(0,(gravityMode.dialogueT-gravityMode.dialogueDelay)*GRAVITY_DIALOGUE_CPS);
    if(chars>=(gravityMode.line||'').length+GRAVITY_DIALOGUE_CPS*GRAVITY_DIALOGUE_HOLD)gravityMode.dialogueDone=true;
  }else if(gravityMode.phase==='charge'){`,
`  if(gravityMode.phase==='drift'){
    if(gravityMode.narrative!==false){
      gravityMode.dialogueT=(gravityMode.dialogueT||0)+dt;
      const chars=Math.max(0,(gravityMode.dialogueT-gravityMode.dialogueDelay)*GRAVITY_DIALOGUE_CPS);
      if(chars>=(gravityMode.line||'').length+GRAVITY_DIALOGUE_CPS*GRAVITY_DIALOGUE_HOLD)gravityMode.dialogueDone=true;
    }
  }else if(gravityMode.phase==='charge'){`,'Stage 5 narrative tick');
once(`  if(phase!=='active'&&(gravityMode.dialogueT||0)>gravityMode.dialogueDelay){`,`  if(gravityMode.narrative!==false&&phase!=='active'&&(gravityMode.dialogueT||0)>gravityMode.dialogueDelay){`,'legacy dialogue draw');
once(`function furyIntroDialogue(G){
 if(!G||G.phase==='active'||G.dialogueT<=G.dialogueDelay)return;`,`function furyIntroDialogue(G){
 if(!G||G.narrative===false||G.phase==='active'||G.dialogueT<=G.dialogueDelay)return;`,'Fury dialogue draw');
if(source.includes('\r\n'))throw new Error('game.js must remain LF');
fs.writeFileSync(file,source,'utf8');
console.log('Applied '+changes+' guarded Arcade replacements.');
