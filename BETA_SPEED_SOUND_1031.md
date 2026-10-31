# BOF speed and sound audit — October30/31,2026

Stage9 Black Event Horizon now uses commissioned PixelLab mint/ivory plasma with an uninterrupted authored core. Six fixed-cell banks,32 hull directions retained. The main engine file is unchanged.

| Motion | Previous | Revised |
|---|---:|---:|
| Normal firing rotation |0.23 turns/s|0.60 turns/s|
| Radial spin |1.35 turns/s|2.00 turns/s|
| Spiral angular motion |0.85 rad/s|1.45 rad/s|
| Full eye sweep |5.6s|3.8s|
| Spinning dash |2.6 turns/s|3.2 turns/s|

The1.3s beam warnings,1.65s orb warning,1.25s dash tell plus1.15s edge warning, projectile speeds, native HP10965 on Furious, damage, half-health gate and rewards are retained. The spiral now samples24 segments per arm rather than14, with effectively the same outer radius.

Explicit audio events: charge, release, three individual orb shots, radial volleys, sustained spiral/sweep/beam bed, phase change, dash launch, edge charge and re-entry. All use the shared mixer/pools, bounded voices and stop on pause/death/stage exit. Important tells briefly duck music. Default40% SFX and100% music were used. Quiet existing water, plasma, toxic and dash families received targeted gain adjustments; heavy guns were left alone.

The major mixer bug found was repeated dialogue redraws replaying already revealed text. Rough Riders:88,489 dialogue-letter requests before,418 after in the same42second fixture. Repainted lines now stay silent, newly revealed characters still tick, and a catch-up frame emits one tick rather than a stack.

## Real-time native samples

These are Furious attack checkpoints and representative enemy roster samples in the actual game engine. They are not full playthroughs or proof of every possible phase/branch. HP/phase/setup writes occur before capture only; the live simulation, attacks, hits and native music/SFX run without recorder changes. Invulnerable player uses ordinary input.

| Sample | Seconds | Native FPS under capture | Playing events | Missing pool names |
|---|---:|---:|---:|---|
|s2-enemy-roster|24|55.68|131|None|
|s5-bomber|24|57.75|99|None|
|s5-chronos|32|47.64|135|None|
|s6-carrier|28|45.43|855|None|
|s6-enemy-roster|24|54.64|377|None|
|s6-fortress|28|58.23|128|None|
|s6-nightwing|32|55.0|399|None|
|s6-red-core|24|57.2|111|None|
|s6-rough-riders|42|60.01|399|None|
|s7-dredger|36|58.83|144|None|
|s7-enemy-roster|24|56.65|229|None|
|s7-warden|36|58.12|213|None|
|s8-brain|36|58.95|79|None|
|s8-chronos-copy|32|58.54|106|None|
|s8-final-life|32|57.51|102|None|
|s8-helicopter|32|59.17|159|None|
|s8-herald-cast|20|57.53|50|None|
|s8-herald-skulls|20|57.51|57|None|
|s8-herald-storm|22|57.91|75|None|
|s8-host|28|59.24|186|None|
|s8-phoenix|36|59.11|98|None|
|s9-enemy-roster|24|55.76|189|None|
|s9-horizon|32|58.07|154|None|
|s9-horizon-water|38|58.44|179|None|
|s9-water|40|58.54|305|None|

Raw requests, accepted requests, actual HTML media playing events, cue levels, bounded live voice counts, screenshots and recorded native mixes are retained under `live-audit/<sample>/`. Some aborted resource requests are expected when lazy voices are recycled or a page closes; final retests separate these from HTTP/game errors.

## Verification limits

Playback and signal levels are instrumented. Audio audition by ear is unavailable in this environment; the recordings are supplied for listening review. This report does not claim speaker/headphone listening. No attacks were relabeled as audible based solely on a file existing.

The engine suite still has exactly its five previously recorded baseline failures (hit-flash duration; Chronos opening dialogue/jump ordering; StageX route persistence/encounter launch). Native Stage9 checks and source/asset checks are recorded separately.

## Native speed without recording

- Stage5 chromehammer: 57.91 FPS, normal native render loop without capture duplication.
- Stage6 warhive: 47.61 FPS, normal native render loop without capture duplication.
- Stage9 voidhorizon: 59.57 FPS, normal native render loop without capture duplication.

Chronos and the Harrier carrier were the slower recording cases; their frame/render cost remains a separate follow-up. Faster Stage9 attack choreography is verified independently from render frame rate.

## Complete revised Stage 9 fight

The full native Furious fight lasts 123.255 seconds and averages 56.79 native FPS while recording. The original 10,965 HP and actual half-health gate lead to native defeat. No HP, attack phase or timer writes occur during filming. Every attack mode appears, including the spinning dash. All five one-shot sound roles play; a separate live sample confirms eight actual starts of the sustained laser bed.
The finished recording measures -19.3 dB mean / -1.5 dB peak, with no page, console, asset or audio-tap errors. It uses the real game mix; no replacement soundtrack was added.
33 native Stage 9 and dialogue checks pass, plus 16 source/asset checks. The archived inputs rebuild pixel-identically offline. The full engine suite completed again with the same five baseline failures listed above.
[Full fight](http://127.0.0.1:51046/?horizon=cyan-1031#clip=stage9-miniboss) · [25 native samples](http://127.0.0.1:51046/audio-speed-1031.html)
