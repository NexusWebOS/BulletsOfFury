# BULLETS OF FURY — COMPLETE SOUND LIST (upgrade spec)
_Generated 2026-07-04 from a full audio-system audit. Three tiers: (A) synth-only sounds that NEED real samples, (B) existing samples worth upgrading, (C) sounds the game doesn't have yet but should._

## Delivery spec (applies to everything)
- **Format:** MP3 (44.1kHz, ~192kbps) — the engine loads `assets/sounds/<name>.mp3` and `assets/music/<name>.mp3`
- **Naming:** exact filenames below; drop-in replaces automatically (the engine sample-swaps any SFX that has a file, falls back to synth otherwise)
- **Loudness:** SFX peak around -6dB, consistent across the set; music around -12 LUFS
- **Length:** SFX short and dry unless noted; the engine pools each sample and rotates 3 voices, so tails under ~1.5s avoid overlap mud
- **Variations:** where marked "xN", deliver N takes — I'll wire round-robin so rapid-fire sounds don't machine-gun the same sample

---

## TIER A — SYNTH-ONLY TODAY, NEEDS REAL SAMPLES (highest priority)
These currently play as WebAudio beeps/noise. A file with the exact name gets auto-used once I add them to the swap list.

| # | Filename | Trigger | Direction / character | Length |
|---|----------|---------|----------------------|--------|
| 1 | `laser.mp3` | Laser weapon firing (held beam) | Sustained energy hum w/ attack transient; must LOOP cleanly or deliver 1.2s re-triggerable | 0.8–1.2s |
| 2 | `missile.mp3` | Player homing missile launch | Whoosh-ignite, rocket motor kick ×3 variations | 0.5s |
| 3 | `firewall.mp3` | Firewall weapon ignition | Flame burst + roaring bed | 0.8s |
| 4 | `crash.mp3` | Rival plane spiraling down / crash | Doppler engine whine descending into impact | 1.5–2s |
| 5 | `getready.mp3` | "GET READY" pre-stage callout | Voice or klaxon sting | 0.8s |
| 6 | `go.mp3` | "GO!" stage start | Punchy voice/sting | 0.4s |
| 7 | `douse.mp3` | Fire extinguished (water/ice interactions) | Steam hiss ×2 | 0.5s |
| 8 | `crackle.mp3` | Electrical damage / crackling wreck | Electric arcing ×3 | 0.6s |
| 9 | `freeze.mp3` | Ice weapon freezing a target | Crystalline freeze-over sweep | 0.6s |
| 10 | `shatter.mp3` | Frozen enemy shattering | Glass/ice shatter burst ×2 | 0.6s |

## TIER B — SAMPLE EXISTS, UPGRADE CANDIDATES (current file in `assets/sounds/`)
Ranked by how often the player hears them (call-count in code × gameplay frequency).

| # | Filename | Trigger | Heard | Upgrade direction |
|---|----------|---------|-------|-------------------|
| 1 | `shoot.mp3` | Player machine gun (every shot, ~12/sec held) | CONSTANT | Tight punchy tap, almost dry; needs ×4 variations badly — this is the most-heard sound in the game |
| 2 | `hit.mp3` | Bullet connects with enemy | CONSTANT | Meaty thunk w/ metallic ring; ×3 variations |
| 3 | `expSmall.mp3` | Small enemy death / crate pop | Very frequent | Crisp compact blast ×3 |
| 4 | `expBig.mp3` | Large explosion / boss hits / bombs | Frequent | Deep chest-hitting boom w/ debris tail ×2 |
| 5 | `enemyShoot.mp3` | Every enemy shot (now incl. FIRETYPES: pellet/dart/gem/orb/comet/flare/blast) | CONSTANT | Distinct from player shot; softer/darker. NOTE: see Tier C — per-firetype sounds would be better |
| 6 | `spread.mp3` | Spread weapon shot | Frequent | Multi-barrel thump |
| 7 | `blip.mp3` | UI cursor move + lock-on acquire ticks (0.11s repeat) | Frequent | Clean short UI tick; must survive rapid repeat |
| 8 | `select.mp3` | UI confirm | Frequent | Satisfying confirm chirp |
| 9 | `powerup.mp3` | Weapon pickup collected | Frequent | Bright ascending reward |
| 10 | `weapon.mp3` | Weapon switch/level-up | Common | Mechanical rack/charge |
| 11 | `bomb.mp3` | Bomb/nuke deployed | Common | Launch thunk + rising whistle |
| 12 | `grenade.mp3` | Grenade toss (Cole kit) | Common | Pin+toss ×2 |
| 13 | `bossAlarm.mp3` | Boss approach warning (8 call sites) | Every stage | Iconic klaxon — worth real production value |
| 14 | `death.mp3` | Player ship destroyed | Occasional | Heavier catastrophic blast + tail |
| 15 | `life.mp3` | Extra life gained | Occasional | Classic 1-UP fanfare sting |
| 16 | `stageClear.mp3` | Stage clear jingle | Per stage | 2–3s victory sting (leads into stats screen) |
| 17 | `gameover.mp3` | Game over sting | Occasional | Somber 2–3s |
| 18 | `victory.mp3` | Final victory | Once/run | Triumphant 3–4s |
| 19 | `announce.mp3` | Title screen announce | Menu | VO or big brass hit |
| 20 | `selectpilot.mp3` | Pilot select screen enter | Menu | Hangar ambience sting |
| 21 | `goodluck.mp3` | "GOOD LUCK PILOT" comm | Per stage | Radio-filtered VO or comm beep flourish |
| 22 | `boot.mp3` | ColeForge boot chime | Once/session | Studio sonic logo — brand moment |
| 23 | `chime.mp3` | Boot/UI chime (aux) | Rare | Pair with boot |

