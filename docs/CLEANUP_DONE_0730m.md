# CLEANUP EXECUTED — drop 0730m

    manifest keys   7162 -> 5924   (-1238)
    media files     7182 -> 5881   (-1301)
    assets on disk  391MB -> 349MB (-42MB)
    quarantine      1291 files, 62MB — ALL RESTORABLE

    build           1335 assertions + 30, node --check clean, 32/32 anchors

Undo anything:
    python3 _BUILD_SOURCE/execute_0730m.py --restore
    python3 _BUILD_SOURCE/sort_fx_0730h.py --restore
    python3 _BUILD_SOURCE/audit_assets_0730b.py --restore

## Removed (quarantined)

    jets-cuts      270   15 aircraft x 6 components x 3 states
    level06        210   n6j_ — ZERO code refs, whole folder was dead
    assigned       183   mba_* 16 elites + nvr_ racer
    boss-legacy    120   chopper / death / fboss / iboss / tankboss / mbp_ir / ncbp / nmc_chain
    furiousdeath   108   mbp_fd1/2/3 — FURIOUS DEATH, stage 6 boss
    level05         72   e5dv / e5it / e5tc capital ships
    sewer-extra     43   kept frame 0 per unit; exca keeps atk_0
    leviathan       34   mbp_rl boss + nrl_ racer
    boats           28   boat_b*
    drone-states    27   air_air death/fire/hurt — idle only
    gator           21   mba_cl — CESSPOOL LEVIATHAN, stage 7 boss
    l6x-orange      19   measured >25% orange
    vault-cull      15   nvg1 nvg2 nvg3 nvi2 nvy3
    turrets         12   esA_navalturret / esC_turretC2 / esC_turretC4
    trt-states      12   trt_ fire + death
    bunkers-dead    12   nbk_r0 / nbk_r3 / nge_
    naval-die        9   n6bc_die_8..16
    minitanks        7   nmt_r4 — unreachable, MINI_DEF uses rows 0,1,3,5,6,7
    tanks-death      7   wreck + hurt kept
    faces            7   superseded by port_*
    gunship-die      6   esB_big*_death
    race             4   nrj_
    tanks-alt        3   tnkG_*_alt
    ui-unwired       3   opt_controls / opt_volume / pwmenu
    orphans         74   nothing in the manifest pointed at them (24MB)

## Moved

    OVERLORD-X          75  -> assets/enemies/boss/overlordx   (ovbody_ + ovrotor_00..71)
    menu buttons        15  -> assets/ui/menubtns              (btn_ + nms_ + diff_)
    portraits           14  -> assets/ui/portraits             (now 9 pilots x 7, one folder)
    air_air              9  -> assets/enemies/drones
    bunkerB rotation     7  -> assets/fx                       (rejoins nbk_r1/r2/r5)
    mbj_cic              3  -> assets/enemies/boats
    fx root            495  -> attacks/ ui/ pickups/ explosions/ thrusters/ hazards/ weather/
    pack0704           115  -> functional folders (folder emptied)
    fx *.json           60  -> assets/fx/_json/                (_thruster_map.json PINNED)

Folders gone: bosses, furiousdeath, level05, level06, leviathan, minitanks, race, turrets,
_icons_v21_backup, ui/buttons, ui/faces, ui/modesel.

## Code changes that make the cull safe

**ART-EXISTS GUARD.** Culling art is only safe if nothing still picks it — drawEnemyArt returns
false and the dispatch falls through to a path with no art, so a culled unit still SPAWNS, MOVES,
SHOOTS and KILLS you while drawing nothing. Every enemy pool now filters to entries whose idle
frame resolves, with a fallback pool:

    stage 3 ships  -> jets        turret emplacements -> trt_ drones
    miniboss craft -> jets        vault stage 4 pool  -> nvg1/nvy3 removed

Restore the art and the pools repopulate on their own. No hand-editing per cull.

**BOSS ART GUARD.** `_bossArtOK()` checks a pack before `buildModularBoss` assembles from it, so
CESSPOOL LEVIATHAN and Leviathan are left unbuilt rather than invisible-with-a-healthbar.

**TANKS.** `enemyArtState` now returns `wreck` when a `_wreck` frame exists, else `death`. That is
what makes dropping the death frames correct rather than just quiet — tnkG_g2/g3/g5 have wrecks,
the four tnkM_ tanks fall back to idle until wrecks are authored for them.

## Still open

**n6e_tlj_ (129) and np5_orb_ (6)** are loose at the fx root. n6e_tlj reads as a sectional
aircraft (lw/rw wings, nc nose-cockpit, te tail-engines) so it is a stage-6 ENEMY, not an effect —
but nothing in the source mentions n6e_ or tlj, so I left them rather than file them wrong.

**Stages 6 and 7 have no boss art.** FURIOUS DEATH and CESSPOOL LEVIATHAN were both culled at your
instruction. The guards stop them spawning invisible, which means those stages currently have no
boss at all. Stage 6 authoring was already the big remaining jam piece.

**29 broken keys, all pre-existing** (26 ncm_font, 3 sfont) — the campaign map font is missing 29
characters, so map text has holes in it. Not caused by this pass.

**The bytes are not in the sprites.** 349MB remains and the top 25 files are 97MB of it:
atlases/main.png 11.5MB, stage3_ice_still_cant_see.wav 8.7MB (a WAV), countdown.wav 2.8MB.
Converting a handful of audio files saves more than everything cut above.
