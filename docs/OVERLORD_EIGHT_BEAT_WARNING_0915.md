# Jungle Overlord-X eight-beat pass warning — 2026-09-15

## Result

Every Overlord-X vertical charge now owns a fixed 1.60-second warning:

1. Eight existing Retina beeps fire in order at 0.20-second intervals.
2. The authored warning cone and overhead alert flash red on every beep while retaining the shared green acquisition and yellow commitment between beats.
3. The helicopter follows the player's horizontal position during the first half, then locks one lane and cannot chase a late dodge.
4. The boss remains vulnerable for the entire warning, giving the player a clear shooting window.
5. The eighth beat releases the fast vertical charge directly along the warned lane. The below-half-health four-pass frenzy reuses the complete sequence before each southbound or northbound crossing.

The dedicated beat scheduler suppresses the shared one-shot alert for this attack, so the eight-beat pattern has no ninth or overlapping alarm. Other attacks using the shared warning system keep their existing audio behavior.

## Verification

- `node --check assets/game.js` passes; `assets/game.js` remains LF-only and `_BUILD_SOURCE/test_fl.js` remains CRLF-only.
- Focused suite section 313: **10/10** assertions pass for start state, exact beat count/order, cadence, red synchronization, halfway lock, shooting window, committed release and absence of an extra alert.
- Full suite: **4,042 passing / 57 failing**, exit 1. Every failure name matches the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium warning probe: **14/14**, zero page or console errors. Five native frames cover beats one, four, six, eight and the charge release.
- Shared warning regression probe: **12/12**, zero page, console or controlled-loop errors across green, yellow, red and release.
- Browser evidence: `docs/qa/overlord_eight_beat_warning_0915.json` and `docs/qa/shared_nonlaser_warning_0915.json`.
- Screenshots: `_shots/overlord_eight_beat_warning_0915/overlord_warning_beep_1.png`, `overlord_warning_beep_4.png`, `overlord_warning_beep_6_locked.png`, `overlord_warning_beep_8_committed.png`, and `overlord_warning_release.png`.
