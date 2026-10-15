"use strict";
/* These modes had cards but no playable route. They use the real campaign,
   seats and encounter controllers; a password cannot earn a campaign receipt. */
const P2M={choice:null,row:0,md:false,pending:null,active:null,ngplus:false,elapsed:0,
 index:0,proof:null,receipt:null,result:null,launching:false,events:[],base:{list:modeList,
 open:modeItemOpen,drawMode:drawModeSelect,hub:drawCampaignHub,start:startRun,begin:beginStage,
 leave:scLeaveStage,victory:triggerVictory,over:triggerGameOver,scene:drawScene,back:menuBackTick,
 complete:achievementRunComplete,state:setState,snapshot:campSnapshot,apply:campApply}};
const P2_CLEAR_KEY='bof_campaign_completion_v2';
function p2CampaignReceipt(q){return !!(q?.version===2&&q.mode==='campaign'&&Array.isArray(q.stages)&&q.stages.length===8&&[1,2,3,4,5,6,7,8].every(n=>q.stages.includes(n)));}
try{const q=JSON.parse(localStorage.getItem(P2_CLEAR_KEY)||'null');if(p2CampaignReceipt(q))P2M.receipt=q;}catch(_){}
// Preserve the old flag/profile and saves. A saved full campaign can provide
// migration evidence; an isolated boolean from encounter passwords cannot.
if(!P2M.receipt&&bonusModesUnlocked){for(const s of [campReadAuto(),...Array.from({length:CAMP_SLOTS},(_,i)=>campReadSlot(i))]){
 if(s?.v===CAMP_SAVE_VER&&[1,2,3,4,5,6,7,8].every(n=>s.rank?.[n])){
 P2M.receipt={version:2,mode:'campaign',stages:[1,2,3,4,5,6,7,8],pilot:s.pilot,difficulty:s.diff,migrated:true};
 try{localStorage.setItem(P2_CLEAR_KEY,JSON.stringify(P2M.receipt));}catch(_){}break;}}}
// Campaign saves carry the completed route; continuing a valid slot must not
// discard the evidence required to unlock the modes after its final battle.
campSnapshot=function(){const s=P2M.base.snapshot.apply(this,arguments);if(P2M.proof&&run.mode==='campaign')s.modeProof={stages:[...P2M.proof.stages]};return s;};
campApply=function(s){const ok=P2M.base.apply.apply(this,arguments);if(ok){const stages=[1,2,3,4,5,6,7,8].filter(n=>s.rank?.[n]);
 P2M.proof={stages,pilot:run.pilot};P2M.active=null;P2M.ngplus=!!s.ngplus;}return ok;};
bonusModesAreUnlocked=function(){return !!P2M.receipt;};
bonusModesUnlockFromCampaign=function(){
 if(P2M.receipt||run.mode!=='campaign'||!P2M.proof||!run._trueFinaleCleared)return false;
 if(![1,2,3,4,5,6,7].every(n=>P2M.proof.stages.includes(n)||campaign.rank[n]))return false;
 P2M.receipt={version:2,mode:'campaign',stages:[1,2,3,4,5,6,7,8],pilot:run.pilot,difficulty:diffKey,at:Date.now()};
 bonusModesUnlocked=true;try{localStorage.setItem(P2_CLEAR_KEY,JSON.stringify(P2M.receipt));localStorage.setItem(BONUS_MODE_UNLOCK_KEY,'1');}catch(_){}
 p2Log('campaign-completed');return true;
};
modeList=function(){return P2M.base.list.apply(this,arguments).filter(m=>m.mode!=='ngplus').map(m=>
 m.mode==='bossrush'||m.mode==='timeattack'?{...m,open:true}:m);};
modeItemOpen=function(it){if(it?.mode==='bossrush'||it?.mode==='timeattack')return !!it.open&&bonusModesAreUnlocked();return P2M.base.open.apply(this,arguments);};
function p2HubSync(){const i=CAMPHUB_ITEMS.findIndex(it=>it.act==='ngplus'),unlocked=bonusModesAreUnlocked(),selected=CAMPHUB_ITEMS[campHubIndex];
 if(unlocked&&i<0)CAMPHUB_ITEMS.unshift({key:'mode_ngplus_0917',label:'NEW GAME +',act:'ngplus'});
 if(!unlocked&&i>=0)CAMPHUB_ITEMS.splice(i,1);
 const resume=CAMPHUB_ITEMS.findIndex(it=>it.act==='continue');
 if(!campCanContinue()&&resume>=0)CAMPHUB_ITEMS.splice(resume,1);
 else if(campCanContinue()&&resume<0)CAMPHUB_ITEMS.splice(CAMPHUB_ITEMS.findIndex(it=>it.act==='new')+1,0,{key:'btn_continue',label:'CONTINUE',act:'continue'});
 if(selected&&CAMPHUB_ITEMS.includes(selected))campHubIndex=CAMPHUB_ITEMS.indexOf(selected);
 campHubIndex=clamp(campHubIndex,0,CAMPHUB_ITEMS.length-1);}
