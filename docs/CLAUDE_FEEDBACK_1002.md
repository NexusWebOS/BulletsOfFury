# October 2: Stage 5 hammer, Stage 6 flights, the Harrier's squadron, the team scene, turbulence

Mike's notes, in order. Every runtime change is in one layer, `assets/feedback_1002.js`. It loads after `feedback_1001b.js` and before the widescreen HUD. The only edit to `assets/game.js` is the one-line Chromium-pose flash. Each section below names what was measured in real Chromium before the change.

All of it was checked against the latest GitHub first (Mike: *"download from the latest github first"*). `origin/claude/epic-clarke-rtfnuk` and `origin/main` had nothing newer than `d19c9666`.

## A. Stage 5: the Chrome Hammer Archmage

> "volley missiles are still striking his hammer, which is disrupting the sequence of his recharge/recover ability. He is also not flashing white when taking damage until the very end ... He should never be able to be killed before doing the circular spin rage form recovery effect."

### Volley missiles never touch the hammer

**What was wrong.** The passive Stage 5 volley rack locked the hammer as a retina piece: `spaceVolleyLocks` and `spaceAcquire` read `spaceTargets`, which lists it. And every missile kind broke the heal, the passive volley included.

**Now.**
- The volley never selects the hammer piece.
- A volley round flies *through* the hammer.
- A stray hit on the hammer counts as a body hit.
- A deliberate manual missile into the raised hammer still breaks the heal, as designed.

### Every absorbed hit flashes

**What was wrong.** `hitBoss` runs `hammerBossDamage` and returns on 0 *before* `markHit`. So nothing flashed for:
- the whole armoured opening;
- rounds into the hammer;
- rounds into the recovery core.

The Chromium pose also re-blitted its own plain plate as the "flash".

**Now.**
- Any hit that changes something flashes: armour, hammer, chaingun, core, the twirl or whirl counters, or the boss's state.
- The pose draws a real white silhouette (`xartTint`).

### He cannot die before the spin recovery

His HP has a floor (8% of max) until two things have happened:
1. The hammer-raised recovery has started (`restorationSeen`).
2. Where the 15% `fr_twirl` is live (Furious), it has actually played: its slam landed, or the pilot broke it into the red rage.

A stale charging heal used to swap the twirl for a stun on its first frame. The twirl now starts clean, and any other early exit re-arms the checkpoint.

**Probe:** `probe_hammer_1002.py`.

| Run | Flash | Volley | Death |
|---|---|---|---|
| Normal | 132/132 hits flash | 8 launches, 0 hammer locks, heal intact | after the recovery |
| Hard | 133/133 | OK | after the recovery |
| Furious | 132/132 | not run (`--novolley`) | the twirl played and broke into rage, then death |
| Busted arm (`--old`) | 0/132 | broke the heal | died in `fr_stun` before any recovery |

## B. Stage 5: the hammer's arrival, in play

> "generate a proper avatar box of our hammer boss, do not pause the game, just darken the arena ... '...Who are you?' '.........' Decker or Cole will be the main point of contact from HQ ..."

**Art.** All boxes are SpriteCook edits, in `assets/game/dispatch_1002/`.

| File | How it was made |
|---|---|
| `hammer_avatar.png` | Built from a composite of the authored Cronos bust in a recoloured comm frame. The composite is kept as `_BUILD_SOURCE/hammer_avatar_comp_1002.png`. |
| `dispatch_cole.png` | Edit of his own comm box: headset, boom mic, command centre behind. Regenerated once, because the first take added glasses he doesn't wear. |
| `dispatch_decker.png`, `dispatch_axel.png`, `dispatch_lizzie.png`, `dispatch_falva.png` | Same edit of each pilot's own comm box. |

