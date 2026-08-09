/* ============================================================================
   DEATH FX, WIRED (drop 0801hy)

   Mike's description of what a death should be:

     "when enemies blow up and die, you got our shockwave ring, the explosive
      effect which now triples 1 by 1 fast so you can cover the whole sprite in
      various sectiosn while still being 25% scaled larger than the actual unit of
      the enemy were blowing up, and then the debris that goes everywhere."

   MEASURED BEFORE: a death produced 1 explosion, a few secondaries, some
   particles - and ZERO rings and ZERO debris. There was no ring system in the
   game at all, and the 1024-key debris library was not referenced by anything.

   THE THREE BEATS
   1. RING     one shock ring, tinted to the damage flavour
   2. TRIPLE   three blasts fired 1-by-1 about 55ms apart, offset across the
               sprite so they cover it in sections rather than stacking on the
               centre. The 25% oversize rule still applies to each.
   3. DEBRIS   chunks from the master library, coloured to the unit's own hull and
               sized by how big the unit was.

   RING FLAVOUR follows the element that killed it where that is known, and the
   stage otherwise - ice stages throw frost, stage 7 throws toxic, space throws
   the comet ring, everything else fire.
   ============================================================================ */

let shockRings = [];

/* which ring a death should throw */
function ringFlavourFor(e, cls){
  if(typeof run==='undefined') return 'fire';
  if(e && e._frozen) return 'frost';                 // killed by ice breath
  if(run.stage===3) return 'frost';
  if(run.stage===7) return 'toxic';
  if(run.stage===5) return 'comet';
  return 'fire';
}

/* the debris palette for a unit, from the library Mike specified */
function debrisRampFor(e, cls){
  const t = String((e && e.type) || '');
  if(cls==='boss' || cls==='mini') return (run && run.stage===6) ? 'bossbl' : 'bossgr';
  if(cls==='boat' || cls==='mboat') return 'navy';
  if(/tank|crawler|apc|halftrack|turret/.test(t)) return (run && run.stage===2) ? 'khaki' : 'olive';
  return (run && run.stage===6) ? 'slate' : 'steel';   // jets and everything airborne
}

function debrisTypeFor(cls){
  if(cls==='boss' || cls==='mini') return 'boss';
  if(cls==='boat' || cls==='mboat') return 'boat';
  if(cls==='tank' || cls==='turret') return 'tank';
  return 'jet';
}

function spawnShockRing(x, y, r, flavour){
  shockRings.push({x, y, t:0, life:0.42, r0:Math.max(8, r*0.30), r1:Math.max(20, r*1.35),
                   fam:'nsr_'+(flavour||'fire')});
}

function updateShockRings(dt){
  for(let i=shockRings.length-1;i>=0;i--){
    const s=shockRings[i];
    s.t += dt;
    if(s.t >= s.life) shockRings.splice(i,1);
  }
}

function drawShockRings(){
  if(typeof XART==='undefined') return;
  for(const s of shockRings){
    const f = clamp(s.t/s.life, 0, 1);
    const k = s.fam+'_'+clamp(Math.floor(f*8),0,7);
    if(!XART.rdy(k)) continue;
    const im = XART.get(k);
    const rad = s.r0 + (s.r1-s.r0)*f;
    const a = 1.0 - f*f;                      // holds bright, then drops off fast
    ctx.save();
    ctx.globalAlpha = a;
    ctx.globalCompositeOperation = 'lighter';
    ctx.drawImage(im, s.x-rad, s.y-rad, rad*2, rad*2);
    ctx.restore();
  }
}

/* THE DEBRIS. Size tier is chosen from how big the unit was, and every death
   throws a MIX - Mike wanted micro through medium, not one size. Wheels (chunk 5)
   and rollers (6) only come off tanks, and they leave in the four cardinal
   directions using the four authored rotations rather than a rotated draw. */
function spawnDeathDebris(e, cls){
  if(typeof XART==='undefined' || !e) return 0;
  const unit = Math.max(e.w||20, e.h||20);
  const ramp = debrisRampFor(e, cls);
  const typ  = debrisTypeFor(cls);
  const isTank = (typ==='tank');
  /* a small unit throws micro and tiny; a boss throws everything up to medium */
  let tiers;
  if(unit < 26)      tiers = ['micro','micro','tiny'];
  else if(unit < 46) tiers = ['micro','tiny','tiny','small'];
  else if(unit < 90) tiers = ['tiny','small','small','medium'];
  else               tiers = ['small','medium','medium','medium'];
  const n = Math.round(clamp(unit*0.22, 4, 18));
  let made=0;
  for(let i=0;i<n;i++){
    /* chunk 1-4 are body pieces, 7-8 fragments; 5 and 6 are wheels and rollers and
       are tank-only, which is what Mike asked for */
    let chunk;
    if(isTank && i<4) chunk = (i%2===0) ? 5 : 6;
    else chunk = [1,2,3,4,7,8][(Math.random()*6)|0];
    const rot  = (isTank && chunk>=5) ? (i%4) : ((Math.random()*4)|0);
    const tier = tiers[(Math.random()*tiers.length)|0];
    const key  = ramp+typ+chunk+'_r'+rot+'_'+tier;
    if(!XART.rdy(key)) continue;
    /* wheels leave along the cardinals, everything else scatters */
    let ang;
    if(isTank && chunk>=5) ang = (i%4)*(Math.PI/2) + rnd(-0.22,0.22);
    else ang = Math.random()*Math.PI*2;
    const spd = rnd(38, 118) * (tier==='micro'?1.35:tier==='tiny'?1.15:1.0);
    particles.push({
      x:e.x + rnd(-unit*0.30, unit*0.30),
      y:e.y + rnd(-unit*0.30, unit*0.30),
      vx:Math.cos(ang)*spd, vy:Math.sin(ang)*spd - rnd(6,26),
      t:0, life:rnd(0.55,1.15), _dbrKey:key, _spin:rnd(-5,5), _rot:Math.random()*6.28,
      kind:'debris'
    });
    made++;
  }
  return made;
}

function drawDeathDebris(){
  if(typeof XART==='undefined') return;
  for(const p of particles){
    if(!p._dbrKey || !XART.rdy(p._dbrKey)) continue;
    const im=XART.get(p._dbrKey);
    const f=clamp((p.t||0)/(p.life||1),0,1);
    ctx.save();
    ctx.globalAlpha = 1.0 - f*f;             // holds, then fades late
    ctx.translate(p.x, p.y);
    ctx.rotate((p._rot||0) + (p._spin||0)*(p.t||0));
    ctx.drawImage(im, -im.naturalWidth/2, -im.naturalHeight/2);
    ctx.restore();
  }
}
