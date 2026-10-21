# October 21 final art and combat pass

## Implemented

- Re-authored Dracodia's corrupted Hammer at256-square production resolution from a new512-square master: clean chromium armor, face and two-handed hammer;15 banks including mirrored gun,20-frame slam bridge,14-frame lift/charge and24-frame ball. One128,112 body pivot, consistent1.1 world scale; new gun muzzle/weapon target and flying hammer-head anchors follow the new art. Stage5 blue Hammer and native combat ownership remain.
- Stage5 siege bomber: core destruction leaves surviving module HP on the gauge and removes the dead core's Retina target. Defeat, reward, cookoff and campaign progression wait for the entire displayed health budget. All four difficulties checked through complete destruction; reward occurs once.
- Forge previews: isolated live Lizzie cannon, death/space/special flags, alternating chaingun barrels and local muzzle clocks. All eight common weapons checked for all nine pilots; live run/player/projectile/cannon state restored. Level1 alternates two physical mounts without changing live combat stats.
- PixelLab animated hex, electric, fire, toxic, ice, code and dark shield variants, plus the Hammer wall and carrier field. Native shield energy/deploy/break/hit owners remain. Transparent centers keep hulls readable. Fixed front-facing dark shield selected from generated footage.
- Portal-only upright violet and blue32-frame loops derived from the existing portal reference. No hardware frame. Stage5 mouth sizing retains the existing pass-through window; final gate and return arrival use blue. The existing screen-warp owner resolves its portal texture through the new blue animation. Cancelled an unsuitable gray-matte warp job rather than shipping it; original portal/gate sources retained.
-40 PixelLab aircraft designs, each with16 roll,16 somersault,16 drift and8 recoil/attack poses, plus idle.13 reused hull/palette families cover53 source design IDs. Three disjoint center/port/starboard source sections reconstruct every frame exactly while sharing one texture. Native yaw, death, gun/projectile emitters and hit paths remain. Stage-specific preload; bounded128-cell tint cache; metallic neutrals and white highlights preserved by alias palettes. Stationary installations and biological ground units retain their authored identity.
- Stage4 carrier receives a16-frame authored drift bank and controlled unshielded lateral travel. Rearm recenters the hull before regenerating its electric cores; all four difficulties checked for visible, in-view nodes. No arbitrary whole-plate boss rotation.
- Five Rebel AI books: Kaia's slow teal wind spread with every lane warned; Jace charging/swerving helix with warned radial split; Voss distance-to-front turbo slingshot and visible recovery; Nyx cloak until regular/Multi-Retina or missile reveals her, then charged dark-purple orbs; Rook retains gun/cannon, Rookhook and ram. Heavy move interlocks protect warning time. Additional8% HP reduction on first setup.
- Star, bowling, H and X squad formations: assemble, warn, two shootable homing missiles per living fighter, scatter south, scaled/shadowed south-to-north return and recovery. Each sequence checked on all four difficulties. Player bullets use the actual interception path. Existing allied arsenal also emits into the shared player projectile path.
- Rook reuses Juggernaut's authored ram vocabulary for windup, launch, actual contact and stop, with shared mixer cues. Juggernaut's existing real bound-input charge/ram tested: full charge, launch, movement, invulnerability and completion.
- Two new smoother PixelLab explosion banks plus fuel rupture, implosion and smoke-core sequences from Mike's supplied packs. Up to10 supplementary final-destruction bursts,12 active-effect cap, attached to the actual dr5Death/finalFall owner. Preserve hit, anchored burning spin, crash, shock ring, native explosions and opaque modular wrecks.
- StageX: SEABREAK CITY / COASTAL FRONT entrance card; coast transitions into continuous northward urban travel. Adjacent reflected districts have pixel-identical meeting rows; the camera never reverses. Blue PixelLab water is a separate scrolling/animated layer. Campaign alternate route has a protected3-second card; Rival route keeps its own entrance state.
- Six generated cinematic concepts using actual Cole, ship and Dracodia references: The Cost of Victory; Red Alarm; Federation Blackout; One Wire Survived; The Last Scream; Beyond the Solar System. Concepts are review proposals, not automatically substituted cinematic shots.

## Runtime and production files

Runtime owners: `rebel_dogfight_1021.js`, `coastal_city_1021.js`, `final_effects_1021.js`, `air_refit_1021.js`, each art owner loaded first. Native bug fixes are in `game.js`, `combat_polish_0927b.js` and `hammer_redesign_1020.js`.

Source, original references, accepted/rejected receipts, raw frames and export audits: `_ART_SOURCES/final_version_1021/`. Production assets live under the owning stage/pilot/effect directories. Builders and native probes are retained in `_BUILD_SOURCE/`. Review: `_shots/final_version_1021/review.html`.

## Verification and limits

Required suite:8,943 assertions passed,0 errors, exit0 after updating three obsolete core-only bomber defeat expectations. Existing hazard cleanup and campaign release checks were preserved and additional total-health/Retina checks added. Main game LF and harness CRLF preserved.

Native Edge/Firefox/Chrome checks exercise Forge state isolation and firing, actual replacement hull selection and damaged pixels, full bomber defeat, portal variants and carry-out, all four formations/difficulties, regular/Multi-Retina Nyx reveal, personal move recovery and Juggernaut bound inputs. Separate contact checks verify actual homing and interception, Rook ram effects, both new Hammer gun targets/muzzles, final death effects and decoded/advancing playback for nine selected sound routes. City/core environment checks cover all four carrier difficulties, protected entrance, monotonic camera, matching seam pixels and animation.

Short live performance samples retain movement, fire and repeated explosions in all three installed browsers. They are local CPU/render observations, not a promise of FPS on every laptop or battery mode. Controlled/protected combat fixtures do not establish human win rates. No new claim of campaign survival percentages is made.

StageX and new combat art are live. Cinematic boards await Mike's choice; other pilots' existing cinematic animation remains outside this pass pending Cole likeness approval. No GitHub push was requested for this pass.

## Final verification record

The finished build has155/155 native Edge contract checks,176/176 native aircraft-action checks in each of Edge/Chrome/Firefox,68/68 Hammer/shield checks,21/21 actual-contact/audio checks and8/8 carrier/city checks. Review works at1440px and390px without overflow. Runtime aircraft atlases total under2.6MB for all40 designs;558 new effect/actor poses and2,280 aircraft poses have no clipped frame edges. One weak silver-fighter roll bank was replaced by an approved true axial roll; unwanted generated purple coloration was corrected offline against each approved master palette. Native source aliases remove retired flight-texture readiness dependencies while retaining destruction reels. Nested renderers now honor the selected somersault bank.

Actual allied guns deliberately acquire and destroy incoming Rebel missiles on all four difficulties; this supplements the verified player interception path. Existing supply and dodge priorities remain.

PixelLab displayed balance:10.58USD at the verified start,2.91USD after generation. No account purchase was performed. Receipts and rejected experiments are retained outside runtime assets. No jobs remain pending. The cinematic concepts are ready for Mike's selection.
