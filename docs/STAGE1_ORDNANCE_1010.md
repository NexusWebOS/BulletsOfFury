# Furious Level 1 ordnance — October 10, 2026

Mike requested faster, shootable Furious miniboss missiles and unshootable
Furious boss sonic waves.

The Furious Razorback's regular rack missiles launch at 4.2 game pixels per
frame (previously 2.424384); its committed rapid salvo launches at 5.2
(previously 3.485052). These are the constructor speeds before the existing
difficulty multiplier. Restoring missile eligibility also restores their
original acceleration and enemy Retina steering. Rapid-salvo missiles retain
their fixed, committed launch lane. The fourteen-missile sequence and warnings
remain unchanged. Missiles have one-hit interception; miniboss sonic rounds
stay weapon-proof. Other Razorback difficulties retain their preceding behavior.

The Overlord's broad sonic front and three narrow waves explicitly forbid
interception. They survive player gunfire, missiles, beams, sonic shots and
orbs. Juggernaut's wrecking balls also leave these waves intact while retaining
their normal gunfire defense. The wave still damages the player and travels
onward. The boss's accompanying missile volleys remain shootable.

Owners: the existing `rzbMissile`, `ovSonicWave` and `wreckTick` functions in
`assets/game.js`, and the corrected Razorback rule in `assets/feedback_1009.js`.
No additional runtime layer or generated art is required.

Verification: `node --check assets/game.js`, `node --check
assets/feedback_1009.js` and the full `node _BUILD_SOURCE/test_fl.js` suite:
8,256 passing assertions, no failures, final success banner, exit 0. This
retains the preceding 8,243 assertions and adds thirteen contract checks.
Game source remains LF; the suite entry file remains CRLF.

Real Chromium: `_BUILD_SOURCE/probe_stage1_ordnance_1010.py` uses the existing
`shoot.py` server/manual clock and balance fixture. All 33 checks pass with
zero page, console or asset errors. Actual missile positions and velocity,
Retina launch, weapon interceptions, wave survival, real player damage, and
the active wrecking-ball positive control are measured. Native screenshots of
the rack, missile destruction, sonic warning and wave were inspected. Portable
results: [QA record](qa/stage1_ordnance_1010.json). Reproducible full log and
screenshots are under the ignored `_shots/stage1_ordnance_1010/` directory.

One cancelled HTTP media request appeared during browser shutdown; this was
a local server connection cancellation, not a page, console or asset failure.
These protected attack fixtures verify collision and rendering; they do not
establish an unassisted Furious clear or human balance approval. The historical
October 9 probe's blanket "no Razorback round" expectation is superseded for
Furious missiles by this probe.

Local changes only. Existing staged, unstaged and untracked work is preserved;
no commit or push was requested for this correction.
