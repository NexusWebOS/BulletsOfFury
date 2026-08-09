# BULLETS OF FURY — OFFICIAL ENEMY ROSTER
_Foundation doc for the Tier-4 roster/sprite/AI pass. Last built: drop 0720._

This maps every enemy across all 8 stages: stats, sprite source (vault pool), movement,
and fire AI. Use this as the spec when cleaning sprites and improving AI — one source of truth.

---

## 1. ENEMY CATALOG (base stats)

Stats are base values; actual HP = `ceil(base × DIFF.eHp)`, fire timing scaled by `DIFF.eFire`.

| type | w×h | HP | fireRate | score | role |
|------|-----|-----|----------|-------|------|
| drone       | 22×18 | 1  | 2.2  | 120 | cannon-fodder swarm, single downward shot |
| assault     | 30×30 | 3  | 1.5  | 300 | fighter, aimed triple |
| gunship     | 40×44 | 7  | 1.1  | 700 | heavy, 5-shot fan |
| turret      | 26×26 | 5  | 1.3  | 400 | emplacement, aimed 3-shot |
| mine        | 18×18 | 2  | — (no shoot) | 150 | drifts, detonates near player |
| octo        | 34×34 | 6  | 1.4  | 600 | spinner, 6-way radial |
| mech        | 30×34 | 8  | 1.2  | 800 | walker, aimed darts |
| tank        | 40×38 | 6  | 1.4  | 550 | ground, single shell (front turret) |
| htank       | 46×44 | 12 | 1.7  | 950 | heavy ground, 3-shell spread |
| frost       | 26×28 | 2  | 1.8  | 200 | ice drone, single ice shot |
| icegun      | 36×38 | 7  | 1.1  | 650 | ice fighter, 3-ice spread |
| cryo        | 34×30 | 5  | 1.5  | 600 | ice gunship, 3-ice fan |
| mgturret    | 34×34 | 7  | 0.72 | 500 | rapid MG emplacement, alternating mg/minigun |
| rockturret  | 38×38 | 11 | 1.9  | 800 | rocket emplacement, twin shells |
| microturret | small | ~4 | ~1.3 | ~200| tiny ground turret, fires straight up |

### Roster-only types (defined in jungle arsenal / special spawns)
These use custom AI phases rather than the generic fire switch:
- **topgun** — fast top-entry diver, twin MGs (`fk:'mg'`)
- **racer** — cross/curl/dive/flee phases, twin-gun burst + lock-on missile (`fk:'homing'`)
- **sideswirl** — side entry, one swirl loop, then dives at player
- **jetflyby** — banks across screen, rippling homing missiles 1-by-1, then exits
- **jungletank** — stage-1 tank variant (barrel blasts + missiles)
- **intcp** — interceptor
- **bomber** — drops bombs
- **stationship** — slow station craft (opener fodder)
- **shieldd** — shielded drone (`pat:'spin'`, spread)
- **turdrone** — turret drone
- **scout** — weaving scout
- **mdrone** — missile drone

---

## 2. SPRITE SOURCE — VAULT SYSTEM

Enemies do NOT have direct sprite keys. `spawnEnemy` assigns `base.art` from stage-themed
vault pools (gamecode ~1119). Sprites resolve per-stage automatically.

**Type → vault pool:**
- tank/htank → `TANKS_S1` (jungle) / `TANKS_S4` (airbase) / `TANKS_S5` (space)
- mgturret → `TURR_MG`, rockturret → `TURR_RK`, turret/turdrone/shieldd → `TURR_G`
- microturret → `[esturret1, esturret2, trt1]`
- assault/gunship/scout/intcp/bomber → `JETS` (or `SHIPS` on naval stage 3)
- drone/mine/mdrone/frost/octo/mech → `DRONES`
- icegun/cryo → `JETS` (ice-tinted)

**Stage-themed air pools** (`VAULT_AIR_STAGE`) — full damage-state units mixed per stage:
- S2 volcanic: nvy (gray) + ac mix
- S3 cryo: nvi (ice) + ac mix
- S4 airbase: nvg (green) + nvy3 + ac mix
- S5 space: nvp (purple) + ac mix
- S6 furious: nvp + ac mix
- **S1 jungle: deliberately absent — Mike-curated, DO NOT TOUCH**

Bosses use `VAULT_BOSS` (bz0-6). Minibosses use `esB_big1-6`.

---

## 3. MOVEMENT PATTERNS (usage counts)

