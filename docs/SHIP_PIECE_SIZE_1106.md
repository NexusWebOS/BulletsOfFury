# Stage5 assembly piece size — November6 / revision F

Mike requested smaller ship pieces after reviewing the restored Stage5 ascent.
The shared incoming kit now uses a64px cell instead of118×1.65=194.7px: about67%
smaller before convergence. Proportional sizes within the twelve-piece family
remain intact. Original128px source artwork is retained, with no regeneration.

The travel/orbit radius is independent of component draw size. Arrival paths,
individual sound timing, charge/scatter timing and final docking positions/sizes
are retained. The central aircraft and48px completed space fighter keep their
existing sizes. Cole's separately authored assembly plate keeps its existing
aircraft-matched scale. The shared pose also feeds SF14 part silhouettes/welds,
so those overlays follow the smaller components without detached old-size glows.

Fourteen focused real headful Chromium checks passed, including recorded native
component blits no larger than64px,300 finite poses across all twelve parts,
exact final docking sizes, the full assembly sequence, white-covered sky/space
swap, continuous countdown-to-PLAY scroll and retained-ship entry. Screenshot
review confirmed smaller pieces remain readable around the actual aircraft.
Nine additional packaged fullscreen EXE checks passed; both packaged scene
sources match repository hashes. No native page exceptions or console errors.

Core syntax check passes. Full test suite exits1 before its summary at the same
existing `difficultyHealthBaseline15` missing helper in combat_polish_0927b.js:151.
No full-campaign or new performance benchmark is claimed by this size change.

Revision F complete installer/ZIP verified every packaged member by CRC/SHA256.
The ZIP has18,957 entries. Receipts and screenshots:docs/qa/ship_piece_size_1106/.
Preview:_shots/ship_piece_size_1106/stage5-smaller-kit-live.mp4(real engine,silent).
No Git commit/push or other stage/weapon/health changes.
