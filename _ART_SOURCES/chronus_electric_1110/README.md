# Chronus death revision — electric radiance and sustained shatter

Mike's November 10 correction replaces the heat-shield/fire aura and implosion. The new owner keeps the full native death dialogue, committed shot/core impact, two-second ignition and five-second outward breakup, followed by the existing cutaway/reward ownership.

## Requested behavior

- The defeated boss continuously trembles through fixed integer offsets and alternates normal/lighted and authored white flash states.
- The source-pixel **1015** treatment illuminates his existing violet/blue emissive clusters with six baked brightness steps and up to three hard pixel spill rings. No heat shield, solid glow dome or fire outline is used.
- A new sixteen-frame prompt-generated electric aura progressively reaches outward. Thin white/cyan/cobalt branches remain open so the boss shows between them. Early frames build reach; the final eight crackle continuously.
- His original eighteen source-pixel armor cuts fly outward. Their sixteen orientation drawings per piece are authored offline; runtime selects frames and translates them, without adding runtime sprite rotation or scaling.
- All three user-selected explosion families fire throughout the breakup: the orange heavy boss blast (attachment 1), blue/ivory Dracodia electrical surge (attachment 2), and gold/blue Stage 5 core ignition (attachment 3). Explosions occur around both the source and moving pieces. They use fixed 176-pixel and 320-pixel authored size banks, with at most twenty simultaneous instances. Each individual explosion has a finite fourteen-frame lifetime and no added opacity fade.

## Art and provenance

The new electric aura was created with built-in image generation using the actual hf17_stunned_00 pose and the user's blue explosion sheet as references. Raw master and exact prompts are retained. Keying, despill and a shared palette use the saved clean-pixel-effect-gifs workflow at native crop size, with fixed padding and a stable origin. It was revised once to retain complete branch tips. This is a sprite-sheet adaptation of the GIF-prompt method.

The three explosion drawings are the user's selected existing generated assets, not newly invented substitutes. Their original native 176-pixel frames are retained exactly. The 320-pixel bank comes directly from each lossless generated master and its established palette. It does not enlarge a reduced sprite to fabricate detail.

The body light/white states derive from the exact native source plate; the original opaque source alpha is retained before one consistent direct native-size export. Added light spill lies only near original emitter clusters. Armor shards derive from the original HF17 cut images and retain their source mounts/trajectories. No new character anatomy is generated.

Source owner: assets/hammer_finale_1017.js. Assets: assets/game/levels/stage_05/boss/chronus_electric_1110/. Rebuild: _BUILD_SOURCE/build_chronus_electric_1110.py. Durable inputs, prior owner and manifests: _ART_SOURCES/chronus_electric_1110/. Old rejected aura/implosion assets remain on disk as history but are no longer used by this owner.

## Verification

The candidate was rendered in real Chromium from the current game's native final-defeat checkpoint, including the complete buildup and breakup. The capture reports normal and white body draws, progressing aura frames, all three explosion families, and source armor pieces leaving the scene. No page errors were captured. Exactly one native core impact, armor release and ending handoff remain. Native captured images are the game's renderer, not a reconstructed Python scene. Installed-source validation and any full-suite limitation are recorded in verification.json.

No commit, push or installer publication is included. Cleanup code: Kasperzack Games, MIT, https://github.com/kasperzackgames/chatgpt-pixel-effects, revision d25ce128ac5f2487e8187d0f1c6f4ac27dced599. The code license does not relicense Mike's BOF artwork.
