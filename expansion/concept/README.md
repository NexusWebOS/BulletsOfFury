# Bullets of Fury — Overdrive concept art

This folder contains the first visual pass for the expansion. These are source concepts for review; no files are registered in the runtime manifest or player atlas.

| File | Purpose |
| --- | --- |
| `overdrive_cover.png` | Expansion graphic with the two new pilots and ships |
| `hotwire_portrait.png` | Hotwire pilot portrait |
| `hotwire_full_body.png` | Hotwire full-body design |
| `hotwire_ship_top.png` | Hotwire top-down ship design |
| `phoenix_portrait.png` | Phoenix pilot portrait |
| `phoenix_full_body.png` | Phoenix full-body design |
| `phoenix_ship_top.png` | Phoenix top-down ship design |
| `hotwire_front_neutral.png` | Hotwire front-facing neutral frame, using the shipped pilot pose/style as reference |
| `phoenix_front_neutral.png` | Phoenix front-facing neutral frame, using the shipped pilot pose/style as reference |
| `hotwire_avatar_box.png` | Earlier portrait-box concept; superseded for the pilot screen |
| `phoenix_avatar_box.png` | Earlier portrait-box concept; superseded for the pilot screen |
| `overdrive_cover_official_logo.png` | Revised cover using the current Bullets of Fury logo as the visual source |
| `overdrive_logo_lockup.png` | Transparent expansion logo candidate |
| `overdrive_word_overlay.png` | Transparent OVERDRIVE wordmark for pairing with the exact existing game logo |

Hotwire is a female pilot with a copper and cyan electrical identity. Her narrow twin-boom interceptor has visible induction coils. Her planned whip attack can borrow elements from the existing fire whip.

Phoenix is a male pilot with a blackened metal and ember identity. His broad strike craft has a central furnace and armored artillery hardpoints. His planned Armageddon attack charges against a ground Retina roughly 100 game pixels north of the player, joined to the player by a generated fire line. Release sends an overhead mortar blast to that target, followed by ground bursts stepping out on both sides. Its explosions need a distinct Phoenix effect family.

The broader expansion plan also calls for Freezer's Ice Wall, Axel's akimbo fire upgrade, eight new levels, a new campaign, and Decker's Fury Tanks entering when air units overwhelm the team by level 4. None of those systems are implemented in this art pass.

Generated art is preserved at its original resolution and alpha. The full-body concepts retain faint lighting behind the figures; isolate and validate those edges before using them as gameplay sprites. The cover has an opaque background.

## Second art pass

The front-neutral frames reference the actual `cinematic_characters/*/poses/01_front_neutral.png` pilots; the avatar boxes reference the `pilot_portraits/*-idle.png` family. They are high-resolution imagegen masters rather than normalized native-size runtime frames. Phoenix's front-neutral master still has faint warm lighting outside the silhouette. Neither new pilot is wired into the game.

The revised cover references the current official `assets/game/ui/logo_0916/bof_logo.png`. For future exact-logo compositing, use that existing logo file unchanged and place `overdrive_word_overlay.png` under it. The transparent combined lockup is a generated visual candidate, so its main logo should not be treated as pixel-identical to the official source.

## Pilot-select avatars

The actual pilot-select lineup draws `pav_<pilot>` from `assets/game/pilots_0922/portraits/<pilot>-idle.png`. Its nine current portraits share the 256x256 armored frame in `assets/game/pilot_avatars/avatar_frame_template_0919.png`. The correct Hotwire and Phoenix candidates are `expansion/pilot_avatars/hotwire-idle.png` and `phoenix-idle.png`. Their new inner portrait art was generated from the approved character identities, then the existing frame was placed on top with the same layout and frame recolor used by `_BUILD_SOURCE/rebuild_pilot_avatars_0919.py`. `expansion/tools/build_overdrive_pilot_avatars.py` reproduces those files. No current pilot portrait was replaced.

Built-in imagegen prompt set: front neutral frames preserve the new pilot identities while matching the existing straight-on, head-to-boot, compact arcade sprites; avatar boxes preserve their faces while matching the shipped square metal-frame portraits; the cover and lockup use the current game logo with a subordinate orange-gold OVERDRIVE title. No procedural or placeholder sprite art was added.
