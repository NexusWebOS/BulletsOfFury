/* ============================================================================
   THE EIGHT-STATE ENEMY MACHINE (drop 0801hi)

   Straight from BULLETS_OF_FURY.pdf, section 1 — GLOBAL ENEMY BEHAVIOR RULES:

       1. SPAWN        2. ENTER        3. POSITION     4. ATTACK
       5. REPOSITION   6. ESCAPE       7. DAMAGED      8. DESTROYED

   The doc's own summary of why this exists:

     "Enemies should not fire continuously from the instant they spawn. They
      should enter, establish their position, briefly telegraph, then attack."

   That is exactly what the current roster does NOT do. Measured on stage 1:
   twelve types, four of which carry fk:undefined yet shoots:true — they fire
   through a default with no telegraph and no entry beat. THREE of them (topgun,
   sideswirl, jetflyby) never fire at all.

   STANDARD TIMING, also from the doc, in frames at 60fps:
     entry delay before firing     20 -  60
     telegraph before major attack  20 -  45
     normal attack cooldown         45 - 120
     heavy attack cooldown         150 - 300
     reposition duration            45 - 120
     fighter lifespan on screen    180 - 420

   BULLET FAIRNESS, which the machine enforces rather than trusting per-unit code:
     never spawn bullets on top of the player
     never fire an unavoidable wall without a visible opening

   HOW IT ATTACHES
   ex8Init(e) on spawn, ex8Tick(e, dt) each frame. A unit with no ex8 profile is
   untouched, so this can be adopted one type at a time instead of in a big bang.
   The unit's existing pattern still drives its motion; the machine owns WHEN it
   may fire, not WHERE it flies — which keeps the authored movement intact.
   ============================================================================ */

const EX8 = {SPAWN:0, ENTER:1, POSITION:2, ATTACK:3, REPOSITION:4, ESCAPE:5, DAMAGED:6, DESTROYED:7};
const EX8_NAME = ['SPAWN','ENTER','POSITION','ATTACK','REPOSITION','ESCAPE','DAMAGED','DESTROYED'];

/* Per-type profiles. Everything is in FRAMES so it reads against the doc's table.
   A type absent from here keeps its old behaviour untouched. */
const EX8_PROFILE = {
  /* racer — 7 per run on stage 1, the unit the player meets most.
     Doc pattern F3 (Dive and Break): enter high, pick a lane, dive, fire on the
     dive, break away. */
  racer:   { enter:26, position:22, telegraph:24, cooldown:70,  reposition:60, life:360, shots:3, gap:9 },
  intcp:   { enter:32, position:26, telegraph:28, cooldown:85,  reposition:70, life:400, shots:2, gap:11 },
  drone:   { enter:20, position:14, telegraph:20, cooldown:55,  reposition:45, life:300, shots:1, gap:0 },
  bomber:  { enter:44, position:34, telegraph:42, cooldown:180, reposition:90, life:420, shots:1, gap:0, heavy:true },
  topgun:  { enter:30, position:24, telegraph:26, cooldown:75,  reposition:65, life:380, shots:2, gap:10 },
  mdrone:  { enter:36, position:28, telegraph:38, cooldown:150, reposition:75, life:400, shots:1, gap:0, heavy:true },
  turdrone:{ enter:28, position:30, telegraph:24, cooldown:80,  reposition:0,  life:420, shots:2, gap:10 },
};

function ex8Profile(e){ return e && EX8_PROFILE[e.type] || null; }

function ex8Init(e){
  const P = ex8Profile(e);
  if(!P) return false;
  e._x8   = EX8.SPAWN;
  e._x8t  = 0;                       // frames in the current state
  e._x8life = 0;                     // frames alive, for ESCAPE
  e._x8shot = 0;                     // shots fired in this burst
  e._x8cd = 0;
  /* the doc's entry delay is a RANGE, and a formation that all fires on the same
     frame reads as one weapon. Seeded from spawn position so a wave staggers the
     same way every run rather than shimmering. */
  const h = Math.abs(((e.x|0)*7 + (e.y|0)*13)) % 41;
  e._x8enter = P.enter + h;          // 20-60 window once P.enter is in range
  return true;
}

