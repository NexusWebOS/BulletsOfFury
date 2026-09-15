# Arcade route audit — September 15, 2026

Fetched and inspected `origin/main`, then fast-forwarded this checkout from
`ee4e87c4` to Mike's requested `7635330b`. The incoming update already includes
pilot-select reveal, boss timers and the first Chrome Hammer fight. Its checklist
records 148 requests: 79 complete, 8 partial and 61 pending.

The next available code item is MODE-01. SpriteCook production items remain
queued: this session has no SpriteCook connector, and its browser is signed out.
The unresolved Stage 2 boss-identity dependency is unchanged.

## Changes

- Arcade results advance directly to the next stage card, without the outbound
  cinematic or campaign map. Score awards and remaining lives, ammunition and
  continues pass through the existing results handler.
- Stage 8 uses its ordinary card/launch in Arcade. A pending campaign rift
  entrance cannot redirect Arcade or be consumed by that run. Campaign retains
  its rift entrance.
- The earned Stage 5 secret gate enters Stage 9 directly. Clearing the bonus
  encounter returns to the saved Stage 5 clock, scroll, spawn clock and wave
  index. Direct/password Stage 9 has no saved level and uses the existing Stage 6
  fallback. Campaign keeps its map route.
- New runs clear stale detour/arrival state. The bonus route cannot reuse a
  return point from an earlier run.
- Arcade suppresses scripted radio exchanges and uses the existing final-score
  card instead of waiting for the pilot-ending cinematic.
- Stage cards, actual encounters, boss defeat sequences, the secret gate effect
  and the Stage 5 ship-transformation launch remain in place.

## Verification

Real Chromium uses the existing `shoot.py` controlled-frame workflow and the
game's own renderer. The probe presses real Enter input after the results panel
lands, tests all seven ordinary inter-stage results paths, exercises earned and
password bonus entry/return, compares the campaign routes, and confirms the final
card returns to title. **20 checks pass**, with zero page, console or controlled
loop errors. Stage 2/5/8 card pixels and the final-score card were inspected.

The initial probe pressed Enter during the panel's intentional 0.18-second
input-blocking entrance. Correcting that fixture timing made the same route
checks pass; no game timing was changed to satisfy the fixture.

The obsolete suite check requiring Arcade's outbound cinematic is replaced by a
behavior check that calls the real results handler and verifies score payment
and next-stage dispatch. The renderer is covered separately by Chromium.

Syntax passes. Full suite: **3,850 passed / 58 failed, exit 1**, final summary reached; no new failing assertion names against the incoming update. The suite is still not clean. Details are recorded in [qa/arcade_routes_0915.json](qa/arcade_routes_0915.json).
Probe source: `_BUILD_SOURCE/arcade_routes_0915/`. Local logs and inspected pixels:
`_shots/arcade_routes_0915/`. Runtime LF and suite CRLF are preserved.

## Remaining MODE-01 work

MODE-01 stays **partial**. These are boundary probes, not a complete natural-play
campaign/Arcade comparison. Remaining audit areas include embedded boss escape
presentation (especially Stage 7), shared campaign-progress mutations, full
encounter parity and co-op-specific routes. The underlying stage tuning and
later-stage cleanup requests remain separately tracked.

The tally remains **79 complete / 8 partial / 61 pending**. Incoming GitHub work
is installed; this continuation's changes are local and have not been committed
or pushed.
