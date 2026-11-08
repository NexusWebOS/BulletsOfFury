# November 6 tester feedback repairs — revision D

The tutorial-to-campaign deployment conflict is fixed. Short effects use decoded
buffers through the existing mixer. Space loading and rendering are bounded without
reducing art resolution. The flamethrower now scales competitively with gun upgrades.

## Campaign flow and controls

- Completing training retains Campaign mode and reaches the native campaign introduction/map.
- Enter, Space, assigned Start and the normal Fire/Confirm action deploy the highlighted mission.
- Back/Esc opens the map menu. Its explicit Save/Load choices still work.
- Map entry clears old tutorial hover/held-click state. A pointer parked over Save cannot silently
  redirect the next confirmation into that menu.
- Fast mouse presses are buffered for mission/toolbar/save-slot input. Moving from the toolbar
  onto a mission restores map focus.
- Native saves, campaign progression, player profiles and Cole's unlock rules remain owners.

## Performance measurements

Same available Windows PC, headful Edge,1366x768,SS2/high-quality rendering,Furious,
Axel,seed116,real native Stage5 entry and a22-second opening with held primary fire.
The baseline routes the pre-change source snapshots into the same current asset build.
These are one paired local run,not a guarantee for every machine or encounter.

| Measurement | Baseline | Revised |
|---|---:|---:|
| Native Stage5 setup call |496.7ms|307.5ms|
| Complete ship formation/loading to play |28.43s|28.26s|
| Opening combat average |36.2FPS|53.7FPS|
| Combat95th percentile frame interval |83.4ms|16.8ms|
| Combat99th percentile |200.1ms|50.0ms|
| Combat intervals over50ms |55|11|
| Game clock advanced during the22-second sample |15.27s|20.63s|
| Attached short-effect streaming players at end |64|5|

Average frame rate improved48%; intervals over50ms fell80%. There are still occasional
cold frame spikes: this is not a constant60FPS claim. The revised run advances further
through the same opening because fewer long frames are lost to the simulation's safety clamp.

Changes:
- One sorted art index per stage replaces repeated scans of24,563 registered keys.
- Loader work is bounded to4ms per tick; three ship-kit images decode at a time.
- Boot-deferred kit requests retry rather than failing the134-image formation gate.
- Several active aircraft used2560x9120 sheets,about89MiB decoded per sheet. Their6748
  direction/animation cells now use lossless pages no larger than1536x1536 and a48MiB
  native-cell LRU. The observed sample used~9MiB of that cell cache,7851 paged blits,
  zero missing-page draws and zero fallback tints.
- The retired Voidreaver bank is kept on disk but excluded from current Stage5 warming.
- The pixel-glow tag carrier skips the main game canvas; offscreen tags remain intact.

## Sound

Short SFX now reuse decoded AudioBuffers instead of repeatedly evicting and reloading
HTML media decoders. Music and held loops keep their native streaming owners.

The64MiB decoded cache,32 active-voice cap,existing per-cue cooldowns,volume settings,
tone filters and shared compressor are retained or enforced. Voice/warning cues have
priority over incidental effects. Pending cues older than120ms are dropped rather
than appearing late; scene/cue cancellation also invalidates pending work.
Portal reflections reuse the same buffer with the native delayed/detuned timing.

In the matched revised opening,256 retained event samples had a0.3ms95th-percentile
request-to-buffer-schedule delay. This excludes output-device latency. The earlier
HTML-media probe observed~187ms95th-percentile request-to-playing-event delays;
the endpoints differ,so these are diagnostic transport measurements,not an
end-to-end listening comparison. Shared-mixer waveform output was nonzero; mute,
stop,unlock and portal/cancellation checks are included. No speaker/headphone
audition or whole-campaign sound audit is claimed.

## Flamethrower

The tester's upgraded-weapon complaint reproduced. Native sustained fire against a
stationary neutral Assault aircraft,Axel,Normal,no forge/missiles,measured the last
four seconds of a six-second firing sample:

| Level | Machine gun DPS | Previous flame DPS including burn | Revised flame DPS including burn |
|---|---:|---:|---:|
|1|40|46.2|46.2|
|3|120|87|129|
|5|288|135|291|

Fire gains27 visible pixels of reach at each level:138–228px before Forge modifiers.
Its width,tick cadence,burn ledger and multi-target behavior are unchanged. The new
fire tick table is3.6/7.2/10.5/19.5/24; Ice Breath keeps its previous damage/freeze role.
Element resistances still apply. Help and tester instructions explain close-range sweeping.
No broad Normal/Hard/Furious difficulty changes were made from one tester's feedback.

## Verification and limits

-6748 source-cell alpha/visible-RGB identity checks;26992 authored tint checks.
-120 native browser rendering comparisons: exact alpha/shape; RGB tolerance2/255 for
  intermediate Canvas premultiplication rounding,zero failures/missing pages/fallbacks.
-Focused tutorial/map/Save/mouse/audio/complete-formation/flame checks and separate edge tests.
-Current game/module syntax checks pass.
-The required full regression harness still exits nonzero on its pre-existing missing
  difficultyHealthBaseline15 setup helper in combat_polish_0927b.js:151,
  reached from test_fl.js:4537. No full-suite pass or complete campaign playthrough is claimed.
-Fullscreen native package and archive verification are recorded with the release receipts.
-No commit or push was requested or performed.

## Delivered build

Revision2026.11.06d: complete launcher/game ZIP3,876,756,470bytes,18,957files. SHA256:
8ec26d3bc5761a882967bc75c578b01b7b86a7c8c60c7978cd0c1819b61b9c38.
All18,956 payload/ready-folder files were checked by size,CRC and SHA256. All666
runtime script files in the packaged game match the current source exactly.
15 focused browser checks,9 edge checks and8 native Windows checks passed.
The native game launched fullscreen,produced measured mixer output,deployed Stage1,
and rendered paged Stage5 combat without missing art or game exceptions.
