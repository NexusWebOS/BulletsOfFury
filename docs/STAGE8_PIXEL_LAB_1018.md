# Stage 8 — PixelLab possession and modular finale

Mike's October18 request replaces all three boss encounters with PixelLab art
and gives the last encounter its main body plus exactly four copies: Hammerboss,
helicopter, Harrier and volcano. This is a specifically authorized Stage8 modular
exception. Other bosses and the existing Stage7/8 field-enemy pass are unchanged.

## Generated art

The actual native bosses were exported and inspected before supplying identity
references to PixelLab. Seven Pro-model designs preserve recognizable cores,
talons, rotor mast, fan casings, hammer and volcanic cannon silhouettes.

| Bank | Poses | Behavior shown |
|---|---:|---|
| Infused drone | 16 | Green eye, infection veins and flexing talons |
| Ghost | 16 | Spectral core, tendrils and claws |
| Main Colossus | 16 | Reactor, armored ribs and scythe claws |
| Hammer | 16 | Charged core and articulated hammer lift |
| Helicopter | 16 | Actual generated rotor orientations |
| Harrier | 16 | Fans rotate inside their fixed casings |
| Volcano | 16 | Reactor, magma channels and chimney flames |
| Drone takeover | 32 | Original drone physically consumed and infused |
| Ghost emergence | 24 | Infected drone armor opens into the spectral form |
| Colossus emergence | 24 | Ghost becomes the armored main organism |
| Four form morphs | 16 each | Tendrils consume/reassemble each specific copy |

These256 poses produce336 module layers and144 full-frame transformation cells,
plus the actual original drone:481 shipping PNGs, approximately8.70MiB.
All boss/effect cells are320×320 with physical pivot160,160. The arrival drone
is256×256. Transparent padding and integer registration use stationary skull or
rotor-mast detail. A pulsing energy centroid never moves the whole body. Each
three-layer reconstruction is RGBA-identical to its full authored frame.

The first MiniMax volcano idle contained gray opaque frames8–12. That whole bank
is retained as rejected source and never registered. Its replacement is16 genuine
standard-model poses from a176×176 reference, normalized proportionally as one
bank. The inspected256×256 MiniMax volcano transformation is the selected morph;
an unused completed standard-model fallback remains in the PixelLab gallery.

Owning build: `_BUILD_SOURCE/build_stage8_pixellab_1018.py`. Source, prompts, job
IDs, anatomical masks, chosen banks and registration audit are under
`_ART_SOURCES/stage8_pixellab_1018`. No shared atlas was modified.

## Native encounter

`assets/stage8_pixellab_1018.js` owns only Stage8's three encounters. Each design
has its own core and independently damageable left/right weapon assemblies.
Rendering, alpha hit tests, Retina positions and gun muzzles use those same
animated layers. Ordinary primary fire and missiles can damage the core. Every
hit flashes the real owner and part pixels; timers expire normally. Destroyed
weapons scatter through the existing destruction system and lose their locks,
ports and their own active beams.

Each identity has three distinct attack types. The drone uses talons, guns and
crossbeams; Ghost uses rails, pincers and targeted blasts; the main body uses
tentacles, fans and a code wall. Copies retain their recognizable weapon grammar:
Hammer strikes/chromium lanes/jumps, helicopter guns/missiles/bombs, Harrier
fan beams/missiles/fans and volcano magma/flamethrower/firewalls. The volcano
flamethrower uses the approved generated fire root/body/tip renderer.

Normal/Hard/Furious warning times are1.10/.96/.82seconds and recovery times
1.15/.85/.60seconds, with increasing gun pressure and fan counts. Warning lanes
and targets commit before release. Later player movement cannot move those
promised lanes.

The last encounter has five finite pools. Main-body and module damage persists
through visits; the rotation visits all four copies. A depleted form is never
selected or healed. Once the five pools are empty, the existing Dracodia death,
red return portal, reunion and single campaign-clear owner take over.

## Phase transitions

The current arena fades out for1.05seconds. The next arena swaps only during a
full-black hold, then fades in while the generated emergence plays. Native
captures measure the playfield as completely black at both swaps. The side HUD
stays in place. Existing PixelLab arena plates and code parallax retain their
phase identities, including the dark final void.

Dracodia's authored monologue is preserved after the third body forms. Its old
cinematic protection cannot leak180seconds of invulnerability into combat:
combat resumes with at most.5seconds of grace, which actually expires. The
preview and verification bot have their own explicit invulnerability override.

## Verification and review

- `node --check assets/game.js`, generated manifest and runtime: pass.
- `node _BUILD_SOURCE/test_fl.js`:8791 passing,0 failing, exit0, final BUILD OK.
- Complete native pass:232 checks,0 failures across all seven identities and
  Normal/Hard/Furious, real primary damage, hit pixels/expiry, modular removal,
  all256 poses, arena changes, five persistent lives and native campaign exit.
- Focused transition pass after the final protection repair:13 checks,0 failures.
- Delivered review page:12 checks,0 failures, including isolated saves, all seven
  scene selectors, full playfield, onion overlay and real weapon-break control.
- No page, console, draw or asset errors. All481 PNG hashes verified. Existing
  `assets/game.js` and `_BUILD_SOURCE/test_fl.js` bytes and line endings preserved.

The broad combat pass preceded the final protection-only repair; the focused
transition pass verifies that change. These257 checks use an invulnerable pilot
and establish functioning, visible, finite encounters; they do not establish
human clearability or final balance.

Interactive review: `docs/previews/stage8_pixellab_1018/index.html`. It embeds the
actual index/game and preserves campaign saves through a separate storage prefix.
Use the scene and difficulty selectors, Onion frames, Break left weapon and
Defeat current form. Review captures and source onion sheets are under
`_shots/stage8_pixellab_1018`; structured results are
`docs/qa/stage8_pixellab_1018.json`.