| pattern | uses | behavior |
|---------|------|----------|
| sine    | 25 | horizontal weave while descending |
| skydive | 20 | dive to a target x, then level |
| ground  | 14 | ground-locked (turrets), scroll with terrain |
| weave   | 12 | S-curve descent |
| straight| 11 | straight down |
| dive    | 8  | steep dive at player |
| strafe  | 4  | side-to-side while firing |
| kamikaze| 2  | ram the player |

Special phased movers (own logic): racer (cross/curl/dive/flee), sideswirl, jetflyby (exit), topgun.

---

## 4. FIRE AI (gamecode ~3451)

Gate: `e.shoots` true, `fireCd` elapsed, `0 < y < VH*0.85`. Decker-cloak special
makes enemies rarely fire. `aimPlayer(x,y)` gives the aim angle.

**Fire-kinds (`e.fk`, priority path):**
- single / triple / aimed / spread / missile / bomb / radial
- **homing** (racer): twin-gun burst ×3, then 4th shot = lock-on missile
- **mg** (strafer): twin guns straight down, every 6th = lock-on missile
- **groundup** (tank): strong front-turret blast, every 3rd = lock-on missile

**Fallback (`switch(e.type)`):** drone/microturret/assault/gunship/turret/octo/mech/
mgturret/rockturret/tank/htank/frost/icegun/cryo — each hardcoded pattern above.

Helper fns: `aimPlayer`, `eShoot`, `eMissile`, `eTwinGuns`, `enemyLockOn`, `eTankBlast`, `eMG`.

---

## 5. PER-STAGE ROSTERS

### Stage 1 — JUNGLE (Mike-curated, authored) ✅
stationship → drone swarm → jungletank → racer → intcp → tank → racer-pair(X) →
mdrone → topgun → bomber → sideswirl → htank+microturret → turdrone → jetflyby →
racer swarm → jungletank+bomber → sideswirl+topgun+intcp → htank×2+jetflyby → finale.
**Identity: varied jungle arsenal. DO NOT MODIFY.**

### Stage 2 — IT'S HOT IN HERE (volcanic, authored) ✅
Kamikaze pressure + relentless divers. **No tanks.** drone/assault/topgun/mine/racer/
bomber/gunship/jetflyby/sideswirl + vKamikazePair waves. Identity: aggressive dive spam.

### Stage 3 — ICE STILL CAN'T SEE (cryo, authored) ✅
Weaving frost walls + strafing iceguns. frost/shieldd/turdrone/cryo/icegun/sideswirl/
topgun/mdrone/bomber/racer. Identity: cold squadrons, weave-heavy.

### Stage 4 — CROUCHING MISSILES (airbase, authored) ✅
Ground armor + missile rain. **Tanks live here.** microturret/drone/tank/mdrone/jetflyby/
assault/htank/intcp/stationship/topgun/gunship. Identity: armor + emplacements.

### Stage 5 — GOD HELP US ALL (deep space, authored) ✅
octo/mech weaves, mine belts, purple tech. drone/mine/octo/sideswirl/mech/gunship/racer/
topgun/jetflyby. Identity: space horrors, mine fields.

### Stage 6 — FURIOUS DEATH prelude (authored) ✅
Everything, fast and dense. topgun/kamikaze/racer/mech/jetflyby/shieldd/octo/assault/
mdrone/sideswirl/bomber/gunship/turdrone/drone. Identity: kitchen-sink gauntlet.

### Stage 7 — ⚠️ NO IDENTITY (generic fallback)
Falls through to generic timeline: drone/assault/gunship/mine spam. **NEEDS AUTHORING.**

### Stage 8 — ⚠️ NO IDENTITY (generic fallback)
Same generic timeline. **NEEDS AUTHORING.**

---

## 6. WORK QUEUE (this pass)

1. **[ ] Author stage 7 roster** — give it a theme + cast + pacing identity.
2. **[ ] Author stage 8 roster** — theme + cast + pacing (pre-finale intensity).
3. **[ ] Sprite cleanup pass** — audit vault pools per stage; fix any mis-themed/wrong-scale
   assignments; ensure damage states resolve. (Stage 1 untouched.)
4. **[ ] AI improvement pass** — per-stage behavior review:
   - smarter aim leading on higher difficulty?
   - pattern variety (currently sine-heavy: 25 sine vs 4 strafe)
   - fire-kind assignment review (which types use fk vs fallback)
   - stages 7-8 need distinct AI feel
5. **[ ] Miniboss bar art** (separate — needs dedicated art, pills were NOT it).

**Standing rules:** never touch stage 1; tanks only stages 1 & 4; verify numeric + visual
each change; no placeholder/procedural art (search vault first).
