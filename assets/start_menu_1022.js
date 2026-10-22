'use strict';
/* ==========================================================================================
   THE START MENU FOR A GAME MODE, AND NO BACK OUT OF ONE (Mike, 2026-10-22).

   "we need a start menu system similar to the in-game start menu, but it allows you to select
    Return to Menu, Save Game, Load Game, Options, Forge/Loadout, Quit Game. Only those options
    when you've entered a game mode. you can no longer press back or your assigned B button to
    exit a menu or screen like pilot select, or being in the arcade or campaign game mode itself.
    Ive noticed I could press back on the pilot select screen, that should be disabled. When I
    selected Campaign and then was in the map, I pressed back and went to selecting the game
    mode, no good."

   ONE LOCK, NOT ELEVEN. Every one of those screens reads Input.menuBack() on its own (drawDiff,
   drawPilot, menuBackTick's MENU_BACK table, the campaign layers, cinematicEscape ...), so a gate
   at each would be eleven gates and the twelfth screen would miss it. Input.menuBack is wrapped
   once: on a game-mode screen it CONSUMES the press and answers false, so no screen behind it can
   be left that way. The only presses still honoured are moves INSIDE a screen that never leave
   the mode - the co-op seat rewind, the campaign slot picker's cancel, the map's button bar and
   its Stage X focus - and this menu's own close.

   THE MENU OPENS ON START (P / the pad's START), NEVER ON ENTER. Enter is bound to START and is
   the confirm on every one of these screens (0917d: on the map Enter is DEPLOY), so taking it
   would make every keyboard confirm open a menu instead.

   THE SCREEN BEHIND IS FROZEN, NOT DRAWN. While the menu is up, drawScene is not called: a
   snapshot of the last frame is shown greyed, the way the in-game pause shows the playfield. The
   screen behind therefore reads no input at all, which is the only way to be sure a press meant
   for the menu does not also move a pilot or a flag.

   The in-game pause (PLAY_PAUSE_ROWS) is untouched: gameplay keeps the pause menu Mike approved.
   window.SM22_OFF=1 restores the old behaviour (back allowed, no menu).
   ========================================================================================== */
const SM22_ROWS=['RETURN TO MENU','SAVE GAME','LOAD GAME','OPTIONS','FORGE / LOADOUT','QUIT GAME'];
const SM22={open:false,mode:'root',sel:0,t:0,shown:0,msg:'',msgT:0,frame:null,md:false,slot:null,blocked:0};
const SM22_LOCKED={};
[GS.DIFF,GS.CAMPHUB,GS.PILOT,GS.COOPROSTER,GS.STAGESEL,GS.OPENING,GS.OUTBOUND].forEach(function(s){ if(s!=null) SM22_LOCKED[s]=1; });

function sm22Off(){ return typeof window!=='undefined' && !!window.SM22_OFF; }
/* A GAME MODE HAS BEEN ENTERED. The password route reaches DIFF too, but a password is not a mode
   - it keeps its BACK to the keypad. */
function sm22Locked(){
  if(sm22Off()) return false;
  if(!SM22_LOCKED[state]) return false;
  if(state===GS.DIFF && typeof passwordDifficulty!=='undefined' && passwordDifficulty) return false;
  return true;
}
/* A press that moves INSIDE the screen and never leaves the mode. */
function sm22BackInside(){
  if(SM22.open) return true;
  if(state===GS.CAMPHUB) return typeof campPick!=='undefined' && !!campPick;
  if(state===GS.PILOT) return typeof coopActive==='function' && coopActive() && typeof coopPick!=='undefined' && coopPick===1;
  if(state===GS.COOPROSTER) return true;          // rewinds one seat, back to P2's pick
  if(state===GS.STAGESEL){
    if(typeof campPause!=='undefined' && campPause) return true;
    if(typeof cmap2!=='undefined' && cmap2 && cmap2.focus==='bar') return true;
    if(typeof map4hXFocused==='function' && map4hXFocused()) return true;
    return false;
  }
  return false;
}
const SM22_BASE={back:Input.menuBack, backButton:(typeof backButton==='function')?backButton:null,
                 hint:controlHintRow, footer:menuControlFooter, scene:drawScene,
                 optApply:optApply, optCancel:optCancel};
