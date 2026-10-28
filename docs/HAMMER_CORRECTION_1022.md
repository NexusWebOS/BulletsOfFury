# Hammer and helicopter corrections — October22

Stage5 has an extended physical straight-down descent and horizontal swing/counter, including Chromium palettes. Both standard and corrupted slam/recovery clips were regenerated again to land the lower circular hammer end-cap, with a diagonal shaft and upright head, instead of laying the curved barrel flat. Native windups, timing, recovery and death remain. Hammer head centres align native landing and exclusive chaingun crate impact.

Stage8 Hammer uses a newly authored clean256 source, padded consistently to320, across16 action families, with mirrored punch/gun variants. Rejected malformed generations remain in the source archive but are excluded from shipping. The gun uses only three mechanically valid held frames; the crossed-arm fire charge uses one authored pose plus the existing animated native aura. These are deliberately limited rather than shipping detached limbs or extra weapons. The spin bank is a front-facing waist sweep, not a complete authored rear-view turn.

Corrupted helicopter now runs the original Overlord attack controller, including charge tell/offscreen return, sweep, missile lock, sonic combo and rush. Current modular form art and actual live-part ports remain; broken guns stop firing. Native collision, hit flash, warning and projectile ownership retained.

27 banks/250 registered cells. Native Hammer40/40 and helicopter5/5. Full core result recorded in source archive. Interactive fixed-pivot onion review: docs/previews/hammer_correction_1022/index.html. No commit or push performed.

End-face regeneration: six PixelLab jobs (two impact poses, two swings, two recoveries), approximately $0.30. Blue down frames5/6 rejected for a collapsing cylinder; recovery2 rejected for an extra overhead flourish. Source clips preserved, excluded cells never shipped.

Superseding direction correction: both slam heads descend along the body centreline and land between the feet, on an end face. The earlier diagonal end-face clips are archived and retired from the live slam/recovery banks. New vertical source jobs are in vertical-jobs.json. Native centreline, hit feedback and target checks40/40.
