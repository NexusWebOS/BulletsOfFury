Sumpjaw side-rush / burrow / paired arches

Both snakes perform four alternating offscreen-to-offscreen side runs at430,560,700 and880px/s. Each has1.05s of source-authored green/yellow/red directional arrows. The heads use the actual path tangent and fire rapid toxic balls forward from their measured mouths. New side rounds outrun the snake and keep the existing unshootable/capped/lifetime rules.

They slither to separate burrow points; the heads descend through authored source-pixel poses while each body section feeds into its pit. Both become fully underground. Two marked emergence points commit to the pilot current position. The snakes rise from their pits and perform staggered high arches over that committed point, land, then leave north and return to the existing book. Moving the pilot after commitment does not move the targets.

Native pools, gill gates, independent7000HP halves, hit flashes, pause, survivor and once-only defeat/reward remain. The earlier continuously moving jumps are retained. Player shooting/interception rules stay native.

GIF: both-snakes-full-sequence.gif â€” full native480x512 view,15fps, first warning through the two landings; MP4 also included. QA starts directly at the new chapter and protects the stationary pilot; all later phases/attacks use native update/draw owners.

New pit art was made with the built-in image generator and saved as generated-burrow-master.png; prompt is in generation-prompt.txt. Existing serpent identity, damage/hit frames and warning-arrow silhouette are retained.448 authored frames in18 fixed even-size banks; editable Aseprite sources in editable/. Runtime uses fixed blits and positions only.

See verification-summary.json for observed speed/overflight results. The full test suite still exits1 at its recorded missing difficultyHealthBaseline15 dependency; it is not a full-suite pass.

Owner: assets/sumpjaw_tandem_1105.js; assets/game/shared/combat/snake_assault_1110/*.png. Source and verification: _BUILD_SOURCE/snake_assault_1110/. No game.js changes, commit, push or installer. The requested arrow warnings are a scoped user override of the older no-arrow preference.

November10 correction: one authored direction-arrow indicator per living snake at its viewport entry edge, replacing the seven repeated lane markers. Green/yellow/red warning timing, direction, side runs, burrow and arches are retained.24 native cases verify both directions, all three warning colors, paired and solo states. Source/evidence: _BUILD_SOURCE/snake_arrow_1110/.
