# STAGE 1 COMBAT SPEC — Mike, drop 0801ib

Recorded verbatim in intent. Where I am unsure I have marked it **OPEN** rather
than guessing.

---

## QUAD LASER (miniboss)

- The sprite I showed was **wrong**. Need the **front-cannon-facing** one.
- **Keep the back-facing one** — this enemy is reused in another level.

---

## TANKS ON STAGE 1

**In play:**

| unit | sprite | role |
|---|---|---|
| jungle tank | tk4 (green) | main ground threat |
| tan tank | tk0 (orange/tan) | second ground unit |
| mini tank | tnkM_m1 | TINY tank, sand areas |
| mini tank | tnkM_m3 | TINY tank, sand areas — green camo |

The two mini tanks are **tiny**, belong in **any sand area**, and must be turned to
**face vertical**.

**Stored for later:** every other tank sprite.

### Per-unit attacks

**RED SCOUT TANK (tk5)**
- **fire-red muzzle flash**
- **dual flare** machine-gun projectile

**JUNGLE TANK (tk4)**
- **regular-coloured muzzle flash**
- fires a **fast tank rocket ONLY**
- **~3 second delay**, then fires again

### Rules for ALL tanks

- Move **only like a tank** — never wobble, never strafe sideways.
- **Slow.**
- **Shake while moving.**
- On firing: **kick back an inch or two AND shake.**

---

## JUNGLE OVERLORD-X (boss helicopter)

Mike: "the helicopter is good, but..."

### Weapons
- Not just homing rockets — **flurries of rockets you have to dodge like a fun shmup**
- Homing volley **puts a retina on the player**; those missiles **can be shot down**
  at regular speed, and there must **not be so many that it is unfair**
- **Machine gun muzzle flash at the front**
- **Burst fire of 8 machine-gun pellets**

### Movement
Follows the player left/right as an **orbit point** — it reads where you are and
tries to take you.

### THE LOOP

1. Flies in **from the top**
2. **Hovers / levitates**, flies a little
3. **Retina appears on the player**
4. **4 missiles from the LEFT side**, one by one, *very very very* short delay —
   **and 4 from the RIGHT at the same time**, also one by one
5. Homing **stops**
6. **Orbit-follows the player and burst-fires — 4 times**
7. After the 4th: **pause, levitate, fly UP off the screen**
8. **Charges at the player via orbit** — about **3 seconds to dodge**
9. Flies off the **bottom**
10. **Circles back from the side**, up to the top
11. **Levitates, pauses** — then back to step 3

### Random interrupt
From **each side**, a **"shotgun" triple regular-missile spread** — about **6
missiles spreading across the screen** — while it works the player with **machine
gun spread on the orbit system**.

### Half health
**Rams at the player.** Mike: "that works good, keep it in."

### DAMAGE STAGING

| HP | what shows |
|---|---|
| 50% | smoke sprites **layered on the back** (or wherever works) |
| 25% | **small explosion on the RIGHT side** + more smoke |
| 15% | **small explosion on the LEFT side** + more smoke on that side |
| 5%  | **multiple small explosions**, lots of smoke, **levitation goes frantic** |

### DEATH SEQUENCE

**No more fading bosses.**

- The full explosion sequence, PLUS
- **layer and explode over the unit in all 8 directions**, small delay between each,
  using the **boss** explosion family
- **the ring, multiple times**
- **lots of debris**
- "make this such a glorified and graphical sequence"

---

## OPEN

- Which sprite is the quad laser's front-cannon-facing plate (I showed the wrong one)
- Exact rocket speed for the jungle tank's "fast tank rocket"
- How many MG pellets in the "spread" during the shotgun interrupt
