/* ============================================================
   RE-SPEC (Mike, 2026-10-22)

   "now we need the option to actually re-spec during between stages in the loadout/forge, and in
    this new menu during the map"

   What was there: forgeRespec only took the equipped form OFF a weapon. The form stayed earned and
   the combine spent on it stayed spent, so it changed nothing a loadout swap could not already do
   for free - and it lived only on the CHARGE button with no label anywhere, the Forge showing a
   lone "X0" on its bottom bar.

   What a re-spec is now: the combination is UNDONE. Every element forged onto that weapon this run
   comes off, the weapon goes back to its base form, and each removed combination hands its
   upgrade back - so the same weapon can be forged with a different element straight away. One
   re-spec per weapon, two per level completion (FORGE_RESPECS_PER_STAGE).

     - It is a visible button on the Forge (its bottom bar) and on the Loadout (its re-spec bar),
       pressed with CHARGE or a click. The first press ARMS it and says what will be removed; the
       second press inside RS22_ARM_T does it. It destroys a combination, so it asks.
     - Decker's Upgrade Center on the map has its own RE-SPEC A WEAPON row (upgrade_center_1022.js).
     - The budget is granted when a STAGE IS CLEARED (entering the debrief), not when the Forge
       opens. forgeStart used to refill it, which is why the map could only ever offer whatever a
       Forge visit had happened to leave behind - and nothing at all on a stage whose Forge never
       opened, or after loading a save. Both counters now ride the campaign save.
     - ⚠ New Game+ purchased recipes (profile-owned forge_<elem>_<w>_C) are re-added by
       ensureForgeForms on every call, so they are NOT removable and NOT refunded; they are a
       permanent purchase. Everything else on the weapon is.
   window.RS22_OFF=1 restores the old unequip-only behaviour and the forgeStart refill.
   ============================================================ */