**The beat.** The 0930 Cronos scene was a *live* director scene, which replaces `updatePlay` and so freezes the world. It is retired, and the arrival is now a beat inside ordinary play:
- The scroll, effects and music keep running.
- The hammer finishes unfolding, then holds the last unfold frame (1.95 s), untargetable.
- Every seat is stunned through the one existing control gate, with the shared stun sparks orbiting the ship.
- `drawBG` gets a dark wash.
- The fight clock does not count the conversation.

Lines:
1. Pilot: "...Who are you?"
2. Boss: "........."
3. HQ: "That signature is not in any Federation file."
4. Pilot: "It's just staring at me."
5. Boss: "........." in arcade. In the campaign, the condensed Cronos reveal instead.
6. HQ: "Its core is spiking! ... NOW!"

FIRE advances a line; lines also advance on their own.

**Dispatcher rule**, as Mike gave it:

| Who is flying | Dispatcher |
|---|---|
| Cole | Decker |
| Decker | Cole |
| Anyone else | Cole or Decker, at random |
| Cole and Decker (co-op) | Axel |
| A woman leading, with both Cole and Decker flying | The other woman (Lizzie ↔ Falva) |

A pilot who is in the air is never the dispatcher. The last row cannot trigger in two-seat co-op as it stands, because if both Cole and Decker are flying, neither seat is a woman. It is implemented for when that changes.

**Probe:** `probe_hammer_intro_1002.py` passes for:
- Cole → Decker;
- Decker → Cole;
- Lizzie (arcade) → random Cole/Decker;
- Falva (arcade) → random Cole/Decker;
- co-op Cole + Decker → Axel.

Across those runs:
- the 0930 pausing scene is never seen;
- `stateT` and the space scroll advance;
- a held real LEFT key does not move the ship;
- the hammer stays `_noHit` and in `unfold`, then becomes hittable;
- the avatar and dispatcher boxes are blitted, identified by key;
- the arena's median luminance drops by roughly 40%;
- zero errors.

The busted arm fails: the pausing scene runs.

## C. Stage 6: the stealth flights replace the bombers

> "Use the stealth fighter jets that are blue, palette swap them to red, and another new enemy to green. The red ones shoot regular missiles that lock retinas on us, the green ones drop the atom bombs ... make an orange one with machine gun turrets ... generate this one entirely with spritecook ... arrows letting us know its coming left, its coming right, its coming down etc with our asterisk and warning box system."

**Art.** `assets/game/stealth_1002/{red,green,orange}.png`, built by `_BUILD_SOURCE/stealth_jets_1002.py`. Each sheet is four 128px cells: east, west, south, north.
- **Red and green** rotate the hue of the blue paint only, about 3,600 px per sheet. Metal, outlines and orange accents are untouched.
- **Orange** is a SpriteCook edit of the blue jet, with wing gatlings and a chin gun.
- The sheets are baked offline. The 1001 runtime swap read pixels, which a `file://` page refuses.

**What was replaced.**
- Every `s6bomber` the stage spawns: the plan's lateral runs and both reinforcement directors.
- The seven cardinal `s6StrikeSpawn` passes.

**The warning.** Each flight is warned first:
- a warning box over the lane it will fly;
- the impact-imminent asterisk at its entry edge;
- three escape-arrow plates pointing the way it travels.

All three step green → yellow → red with the shared warning beeps. Only then does the jet enter.

**Roles.**

| Colour | Attack |
|---|---|
| Red | One retina lock, two regular missiles bound to it. |
| Green | Lizzie's atom bomb onto a committed reticle. |
| Orange | Aimed three-gun bursts. |

The opening assault squadron keeps its own gates, but now wears the role colour:
- bomb carriers are green;
- a Furious machine-gun gate is orange;
- an unarmed gate keeps the authored blue.

**Probe:** `probe_stealth_1002.py` passes on Normal and Furious. It covers six role/direction cases, an `s6bomber` replacement and a strike replacement. In every case:
- the warning runs about 92 frames with no jet on the field;
- the arrow and asterisk are drawn;
- the jet is drawn from its role sheet;
- red opens a lock with 2 missiles;
- green drops a bomb;
- orange fires.

