# Campaign map: closer approaches and readable flags

Mike: the map still stayed too far away when approaching or selecting a level,
and the flag was difficult to read. Bring the ship, flag and floating level closer.

The previous follow camera capped zoom at 0.62. Independently, flags cancelled
camera zoom and stayed 28 logical pixels tall; the actual pilot hull stayed 40.
Changing the camera alone therefore could not enlarge the Roman numeral.

## Change

- `assets/campaign_follow_1009.js` now holds ordinary selected levels at
  1.077-1.10 zoom, approximately 74-77% more magnification. Approach zoom settles
  faster. Bounded look-ahead and responsive smooth tracking keep the jet visible
  during horizontal and vertical flights at the closer distance.
- Shared detail sizing raises the selected flag from 28 to 56 logical pixels
  and the actual pilot hull from 40 to 52. Their existing authored pixels and
  proportions remain unchanged, with image smoothing disabled. The larger flag
  puts its numeral above the ship instead of letting the hull hide the cloth.
- `assets/campaign_landscape_1004e.js` uses that size for the live selected flag;
  `assets/audio_feedback_1010.js` uses it in the final live ship renderer.
- Selected VI/VII return to the close view after the rebel departure cinematic.
  Earned IX also gets the close view. Stage X encounter framing, boot, rift
  cinematics and the menu overview retain their own camera behavior. Existing
  navigation, locked-stage rules, ranks and unlock timing remain authoritative.

No new art or atlas edits. No game.js or assertion-harness edits. Three existing
loader URLs use cache revision `campaign-close-1017`; other index bytes remain.

## Review and verification

`docs/previews/campaign_close_1017/index.html` runs the actual game in an iframe,
with level selection, an HQ approach replay and the normal map overview. Its
storage namespace is isolated before game boot, including `clear()`, so review
save actions do not alter real campaign slots.

`python _BUILD_SOURCE/probe_campaign_close_1017.py` exercises all nine levels,
actual flag/hull draw sizes and smoothing, travel, the menu overview, rebel and
Stage X behavior, post-clear unlocks and a compact viewport. `--review-only`
checks the live review controls and save isolation. Actual Chromium screenshots
are inspected; keys are observed through XART and the game's own drawImage.

Final measurements and assertions: `docs/qa/campaign_close_1017.json`. Ignored
before/after captures and logs: `_shots/campaign_close_1017/`.

Native camera/render checks: 57/57. Review and save-isolation checks: 7/7.
The existing map boot/unlock regression also passed 7/7. No browser errors.

Required full suite reached `FALVA/LIZZIE BUILD OK`: 8,754 passing assertions,
0 errors, exit 0. Node syntax checks passed for the three changed owners and
game.js. Core, harness and separate local gameplay hashes remain unchanged.
No commit or push performed by this pass.