const RS22_ARM_T=3.0;
function rs22Off(){ return typeof window!=='undefined' && !!window.RS22_OFF; }
function rs22Kept(elem,w){
  const O=(typeof achievementState!=='undefined'&&achievementState&&achievementState.owned)||{};
  return !!(run&&run.ngplus&&O['forge_'+elem+'_'+(w|0)+'_C']);
}
function rs22FormsOn(w){
  const F=run&&run.forgeForms&&run.forgeForms[w|0];
  return F?Object.keys(F).filter(function(e){ return INFUSIONS[e] && !rs22Kept(e,w); }):[];
}
/* while the chaingun stands in for the machine gun it wears the MG's forms (forgeEntry does the same) */
function rs22Weapon(w){
  w=w|0;
  if(w===7&&!rs22FormsOn(7).length&&typeof chaingunReplacesMG==='function'&&chaingunReplacesMG()) return 0;
  return w;
}
function respecInfo(w){
  const ww=rs22Weapon(w), forms=rs22FormsOn(ww);
  return {w:ww, shown:w|0, forms:forms,
          names:forms.map(function(e){ return typeof forgeComboName==='function'?forgeComboName(e,ww):e.toUpperCase(); }),
          left:Math.max(0,(run&&run.forgeRespecs)|0)};
}
function respecLabel(w){
  return (typeof weaponDisplayName==='function')?weaponDisplayName(w):(WEAPONS[w]||'WEAPON');
}
/* the text a first press shows - what will come off and what comes back */
function respecWarn(w){
  const I=respecInfo(w);
  if(!I.forms.length) return respecLabel(w)+' HAS NO FORGED UPGRADE TO RE-SPEC';
  if(I.left<=0) return 'NO RE-SPECS LEFT - CLEAR A STAGE FOR TWO MORE';
  return 'AGAIN TO RE-SPEC: REMOVES '+I.names.join(' + ')+'  -  REFUNDS '+I.forms.length+' UPGRADE'+(I.forms.length>1?'S':'');
}
const RS22_BASE=forgeRespec;
forgeRespec=function(w){
  if(rs22Off()) return RS22_BASE.apply(this,arguments);
  if(!run) return 'bare';
  const I=respecInfo(w);
  if(!I.forms.length) return 'bare';
  if((run.forgeRespecs|0)<=0) return 'spent';
  for(const e of I.forms) delete run.forgeForms[I.w][e];
  if(run.forgeForms[I.w]&&!Object.keys(run.forgeForms[I.w]).length) delete run.forgeForms[I.w];
  if(run.forge) delete run.forge[I.w];
  /* the Fire Whip IS the laser's fire form; without it the laser goes back to its base beam */
  if(I.w===3&&run.wvars&&run.wvars[3]==='firewhip') run.wvars[3]=null;
  run.forgeCombos=(run.forgeCombos|0)+I.forms.length;
  run.forgeRespecs=(run.forgeRespecs|0)-1;
  const cur=run.weapon|0;
  if(cur===I.w||(cur===7&&I.w===0)){ run.infusion=null; if(typeof forgeApply==='function') forgeApply(); }
  run._lastRespec={w:I.w, forms:I.forms.slice(), names:I.names.slice()};
  return 'ok';
};
/* one press arms, a second press on the SAME weapon inside RS22_ARM_T does it. Returns a word. */
function respecPress(S,w,t){
  if(w==null) return {r:'none', msg:'NO WEAPON SELECTED'};
  const I=respecInfo(w);
  if(!I.forms.length){ S._rsArm=null; return {r:'bare', msg:respecWarn(w)}; }
  if(I.left<=0){ S._rsArm=null; return {r:'spent', msg:respecWarn(w)}; }
  if(S._rsArm&&S._rsArm.w===(w|0)&&t-S._rsArm.t<=RS22_ARM_T){
    S._rsArm=null;
    const r=forgeRespec(w);
    if(r==='ok') return {r:'ok', msg:respecLabel(w)+' RE-SPEC - '+I.forms.length+' UPGRADE'+(I.forms.length>1?'S':'')+' BACK  -  RE-SPECS LEFT '+(run.forgeRespecs|0)};
    return {r:r, msg:respecWarn(w)};
  }
  S._rsArm={w:w|0, t:t};
  return {r:'armed', msg:respecWarn(w)};
}
function rs22Armed(S,w,t){ return !!(S&&S._rsArm&&S._rsArm.w===(w|0)&&t-S._rsArm.t<=RS22_ARM_T); }
function rs22ChargeTap(){ return (keybind.charge||[]).some(function(k){ return Input.tap(k); }); }
function rs22SfxFor(r){ return r==='ok'?'powerup':(r==='armed'?'blip':'blocked'); }
/* the button: a dark bar, a red pulse while armed, the pad X glyph and its label */
function rs22Button(x,y,w,h,label,armed,t,enabled){
  ctx.save();
  ctx.fillStyle='#080b12'; ctx.fillRect(x,y,w,h);
  if(armed){ ctx.globalAlpha=.6+.4*Math.sin(t*14); ctx.strokeStyle='#ff4a3a'; ctx.lineWidth=2; ctx.strokeRect(x+1,y+1,w-2,h-2); }
  else if(enabled){ ctx.globalAlpha=.75; ctx.strokeStyle='#d9a83f'; ctx.lineWidth=1; ctx.strokeRect(x+.5,y+.5,w-1,h-1); }
  ctx.restore();
  ctx.save(); if(!enabled) ctx.globalAlpha=.55;
  if(typeof controlHintRow==='function') controlHintRow([['pad_x',label]],y+h/2,x+w/2,w-12,Math.min(24,h*.8));
  ctx.restore();
}

/* ---------------- the budget ---------------- */
const RS22_SET=setState;
setState=function(s){
  const prev=state, r=RS22_SET.apply(this,arguments);
  if(!rs22Off()&&run&&s===GS.STAGECLEAR&&prev!==GS.STAGECLEAR){
    run._rs22Serial=(run._rs22Serial|0)+1;
    run.forgeCombos=FORGE_COMBOS_PER_STAGE; run.forgeRespecs=FORGE_RESPECS_PER_STAGE;
  }
  return r;
};
const RS22_FORGE_START=forgeStart;
forgeStart=function(){
  const granted=!rs22Off()&&run&&(run._rs22Serial|0)>0, c=run&&run.forgeCombos, r=run&&run.forgeRespecs;
  const out=RS22_FORGE_START.apply(this,arguments);
  if(granted){ run.forgeCombos=c|0; run.forgeRespecs=r|0; }      // the stage clear granted it; a visit spends it
  return out;
};
const RS22_SNAP=campSnapshot;
campSnapshot=function(){
  const s=RS22_SNAP.apply(this,arguments);
  if(s&&run){ s.forgeCombos=run.forgeCombos|0; s.forgeRespecs=run.forgeRespecs|0; s.rs22Serial=run._rs22Serial|0; }
  return s;
};
const RS22_APPLY=campApply;
campApply=function(s){
  const ok=RS22_APPLY.apply(this,arguments);
  if(ok&&s&&run){ run.forgeCombos=Math.max(0,s.forgeCombos|0); run.forgeRespecs=Math.max(0,s.forgeRespecs|0); run._rs22Serial=Math.max(0,s.rs22Serial|0); }
  return ok;
};

