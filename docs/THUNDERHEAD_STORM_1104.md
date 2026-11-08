# Thunderhead storm reactor — November4

Thunderhead's Furious Stage6 left-route encounter now controls the city weather
and attacks with its reactor instead of relying on a generic gun/front book.

| Turn | Tell | Active attack and counter |
| --- | --- | --- |
| Cyclone Salvo |1.6s staged cyan/white core1015 charge and committed lanes |Three waves of core-born rotating wind cyclones; surviving guns fire straight lightning hail. Break a module to cancel its owned rounds. |
| Twin Tornadoes |1.6s core/pressure charge and tower lanes |Living pressure towers launch growing, looping and dissipating electric tornadoes. A central route remains open. Destroyed towers cancel their own fronts. The exposed core retains a single-tornado fallback. |
| Thunderstorm |1.9s core charge; darker clouds and heavier rain |Four finite ground strikes. Each actual landing mark gets2s of green/yellow/red warning and audio before impact; it never tracks after commitment. Collision matches its44x22px ground ellipse. |
| Tempest Cataclysm |2.8s escalating core charge and a200px committed lane |A304px animated electric hurricane leaves the real core; its180px contact width leaves90px flank corridors in the committed camera view. Three additional marked strikes keep it a lightning storm. The front persists through contact, then leaves through the bottom. |

The four-turn healthy book is cyclone/tornado/thunder/tempest. The exposed-core
book prioritizes tempest. Native6348HP, six destructible modules, core protection,
hit flashes, damage attribution, rewards and defeat remain with FB112. Normal,
Hard, Stage X and the Rough Riders route keep their existing encounters.

Weather consists of two separately moving source-authored cloud families, baked
storm-lighting steps and two rain densities behind ships/projectiles. Simulation
time drives every layer. Pause freezes it; death/cancel/retry/stage exit clears
owned marks/fronts/rounds and relinquishes weather. Reduced-motion mode holds the
core loop and shortens decorative bolt exposure. Source-over only: no new runtime
opacity/palette/rotation/scale animation or additive glow.

## Art and ownership

- `assets/thunderhead_storm_1104.js` owns the storm turns and scoped weather.
- `assets/thunderhead_storm_art_1104.js` contains source rectangles, timing and hashes.
- `assets/game/levels/stage_06/boss/thunderhead_storm_1104/` contains13 banks /193 fixed frames,5.59MB of PNG pages.
- `_BUILD_SOURCE/thunderhead_storm_1104/` contains the builder, actual registered source exports, Aseprite sources and verification/recording tools.
- Existing approved storm_source art, native cloud frames, lightning and ground Retina art are reused. No additional generation credits were spent.
- FB112 skips its legacy additive hull flow for Thunderhead and opens pressure frames for the new tornado turn. The previous exact collision masks/lossless pages/performance correction remain intact.
- PFX13 recognises these already-authored storm rounds: it counts their visible draw but skips runtime cleanup/recolour/glow/trail synthesis. Other rounds retain their existing renderer.
- Caps:24 ordinary rounds,4 weather fronts,3 ground marks,4 impact aftermaths and6 core/pressure muzzle events per owner. Observed ordinary-round peak11 and twin-front peak2.

## Verification

-22/22 native checks: actual attack book, clocks, HP/core gate, sockets, part cancellation, warned impacts, finite caps, pause, death/reset and route separation; no page/render errors.
-193/193 frames re-exported through Aseprite: exact visible RGBA/alpha retained across all13 banks. Isolated effects keep their fringes inside the cell; rain/grade intentionally tile and lightning intentionally continues beyond the top edge.
- Uncaptured high-quality real-RAF profile:59.93FPS over50s, p95 frame gap16.8ms, p9917.1ms. All four turns occurred.
- Final full native high-quality fight:53.66 engine FPS,101.552s, native HP/defeat,0 pilot deaths with labelled GOD.45s player hold-fire; native allies continue acting.
- Charge, wind and lightning were observed in actual capture audio; peak-0.5dB. Full movie decode, native health, source stability, asset/browser/audio checks passed.
- Combined-cabinet capture caused costly cross-canvas copies in diagnostic takes. The final take records the actual960x1024 game canvas directly, including its native boss bar; cabinet side rails are outside that canvas. No game art-quality reduction.
- Preview11/11 checks: real frames/dimensions, seeking/playback/audio, byte ranges and mobile width.
- `node --check` passes. Required `_BUILD_SOURCE/test_fl.js` still stops before its summary on the existing `difficultyHealthBaseline15 is not defined` in combat_polish_0927b.js:151. This is not a full-suite pass.

Movie: `_shots/boss_comparison_1102/thunderhead-storm-native-final-1104/stage6-boss/stage6-furious.mp4`.
Local review: http://127.0.0.1:65118/?storm=1104#thunderhead .
Detailed receipts: `docs/qa/thunderhead_storm_1104/`.

The GOD film demonstrates behavior and rendering. Human dodgeability and a complete
campaign run remain playtest work. This correction is local; no commit/push was requested.