Input.menuBack=function(){
  const hit=SM22_BASE.back.apply(Input,arguments);
  if(!hit) return false;
  if(sm22Locked() && !sm22BackInside()){ SM22.blocked++; return false; }   // consumed, and it goes nowhere
  return true;
};
if(SM22_BASE.backButton) backButton=function(){
  if(sm22Locked() && !sm22BackInside()) return false;   // the on-screen BACK box goes with the B button
  return SM22_BASE.backButton.apply(this,arguments);
};
/* AND THE SHARED BACK ROUTER NEVER ROUTES A GAME-MODE SCREEN. menuBackTick runs before the screen and
   MENU_BACK still says PILOT -> DIFF and STAGESEL -> MODESEL, so an allowed press (the co-op seat rewind)
   was taken by the router first and dropped both players to difficulty - measured: Escape on P2's pick
   landed on 'diff'. On a locked screen only the map's own Stage X focus may use it; the screen keeps the rest. */
const SM22_TICK=menuBackTick;
menuBackTick=function(){
  if(!sm22Locked()) return SM22_TICK.apply(this,arguments);
  if(state===GS.STAGESEL && typeof Rival24!=='undefined' && Rival24.mapBack && Rival24.mapBack()) return true;
  return false;
};
/* the hint row stops promising a BACK that no longer exists */
controlHintRow=function(items){
  if(sm22Locked() && !SM22.open && Array.isArray(items) && !(state===GS.STAGESEL && sm22BackInside()))
    items=items.map(function(it){ return (it && it[0]==='pad_b' && /^BACK$/i.test(it[1])) ? ['pad_start','MENU'] : it; });
  arguments[0]=items;
  return SM22_BASE.hint.apply(this,arguments);
};

function sm22StartTap(){
  let hit=false;
  for(const seat of [1,2]){
    const kb=(typeof keybindFor==='function')?keybindFor(seat):keybind;
    for(const k of (kb&&kb.start)||[]){ if(k==='enter'||/^mouse\d/.test(k)) continue; if(Input.tap(k)) hit=true; }
  }
  if(Input.tap('pad_b9')) hit=true;
  return hit;
}
/* the menu opens only on a screen that is settled - never mid-boot, mid-zoom or mid-confirm */
function sm22CanOpen(){
  if(!sm22Locked()) return false;
  if(state===GS.OPENING || state===GS.OUTBOUND) return false;   // cinematics: B is locked, the menu waits for a screen
  if(typeof _selFlash!=='undefined' && _selFlash) return false;
  if(state===GS.STAGESEL){
    if(typeof campPause!=='undefined' && campPause) return false;
    if(typeof sselZoom!=='undefined' && sselZoom) return false;
    if(run.mode==='campaign' && typeof campPauseIsCampaignScreen==='function' && !campPauseIsCampaignScreen()) return false;
  }
  if(state===GS.PILOT && typeof pilotPending!=='undefined' && pilotPending!=null) return false;
  if(state===GS.CAMPHUB && typeof campPick!=='undefined' && campPick) return false;
  return true;
}
function sm22Snapshot(){
  const cv=document.getElementById('screen');
  if(!cv) return null;
  const c=document.createElement('canvas'); c.width=cv.width; c.height=cv.height;
  try{ c.getContext('2d').drawImage(cv,0,0); }catch(_e){}
  return c;
}
function sm22Open(){
  SM22.open=true; SM22.mode='root'; SM22.sel=0; SM22.t=0; SM22.shown=0; SM22.msg=''; SM22.msgT=0;
  SM22.md=!!(Input.mouse&&Input.mouse.down); SM22.frame=sm22Snapshot(); SM22.from=state;
  try{ XART.rdy('pause_button_0915'); if(typeof map4hWarm==='function') map4hWarm(); }catch(_w){}
  try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_s){}
  Input.clearTaps();
}
function sm22Close(){ SM22.open=false; SM22.mode='root'; SM22.frame=null; SM22.slot=null; Input.clearTaps(); }
function sm22Say(m){ SM22.msg=m; SM22.msgT=2.2; }

/* what each row can do from here, and why not when it cannot */
function sm22MapLive(){
  return state===GS.STAGESEL && run.mode==='campaign' &&
         (typeof campPauseIsCampaignScreen!=='function' || campPauseIsCampaignScreen());
}
function sm22Why(i){
  if(i===1){
    if(run.mode!=='campaign') return 'ARCADE RUNS DO NOT SAVE';
    if(!sm22MapLive()) return 'SAVE FROM THE CAMPAIGN MAP';
  }
  if(i===4){
    if(run.mode!=='campaign' || !sm22MapLive()) return 'FORGE OPENS ON THE CAMPAIGN MAP';
  }
  return '';
}

