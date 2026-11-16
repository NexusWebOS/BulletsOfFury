# Release-readiness QA — November 16, 2026

**Release verdict: HOLD.** The build is materially improved, but a green core suite and protected encounter fixtures are insufficient to certify a finished game. This pass uses original BOF on D:, not BOFII. No commit, push, deployment or public release occurred.

## Confirmed fixes

- Local co-op controller 2 retains its seat when controller 1 disconnects/reconnects; solo first-present mapping retained.
- Online guest full current multi-canvas HUD, native mixer audio, safe room reopening, focus-loss key release and saved controller bindings.
- Standalone Stage 6 boss/miniboss preview warning no longer trapped in ordinary prologue/crew conversation.
- Ending conversation automatic reading holds for all nine pilot routes.
- Current approved orange-vest Juggernaut guitar insert: six preserved whole 512×512 poses, direct 270×270 comic exports, both native art registries corrected and actual drawn pixels independently verified.
- Authored wide Forge/comic canvases preserve their backing-store aspect through legacy fullscreen CSS; native mouse registration and combat HUD restoration verified.

## Current evidence

- Baseline and final core suite: 8,969 passes / 0 errors; no new failing assertion names. Active shipping scripts: 749 parse checks. Engine LF and core test CRLF preserved.
- 730 eligible native ground pilot/weapon/element previews: no emitter/render exceptions, empty emissions or live-state leaks. Selected native pixels inspected. Preview coverage does not prove combat balance or every projectile collision.
- 135 native space previews cover all 9 pilots, all 5 Laser/Fusion/auto-volley tiers, with no empty emissions, exceptions or state leaks.
- 26 desktop/narrow native menu geometry, pointer-registration and combat-restoration checks pass. The wide Forge is no longer squeezed, but small-window text is still too small for a supported mobile release.
- 46 developer encounter starts sampled on Normal 1–5 and Hard/Furious 1–9, with original warnings/native AI and held primary input. Full screenshots and page/console/HTTP inspection retained. These are stationary protected smoke fixtures, not human wins. Original failed rows remain visible; separate follow-up resolves all four Stage 6 preview-entry cases.
- The two protected-fixture deaths are not hidden: Stage 8 traces show a real whole-arm swipe after the intro changes the temporary protection. Stage 5 is not consistently reproduced; no invented fix is claimed.
- Two independent online clients use real Supabase anonymous auth/private rooms, WebRTC, native seat2 input, decoded video and decoded mixer audio (positive remote audio peak). Test rooms close through the native owner. This is not WAN/NAT certification.

| Area | Latest checks | Detailed receipt |
|---|---|---|
| forge | 29 passed / 0 failed | _shots/release_qa_1116/forge/report.json |
| online | 18 passed / 0 failed | _shots/release_qa_1116/online/report.json |
| controls modes | 19 passed / 0 failed | _shots/release_qa_1116/controls-modes/report.json |
| ending | 7 passed / 0 failed | _shots/release_qa_1116/cinema/report.json |
| followup | 13 passed / 0 failed | _shots/release_qa_1116/followup/report.json |
| carrier waves | 4 passed / 0 failed | _shots/release_qa_1116/carriers/campaign-checks.json |
| special pickups | 23 passed / 0 failed | _shots/release_qa_1116/signatures/report.json |

## Strict release gates still open

- No full unassisted Campaign/Arcade wins across all difficulties/pilots/routes. 30-second protected encounter samples do not certify complete multi-form attack books or balance.
- No physical 8BitDo controller attached. Raw-API boot/remap/disconnect tests do not certify wireless/driver modes.
- Online tested on two independent same-machine browser contexts. STUN only; restrictive-NAT/WAN/TURN/reconnect and long-session validation remain.
- All enemy types, both co-op pilots in every live weapon/form combination, all ending/workshop artwork, all attack sounds and sustained performance are not exhaustively certified.
- Legacy native probes have stale fixtures/assertions: normalized Forge tiers, removed automatic opening specials, old HUD/typewriter owners and removed health test switches. Original failed logs retained; current replacements cover stated scopes only.
- Stage 6 native four-wave retry passes 4/4; earlier aborted probe and its renderer exception remain archived. Fresh Edge boot and stepwise fixture isolation pass. Cold-load/performance soak remains a release gate. Fresh native special pickups pass for both tiers/all nine pilots, but all five Rough Rider personal signatures are not freshly certified.
- Wide menus are proportionate on narrow windows but their labels become too small. A separate responsive layout/readability pass is required before claiming phone support.

The shipping page currently references 749 separate JavaScript files. Cold-start/request/decode costs and sustained frame pacing need measured budgets on target hardware. Remaining old runtime graphics paths and baked paired-character scenes also need a deliberate art audit; this pass does not label them all consistent.

Four fresh native-RAF first-form samples (Stages 5, 6, 8, 9; 20 wall-clock seconds each) retained browser errors and frame times. No page/console/HTTP errors occurred. Stage 6 was materially slower here: median 33.3 ms, p95 66.6 ms, p99 83.3 ms. CPU sampling points mainly to `th114Weather` authored tile blits, then native reactor rendering. These software/headless measurements do not certify target-GPU performance. The stationary Stage 8 player death is not a successful fight. Default browser resource-timing buffers cap the separate recorded resource list at 250; that is not the full 749-script inventory. Full logs: `_shots/release_qa_1116/pacing/report.json` and `profile/hot-stacks.json`.

## Test hygiene and reproduction

Temporary evidence is under `_shots/release_qa_1116/`; the review page links raw receipts and actual screenshots. Core before/after hash receipts and original files are under `_ART_SOURCES/release_qa_1116/`. Applied patch recipes are historical; do not run them again against already-patched files. Current probes use the local native HTTP server at 127.0.0.1:8765. Legacy probe failures are retained rather than erased or counted as shipping fixes. Detailed current machine receipt: `docs/qa/release_readiness_1116.json`.

No test-generated leaderboard scores or announcements are submitted. Profiles are isolated browser contexts. Current native game/save/reward/damage/health owners remain intact.


## Strict beta criticism and next sign-off gates

| Priority | Finding | Required evidence before sign-off |
|---|---|---|
| P1 | Whole-mode wins, alternate routes and complete boss phase books are not certified by short checkpoint samples. | Unassisted complete Campaign/Arcade runs, Boss Rush/Time Attack outcomes, achievement/reward/save verification and both-player failures/revivals. Include Easy/Insanity where earned and available. |
| P1 | Online co-op uses STUN without TURN and was tested on one machine. | Two actual machines on separate networks, restrictive NAT, latency/loss, disconnect/rejoin and long sessions. |
| P1 | One carrier probe hit an initialization exception; subsequent boot/isolation/retry checks passed. The page loads 749 script files. | Repeated cold boots and a sustained target-hardware soak with browser logs, frame-time budgets and memory/request/decode measurements. No production fix is claimed for the unreproduced exception. |
| P1 for competitive release | Public leaderboard results are submitted by the client. | Define trusted submission/anti-cheat requirements and verify authoritative validation before advertising competitive integrity. No forged QA scores were submitted. |
| P2 | Wide layouts preserve proportions but are too small in narrow windows. | A dedicated readable layout and full interaction check before claiming phone support. |
| P2 | The complete art/effect/audio inventory has not received a final visual/auditory audit. | All paired workshop scenes, character identities, attack warnings, hit reactions and attack sounds reviewed in actual play. |

These are observed limitations or missing certification evidence, not a claim that every listed system is broken. The known original legacy-probe failures remain in the machine receipt with their replacement coverage described separately.
