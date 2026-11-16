# Bullets of Fury — overnight cinematic and rendering QA

Original BOF source: `D:/BOF-Downloads/2026-11-14/RevG-source`. November16,2026. **Release remains HOLD.** Confirmed faults below are repaired; this is not a claim that every mode, achievement, difficulty and device is release-certified. No commit/push/deployment/public scores.

## Applied corrections

| Owner | Result |
|---|---|
| `assets/night_cinema_1116.js` | Complete-text reading holds; post1 ship-system replies preserve lost squad comms; obsolete power-cell request removed; ordinary scenes and Stage8 possession wait for actual required art; loading spends no campaign time/distance; friendly speakers keep the standard metal frame. |
| `assets/night_hq_art_1116.js` | Four conference poses now use approved row-B orange-vest Juggernaut. Master/comic registries share the correction; editable source retained. |
| `assets/night_city_atlas_1116.js` | Transparent padding repairs20 thruster rectangles; one wholly empty beam end frame now references valid transparent pixels. Native before/after pixels are identical. |
| `assets/night_weather_1116.js` | Skips off-canvas authored weather only.48 pixel comparisons+5 special-context fallbacks are identical; representative33 bitmap submissions become15–16. No weather art, clocks, resolution or combat changes. |
| `assets/night_missile_stats_1116.js` | Boss/miniboss/component missile damage receives the missing hit credit. Real missile damage stays34; tally0→1. New observer credits deduplicate per actual missile/encounter and preserve existing native credits. AI/wing flags and space primary volleys are excluded. |
| `_BUILD_SOURCE/serve_nocache_1017.py` | Same-origin local server keeps no-cache headers with a larger accept queue and bounded idle connections after actual refused script requests. Small cold-boot samples do not prove the original refusal's root cause. |

## Current evidence

The [review board](../_shots/cinema_overnight_1116/review.html) contains27 full clips, nine gameplay contact boards and correction screenshots. It selects one seekable film at a time. Main machine receipt: [cinema_overnight_1116.json](qa/cinema_overnight_1116.json). Reproduction recipes are in `_BUILD_SOURCE`; editable art/manifests/backups in `_ART_SOURCES/cinema_overnight_1116`.

| Scope | Result | Practical limit |
|---|---|---|
| Core/syntax |8,969 assertions/0 failures;754 external+5 inline scripts parse; unchanged failure-name list | Core assertions do not prove pixels or balance. Engine LF/tests CRLF and old production source hashes retained. |
| Story inventory |6,804 pilot/co-op-pair/difficulty/route cases; no listed issues after repair | Metadata, not playthroughs. |
| Native director |126 runs/1,008 shot visits;139 checks pass | Prepared scenes, automatic traversal+native pause/reveal/next/skip/callbacks. |
| Actual story drawing |224 renders/13,457 bitmap draws; no invalid source/state/smoothing issues | Cole/Hard checkpoint composition pass. Additional all-pilot native arrivals/openings/endings tested separately. |
| Atlas metadata |80,918 source rectangles across265 registries, zero out-of-bounds candidates | Includes retained legacy registries; not every custom renderer format. |
| Entry/control checks |18 fresh arrivals; Easy/Normal homecoming21 checks; opening11; city11; kit53+16; loading5; Stage8 loading9+controls7 | Prepared native checkpoints. No earned campaign-clear claim. |
| Encounter starts |Normal1–5/Hard1–9:28 cases/140 checks | First60 simulated seconds, protected stationary no-fire fixtures. |
| Ordinary waves |12 fixtures/54 checks; all9 stages, Stage4 all3 difficulties, Stage8 Hard/Furious |90 simulated seconds each with protected primary-fire input. No kill-call coordinate jumps; fixed viewport. Kill records count calls, not distinct enemies. |
| Furious full fights |All9 bosses+all9 minibosses reached native defeat | Real input-only protected bots with native GOD; no enemy HP/phase/timer writes. Not human balance or campaign wins. Default loadouts/pickups vary; do not rank difficulty by clear time. |
| Same-tab replay |18 repeated starts completed without timeout/error | Yields every6 frames. Original30-frame-batch stall not reproduced; root cause unproven. Original partial receipt retained. |
| Missile accounting |Physical A/B identical34 damage, hits0→1; seven controlled fixtures/35 core checks; spaceVolley exclusion; module-finisher/wreck checks | Controlled damage calls are not physical-impact/fight wins. Live AI missile unavailable in the15-second window. Source excludes ally/wing flags; full automatic/co-op accuracy denominators remain uncertified. |
| Fresh Normal campaign |273.22s opening→map→comic→combat→deaths→Continue, no runtime errors | Limited input bot lost before beating Razorback; no GOD/HP/lives/timer/phase edits. **Not a successful clear or human balance proof.** |

Current recordings include service-link/volcanic rumble/lift-off, Stage3 arrival/HQ/workshop, Stage4 prototypes/code-only satellite, full native kit assembly, Chronos death/return and HQ welcome/radar/evacuation/defense. These prepared clips omit intervening result/equipment/map menus. Combat films precede the final statistics-only repair; its final real-impact and component receipts are separate.

## Failures and limits kept visible

- Original missing-art and spent-campaign-clock failures remain linked beside passing retries. Obsolete direct-HP probes and mistaken God/co-op fixture assumptions were not erased or called gameplay repairs.
- First real-impact A/B had correct damage/tally data but a resourceHTTP429, so it failed the error check. The original host was not captured. A fresh shipping boot had no HTTP failures. Isolated A/B with optional online configuration disabled only in its browser contexts passes. Shipping `online.js` is unchanged; do not call a rate-limit cause fixed.
- The first component fixture accidentally selected an ordinary space container while Chronos was protected; final selection filters actual encounter ownership. Old failed logs remain. The slower per-tile-transform weather prototype was rejected; the cached-transform version shipped.
-268 raw legacy registrations (134 unique keys) still name absent loose files; current owners/atlases supersede many. They are audit candidates, not268 proven live missing sprites. Five archived627x627 finale banks also remain. Do not restore retired art or redirect these blindly.
- Prior release report's older co-op/signature probes retain their10/18 failures against superseded assumptions. Current scoped tests do not erase those historical results.

## Remaining release gates

1. Human unassisted all-mode/difficulty/character runs, full death/continue/save/achievement routes, weapon combinations and actual balance assessment. Protected bot clears cannot settle this.
2. Real8BitDo Genesis pad cold-start/reconnect and two-controller hardware. Native synthetic-binding/seat tests already pass; hardware/driver behavior remains open.
3. Separate-machine internet co-op under latency/loss/reconnect with guest audio and focus transitions. Prior two-context same-machine WebRTC proof is narrower.
4. Target-hardware performance, particularly Stage6. Culling is pixel-identical and reduces submissions; headless microbenchmarks do not certify60FPS. Narrow-window menu readability and distributable packaging also remain open.
5. Creative review of the small post7 portal composition, angled Photon bench presentation and epilogue location continuity; legacy renderer/registration retirement. Existing approved art was not rewritten on assumption.

See [CINEMA_OVERNIGHT_1116.md](CINEMA_OVERNIGHT_1116.md) for checkpoints, raw fixture distinctions and source ownership. Keep the game server on8765 and media server on8766 for Mike's morning review.
