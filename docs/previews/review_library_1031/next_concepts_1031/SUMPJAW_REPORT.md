# Sumpjaw pair and twelve new encounter concepts

SJ98 implements Mike's approved Sumpjaw as two independent creatures in Stage7's Furious miniboss slot. The native Insanity difficulty follows this Furious-family route. Normal and Hard retain Caustic Dredger. Each Sumpjaw owns an authored overhead health frame and its own25% /25% /50% gill/gill/intake-heart budget. The standard screen-top miniboss bar is not drawn for this pair.

## Combat and progression

The pair shares the former Dredger health budget plus10%, divided evenly between the two actors. Both gills on a creature must be destroyed before its heart becomes a target. Sealed center pixels do not consume bullets; all four starting gills are reachable through normal gunfire, beams and native Retina targeting. The parent displays the sum of all actual surviving pools. Native first-hit protection on new pools remains. Destroyed gills retain their metal outlines with charred, cracked liquid interiors; the whole body is never chopped into rectangular pieces.

A shared director permits one heavy attack at a time and alternates the living actors through a breach, three toxic lobs and a bite. A breach dives, acquires a moving floor mark during the first42% of its1.35s tell, commits, then rises through authored depth/rotation frames. It cannot be targeted or bite while submerged. A1.25s bite tell marks the committed impact point before a0.45s lunge and visible recovery. Lobs leave the actual mouth, arc toward separate ground Retinas and splash into five finite unshootable droplets; no bouncing fragments. The resting partner stays out of the active creature's lane. Camera-relative rest positions preserve both complete passive silhouettes at either camera edge.

White hit frames have the exact normal alpha and a65ms flash with a160ms retrigger interval, retaining clear damage feedback without permanent white glare under a held beam. Gill rupture interrupts that creature and exposes its heart; the surviving actor keeps its own HP and behavior. Each creature trembles, blows up and scatters source-derived pieces. Only exhaustion of both real health budgets triggers the single native miniboss achievement/reward/handoff. Stage7 Warden, collapse and portal owners remain unchanged.

New Game Plus adds exactly25% to all three pools on each actor once. The shared director gap and native recovery clocks speed up15%; warnings, entrances, projectiles and deaths keep real-time duration. Pause freezes the encounter. Actual shared-mixer charge, warning beeps, bite rush, impact, toxic spit, module-break and explosions were recorded and decoded.

## Production assets and sources

- `assets/sumpjaw_duo_1031.js`: isolated paired encounter owner, native point/beam/Retina damage routing, contact, attack director, local bars and one final reward.
- `assets/sumpjaw_art_1031.js` / `assets/game/levels/stage_07/miniboss/sumpjaw_duo_1031/`:847 fixed authored frames in18 even-cell banks. Complete source body motion, normal/hit/1015-hot states for four gill conditions, baked turns/depth, existing toxic orb/splash and native ground Retina, source-pixel fragments and custom local health art. No runtime sprite rotation, scaling, alpha animation, tint/filter or procedural VFX; only fixed blits, clipping and horizontal flipping.
- `_ART_SOURCES/sumpjaw_duo_1031/`: approved original concept, generated transparent production seed, all original PixelLab frames, exact prompts and18 editable Aseprite banks.
- `_BUILD_SOURCE/build_sumpjaw_duo_1031.py`: deterministic offline source recipe. It reproduces every installed PNG exactly. Source sheets and editable animation files retain common pivots, even cells and one proportional source unit.
- `_BUILD_SOURCE/test_sumpjaw_duo_1031.py`, `test_sumpjaw_edges_1031.py` and `record_sumpjaw_duo_1031.py`: reusable native probes and input-only recorder; outputs go to ignored `_shots/sumpjaw_duo_1031/`.

