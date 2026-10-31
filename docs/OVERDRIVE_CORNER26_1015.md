# Overdrive Corner26 — Genesis HUD, 2026-10-15

Build `overdrive1015-corner26-r1`, stages3 and7. Replaces the full-width
top/bottom player HUD with Mike's specified three-part arrangement:

- Top left: current pilot's existing face (Yuri when playing Yuri), `X` and
  current lives, a generated rectangular health track and segmented fill.
- Top right: `AMMO = value`, including infinity for the unlimited rifle;
  underneath, the actual current action (cover, firing, prone/crawl, roll,
  blindfire, free aim, jump, grenade, down/recovery and other applicable states).
- Top center: Score and High Score with live numeric values. High Score saves
  to the expansion-only `bof_od_onfoot_high_score` key and survives reloads.

Five PixelLab-generated components:56x56 portrait frame,144x24 health track,
128x14 green/red fill plates and128x48 ammo bracket. Source512x288 atlas is
retained with the prompt, job ID and hashes under `art/corner26/source`.
The gray/blue bevels, lime/red segmented bars and hard pixel edges use a
restricted Genesis-style palette. Blank centers are9-sliced; portrait and fills
are padded without nonuniform rescaling. Runtime text uses the game's existing
arcade font. Existing pilot portrait is cropped/composited locally, not uploaded.
Normal HP clips the green generated fill proportionally;30% or less selects red.
The HUD has no full-width backing and no bottom strip.

Existing boss bars and portrait conversations remain. Boss bar moved down20px
to clear the player health gauge; targeting alerts and stage7 boss messages move
accordingly. Boss damage, shield, animation, music and controls are unchanged.
No new enemy/background assets and no assets/game.js modification.

Owner `_research/build_corner26.py` rebuilds the manifests/components from the
retained source. Runtime `js/corner_hud26.js`, hook `js/ground20_encounter.js`;
`js/prism_bastion_1013.js` only adjusts boss message placement. `index.html`
registers the pack and new build stamp. PixelLab cost25included generations;
1763 remained afterward. No cash credits or original-art uploads.

27/27 native Chromium checks passed. Real keyboard actions verify finite ammo,
prone/crawl, roll-to-prone, free aim, blindfire, stage3 jump and grenade labels.
Health full/half/empty plus real stage7 damage, lives binding, score progression,
saved high-score reload, old-panel removal, boss spacing and conversation frame
checked. Screenshots inspected at actual game rendering scale. Zero page,
console/shader or asset errors. All820 prior PNG hashes match. Base regression
completed BUILD OK /0ERRORS /exit0, JS syntax checks passed. No physical controller
test or full campaign playthrough is claimed for this focused HUD revision.

Evidence: `docs/qa/overdrive_corner26_1015.json`, `docs/qa/corner26_views`.
Probe: `_research/probe_corner26.py`. Local preview port8781.
Local changes only; no commit/push. Preserve all other local work.
