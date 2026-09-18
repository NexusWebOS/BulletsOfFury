#!/usr/bin/env python3
"""
patch_forge_sequence_0917b.py - the Forge sequence split into its beats.

Mike, 0917b: "Defeat boss, end screen - currency conversion during end screen and stats given -
weapons gained screen/powers gained screen - the forge screen - the forging screen itself - the
forged product screen - the loadout selection screen - fade to next level."

Every anchor is asserted: a str.replace whose needle is absent does not raise, and this repo has
shipped three commits describing changes the code never received that way (0906v).
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(ROOT, 'assets', 'game.js')
s = open(P, encoding='utf-8').read()
assert '\r\n' not in s[:20000], 'game.js is LF'

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, 'anchor found %d times (want %d): %r' % (n, count, old[:90])
    s = s.replace(old, new)

# ---------------------------------------------------------------- E1 registration
rep("""    X._src['inf_'+_e]='assets/game/ui/infusion_0917/inf_'+_e+'.png';
""", """    X._src['inf_'+_e]='assets/game/ui/infusion_0917/inf_'+_e+'.png';
  /* THE FORGE SEQUENCE'S TWO PLATES (0917b). SpriteCook, 1376x768 = the debrief's own 477:266 aspect,
     so they fill the cinematic viewport edge to edge with no distortion. The chamber is a 1:1 EDIT of
     the 0916 concept plate Mike liked (edit_asset_id, every socket emptied), the bays are generated
     against it as a reference so the two read as one family. */
  X._src['forge_chamber_0917b']='assets/game/ui/forge_0917b/forge_chamber.png';
  X._src['loadout_bays_0917b']='assets/game/ui/forge_0917b/loadout_bays.png';
""")

# ---------------------------------------------------------------- E2 GS enum + the one predicate
rep("""  VAULT:'vault', ARMORY:'armory' };""",
"""  VAULT:'vault', ARMORY:'armory',
  /* the Forge sequence's own beats (0917b): the weld, the product, the six bays */
  FORGING:'forging', FORGED:'forged', LOADOUT:'loadout' };
/* ⚠ ONE LIST OF THE SCREENS THAT SHARE THE DEBRIEF'S ASPECT (0917b). It was written out four times
   (both viewport lines, the setState predicate, the HUD wants) and 0916 records that a state missing
   from ONE of them draws its plate stretched into the play column. Three new states would have been
   twelve edits; this is one. */
function debriefFamily(st){
  return st===GS.STAGECLEAR||st===GS.UNLOCKS||st===GS.FORGE||st===GS.FORGING||st===GS.FORGED||st===GS.LOADOUT;
}""")
rep("""      const ar=(state===GS.STAGECLEAR||state===GS.UNLOCKS||state===GS.FORGE) ? (477/266)""",
    """      const ar=debriefFamily(state) ? (477/266)""")
rep("""      CINEMA_VW=(state===GS.STAGECLEAR||state===GS.UNLOCKS||state===GS.FORGE) ? Math.round""",
    """      CINEMA_VW=debriefFamily(state) ? Math.round""")
rep("""state===GS.VICTORY||state===GS.STAGECLEAR||state===GS.UNLOCKS||state===GS.FORGE) _setCinematicViewport(true);""",
    """state===GS.VICTORY||debriefFamily(state)) _setCinematicViewport(true);""")
rep("""         s===GS.INTRO || s===GS.STAGECLEAR || s===GS.UNLOCKS || s===GS.FORGE || s===GS.RIVAL;""",
    """         s===GS.INTRO || debriefFamily(s) || s===GS.RIVAL;""")
rep("""                        s===GS.STAGECLEAR || s===GS.UNLOCKS || s===GS.FORGE);   // the unlock page and the Forge share the debrief's plate and aspect""",
    """                        debriefFamily(s));   // the unlock page and every Forge beat share the debrief's plate and aspect""")

# ---------------------------------------------------------------- E4 drawScene
rep("""    case GS.FORGE:      return drawForge(dt);
""", """    case GS.FORGE:      return drawForge(dt);
    case GS.FORGING:    return drawForging(dt);
    case GS.FORGED:     return drawForging(dt);
    case GS.LOADOUT:    return drawLoadout(dt);
""")