function sm22Choose(i){
  const why=sm22Why(i);
  if(why){ sm22Say(why); try{ (Audio.SFX.blocked||Audio.SFX.blip)(); }catch(_b){} return; }
  try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_s){}
  if(i===0){
    sm22Close();
    if(run.mode==='campaign' && typeof campaignEnd==='function') campaignEnd();
    if(typeof coopOn!=='undefined') coopOn=false;
    menuIndex=0; goTitle();
  } else if(i===1||i===2){
    SM22.mode=i===1?'save':'load'; SM22.slot={mode:SM22.mode,sel:0,t:0,msg:'',msgT:0}; Input.clearTaps();
  } else if(i===3){
    SM22.mode='options'; optSnap=null; optSelIdx=0; optScroll=0; optSnapshot(); Input.clearTaps();
  } else if(i===4){
    sm22Close(); sm22ForgeLoadout();
  } else if(i===5){
    sm22Close(); tryExit();
  }
}
/* THE FORGE FROM THE MAP MUST NOT REFILL THE STAGE'S UPGRADES. forgeStart hands out a fresh
   FORGE_COMBOS_PER_STAGE and FORGE_RESPECS_PER_STAGE every time it opens - right at a debrief,
   where it is the stage's budget, and an unlimited supply here. The counts it had are put back. */
function sm22ForgeLoadout(){
  const combos=run.forgeCombos, respecs=run.forgeRespecs, shown=run._forgeShown;
  const back=function(){ if(typeof openStageSelect==='function') openStageSelect(run.stage,{}); else setState(GS.STAGESEL); };
  forgeStart(function(){ run._forgeShown=shown; loadoutStart(back); });
  run.forgeCombos=combos==null?0:combos; run.forgeRespecs=respecs==null?0:respecs;
}
/* OPTIONS returns to this menu, never to the title. optApply / optCancel both end on
   setState(GS.TITLE); while this menu owns the options page that one call is swallowed. */
function sm22OptsWrap(base){
  return function(){
    if(!(SM22.open && SM22.mode==='options')) return base.apply(this,arguments);
    const real=setState; setState=function(){};
    try{ base.apply(this,arguments); } finally{ setState=real; }
    SM22.mode='root'; SM22.t=.85; menuIndex=0; Input.clearTaps();
  };
}
optApply=sm22OptsWrap(SM22_BASE.optApply);
optCancel=sm22OptsWrap(SM22_BASE.optCancel);

