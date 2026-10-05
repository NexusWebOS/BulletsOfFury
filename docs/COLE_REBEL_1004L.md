# Cole's arsenal and the stolen-tech introduction

Mike's October 4 request adds selectable Cole primary tiers VI/VII/VIII and a
three-times Fusion overcharge, followed by the Rebels demonstrating stolen tech.

Fire/A plus Multi-retina/Y cycles the earned tiers once per chord. VI fires yellow
lasers; VII fires black lasers and its existing homing trident; VIII owns hold and
release for Fusion. The equipped plate updates immediately. Switching cancels
charge and blocks accidental firing/scanning until the buttons are released.
Selected and earned tiers persist through campaign snapshots. Death clears them
along with the existing weapon-power loss. Gravity Mode retains its own arsenal.

Fusion uses the existing primary charge duration as 100%. Held charge scales two
purple helix lances up to 314%, with fast authored phase animation. Above 200%,
pink screen flashes, red DANGER text, ship rumble and camera shake intensify.
At 300%, the bar and RELEASE warning alternate white/red. 315% invokes the normal
anchored ship death even with invulnerability or shield protection. Release below
315% remains safe; no pellets fire beneath the charge.

The projectile controller reuses spaceship target collection, modular Retina
damage routing, weapon attribution and interceptable-ordnance rules. Swept hits
produce splash, two ricochets and eight damaging purple shards. A per-owner/module
memo prevents piercing hits from being counted every frame. Secondary impacts
do not recursively create fragments. Explosion reels finish without fading.

The protected Rebel introduction shows Nyx's bright rotating crystal diamonds,
Jace charging and releasing a full-size red/orange helix ball, Decker or Cole's
recognition, Rook's taunt and outward slug rain, and Voss's warned angled departure
and fast turbo pass. Demonstration objects are separate from collision bullets;
all ten ships retain HP throughout. Voss returns to formation before combat.
Jace also uses the enlarged ball in combat, with the existing eight-way nova.
The cloak controller shares the new diamond art with the battle and rescue scene.
Friendly combat navigation and the shield-wave formation hold the lower arena.
The authored main HUD strip is restored above the game canvas.

Two new imagegen sheets retain their original RGBA bytes. Their measured frame
rectangles and registrations are rebuilt together by
`python _BUILD_SOURCE/import_cole_fusion_1004l.py`. Sources, hashes and briefs live
under `_ART_SOURCES/cole_fusion_1004l`; existing atlases are unchanged.

Validation: syntax checks pass. The full suite reaches its final summary with
7,223 passing assertions and exit 0 (baseline 7,200). Twenty-five native Chromium
and playable-review checks pass with zero page/console errors. Actual keyboard
chords, charge/release/death, moving shots, boss module collision, intro timing,
art blits, HUD pixels and all five review shortcuts were checked. Screenshots were
inspected. Initial probe reset/fixture mistakes and one palette-cache instrumentation
gap were corrected; the overload unit fixture uses the preserved native death
handler because earlier historical tests replace `playerHit` with a no-op.

Review: `_shots/cole_rebel_1004l/review.html`.
Evidence: `docs/qa/cole_rebel_1004l.json`. These are scoped automated checks,
not a campaign clear or a final difficulty judgment. Mike authorized publishing this pass to GitHub on October 4.
