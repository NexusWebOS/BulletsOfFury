# Chronos silhouette aura and physical chaingun handoff — October 25

Mike rejected the detached flame-shaped rage aura and the unclear crate/pickup/
firing animation. This correction is in the live Stage5 owners, with a fresh
Furious recording on `docs/previews/chronos_frames_1025/index.html`.

## Actual faults found in Chromium

- HF22 painted the same four-frame flame field around every humanoid pose. It
  did not follow the body, weapon orientation or background scale.
- The later held-pose head resolver continued to report the old slam's hammer
  position after HT23 had released it. The thrown hammer consequently hovered
  in front of the body throughout the gun catch.
- CH23 requested animated body indices but its body and grip banks each held
  only one pose. Its old rotor moved mainly at the endcap and ran too quickly
  to read clearly. The crate's previous reel never visibly opened into a shell.
- C27's later activation owner bypassed the acquired-gun return path. Delegating
  that case to HT23 again preserves the gun and returns to `chain_warn`.

## Live changes

`assets/chronos_motion_1025.js` retires the Stage5 flame field. A small LRU of
alpha stencils traces the current authored plate; narrow red/pale contours and
short rising contour echoes use exactly its frame, pivot, rotation and scale.
No generic replacement sprite or silhouette is invented. The original plate
and its hit flash still draw on top. The 15%-HP charge raises the actual held
hammer and changes to red armor; it no longer selects the old baked flame image.
Permanent rage, doubled hammer clocks, native HP/counter rules and the original
eight whole two-handed spin views are retained. Stage8/HAMA keep their owners.

`assets/hammer_tactical_1023.js` holds the visible strike on the box before the
toss, then uses the actual release point and upward flight path. Sequence times
are centralized: impact1.78s, toss1.98s, release2.46s, gun ejection3.06s,
catch3.54s, tactical readiness4.72s. The box opens before ejection; its empty shell
falls only after the real gun leaves it. The full authored catch remains visible.

`assets/chronos_modular_1023.js` plays six whole-body recoil poses and eight
visible rotor phases plus rest, with rev-up and coast. The approved independent
gun and foreground grip remain registered to that intact body. Recoil affects
both the visible gun and its native muzzle/alpha target. Its native gun HP,
ordinary unshootable rounds, alternating down-rakes/fans, FOV reaction windows,
destruction recovery and white hit flashes remain. No held hammer modularity
was introduced. The shared pickup cue intentionally resolves to `weapon` in
`b20Cue`; impact, throw, pickup and chaingun playback are captured through the
existing mixer.

## Source selection and rebuild

- `_ART_SOURCES/chronos_aura_gun_1025` retains exact input references, all27
  PixelLab source frames, job IDs, original manifests and selection evidence.
- `_BUILD_SOURCE/fetch_chronos_aura_gun_1025.py` retrieves those selected jobs.
- `_BUILD_SOURCE/build_chronos_aura_gun_1025.py` owns the revised sheets and
  their registrations together. Old source sheets remain untouched.
- Recoil source frames3–5 were rejected for an invented side grip. Accepted
  whole poses0,1,2,6,7,8 use a uniform384×512 canvas and192,230 pivot.
- Generated rotor illumination/housing changes were rejected. Only moving
  barrel interiors are used, within the original104×208 silhouette, with its
  original receiver/handles/length,54,46 pivot, muzzle and metallic tonal range.
- The new crate is nine80×80 frames at40,40. Regular/chromium/red banks share
  geometry; white masks come from their actual alpha. All frame dimensions are
  even. No main production atlas was repacked.

## Verification

- Native targeted checks:22 passed,0 failed. Includes actual impact overlap,
  throw/catch ordering, every recoil/rotor phase's pixels, native gun damage and
  white flash expiry, real muzzle/round agreement, gun destruction, rev/coast,
  acquired-gun armor activation and pose/scale-dependent aura pixels.
- Existing final-combat regression:17 passed,0 failed (15% gate, permanence,
  raised chromium charge, three physical missile slams, no laser regression).
- Existing original-spin regression:16 passed,0 failed (whole two-hand frames,
  head pixels, damage/dodge, recoil, flash, HAMMER music-scene ownership).
- Aura's measured99th-percentile distance from the actual full-size body was
 12.1–12.7 pixels, and5 pixels at0.36 background scale. Pulses visibly change.
- Final47.1-second native review:9/0 AV checks; full decode, all six recoil/eight rotor phases, actual shared-mixer impact/throw/pickup/chaingun playback, no game errors. Decoded audio peak0.510 and RMS0.099. Review page plays unmuted, seeks correctly, and pose stepping changes native source pixels; no browser errors.
- Changed JavaScript and `node --check assets/game.js` pass.
- Required `node _BUILD_SOURCE/test_fl.js` exits1 before any assertion or final
  summary because `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. This
  existing blocker remains explicit; the suite was not bypassed or reported green.

Artifacts/probes are under `_shots/chronos_aura_gun_1025` and the matching
`_BUILD_SOURCE/*chronos_aura_gun*1025.py` scripts. Durable check results are in
`docs/qa/chronos_aura_gun_1025.json`. The audible review is explicitly labeled as
native checkpoint demonstrations, not a continuous full-fight clear. Earlier
footage is preserved as `combat-review-before-aura.html`. An invalid recorder
fixture that entered `storm_warn` without its attack setup was removed; the final
recording follows the native spin into its own background jump and combos.

No commit or push. Existing unrelated work and the original hammer assets are
preserved. `assets/game.js` and `_BUILD_SOURCE/test_fl.js` were not edited here.