/* the menu draws in the 480x512 field, centred in whatever canvas the screen behind was using */
function sm22Field(){
  const cv=document.getElementById('screen');
  const W=cv?cv.width:VW*SS, H=cv?cv.height:VH*SS, k=Math.min(W/VW,H/VH);
  return {W,H,k,ox:(W-VW*k)/2,oy:(H-VH*k)/2};
}
function sm22DrawRoot(dt){
  const P=SM22, m=Input.mouse||{};
  if(P.t>.25){
    let ch=0; if(Input.menuDown()) ch=1; if(Input.menuUp()) ch=-1;
    if(ch){ P.sel=(P.sel+ch+SM22_ROWS.length)%SM22_ROWS.length; try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_b){} }
  }
  msgText('MENU',VW/2,58,28,'#2aff5a',0,1,.12);
  const w=Math.min(300,VW-96),h=34,gap=48,y0=118;
  let clicked=-1;
  for(let i=0;i<SM22_ROWS.length;i++){
    const k=clamp((P.t-i*.085)/.28,0,1); if(k<=0) continue;
    if(i>=P.shown){ P.shown=i+1; try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_b){} }
    const y=y0+i*gap-(1-k)*(1-k)*VH*.75, sel=i===P.sel, off=!!sm22Why(i);
    ctx.save(); ctx.globalAlpha=k*(off?.5:1);
    if(!(typeof playPauseButtonArt==='function' && playPauseButtonArt(VW/2,y,w,h,sel))){
      octFill(VW/2-w/2,y-h/2,w,h,7,sel?'#133623':'#141b19');
      ctx.strokeStyle=sel?'#2aff5a':'#3c5550'; ctx.lineWidth=sel?2:1; ctx.strokeRect(VW/2-w/2+4,y-h/2+3,w-8,h-6);
    }
    campText(SM22_ROWS[i],VW/2,y+(typeof PAUSE_LABEL_DY==='number'?PAUSE_LABEL_DY:-2),12,sel?'#dfffe9':'#a0b2a8');
    if(sel && typeof menuSelMark==='function') menuSelMark(VW/2,y,w/2,'green');
    ctx.restore();
    const mx=sm22MouseX(), my=sm22MouseY();
    if(k===1 && m.inside && Math.abs(mx-VW/2)<=w/2 && Math.abs(my-y)<h/2){
      if(Input.consumeMouseMoved()) P.sel=i;
      if(m.down && !P.md && P.t>.85) clicked=i;
    }
  }
  P.md=!!m.down;
  const why=sm22Why(P.sel);
  if(P.msgT>0) campText(P.msg,VW/2,VH-50,10,'#ff7474');
  else if(why) campText(why,VW/2,VH-50,10,'#8fa79a');
  if(Input.menuBack() || sm22StartTap()){ try{ Audio.SFX.blip&&Audio.SFX.blip(); }catch(_b){} sm22Close(); return; }
  if(clicked>=0){ P.sel=clicked; sm22Choose(clicked); return; }
  if(P.t>.85 && Input.menuConfirm()) sm22Choose(P.sel);
}
/* the mouse is reported in the screen behind's logical space; bring it into this field */
function sm22MouseX(){ const m=Input.mouse||{}, F=sm22Field(); return ((m.x||0)*SS-F.ox)/F.k; }
function sm22MouseY(){ const m=Input.mouse||{}, F=sm22Field(); return ((m.y||0)*SS-F.oy)/F.k; }

function sm22DrawSlots(dt){
  const P=SM22.slot; if(!P) return;
  P.t+=dt; P.msgT=Math.max(0,(P.msgT||0)-dt);
  const count=CAMP_SLOTS+(P.mode==='load'?1:0), per=4, page=Math.floor(P.sel/per), start=page*per, n=Math.min(per,count-start);
  msgText(P.mode==='save'?'SAVE GAME':'LOAD GAME',VW/2,40,22,'#2aff5a',0,1,.12);
  campText('PAGE '+(page+1)+' / '+Math.ceil(count/per)+'   LEFT / RIGHT',VW/2,66,9,'#8fbad2');
  const rw=390, rh=82, gap=6, x=(VW-rw)/2, y0=80;
  for(let i=0;i<n;i++){
    const idx=start+i, r={x,y:y0+i*(rh+gap),w:rw,h:rh};
    /* the load list puts the AUTO SAVE first, the way the map's own load page does */
    const slot=P.mode==='load'?(idx===0?CAMP_SLOTS:idx-1):idx;
    if(typeof map4hSlotDraw==='function') map4hSlotDraw(slot,r,idx===P.sel,P.mode);
    else { ctx.fillStyle=idx===P.sel?'#1b3a28':'#12181a'; ctx.fillRect(r.x,r.y,r.w,r.h); campText((slot===CAMP_SLOTS?'AUTO':'SLOT '+(slot+1)),VW/2,r.y+r.h/2,12,'#dfffe9'); }
  }
  if(P.msgT>0) campText(P.msg,VW/2,VH-50,10,'#ffe082');
  if(Input.menuLeft()){ P.sel=Math.max(0,P.sel-per); try{ Audio.SFX.blip(); }catch(_b){} }
  if(Input.menuRight()){ P.sel=Math.min(count-1,P.sel+per); try{ Audio.SFX.blip(); }catch(_b){} }
  if(Input.menuUp()){ P.sel=(P.sel+count-1)%count; try{ Audio.SFX.blip(); }catch(_b){} }
  if(Input.menuDown()){ P.sel=(P.sel+1)%count; try{ Audio.SFX.blip(); }catch(_b){} }
  if(Input.menuBack()){ SM22.mode='root'; SM22.slot=null; SM22.t=.85; Input.clearTaps(); return; }
  if(P.t>.25 && Input.menuConfirm()){
    const slot=P.mode==='load'?(P.sel===0?CAMP_SLOTS:P.sel-1):P.sel;
    sm22SlotCommit(P,slot);
  }
}
function sm22SlotCommit(P,slot){
  if(P.mode==='save'){
    const ok=campWriteSlot(slot);
    if(ok && typeof campSession!=='undefined') campSession=campReadSlot(slot);
    try{ (ok?Audio.SFX.select:(Audio.SFX.blocked||Audio.SFX.blip))(); }catch(_s){}
    SM22.mode='root'; SM22.slot=null; SM22.t=.85;
    sm22Say(ok?'SAVED TO SLOT '+(slot+1):'SAVE FAILED - STORAGE BLOCKED');
    return;
  }
  const data=slot===CAMP_SLOTS?(typeof campReadAuto==='function'?campReadAuto():null):campReadSlot(slot);
  if(!data){ P.msg='THAT SLOT IS EMPTY'; P.msgT=2; try{ Audio.SFX.blip(); }catch(_b){} return; }
  if(!campApply(data)){ P.msg='THAT SAVE IS FROM AN OLDER BUILD'; P.msgT=2; return; }
  if(typeof campSession!=='undefined') campSession=data;
  try{ Audio.SFX.select&&Audio.SFX.select(); }catch(_s){}
  sm22Close();
  if(typeof campPick!=='undefined') campPick=null;
  if(typeof coopOn!=='undefined') coopOn=false;
  openStageSelect(run.stage,{});
  try{ if(typeof cmap2Toast==='function') cmap2Toast(slot===CAMP_SLOTS?'LOADED AUTO SAVE':'LOADED SLOT '+(slot+1)); }catch(_t){}
}

