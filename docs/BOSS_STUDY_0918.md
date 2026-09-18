# Boss Study 0918 — what makes a good boss fight, and what BOF should take from it

**Sources.** Frame-by-frame notes on seven boss videos. Six were sampled fully: Contra: Hard Corps (CHC), Contra III (C3),
Alien Soldier (AS), Sky Raptor (SR), Galaxy Attack on Hard (GA) and Mega Man X3 (X3). The notes are in the session
scratchpad as `bossvids/NOTES_*.md`. The seventh, the Fire Shark final boss (FS), was only partly sampled. Timestamps
below are video time from those notes. Everything is described in my own words.

**Context read:** `docs/WARHIVE_BOSS_0918.md`, `docs/WORK_ORDER_0914.md`, `CLAUDE.md`, and the live `bossDie` /
`updateBoss` death path in `assets/game.js`.

**How to read the tags in this document:**

| tag | meaning |
|---|---|
| **[HAVE]** | BOF already does this. The note says where. |
| **[PART]** | BOF does part of it. |
| **[NEW]** | Buildable with BOF's existing tools. |
| **[MIKE]** | A design call. Listed in §7 and not assumed anywhere in this document. |

**House rules that shape every recommendation:**

- **No boss splits.** "Parts falling off" becomes three things: a whole-plate damage-state swap, smoke and fire anchored
  to a point on the plate, and hit regions. Only the named exceptions exist: the Furnace Tyrant's head, the carrier bays
  and the Warhive's hit regions.
- **Shared warnings.** Every dangerous attack uses the shared green/yellow/red warning: the FOV cone plus the alert sign.
- **Homing is lock-bound.** Missiles steer only while the Retina lock holds.
- **Palette and luminance swaps only, never overlays.**
- **The player's death is fixed.** It is a spin-out with explosions anchored to the ship.

---

## 1. What makes a good boss fight (one page)

The seven games agree on more than they differ. Each principle below lists the sources that show it best.

**1. Telegraph with shapes in the world, not icons.**
The best tells are geometry the player can read against the playfield:
- C3's saucer throws a searchlight cone on the floor. It is literally BOF's FOV cone (C3 5:10).
- SR draws a 1–2 px guide line before every beam (SR 3:48) and puts a red triangle on the top edge above a missile's
  column (SR 17:05).
- GA runs a colour ramp on a charging core (GA 24:27).
- X3 grows an area hazard from a point before it can hurt (X3 9:30).

Tell lengths cluster tightly:
- 0.3–0.5 s for a body charge.
- 0.7–1.5 s for a beam.
- About 2 s for a screen-filling burst.

One grammar holds across all 30 SR fights, so once a player learns it, a new boss is readable on first sight.

**2. Commit at the start, then be dumb.** X3's fairness rule: an aimed move reads the player's position once, when it
starts, then follows a fixed path. It is smart when it chooses and dumb while it executes. BOF already has this in the
Nightwing's charge dash (aim committed at 60%) and in the Overlord's lane lock.

**3. Rhythm is attack → visible opening → attack.** Every good fight here shows its vulnerable window:
- CHC's ring shield fades (CHC 10:12).
- SR's armour opens, the boss is vulnerable, the armour closes (SR 12:56–13:17).
- The boss hits a wall and is stunned (X3 8:05).
- AS's cyan ghost is invulnerable and shows it (AS 19:26).

Two things make these windows work:
- **The punish window comes from the move's own physics** (overshoot, wall hit, reel-in), not from an idle timer.
- **Invulnerability is always drawn,** never hidden.

**4. Readability is colour discipline.**
- Each boss owns one dominant hue.
- Its bullets are that hue's complement, with a white core and a dark or glowing rim (GA, SR).
- The player's shots never share the boss's hue.
- Bullet shape encodes speed: round means slow, needles and arrowheads mean fast (GA §3).
- The background stays darker and lower-contrast than anything that can kill you.

