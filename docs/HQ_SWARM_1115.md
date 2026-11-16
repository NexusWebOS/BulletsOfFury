# November15: rapid HQ evacuation, stealth missiles and somersault escape

Original BOF, D:/BOF-Downloads/2026-11-14/RevG-source. Mike requested faster departures and attackers, faster Decker/Axel kills, a reinforcement swarm with stealth missiles, then actual somersaults and boosts to warn the team. Supersedes the1.3s/six-kill timing in HQ_TURNS_1115.md.

All9 departures now take0.75s each, separated by0.9s, alternating southwest/southeast with a0.15s gap. The first seven leave within a7.5s beat; both guards leave later. Existing20-cell banking/exhaust banks, actual pilot identities and B42 remain. The5s quiet base pause remains.

Enemy approach0.32s, reinforcement interval0.24s, bounded32 total. Every third attacker is an actual native AF21 stealth fighter. Wing-pod missiles use native missile/muzzle/airburst frames and the shared enemyMissile cue. Rendered missiles accelerate toward HQ; fired missiles continue, but dead launchers stop emitting. This is cinematic ordnance and never inserts real gameplay bullets or damage.

Decker/Axel fire from their rotating noses and alternate ten visible takedowns at0.25s intervals, finishing by3.9 guard seconds. Targets flash white before fixed-position native explosions. Reinforcements grow to22 survivors with up to9 concurrent visible missiles in the native probe. The guards realize they must warn the others, then Decker flips at7.1s/boosts at7.6s and Axel flips at8.0s/boosts at8.5s. Each flip uses eight fixed256 cells from that actual aircraft's native somersault bank, not flat-plane rotation. First/last poses match the existing banked exit cell exactly. Somersault and boost cues use the shared mixer. Final escape fades into the native Stage6 opening.

Native Chronos death, frozen settled Earth/starfield,16 physical door frames, all9 walk/cheer banks,16-frame radar and one460x84 metal portrait box remain. Normal/Easy retain their original completion owner; Hard/Furious continue to Stage6. No combat, rewards, global flight controls, game.js or tests changed.

Verification:31/31 focused native checks,26/26 lifecycle checks and27/27 movie/browser checks. Native page/console/HTTP errors:0. Shared somersault, missile and boost sounds decode audibly; two somersault and11+ boost cues dispatch. Both new pages and registry reproduce byte-for-byte, with fixed even cells/pivots and exact exit endpoints. Full suite8,969 passed,0 failures,exit0; failing-name list remains empty. game.js LF and test_fl.js CRLF unchanged.

Updated HQ film:43.40s, H264/AAC1824x1024,30fps; native audio, full decode passes. Focused Cole/Hard checkpoint from evacuation through Stage6's first interception; earlier homecoming omitted. Not a campaign win. Separate Stage6-7 film66.70s captures the current Harrier aftermath and native entry without dialogue skips; see STAGE67_CINEMATICS_1115.md for the observed post-countdown display limitation.

Runtime owner: assets/hq_return_attack_1114.js. Registry: assets/hq_swarm_art_1115.js, loaded before owner in index.html. Sources/provenance: _ART_SOURCES/hq_swarm_1115. Repack: _BUILD_SOURCE/hq_swarm_1115_pack_saved.py. Probe/lifecycle/record/package/verify_movie scripts share that prefix. Evidence: docs/qa/hq_swarm_1115.json and _shots/hq_swarm_1115. No SpriteCook, generation, commit, push, installer or release in this pass.

Review: http://127.0.0.1:8766/_shots/hq_swarm_1115/review.html