Orange's round count varies because the shared `ai27` fair-fire rule holds shots that would be point-blank. That rule is intended.

## D. Stage 6: the Harrier's launched jets fight as a squadron

> "those jets that come out of the harrier to attack us, needs to be more advanced AI and proper attacks."

These are the Warhive's hivewing escorts. On top of `hivewingTick`:

- **Lead aim** on bursts and dives.
- **A warned dive.**
  - The shared lane warning runs along the committed vector: 0.78 / 0.66 / 0.56 s by difficulty, where the old tell was a 0.4 s nose flash.
  - The vector locks at 60% of the tell, so a late break still dodges.
- **A squadron brain** rotating three plays:
  - **Pincer**: two jets break to opposite edges, warn their crossing lanes, then fire converging 6-round streams.
  - **Missile**: one escort opens a retina lock.
  - **Bracket**: the free jets re-slot either side of the pilot's column.
- **Lane discipline**: a jet that has sat in the pilot's fire lane for 0.35 s rolls out of it.

**Probe:** `probe_hivewing_1002.py` passes on Normal and Furious:
- 9 dives, each with a 0.77 s warned tell, each running on its committed vector;
- two two-sided pincers that fired their streams;
- an escort lock with 2 missiles;
- bursts leading the weaving pilot.

The busted arm fails on the tell, the vector, the pincer and the lock.

## E. Stage 6: "who stayed behind at base?!" and Secret Weapon Callisto

