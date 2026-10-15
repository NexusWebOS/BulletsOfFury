# Overdrive GitHub publication — October 13, 2026

Mike requested publishing the current Overdrive work. Target: `main` at
[NexusWebOS/BulletsOfFury](https://github.com/NexusWebOS/BulletsOfFury).
Before publication, `origin/main` was fetched and reviewed at `4c3f7b26`;
there were no incoming commits or divergence.

## Release contents

- Level 3, **Fortress / Dead Signal**: destructible cover and relays, wall peeks,
  on-foot Retina, unlimited assault rifle, finite upgrade weapons and Gosfer.
- Level 6, **Night Run / Hull Zero**: Hotwire drives the green Silverado;
  150 seconds of turret defense, interceptable rockets, gun trucks, robots and
  late red elites. Hull destruction restarts the run; there is no boss.
- Jackal, Lancer, Manticore and Bastion enemy tanks in the existing tank stages.
- Yuri's authored eight-direction action sprites, followed by **316 new motion
  frames in 24 banks** for walking, firing while moving and crawling. Animation
  follows actual movement, preserves firing phase and settles when blocked.
- Campaign progression, compatible passwords, help labels and fullscreen
  launcher updated for build `overdrive1013-yuri-motion-r1`.
- Generated source art and prompts, owning export scripts, manifests, animation
  viewer, native probes, screenshots and portable verification records.

## Verification

Completed against the release gameplay before the publication documentation:

| Check | Result |
| --- | --- |
| Latest Yuri movement/art/viewer Chromium probe | 26/26; no browser or asset errors |
| Assault Chromium probe, rerun after the motion revision | 38/38; no browser or asset errors |
| Required base regression suite | 8,700 passes; 0 errors; final summary; exit 0 |
| Earlier real-input fortress route probe | 20/20 |
| Earlier controller / Retina / Warrior regression | 40/40 |

Publication checks also passed: 31 JavaScript syntax checks, all 834 registered
art assets and 41 entrypoint dependencies present in the Git index, and a
CRLF-aware staged whitespace check. Original file line endings are preserved.

All 316 new motion exports were inspected through the game's native art
renderer. Controller checks used simulated pad input; these results do not
claim a physical-controller or human difficulty playtest.

QA records: [latest motion](qa/overdrive_yuri_motion_1013.json) and
[initial assault](qa/overdrive_assault_1013.json). The latest record's
`localOnly` field describes the verification snapshot before this publication.
Full controls, passwords and stage details: [Overdrive assault notes](OVERDRIVE_ASSAULT_1013.md).

The publication scope is Overdrive and its handoff, documentation and QA files.
Other local projects, private configuration, raw sound imports and ignored
scratch files are outside this release.
