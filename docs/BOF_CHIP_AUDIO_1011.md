# BOF — approved ColeForge sound pass, October 11

Mike approved the named cues in `BOF_Chip_Library_1011`, all four score bullets,
all tank/ground cues, and the remaining BOF-tab entries from `gd_shellImpact`
through `gd_ammoPickup`. The separate genre study banks are outside this pass.
Spelling is resolved to the library's canonical names, including
`element_lightning_hit`, `missileLaunch`, `decker_shell`, `laserBeamHit` and
`gd_turretTraverse`.

[Audition all approved cues](previews/chip_audio_1011/index.html).
[Open BOF](../index.html). [Open Overdrive](../expansion/topdown/index.html).

## Installed bank and events

The main game imports **81 approved MP3s**, byte-for-byte, with their recipes
and source hashes. The external library is unchanged. The owning
[builder](../_BUILD_SOURCE/build_chip_audio_1011.py) writes the
[manifest](../assets/game/shared/audio/chip_1011/manifest.json) and classic-script
registry. Existing generated manifests are untouched. Its 43 excluded keys are
recorded explicitly. In particular, the separately named unapproved enemy
missile cue, ordinary explosion pair, general blip/pickup sounds and music
retain their recordings.

The [runtime owner](../assets/chip_audio_1011.js) loads after earlier sound and
encounter extensions. Canonical names and approved aliases share a pool and a
retrigger gate. This prevents a single volley from stacking several aliases of
the same recording. Short sounds retain the existing 64-decoder budget, mixer
and volume sliders. Approved chip recordings bypass old tone filters; they also
play through the portable `file://` build.

| Event | Approved recording / connection |
| --- | --- |
| Save/map errors, kill credit, bomber/rebel alerts and bomb release | `error`, `enemyDie`, `alert`, `bombDrop` now have real samples |
| Shield collapse, including combat and Rebel cloak break | `shieldBreak` and its `shieldBreakCombat` alias |
| Forge welding and completed product | One `forgeWeld` loop during welding; `forgeComplete` at the reveal |
| Weapons Gained, Loadout cursor/equip/launch | `weaponFound`, `loadoutSelect`, `loadoutEquip`, `loadoutLaunch` |
| Lightning infused contact and geyser | `element_lightning_hit`; `geyserLightning` starts with the plume/column eruption |
| 100/250/500/1000 score pickups | The four corresponding `scoreBullet` cues |
| Stylish dodge, score-to-Furious conversion and new achievement | `stylishDodge`, `furiousCoin`, `achievement` |
| Timed bomb fuse and explosion; Juggernaut ram launch | `timedBombBeep`, `timedBombBlast`, `chargeDash` |
| Normal enemy pulse lasers; missiles/volleys; nuclear launch | `enemyLaser`, `missileLaunch`, `nuclearLaunch` |
| Boss cannon, rail cannon, metal contact, missile hit and bomb | `bossCannon`, `railCannon`, `impactMetal`, `missileHit`, `bombDropLegacy` |
| Extra life, player death and Decker shell eject | `extraLife`, `playerDeath`, `decker_shell` |
| Heavy enemy laser, quad fire, Furnace and Hammer releases | Four distinct approved cues, including through the realm sound dispatcher |
| Shield impacts/deflection, block/slice/douse/freeze/lock | Their named approved cues replace the prior handles |
| Boss/ice explosions, lightning chaingun, gravity/shadow families | Their named approved cues use the new bank |
| Laser Mist unlock, Fury arrival, boss shield teleport/static | Their named approved cues use the new bank |
| Tank/ground vocabulary | All 18 cues are registered; owning BOF tank events use those listed below |

Registration does not invent an ability, infantry mission or event in BOF where
none exists. Remaining ground cues stay available to their Overdrive owners.

## Firewall timing

The Stage 2 weather controller creates the sound with its actual travelling
wave. Four 1/2/4/8-second variants are derived from the original WAV with
FFmpeg `atempo`; Chromium chooses a nearby span and preserves pitch while
matching the remaining travel time. Current wave travel is about **1.28 seconds**.

One voice follows that wave. It stops at controller retirement, boss-warning
cancellation, pause, death, scene exit or focus loss. Resume seeks into the
remaining wave rather than repeating a whole launch. Master/SFX changes apply
during travel. The existing separate warning and pass-by events remain.

## Tank bosses

Razorback and the three password rigs have a quiet engine bed when alive and
visible. Treads require actual movement; traversal requires changing aim. Beds
are shared across nearby eligible tanks rather than multiplying by the module
count. They retire with the owning action/state.

- **SONIC:** tank engine/treads; existing sonic pressure and charge identity.
- **ORDOS:** tank engine/treads, approved missile launch and missile impact.
- **HARK:** tank engine/treads, approved tank cannon and ground shell impact.

No attack timing, damage, projectile speed or collision geometry changed.

## Overdrive

The existing [Overdrive sound pass](OVERDRIVE_CHIP_AUDIO_1011.md) already imported
the same 81 approved source recordings. It retains its separate portable bank
and current event connections. This follow-up fixes its future firewall hook's
Master-slider application, including changes while a wave is active.

Overdrive currently has no travelling firewall attack; its hook is tested, not
claimed as a new playable attack. The audio probe now explicitly navigates the
voiced intro and yields between input batches. An older accelerated route could
leave a pending pilot launch, invalidating the subsequent pause assertion.

## Verification

- JavaScript syntax checks pass.
- Full base suite: **8,700 assertions, 0 failures, final success summary, exit 0**.
- BOF native audio/event/audition probe: **46 checks**, including actual playback
  of all 81 cues, canonical gates, named boss routing, Forge, rewards, firewall
  ownership, all three password tanks, volume, death/pause/focus cleanup and
  `file://` playback. Zero page/console/asset errors.
- Overdrive native audio probe: **44 checks**, including playback of all 81 cues,
  current menu flow, tank/infantry/boss events, master-volume changes and portable
  playback. Zero page/console/asset errors.
- Inspected native screenshots of the firewall, Forge and tank encounters, plus
  desktop and 390-pixel audition layouts. Audio fixtures use player protection;
  they do not establish a campaign clear rate or substitute for Mike's mix review.
- `game.js` remains LF; the untouched `test_fl.js` remains CRLF.

Reproduce with `python _BUILD_SOURCE/probe_chip_audio_1011.py`,
`python expansion/topdown/_research/probe_chip_audio_1011.py`,
`node --check assets/game.js` and `node _BUILD_SOURCE/test_fl.js`.
Portable record: [sound verification](qa/bof_chip_audio_1011.json).
Local captures/logs remain in ignored `_shots/chip_bof_1011/` and
`_shots/chip_audio_1011/`.

Local changes only. No commit or push was requested for this sound pass.