**Where it plays.** After the fighters and the Harrier pass over (the "Harrier breaking left" beat and Voss's taunt), and before the split-the-wing choice. The base flow is held at the end of that beat and released into the choice unchanged.

**The argument.**
1. Cole: "Who stayed behind at base to defend it?!"
2. Silence, then "Not me", "Uhhh....", "Well...", "We were attacked, and we saw everyone was getting attacked, and-"
3. Cole loses it in three generated shouting frames: snarl, yell, scream (`cole_rage_0..2`, SpriteCook edits of his anger box).
4. Heads down: "Sorry, boss..."
5. Cole calms down and lays out the split.

**Playing Cole only.**
1. "SECRET WEAPON CALLISTO / WEAPON STATUS = ACTIVATED" types letter by letter in the powerup banner face. ACTIVATED is green and flashes on five beeps.
2. Cole explains the field tests.
3. He demonstrates on his own ship:
   - the fusion cannon charges and releases;
   - his level-7 lasers fire a long burst. These are the black four-wide rows plus the homing trident arch, i.e. `coleTier` 7.
4. The team reacts in shock.
5. The choice opens.

Two details of the demo:
- A random Stage 6 Sonic Boom grant claims his trigger, so the demo suspends it for each scripted shot only.
- The pilot's own weapon is restored afterwards.

The scene runs in play: controls are held, enemy rounds are cleared and nothing can hit the ship. Speakers come from the nine pilots in the air.

**Probe:** `probe_teamscene_1002.py` passes for Cole and for Lizzie:
- the choice waits for the scene;
- `stateT` advances;
- the ship can't move and takes 0 hits;
- the rage frames animate;
- for Cole: both banner lines are drawn, ACTIVATED is tinted `#39ff5a`, 5 beeps, the fusion cannon releases, 184 laser rounds, and the weapon is restored;
- for Lizzie: no Callisto.

## F. Stage 6: turbulence

> "we also need turbulence noises generated for the harrier and them going over us and stuff."

Two cues, generated with ElevenLabs text-to-sound v2. The sources are kept in `_BUILD_SOURCE/sfx_src_1002/` and mastered by `_BUILD_SOURCE/turbulence_1002.py`.

| Cue | Use | Mastering |
|---|---|---|
| `turbulence_carrier_1002.mp3` | Seamless loop under the carrier turbine. It rides the turbine's own `loopOn`/`loopOff` calls, so it plays during the opening flyover and the "Harrier breaking left" beat. | Matched to the turbine, mean −18.8 dB. |
| `jetwash_1002.mp3` | One-shot, once per jet, the first time any Stage 6 jet streaks past within reach. Comes with a small shake. | Matched to `jetDash`, mean −18.3 dB. |

This layer loads after the audio pools are built, so it registers its own lazy pools and TAME rows.

**Probe:** `probe_turbulence_1002.py` passes:
- both pools and TAME rows exist;
- the files serve with HTTP 200/206;
- the loop is on with the turbine for 40/40 flyover samples, and its element advances 0→1.06 s;
- one stealth pass plays exactly one jet wash, and that voice plays;
- zero errors.

## Verification

- `node --check` passes on every touched script.
- Suite section `test_feedback_1002.cjs`: 45 assertions.
- **Full suite: 6,276 ok, banner reached, 0 errors, exit 0.**
- The probes above all pass in real Chromium.

Credits spent: SpriteCook 309 → 153; ElevenLabs about 67.

## G. The fusion beam is a solid plasma column, and every icon keeps one size (follow-up)

> "the fusion cannon beams. they should not be spikey lasers ... solid pink beams like falva's laser beams, but more 'Fusion' energy like while still pinkishpurple. also, their weapon pick up icons are very small in game ... we should be keeping a unified system of h/w for each icon as an engine rule."

### The beam

Both fusion weapons drew a branching lightning lance:
- the space-slot Fusion used `fusion_0930/beam.png`;
- Cole's level-8 fusion cannon used the green enemy laser, hue-rotated through a CSS filter.

Both now draw `assets/game/fusion_1002/beam.png`:
- **Source.** A SpriteCook edit of Falva's own solid laser plate (`fllaser_0`): a pink-violet sheath, a white-hot core and a contained double helix. It is kept as `_BUILD_SOURCE/fusion_beam_spritecook_1002.png`.
- **Animation.** Built by `_BUILD_SOURCE/fusion_beam_1002.py`. One measured helix period (57 px) is tiled down the interior and offset by an eighth per frame. The helix flows up the beam while the silhouette, caps and alpha never change. A first cut that rolled the interior left a hard seam on half the frames; tiling removed it.
- **Gameplay unchanged.** Damage, speed, hit width and charge scaling stay as they were.

### Icons: the engine rule

Measured in Chromium through `iconBlit` itself (`_BUILD_SOURCE/icon_ink_1002.py`), each art family carries its own transparent margin inside its cell. At a 100 px request:

| Icons | Ink drawn |
|---|---|
| Space Fusion badges | 65–77 px, different per tier |
| Thermoshock | 72 px |
| Volley badges | 100 px |

In the pre-change build, 100 of 256 icon draws missed their requested height, and icons reported different widths to their callers.

**The rule.** Every icon with a measured ink box is drawn so its ink fills one unified box:
- the ink height equals the requested height;
- the ink is never wider than 0.93 × the height (the badge family's own 104:112);
- the ink is centred in that box;
- every icon reports the same box width.

**How it works.**
- The ink table is measured once from the raw draw. The script always calls the unwrapped `iconBlit`, so re-running it cannot measure the rule itself.
- It ships as `assets/icon_ink_1002.js`, because a `file://` page cannot fetch JSON.
- An icon with no entry draws exactly as before. When a new icon family is added, re-run `python3 _BUILD_SOURCE/icon_ink_1002.py --write`.

**Probe:** `probe_fusion_icons_1002.py`:
- all 128 measured icons fill the box at 40 and 64 px, with one box width per height;
- the Fusion badges now ink at 63–64 of 64 (they were 42–49);
- the space Fusion round and Cole's cannon both draw `fb2_fusion_beam`;
- the busted arm fails on every point.
