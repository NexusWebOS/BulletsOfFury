# Bullets of Fury — audio routing inventory

_Runtime-verified 2026-08-27. This describes the current build; it is not an asset wish list._

## Runtime layout

- Sound effects live in `assets/game/sounds/`.
- Music lives in `assets/game/music/`.
- `BOFA.sfx` currently registers 160 named cues backed by shipped files (135 physical sound files; aliases intentionally share some files).
- `BOFA.music` registers 35 runtime keys backed by 22 physical tracks.
- The sample layer builds `Audio.SFX.<name>()` from every `BOFA.sfx` entry. There is no fixed whitelist.
- A sound entry may be a URI or an array of URIs. Arrays rotate real variations while every cue retains a three-voice overlap pool.
- Held sounds use `Snd.loopOn`, `Snd.loopTick`, and `Snd.loopOff`; release fades instead of cutting.
- High-frequency cues are throttled and/or gain/low-pass shaped through `Snd.TAME`.

## Signature combat routes

| Runtime key | Shipped file | Live trigger |
|---|---|---|
| `machineGun` | `jet_machinegun_shot_01.wav` | standard player machine gun |
| `heavyMachineGun` | `jet_machinegun_shot_03.wav` | Lizzie mounted heavy machine gun |
| `enemyMachineGunLight` | `enemy_machine_shot_light.wav` | light enemy guns |
| `enemyMachineGunHeavy` | `enemy_machine_shot_heavy.wav` | heavy enemy guns |
| `enemyMachineGunBurst` | `enemy_machine_burst.wav` | enemy burst controller |
| `coleSonicBoom` | `cole_sonic_boom.wav` | Cole Sonic Boom release |
| `laserBeamStart` | `laser_beam_start.wav` | shared held laser creation |
| `laserBeamLoop` | `laser_beam_loop.wav` | shared held laser body |
| `laserBeamEnd` | `laser_beam_end.wav` | shared held laser release |
| `flameThrowerStart` | `flamethrower_ignite.wav` | flamethrower ignition |
| `flameThrowerLoop` | `flamethrower_loop.wav` | held flamethrower body |
| `flameThrowerEnd` | `flamethrower_release.wav` | flamethrower release |
| `iceBreathStart` | `ice_breath_start.wav` | Ice Breath intake |
| `iceBreathLoop` | `ice_breath_loop.wav` | held Ice Breath body |
| `iceBreathEnd` | `ice_breath_release.wav` | Ice Breath release |

The shared laser uses one attack/body/release lifecycle. Refreshing the held beam does not stack attack transients. Maverick's homing laser volleys are discrete shots and intentionally do not start the shared held-beam loop.

The V4 bank also includes dedicated enemy pulse/heavy/scatter lasers, elemental bolts, rail and boss cannons, shield impacts/breaks, metal debris, ricochets, weapon charge, and expanded air/ground/water/boss explosion families.

## Music routing

| Route | File |
|---|---|
| title and main menu | `title_main_menu.mp3` |
| pilot select | `pilot_select.mp3` |
| campaign map | `campaign_map.mp3` |
| password and stage-clear stats | `password_and_stage_clear.mp3` |
| stages 1–9 | dedicated `stage1_...mp3` through `stage9_bonus_warp_run.mp3` tracks |
| bosses 1–8 | dedicated `boss1_...mp3` through `boss8_vile_existence.mp3` tracks |
| credits | the retained former Stage 8 theme |

The stage-clear sequence also fires the shipped `stageClear` jingle before the statistics screen. Main-menu music is restored when Campaign exits back to the main screen.

## Nonvisual regression coverage

`_BUILD_SOURCE/test_fl.js` verifies that registered audio paths exist, generated `Audio.SFX` methods are callable, mix shaping exists, signature call sites are wired, and held laser/flame lifecycles do not stack. It cannot judge loudness, timbre, clipping, or subjective mix balance; those remain listening/playtest checks.