Generation mode: built-in `image_gen.imagegen`, transparent production seed using the approved Sumpjaw board as identity reference; PixelLab `animate_image` for two8-frame motion generations plus each supplied first frame,192x192, transparent, seeds730198/730199. Jobs86d8100a-a47b-46d3-a506-ff196b86ee00 and09cadfa8-bf7c-47d5-b233-662826f04987. Reported PixelLab credit charges total$0.0603. Generated seed originally saved at `C:/Users/Mike/.codex/generated_images/01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f/exec-a5897aa3-96f6-4f1d-b37f-ffed101d33e6.png`; project copy is `_ART_SOURCES/sumpjaw_duo_1031/sources/generated_sumpjaw.png`. Exact source and animation prompts: `_ART_SOURCES/sumpjaw_duo_1031/generation_prompts.json`.

## New concepts awaiting approval

Six new1536x1024 boards contain twelve separate proposed designs. Each board presents a miniboss and boss; either can be selected independently.

| Stage | Option | Miniboss | Boss |
|---|---|---|---|
|6|A|Windrazor|Stratosphere Leviathan|
|6|B|Draft Widow|Sky Anvil|
|6|C|Cloud Guillotine|Tempest Choir|
|9|A|Eye of the Undertow|Pelagic Crown|
|9|B|Abyssal Nautilus|Trench Cathedral|
|9|C|Prism Wraith|Riptide Hydra|

All Stage9 proposals are modular and built from scratch around the current alien-optic/hydraulic roles, using actual native stills for palette and role reference. The space/void arena stays. Each brief identifies detachable assemblies, true weapon sockets, planned attack counters and future frame requirements. These are approval concepts, not cut-ready production sprites or verified attack patterns. Exact canonical module counts and frame/target assembly must be locked after selection. Stage6/9 live encounters and Dracodia/Herald art/controllers were not changed.

Saved concept boards and full design briefs: `docs/concepts/next_wave_1031/`. Exact prompts/tool mode: `prompts.json` and `GENERATION.md` in that folder. All six used separate built-in imagegen calls. Browser shortlist is local storage only and never activates encounters or represents production approval.

## Verification and footage

52 focused checks pass:30 frame/native encounter checks,7 additional camera/native-gunfire/NGplus checks,3 source/rebuild checks and12 browser/gallery/playback checks. Covered all gills and protected hearts, visible white damage/expiry, individual/full defeat, finite splashes, no heavy overlap, pause, retry, normal/hard retention, both camera edges, actual machine-gun damage, exact NGplus health and warning timing, desktop/mobile layouts, all six generated boards, independent saved shortlist, native video seek/play and preserved Dredger chapters. No browser, rendering, asset or audio-tap errors. Actual native and decoded movie frames were inspected; the first recording's camera clipping was corrected and the current film recaptured.

Fresh full-budget native Furious film: 74.035s,1280x800,30fps capture,57.89 average native engine fps. Both Sumpjaws start intact,1116HP each /2232HP total. Cole uses native GOD and input-only controls, initially level5 Laser and40 missiles; normal pickups can change his weapon. First25s demonstrate the book. All damage, gill breaks, individual deaths, whole pair defeat and stage return run through native rules. No enemy HP/phase/timer writes during filming. Full movie decode is clean; audio mean_volume: -20.5 dB / max_volume: -2.3 dB.

- [Fight and all new concepts](http://127.0.0.1:51046/furious-next-wave-1031.html?v=paired-final)
- [Full fight in the existing library](http://127.0.0.1:51046/?sumpjaw=duo-1031#clip=stage7-sumpjaw-duo)
- Local video: `C:/Users/Mike/Documents/New project/BOF-Downloaded-Stage6-9-1028/https://github.com/NexusWebOS/BulletsOfFury/releases/download/bof-complete-review-2026-10-31/preview--videos--stage7-sumpjaw-duo-1031.mp4`.

Current `stage7-miniboss` and new Sumpjaw shortcut use this film. Dredger's previous film and all four chapters are retained separately for comparison. The prior concept page links to the new review. QA evidence: `docs/qa/sumpjaw_duo_1031.json`.

Syntax checks pass. Required full `node _BUILD_SOURCE/test_fl.js` completes with exit1 and the same five pre-existing failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

Core `assets/game.js` SHA256 remains `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`. No Git commit, push or remote video upload was requested/performed in this pass.