function sm22Draw(dt){
  dt=Number.isFinite(dt)?dt:1/60;
  SM22.t+=dt; if(SM22.msgT>0) SM22.msgT-=dt;
  const F=sm22Field();
  ctx.save(); ctx.setTransform(1,0,0,1,0,0);
  ctx.fillStyle='#000'; ctx.fillRect(0,0,F.W,F.H);
  if(SM22.frame){ ctx.save(); ctx.filter='grayscale(1) brightness(.62)'; ctx.drawImage(SM22.frame,0,0); ctx.restore(); }
  ctx.restore();
  ctx.save(); ctx.setTransform(F.k,0,0,F.k,F.ox,F.oy);
  if(SM22.mode==='options'){
    if(Input.menuBack() && !(typeof rebindAction!=='undefined' && rebindAction)){ optCancel(); }
    else drawOptions(0);
  } else {
    ctx.fillStyle='rgba(0,0,0,.50)'; ctx.fillRect(0,0,VW,VH);
    if(SM22.mode==='save'||SM22.mode==='load') sm22DrawSlots(dt); else sm22DrawRoot(dt);
  }
  ctx.restore();
}

drawScene=function(dt){
  if(SM22.open){
    if(state!==SM22.from){ sm22Close(); return SM22_BASE.scene.apply(this,arguments); }   // something else took the screen
    if(typeof window!=='undefined') window.__bofFrames=(window.__bofFrames|0)+1;
    return sm22Draw(dt);
  }
  if(sm22CanOpen() && sm22StartTap()){ sm22Open(); return sm22Draw(dt); }
  return SM22_BASE.scene.apply(this,arguments);
};
menuControlFooter=function(){
  if(SM22.open){
    const F=sm22Field();
    ctx.save(); ctx.setTransform(F.k,0,0,F.k,F.ox,F.oy);
    /* the frozen frame carries the screen's own hint row; a dark strip keeps the two from reading as one */
    if(SM22.mode!=='options'){ ctx.fillStyle='rgba(0,0,0,.88)'; ctx.fillRect(-F.ox/F.k,VH-34,F.W/F.k,34+F.oy/F.k); }
    if(SM22.mode==='options'){ if(!(typeof rebindAction!=='undefined' && rebindAction)) controlHintRow([['pad_dpad','ADJUST'],['pad_a','SELECT'],['pad_b','CANCEL']]); }
    else if(SM22.mode==='root') controlHintRow([['pad_dpad','MENU'],['pad_a','SELECT'],['pad_b','CLOSE']]);
    else controlHintRow([['pad_dpad','SLOT'],['pad_a',SM22.mode==='save'?'SAVE':'LOAD'],['pad_b','BACK']]);
    ctx.restore();
    return;
  }
  return SM22_BASE.footer.apply(this,arguments);
};
if(typeof window!=='undefined'){ window.SM22=SM22; window.sm22Open=sm22Open; window.sm22Locked=sm22Locked; }
