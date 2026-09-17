#!/usr/bin/env python3
"""
patch_stylish_0917.py - 250 a pickup, and the STYLISH! award for dodging on the manoeuvre.

Mike, 0917: "Collecting items, powerups and special abilities also gives you points like 250 each.
Somersalting, or barrel rolling before a projectile would've impacted you grants you a 'Stylish!'
award of 500 points that appears letter by letter and glows before fading away letter by letter."

1. THE PICKUP IS 250, AND IT MOVES INTO `applyPowerup`
   It was 50, written at the ONE collision that awards it - which excludes the crate, the capsule and
   the missile-box routes by name, and those call `applyPowerup` from elsewhere. Scoring inside
   applyPowerup pays every route the same and cannot drift again. ⚠ It stays inside the seat window
   it was already in, so in co-op the score still goes to the player who flew into it.

2. "WOULD'VE IMPACTED YOU" IS EXACTLY MEASURABLE, BECAUSE THE MANOEUVRE'S I-FRAMES ARE WHAT SPARE YOU
   A roll and a somersault both set `player.invuln` for their whole duration, and the enemy-bullet
   loop returns on `invuln>0` BEFORE it tests the hitbox - so a round that would have hit is a round
   that overlaps the hitbox during those frames. The test goes in front of that early return, gated on
   `player.roll || player.somer`, so ordinary post-hit or respawn i-frames - where you were NOT being
   stylish, you were being lucky - award nothing.
   ⚠ ONE AWARD PER MANOEUVRE, NOT PER ROUND. A roll through a curtain of twenty rounds would otherwise
   pay 10,000 points, which is more than the level converts. The flag lives on the manoeuvre object,
   so it dies with it and the next roll can earn again.
   ⚠ AND IT IS NOT THE CHARGE DASH. Mike named the somersault and the barrel roll; Juggernaut's dash
   is already a damage move with its own reward.

3. THE AWARD IS TYPED IN AND ERASED THE SAME WAY - letter by letter, in, then out, glowing in between.
   `STYLISH_*` are the three beats. It draws in SCREEN space over the field, so it is not carried off
   by the scroll while it is being read.
   ⚠ The stage faces have no exclamation mark on every sheet and a missing glyph draws a SPACE
   (0903's CHOO E YOUR PILOT, 0906g's arrows) - the word is drawn without one and the +500 carries
   the punch instead.

Every edit is anchored on a single line of assets/game.js (LF) and refuses if the anchor is not found
exactly once.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'STYLISH_SCORE' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the pickup is worth 250, scored where every route passes -------------------------------
rep("function applyPowerup(p){\n",
    "/* WHAT A PICKUP IS WORTH (Mike, 0917: \"Collecting items, powerups and special abilities also gives\n"
    "   you points like 250 each\"). Scored HERE rather than at the touch collision, because that one\n"
    "   excludes the crate, the capsule and the missile boxes by name and they reach this function by\n"
    "   other routes - the old 50 was paid on some collections and not others. */\n"
    "const PICKUP_SCORE=250;\n"
    "function applyPowerup(p){\n"
    "  if(run) run.score=(run.score|0)+PICKUP_SCORE;\n")
rep("{ applyPowerup(p); run.score+=50; return true; }",
    "{ applyPowerup(p); return true; }   /* applyPowerup scores it - PICKUP_SCORE (0917) */")

# ---- 2. the award ------------------------------------------------------------------------------
rep("function chargeAvailable(){\n",
    r"""/* ============================================================
   STYLISH! (Mike, 0917)
   "Somersalting, or barrel rolling before a projectile would've impacted you grants you a 'Stylish!'
    award of 500 points that appears letter by letter and glows before fading away letter by letter."
   ============================================================ */
const STYLISH_SCORE=500, STYLISH_IN=0.42, STYLISH_HOLD=0.70, STYLISH_OUT=0.42;
let stylish=null;
function stylishManoeuvre(){ return (typeof player!=='undefined'&&player) ? (player.roll||player.somer||null) : null; }
/* ⚠ ONE PER MANOEUVRE - see this patch's header. The flag rides the roll/somersault object, so it is
   gone the moment that object is, and the next one can earn again. */
function stylishAward(x,y){
  const m=stylishManoeuvre(); if(!m || m._styl) return false;
  m._styl=true;
  if(run) run.score=(run.score|0)+STYLISH_SCORE;
  stylish={t:0, x:(x!=null?x:VW/2), y:(y!=null?y:VH*0.42), n:0};
  try{ (Audio.SFX.arcBarrelRoll||Audio.SFX.select||function(){})(); }catch(_sa){}
  return true;
}
/* a round that overlaps the hitbox while the manoeuvre's i-frames are up is a round that WOULD have
   impacted - that is the whole claim, and it is why this is called in front of the loop's own
   `invuln>0` return rather than after it. */
