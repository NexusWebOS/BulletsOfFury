"use strict";
/* Arrival order: dialogue, native chromium charge/lock, then combat. The
   live radio never stops world scrolling or player controls. */
const IN1003_INTRO_START=fb2IntroStart,IN1003_INTRO_END=fb2IntroEnd,IN1003_SCRIPT=fb2HammerIntroScript;
fb2IntroStart=function(b){if(b?._hammer)b._hammer.intro1002=true;return IN1003_INTRO_START.apply(this,arguments);};
fb2HammerIntroScript=function(lead,dispatcher,campaign){
 const lines=IN1003_SCRIPT.apply(this,arguments);
 if(campaign)lines.splice(lines.length-1,0,
  {who:'CHRONOS',kind:'boss',text:'Coming up here was merely a trap. The Legion has already launched its attack down on Earth.'},
  {who:'CHRONOS',kind:'boss',text:'Such a foolish mortal. This is the fate of the one who dances to their death. Now, let us dance!'});
 return lines;
};
fb2IntroEnd=function(){
 const b=fb2Intro?.boss,first=fb2Intro&&!fb2Intro.done;
 const result=IN1003_INTRO_END.apply(this,arguments);
 if(first&&b===boss&&!b.dead&&b._hammer&&b._hammer.state==='unfold'){
  b.enter=false;b._noHit=false;b._hammer.intro1002=true;b._hammer.openingJump1003=false;
  // Let the native idle tick establish the difficulty-scaled health budget.
  // Its next tick begins fr_activation before any attack can be selected.
  hammerState(b,'hammer');
 }
 return result;
};
const IN1003_ARMOR_BEGIN=fr27BeginArmor;
fr27BeginArmor=function(b){
 if(fb2IntroActive()&&fb2Intro.boss===b)return null;
 return IN1003_ARMOR_BEGIN.apply(this,arguments);
};
