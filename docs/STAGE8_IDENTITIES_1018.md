# Stage 8 identity and defeat correction — October 18

Mike requested the new Dracodia avatar and death acting, removal of the extra
Hammer arm, actual Stage 5 Hammer combat, actual Stage 2 Furnace modularity,
distinct symbiote attacks, and the Colossus lifting both arms and roaring.
The older modular Harrier was explicitly approved for this pass.

`assets/stage8_identity_1018.js` and its generated art registry load after the
previous PixelLab Stage 8 layer. They are Stage 8 scoped. The existing three
outer encounters and five finite final pools remain authoritative: Colossus,
Hammer, helicopter, Harrier and volcano. No sixth identity is enabled.

- Hammer uses the live `hammerBossTick`/damage controller, its committed
  strikes, depth scaling, armor, missile recovery counter and Chromium
  bottom-half columns. Existing HK5 plates contain the correct two arms.
  The native sixteen-frame left/right swings use their measured tips and
  one luminance-preserving symbiote recolor. No pasted third arm survives
  in combat, onion display, entry, exit or defeat.
- Volcano has six registered render plates and four native Furnace damage
  pools. Arms break first, then the body, then the detached head. Arms aim,
  recoil and spin with the Stage 2 controller. The flamethrower remains a
  continuous authored fire plume; the other arm alternates magma and fire
  waves. The head charges, shakes and completes a committed 360-degree
  twin-eye sweep using Stage 2 difficulty timings. Muzzles and eye sockets
  are measured on the actual plates. Whole-body extents stay on screen.
- Harrier restores the approved older six-piece fan/launcher/reactor rig
  and its native carrier controller. Destroyed pieces stop their attacks.
- Infused host uses physical talon lunges and optic spores; Ghost uses
  claw rakes, soul bursts and forming/closing purple-black void wells.
  The helicopter fires from its pods, drops belly bombs and sheds rotor
  spores. Colossus uses scythes, core spores and a radial void roar. Its
  arms never launch ordinary missiles or gun lasers. All melee collision
  follows the visible moving limb masks. Warnings match the attack origin.
- Every module retains real owner/part hit flashes and expiry. No timer
  is zeroed or skipped to preserve a palette. Copy pools and module damage
  persist across visits. Furnace pool rounding cannot increase total HP.

PixelLab generated the avatar, sixteen speaking poses, twenty-four roar,
twenty-four scythe, twenty-four host-collapse, twenty-four Ghost-implosion
and thirty-two final death source poses. Twenty detailed final death poses
were selected; the flat clover-shaped blast tail was rejected. The native
detailed explosion banks finish the blast. Final armor splits into real
80x80 pixel fragments, retains opacity, scatters beyond the playfield and
explodes repeatedly. A last copied form shatters and reforms Dracodia before
the true final death. No old-body sunbeams or old avatar remain in that scene.
The existing red return portal and reunion still pay one campaign reward.

All generated source frames are 256x256. Shipping boss/action cells use
320x320 with pivot160,160; source pixels receive shared32px padding. One
common proportional scale is used per bank. Existing Hammer bank geometry
and its actual physical tips are preserved. There are315 new shipping PNGs,
9,370,795 bytes (8.94MiB), plus the small registry/runtime. Existing art is
retained; no shared atlas was edited.

Sources, job IDs and prompts: `_ART_SOURCES/stage8_identity_1018/`.
Owner: `_BUILD_SOURCE/build_stage8_identity_1018.py`. Native donor reference
inspection: `_BUILD_SOURCE/export_stage8_identity_1018.py`. Onions/contact
sheets/GIFs and browser captures: `_shots/stage8_identity_1018/`.

Review: `docs/previews/stage8_pixellab_1018/index.html`. It runs the actual
game index, isolates campaign saves, and offers each identity, the new
avatar, roar, final death, detached Furnace head, module breaks and onion
views. The review pilot alone is invulnerable; production controls retain
their existing protection rules.

QA results are recorded in `docs/qa/stage8_identity_1018.json` after the
complete native and core runs. The first browser pass caught an invisible
Harrier lookup and a one-point Furnace rounding heal; both were repaired
and rechecked on Normal, Hard and Furious. Source `game.js` and the core
suite are unchanged by this correction; their pre-existing edits remain.
