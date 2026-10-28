# Dracodia — Neural Archon

Replaces only Dracodia's Stage8 transformation slot6. The standalone Harrier
encounter remains. The other copies remain Hammer, helicopter and volcano.

PixelLab references Dracodia's actual current black/chrome/violet demon sprite.
New whole brain has three crown spikes, chrome brow, red evil eyes and violet
lobes/circuit animation. Generated tendril/lobe frames preserve an offline locked
brow/eye rectangle for fixed emitters. The native brain floats in both axes.

Three attacks cycle:

- Two eye lasers commit to vertical lanes after green/yellow/red warnings.
  Six authored widths expand8/16/26/38/52/64px;2 generated flicker poses each.
  Actual visible beam-alpha pixels, plus the player's4px contact allowance,
  determine hits. No moving aim after the warning.
- Code geysers commit3/4/5 distinct spots on Normal/Hard/Furious. Each has a
  warning column, staggered release, violet erupting plume/debris and recovery.
  The current visible plume pixels determine damage inside the core footprint.
- Cloud Aegis circulates generated opaque dark violet smoke around the brain.
  Its finite shield is12% of this form's maxHP, lasts2.35s after charge, can
  break early, and expires into an unshielded recovery. Body HP stays intact
  while shield HP absorbs a hit. No shield HP carries into another form.

Body has one core/Retina target and authored white hit poses. Hit flashes expire
through native clocks. HP/damage save into the original slot6 budget; changing
forms preserves damage. Zero health enters native copy-death; all other forms
and the single final death, portal, reunion and reward remain native owners.

New exports:71 fixed even cells,18 lossless WebP sheets, body384x384/unit1.5
from256px source/pivot192,192. Measured eyes158,228 and216,228. No runtime
rotation, scaling, tint, blend, fade, visual masks or procedural FX in the new
renderer. Pixel readbacks are collision masks only. Existing downloaded sky
arena and unrelated older effect owners retain their prior rendering.

Selected changes after review: exclude geyser source7/8 (unwanted second
eruption); change accidental cyan energy to violet, retaining white cores;
offline fixed12px breakup map removes the persistent face from the generated
dissolve while retaining its authored detached sparks. All raw frames and
selection notes are preserved. The brain crown clears the boss HUD.

Sources/prompts/jobs/selections/hashes: `_ART_SOURCES/dracodia_brain_1023/`.
Builder, downloader, installer and native probe: `_BUILD_SOURCE/*dracodia_brain_1023.py`.

The early candidate smoke used completed PixelLab base art in browser-only
routes while animation jobs were still processing. It is not final animation
evidence. Final native report and movie use the installed generated banks.
No commit/push or unrelated project cleanup is part of this change.

Final verification:31 native combat/art/audio checks plus4 continuity checks
passed; no page/asset errors. The required complete core suite ended BUILD OK,
0 errors, exit0. Continuity initially tried to morph the main form before its
existing attack-book gate; the fixture now satisfies that gate, which remains
unchanged. The movie is a controlled native demonstration, not a full human
campaign playthrough.
