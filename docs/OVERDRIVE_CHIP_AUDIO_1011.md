# Overdrive — approved ColeForge chip sound pass, October 11

Entry point: [Ground Operations](../expansion/topdown/index.html).
This pass uses Mike's `BOF_Chip_Library_1011` library and the approval given in
**BOF - OVERDRIVE - Xpack**. It applies to the standalone expansion.

## Later menu mix adjustment

The subsequent [BOF chip sound pass](BOF_CHIP_AUDIO_1011.md) reverified the same
81 recordings in both games. Overdrive's firewall hook now applies Master as
well as SFX volume at creation and during travel. The current audio probe has
**44 passing checks, zero browser errors**, including the new volume check.
It explicitly skips the spoken intro before navigating title/difficulty/pilot;
the former accelerated route could leave a launch pending. Older counts below
describe the initial import and menu checkpoints.

The restored [Overdrive Options/menu pass](OVERDRIVE_MENU_1011.md) reduces the
engine cue gain from .22 to .08 and boosted engine playback rate from 1.22 to
1.12. Options adds Master, Music, SFX, Voice and a separate Tank Engine slider.
The imported MP3s are unchanged. Current sound regression remains 43/43 with
zero browser/media errors. Earlier base-suite results below are historical;
the later menu pass reaches 8,696 base assertions with zero errors, exit 0.

## Imported bank

The [code-owned manifest](../expansion/topdown/audio/chip_1011/manifest.json)
contains **81 approved cues**, their original recipes, source SHA-256 hashes,
loop flags, duration, gain and retrigger gates. Shipping MP3s are copied
byte-for-byte from the external library. Its originals remain intact.

The import resolves Mike's spelling to the library's canonical keys, including
`element_lightning_hit`, `decker_shell`, `gd_turretTraverse`, `gd_tankCannon`
and `gd_shellImpact`. It includes all four `scoreBullet` cues and all 18 ground
cues. “All sounds after that” includes the rest of the **BOF library tab** after
`chip_gd_shellImpact`, through `chip_gd_ammoPickup`. Genre study banks are separate.
The manifest records the 43 unapproved BOF cues excluded from this pass.

The [import builder](../expansion/topdown/_research/build_chip_audio_1011.py)
owns the copied bank and its manifests. The base game's generated manifest and
audio files are not rewritten.

## Gameplay connections

| Event | Approved cues |
| --- | --- |
| Tank idle, actual travel, independent turret rotation | `gd_tankEngineLoop`, `gd_tankTreadLoop`, `gd_turretTraverse` |
| Starting speed boost | `chargeDash` once per boost start |
| Uncharged cannon / armor-piercing release | `gd_tankCannon` / `railCannon` |
| Tank shells / missiles / laser contact | `gd_shellImpact` / `missileHit` / `laserBeamHit` |
| Homing and Retina launches; empty rack | `missileLaunch`; `error` |
| Enemy armor destruction | `enemyDie` |
| Warrior and Machinist volleys | `quadFire`, `enemyHeavyLaser`, `missileLaunch` |
| Other enemy cannon / rail and laser fire | `gd_tankCannon`, `bossCannon`, `railCannon`, `enemyLaser` |
| Wren's active Bastion, absorbed hits, broken module | `bossShieldStatic`, `shieldImpact`, `shieldImpactHeavy`, `shieldBreak` |
| Boss destruction | `expBoss` at the wreck beat |
| Concrete cover / building collapse / crates and exhibits | `gd_wallBreak` / `gd_buildingCollapse` / `gd_crateBreak` |
| Infantry movement, rifle, death/CQC, prone cover | Alternating `gd_footstepA/B`, `gd_soldierRifle`, `gd_soldierDown`, `gd_coverEnter` |
| Grenade throw / napalm / infantry rocket | `bombDrop` / `bombDropLegacy` / `missileLaunch` |
| Reload, dry magazine, blocked hand socket, roll | `loadoutEquip`, `gd_ammoPickup`, `error`, `blocked`, `stylishDodge` |
| Spotting and current ALERT phase | `gd_spotted`, `alert`, `gd_alarmLoop` |
| Fortress gate and cleared Museum room | `gd_doorOpen` |
| Pilot/mission selection, confirmation, launch; Museum gun swap/boarding | `loadoutSelect`, `loadoutEquip`, `loadoutLaunch` |
| Weapon, ammunition/repair, life and score pickup | `weaponFound`, `gd_ammoPickup`, `extraLife`, `scoreBullet1000` |
| Fatal player damage; rescue/clean-clear reward | `playerDeath`; `achievement` |

