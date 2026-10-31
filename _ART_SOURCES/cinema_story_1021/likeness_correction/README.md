# HQ Cole / Maverick likeness correction — October21

Cole is the far-left standing pilot: reference-matched swept undercut, blue eyes,
short beard, green hooded flight suit and silver harness. Maverick is the pilot
leaning on the table beside him: fuller beard, combed-back hair, olive open collar
and eagle shoulder patch. Four targeted PixelLab jobs, $0.32; balance $4.33.
The initial head edit was too conservative; Pro candidate0 supplies the accepted
head/neck artwork at one proportional5/8 scale. This is a correction for review,
not a record of Mike approving Cole's likeness or other-pilot animation production.

Original scene is retained as hq-regroup-before.png. apply_hq_likeness.py owns
the actor extraction and composition, then build_cinema_rebuild.py owns the
lossless WebP and registry. Full688x384 canvas preserved. The entire right side,
including the existing nine-cell HQ motion patch, remains pixel-identical.
The asset path uses its content hash to prevent stale browser art.

Seven focused native Chromium checks passed. Actual XART-decoded Cole pixels
equal the revised WebP; native drawImage renders the scene for Cole and Maverick;
no page/console errors. Source and native screenshot inspected. Runtime story,
dialogue UI and gameplay code unchanged, so no new full gameplay suite run.
Previous full core suite8943/0 remains the last gameplay baseline. Local only.