drawCampaignHub=function(dt){p2HubSync();return P2M.base.hub.apply(this,arguments);};
function p2ModeChoose(mode){
 P2M.active=null;P2M.pending=null;P2M.ngplus=false;P2M.choice=null;coopOn=false;run.ngplus=false;
 if(mode==='coop'){P2M.choice='coop';P2M.row=0;P2M.md=Input.mouse.down;return true;}
 if(mode==='arcade'&&bonusModesAreUnlocked()){P2M.choice='arcade';P2M.row=0;P2M.md=Input.mouse.down;return true;}
 if(mode==='bossrush'||mode==='timeattack'){
  if(!bonusModesAreUnlocked())return true;P2M.pending=mode;run.mode='arcade';passwordDifficulty=false;setState(GS.DIFF);return true;}
 return false;
}
function p2ChoiceConfirm(){const type=P2M.choice,row=P2M.row;P2M.choice=null;Audio.SFX.select?.();
 if(type==='coop'&&row===1){if(window.BOFOnline)window.BOFOnline.open();else campHubSay('ONLINE CONNECTION UNAVAILABLE');return;}
 coopOn=type==='coop';if(coopOn)coopPick=0;run.mode='arcade';run.ngplus=type==='arcade'&&row===1;P2M.ngplus=run.ngplus;
 passwordDifficulty=false;setState(GS.DIFF);
}
function p2ChoiceDraw(dt){const coop=P2M.choice==='coop',labels=coop?['LOCAL CO-OP','ONLINE CO-OP']:['NEW GAME','NEW GAME +'],keys=coop?['nms_coop','nms_coop']:['btn_newgame','mode_ngplus_0917'];
 drawCanonBackdrop('nbt_3',.65);campText(coop?'CO-OP':'ARCADE',VW/2,82,22,'#ffd36b');
 if(Input.menuUp()||Input.menuDown())P2M.row=1-P2M.row;
 const press=Input.mouse.down&&!P2M.md;P2M.md=Input.mouse.down;
 for(let i=0;i<2;i++){const y=210+i*100,key=keys[i],sel=P2M.row===i;XART.rdy(key);
  if(XART.rdy(key)){const im=XART.get(key),w=sel?300:286,h=Math.min(74,w*im.height/im.width);ctx.save();ctx.globalAlpha=sel?1:.7;ctx.drawImage(im,VW/2-w/2,y-h/2,w,h);ctx.restore();}
  campText(labels[i],VW/2,y+(coop?46:47),13,sel?'#fff':'#91a5bb');
  if(sel)drawSelArrow(VW/2-175,y,22,false);
  if(press&&Math.abs(Input.mouse.x-VW/2)<160&&Math.abs(Input.mouse.y-y)<42){P2M.row=i;p2ChoiceConfirm();return;}
 }
 campText(coop?'TWO PILOTS - SEPARATE LIVES AND SCORES':'CHOOSE BEFORE DIFFICULTY',VW/2,414,12,'#a6d8ef');
 controlHintRow([['pad_dpad','SELECT'],['pad_a','CONFIRM'],['pad_b','BACK']]);
 if(stateT>.25&&Input.menuConfirm())p2ChoiceConfirm();
 if(Input.menuBack()){P2M.choice=null;Input.clearTaps?.();}
}
drawModeSelect=function(dt){if(P2M.choice)return p2ChoiceDraw(dt);return P2M.base.drawMode.apply(this,arguments);};
menuBackTick=function(){if(state===GS.MODESEL&&P2M.choice){if(Input.menuBack()){P2M.choice=null;Input.clearTaps?.();return true;}return false;}
 if(state==='p2result')return false;return P2M.base.back.apply(this,arguments);};
const P2_GAUNTLET=[
 {stage:1,role:'boss',code:'BOSS1'},{stage:2,role:'boss',code:'BOSS2'},
 {stage:3,role:'boss',code:'BOSS3'},{stage:4,role:'boss',code:'BOSS4'},
 {stage:5,role:'boss',code:'BOSS5'},{stage:6,role:'boss',code:'HARR6',route:'left'},
 {stage:6,role:'boss',code:'REBEL6',route:'right'},{stage:7,role:'boss',code:'BOSS7'},
 {stage:8,role:'boss',code:'BOSS8'}
];
function p2RushLaunch(){const E=P2_GAUNTLET[P2M.index];if(!E)return p2ModeFinish(true);
 P2M.launching=true;try{run.stage=E.stage;P2M.base.begin.call(this,E.stage);BOFCinematicDirector.cancel();story=null;H3.ending=null;
  if(E.route){GP4.route=E.route;GP4.routeReady=true;GP4.stage6Only=true;gp4QuickEncounter();}
  else on5LaunchEncounter(E);
  // Retain the pilot, score and equipment. A small service window replenishes
  // missiles/shield, never makes the pilot invincible or resets a boss's HP.
  if(P2M.index>0){run.shield=Math.max(run.shield,1);run.bombs=Math.max(run.bombs,2);player.invuln=Math.max(player.invuln,1.5);}
  P2M.events.push({event:'rush-encounter',code:E.code});Input.clearTaps?.();
 }finally{P2M.launching=false;}
}
startRun=function(from=1){const mode=P2M.pending,ng=!!P2M.ngplus;P2M.pending=null;P2M.active=null;P2M.elapsed=0;P2M.index=0;P2M.result=null;
 P2M.proof=run.mode==='campaign'&&from===1&&!ON5.pending?{stages:[],pilot:run.pilot}:null;
 const r=P2M.base.start.apply(this,arguments);run.ngplus=ng;run2.ngplus=coopOn&&ng;
 if(ng)ensureForgeForms();
 if(mode){P2M.active=mode;P2M.proof=null;run.mode='arcade';run._p2Mode=mode;if(mode==='bossrush')p2RushLaunch();}
 return r;
};
beginStage=function(n){
 if(P2M.active==='bossrush'&&!P2M.launching){
  if(n!==P2_GAUNTLET[P2M.index]?.stage&&bossDefeated)return scLeaveStage({bonus:0});
  return p2RushLaunch();
 }return P2M.base.begin.apply(this,arguments);};
