"use strict";
/* Stage X is an arrival in the central arena, followed by the chosen encounter. */
const AP10_X={intro:null,events:[],base:{quick:gp4QuickEncounter,play:updatePlay,
 world:drawWorld,locked:h3Locked,hit:playerHit,leave:scLeaveStage,rebel:h3RebelTick}};
gp4QuickEncounter=function(){
 if(AP10_X.intro||!GP4.routeReady||state!==GS.PLAY)return;
 if(GP4.stage6Only)return AP10_X.base.quick.apply(this,arguments);
 const route=GP4.route;run._gp4StageX=route;GP4.routeReady=false;
 s6Opening=null;story=null;fb2Talk=null;BOFCinematicDirector.cancel();stagePlan=[];spawnClock=9999;
 enemies=[];pBullets=[];eBullets=[];powerups=[];subBoss=null;subBossActive=false;subBossDone=subBossTriggered=true;
 boss=null;bossActive=false;s6WingInit();s6Wing.route=route;s6Wing.all=true;s6WingLaunch(4,true);s6Wing.line=null;
 AP10_X.intro={t:0,route,x:worldWidth()/2};player.x=AP10_X.intro.x;player.y=VH+45;player.invuln=5;
 Audio.startMusic('stagex');XART.rdy('fr27_stagex_card');Input.clearTaps?.();
 AP10_X.events.push({event:'arrival',route});
};
h3Locked=function(){return !!AP10_X.intro||AP10_X.base.locked.apply(this,arguments);};
playerHit=function(){if(AP10_X.intro)return;return AP10_X.base.hit.apply(this,arguments);};
updatePlay=function(dt){const wasIntro=h3RebelIntro(),r=AP10_X.base.play.apply(this,arguments),I=AP10_X.intro;
 if(wasIntro&&!h3RebelIntro()&&boss?._rebels?.frIntro?.done)H3.release=false;
 if(!I||state!==GS.PLAY)return r;
 I.t+=dt;const u=clamp(I.t/2.5,0,1),ease=u*u*(3-2*u);player.x=I.x;player.y=lerp(VH+45,VH*.79,ease);
 for(const [i,q] of (s6Wing?.ships||[]).entries()){
  const v=clamp((I.t-.18-i*.22)/2.1,0,1),e=v*v*(3-2*v),side=i%2?1:-1;
  q.x=I.x+side*(i<2?76:144);q.y=lerp(VH+80,VH*(i<2?.84:.90),e);
 }
 if(I.t>=4.2){AP10_X.intro=null;GP4.route=I.route;GP4.routeReady=true;GP4.stage6Only=false;
  AP10_X.base.quick();H3.release=false;AP10_X.events.push({event:'encounter',route:I.route});}
 return r;
};
drawWorld=function(dt){const r=AP10_X.base.world.apply(this,arguments),I=AP10_X.intro;if(!I)return r;
 ctx.save();worldXformEscape();ctx.imageSmoothingEnabled=false;
 if(!cc21Live()&&XART.rdy('fr27_stagex_card')){const im=XART.get('fr27_stagex_card'),w=VW*.63,h=w*im.height/im.width;
  ctx.drawImage(im,(VW-w)/2,VH*.22-h/2,w,h);}
 campText(I.route==='left'?'HARRIER PURSUIT':'REBEL FURY',VW/2,VH*.37,17,'#e8edf8');
 const full=I.route==='left'?'Fury flight, all five ships accounted for. The Harrier is ahead.':'Five against five. Fury flight, form up. We finish this together.';
 const shown=full.slice(0,Math.floor(Math.max(0,I.t-.3)*36));
 dlgBox({who:'COLE',portrait:'cole',full,shown,forceShown:true,fade:clamp(I.t*3,0,1),pw:VW*.92,ph:VH*.22,x:VW*.04,y:VH*.52});
 ctx.restore();return r;
};
// Combat starts on the next beat even when Fire remains held during the intro.
// The introductory missile exhibition can never strand the trigger latch.
h3RebelTick=function(b,dt){const was=!!b._rebels?.frIntro?.done,r=AP10_X.base.rebel.apply(this,arguments);
 if(!was&&b._rebels?.frIntro?.done){H3.release=false;player._tapHeld=false;player._tapT=null;Input.clearTaps?.();
  AP10_X.events.push({event:'rebel-trigger-released'});}return r;};
function ap10StageXReward(){
 if(!run._gp4StageX||run._ap10XReward||campaign.stageX1004?.rewarded)return;
 run._ap10XReward=true;if(campaign.stageX1004)campaign.stageX1004.rewarded=true;
 for(const seat of seatList())withSeat(seat,()=>{
  manualMissileApplyUpgrade('super',run);run.bombs=clampManualMissiles((run.bombs||0)+12,run.missileTier);
  run.lives=Math.min(9,(run.lives||0)+1);run.forgeCombos=(run.forgeCombos||0)+1;
 });
 AP10_X.events.push({event:'air-superiority-reward'});
 AP10_X.reward={t:0};
}
scLeaveStage=function(){ap10StageXReward();return AP10_X.base.leave.apply(this,arguments);};
const AP10_X_MAP_DRAW=drawStageSelect,AP10_X_BRIEF=mapgBriefingDraw;
drawStageSelect=function(dt){if(AP10_X.reward){AP10_X.reward.t+=dt;if(AP10_X.reward.t>=8)AP10_X.reward=null;}
 return AP10_X_MAP_DRAW.apply(this,arguments);};
mapgBriefingDraw=function(info){if(AP10_X.reward)info={key:'ap10-air-superiority',title:'STAGE X CLEAR - AIR SUPERIORITY',
 body:'SUPER MISSILES UPGRADED. +12 MISSILES. +1 LIFE. +1 FORGE COMBINE. FURY FLIGHT, RETURN TO BASE.'};
 return AP10_X_BRIEF.call(this,info);};
