#!/usr/bin/env python3
"""patch_bossdrop_reach_0917.py - the combination drop was GUARANTEED and UNCATCHABLE.

Measured (probe_dropreach_0917.py, the real stage-1 boss death): the pickup existed for **0 frames**.
It was spawned at `boss.y` = 618.6 on a 512-tall playfield and the cull killed it on the frame it was
born. Every assertion about the drop passed - it existed, it named an unowned pair, it was at the
boss's position - and a player could never have touched one.

⚠ "THE PICKUP EXISTS" AND "THE PICKUP IS CATCHABLE" ARE DIFFERENT CLAIMS, and this file's own history
is full of the first one passing for the second. A reward on a 9-second boss cook-off has to survive
the cook-off.

TWO FAULTS, BOTH FIXED HERE

1. A BOSS'S `y` IS NOT WHERE IT IS DRAWN. `drawBoss` reads `boss._drawY` when it is set, and several
   rigs keep their logical y well outside the playfield. The drop now takes the DRAWN position and is
   clamped into the field, which is the same "world coordinate vs the one on screen" confusion this
   file records five times over, one layer along.

2. IT MUST NOT FALL AWAY WHILE THE BOSS IS STILL EXPLODING. It descends to a hover line at 58% of the
   playfield, holds there, and then drifts toward the player - a boss reward that waits, which is what
   every arcade game in this genre does with one. `_fcHold` is that behaviour, and it is exempt from
   the bottom cull for as long as it is the reward of a boss that has just died.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if '_fcHold' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. it spawns where the boss is DRAWN, inside the field --------------------------------------
rep("function forgeBossDrop(x,y){\n"
    "  if(typeof powerups==='undefined') return null;\n"
    "  const c=forgeComboRoll(); if(!c) return null;\n"
    "  const P={x:x, y:y, vy:0.85, t:0, kind:'forgecombo', elem:c.elem, fw:c.w, w:24, h:24, bob:rnd(0,TAU)};\n",
    "function forgeBossDrop(x,y){\n"
    "  if(typeof powerups==='undefined') return null;\n"
    "  const c=forgeComboRoll(); if(!c) return null;\n"
    "  /* ⚠ CLAMPED INTO THE PLAYFIELD, because a boss's own y is not where it is drawn: the stage-1\n"
    "     helicopter reports 618.6 on a 512-tall field, so the first build spawned this reward below the\n"
    "     screen and the cull killed it on frame one. Measured, not reasoned about. */\n"
    "  const _lo=(typeof camLeftX==='function')?camLeftX()+22:22, _hi=(typeof camRightX==='function')?camRightX()-22:VW-22;\n"
    "  x=clamp(Number.isFinite(x)?x:VW/2, Math.min(_lo,_hi), Math.max(_lo,_hi));\n"
    "  y=clamp(Number.isFinite(y)?y:VH*0.35, 40, VH*0.52);\n"
    "  const P={x:x, y:y, vy:0.85, t:0, kind:'forgecombo', elem:c.elem, fw:c.w, w:24, h:24, bob:rnd(0,TAU),\n"
    "           _fcHold:VH*0.58};   /* it descends to here and then WAITS - see this patch's header */\n")

# ---- 2. the boss hands it the DRAWN position -----------------------------------------------------
rep("  if(typeof forgeBossDrop==='function') try{ forgeBossDrop(boss.x, boss.y); }catch(_fbd){}\n",
    "  if(typeof forgeBossDrop==='function') try{ forgeBossDrop(boss.x, (boss._drawY!=null?boss._drawY:boss.y)); }catch(_fbd){}\n")

# ---- 3. it holds, then comes to the player -------------------------------------------------------
rep("    p.t+=dt; p.y+=p.vy; p.x+=Math.sin(p.t*3+p.bob)*0.4;\n",
    "    /* ⚠ THE BOSS REWARD WAITS. Everything else falls past the player and is gone; this one is the\n"
    "       only thing a whole boss fight paid for, and it arrives while the screen is still detonating.\n"
    "       It settles at its hover line and then closes on the player, so it cannot be lost to a timer. */\n"
    "    if(p._fcHold!=null){\n"
    "      p.t+=dt;\n"
    "      if(p.y<p._fcHold) p.y=Math.min(p._fcHold, p.y+p.vy);\n"
    "      else { p.vy=0;\n"
    "        const _T=(typeof targetShip==='function')?targetShip(p.x,p.y):player;\n"
    "        if(_T && !_T.dead){ const dx=_T.x-p.x, dy=_T.y-p.y, d=Math.hypot(dx,dy);\n"
    "          if(d>1){ const sp=Math.min(2.2, 0.45+d*0.012); p.x+=dx/d*sp; p.y+=dy/d*sp; } } }\n"
    "      if(p.flash>0) p.flash-=dt;\n"
    "    } else {\n"
    "    p.t+=dt; p.y+=p.vy; p.x+=Math.sin(p.t*3+p.bob)*0.4;\n"
    "    }\n")

# the two lines that followed the motion read p.flash / the missile scatter: keep them for the others
rep("    if(p._looseMissile&&p.t<.55){p.x+=p._scatterVx*dt*Math.max(0,1-p.t/.55);p.x=clamp(p.x,camLeftX()+12,camRightX()-12);}\n"
    "    if(p.flash>0) p.flash-=dt;\n",
    "    if(p._looseMissile&&p.t<.55){p.x+=p._scatterVx*dt*Math.max(0,1-p.t/.55);p.x=clamp(p.x,camLeftX()+12,camRightX()-12);}\n"
    "    if(p._fcHold==null && p.flash>0) p.flash-=dt;\n")

# ---- 4. and it is exempt from the bottom cull ----------------------------------------------------
rep("    if(p.y>VH+20) p.dead=true;\n",
    "    /* ⚠ THE BOSS REWARD IS EXEMPT FROM THE BOTTOM CULL. It holds inside the field and never\n"
    "       reaches this, but a rig that spawns it low would otherwise delete a guaranteed reward. */\n"
    "    if(p.y>VH+20 && p._fcHold==null) p.dead=true;\n"
    "    if(p._fcHold!=null) p.y=clamp(p.y, 24, VH-24);\n")

open(p, 'wb').write(s.encode('utf-8'))
print('patched: the combination drop lands in the field, waits, and comes to the player')
