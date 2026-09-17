#!/usr/bin/env python3
"""
patch_infusion_levels_0917.py - the forged rounds LOOK upgraded per level, I..V, like the base weapons do.

Mike, 0917: "like our previous level 1-5 variants, they should appear upgraded per each level even in
this new bullet elemental form or laser upgrade form. Just for extra graphical effect."

What a level adds, on top of the palette the element already wears (all additive, all cheap):
  II   an element-coloured GLOW plate under the round (a baked radial gradient, blitted 'lighter' at an
       integer origin - never shadowBlur: 0916ab measured 138 blurred draws a frame at 1.4 fps), and a
       sparse trail of element sparks behind it
  III  the glow grows and a second, wider faint halo joins it; the trail thickens
  IV   brighter still, the trail doubles, missiles/orbs/shards carry it too
  V    a pulsing four-point core flare on every round, the densest trail
  the BEAM: an element-coloured additive column under the authored beam that widens with the level,
       and from IV sparks crackle along the column
The level rides the round as b._infLv, stamped beside b._inf. Every edit is anchored on a single line
of assets/game.js (LF) and refuses if the anchor is not found exactly once.
"""
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = os.path.join(ROOT, 'assets', 'game.js')
s = open(p, 'rb').read().decode('utf-8')
assert '\r\n' not in s, 'game.js is LF'
if 'infusionAuraDraw' in s:
    print('already patched'); raise SystemExit(0)

def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, 'anchor found %d times (wanted %d): %r' % (c, n, old[:90])
    s = s.replace(old, new)

# ---- 1. the level rides the round ---------------------------------------------------------------------
rep("      b._inf=(typeof infusionActive==='function'&&infusionActive()&&infusionCarrier(b)&&!b._enemyReflected)?run.infusion.elem:null;\n",
    "      b._inf=(typeof infusionActive==='function'&&infusionActive()&&infusionCarrier(b)&&!b._enemyReflected)?run.infusion.elem:null;\n"
    "      b._infLv=b._inf?(run.infusion.lv|0):0;   /* the LEVEL rides the round too (0917): the aura and the trail read it */\n")

# ---- 2. the trail, spawned from the update loop (never the draw) --------------------------------------
rep("   /* +10% AND +1 a level: a 2-damage pellet rounds +20% away to nothing */\n",
    "   /* +10% AND +1 a level: a 2-damage pellet rounds +20% away to nothing */\n"
    "    }\n"
    "    /* THE LEVEL'S TRAIL (0917, Mike: \"they should appear upgraded per each level\"): element sparks\n"
    "       behind every carrier from level II, denser each level; the beam crackles along its column from IV.\n"
    "       Spawned HERE, from the update, so a paused or re-drawn frame never doubles it. Capped. */\n"
    "    if(b._inf && (b._infLv|0)>=2 && !b._child && !b.dead && particles.length<INF_TRAIL_CAP){\n"
    "      const _tl=INFUSIONS[b._inf]; if(_tl){\n"
    "        if(b.kind==='beam'){\n"
    "          if((b._infLv|0)>=4 && Math.random()<INF_BEAM_SPARK_P[b._infLv|0]){ const _bt=(b.top!=null?b.top:0), _bb=(b.bot!=null?b.bot:player.y-14), _bw=Math.max(6,b.w||14);\n"
    "            particles.push({x:b.x+rnd(-_bw*0.5,_bw*0.5),y:rnd(Math.min(_bt,_bb),Math.max(_bt,_bb)),vx:rnd(-1.4,1.4),vy:rnd(-0.8,0.8),t:0,life:rnd(0.14,0.26),r:rnd(1.2,2.2),color:chance(0.5)?_tl.glow:'#ffffff',_infTrail:1}); }\n"
    "        } else if(Math.random()<INF_TRAIL_P[b._infLv|0]){\n"
    "          particles.push({x:b.x+rnd(-2,2),y:b.y+rnd(-2,2),vx:-(b.vx||0)*0.12+rnd(-0.35,0.35),vy:-(b.vy||0)*0.12+rnd(-0.35,0.35),t:0,life:rnd(0.2,0.4),r:rnd(1.1,1.5+0.35*(b._infLv|0)),color:chance(0.55)?_tl.body:_tl.glow,_infTrail:1}); }\n"
    "      }\n"
    "    }\n"
    "    if(false){\n")

# ---- 3. the aura, drawn under every infused round ------------------------------------------------------
rep("  for(const b of pBullets){\n    if(b.kind==='yuriLightningOrb'||b.kind==='yuriLightningBolt'){\n",
    "  for(const b of pBullets){\n"
    "    /* THE LEVEL'S AURA (0917) - under the round, before any kind branch, so every carrier gets it */\n"
    "    if(b._inf && (b._infLv|0)>=2 && !(b._launchDelay>0) && typeof infusionAuraDraw==='function') infusionAuraDraw(b);\n"
    "    if(b.kind==='yuriLightningOrb'||b.kind==='yuriLightningBolt'){\n")

