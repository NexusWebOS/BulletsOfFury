# Full boss comparison library — November2

Review: http://127.0.0.1:8805/current/boss-comparison-1102.html

All current Stage1–9 minibosses and bosses are recorded on Normal, Hard and
Furious. The separate Stage6 Rough Riders route adds three films:57 total.

| Difficulty | Complete films | Recorded time |
| --- | ---: | ---: |
| Normal | 19 | 35m42s |
| Hard | 19 | 40m26s |
| Furious | 19 | 46m01s |

The shared baseline is Normal×1, Hard×1.15, Furious×1.3225 for health and turret
aiming/firing. Native difficulty-specific patterns remain. Furious Stage6 instead
uses Razorwake and Thunderhead; the right Rough Riders route remains. Furious
Stage7 uses the existing generated Sumpjaw pair, with two independent actors.

Normal campaign still ends at Stage5. Normal6–9 are isolated review-only entries.
Stage9 remains the bonus stage. Each film starts with level5 Cole and40 missiles,
uses native invulnerability, and advances through native input-driven damage and
defeat. No enemy HP, phase or attack-clock writes occur after the fresh spawn.
Native pickups and allied fire remain active, so fight length also depends on
weapon drops and targeting. Use HP and attack patterns to compare difficulty.

The page has three video columns, one audible selection, shared seeking and
per-film metrics. Play-all defaults to audible Normal. Dracodia has jumps for
the actual final transformation, Hammer, Neural Archon, helicopter, volcano and
unlocked final body. Compare-final-transformation starts each difficulty at its
own native chapter time.

The four Stage2–5 concept boards are proposals awaiting Mike's judgment. They
have not replaced live encounters. Sources, exact built-in Imagegen prompts,
asset rebuilds, new combat ownership and audio work are documented in
`FURIOUS_ENCOUNTERS_1102.md`.

## Evidence and limitations

- Every film passes native completion, full ffmpeg decode, audible audio,
  source stability during capture, difficulty and game/asset/audio-error checks.
- `collection-checks.json`:20/20 coverage/pool/form/difficulty checks.
- `playback-checks.json`:57/57 actual published URLs decode and seek through
  three nonblank movie frames in Chromium.
- `page-checks.json`:11/11 desktop/mobile/playback/sound/chapter checks.
- Native storm probes:29/29 ownership/pool/pixel checks and6/6 collision,
  evasion, continuous-flight and part-contact checks.
- Instrumental sound checks:603 cues,366 exact sources decoded and audibly
  played;136 enemy,108 weapon,18 missile and15 pickup route cases. All9 specials
  and41 unique music routes play audibly. Master mute and suspend/resume pass.
- Razorwake's published capture averages41.2 native fps; Thunderhead59.2.
  Isolated Razorwake gameplay measured55–58fps after the bounded frame cache.
  Its recording-performance dip remains visible for review. Exports are30fps.
- Required `test_fl.js` exits1 before assertions/summary because the existing
  ignored `UNUSED_ASSETS/retired_art_1022/manifest.json` is missing. No fake
  manifest or bypass was introduced.

Receipts are under `_shots/boss_comparison_1102/` and sound/native probe evidence
under `_shots/furious_encounters_1102/`. Completed media lives on D: with junctions
preserving original paths. Failed/diagnostic takes remain local and unpublished.
No Git commit or push was performed.
