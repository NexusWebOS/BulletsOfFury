# Furyship cloud-flight revision — September 14

Mike rejected the earlier small, six-piece assembly and slow sky/space sweep.
The new Stage 5 fighter intro now stays at **420 pixels per second** throughout
sky travel, assembly, reveal, loading and countdown. It does not enter the old
braking or 40-pixel cruise phases.

## Sequence

1. Twelve seconds of extended sky travel. The plane initially flies over the
   existing authored sky. Dense foreground clouds then rush past, with natural
   gaps that reveal the plane and arriving kit.
2. The cloud deck opens into a clearing surrounded by moving cloud banks. The
   original six component families now form **twelve independent pieces**, adding
   paired gun sections, boosters and shoulder sections from the authored kit.
   No new generic placeholder art is used.
3. The assembly is presented at a 118-pixel cinematic hull size. Full-size loose
   component cells draw at 194.7 pixels (118 × 1.65), with smaller paired hardware
   proportioned separately. They converge into the approved completed fighter.
4. Fusion fades the **entire screen** to white, holds white, then fades back to the
   completed ship in space. The backdrop changes only underneath opaque white.
   HQ, the model label and scanlines are covered by the fade too.
5. The fighter eases to its 48-pixel play size during the countdown. The background
   continues at the same fast intro speed. An already-earned fighter skips the
   rebuild and retains its normal size.

The energy ring now stays near the ship: charge effect width changed from 2.6×
to 1.22× hull size, and fusion width from 2.1× to 1.12×. The old large vertical
curtain and travelling cyan horizon strip are not used by this revised intro.
The flame/thruster reel keeps animating during the countdown.

This implements Mike's latest fade request, which supersedes the older prohibition
on fades for this sequence. Other stages and the SPCBOY legacy intro retain their
existing routes. Normal Stage 5 gameplay retains its existing scroll tuning after
the intro hands control to the player.

## Art and verification

Clouds are the inspected authored `campaign_map_v2/cloud_0..6.png` family, loaded
through its existing `cm2_cloud_*` XART keys and drawn above the aircraft. The sky
is the existing `stage6_blue_master`; no biome plate or shipping atlas was edited.

- `node --check assets/game.js`: passed.
- Full suite: **3,850 passed / 60 failed, exit 1**, final summary reached. All
  failure names exist in the previous baseline. The historical random sand-tank
  assertion passed this time; no sand-tank fix is claimed. Test file unchanged.
- Native Chromium via `shoot.py`/`capture3`: **11 scene checks passed**. The full
  intro ran from time zero with the entire HQ line and no phase skipping. Checks
  include measured scroll increments, twelve pieces, enlarged drawing sizes,
  sky retention until white, opaque-white backdrop swap, all-white pixel coverage
  and the final handoff to PLAY. No page, console or loop errors.
- Separate native retained-fighter probe: no rebuild, 48-pixel ship, both exhaust
  frames, constant speed and zero browser/loop errors.
- Screenshot sequence visually inspected. The **26-second H.264/AAC video** is
  `_shots/furyship_cloud_0914/BulletsOfFury_Cloud_Transformation_0914.mp4`.
  The game event log supplies synchronized sound effects; constant export gain
  prevents clipping. ffmpeg decoded the entire final movie successfully.

Capture-only invincibility prevents a death after GO from ending the demonstration.
No runtime invincibility or gameplay audio-volume changes were added.

Proof: `docs/qa/furyship_cloud_intro_0914.json`.
Runtime SHA-256:
`3d55604968cc2af62926ed8ef7ed296a03cf051c57d87686ad6434d9405e2978`.
Runtime LF and test CRLF preserved. Source/build/capture tools are in
`_BUILD_SOURCE/furyship_cloud_0914/`; the guarded integrator starts from the prior
live-integration snapshot and must not overwrite later work.

Checklist totals remain **51 complete / 11 partial / 73 pending**. SPACE-12 still
tracks generated-pose silhouette consistency and component perspective refinement;
this revision addresses the requested staging, visibility and speed. SPACE-13's
effect/transition evidence now points here. No commit, push or user-data deletion.


## Later solid-assembly revision

The current faster intro, opaque top-view parts, individual bottom entrances and removal of travelling cloud caps are documented in [FURYSHIP_SOLID_ASSEMBLY_0914.md](FURYSHIP_SOLID_ASSEMBLY_0914.md).