# ---------------------------------------------------------------- E5/E6 what this stage's boss gave
rep("""  achievementState.owned[id]={at:Date.now()};   /* no cost: it was not bought */
  achievementSave();
  return 'ok';""", """  achievementState.owned[id]={at:Date.now()};   /* no cost: it was not bought */
  achievementSave();
  /* the POWERS GAINED page reads this - what THIS stage's boss handed over (0917b) */
  if(run){ if(!run._stageCombos) run._stageCombos=[]; run._stageCombos.push({elem:elem, w:w|0}); }
  return 'ok';""")
rep("""  if(run) run._fpLevelDone=false;   /* a new level may convert again (0917) */""",
    """  if(run) run._fpLevelDone=false;   /* a new level may convert again (0917) */
  if(run) run._stageCombos=[];       /* and the powers-gained page starts empty (0917b) */""")

# ---------------------------------------------------------------- E7/E8 the powers-gained page
rep("""function unlockRowsFor(stage, pk){
  const T=SC_UNLOCKS[stage|0]; if(!T) return [];
  const rows=(pk && T[pk]) ? T[pk] : (T.all||[]);
  return rows.slice(0, UNLOCK_MAX);
}""", """function unlockRowsFor(stage, pk){
  const T=SC_UNLOCKS[stage|0];
  const rows=T ? ((pk && T[pk]) ? T[pk] : (T.all||[])).slice() : [];
  /* ⚠ POWERS GAINED (Mike, 0917b: "weapons gained screen/powers gained screen"). The combination the
     boss dropped is announced on the same page, lettered in its ELEMENT's colour and drawn with its
     forged badge - row[2] is the tint and row[3] marks it a power, so the page can say which it is. */
  const C=(run && run._stageCombos) || [];
  for(const c of C){
    const nm=(typeof forgeComboName==='function')?forgeComboName(c.elem,c.w):String(c.elem).toUpperCase();
    rows.push([nm, 'micon_forge_'+c.elem+'_'+c.w, (INFUSIONS[c.elem]||{}).body||null, 'power']);
  }
  return rows.slice(0, UNLOCK_MAX);
}
function unlockHasPower(rows){ return (rows||[]).some(function(r){ return r && r[3]==='power'; }); }
function unlockHasWeapon(rows){ return (rows||[]).some(function(r){ return r && r[3]!=='power'; }); }""")
rep("""    const tH=(typeof stageFitH==='function')?stageFitH(art,'NEW WEAPONS UNLOCKED',b[2]*0.90,b[3]*0.62,10,0.08):b[3]*0.5;
    stageText(art,'NEW WEAPONS UNLOCKED',b[0]+b[2]/2,b[1]+b[3]*0.55,tH,'#ffd24a',0.9,A(0.10),0.08);""",
"""    const _uTitle=unlockHasPower(U.rows)?(unlockHasWeapon(U.rows)?'WEAPONS AND POWERS GAINED':'POWERS GAINED'):'NEW WEAPONS UNLOCKED';
    const tH=(typeof stageFitH==='function')?stageFitH(art,_uTitle,b[2]*0.90,b[3]*0.62,10,0.08):b[3]*0.5;
    stageText(art,_uTitle,b[0]+b[2]/2,b[1]+b[3]*0.55,tH,'#ffd24a',0.9,A(0.10),0.08);""")
rep("""    const msg='STAGE '+(run.stage|0)+' CLEARED. YOUR ARSENAL GROWS - THE FOLLOWING WILL NOW DROP FROM SUPPLY CRATES.';""",
"""    const msg=unlockHasWeapon(U.rows)
      ? ('STAGE '+(run.stage|0)+' CLEARED. YOUR ARSENAL GROWS - THE FOLLOWING WILL NOW DROP FROM SUPPLY CRATES.')
      : ('STAGE '+(run.stage|0)+' CLEARED. THE BOSS LEFT SOMETHING BEHIND - A NEW COMBINATION IS READY FOR THE FORGE.');""")
rep("""unlockTint(r[1]),0.85,a,0.06);""", """(r[2]||unlockTint(r[1])),0.85,a,0.06);""")
rep("""    if(goA>0){ stageText(art,'LOOK FOR THEM IN THE FIELD',""",
    """    if(goA>0){ stageText(art,(unlockHasWeapon(U.rows)?'LOOK FOR THEM IN THE FIELD':'WELD IT AT THE FORGE'),""")

