"use strict";
/* Reconcile the independently authored Oct 2 campaign layers. Claude owns the
   live arrival; retain Mike's trap taunt and the immediate opening jump. */
const IN1003_INTRO_START=fb2IntroStart,IN1003_INTRO_END=fb2IntroEnd,IN1003_SCRIPT=fb2HammerIntroScript;
fb2IntroStart=function(b){if(b?._hammer)b._hammer.intro1002=true;return IN1003_INTRO_START.apply(this,arguments);};
fb2HammerIntroScript=function(lead,dispatcher,campaign){
 const lines=IN1003_SCRIPT.apply(this,arguments);
 if(campaign)lines.splice(lines.length-1,0,
  {who:'CRONOS',kind:'boss',text:'Coming up here was merely a trap. The Legion has already launched its attack down on Earth.'},
  {who:'CRONOS',kind:'boss',text:'Such a foolish mortal. This is the fate of the one who dances to their death. Now, let us dance!'});
 return lines;
};
fb2IntroEnd=function(){
 const b=fb2Intro?.boss,first=fb2Intro&&!fb2Intro.done;
 const result=IN1003_INTRO_END.apply(this,arguments);
 if(first&&b&&!b.dead&&b._hammer&&b._hammer.state==='unfold'){
  b.enter=false;b._noHit=false;b._hammer.intro1002=true;b._hammer.openingJump1003=true;hammerTarget(b);hammerState(b,'warn');
 }
 return result;
};
// Chromium's first activation must not replace the promised post-dialogue jump.
// Let the ordinary warned leap, landing recovery and return finish, then activate.
const IN1003_ARMOR_BEGIN=fr27BeginArmor,IN1003_HAMMER_TICK=hammerBossTick;
fr27BeginArmor=function(b){
 const h=b?._hammer;
 if(h?.openingJump1003){
  if(['warn','leap','recover','back'].includes(h.state))return null;
  h.openingJump1003=false;
 }
 return IN1003_ARMOR_BEGIN.apply(this,arguments);
};
hammerBossTick=function(b,dt){
 const h=b?._hammer;
 if(h?.openingJump1003&&h.state==='recover'){h.followCount=5;h.comboPending=false;}
 return IN1003_HAMMER_TICK.apply(this,arguments);
};