scLeaveStage=function(R){
 if(P2M.active==='bossrush'){
  if(P2M.result?.intermission)return;
  run.score+=R.bonus||0;P2M.index++;
  if(P2M.index>=P2_GAUNTLET.length)return p2ModeFinish(true);
  P2M.result={complete:false,success:true,intermission:true};setState('p2result');return;}
 if(P2M.proof&&run.mode==='campaign'&&bossDefeated&&!P2M.proof.stages.includes(run.stage))P2M.proof.stages.push(run.stage);
 return P2M.base.leave.apply(this,arguments);
};
achievementRunComplete=function(){if(P2M.active||run.mode!=='campaign')return [];return P2M.base.complete.apply(this,arguments);};
function p2ModeFinish(success){const mode=P2M.active;if(!mode)return;
 P2M.result={complete:true,success,intermission:false,mode,elapsed:P2M.elapsed,score:run.score};
 if(success){const key='bof_'+mode+'_'+run.pilot+'_'+diffKey;try{const old=JSON.parse(localStorage.getItem(key)||'null');
  if(!old||P2M.elapsed<old.elapsed)localStorage.setItem(key,JSON.stringify({elapsed:P2M.elapsed,score:run.score,at:Date.now()}));}catch(_){}}
 setState('p2result');Audio.stopMusic();Audio.SFX[success?'victory':'gameover']?.();
}
triggerVictory=function(){if(P2M.active){p2ModeFinish(true);return;}return P2M.base.victory.apply(this,arguments);};
triggerGameOver=function(){if(P2M.active){p2ModeFinish(false);return;}return P2M.base.over.apply(this,arguments);};
function p2TimeString(t){return Math.floor(t/60).toString().padStart(2,'0')+':'+(t%60).toFixed(2).padStart(5,'0');}
function p2ModeResultDraw(){const R=P2M.result;if(!R)return;drawCanonBackdrop('nbt_3',.65);bofPanel(30,72,VW-60,350);
 campText(P2M.active==='bossrush'?'BOSS RUSH':'TIME ATTACK',VW/2,118,22,'#ffd36b');
 campText(R.complete?(R.success?'RUN COMPLETE':'RUN ENDED'):'ENCOUNTER COMPLETE',VW/2,182,17,'#fff');
 campText(p2TimeString(P2M.elapsed),VW/2,245,28,'#71e4ff');campText('SCORE  '+Math.floor(run.score),VW/2,290,15,'#fff');
 if(P2M.active==='bossrush')campText(Math.min(P2M.index,P2_GAUNTLET.length)+' / '+P2_GAUNTLET.length+' ENCOUNTERS',VW/2,331,14,'#a5cae7');
 controlHintRow([['pad_a',R.complete?'TITLE':'NEXT FIGHT'],['pad_b','TITLE']]);
 if(stateT>.3&&Input.menuConfirm()){if(R.complete){P2M.active=null;P2M.result=null;setState(GS.TITLE);}else{P2M.result=null;p2RushLaunch();}}
 else if(Input.menuBack()){P2M.active=null;P2M.result=null;setState(GS.TITLE);}
}
drawScene=function(dt){if(state==='p2result')return p2ModeResultDraw();
 if(P2M.active&&state===GS.PLAY)P2M.elapsed+=Math.max(0,Math.min(.05,dt));
 const r=P2M.base.scene.apply(this,arguments);
 if(P2M.active&&state===GS.PLAY){ctx.save();worldXformEscape();campText((P2M.active==='bossrush'?'RUSH ':'TIME ')+p2TimeString(P2M.elapsed),VW/2,viewTopY()+22,10,'#fff1ab');ctx.restore();}return r;
};
setState=function(next){if([GS.TITLE,GS.PASSWORD].includes(next)){P2M.active=null;P2M.choice=null;P2M.pending=null;P2M.ngplus=false;}return P2M.base.state.apply(this,arguments);};