## TIER C — DOESN'T EXIST YET, SHOULD (new features have no audio)
These systems shipped recently with NO dedicated sound. I'll wire each once files arrive (exact names below).

**Rival dogfight (whole feature is under-scored):**
| Filename | Trigger |
|----------|---------|
| `rival_flyby.mp3` | Rival's high-speed flyby pass in the intro cinematic (doppler scream) |
| `rival_lockon.mp3` | Retina lock CONFIRMED on rival (distinct from acquire blips) |
| `rival_throttle_up.mp3` | Holding M — engine spool-up / afterburner |
| `rival_throttle_down.mp3` | Holding N — engine ease-off |
| `crate_crack.mp3` | Missile crate cracked open mid-air |
| `pack_collect.mp3` | Missile pack magnetized + collected |
| `dlg_tick.mp3` | Dialogue typewriter tick (currently silent) |
| `dlg_advance.mp3` | Dialogue line advance |

**Fire-type projectiles (all currently share `enemyShoot`):**
| Filename | Trigger |
|----------|---------|
| `ft_pellet.mp3` | MG pellet streams (rival, turrets, boss MG) |
| `ft_dart.mp3` | Dart volleys |
| `ft_gem.mp3` | Ice gem shots |
| `ft_comet.mp3` | Comet/plasma lobs (deep whoosh) |
| `ft_flare.mp3` | Flare ring bursts |
| `ft_blast.mp3` | Leviathan heavy blast streams |

**New enemy classes (deaths currently share expSmall/expBig):**
| Filename | Trigger |
|----------|---------|
| `death_tank.mp3` | Ground vehicle destroyed (metal + treads) |
| `death_boat.mp3` | Naval unit destroyed (blast + water) |
| `death_air.mp3` | Aircraft destroyed (blast + falling whine) |
| `death_turret.mp3` | Emplacement destroyed (structural collapse) |
| `death_miniboss.mp3` | esB big-craft destroyed (multi-stage detonation) |
| `deco_break.mp3` | Destructible decorative broken |

**Misc gaps:**
| Filename | Trigger |
|----------|---------|
| `menu_back.mp3` | Cancel/back in menus (currently reuses blip) |
| `pause.mp3` / `unpause.mp3` | Pause toggle (silent now) |
| `lowhealth.mp3` | Player at 1 HP warning loop |
| `retina_charge.mp3` | C-hold retina charging loop |
| `nuke_warhead.mp3` | Cole's warhead — deserves a signature launch+impact pair |
| `credits_amb.mp3` | Victory flyover wind/engine ambience under credits |

## MUSIC (all present as files — upgrade at your discretion)
| Key(s) | File | Where |
|--------|------|-------|
| title, menu | `main-menu.mp3` | Title + menus |
| select | `selectscreen.mp3` | Pilot select |
| password | `enter-password.mp3` | Password entry |
| lvl1–lvl6 (stage/jungle alias lvl1) | `lvl1..lvl6.mp3` | Stage themes (note: only 5 stages exist; lvl6 reserved) |
| boss1–boss6 (boss aliases boss1) | `boss1..boss6.mp3` | Boss themes |
| rival | `rival.mp3` | Rival dogfight (Rival Dog Showdown — new, keep) |
| — MISSING — | `stageclear_theme.mp3` | Stats screen currently reuses stage music post-jingle |
| — MISSING — | `credits.mp3` | Victory credits currently silent under flyover |

## Wiring notes (for me, when files arrive)
- Tier A/B: drop files in `assets/sounds/`, add Tier-A names to `SFXMETHODS` swap list (one line).
- Tier C: new `Snd.play()` hooks at each trigger — call sites already identified in this audit.
- 3-voice pooling per sample exists; round-robin variation support needs a small extension (name suffixes `_1.._n`).
