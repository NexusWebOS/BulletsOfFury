# September 22 repair pass

Latest request takes precedence over the historical checklist. Existing uncommitted work was preserved; nothing was committed or pushed.

Tally for this repair pass: **15 implemented groups; 5 open groups.** These are grouped work items, not a percentage of the entire game backlog.

## Implemented

- [x] Stage 5 uses Chromium Hammer on every difficulty, including Hard/Furious. Debug fight selection names the same encounter.
- [x] Stage 4 escorts participate explicitly in projectile collision outside the main hull. Orbs now hit minibosses and their escorts; the orb loop previously skipped minibosses entirely.
- [x] Stage 9 return restores Stage 5's miniboss completion/trigger flags, wave index, clocks and map scroll. Both return paths consume the same snapshot.
- [x] Stage 6 opening: faint cloaked escorts, spaced typewriter dialogue, reveal, seven lock pulses, two interceptable missiles, side departures, countdown, then the massive north-facing carrier and moving silhouette shadow. Stage waves and bonus crates wait until the sequence finishes. Failing the interception costs one life before the countdown resumes.
- [x] Dialogue is bottom-centered and drawn after the equipment overlay.
- [x] Generated lock-alert metal frame with half-opacity glass; native aspect ratio preserved. Gray idle lock/red flashing active alert. SpriteCook asset/model recorded beside the PNG.
- [x] Ice Breath and Thermoshock are Freezer-only. Other pilots cannot select them; legacy equipped forms are guarded.
- [x] Loadout selection keeps weapon bays fixed. Down selects forms, left/right selects a type within that weapon. Selecting a catalog item targets its existing bay.
- [x] Post-Stage-4 and post-Stage-9 Forge/loadout screens are skipped. The post-Stage-5 Forge restores ground weapons before editing them; space weapons do not appear in these screens.
- [x] Static pickup faces rotate rather than using false back-face reels. Score bullets and bombs use their existing standalone source art at smaller sizes.
- [x] Widescreen leaderboard/sidebar text uses the actual dialogue bitmap glyphs.
- [x] Controller disconnect clears stale held-button states, including a missing second controller.
- [x] Stage 3 Hard/Furious attack recovery is shorter; Frost Cruiser missiles are faster. Warning durations are retained.
- [x] Boss Mode Save enables persisted overrides; storage failures are reported. Scripted encounters explicitly say when changes are design notes only. Their saved notes are restored on reopening. Added a START HERE guide without covering scene controls.
- [x] Debug fight picker has a difficulty selector and uses the generated frame/dialogue heading. Bullets of Debug APPLY commits focused live controls and explains that lab changes are temporary.

## Verification and limits

- `node --check assets/game.js`, Boss Mode and Bullets of Debug scripts pass.
- Full `node _BUILD_SOURCE/test_fl.js` reaches its final summary and exits **1: 76 failures**. Failing assertion names exactly match `_shots/stage6_cinematic_final_test_fl.log`; no new failures. Updated the obsolete test that expected every pilot to equip Freezer's forms.
- `_shots/verify_0922.py`: passed; no page/console errors. Captured every Stage 6 phase and carrier midpoint, checked all four Stage 4 shield cycles via native missile-component damage, Furious Hammer, and gamepad A firing after a real save/load roundtrip.
- `_BUILD_SOURCE/probe_latest_repairs_0920.py`: passed again; a native projectile hits a distant Stage 4 escort, password flow and graphical pickup text remain valid.
- Additional browser checks exercised the failed stealth ambush (3 lives to 2), Stage 9 snapshot restore, post-space ground inventory restoration, orb damage to an escort (128 to 105 HP), fixed-bay Freezer form selection, and Debug launching Hammer.
- `_shots/editor_0922.py`: passed with no page/console errors. Changed HP through the actual field, saved, reloaded and retained 4321 HP with overrides enabled. Added and dragged a scene waypoint from (6, 5.5) to (7.5, 6.5) tiles. Selected and spawned an enemy through Debug's roster, then applied its live inspector.
- Visual evidence under `_shots/repair_0922/`. Checks use ephemeral Chromium profiles and do not alter the user's saved editor documents.
- Recording review used sampled frames from the supplied 24-minute recording; it shows Stages 1–4. This is not an exhaustive real-time audiovisual review.

## Still open — do not mark complete

- [ ] ElevenLabs production sound bank and audible mix review for every enemy/boss/weapon. Generated carrier-fan and cannon batches in the signed-in account, but browser download/export did not deliver local files. Local SFX API credentials are absent; requested local configuration, never a key in chat. Existing ColeForge bank remains in use. No claim that the generated ElevenLabs sounds are installed.
  - Carrier history: `9Q7qzl9G7Y0af30vOwN8` (four candidates).
  - Cannon history: `Vs0ZaYKIfCB5aZmHjgPe` (four candidates); first saved to ElevenLabs Assets as `One short powerful futuristic boss cannon discharg.opus`.
  - 134 ElevenLabs credits used in these two batches. No further batches while export is unresolved.
- [ ] Pin Stage 6 reveal to the measured main riff of City in the Sky. Current reveal is 22 seconds into this opening; launch/music timing needs an audible pass.
- [ ] Comprehensive full-fight balance/playthrough review for Stage 3 Hard/Furious and Stage 4/9. Component/idle checks do not certify every phase or difficulty; the remaining baseline failures must not be hidden.
- [ ] Full Boss Mode redesign and adapters for scripted fights (including custom Hammer). Existing grid/path/art tools work only where the engine supports them; data-only fields remain labeled. No private GPT API key was supplied or embedded.
- [ ] Complete projectile/art-family audit beyond the corrected pickups and current static projectile paths. Do not blindly alter ship bank/roll or authored directional frame sets.

Older requests remain tracked in `REQUEST_CHECKLIST_0914.md`; its historical completion totals have not been recomputed for this new repair batch.