**5. Escalate by reshaping, not by adding HP.** The late phases of the best fights change what the threat *is*:
- A debris storm (CHC B6).
- A shrinking arena (C3 B3b's spike ceiling).
- A swarm formation (CHC B26).
- A new axis (C3's final vertical chase).

AS introduces something new every 15–20 s, with a median fight length of about 55 s. The weak fights all break this rule:
- CHC B11 is 1:45 of repeating cycles.
- SR B6 and B15 are long, even attrition.
- GA's Hard mode stacks HP bars.

**6. The arena takes part.** The arena changes during the fight:
- A curving road (CHC B5).
- A bridge that sags (CHC B10).
- Sky that turns into space through a window (CHC B16).
- Missiles for a floor (C3 B6).
- Spikes that close the room (C3 B3b).
- Gravity flips (AS B16, B27).
- Water that drains (AS B24).

A phase change shown as a *world* change reads instantly.

**7. Mobility answers: take the position, don't chase.** AS's bosses face a very mobile player. They never copy the
player, and they never chase. They relocate: to the opposite side, off-screen, to another surface. They fill an axis
rather than a point (row attacks, beam lanes). They lag-aim instead of snap-aiming. For BOF's rolling and somersaulting
ship, this is the most transferable single idea.

**8. Show damage without a bar.** Even the games that have bars mostly show damage on the art:
- **Dead parts stay on the model.** Black pod husks, grey sockets and burning pits turn the boss into a record of the
  fight (SR B4, B5, B11, B14).
- **Palette state:** crimson means dying, all-red means charging, cyan ghost means invulnerable, bone grey means armoured
  (AS §3).
- **Heat pulse before death:** red-hot and normal alternate at 2–4 Hz (SR 4:29).
- **Silhouette loss:** the boss's outline shrinks (SR B20).
- **Countdown digits on the body** (CHC B23).
- **Explosions that keep erupting at the impact point** while you deal damage (CHC B9).

In BOF these become whole-plate state swaps plus anchored smoke. The Warhive's 75/50/25% plume ladder is already the
right shape.

**9. The death is its own phase.** It lasts 3–14 s, it has choreography, and the player usually keeps control. It
leads straight into the next beat:
- A pilot tumbles out (CHC B5).
- The scroll resumes (C3 gates).
- An exterior cutaway (CHC B17).
- A hangar splits and launches the next form (SR B5, which is BOF's own Warhive → Nightwing).

No great death is a dead end.

**10. Deliberate dead air.** Silence makes the next hit land:
- C3 holds 8 s of empty room before the skeleton bursts in.
- X3 freezes for 1.5 s on the killing blow.
- 2–3 s of quiet usually follows a death.

The quiet *is* the reward.

---

## 2. Per-game highlight reel

### Contra: Hard Corps (CHC) — the best source for staging and deaths
- **Signature death, 05:14–05:19 (B5 road walker).** The death has distinct stages:
  1. A dying-palette strobe.
  2. Radial shard streaks cross the whole screen.
  3. An implosion.
  4. A ring of fire dots becomes an arch, which collapses into a column, which becomes a torus.
  5. 0.7 s of full white.
  6. The screen fades back in with the pilot lying on the road.

  The same recipe reappears at 10:09 (B9), so it is a reusable effect, not a one-off.
- **The boss is built from parts, and the parts are the story.**
  - The walker loses its legs and becomes a pod (05:00).
  - Scrap assembles into a body, scatters as a *hazard storm*, and reassembles (05:39–06:10).
  - Three vehicles combine into four different mechs (37:57–39:51).
- **One unchanging weak point inside a changing shape (B8, 07:57–08:50).** It is a red core tile inside a formation that
  rearranges into a tank and a turret. When the formation shatters, the core drifts down like a falling leaf (08:45).
- **Colour means moveset (B12, 15:00–18:39).** Olive, then orange, then purple, then red, then blue. By the second cycle,
  each palette tells the player which attack set is coming.
- **The arena takes part in the fight.**
  - The rope bridge bows into a V (12:24).
  - Through the window, the sky climbs into space (29:03).
  - The train rounds a bend mid-fight and the boss reappears climbing the side (44:44).
  - The room mutates before a transformation (48:42).
- **Aftershock (26:52, 50:08).** Bands of explosions roll across the room *after* the victory banner, while the player
  walks out.
- **Exterior cutaway (31:46).** The space station is shown as a small sprite over Earth, wrapped in explosions, with a
  debris column falling. Then white, then glints over the horizon.
- **Pinwheel death (39:58).** A 2–3-arm spiral of explosion balls, white at the centre and red at the tips, rotating for
  about 2.7 s.
- **Lessons from the weak fights.**
  - B11 is 1:45 with no escalation.
  - B14 changes form so fast it can never be learned.
  - B25's hairline lasers are elegant and unreadable against a busy background (47:06).

### Contra III (C3) — telegraphs as world geometry, and a boss that lies about dying
- **A searchlight cone as the telegraph (B4, 5:10–5:30).** The cone sweeps. Bombs drop along its foot when it settles on
  the player. This is BOF's FOV cone exactly.
- **An entrance by breaking scenery (0:28–0:34, 6:48).**
  - The wall cracks into holes over 4 s, then the boss shoulders through.
  - In the second case, the torn wall reveals a starfield: the room was a ship.
- **Arena hazards belong to the boss (B3b, 4:18 and 4:46).**
  - Spike rows appear to shrink the climb range in phase 2.
  - They vanish in the same frame the boss dies.
- **Best death in the game, the colour window (B6, 10:04–10:10).**
  1. A circle grows from the core, palette-swapping everything inside it red, then yellow, then magenta.
  2. 4.6 s of full white.
  3. Shrinking hue circles, during which the bomber is swapped out of the scene.
- **The fake death (B10, 18:42–19:03).**
  1. The brain goes dull purple and the room explodes around it.
  2. The player is airlifted out.
  3. 4 s of empty room.
  4. The eye blinks once for a single frame.
  5. The brain snaps back to red and armour slams in from both sides.
  6. A new axis follows: a vertical chase, firing downward.
- **Heartbeat white-outs (19:41–20:00).** Single-frame white flashes about every 0.9 s through a long explosion field.
- **Deaths as gates (4:47, 5:39, 12:36).** The level just resumes scrolling, with no fade. Only stage bosses get the
  intermission.
- **Where the expert parked.** They held one spot in almost every fight: the upper balcony, directly under the head, the
  left edge. The bosses rarely took that spot away.

### Alien Soldier (AS) — the boss-rush template, and answers to a mobile player
- **The standard kill (B3, 1:44–1:52).**
  1. The boss recolours to burnt crimson and flickers against pink.
  2. The corpse *keeps fighting* for about 6 s while it explodes.
  3. A tint rises to pure white.
  4. The boss is gone.
  5. A flat ellipse left at its centre expands in dithered steps and cools from white through yellow, orange and red to
     gone.
  6. 1 s of silence, then the banner.
- **Relocation, not chasing.**
  - The totem ghosts to cyan (invulnerable), shears apart scanline by scanline, and rebuilds on the opposite side (B18,
    19:26–21:22).
  - The pod belt moves from the floor row to the ceiling row (B28, 32:02).
  - The wyvern spends most of its fight off-screen (B8).
- **Attacks that follow the player's position, with lag.**
  - A spark snake runs along the floor, then turns up at the player's x (21:12).
  - Final-boss pillars chase the player's x with a 0.5 s lag, behind an arrow glyph (34:04).
  - A web ring appears centred on the player as a net (17:11).
- **One creature, four bodies (B20–B23, 22:22–26:17).** Each kill cuts to a 1-bit frame: white ground, black
  silhouettes. Only the boss core's orange node dots keep their colour. Each time, the core visibly escapes to the next
  form.
- **The environment-changing kill (B24, 27:11).** A 1-bit freeze. Then the water is gone. Then a 10 s harmless explosion
  storm that the player flies through.
- **The timer is the second health bar.** It freezes on zero HP, and the time left becomes the bonus. Intros are about
  2 s. The next stage's title card arrives with no fade. This is the Boss Rush pacing model.
- **The delayed secondary death (B12, 12:19).** The boss is gone and there is 1.2 s of calm. Then the *boat* strobes red
  and explodes under the whole bonus count.

### Sky Raptor (SR) — the portrait vertical-shmup reference, and the Warhive's closest cousin
- **The carrier-dreadnought (B14, 17:36–18:36).** The beats run in order:
  1. It flies up from *below* the player and overtakes.
  2. Lock brackets flash around the player.
  3. It backs down tail-first.
  4. Side racks open.
  5. A hangar slot launches fighters.
  6. The racks die into grey puffing sockets.
  7. Cracks run down the spine.
  8. The hull **tilts and slides off to crash** instead of exploding.
  9. A small escape gondola is left as the last phase.
- **The hangar-split launch (B5, 6:46–6:52).**
  1. The fortress desaturates to dead grey.
  2. The hull splits like a hangar.
  3. A jet rolls out while the carcass scrolls away.
  4. The jet's wings unfold over 1.5 s.

  The player is never idle.
- **Dead parts stay attached and dark (B4, 4:21–4:24).** They read as a record of the fight. A part lost changes the
  pattern: two beam lanes become one (3:56).
- **The telegraph grammar.** A thin guide line comes 0.75–1.5 s before a beam (3:48, 25:54). A red triangle on the top
  edge warns of a missile column (17:05).
- **The pre-death heat pulse (4:29–4:32).** The hull alternates red-hot and normal every 0.25–0.5 s while still firing.
- **The signature pop.** A fireball is swapped in place for a black smoke puff, inside a double shockwave ring (0:51,
  4:35). It costs two sprites and it is the game's whole look.
- **Leftover missiles keep falling after the kill (17:18).** It is a residual danger after the victory.
- **Correction:** the player *does* die three times in this video (5:04, 28:00, 30:36). These fights are not trivial.

### Galaxy Attack, Hard (GA) — beam telegraph numbers and "Hard" by space, not density
- **The one-third beam (L35, 24:23–24:35).**
  1. The core ramps red, orange, yellow, white over about 0.9 s.
  2. A hairline runs to the player for about 0.7 s.
  3. The beam fires 25–30% of the screen wide, with the angle **locked** and no tracking, for 1.7 s.

  This is the exact template for the Warhive's Hard beam and for S3-12.
- **Breathing twin beams (L18, 9:09–9:19).** The two beams swing between a V and parallel on a 3–4 s cycle. The safe
  corridor narrows and widens. Sparse pellets inside the corridor stop the player from parking.
- **The lightning tether fence (L31 Electro, 18:46–18:53).** Two detached pods are joined by a tether that sweeps down the
  screen. Then four pods form a rotating lightning rectangle.
- **The phase change is always shown (L34 22:54, L35, L40 27:39).** Armour rips away, a shield bubble drops, wings
  sprout, or the background flashes.
- **"Hard" in this game.** Stacked HP bars, layered bullet speeds, and rings spawned around the boss before release.
  None of these is worth copying except the layered speeds.
- **A trap to avoid.** Deaths that leave live bullets on screen, or happen off-frame, or are just a smoke puff.

### Mega Man X3 (X3) — the duel rulebook, for the Nightwing Ace
- **The standard death (Blizzard Buffalo, 1:34–1:48).**
  1. **1.9 s freeze** on the last hit.
  2. The scene tints blue, then cyan, then white, with single-frame white strobes.
  3. The boss goes to a black silhouette on white.
  4. The silhouette **lightens** away (it is not alpha-faded).
  5. Explosions outlive the body by 1 s.
- **The two-step lock-on (Blast Hornet, 3:21).** A drone paints a reticle on the player first. Then the homing wave comes.
  This is BOF's Retina rule, seen from the other side.
- **Commit-then-execute plus a physical punish window.** Byte's shoulder charge ends stunned against the wall
  (8:05). The Hornet climbs back slowly after its dive.
- **Absorb-and-return (Doppler, 21:48–22:42).** A green aura soaks your shots and pays them back as a flaming dash. It
  punishes holding the fire button.
- **The vehicle blow-up that reveals the pilot (Goliath → Vile, 19:22–19:26).** Fire explosions, then white. The pilot
  fades in *during the grey return* where the armour stood.
- **The black-void rebirth (Sigma, 25:09–25:24).** Full black with only the player lit. Two glints in the dark. Then the
  giant.
- **The retreat ending (Bit, Byte, Vile 1).** The fight freezes, a line of dialogue, and the boss teleports out. This
  sets up a rematch.

### Fire Shark final (FS) — partial sample
A large armoured fortress with several turret pods firing arcs of cyan pellets and orange orbs.

- Its sections **go dark as they break.** This is the same "dead parts stay on the model" rule, and it maps directly onto
  BOF damage states.
- It dies to a **dark silhouette or afterimage.**
- The scroll then **cools down while a special-bonus tally counts off, and the level keeps scrolling.** The victory never
  stops the camera.

---

## 3. Graphical style notes

**Palettes.**
- One dominant boss hue on a desaturated or cool background (CHC, C3, AS).
- A single accent colour on the weak point: the red eye, red core or blue iris.
- The player sprite never shares the boss hue.
- BOF already works this way per stage (the 0905e rule: an alert must contrast with the *field*, keyed by family).
- The stage-2 arena dim at 0918c follows the same idea: the backdrop gives up luminance so the boss and its rounds read.

**Hit-flash conventions seen, and their BOF equivalents:**

| convention | source | BOF |
|---|---|---|
| 1-frame whole-sprite white | CHC B8, AS, C3 | [HAVE] `markHit` is called first in all three hit routers (0912y) |
| alternating with a "dead" palette every 2 frames | CHC B5, B23 | [NEW] cached `xartPalette` keys, toggled on a timer |
| flat single-colour silhouette fill (cyan) | X3 | [NEW] `xartPalette(key, hex)` — a hue swap that keeps luminance, so the shading survives |
| palette cycling, one palette per frame | CHC B1, B26 | [NEW] only for the final boss; cache 4–6 keys |
| crimson/pink at 6–10 Hz = dying | AS | [NEW] death-kit phase (§4 #6) |
| red-hot pulse at 4 Hz = about to blow | SR | [NEW] §4 #5 |

**Bullet readability.** Every source uses three rules:
1. A white or pale core.
2. A saturated rim.
3. A shape that encodes speed.

GA's colour discipline is the cleanest: one dominant bullet hue per boss, and a second hue only for the second pattern
layer. CHC's warning is the counter-example: hairline projectiles against busy art vanish.

BOF-specific traps:
- ⚠ Glow must be **baked**, never set with `shadowBlur` per projectile. 0916ab measured one per-round blur taking two
  stages to about 1–9 fps.
- ⚠ Enemy bullets are one hit and cost one pip, whatever the art. Size and shape are the only threat language available.

**Scale.**
- Bosses fill 40–100% of the screen.
- The biggest are longer than the screen and are **scrolled through** rather than framed (SR B5, B12, B14).
- Size is sold by cropping at the screen edge, not by scaling (C3).

BOF's Warhive at 461×259 on a 480-wide camera is in the right band.

**Showing state.** In order of how well each reads, with BOF's options:
- A whole-plate damage state: intact, damaged, critical, dead. [HAVE] on most bosses.
- Anchored smoke and fire per part by HP tier. [HAVE] on the Warhive. [NEW] everywhere else.
- A palette state: enrage red, invulnerable ghost, dying crimson. [PART] The Sovereign helpers' enrage red and the Furious
  black/blue plates exist.
- Parts going dark on a dead socket. [HAVE] the Warhive wreck plate.
- The pre-death heat pulse. [NEW]
- An arena change. [PART] the stage-2 dim.

---

## 4. Death & transition catalogue (merged, de-duplicated)

**BOF's building blocks,** all verified present in `assets/game.js`:

| tool | what it does |
|---|---|
| `explode(x,y,size,pal,kind,fam,cls)` | an explosion; `fam` from `BOSS_COMBO` = `nxp_dense`, `barrage`, `clus`, `radial`, `upward`, `white`, `ring`, `smoke` |
| `spawnShockRing(x,y,r,flavour)` | a ring over 0.42 s, family `nsr_<flavour>` |
| `fxBurst(x,y,size,{color,rings,chunks,sparks})` | rings, chunks and sparks in one call |
| `flashScreen` | decays on its own |
| `whiteBlast` | ⚠ **never decays on its own** (0917c). Set it and clear it explicitly. |
| `shake` | screen shake |
| `xartPalette(key, 'black' / 'white' / hex)` | cached luminance-preserving swaps |
| `weaponFeedbackArt(key,x,y,w,h,a,ang,add)` | anchored smoke, e.g. `nsd_chim_*` and `nxp_upward_*` |
| `_smokeRings` | angled flat smoke rings; the Hammer death uses crossed ones |
| `unitDeathFX` | a class death sized to the unit |
| `worldXformEscape` | for anything drawn in screen space |

⚠ **Anything drawn in screen space must subtract the camera.** This file records the world-vs-screen trap six times.

**What BOF's stock boss death already is** (`updateBoss`, dead branch, 9.4 s): explosions accelerate into a steady
rhythm, 60% of them inside the hull and 40% anywhere on the screen. Debris particles fall. The boss sinks slowly.
The shake ramps up. From 6.0 s the screen blooms to white, holds, and fades back while the boss is still coming apart.
On the kill, `bossDie` clears the enemy bullets and detonates every live enemy through its own class death. On stage 1
the dam is swapped under the peak white. `bossDeathAlpha`/`bossDeathChar` fade the draw. Several rigs have their own
deaths: the Warden, the stage-4 cook-off, the Hammer's rings, and the Warhive's fall and ace spin-out.

### The kill moment
1. **Kill freeze (hitstop).** [NEW]
   - Sources: X3 1.25–1.9 s; SR 0.3 s.
   - On the killing blow, hold every update except the audio for 0.25 s on Normal, or up to 0.8 s on a stage's final boss.
     Then start the cook-off.
   - Use its own `_killStop` counter checked at the top of `updatePlay`.
   - ⚠ **Not `timeScale`**: line ~33056 resets `timeScale<1` whenever Freezer's special is not active.
2. **Bullet clear on kill.** [HAVE] `bossDie` sets `eBullets.length=0`.
   - The SR/GA variant lets scripted missiles already in flight keep falling. See §5 #3.
3. **Field-wide detonation of leftover enemies.** [HAVE] `bossDie` runs `unitDeathFX` per unit.

### While it burns
4. **Explosion field inside the silhouette, plus screen saturation.** [HAVE]
   - Sources: CHC #1/#13, C3 #1, AS #1.
   - This is the existing cook-off. The only upgrade is to bias spawn points to the plate's *alpha mask* instead of the
     box, so a thin hull doesn't bloom into empty air.
5. **Heat-pulse countdown.** [NEW]
   - Source: SR 4:29.
   - Below 10% HP, and for the final 0.6 s before scripted deaths, alternate `xartPalette(plate, '#ff4a1a')` and normal
     every 0.25 s. Tighten to 0.12 s in the last 0.5 s.
   - This is a luminance swap, not an overlay, so it passes the rule.
6. **Dying palette strobe.** [NEW]
   - Sources: CHC #6, AS #2.
   - At 0 HP, toggle two cached keys every 3–5 frames for 1.5–2 s: a crimson (`#8a1a12`) plate and a pink (`#ff5a8a`)
     plate.
   - The X3 variant ramps the whole plate toward navy, then black (`xartPalette('black')`) as the white rises.
7. **Chain-pop walk-up.** [NEW]
   - Source: SR #1.
   - Before the big cook-off, fire 3–6 `explode(anchor, size 0.3–0.5×)` at the plate's **named mounts**, 0.2 s apart.
     Add a 2–3 px shake per pop.
   - It reads as the machine failing system by system. BOF's `shipBossMount` / `_mounts` already give the points.
8. **Explosion migration.** [NEW]
   - Sources: CHC B17 top→bottom, C3 B3a up the rail, C3 B10 along the crown.
   - Move an emitter cursor along a line on the plate at 120–150 px/s, with `explode()` every 3–4 frames.
   - Warhive use: from the dead thruster, across the spine, to the bay.
   - ⚠ C3's version ran 12 s and was dead air. Cap it at about 2 s.
9. **Anchored fire, smoke and pops per part.** [HAVE on the Warhive]
   - Plumes at `>75 / <75 / <50 / <25 / dead`, anchored every frame.
   - Take it to every multi-mount boss through the same ladder. It is the house answer to "parts falling off" without a
     split.
10. **The burning corpse keeps fighting.** [NEW]
    - Source: AS #1.
    - The AI keeps running at about 60% speed for 3–5 s while dying, and contact still hurts.
    - Normal: harmless movement only. Hard and above: see §5 #1.
11. **Keep-moving / drifting-hull death.** [PART]
    - Sources: CHC B4, C3 B7, SR scroll-away.
    - The emitter is parented to the boss while it keeps drifting on its exit path.
    - BOF sinks at `dt*4`, which is barely visible. Give ship bosses their exit velocity instead.

### The signature flourish (one per boss, so deaths stop looking alike)
12. **Implosion → ring → column → torus.** [NEW]
    - Sources: CHC B5, B9, B24.
    - 0.5 s of contracting streaks at the core.
    - A ring of ~24 `explode()` at radius 0.5×VH that thickens into larger balls.
    - Then a vertical stack of 6–8 `explode(... 'nxp_upward')` down the core's column.
    - Then scattered small dots.
    - Each step 2–3 frames. It suits a stationary boss (Rime Wall, Sludge Emperor).
13. **Rotating pinwheel.** [NEW]
    - Source: CHC B21.
    - 2–3 arms of about 10 `explode()` each on a logarithmic spiral, white at the centre and red at the tips.
    - Rotate 30° every 0.17 s for about 2.5 s, then remove the balls from the centre outward.
    - It suits a spinning or ship boss (Storm Sovereign, Xeno Regent).
14. **Firework fountain.** [NEW]
    - Source: CHC B25.
    - From one apex, two parabolic streams of `explode()` arc to both lower corners over 1.5 s, then decay into rings.
    - It suits a boss high on the screen (Overlord).
15. **Radial shard lines / light rays.** [NEW]
    - Sources: CHC B3, B24; SR #2.
    - 12–24 thin additive lines, re-randomised each frame from the core for 0.7–3 s.
    - Draw them in world space. Bake no blur.
16. **Fireball → black smoke swap inside a double ring.** [NEW]
    - Source: SR's signature.
    - A hull-sized `explode()` for 0.3 s, replaced in place by an `nxp_smoke` / `nsd_chim_` puff that drifts with the
      scroll.
    - Plus `spawnShockRing` twice, 0.08 s apart.
    - Cheapest of all. It suits the Warhive's final blast and the ace.
17. **Black-hole implosion ring.** [NEW]
    - Sources: SR B9, B12, used for **part** deaths.
    - A dark disc with an orange rim shrinking from 1.2× to 0 over 0.3 s. It is the reverse of `spawnShockRing`.
    - Use it for Warhive thruster deaths and Sovereign helper deaths, so a part death reads differently from the boss
      death.
18. **Colour-window circle.** [NEW] [MIKE]
    - Source: C3 B6.
    - A circle grows from the core over 0.4 s. Inside it, the scene is composited with `globalCompositeOperation='color'`
      stepping red → yellow → magenta. Then the white hold. Then shrinking circles through 5–6 hues while the boss is
      removed.
    - `'color'` keeps luminosity, so it respects the swap rule. It is still a *screen* effect, so it is Mike's call.

### White, silhouette and cut
19. **White-out that keeps exploding underneath.** [HAVE]
    - `whiteBlast` 6.0–8.6 s.
    - Variant, heartbeat whites (C3 final, X3): one-frame `flashScreen` 0.9 pulses every 0.8–1.0 s through the cook-off.
      [NEW]
20. **Swap under the white.** [HAVE] The stage-1 dam.
    - Generalise it: any arena change, form change or empty-arena reveal belongs under the peak white (CHC #15, X3 4.4).
21. **Black silhouette on white, lightened away.** [NEW]
    - Sources: X3 4.1, AS #9.
    - At peak white, draw the plate as `xartPalette(plate, 'black')`. Then step it through grey to white over 1 s.
    - This is *not* an alpha fade. The steps are lighter palettes.
    - The AS variant keeps one feature in true colour: the core dots, or the Nightwing's engine glow.
22. **Cooling dome.** [NEW]
    - Source: AS standard kill.
    - After the white, draw a flat ellipse at the boss's centre and scale it from 0.3× to 2.5× the screen width over
      80 frames.
    - Step its colour white → yellow → orange → red → gone every 12 frames, with a 50% checkerboard after step one.
23. **Chunked silhouette.** [NEW] [MIKE]
    - Source: X3 Kaiser.
    - The black silhouette is sliced into 4–6 rectangles along the plate's natural parts, each nudged outward 1–2 px per
      frame, only inside the white.
    - It is a death visual, not a split, but it *looks* like pieces coming apart. Ask Mike first.
24. **Fall-away crash.** [PART] The Warhive already sinks with chain explosions.
    - Source: SR B14.
    - Rotate the whole plate 15–20°, slide it about 400 px off a lower corner while scaling it to 0.85 over 2 s, with pops
      along the path.
    - It reads as crashed, not exploded.

### Aftermath and transition
25. **Explosions outlive the body.** [NEW]
    - Sources: X3, CHC.
    - Keep the emitter running at the last position for 1 s after the plate is gone.
26. **Hard removal plus 2–3 s of silence.** [NEW]
    - Source: C3 #8.
    - Delete the boss and every hazard it owns in one frame, then hold an empty, quiet field.
27. **Delayed secondary death / aftershock / late puff.** [NEW]
    - Sources: AS B12, CHC B15/B26/B28.
    - About 1.2 s after calm, the *arena* dies: diagonal bands of `explode()` roll across the field under the debrief.
    - A variant is one late small puff a beat after everything calms. It suits Stage 2 (S2-10 "residual explosions") and
      Stage 7.
28. **Smouldering loop under dialogue.** [NEW]
    - Source: CHC B2.
    - A 4–6-ball loop at the wreck for as long as the post-fight comm window is open.
29. **Pilot ejection / pilot reveal.** [NEW] [MIKE]
    - Sources: CHC B5/B24, X3 Goliath → Vile.
    - A small pilot sprite tumbles out in an arc during the grey return from white.
30. **Fake death with a one-frame tell.** [NEW] [MIKE]
    - Sources: C3 B10, X3 idea 5.7.
    1. A dead-colour swap and the room explosion.
    2. 3–4 s of empty field.
    3. A one-frame eye or engine blink.
    4. The palette snaps back and the next form arrives.
31. **Scroll continues; the tally counts while flying.** [PART]
    - Sources: FS, C3 gates, SR "the scroll never stops".
    - BOF resumes the scroll after the boss dies and has the flyover. The FS touch is a bonus tally counting *during* the
      scroll cooldown, before the debrief. BOF's arcade kill floaters could carry it.
32. **Break-out cut.** [NEW]
    - Source: C3 20:03.
    - At the peak, a hard cut from a dark arena to open sky with no fade. It suits the end of Stage 8 → Stage 9.

### Entrances (for the same "set-piece" standard)
33. **Fly up from below and overtake.** [HAVE] Overlord (S1-09). Also [NEW] as an option for the Warhive (SR B3/B14).
34. **HP-gauge fill ritual before the boss can act.** [HAVE] Overlord (S1-10), from X3 4.9.
35. **Materialise in light columns / lights-out / scenery breaks.** [NEW]
    - Sources: C3 B9, X3 4.7, C3 B1/B5.
    - Candidates: the Xeno Regent (light columns) and the Sludge Emperor (lights-out).
36. **Transformation behind white, with arena mutation first.** [NEW]
    - Sources: CHC B26, AS B9 two curtains, X3 4.4.
    - Change the floor or background, then hold white for about 2 s, then fade in with the new form already in place.
      Candidate: Vile Existence's four forms.

---

## 5. HARDER / OUTSIDE THE BOX — the best 20

The theme across all of these: no-hit players find a **parking spot** and a **safe victory lap**. Take both away,
fairly. Everything below still uses the shared warning and commit-then-execute. Nothing here is proposed for Normal
without Mike's say-so.

| # | idea | source | best fit in BOF |
|---|---|---|---|
| 1 | **A dangerous corpse.** The last 1–2 s of the cook-off throws real, warned shrapnel toward the player. Only a roll or somersault clears it. | CHC §5, AS "delay the death", GA #10 | every boss on Hard+; Nightwing Ace first |
| 2 | **Anti-parking.** Track the player's dwell per lane. After about 4 s in one band, the next attack is spent on it, with the FOV cone growing brighter as the tell. | C3 §5 | Rime Wall, Sludge Emperor, Furnace Tyrant |
| 3 | **No free victory lap.** Scripted missiles already in flight survive the bullet clear. | SR B13/B23 | Warhive (escorts' missiles), Stage 8 |
| 4 | **Parts change what the other parts do.** Killing one Warhive thruster makes the carrier yaw toward the dead side, skewing its gun lanes. The surviving cannon inherits the dead one's pattern. | SR §5.3, GA §C.9 | Warhive Hard |
| 5 | **Optional risky window.** The weak point is exposed only while it charges, so dealing damage means sitting in the lane about to fire. | GA §C.8, SR §5.4 | Warhive bay; S3-12 giant beam |
| 6 | **The breathing corridor.** Twin beams swing between a V and parallel on a 3–4 s cycle. On the hardest setting the corridor also drifts. | GA L18 | Warhive Hard cannons; S3-12 |
| 7 | **Beam plus orb crossfire.** One cannon holds a one-third beam while the other lobs slow orbs into the safe two-thirds. | GA §C.2 | Warhive Hard |
| 8 | **A tether fence.** Two detached drones linked by a sweeping lightning fence with one gap. The gap is where the orbs are not. | GA L31 | Storm Sovereign helpers (Furious) |
| 9 | **The ace dodges your column.** It sidesteps the player's column within 0.4 s of fire. | SR §5.15 | Nightwing — [HAVE] roll-on-incoming |
| 10 | **Mirror the last 3 s.** The ace replays the player's own recent path one lane over. Cap it at one move in three. | AS §5, X3 §5.3 | Nightwing Ace |
| 11 | **Absorb-and-return.** A short deflector shimmer stores hits and returns them as a spread along each incoming line. It punishes holding fire. | X3 Doppler | Nightwing (Furious), or a Stage 7/8 form |
| 12 | **The counter-dash clash.** If both jets charge within one window, they spark off each other with a 0.3 s freeze. | X3 §5.4 | Nightwing Hard (spectacle) |
| 13 | **Shrink the tell as HP drops.** The tell shortens 0.5 → 0.25 s (never below 0.25). One decoy arrow that never fires, on Furious/Insanity only. | AS §5, SR §5.6, GA §C.7 | Rime Wall — [HAVE] S3-13 Simon-Says feints |
| 14 | **Arena squeeze.** A dash leaves a fire trail for 2–3 s, or a spike or wall line descends as a soft timer. | X3 §5.9, C3 B3b | Frost Cruiser Furious, Furnace Tyrant |
| 15 | **Debris as projectiles.** Anything broken keeps its momentum as a hazard, with anchored fire trailing. | SR §5.9, CHC B6 | Stage-2 vents — [HAVE] fire debris; Warhive wreck |
| 16 | **Escorts that outlive the boss and go berserk.** Faster, aimed, red palette. | SR B27 | Warhive → only if the ace fight wants it [MIKE] |
| 17 | **Timer pressure.** Kill the carrier slowly and it launches a second full wave. A fleeing boss heals slightly while off-screen. | SR §5.14, AS §5 | Warhive "away" phase |
| 18 | **A shootable core during the transition.** Hit the escaping core during the interlude to shorten the next form. Miss, and the next form gets a shield. | AS B20–23 | Vile Existence form changes |
| 19 | **Relocate, don't chase.** The boss swaps to the opposite side through a visible ghost or scanline shear. One time in three it reappears on the *same* side. | AS B18 | Tempest Leviathan duo, Nightwing |
| 20 | **Fake death on the highest difficulty only.** Run §4 #21 up to the silhouette, then the boss punches out of the white, damaged and on fire. | C3 B10, X3 §5.7 | final boss or Nightwing [MIKE] |

---

## 6. TRANSLATION TO BOF — prioritised proposals

**Cost key:**

| cost | meaning |
|---|---|
| **S** | under a day, code only |
| **M** | 1–3 days, or needs one generated asset |
| **L** | a week, or several assets |

"Risk" names the specific trap from `CLAUDE.md` that applies.

### 6a. Warhive Carrier + Nightwing Ace — tuning passes, not rewrites

| pri | what | why (reference) | cost | risk |
|---|---|---|---|---|
| **1** | **Measure the dead air.** Play the fight and log (a) seconds between visible changes, (b) the length of the `away` phase, (c) time-to-kill each escort wave, on Normal and Hard. Target: something new at least every 20 s. | SR §2.1, AS §2.11; SR B6/B15 as the bad example | S | None. It is a measurement. `away`'s 45 s safety is the number most likely to be too long. |
| **2** | **Escort shield family.** The crimson rings dominate the frame with 6–8 escorts (`03_escorts.png`). Try `hex` or `ion`, which is one word on `ELITEX.hivewing`. | GA §3 colour discipline; readability first | S | Mike's call. The doc already flags it. |
| **3** | **A distinct part death for each thruster.** A black-hole implosion ring (§4 #17), then the existing six-blast and wreck plate. Add a smoke puff every 0.3 s from the wreck socket via `nsd_chim_`. | SR B4/B14 "dead parts stay and puff" | S | Keep it anchored to the hub **every frame** (the hub moves with the carrier). |
| **4** | **Heat pulse on the last live thruster below 25%.** `xartPalette` red on the *whole* carrier plate at 4 Hz. It tells the player the carrier fight is nearly over. | SR 4:29 | S | Cache the palette key. Never tint per frame through a flood (the E→B font lesson). |
| **5** | **The fall, with a signature.** At 3.6 s, add the SR fireball → black-smoke swap and a double `spawnShockRing` behind the carcass, plus a 15° tilt-and-slide on the sinking plate (§4 #16, #24). | SR B14 18:15, SR 4:35 | S–M | Tilt is a whole-plate transform, not a split. Check the drop cells still anchor. |
| **6** | **Nightwing RECOVER windows.** After a charge dash, 0.6 s of overshoot and a slow bank back. After a somersault, a 0.4 s stall at the top. Right now "smart reactive" can read as always-dodging. | X3 §2.5 "the punish window is physics" | S | Must not collide with its roll i-frames. Record what the ace is doing per frame in the probe. |
| **7** | **Ace kill freeze plus a 1-bit silhouette.** A 0.3 s `_killStop` on the last hit. At peak white, draw the ace `xartPalette('black')` with only its engine glow in colour, then the existing crash. | X3 4.1, AS §5 closing | S–M | ⚠ `whiteBlast` does not decay by itself. `_killStop` must not use `timeScale`. |
| **8** | **Hard: anti-parking for the cannon beam.** Never fire the one-third beam into the same third twice running. Add a sparse slow-pellet field in the safe two-thirds while it burns. | GA §B.4, L18 | S | The beam already uses the shared cone. Keep the lane choice committed at the warning. |
| **9** | **Hard: breathing twin beams** as a new cannon pattern after the single beam. 6–9 s sweep, narrowest corridor about 20% of the width. | GA L18 | M | A new pattern needs its own probe with the busted-arm discipline. |
| **10** | **Optional: an overtake entrance** — the carrier flies up from below, crosses the screen, then backs down from the top. | SR B14 17:36 | M | Mike's spec says the carrier "comes down on screen". This replaces that. [MIKE] |

**Not recommended for the Warhive:** escorts that outlive the carrier. The spec has the carrier waiting for the escorts,
not the reverse. Do not add a Warhive HP bar either: the no-bar carrier is Mike's spec.

### 6b. Open work-order boss items

**S2-10 · Stage-2 finale** (pending Mike's identity call; do not generate head art before it).
The brief: accelerating screaming head frames, shrieks and shake; two fire-ring X cycles; a final white flash; the boss
gone; residual explosions. The recipe is fully in the kit:
1. The head strobes crimson/pink (§4 #6) on an accelerating frame cadence, with a shriek cue per cycle, and `shake`
   ramping 6 → 18.
2. The two fire-ring X cycles are two crossed pairs of flat `_smokeRings`. The Hammer death already crosses them at
   0 / π/2 / ±π/4. Add a fire-flavour `spawnShockRing` on each.
3. A single white (`whiteBlast` set and cleared by hand). The head is removed under it (§4 #20).
4. Residual explosions for 2–3 s on the empty arena (§4 #25, #27).

- Refs: AS standard kill; C3 hard removal plus silence; CHC aftershock.
- Cost: M once the identity exists.
- Risk: the Furnace head is the named split exception, so its death must not invent new detached pieces.

**S2-11 · Scroll after defeat, and the pilot line.** The FS model: the level keeps scrolling while a tally cools down.
C3's gates: no fade. Pair it with §4 #28, a smouldering loop at the wreck under the comm window.
- Cost: S–M.
- Risk: the 0814d dam lesson. A post-death scroll must bring whatever changed *into* frame. Measure it on screen.

**S3-10 · Hard stage-3 boss: dash, circular return, persistent hull shadow.**
- Refs: X3 commit-then-execute; Byte's wall stun as the punish window; SR "ramming pass with a shadow tell"; CHC B5 pod
  dive.
- The shadow is the hull silhouette flooded black (the Razorback precedent: never a translucent rectangle). It leads the
  dash down the committed lane during the yellow/red warning, which makes it the telegraph as well as the persistent
  shadow.
- The return is a cubic arc (the Olive Warden precedent), collision-safe.
- Cost: M plus a SpriteCook charge-FX asset.
- Risk: ENG-02 compliance. The lane must be locked from yellow.

**S3-12 · Furious stage-3: black/blue plate, all the Hard patterns, and a giant beam.**
- The palette is `xartPalette` black/blue. The Frost Cruiser Hard variant is the worked example.
- The giant beam is GA L35 exactly:
  - A core ramp red → orange → yellow → white over 0.9 s, shown in the shared cone.
  - The width is a third of the screen, shown as **two edge lines**, not a centre line (GA §B.4).
  - The angle locks at release. It burns 1.5–1.8 s with a 0.2 s taper.
  - It never takes the same third twice running.
  - Optional lingering scorch line for 1–2 s (GA §C.4).
- Cost: M. It depends on S2-09's Furnace beam art.
- Risk: a smoothed cone at length (0912x). The beam glow must be baked, not blurred per frame.

**ENG-02 · Shared warnings, remaining families.** Proposal:
- Build a one-page audit table: every `eShoot` / `_shipShot` site per boss, and whether a warning precedes it. This is the
  SR "one grammar across all fights" standard.
- Then map the three reference grammars onto the one BOF warning:

| reference tell | BOF form |
|---|---|
| thin guide line | the FOV cone in green, then yellow |
| top-edge triangle for a falling column | the alert sign pinned at the top of the lane |
| concentric rings on a core | the cone at radial scale |

- Decoy tells stay Furious/Insanity only [MIKE].
- Cost: M (audit S, fixes per family).
- Risk: the shared cone draws smoothed and is sized to the beam, not to `sceneDrawZone`'s mapping (0912x).

**SPACE-06 · Stage-5 balance (Chrome Hammer Archmage).**
- Log per phase: time-to-kill, longest gap with no new idea, and deaths per attack. Target a fight of 55–90 s, with
  something new every 15–20 s (AS §2.11).
- The warned leap, boomerang and spiked ball are all shipped. The likely tuning is dead air around the core-orbit
  recovery (0916) and the mega-wave.
- Cost: S to measure, M to tune.
- Risk: this is a natural-play review *with Mike*, per the work order. Do not tune blind.

**ACH-14 · Boss Rush and Time Attack.** Alien Soldier *is* the template:
- A warning card, then the fight within about 2 s.
- A per-fight timer that freezes on zero HP. The time left becomes the bonus.
- The next title card with no fade.
- Save long cinematics for landmark bosses.

BOF already has what this needs:
- The ACH-09 boss timer (upper right, excludes the entry, freezes on defeat).
- The debug fight list (`debugFightList`, 17 fights, runs the *real* stage path).
- The locked mode cards (ACH-12/13).

Proposal:
- **Boss Rush** runs the nine main bosses in stage order through the debug-jump path with warnings kept. Entrances play in
  full the first time and at 2× afterwards [MIKE]. HP carries between fights, with a Life Up between fights [MIKE].
- **Time Attack** scores the ACH-09 time per boss against a stored best.

- Cost: L (mode plumbing, results screen, save).
- Risk: 0916 records a whole class of front-end breaks. Drive it with real key taps in Chromium, watching `pageerror` and a
  frame counter.

### 6c. Shared "boss death kit" — one upgrade for every boss

**What.** A table-driven death timeline. `BOSS_DEATH[kind] = {stop, pops, flourish, white, after, exit}` feeds one
`bossDeathKitTick(b, T)`, called from the existing dead branch **before** the stock cook-off. Every field is optional,
and a missing row means today's 9.4 s death exactly.

| field | options | catalogue refs |
|---|---|---|
| `stop` | kill-freeze seconds (0.25 default, up to 0.8 for stage finals) | #1 |
| `pops` | chain-pop through the plate's mounts, count and interval | #7 |
| `pulse` | heat-pulse / dying-strobe keys and rates | #5, #6 |
| `flourish` | one of: `ringColumnTorus`, `pinwheel`, `fountain`, `rays`, `smokeSwap`, `migration(path)` | #8, #12–16 |
| `white` | `stock` / `heartbeat` / `silhouette(keepColour)` / `dome` | #19, #21, #22 |
| `after` | `outlive(1s)`, `silence(2s)`, `aftershock`, `smoulder` | #25–28 |
| `exit` | `sink`, `drift`, `fallAway`, `scroll` | #11, #24, #31 |

**Suggested signatures** (so no two deaths look alike, which is the lesson from CHC's best fights):

| boss | signature |
|---|---|
| Overlord | `fountain`, `fallAway` |
| Furnace Tyrant | S2-10 recipe, `aftershock` |
| Rime Wall | `ringColumnTorus` in blue, `silhouette` |
| Storm Sovereign | `pinwheel`, `heartbeat` |
| Xeno Regent / Archmage | `rays`, `dome` |
| Warhive | `migration(thruster → spine → bay)`, `smokeSwap`, `fallAway` |
| Nightwing | spin-out (have), `silhouette(engine)` |
| Sludge Emperor / Warden | `smoulder`, `aftershock` |
| Vile Existence | `heartbeat` white, `silhouette`, then the break-out cut (#32) into Stage 9 |

- **Why.** Every source game gives its landmark bosses a signature death. BOF gives all of them the same well-built 9.4 s
  (CHC §2.10–12; AS reserves spectacle for three landmark fights).
- **Cost.** M for the kit and three flourishes, then S per boss row.
- **Risks.**
  1. `bossDie` has several rig-specific exits: the Warden, stage-4 `_cinDeath`, the Hammer, the Warhive. The kit must run
     only where the stock branch runs, or be called explicitly by those rigs.
  2. `whiteBlast` never self-decays.
  3. The screen-space parts go through `worldXformEscape`.
  4. Keep the `explode()` count within the existing cadence, and bake every glow (0916ab).
  5. Prove each death with a probe that records the blit **keys** and a proof strip, not state (rules 1–2).

---

## 7. Questions for Mike

1. **Dangerous deaths.** Should a boss's last seconds be able to kill a player who stops dodging (warned shrapnel,
   surviving missiles)? If yes, from which difficulty up — Hard, or Furious only?
2. **No boss splits during the death.** Does the rule also cover the *death animation*? Chunked silhouettes (X3), limbs
   flying off as burning debris (CHC), a pilot ejecting. Which, if any, are allowed?
3. **Signature deaths.** Do you want one house death for every boss, or a signature per boss as proposed in §6c? If a
   signature, do you agree with the pairings?
4. **Screen effects.** Full-screen negative frames, colour-window circles and heartbeat white strobes are all screen-level
   effects, and strobing raises a photosensitivity concern. Allowed, and on which bosses?
5. **Kill freeze.** How long a stop on the killing blow — 0.25 s, or longer for stage finals?
6. **Fake death / resurrection.** Should any boss lie about dying? Which one — the final boss, or the Nightwing on the
   highest difficulty?
7. **The Nightwing's story.** Should the ace appear earlier and *retreat* (X3's retreat ending) so Stage 6 is a rematch?
   Should it eject a pilot when it dies?
8. **Warhive tuning.**
   - Is 45 s a reasonable `away` limit, or should the carrier come back sooner to press the player?
   - Should losing a thruster tilt the carrier?
   - Which escort shield family: crimson, hex, ion or none?
   - Do you want the SR-style overtake entrance?
9. **Decoy telegraphs.** Is a tell that lies acceptable anywhere, given the green/yellow/red rule? If so, Furious and
   Insanity only?
10. **Anti-parking.** Should bosses deliberately aim at a lane the player has camped in?
11. **Boss Rush.**
    - Nine main bosses only, or minibosses too?
    - Does HP carry between fights, with a heal between them?
    - Should entrances shorten after first viewing?
12. **Stage 2.** The S2-10 finale still needs your boss-identity call before any head art is generated.
