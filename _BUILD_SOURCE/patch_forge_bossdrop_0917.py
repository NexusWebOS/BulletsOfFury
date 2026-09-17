#!/usr/bin/env python3
"""
patch_forge_bossdrop_0917.py - a COMBINATION is earned from the boss, not discovered in the field.

Mike, 0917: "Additionally, you dont unlock all these weapon combination upgrades. Your going to make
powerup upgrade's for these new weapon types that drop from the boss when they die at each level, and
thats how we gain new combinations and such."

THE RULE
  A combination is one ELEMENT on one WEAPON SLOT - FIRE on the machine gun is INCENDIARY SLUGS, and
  it is a different thing from FIRE on the laser. Until the pair is OWNED the Forge refuses it, and
  the only way to own one is to pick up the powerup a boss leaves when it dies.

WHAT THAT REPLACES
  `forgeDiscover(elem)` fired on any infusion pickup and licensed that element on ALL NINE slots at
  once, so one crate on stage 1 opened nine combinations. It still records what has been SEEN - the
  Forge greys an element it can name - but it no longer grants anything.

⚠ THE OWNERSHIP LIVES IN THE PROFILE, BESIDE THE ARMORY'S LEVELS, NOT ON `run`. A combination is
progression: it has to survive the run that earned it, or a boss drop is worth nothing the moment you
die. `forge_<elem>_<slot>_C` sits in the same `owned` store as `forge_<elem>_<slot>_L<n>`, is written
with NO `cost`, and is therefore invisible to furiousSpent and to the price ladder (a reward that
raised your prices would be a punishment).

⚠ AND THE ARMORY MAY NOT SELL A LEVEL OF A COMBINATION YOU CANNOT USE. Its rows for unowned pairs are
shown locked, saying where the pair comes from, and `forgeLevelBuy` refuses with 'locked' - the same
rule the Vault's undeliverable rows already follow (taking the points for something that does not
arrive is the one failure a derived balance cannot repair).

⚠ THE DROP IS GUARANTEED, ONE PER BOSS. "Thats how we gain new combinations" is a progression
promise, not a loot roll - a boss that sometimes pays nothing would stall the whole system behind
chance. It pays nothing only when there is nothing left to give.

Every edit is anchored on a single line of assets/game.js (LF) and refuses if the anchor is not found
exactly once.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'forgeComboId' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the combination, its store, and the boss's choice ---------------------------------------
rep("function forgeLevelId(elem,w,lv){ return 'forge_'+elem+'_'+(w|0)+'_L'+(lv|0); }\n",
    r"""function forgeLevelId(elem,w,lv){ return 'forge_'+elem+'_'+(w|0)+'_L'+(lv|0); }
/* ============================================================
   THE COMBINATION IS EARNED FROM THE BOSS (Mike, 0917)
   "you dont unlock all these weapon combination upgrades. Your going to make powerup upgrade's for
    these new weapon types that drop from the boss when they die at each level, and thats how we gain
    new combinations and such."
   One id per ELEMENT x SLOT, in the profile beside the Armory's levels, written with no `cost` so a
   free reward can never advance the price ladder or read as spending.
   ============================================================ */