Loops belong to live actors and actions. They stop on release, lack of actual
travel against a wall, death, pause, Help/setup/menu, mission restart, ejection,
focus loss or invisibility of nearby actors. Nearby armor is quieter than the
player. One-shot pools have four voices per key and a 24-voice active ceiling;
continuous effects have a 12-voice ceiling. Retrigger gates share a canonical
key across aliases. A heavily armored hit still selects its sound from incoming
strength, before armor reduces damage.

The dedicated [sound owner](../expansion/topdown/js/audio_1011.js) uses HTMLAudio
and works over HTTP and `file://`. The earlier supplied Warrior boss music retains
its owning fight and loop. Existing flight guns/charge/impact cues without an
approved contextual replacement retain their existing recordings.

## Firewall timing and later abilities

`firewallLaunch` has four additional **1, 2, 4 and 8 second** variants made from
the authored WAV using FFmpeg `atempo`, preserving pitch. The original approved
MP3 is also retained. A caller can use:

```js
TD.Audio.firewall(wave, expectedVisibleTravelSeconds);
```

The sound owner chooses a nearby duration variant and retimes it with pitch
preservation. The supported span is 0.5–16 seconds with media playback rates
between 0.5 and 2. The wave's live bounds stop it earlier on leaving the visible
playfield, impact/death, pause or scene exit. A caller may supply a third
argument, a visibility predicate, for its exact multi-part wave bounds.

**This ground build currently has no travelling firewall attack.** This is a
verified timing/ownership hook for that attack, not a new gameplay mechanic.
Approved Forge, element, gravity, shadow, ice, timed-bomb and flight-boss cues
remain registered for their owning future expansion systems. Importing a cue
does not add those systems or attach unrelated sounds to current attacks.

## Verification

- All standalone JavaScript and `assets/game.js` pass `node --check`.
- Native sound probe: **43/43**; all 81 imported cues decode and advance, including
  real loop playback. No sound runtime, page, console or asset errors. Portable
  `file://` playback also passes.
- Existing Warrior/boost/music probe: **22/22**, zero browser errors. The supplied
  music actually plays and loops; the large authored modules still detach with
  their exact rotation, pivot and scale.
- Native screenshots of tank boost, concrete demolition, Warrior volleys,
  infantry movement and death were inspected. Fixture protection flashes are
  hidden only for the living-player screenshots; gameplay art remains authored.
- Required base suite reaches its final summary with **8,687 passing assertions,
  5 failures, exit 1**. The base harness does not load this standalone expansion.

The base failures are the Decker and Juggernaut pilot labels, Stage 6's twelve
Heavy Turbulence airframes, Stage 7's eleven field units and the measured toxic
sewer roster missing `s7walker`. Two labels also failed in the preceding Warrior
record (9 failures); the three roster names differ from that prior record.
Separate active base-game work has changed during this session. This pass makes
no claim that the full base suite is green or that those findings are fixed.

See [portable verification record](qa/overdrive_chip_audio_1011.json). Native
logs, screenshots and the full suite log are in ignored `_shots/chip_audio_1011/`.
The fixtures verify playback, events and pixels; they do not replace Mike's mix
review or establish an unassisted campaign clear rate.

```powershell
python expansion/topdown/_research/build_chip_audio_1011.py
python expansion/topdown/_research/probe_chip_audio_1011.py
python expansion/topdown/_research/probe_warrior_1011.py
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
```

Changes are local; this sound pass has not been committed or pushed.
