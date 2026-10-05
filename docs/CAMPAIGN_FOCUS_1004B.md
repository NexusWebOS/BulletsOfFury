# Stage 6 and Stage 8 follow-up — October 4

Mike's follow-up recording: `C:/Users/Mdogg/Videos/2026-10-04 10-46-40.mp4`.
Music source: `C:/Users/Mdogg/Desktop/finalform.wav`.
Local review: `_shots/campaign_focus_1004b/review.html`.

## Changes

- **Five versus five:** the old route-choice code was sending every other ally away after the newer roster had already reduced the team to five total ships. Removed that second split. All nine pilot choices retain four distinct allies, including during Gang Mode and after Decker's rescue. Navigation uses the actual roster length instead of eight slots.
- **Rebel pressure:** Furious supports two staggered personal attacks at once, with Fusion and roller attacks kept apart. Both stealth pilots now fire repeated ambush volleys. All five personal weapons still operate, and Gang Mode retains the missile, turbo, cloak and helper upgrades. Whole hulls and shield removal are preserved.
- **Defeat HUD:** only living Rebel pilots draw their individual health bars. A dying ship and its final portrait transmission can remain visible without a stale health bar.
- **Stage X:** completing the Stage 6 Harrier route sends the five Rebels to the central city; completing the Rebel route sends the escaped Harrier there. Authored ships visibly travel to the hub. The pending encounter survives save/load, launches from the map with the full wing and returns to the campaign map after victory. Existing `XHARR` and `XREBEL` practice passwords remain valid. Older saves without the new route record retain their historical Stage X data; no past route is guessed or overwritten.
- **Stage 7 → 8:** the live Warden exit now goes directly into Stage 8's in-engine portal arrival, bypassing the intervening results screen, briefing and campaign map. Results, rank, score, achievements and Furious conversion are still recorded; equipment and lives carry through. The existing arrival dialogue plays over the live world and then returns control. This implements the direct-portal reading of Mike's instruction.
- **Rewards:** Stage 6 now grants Prism; Stage 8 grants Dark Matter. Previously earned inventory is not removed.
- **Finale structure:** normal drone arrival/mutation → mutated drone → ghost → Dracula remains intact. Only Dracula borrows the eight forms, whose existing persistent health and module pools remain separate. The single refilling gauge and actual active-form health remain in use.
- **Dracula:** the existing large body now has independently articulated sweeping hands, an inward crush, flanking projectiles and a bounded orbital pull. The three attacks precede a transformation. Hand warnings follow the actual articulated path; sustained fire uses brief hit accents so it no longer whites out the entire character continuously.
- **Knight:** twelve newly generated components provide crouch, airborne, impact and recovery poses. Neck, shoulder, hip and hand sockets were measured on the imported pixels. The approved head-only art, separate arms, sword, shield and power effects remain. Hammer's actual controller drives the attacks. The thrown sword renders at its damaging position and returns to the hand; destroying it cancels the projectile. Heavy gun, spell pillars, charged ground spikes and beam effects now render alongside their source attacks. Compact rolling and orbital-jump poses retain the modular body.

## Music

| Fight | Runtime file | Recording |
|---|---|---|
| Mutated drone | `assets/game/music/Level8b.mp3` | Previous second-fight track, originally `unused3 - stage8b-p3.mp3` |
| Ghost | `assets/game/music/Level8b2.mp3` | Previous third-fight track, The Final Confrontation |
| Dracula and transformations | `assets/game/music/Level8b3.mp3` | New `finalform.wav` |

The new recording is 131.44 seconds, converted to 256 kbps MP3 without trimming, gain, speed or pitch changes. All three files decode fully. Actual encounter transitions were checked for `boss8`, `boss8p2`, `boss8p3` in that order. The old first track remains preserved as `Unused_FinalBossDrone.mp3`. Herald retains its existing shared `Level8b.mp3` assignment.

## Recording and reference review

The new recording is 15:15.77 and contains Stage 7 and Stage 8. Its entire timeline was inspected at two-second intervals across 20 contact sheets. This is sampled visual inspection, not every video frame or a complete audio review. The prior hour-long recording's Stage 6 audit is recorded in `docs/GAMEPLAY_AUDIT_1004.md`.

- 00:00: the Forge already lists Dark Matter before Stage 7, consistent with the incorrect Stage 6 reward.
- Around 04:56–05:14: results/menu/map/briefing interrupt the portal continuation.
- Around 07:04: mutated-drone encounter; around 07:38: ghost; around 08:16: Dracula.
- Around 08:38–13:36: borrowed forms cycle; sustained full-body white flashes obscure the boss, and poses do not communicate the donor's attacks clearly.
- Around 13:38 onward: ending sequence.

The supplied [Dracula reference](https://www.youtube.com/watch?v=KfsBXXuSD_w&t=159s) was inspected in the browser from the requested fight segment. The large central body and independently moving hands informed the existing alien rig's new motion. No reference video or art was downloaded into the game.

## Assets and ownership

- Runtime: `assets/campaign_focus_1004b.js`, loaded after `finale_donors_1004.js`.
- Narrow edits: route choice and element table in `assets/game.js`; Rebel scheduling/HUD in `assets/rebel_gang_1004.js`; donor bounds in `assets/finale_donors_1004.js`; fallback exit in `assets/stage67_review_0929.js`.
- Generated source: `_ART_SOURCES/campaign_focus_1004b/knight_poses.png` with provenance and hashes. Original source pixels preserved.
- Importer: `_BUILD_SOURCE/build_focus_1004b.py`. Component alpha bounds exclude isolated generation dust and neighboring-row fragments. Measured metadata: `assets/game/campaign_focus_1004b/manifest.json`.
- No shared atlas edits. `ART_TAXONOMY.json` registers the `cf4_` family. Music provenance is in `_ART_SOURCES/campaign_focus_1004b/music.json`.

## Verification

- `node --check assets/game.js`, the new module and modified donor/Rebel modules: exit 0.
- `node _BUILD_SOURCE/test_fl.js`: **7,053 passing assertions; final summary `FALVA/LIZZIE BUILD OK, 0 ERRORS`; exit 0**. Previous baseline: 7,038. The first run exited 1 for two old Prism/Dark Matter expectations; those expectations were updated to Mike's explicit new reward order. No assertions were removed.
- Three native Chromium probes: **37 checks pass, zero page/console errors**. These cover nine pilot route choices, complete teams after rescue, personal attack releases, Gang Mode, dead-pilot HUD, both Stage X routes and persistence, the Warden's natural death state through `updatePlay`, full portal arrival, Dracula's three patterns, generated knight poses, extended native attacks, thrown/disarmed sword, audio transitions and all eight practice shortcuts.
- Screenshots were inspected for actual component alignment, warning graphics, attack effects and map/portal transitions. Early probe fixtures needed the Warden's `dead` mode and the full 15-second existing arrival duration; final checks use those real conditions.
- Review practice frames suppress storage writes; all eight buttons were checked against a preserved storage marker.

Evidence: `docs/qa/campaign_focus_1004b.json`. Reproduction probes: `_BUILD_SOURCE/probe_campaign_focus_1004b.py`, `probe_focus_combat_1004b.py`, `probe_focus_review_1004b.py`.

These are controlled encounter and rendering checks, not a complete human campaign clear or a final difficulty verdict. Existing staged, unstaged and untracked work is preserved. No commit or push.