const FORGE_COMBO_ID_RE=/^forge_[a-z]+_[0-9]_C$/;
function forgeComboId(elem,w){ return 'forge_'+elem+'_'+(w|0)+'_C'; }
function forgeComboOwned(elem,w){ return !!(INFUSIONS[elem] && forgeCanTake(w) && furiousOwned(forgeComboId(elem,w))); }
function forgeComboGrant(elem,w){
  if(!INFUSIONS[elem] || !forgeCanTake(w)) return 'unknown';
  const id=forgeComboId(elem,w);
  if(furiousOwned(id)) return 'owned';
  if(!achievementState.owned) achievementState.owned={};
  achievementState.owned[id]={at:Date.now()};   /* no cost: it was not bought */
  achievementSave();
  return 'ok';
}
function forgeCombosOwned(){
  const out=[]; const O=achievementState.owned||{};
  for(const id of Object.keys(O)){ if(!FORGE_COMBO_ID_RE.test(id)) continue;
    const m=/^forge_([a-z]+)_([0-9])_C$/.exec(id); if(!m) continue;
    if(!INFUSIONS[m[1]] || !forgeCanTake(+m[2])) continue;
    out.push({elem:m[1], w:+m[2]}); }
  return out;
}
/* what a slot may be combined with TODAY: owned, and past whatever gate the element carries */
function forgeElemsFor(w){
  if(!forgeCanTake(w)) return [];
  return Object.keys(INFUSIONS).filter(function(e){ return forgeComboOwned(e,w) && infusionGateOpen(e); });
}
/* every pair that could still be given. The weapon side is the UNLOCKED pool, never the whole table -
   a combination for a weapon the pilot cannot hold is a reward you cannot look at. */
function forgeComboCandidates(){
  const pool=(typeof crateWeaponPool==='function')?crateWeaponPool(true):FORGE_WEAPONS.slice();
  const ws=FORGE_WEAPONS.filter(function(w){ return pool.indexOf(w)>=0; });
  const out=[];
  for(const e of Object.keys(INFUSIONS)){
    if(!infusionGateOpen(e)) continue;
    for(const w of ws) if(!forgeComboOwned(e,w)) out.push({elem:e, w:w});
  }
  return out;
}
/* the boss's pick. Biased toward the stage's own element and toward the weapon in the player's hands,
   so the drop reads as belonging to the fight that paid for it rather than as a lottery ticket. */
function forgeComboRoll(){
  const C=forgeComboCandidates(); if(!C.length) return null;
  const bias=INFUSION_STAGE_BIAS[(run&&run.stage)|0]||null, held=(run&&run.weapon)|0;
  const pref=C.filter(function(c){ return c.elem===bias && c.w===held; });
  if(pref.length && Math.random()<0.50) return pref[(Math.random()*pref.length)|0];
  const be=C.filter(function(c){ return c.elem===bias; });
  if(be.length && Math.random()<0.55) return be[(Math.random()*be.length)|0];
  const bw=C.filter(function(c){ return c.w===held; });
  if(bw.length && Math.random()<0.40) return bw[(Math.random()*bw.length)|0];
  return C[(Math.random()*C.length)|0];
}
/* ⚠ GUARANTEED, ONE PER BOSS - see this patch's header. Returns the pickup, or null when every
   combination the player could use is already owned. */
