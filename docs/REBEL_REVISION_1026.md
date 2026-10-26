# Rebel animation and live shield revision — October26

Owner: assets/rebel_revision_1026.js, loaded after the prior encounter/render owners.

- Cloak: 24 indexed material-fade steps and 16Hz background refraction through the actual heading alpha. No Nyx spiral. Heading cells have shared pivots/scale; surviving native module clips and white hit feedback remain.
- Decker: the old team-cloak rescue is replaced with a third shootable supply icon in the live Stage6 squad fight. Native allied AI targets it, Decker shots break it, and an eight-second cyan holographic wall covers the lower half of the playfield. It reflects bullets/energy/missiles defensively toward different surviving rebels, dealing native damage on return contact. This does not make ordinary bullets offensively shootable. The separate Stage10 duel gets no wall intervention.
- Radio: live portrait dialogue announces the wall, the rebels react to returned fire, and Cole/Decker exchange the surprise/nick-of-time banter. It never pauses input or combat.
- Heavy arsenal: background guns have one active lane with longer tells; dense tracer emissions become lower-rate destructible energy charges. Voss fusion becomes a charged projectile. Jace retains his helix ball; player interception triggers a local 210-unit counterburst against live rebels using their native damage owner. Unintercepted helix bursts threaten the player within 42 units, without spawning a bullet ring.
- Flight: all five use the authored eight-heading bank instead of AF21 static-frame rotation. A separated staggered formation commits a missile volley, then makes fast diagonal north/south departures and continuous returns. Native HP, module budgets, Retina, owner death and reward rules remain.

Generated PixelLab art: wall_box.png 128x128 (job aacea785-8b66-4236-bb22-4019c4555a1e); wall.png 384x160 (job eb66ba27-7e06-4fbf-8f5e-34542a49fdfd). See the adjacent asset manifest. The wall uses proportional fill with playfield clipping.

Verification: _BUILD_SOURCE/probe_rebel_revision_1026.py, _shots/rebel_revision_1026/report.json. Ten native checks cover actual player-shot helix interception, Decker-shot box opening, multiple reflected targets/native damage, frame selection, live scene ownership, flight and actual damaged pixels/flash expiry. A sustained Normal opening/gang audit ran 45 seconds each with full allied AI and no browser errors. Recording uses live allies, a protected non-firing observer and a scheduled rescue checkpoint; it is a focused preview, not proof of human survival or a full campaign clear. Native sounds are captured through the shared mixer.

Syntax checks pass. Required full test_fl.js still exits 1 before assertions/final summary due the existing missing retired_art_archive_1022.cjs. Dark weapon variants remain a separate deferred pass.

## Central two-way wall correction

The wall now tiles three proportionally drawn authored panels into a narrow horizontal divider at the visible screen center. Native player/allied/rebel positions cannot cross its solid band. Swept projectile checks return hostile fire toward rebels and return friendly shots as hostile energy toward the friendly side; continuous player beams stop at the wall. Decker explicitly warns that it reflects both ways. The wall uses the actual 1015 glow baker's emissive mask/rings, with an explicit cyan-grid mask for this self-lit effect, registered through PXG_SHEETS and driven through its six brightness steps at 12Hz. Impacts drive the grid to peak. Rebuild companion with _BUILD_SOURCE/build_rebel_wall_glow_1026.py. Three panels retain the source proportions and are cropped to the authored frame edges, not stretched.

The dedicated rr26WallHum loop reuses the shared helixCharge energy bed through Snd, preloads, maintains gated playback, and stops on expiry/stage change. Native recording confirms readyState4, audible playback and on=false after expiry. Current evidence is _shots/rebel_wall_1026/report.json and center_video/. The full suite still exits1 before its final summary on the existing missing retired_art_archive_1022.cjs.


## Missile Retina correction
Rebel personal rockets and formation missiles now use target-centered authored animated Retina locks, without missile FOV lanes. The existing shared-mixer retinaLockBeep accelerates from 0.32 to 0.10 seconds during acquisition and stops when the native launch/recovery cancels the tell. Other attack warnings and shootable physical missiles remain unchanged. Native Chromium: 18 checks pass, including no missile FOV draw and active lock cue, actual Retina screenshot inspected, no page/console errors. Syntax passes; full suite exits 1 before summary on existing missing retired_art_archive_1022.cjs.


## Kaia roller gatling
Kaia personal windspread/rocket attack is replaced after native scheduling/interlocks with a 1.35-second committed warning, 8/12/14/16 medium roller balls by difficulty at 120ms cadence, then 1.4-second recovery and native cooldown. Uses actual nfrb_0..3 Falva frames at 20fps, 40px proportional canvas, cyan-green palette, native shootable ordnance HP/flash/death and reflected-wall ownership. Removes her attached launcher plates and background cannon rounds. Formation missile Retina rules remain. 20 native checks pass, including 12-shot Normal burst and interception; screenshot inspected, no browser errors. Syntax passes; required full suite still exits 1 before summary on missing retired_art_archive_1022.cjs.


## Rook chaingun / Voss charged dash
Rook pauses for a 1.65s authored FOV and pilot-colored Retina tell; lock beeps accelerate, aim commits after 72%, and the final 30px capture decides limited 1-second bullet tracking. Actual unshootable s6tracer rounds at 90ms cadence, native heavy machine-gun cue/muzzle and finite recovery. Owner death cancels bullets. Voss retains native turbo cruise and replaces the energy cannon with an animated energy charge and 780px/s dash, offscreen exit, concealed reposition and continuous north entry at original scale. Native ram collision and authored heading cells remain. 23 native checks pass; syntax passes; required full suite exits 1 before summary due existing missing retired_art_archive_1022.cjs.


## Authored attack animation and Decker casting
Restored existing AF21 idle/attack cells for forward-facing combat and actual AM13 roll frames for upright evasions; directional travel retains its authored heading cells without canvas rotation. Native part clipping and real white hit flashes remain. Rook now uses native chaingun round art, paired measured emitter offsets, chaingun muzzle family and release recoil. Kaia uses a visible nfrb charge at her nose and matching orb releases; stray generic energy rounds from both are suppressed. Voss accelerates into the dash and eases into his north return. No new generated art or atlas mutations.

Decker launches an authored cyan energy orb from his live ship over 1.4s; the wall builds outward over .65s, holds fully active for 10s, then fades in 24 renderer steps over .9s. Collision starts after construction and ends as dissolution begins. Existing 1015 glow, dedicated hum, bidirectional reflection and actor-side blocking remain. Total lifetime 12.95s. 24 native checks pass and build pixels inspected; syntax passes; required suite still exits 1 before summary on missing retired_art_archive_1022.cjs. Fresh film in _shots/rebel_wall_1026/animation_video.