function stylishCheck(b){
  if(!b || b.dead || typeof player==='undefined' || !player || player.dead) return false;
  if(!stylishManoeuvre()) return false;
  const _hx=(player._hx!=null?player._hx:9), _hy=(player._hy!=null?player._hy:10);
  if(Math.abs(b.x-player.x)>=(_hx+(b.w||6)*0.15) || Math.abs(b.y-player.y)>=(_hy+(b.h||6)*0.15)) return false;
  return stylishAward(player.x, player.y-34);
}
function stylishTick(dt){
  if(!stylish) return;
  stylish.t+=dt;
  if(stylish.t>=STYLISH_IN+STYLISH_HOLD+STYLISH_OUT) stylish=null;
}
/* typed in, held glowing, then erased from the front - the same order it arrived in */
function stylishDraw(){
  if(!stylish) return;
  const W='STYLISH', n=W.length, t=stylish.t;
  let shown=n, gone=0;
  if(t<STYLISH_IN) shown=Math.min(n, Math.floor((t/STYLISH_IN)*n)+1);
  else if(t>=STYLISH_IN+STYLISH_HOLD) gone=Math.min(n, Math.floor(((t-STYLISH_IN-STYLISH_HOLD)/STYLISH_OUT)*n)+1);
  if(gone>=n) return;
  const art=(typeof curFontArt==='function')?curFontArt():null;
  const H=22, glow=0.55+0.45*Math.sin(t*9.0);
  const txt=W.slice(gone, shown);
  if(!txt) return;
  ctx.save();
  ctx.textAlign='center';
  /* the glow is a second pass at a larger size and low alpha, never shadowBlur: 0916ab measured what
     a per-draw blur costs, and this draws every frame it is up. */
  if(art && typeof stageText==='function'){
    stageText(art, txt, stylish.x, stylish.y, H*1.14, '#ffd45a', 0.85, 0.22*glow, 0.06);
    stageText(art, txt, stylish.x, stylish.y, H, '#fff6d0', 0.85, 1, 0.06);
    if(t>=STYLISH_IN && gone===0) stageText(art, '+'+STYLISH_SCORE, stylish.x, stylish.y+H*1.15, H*0.62, '#ff8a3a', 0.85, 1, 0.06);
  } else {
    ctx.globalAlpha=0.30*glow; ctx.fillStyle='#ffd45a'; ctx.font='bold '+Math.round(H*1.14)+'px "BOFmil", monospace';
    ctx.fillText(txt, stylish.x, stylish.y);
    ctx.globalAlpha=1; ctx.fillStyle='#fff6d0'; ctx.font='bold '+Math.round(H)+'px "BOFmil", monospace';
    ctx.fillText(txt, stylish.x, stylish.y);
    if(t>=STYLISH_IN && gone===0){ ctx.fillStyle='#ff8a3a'; ctx.font='bold '+Math.round(H*0.62)+'px "BOFmil", monospace'; ctx.fillText('+'+STYLISH_SCORE, stylish.x, stylish.y+H*1.15); }
  }
  ctx.restore();
  ctx.textAlign='left';
}
function chargeAvailable(){
""")

# ---- 3. the hook, in front of the loop's own invuln return --------------------------------------
rep("      if(withSeat(_s, function(){\n"
    "      if(player.dead || player.invuln>0) return false;\n",
    "      if(withSeat(_s, function(){\n"
    "      /* ⚠ BEFORE THE i-FRAME RETURN, ON PURPOSE. A roll and a somersault spare you by setting\n"
    "         `invuln`, so the round that would have hit you is only visible on this side of it (0917). */\n"
    "      if(typeof stylishCheck==='function' && stylishCheck(b)) { /* the dodge is scored; the round flies on */ }\n"
    "      if(player.dead || player.invuln>0) return false;\n")

# ---- 4. the clock and the draw -------------------------------------------------------------------
rep("  for(const f of floaters){ f.t+=dt; if(f.score){",
    "  if(typeof stylishTick==='function') stylishTick(dt);\n"
    "  for(const f of floaters){ f.t+=dt; if(f.score){")
rep("  /* the pickup announcement, over the field and in screen space (drop 0811m) */\n"
    "  if(typeof drawArcadeBanner==='function') drawArcadeBanner();\n",
    "  /* the pickup announcement, over the field and in screen space (drop 0811m) */\n"
    "  if(typeof drawArcadeBanner==='function') drawArcadeBanner();\n"
    "  if(typeof stylishDraw==='function') stylishDraw();\n")

# ---- 5. it does not survive the stage that earned it ---------------------------------------------
rep("  if(run) run._fpLevelDone=false;   /* a new level may convert again (0917) */\n",
    "  if(run) run._fpLevelDone=false;   /* a new level may convert again (0917) */\n"
    "  stylish=null;\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: PICKUP_SCORE 250 in applyPowerup, STYLISH award + typed-in/typed-out draw')
