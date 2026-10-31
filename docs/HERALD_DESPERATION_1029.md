# Herald final desperation — October29

[Watch the focused native sequence](http://127.0.0.1:51046/?herald=desperation-1029#clip=stage8-herald-desperation).

At exactly 20% HP, a final native hit is clamped before defeat: no HP refill or replacement health pool. The real 4264-HP Furious miniboss retains 852.8HP. He sheds any remaining outer modules through native breakup, glows red in protection, rumbles and retreats north offscreen. The reduced skull/core returns in the background, shaking and accelerating its eye/head glow for five full seconds.

The 32-view PixelLab turntable keeps the skull, crown, shoulder sockets and tapered armored spine. It turns in depth while its rotation and skull releases accelerate. Actual Falva roller art supplies the red/black spheres; ten baked sizes grow from 12 to 66px, with 32 rotating glow frames each. Distant balls are harmless visual approach objects. At 65% of their flight they become actual native enemy ordnance, with a growing collision box matching their visible size. Ordinary player bullets cannot erase them.

After eleven seconds of fire, Herald goes north again and returns at full size for a six-second vulnerable foreground window. Surviving that window repeats the final phase, rather than returning to wing attacks. Native part hits, white hit pixels/expiry, element damage accounting, defeat and rewards remain authoritative. Protected targets are absent from Retina and bullet-solid queries. Generic full-sized low-HP smoke is suppressed only while he is protected in this depth sequence. Native smoke/death effects resume in the foreground.

All new rotation, scale, depth, red glow and white-hit art is authored offline in Aseprite: seventeen fixed-cell banks, 48.69MiB decoded. Runtime uses ordinary source-over frame blits, no new image transforms, filters or additive rendering. Sources, editable files, generation IDs, frame selection and hashes live in the asset folder. Rebuild with `_BUILD_SOURCE/build_herald_desperation_1029.py --aseprite <path>`.

## Verification

- 25 focused native engine checks, 18 art checks and 15 film/playback checks pass.
- Final real-RAF Furious film: 117.97s, 58.89 native FPS. Invulnerable input-only Cole bot, Laser5 and actual missiles; no enemy HP, phase or timer writes during recording. Native defeat completes.
- Decoded audio mean -20.9dB, peak -3.8dB. No game/console/asset/audio exceptions. Routine canceled pooled-audio requests are logged separately.
- Syntax checks pass. The full existing suite reaches its summary and exits1 with the same five baseline failures: flash hold; opening dialogue jump warning; opening jump/chromium ordering; opposite StageX persistence; StageX right branch full encounter.

The latest root Herald film and focused desperation chapter are in the local Stage6–9 gallery. Previous tornado, skull, lightning, spellcaster and landing films/chapters are preserved. No GitHub push was requested for this pass.