/* ---------------- the Forge ---------------- */
const RS22_FORGE_BAR=[.150,.856,.700,.070];
/* above the loadout's own hint row (y .925), over the old "RE-SPECS n" counter */
const RS22_LOADOUT_BAR=[.330,.844,.340,.058];
const RS22_DRAW_FORGE=drawForge;
drawForge=function(dt){
  const F=forge;
  if(rs22Off()||!F) return RS22_DRAW_FORGE.apply(this,arguments);
  const W=(typeof cutsceneViewWidth==='function')?cutsceneViewWidth():VW, H=VH;
  const load=run.loadout||[], selW=load.length?load[clamp(F.sel|0,0,load.length-1)]:null;
  const B=frc(RS22_FORGE_BAR,W,H);
  /* input FIRST - drawForge reads CHARGE itself, and a tap is consumed by whoever reads it */
  if(F.row===0&&(F.t||0)>0.6&&state===GS.FORGE){
    const m=Input.mouse||{}, click=m.down&&!F.md&&m.x>=B[0]&&m.x<=B[0]+B[2]&&m.y>=B[1]&&m.y<=B[1]+B[3];
    if(rs22ChargeTap()||click){
      if(click) F.md=true;                     // the base must not read this click as "open the slot"
      const q=respecPress(F,selW,F.t||0); forgeSay(q.msg,rs22SfxFor(q.r));
    }
  }
  const out=RS22_DRAW_FORGE.apply(this,arguments);
  if(forge===F&&state===GS.FORGE){
    const I=selW!=null?respecInfo(selW):null, n=Math.max(0,run.forgeRespecs|0);
    const label=(I&&I.forms.length?'RE-SPEC '+respecLabel(selW):'RE-SPEC')+'   '+n+' LEFT';
    rs22Button(B[0],B[1],B[2],B[3],label,rs22Armed(F,selW,F.t||0),F.t||0,!!(I&&I.forms.length&&n>0));
  }
  return out;
};

/* ---------------- the Loadout ---------------- */
const RS22_DRAW_LOADOUT=drawLoadout;
drawLoadout=function(dt){
  const L=loadoutScr;
  if(rs22Off()||!L) return RS22_DRAW_LOADOUT.apply(this,arguments);
  const W=(typeof cutsceneViewWidth==='function')?cutsceneViewWidth():VW, H=VH;
  const load=run.loadout||[], selW=load.length?load[clamp(L.sel|0,0,load.length-1)]:null;
  const RB=frc(RS22_LOADOUT_BAR,W,H);
  if(L.row===0&&L.exitT<0&&(L.t||0)>=.55&&state===GS.LOADOUT){
    const m=Input.mouse||{}, click=m.down&&!L.md&&m.x>=RB[0]&&m.x<=RB[0]+RB[2]&&m.y>=RB[1]&&m.y<=RB[1]+RB[3];
    if(rs22ChargeTap()||click){
      if(click) L.md=true;
      const q=respecPress(L,selW,L.t||0); loadoutSay(q.msg,q.r==='ok'?'loadoutEquip':rs22SfxFor(q.r));
    }
  }
  const out=RS22_DRAW_LOADOUT.apply(this,arguments);
  if(loadoutScr===L&&state===GS.LOADOUT&&L.row!==2&&L.exitT<0){
    const I=selW!=null?respecInfo(selW):null, n=Math.max(0,run.forgeRespecs|0);
    const label=(I&&I.forms.length?'RE-SPEC '+respecLabel(selW):'RE-SPEC')+'   '+n+' LEFT';
    rs22Button(RB[0],RB[1],RB[2],RB[3],label,rs22Armed(L,selW,L.t||0),L.t||0,!!(I&&I.forms.length&&n>0));
    /* the loadout's status line under the bays shows what the press did */
    if(L.msgT>0&&L.row===0){ const art=(typeof curFontArt==='function')?curFontArt():null;
      if(art){ const y=H*.627, w=W*.82;
        ctx.save(); ctx.fillStyle='rgba(8,16,28,.94)'; ctx.fillRect((W-w)/2,y-H*.02,w,H*.04); ctx.restore();
        stageText(art,L.msg,W/2,y,Math.min(9,stageFitH(art,L.msg,w*.96,9,5,.04)),'#ffffff',.9,1,.04); } }
  }
  return out;
};
if(typeof window!=='undefined'){ window.respecInfo=respecInfo; window.respecPress=respecPress; }
