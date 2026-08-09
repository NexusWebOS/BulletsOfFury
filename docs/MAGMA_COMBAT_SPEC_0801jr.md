# MAGMA COLOSSUS — COMBAT RULES & DEATH (Mike, drop 0801jr)

Recorded close to verbatim. Companion to `MAGMA_COLOSSUS_SPEC_0801iu.md`.

> "This is going to the best fucking bossfight of an AI game jam"

---

## PHASE 1 — THE SHIELD IS UP

While the shield is active (limbs alive), the torso cannot be hurt, and **every
weapon type behaves differently**:

| weapon | what happens |
|---|---|
| **missiles / bullets** | **DEFLECTED BACK AT YOU** |
| **lasers** | deflected — and the **beam STOPS at the point of contact** on the torso |
| **FIRE weapons** | **HEALS** whatever body part you hit |
| **fire on the TORSO** | the white turns **more REDDISH**, flashes **faster**, and eventually **he CHARGES and RAMS you — kill** |
| everything else | simply deflected back |

**Deflected shots can hurt you.** That is the point — attacking the shield is
punished, not just wasted.

### Attackable in phase 1
The **cannons, legs and arms**. The torso only opens once they are gone.

---

## PHASE 2 — THE CORE

Once every limb is destroyed:

- The **torso POWERS DOWN**, leaving it open
- **Only the CORE can be damaged**
- **Retina targeting the torso targets ONLY the core**
- The **head still cannot be attacked**
- **The core can only be damaged by MISSILES**

### The missile crate
A **missile box appears** — always a **10-missile crate**. It appears **every time**
this phase begins.

### The core's attack
It shoots **energy balls, faster now**. You dodge, barrel roll or manoeuvre around
them. **They are NOT shootable.**

### THE SHOOT SIGN
- Use the existing **Shoot sign**
- The letters **glow via pixel animation**, and it animates **FAST** — like it is
  literally shouting SHOOT
- It **anchors above the boss's head** while the retina is targeting the core
- When the **retina times out the sign goes away**, unless the torso is destroyed
  first

---

## THE TORSO'S DEATH

- The torso **falls and detaches from the head**
- It **blows up and bursts**, sending **armour fragments everywhere**
- Use the **armour palette on the debris chunks**
- A **giant pulsating ARMOUR shock ring**
- The **massive boss explosion NINE times** — not three — **all over, one by one, on
  tics**
- It **falls into the lava** as it bursts, with the rings

---

## PHASE 3 — THE HEAD

The head is now floating free and:

- **Flies erratically, trying to avoid you**
- Shoots **rapid orange/white CYCLOPS BEAMS from its eyes**
- **Kicks back every time it fires**
- The **eyes glow on every shot**
- **Another missile box, 10 missiles, always**
- You **need the missiles** to kill it
- The **Shoot sign** takes place again

---

## THE FINAL KILL

When the boss is at the HP where **the next missile will certainly kill it**:

1. The **Shoot sign** as always
2. **SLOW TIME** — like Freezer's time distortion
3. The **Matrix slow-down sound**
4. **ZOOM, and the camera anchors and follows that missile** all the way to the head
5. The **mech SCREAMS** as the missile is about to impact
6. **Shock ring explosion**, debris scatters, **parts of the head fall into the lava**
7. When the head hits the lava: **GIANT shock ring**, the **screen FLASHES WHITE**,
   then back to normal
8. The explosion sequence all around

---

## ART / SYSTEMS THIS NEEDS

- deflection: bullets and missiles reversed back at the player, able to damage them
- laser termination at the contact point on the torso
- fire-heals-limb rule, and the reddening/faster shield flash on the torso
- the ram-kill charge
- core-only damage gating, missile-only damage on the core
- retina retarget to the core
- 10-missile crate, spawned on both phase 2 and phase 3
- Shoot sign with fast pixel-glow letters, anchored above the head
- armour-palette debris chunks
- pulsating armour shock ring
- boss explosion x9 on tics
- cyclops eye beams (player laser art, orange/white swap), with kickback
- time distortion + Matrix sound + missile-follow camera on the final blow
- giant ring + white screen flash on the lava impact

---

# THE CANNONS (Mike, drop 0801jv)

## THE MUZZLES
The cannon holes **fill in with 16-bit pixel-shaded orange/white circles**. The
cannons then **charge and glow orange, with sound**, and fire **powerful lasers** —
use **Maverick's straight helix lasers, palette-swapped to orange/white**.

## THE FAN SWEEP
The cannons are anchored, so when one charges and releases:

- Imagine a **fold-out fan**, the fan part **facing south** like the cannon
- It goes **left to right** and **fires 3 times**
- **While FOLLOWING the player via the orbit tracker**, trying to hit them

## WHICH CANNON FIRES
- Player flies **LEFT** → the **left** cannon fires
- Player flies **RIGHT** → the **right** cannon fires
- Player stays **MIDDLE** → **both** fire

## THE COUNTERPLAY, AND THE PUNISH
The two cannons have **separate charge timers**. A smart player can **barrel roll
back and forth to interrupt the charge**.

**But the boss detects this** and retaliates with the **core attack** — the
orange-converted **helix ball**.

## THE OTHER CANNON MODES
- **Fireballs from the cannons** — the existing magma balls, launched in **spread
  volleys** like a shmup, from **one** cannon
- Meanwhile the **other cannon becomes a MINIGUN of magma balls**
- …while the **core charges its helix ball**

## THROUGHOUT THE FIGHT
- The **firewaves still come at you**
- **Powerup boxes** appear
- **Speed pills** appear
- **Every character may get their special ability box ONCE** during this fight,
  **before the halfway mark**

## ART THIS NEEDS
- muzzle-fill circles, 16-bit shaded, orange/white
- cannon charge glow, orange, with sound
- Maverick's helix laser palette-swapped orange/white
- the fan-sweep firing pattern (3 shots, left to right, orbit-tracked)
- magma-ball spread volley and minigun modes
- helix ball, orange/white (already specced in the core section)
