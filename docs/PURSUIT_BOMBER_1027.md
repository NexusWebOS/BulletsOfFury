# Stage 6 Eclipse pursuit bomber — October27

The two inner launch pods are now bomb racks. Engines retain their native propulsion flames and never launch attacks. This change applies only to the Stage 6 Earth Siege Bomber; space bombers and other encounters keep their existing owners.

## Encounter loop

The bomber weaves laterally and bobs vertically while alternating warned ground drops from living racks. It spools, accelerates fully beyond the north edge, and stays ahead until the player closes the gap. Forward player movement catches it substantially sooner; a3.7-second cap prevents a stationary player from softlocking the encounter. It returns into a committed hull warning away from the player, notices the pursuer, then drops bombs and fans physical ground missiles from its live bays. A shifting committed opening remains in each fan. Recovery returns it to pursuit.

Weave lasts 6.2/5.8/5.2/4.8seconds on Easy/Normal/Hard/Furious. Return takes 1.3seconds. The first barrage warning is 1.65/1.4/1.25/1.15seconds, followed by 4/5/6/7 waves. Subsequent wave gaps are .88/.76/.67/.59seconds. Ground impacts retain their own longer warning and travel time. Maximum owned projectile population 128; simultaneous warned ground bombs 14. Two brief ally radio lines correspond to actual boost and barrage beats.

Destroyed launch pods cancel unreleased drops, stop their missiles and retain native white hit flash/breakup. Surviving engines slow lateral/forward movement when destroyed. A center bay remains available after both racks break while the body lives. The fully offscreen bomber cannot be damaged or Retina-targeted; it returns visibly before vulnerability resumes. All original module/core HP, death, rewards and stage progression remain native.

Physical missiles may be intercepted; explosive fragments are ordinary unshootable bullets. The single interception policy is used immediately, before their first update. Native impact reticles, FOV colors, shared mixer/retrigger cues and native defensive clears remain owners.

## Runtime and art ownership

- assets/pursuit_bomber_1027.js owns Stage 6 pursuit/choreography, launch sockets, eligibility and fixed-cell draw routing.
- assets/pursuit_bomber_art_1027.js registers loose atlas cells; index.html loads both after the current HUD owner.
- assets/game/levels/stage_06/miniboss/pursuit_1027 contains fixed even cells: 48x104 launch pod and white-hit banks, 16-phase 64x64 falling bomb, 4 cycles x 64 headings for 64x64 missiles and 32x32 fragments.
- _ART_SOURCES/pursuit_bomber_1027 preserves PNGs, manifest, Aseprite source and reproducible build_art.py. Set ASEPRITE_EXE to export the editor source; runtime PNGs rebuild without it. The builder finds the repository from its own path. Existing BOF bomber and Stage4 ordnance art are the only inputs; no paid generation or original-atlas edits.
- _BUILD_SOURCE/probe_pursuit_bomber_1027.py runs the native browser regression fixtures; --out selects the evidence folder. Fixtures deliberately force states and damage to test invariants; they are separate from the live recording.

## Verification and limits

47 native Chromium checks pass across all four difficulties, including complete loops, emission sockets, damage protection, player-distance pursuit, pause clocks, rack break cancellation, actual white damaged pixels, projectile interception, full native modular exhaustion/exit and space-bomber exclusion. Actual native screenshots and decoded film frames were inspected. No final page, console or HTTP errors occurred in the deterministic probe.

The 77.76-second native Furious film reaches normal defeat at 71.665seconds after four throttle runs. Cole uses an input-only invulnerable observer with normal allies, initial level 5 Laser/40 missiles and native pickups. The initial 35 seconds withhold player fire to show the full pattern. No enemy HP, phase, position or timer is written during capture. The observer takes 27 prevented hits, so this is behavior/animation evidence, not proof of human difficulty. Native rendering averaged 42.16fps during capture; the MP4 is encoded at 30fps. Decoded audio is audible at -18.9dB mean/-2.9dB peak. No game, bot, asset HTTP or console errors; nine unrelated background preloads were aborted during navigation/closure. Film and source hashes are retained with the evidence.

Syntax checks pass. The required full test suite still reaches its summary with the same five pre-existing failures: single-hit flash duration, two Chronos opening-jump expectations and two StageX right-branch expectations. These were not altered. See docs/qa/pursuit_bomber_1027.json. No commit or push.

The portable art rebuild reproduces all five runtime PNGs and the registry byte-for-byte. Nine Chromium video playback/seek/source-hash checks pass. Current film review: http://127.0.0.1:56142/index.html.
