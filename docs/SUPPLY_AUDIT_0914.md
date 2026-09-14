# Draven and missile supply audit — September 14, 2026

Decker's transformation now announces **SPACE FIGHTER DRAVEN**, as Mike requested.
The next queued item, MSL-09, now covers the remaining missile-supply routes.

| Route | Easy/Normal | Hard/Furious |
| --- | --- | --- |
| Boss opening supply | 7 seconds | 5.6 seconds |
| Boss repeat supply | 18 seconds | 14.4 seconds |
| Fodder loose-missile roll | 10% | 12.5% |
| Legacy single-ammo roll within its eligible death route | 6.2% | 7.75% |
| Scheduled level/guaranteed phase crates | Original crate | Original plus a 25% bonus-crate roll |

Finite stage events use a bonus probability rather than duplicating every box.
Earned extra crates wait at least two active seconds and until the original box
and any released missile pack have cleared. Bonus crates cannot roll more bonus
crates, and the already accelerated boss clock does not receive another bonus.
The queue pauses with gameplay, waits during real player death, can carry into
the next stage, and clears on a fresh run or campaign load. It is shared supply
state, not a per-seat ammunition balance.

The original ammo, shield and Life Up probability intervals remain intact; the
extra ammo interval does not replace shields or the Life Up bonus. Scheduled,
bonus and scripted crates use the visible camera bounds. The preserved scripted
core-opening route still guarantees its x10 pack through the shared factory.

## Verification

- `node --check assets/game.js` passes; runtime LF and suite CRLF preserved.
- Full suite: **3,839 passed / 61 failed, exit 1**, final summary reached.
  All 21 new section-308 checks pass; no new failing assertion names versus the
  recorded 61-name baseline. The variable sand-tank assertion failed this run.
- Section 307's upper Life Up boundary now checks that the outcome is not a
  life, allowing the newly requested extra-ammo interval immediately above it.
- Native Chromium: **27 passed / 0 failed**, zero page, console or controlled-loop
  errors. All difficulty/mode combinations exercise the actual level scheduler.
  Real gun input breaks a crate; actual ammo collection releases the queued extra.
  Pause and the real hit/death sequence stop its timer. Boss opening/repeat rates
  and the non-recursive supply behavior are verified.
- Inspected native Draven text, original supply and subsequent bonus-supply pixels.
  Existing ship/box art is retained. No generated asset or atlas changes.

The scripted test calls the same supply factory wired into the retained legacy
core-opening controller. Its retired modular boss art cannot initialize on this
build and was not revived or claimed visually verified. Initial death-probe setup
used a zero countdown and respawned immediately; the final test invokes the real
player-hit path and verifies the active death window instead.

Proof: [qa/supply_audit_0914.json](qa/supply_audit_0914.json). Sources:
`_BUILD_SOURCE/supply_audit_0914/`; native screenshots/logs:
`_shots/supply_audit_0914/`. No commit, push or deletion of user data.

## Next queued asset inspection

The registered SpriteCook ledger currently lists Warden and campaign-map assets,
not a replacement player ship. The active ship's owning source is
`_ART_SOURCES/gravity_mode_v2/canonical_fury_ship_rotations.png`, used by
`_BUILD_SOURCE/build_gravity_mode_v2.py`. Named game-asset and source inventories
have not yet identified a distinct newer SpriteCook concept. SPACE-11 stays
pending; do not substitute the already-shipped ship or the GPT-named component
master and call it the requested new concept.
