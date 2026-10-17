# Stage 4 Warden helper entry safety — October 17

Mike reported that the updated helper jets killed him while shrinking into the
screen from the south or sides. The new orbit wing cleared `_noHit` after only
25% of its 1.25-second entry. Its visible scale was still greater than one, but
the normal body-contact loop could already kill the player. Newly spawned jets
also lacked the protection until their first movement tick.

`assets/warden_last_stand_1017.js` now sets `_noHit` at spawn and keeps it set
through the complete entry. The existing orbit branch restores ordinary contact
exactly when the jet reaches scale one. South, north, east, west and every
five-second replacement share that path. Entry releases no gunfire. Settled
jets retain their orbit, committed warning/burst cycle, destructibility and hit
flash. The Warden's own attacks retain their existing pressure.

The owning module contains the previously authored orbit-wing and last-stand
update on which this repair depends. It loads after `stage34_assault_1014.js`.
The loader cache key is `warden-entry-safe-1017`.

## Verification

- `_BUILD_SOURCE/probe_warden_entry_safety_1017.py`: **43/43** in real Chromium,
  zero page, console or missing-asset errors. Covers Hard, Furious and Insanity;
  all available entry edges, initial spawn, the full scaling interval, actual
  unshielded player overlap, on-plane collision, five-second replacements,
  warned gunfire and damaged pixels with naturally expiring hit feedback.
- The same native probe passes **43/43** against the exact publishing candidate:
  the existing GitHub build plus this owning module and loader, with unrelated
  local gameplay modifications excluded.
- Preserved pre-fix source is a broken control: the probe detects **30 failed
  entry checks**, including real unshielded deaths during the incoming pass.
  On-plane collision and the remaining attack/feedback checks still pass.
- Existing `probe_warden_wing_1017.py`: **41/41**, zero browser errors. Normal
  keeps the old fly-in turns; Hard has four orbit jets, Furious/Insanity six.
  Circling, five-second same-edge replacement, module/hull hit feedback, sounds,
  no-lightning rule and last-stand attacks remain active.
- `node --check assets/game.js` and the owning module pass. The current local
  full suite completes with **8,742 passing / zero failures**, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS`, exit 0. That suite also includes the separate
  local modular-hit and spread work; the candidate browser run above verifies
  the narrower published build directly.

The collision fixture isolates the miniboss hull through its existing
`_s4MiniSafe` flag so a helper test over the hull measures the helper alone.
It retains the real enemy contact loop, real `playerHit`, damage and rendering.
The combat-plane positive control still kills the unshielded ship. These are
controlled fixtures, not a claim of a complete human campaign clear.

South/side overlap captures were inspected. Logs, the preserved broken source
and screenshots are under ignored `_shots/warden_entry_safety_1017/`; portable
results are in [warden_entry_safety_1017.json](qa/warden_entry_safety_1017.json).

Other local tutorial, modular-hit, weapon and launcher work remains untouched
and outside this publication.