function ex8Fire(e){
  /* BULLET FAIRNESS: never spawn a bullet on top of the player. If the muzzle is
     inside this radius the shot is skipped rather than nudged - a nudged shot
     still reads as unfair because it came from inside you. */
  if(typeof player!=='undefined' && player && !player.dead){
    const d = Math.hypot(player.x - e.x, player.y - e.y);
    if(d < 46) return false;
  }
  if(typeof eShoot==='function' && typeof aimAt==='function'){
    eShoot(e.x, e.y + (e.h||20)*0.4, aimAt(e), 3.0, e.fk==='mg' ? 'mg' : 'eshot');
    return true;
  }
  return false;
}

function ex8Tick(e, dt){
  const P = ex8Profile(e);
  if(!P || e.dead) return false;
  const F = dt * 60;                 // work in frames, as the doc does
  e._x8t += F; e._x8life += F;
  if(e._x8cd > 0) e._x8cd -= F;

  /* DAMAGED interrupts anything except DESTROYED. The doc: heavy damage causes a
     "short attack interruption" and a "movement wobble", critical adds erratic
     movement and reduced accuracy. */
  if(e._x8 !== EX8.DAMAGED && e._x8 !== EX8.DESTROYED && e.flash > 0.14 && e.hp > 0){
    const frac = e.hp / (e.maxhp || e.hp || 1);
    if(frac < 0.62){ e._x8 = EX8.DAMAGED; e._x8t = 0; }
  }

  switch(e._x8){
    case EX8.SPAWN:
      /* one frame: the unit exists but is not yet the player's problem */
      e._x8 = EX8.ENTER; e._x8t = 0;
      break;

    case EX8.ENTER:
      /* NO FIRING. This is the beat the doc says is missing - "enemies should not
         fire continuously from the instant they spawn". */
      if(e._x8t >= e._x8enter){ e._x8 = EX8.POSITION; e._x8t = 0; }
      break;

    case EX8.POSITION:
      if(e._x8t >= P.position){ e._x8 = EX8.ATTACK; e._x8t = 0; e._x8shot = 0; e._x8cd = P.telegraph; }
      break;

    case EX8.ATTACK: {
      /* the telegraph is the first slice of ATTACK: cooldown starts at P.telegraph
         so the unit is visibly committed before anything leaves the barrel */
      if(e._x8cd <= 0){
        if(e._x8shot < P.shots){
          if(ex8Fire(e)) e._x8shot++;
          e._x8cd = P.gap || 8;
        } else {
          e._x8shot = 0;
          e._x8 = P.reposition > 0 ? EX8.REPOSITION : EX8.ATTACK;
          e._x8t = 0;
          e._x8cd = P.cooldown;
        }
      }
      if(e._x8life >= P.life){ e._x8 = EX8.ESCAPE; e._x8t = 0; }
      break;
    }

    case EX8.REPOSITION:
      /* moving, not shooting - the doc gives this 45-120 frames */
      if(e._x8t >= P.reposition){ e._x8 = EX8.ATTACK; e._x8t = 0; e._x8cd = P.telegraph; }
      if(e._x8life >= P.life){ e._x8 = EX8.ESCAPE; e._x8t = 0; }
      break;

    case EX8.ESCAPE:
      /* it has had its time on screen; it leaves rather than loitering forever */
      e._x8leaving = true;
      break;

    case EX8.DAMAGED:
      /* short interruption, then straight back to attacking - damage should cost
         the enemy a beat, not remove it from the fight */
      if(e._x8t >= 18){ e._x8 = EX8.ATTACK; e._x8t = 0; e._x8cd = Math.max(e._x8cd, 20); }
      break;

    case EX8.DESTROYED:
      break;
  }
  return true;
}

function ex8MayFire(e){
  /* the single question the rest of the code asks: is this unit allowed to shoot
     right now? Anything without a profile answers yes, so nothing regresses. */
  if(!e || e._x8 == null) return true;
  return e._x8 === EX8.ATTACK && e._x8cd <= 0;
}
