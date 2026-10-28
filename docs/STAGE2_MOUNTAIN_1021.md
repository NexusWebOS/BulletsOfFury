# Stage 2 mountain transition - October 21

The boss-arena join slid a single screen-height terrain crop down over the animated
lava. If the boss started before the source window reached master row zero, the
top of that rectangle visibly sliced through the mountain.

`drawLevelMaster` now advances through the remaining authored source rows as the
join progresses, revealing the full top of the plate before it leaves the view.
The existing join clock still travels at 210 units per second to the visible
window height. The remaining world travel is mapped onto that same clock, and
the blit stays at native 1:1 scale with the published ground coordinates.
No new artwork, runtime textures, allocations, enemy changes or combat delays.
Other stage rendering paths and the independent lava clock are retained.

Verification: 360 native Edge source-window samples, spanning Easy / Normal /
Hard / Furious, both camera modes, five starting scroll positions and nine
join points. Actual terrain pixels match an independently drawn whole-source
reference with no exposed cropped edge. Ten check groups also cover original
completion timing, boss HP, complete departure, retry reset, animated lava and
zero browser errors. The first probe confused destination width with destination
Y in its separate cut-edge predicate; the whole-source pixel comparisons were
already clean. The corrected probe and original failed fixture receipt are kept.

Required full regression: 8,943 passing assertions, zero errors, exit 0 and final
BUILD OK. Core syntax clean; game.js LF and test_fl.js CRLF retained. Owning
probe: `_BUILD_SOURCE/probe_stage2_peak_1021.py`; matched native before/after
capture: `_BUILD_SOURCE/capture_stage2_peak_1021.py`. QA summary:
`docs/qa/stage2_peak_1021.json`. Local visual review:
`_shots/stage2_peak_1021/review.html`.

Base synchronized safely to completed GitHub update 06f413a3c before the fix;
unrelated Overdrive work preserved. This fix is local and has not been pushed.