# ---------------------------------------------------------------- E9 the order after the debrief
rep("""      const _forgeThen=function(){ if(typeof forgeVisible==='function' && forgeVisible()) forgeStart(_leave); else _leave(); };""",
"""      /* debrief -> weapons/powers gained -> forge (-> forging -> forged, from inside it) -> LOADOUT -> fade
         -> next stage (Mike, 0917b). Each beat runs the next from its own CONTINUE; the exit is still ONE
         function, and a beat with nothing to do skips itself rather than teaching the player to mash. */
      const _toLoadout=function(){ if(typeof loadoutVisible==='function' && loadoutVisible()) loadoutStart(_leave); else _leave(); };
      const _forgeThen=function(){ if(typeof forgeVisible==='function' && forgeVisible()) forgeStart(_toLoadout); else _toLoadout(); };""")

# ---------------------------------------------------------------- E10 the Forge screen itself
# (a) the loadout-box cursor: no square - the menu arrow under the box
rep("""      /* the cursor: a drawn frame, the same amber as the plate's rails */
      if(i===F.sel){
        const pulse=0.55+0.45*Math.sin(t*6);
        ctx.save(); ctx.globalAlpha=a*(F.row===0?pulse:0.35); ctx.strokeStyle='#ffd24a'; ctx.lineWidth=Math.max(2,bw*0.03);
        ctx.strokeRect(bx-2,RY-2,bw+4,bh+4); ctx.restore();
      }""",
"""      /* the cursor (0917b): NOT a square (Mike). The traced pointer rings the weapon's own badge and the
         menu's arrow rises under it; on the element row the slot keeps a still, dim ring so it is clear
         which weapon the element is going onto. */
      if(i===F.sel){
        const key2=weaponIconKey(w, Math.max(1,(run.wlevels&&run.wlevels[w])|0));
        ctx.save(); ctx.globalAlpha=a*(F.row===0?1:0.45);
        if(F.row===0) forgeHexPointer(key2,bx+bw/2,RY+bh/2,bh*0.78,'#ffd24a');
        ctx.restore();
        if(F.row===0) forgeSelArrowUp(bx+bw/2, RY+bh+nameH*1.55, Math.min(nameH*2.2,bh*0.30));
      }""")
# (b) the element cursor: traced hex + arrow, never a square
rep("""        if(F.row===1 && disc[F.esel]===el){
          const pulse=0.55+0.45*Math.sin(t*6);
          ctx.save(); ctx.globalAlpha=ea*pulse; ctx.strokeStyle=INFUSIONS[el].glow||'#ffffff'; ctx.lineWidth=Math.max(2,ew*0.06);
          ctx.strokeRect(ecx-ew/2-3,ecy-eh/2-3,ew+6,eh+6); ctx.restore();
        }""",
"""        /* ⚠ THE SELECTOR IS NOT A SQUARE (Mike, 0917b: "make the selector do a pixel flash bottom to top
           mirror of the arrow from the menu ... trace the icon to make our own hexagon pointer that blinks
           rapidly"). The ring is traced off the badge's OWN alpha, so it is a hexagon because the badge is. */
        if(F.row===1 && disc[F.esel]===el){
          forgeHexPointer('inf_'+el,ecx,ecy,eh,INFUSIONS[el].glow||'#ffffff');
          forgeSelArrowUp(ecx, ecy+eh*0.56, Math.min(EH*0.24, eh*0.34));
        }""")
# (c) row 0 FIRE: straight to the element row - the weapon list lives on the LOADOUT screen now
rep("""      else { F.row=2; F.psel=Math.max(0,F.pool.indexOf(selW)); F.pscroll=0; blip(); }
    }""", """      /* the weapon LIST moved to its own LOADOUT screen (0917b) - here a slot goes straight to its elements */
      else if(!forgeCanTake(selW)) forgeSay(WEAPONS[selW]+' CANNOT TAKE AN ELEMENT','blocked');
      else if(!disc.length) forgeSay('NO COMBINATION FOR THIS WEAPON YET - BEAT A BOSS','blocked');
      else if((run.forgeCombos|0)<=0) forgeSay('NO COMBINES LEFT THIS STAGE','blocked');
      else { F.row=1; const f=forgeEntry(selW); F.esel=f?Math.max(0,disc.indexOf(f.elem)):0; blip(); }
    }""")