AURA = r"""
/* ============================================================
   THE LEVEL'S LOOK (Mike, 0917): "like our previous level 1-5 variants, they should appear upgraded per
   each level even in this new bullet elemental form or laser upgrade form. Just for extra graphical
   effect."

   Level I is the element's palette on the authored round (0917, unchanged). From II the round carries an
   additive GLOW PLATE in the element's glow colour - a radial gradient BAKED ONCE per element x level x
   size into a scratch canvas and blitted at an integer origin, which is the 0916ab discipline: the space
   stages ran at 1.4 fps on 138 shadowBlur'd draws a frame, and a baked halo is the same pixels at 60. III
   adds a wider faint halo, IV brightens, V adds a pulsing four-point core flare. The BEAM gets an additive
   element column under the authored plate that widens with the level. The TRAIL sparks are spawned from
   the update loop (see the stamp site), never from here.
   ============================================================ */
const INF_TRAIL_P=Object.freeze([0,0,0.16,0.28,0.42,0.58]);       /* trail spark chance per frame, by level */
const INF_BEAM_SPARK_P=Object.freeze([0,0,0,0,0.45,0.75]);        /* beam crackle chance per frame, by level */
const INF_TRAIL_CAP=520;
const INF_AURA_ALPHA=Object.freeze([0,0,0.30,0.42,0.54,0.66]);
const INF_AURA_SCALE=Object.freeze([0,0,1.35,1.65,1.95,2.25]);   /* plate radius as a share of the round's size */
const _infGlowCache={};
function infusionGlowPlate(elem,lv,r){
  const I=INFUSIONS[elem]; if(!I) return null;
  r=Math.max(4,Math.round(r/2)*2); lv=clamp(lv|0,2,INFUSION_MAX);
  const k=elem+'|'+lv+'|'+r; let c=_infGlowCache[k]; if(c) return c;
  const d=r*2+2; c=document.createElement('canvas'); c.width=d; c.height=d;
  const g=c.getContext('2d'); if(!g) return null;
  const grd=g.createRadialGradient(r+1,r+1,0,r+1,r+1,r);
  grd.addColorStop(0,I.glow||'#ffffff'); grd.addColorStop(0.35,I.body||I.glow||'#ffffff'); grd.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=grd; g.fillRect(0,0,d,d);
  /* the wider faint halo from III: a second, softer ring baked into the same plate */
  if(lv>=3){ const g2=g.createRadialGradient(r+1,r+1,r*0.55,r+1,r+1,r); g2.addColorStop(0,'rgba(0,0,0,0)'); g2.addColorStop(0.6,I.glow||'#ffffff'); g2.addColorStop(1,'rgba(0,0,0,0)');
    g.globalAlpha=0.22+0.06*(lv-3); g.fillStyle=g2; g.fillRect(0,0,d,d); g.globalAlpha=1; }
  _infGlowCache[k]=c; return c;
}
function infusionAuraDraw(b){
  const lv=clamp(b._infLv|0,2,INFUSION_MAX), I=INFUSIONS[b._inf]; if(!I) return;
  const pulse=0.86+0.14*Math.sin((b.t||0)*22+(b.x|0));
  if(b.kind==='beam'){
    /* the element COLUMN under the authored beam, widening with the level; the authored plate draws over it */
    const top=(b.top!=null?b.top:PLAY.y), bot=(b.bot!=null?b.bot:(player.y-14)), bw=Math.max(6,b.w||14);
    const ww=bw*(1.3+0.35*(lv-2))*pulse, a=INF_AURA_ALPHA[lv]*0.55;
    ctx.save(); ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=a;
    ctx.fillStyle=I.glow||'#ffffff'; ctx.fillRect(b.x-ww/2,Math.min(top,bot),ww,Math.abs(bot-top));
    if(lv>=3){ ctx.globalAlpha=a*0.5; ctx.fillStyle=I.body||I.glow; ctx.fillRect(b.x-ww*0.8,Math.min(top,bot),ww*1.6,Math.abs(bot-top)); }
    ctx.restore(); return;
  }
  const sz=Math.max(b.w||6,b.h||10), r=sz*INF_AURA_SCALE[lv]*0.5;
  const pl=infusionGlowPlate(b._inf,lv,r); if(!pl) return;
  const ox=Math.round(b.x-pl.width/2), oy=Math.round(b.y-pl.height/2);
  ctx.save(); ctx.globalCompositeOperation='lighter'; ctx.globalAlpha=INF_AURA_ALPHA[lv]*pulse;
  ctx.drawImage(pl,ox,oy);
  if(lv>=5){   /* the core flare: a four-point star, pulsing */
    const f=(sz*0.9+2)*(0.7+0.3*Math.sin((b.t||0)*30)); ctx.globalAlpha=0.55*pulse; ctx.strokeStyle='#ffffff'; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(b.x-f,b.y); ctx.lineTo(b.x+f,b.y); ctx.moveTo(b.x,b.y-f); ctx.lineTo(b.x,b.y+f); ctx.stroke(); }
  ctx.restore();
}
"""
rep("function infusionClear(){ if(run) run.infusion=null; }\n", "function infusionClear(){ if(run) run.infusion=null; }\n" + AURA.lstrip('\n'))

open(p, 'wb').write(s.encode('utf-8'))
print('patched: _infLv stamp, level trail + beam sparks, aura plates + beam column')