function forgeBossDrop(x,y){
  if(typeof powerups==='undefined') return null;
  const c=forgeComboRoll(); if(!c) return null;
  const P={x:x, y:y, vy:0.85, t:0, kind:'forgecombo', elem:c.elem, fw:c.w, w:24, h:24, bob:rnd(0,TAU)};
  powerups.push(P);
  try{ if(typeof stageStats!=='undefined' && stageStats.pickupsSeen!=null) stageStats.pickupsSeen++; }catch(_fb){}
  try{ if(typeof XART!=='undefined'){ XART.rdy('inf_'+c.elem); if(typeof weaponIconKey==='function') XART.rdy(weaponIconKey(c.w,1,{bare:1})); } }catch(_fb2){}
  return P;
}
function forgeComboName(elem,w){
  const T=FORGE_NAMES[elem];
  return (T && T[w]) ? T[w] : (((INFUSIONS[elem]||{}).name||'')+' '+((typeof WEAPONS!=='undefined'&&WEAPONS[w])||'WEAPON'));
}
""")

# ---- 2. the Forge refuses a combination that is not owned ----------------------------------------
rep("  if(!INFUSIONS[elem] || !infusionGateOpen(elem)) return 'unknown';\n"
    "  if((run.forgeCombos|0)<=0) return 'spent';\n",
    "  if(!INFUSIONS[elem] || !infusionGateOpen(elem)) return 'unknown';\n"
    "  /* ⚠ THE PAIR HAS TO HAVE BEEN EARNED. This is Mike's whole rule: a combination comes off a boss,\n"
    "     so an element you have merely SEEN cannot be welded onto a slot you never won it for (0917). */\n"
    "  if(typeof forgeComboOwned==='function' && !forgeComboOwned(elem,w)) return 'locked';\n"
    "  if((run.forgeCombos|0)<=0) return 'spent';\n")

# ---- 3. a field pickup records what was SEEN, and grants nothing ---------------------------------
rep("/* an element is DISCOVERED when one of its pickups is collected in play */\n"
    "function forgeDiscover(elem){ if(run && INFUSIONS[elem]){ if(!run.forgeElems) run.forgeElems={}; run.forgeElems[elem]=1; } }\n"
    "function forgeDiscovered(){\n"
    "  if(!run || !run.forgeElems) return [];\n"
    "  return Object.keys(INFUSIONS).filter(function(e){ return run.forgeElems[e] && infusionGateOpen(e); });\n"
    "}\n",
    "/* an element is SEEN when one of its pickups is collected in play. ⚠ SINCE 0917 THIS GRANTS\n"
    "   NOTHING - it used to license that element on all nine slots at once, which is exactly the\n"
    "   \"you dont unlock all these weapon combination upgrades\" Mike ruled out. The Forge uses it only\n"
    "   to show an element it can name; forgeElemsFor(w) is what may actually be combined. */\n"
    "function forgeDiscover(elem){ if(run && INFUSIONS[elem]){ if(!run.forgeElems) run.forgeElems={}; run.forgeElems[elem]=1; } }\n"
    "/* every element combinable on ANY slot right now - the union of the owned pairs, which is what a\n"
    "   screen asking \"is there anything to do here\" needs. */\n"
    "function forgeDiscovered(){\n"
    "  const seen={}, out=[];\n"
    "  for(const c of forgeCombosOwned()){ if(seen[c.elem] || !infusionGateOpen(c.elem)) continue; seen[c.elem]=1; out.push(c.elem); }\n"
    "  return out;\n"
    "}\n")

# ---- 4. the Armory refuses a level on an unowned pair --------------------------------------------
rep("  if(!INFUSIONS[elem]||!forgeCanTake(w)) return 'unknown';\n"
    "  const lv=forgeOwnedLevel(elem,w); if(lv>=INFUSION_MAX) return 'maxed';\n",
    "  if(!INFUSIONS[elem]||!forgeCanTake(w)) return 'unknown';\n"
    "  /* ⚠ A LEVEL OF A COMBINATION YOU DO NOT OWN IS AN UNDELIVERABLE SALE. The Vault's own rule\n"
    "     (0916): a row that cannot deliver must not take the points. */\n"
    "  if(typeof forgeComboOwned==='function' && !forgeComboOwned(elem,w)) return 'locked';\n"
    "  const lv=forgeOwnedLevel(elem,w); if(lv>=INFUSION_MAX) return 'maxed';\n")

# ---- 5. the profile keeps the combination ids ----------------------------------------------------
rep("    for(const id of Object.keys(v.owned)){ if(!FURIOUS_SHOP[id] && !FORGE_LEVEL_ID_RE.test(id)) continue; const q=v.owned[id]||{};\n"
    "      out.owned[id]={at:Number.isFinite(q.at)?q.at:0,cost:Number.isFinite(q.cost)?q.cost:((FURIOUS_SHOP[id]||{}).cost|0)}; }\n",
    "    for(const id of Object.keys(v.owned)){\n"
    "      if(!FURIOUS_SHOP[id] && !FORGE_LEVEL_ID_RE.test(id) && !FORGE_COMBO_ID_RE.test(id)) continue;\n"
    "      const q=v.owned[id]||{};\n"
    "      /* ⚠ A COMBINATION CARRIES NO `cost` AND MUST NOT GAIN ONE HERE. Defaulting it to 0 would be\n"
    "         harmless; defaulting it to a shop price would charge the player for a boss drop. */\n"
    "      if(FORGE_COMBO_ID_RE.test(id)){ out.owned[id]={at:Number.isFinite(q.at)?q.at:0}; continue; }\n"
    "      out.owned[id]={at:Number.isFinite(q.at)?q.at:0,cost:Number.isFinite(q.cost)?q.cost:((FURIOUS_SHOP[id]||{}).cost|0)}; }\n")

# ---- 6. the boss drops it ------------------------------------------------------------------------
rep("  run.score+=5000*run.stage; eBullets.length=0;\n",
    "  run.score+=5000*run.stage; eBullets.length=0;\n"
    "  /* THE COMBINATION POWERUP (Mike, 0917: \"drop from the boss when they die at each level, and\n"
    "     thats how we gain new combinations\"). Dropped where the boss died, before the cook-off\n"
    "     detonates the field, so it is visible for the whole of the death sequence. */\n"
    "  if(typeof forgeBossDrop==='function') try{ forgeBossDrop(boss.x, boss.y); }catch(_fbd){}\n")

# ---- 7. collecting it ----------------------------------------------------------------------------
rep("    case 'infuse':\n",
    "    case 'forgecombo': {\n"
    "      const _fc=(typeof forgeComboGrant==='function')?forgeComboGrant(p.elem,p.fw):'unknown';\n"
    "      if(_fc==='ok'){\n"
    "        if(typeof arcadeBanner==='function') arcadeBanner('NEW COMBINATION  -  '+forgeComboName(p.elem,p.fw));\n"
    "        else floatText(p.x,p.y,'NEW COMBINATION','#ffd45a');\n"
    "        /* it can be welded on at the next Forge; the round in hand is not changed here */\n"
    "        if(typeof forgeDiscover==='function') forgeDiscover(p.elem);\n"
    "        try{ Audio.SFX.life&&Audio.SFX.life(); }catch(_fg1){}\n"
    "      } else { floatText(p.x,p.y,'+250','#ffd45a'); if(typeof addScore==='function') addScore(250); }\n"
    "      break; }\n"
    "    case 'infuse':\n")

# ---- 8. drawing it -------------------------------------------------------------------------------
rep("    if(p.kind==='infuse'){\n",
    "    if(p.kind==='forgecombo'){\n"
    "      /* the ELEMENT badge with the WEAPON's own icon inside it - the two halves of the pair, so\n"
    "         what is on the ground says which combination it is rather than just \"an upgrade\" */\n"
    "      const I=(typeof INFUSIONS!=='undefined'&&INFUSIONS[p.elem])||null;\n"
    "      const col=I?I.glow:'#ffd45a';\n"
    "      ctx.save(); ctx.translate(p.x, yb+Math.sin((p.bob||0)+performance.now()/300)*2.8);\n"
    "      ctx.shadowColor=col; ctx.shadowBlur=18;\n"
    "      let drew=null;\n"
    "      if(typeof iconBlit==='function'){ try{ drew=iconBlit(ctx,'inf_'+p.elem,0,0,PICKUP_BOX*1.25,true); }catch(_fcb){ drew=null; } }\n"
    "      if(drew==null){ ctx.rotate(Math.PI/4); ctx.fillStyle=I?I.body:'#888'; ctx.fillRect(-11,-11,22,22);\n"
    "        ctx.strokeStyle='#101018'; ctx.lineWidth=2; ctx.strokeRect(-11,-11,22,22); ctx.rotate(-Math.PI/4); }\n"
    "      ctx.shadowBlur=0;\n"
    "      if(typeof iconBlit==='function' && typeof weaponIconKey==='function'){\n"
    "        try{ const _wk=weaponIconKey(p.fw,1,{bare:1}); if(_wk) iconBlit(ctx,_wk,0,0,PICKUP_BOX*0.62,true); }catch(_fcw){}\n"
    "      }\n"
    "      ctx.restore();\n"
    "      continue;\n"
    "    }\n"
    "    if(p.kind==='infuse'){\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: combinations are boss drops - owned per elem x slot, forge and armory gated, drop/collect/draw')