# (d) element FIRE: the weld is its own screen now
rep("""      if(r==='ok'){ const f=forgeEntry(selW); forgeSay(forgeName(selW)+'   LEVEL '+f.lv+'   -   COMBINES LEFT: '+(run.forgeCombos|0),'powerup'); F.row=0; }""",
"""      if(r==='ok'){ const f=forgeEntry(selW); F.row=0;
        /* the combine is committed HERE (so the word is known) and then WELDED on screen (0917b) */
        forgingStart({w:selW, elem:el, lv:f.lv}); return; }""")
# (e) START goes to the loadout (the callback is it); the hints say so
rep("""                 :[['pad_a','SELECT SLOT'],['pad_x','RE-SPEC'],['pad_y','ARMORY'],['pad_start','CONTINUE']];""",
    """                 :[['pad_a','SELECT SLOT'],['pad_x','RE-SPEC'],['pad_y','ARMORY'],['pad_start','LOADOUT']];""")
rep("""    else if(F.row===2) l2='SLOT '+(F.sel+1)+':  UP / DOWN SCROLL   -   FIRE PICKS   -   BACK KEEPS '+WEAPONS[selW];
""", "")
rep("""    else l2='FIRE: COMBINE THE '+WEAPONS[selW]+' WITH AN ELEMENT';""",
    """    else l2='FIRE: FORGE THE '+WEAPONS[selW]+' WITH AN ELEMENT';""")

# ---------------------------------------------------------------- E11 the conversion on the debrief
rep("""    const mW=b[2]*0.92;
    let H=ph2*0.022;
    for(;H>ph2*0.009;H-=0.3){ if(stageWrapCount(art,msg,H,mW,0.05)*H*1.32 <= b[3]*0.88) break; }
    const n=Math.max(1,stageWrapCount(art,msg,H,mW,0.05));
    stageWrapCen(art,msg,b[0]+b[2]/2,b[1]+b[3]/2-((n-1)*H*1.32)/2,H,mW,1.32,1,0.05);""",
"""    const mW=b[2]*0.92;
    /* ⚠ THE CONVERSION IS SAID ON THE DEBRIEF (Mike, 0917b: "end screen - currency conversion during end
       screen and stats given"). It used to be said only on the FORGE's brief line - a screen that skips
       itself whenever there is nothing to forge, so most clears converted in silence. Counted up after the
       stamp lands, over the level's own score, in the plate's sign-off bay above the send-off. */
    const _fp=run._fpLevel, _fk=Math.min(1,Math.max(0,(t-1.55)/0.9));
    let _mTop=b[1], _mH=b[3];
    if(_fp && (_fp.score|0)>0){
      const _n=Math.round((_fp.fp|0)*_fk), _sc=Math.round((_fp.score|0)*_fk);
      const conv='SCORE '+_sc.toLocaleString('en-US')+'   =   +'+_n+' FURIOUS PTS';
      const cH=Math.min(b[3]*0.40, (typeof stageFitH==='function')?stageFitH(art,conv,mW,b[3]*0.40,7,0.06):b[3]*0.36);
      stageText(art,conv,b[0]+b[2]/2,b[1]+b[3]*0.24,cH,'#ffd24a',0.9,1,0.06);
      if(_fk<1 && Math.floor(t*20)!==Math.floor((t-dt)*20) && Audio.SFX.blip) Audio.SFX.blip();
      _mTop=b[1]+b[3]*0.44; _mH=b[3]*0.56;
    }
    let H=ph2*0.022;
    for(;H>ph2*0.009;H-=0.3){ if(stageWrapCount(art,msg,H,mW,0.05)*H*1.32 <= _mH*0.88) break; }
    const n=Math.max(1,stageWrapCount(art,msg,H,mW,0.05));
    stageWrapCen(art,msg,b[0]+b[2]/2,_mTop+_mH/2-((n-1)*H*1.32)/2,H,mW,1.32,1,0.05);""")

# ---------------------------------------------------------------- the new beats
NEW = open(os.path.join(ROOT, '_BUILD_SOURCE', 'forge_sequence_0917b.js'), encoding='utf-8').read()
rep("""
function drawGameOver(dt){""", "\n" + NEW + "\nfunction drawGameOver(dt){")

open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('patched OK')
