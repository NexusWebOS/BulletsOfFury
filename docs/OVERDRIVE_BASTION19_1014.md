# Overdrive: gritty base / ground animation pass — 2026-10-14

Build: `overdrive1014-bastion19-r1`. Local game:
http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-bastion19-r1

The eight-room rear-view base now uses an inset rocky border, tapered industrial
wall/ceiling/floor, rusty panel materials, an authored rear blast door and matching
core/corner fixtures. Damage progresses through authored wall states. Room
transitions retain blast → hop → forward perspective travel → full black → new room.
Yuri is drawn behind foreground cover; intact cover hides his crouched body and
blindfire raises the rifle. Player combat camera remains fixed during boss fights.

Room eight replaces the computer-face plate with a blue cylindrical glass reactor:
red/black clamps, conduits, contained white/cyan sphere, rotating arcs/rays,
progressive glass damage and containment shatter followed by the white reveal.
Helios has a new luminous fire/violet-prism identity, short authored flame aura,
surface lighting, walk/run, charging/throw/recovery, lightning, jump/slam, hit and
collapse banks. Run/throw/jump use 16 drawings. Volley release uses the actual
authored hand point. Matching new warning seals, orb, geyser and lightning effects.

Gosfer has new readable armor and a long two-handed laser rifle. Patrol/walk,
charged fire, reflex dash and collapse are authored whole figures. The encounter
cycles laser bursts, sweeps, a lateral dash and a telegraphed cover breaker.
Its front-facing cover has 48 HP, eight visual wear states and loses collision
when broken. Ordinary ground bunkers and tall walls retain their existing behavior.

Yuri's new eight-facing rifle/walk and grenade banks retain suit color and grip.
Moving fire shares the walking phase; stationary fire and cover rise use planted
feet. Prone/crawl, rise, blindfire, sidestep, knockback/revive and hop art are
registered into the runtime. Grenade facing is captured at throw start; the throw
never selects the old south-only bank. Muzzle effects use current pose sockets
throughout their short lifetime, including movement and recoil. Enemy troops have
new matching walk/fire/crouch/collapse art and a vault bank.

Quick keyboard action taps are buffered until the next simulation step. F toggles
prone; WASD crawls. On the raw M30 2.4G six-button layout, Mode + X toggles prone
and the D-pad crawls. Options continue to support M30, Genesis and standard presets.
The physical controller checks use synthetic reports; they do not claim a human
pressed the hardware. The full D-pad route uses logical controller actions.

Owning art workflow: `expansion/topdown/_research/build_bastion19.py`.
Pack: `expansion/topdown/art/bastion19/manifest.json` and `manifest.js`.
621 unique authored PNGs, 634 keys including aliases, 197 sequence keys including
aliases. Every export uses even dimensions, hard alpha, a shared bank canvas and
one proportional bank scale. Original built-in image-generator PNGs, prompts,
rejected candidates, supplied references and the technical gait guide are retained
under `source/`. There are no reconstructed limb rigs or synthetic tween drawings.
Existing unchanged roll/jump and unrelated pilot banks remain available as fallbacks.

Validation: 15 focused checks and 23 M30 checks pass; all 621 new PNGs drawn through
the native Art renderer without page/console/asset errors. Actual native rifle
shots defeat animated Gosfer in an isolated protected fixture. Both complete
Normal routes clear eight rooms, seven full passages and both final forms with
33 kills and no deaths: mouse 139.017 seconds, D-pad Retina 145.250 seconds.
Both collect and fire shotgun, laser and minigun. Required main-game syntax check
and test_fl complete with zero errors and exit 0. See
`docs/qa/overdrive_bastion19_1014.json`; native gallery, onions, contact sheets and
animated WebP clips are under ignored `_shots/bastion19/`.

Level 7 pinned password: `OD-237F-5JXR`.
Level 3 pinned password: `OD-237B-5JXM`.
No commit/push requested. This pass does not change `assets/game.js`.
