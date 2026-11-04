"use strict";
/* ============================================================
   WAVE FOLLOW-UPS (drop 1104) - WF14. Loaded last. From the wave audit (docs/WAVE_AUDIT_1103.md).
   window.WF14_OFF=1 disables all of it; each part also has its own switch.

   1. STAGE 6 SCENE SKIP (WF14_TALK_OFF). The team-argument scene (fb2Talk) freezes combat for 45-58 s.
      The original scene let FIRE finish a line and then advance; feedback_1003h replaced fb2TalkTick
      with an auto-advance-only version. FIRE (or confirm) now finishes the typing on the first press
      and moves to the next line on the second, as before. Each line is on screen at least 0.25 s
      before a press counts, so mashing FIRE cannot blank-skip lines. Auto-advance, the Callisto banner and the
      Cole demo are untouched (those beats ignore the press).

   2. STAGE 5 RAMMER TELL (WF14_RAM_OFF). S511's rammer warns with a lane for .64/.42/.30 s (N/H/F) and
      charges at 440/650/850 px/s. Every Normal death on Stage 5 in the audit was this hull. During
      the tell it now blinks white twice and eases back ~10 px against its charge line (back to its
      start by the end, so the warned lane stays exact) on every difficulty. Normal only: the tell
      lasts .90 s and the charge tops out at 360 px/s. Hard/Furious timing and speed are unchanged.

   3. BELOW-SCREEN UNITS (WF14_CAP_OFF). game.js's wave dispatcher counts live enemies against the
      stage cap. A unit whose top edge has scrolled past the bottom of the playfield still counted
      until it was culled, holding a due wave up to 2.5 s per stage (measured: probe_cap_offscreen_1104).
      game.js now asks wf14BelowScreen(e) and skips those units; nothing else reads it.
   ============================================================ */
(function(){
if(window.WF14_OFF)return;
const WF={stat:{talkSkips:0,talkFinishes:0,ramTells:0,ramBlinks:0}};

/* ---- 1. Stage 6 scene: FIRE finishes, then advances ---- */
if(typeof fb2TalkTick==='function'){
  const baseTalk=fb2TalkTick;
  fb2TalkTick=function(dt){
    const S=fb2Talk,b=S&&!S.done?S.beats[S.i]:null;
    if(!window.WF14_TALK_OFF&&b&&!b.kind&&typeof b.text==='string'&&S.age>.35&&S.t>=.25&&
       (Input.tapAny(keybind.fire)||Input.menuConfirm())){
      const full=b.text.length;
      if(S.shown<full){S.t=Math.max(S.t,full/32);S.shown=full;WF.stat.talkFinishes++;}
      else{fb2TalkNext();WF.stat.talkSkips++;}
      return;
    }
    return baseTalk.apply(this,arguments);
  };
}

/* ---- 2. Stage 5 rammer wind-up ---- */
if(typeof s5SpaceTick==='function'){
  const baseTick=s5SpaceTick;
  s5SpaceTick=function(e,dt){
    const A=e&&e._s511;
    if(window.WF14_RAM_OFF||!A||A.model!=='rammer')return baseTick.apply(this,arguments);
    const normal=ai27Level()===0,x0=e.x,y0=e.y,before=A.phase;
    const out=baseTick.apply(this,arguments);
    if(A.phase==='tell'){
      if(before!=='tell'){                     // tell just started this frame
        if(normal)A.warm=Math.max(A.warm,.90);
        A._wf14={lurch:0,blinks:0};WF.stat.ramTells++;
      }
      const W=A._wf14||(A._wf14={lurch:0,blinks:0}),k=clamp(A.t/A.warm,0,1);
      // ease back against the charge line and return by the end of the tell
      const want=-10*Math.sin(Math.PI*k),d=want-W.lurch;W.lurch=want;
      e.x+=Math.cos(A.head)*d;e.y+=Math.sin(A.head)*d;
      // two white blinks, at 45% and 80% of the tell
      for(const [i,at]of[[0,.45],[1,.80]])if(W.blinks===i&&k>=at){W.blinks++;e.flash=Math.max(e.flash||0,.07);WF.stat.ramBlinks++;}
    }else if(A.phase==='ram'&&normal&&before==='ram'){
      // S511 moved it by its own speed this frame; scale that step to the Normal cap
      const dx=e.x-x0,dy=e.y-y0,step=Math.hypot(dx,dy),cap=360*dt;
      if(step>cap&&step>0){e.x=x0+dx*cap/step;e.y=y0+dy*cap/step;}
    }
    return out;
  };
}

/* ---- 3. below-screen units do not hold waves ---- */
window.wf14BelowScreen=function(e){return !window.WF14_CAP_OFF&&e.y-(e.h||0)/2>VH;};

window.WF14=WF;WF.version='1104';
})();
