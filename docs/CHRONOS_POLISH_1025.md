# Chronos gun and charge readability â€” October 25

Authorized follow-up to all three recorded fight recommendations.

- C29 firing interval/heat and C31 actual rotor ramp now reach maximum at 4 firing seconds. Existing 5-second damage protection is unchanged.
- C37 multiplies the initialized native chaingun HP/max by 3 (Furious 230 â†’ 690). It remains Retina-targetable and only its real exhaustion ends firing.
- Native markHit body feedback lasts 65 ms with a 420 ms retrigger interval. Armor and gun flashes also use 65 ms; existing gun gate remains. White hit art is unchanged. Damage, shield absorption and stun ownership remain native.
- During chromium/hammer/rage charging and rage depth/gather/warning/release, new asteroid/comet stream arrivals and timed armory/missile supplies pause. Regular crate requests queue and resume at most once per two seconds outside these states. Existing objects retain movement, collision, collection and rewards; backdrop/FOV clocks continue.

Owner: assets/chronos_polish_1025.js after C36. Existing C29/C31 ramp divisors changed together. No changes to assets/game.js or test_fl in this task.

Verification: native Chromium 10/10, including actual damaged pixels, restored palette, the unchanged protection boundary, RPM at four seconds, deferred/resumed supply, and no browser errors. Syntax checks pass. Required test_fl exits 1 before assertions/final summary because retired_art_archive_1022.cjs is missing (existing blocker).

Full recording and delivery measurements are in docs/qa/chronos_polish_video_1025.json. Capture uses real-time native inputs, Furious, Cole, level-5 Fusion starting loadout, and labelled invulnerability. No HP or phase injections. No commit/push.

Recorded result: {"full_speed_at_firing_seconds": 4.099999999999991, "full_speed_hp": 690, "gun_max": 690, "first_damage_at_firing_seconds": 5.3833333333333195, "destroyed_at_firing_seconds": 10.100000000000081, "after_first_damage_seconds": 4.864700000017876, "deferred_crates": 3, "video_seconds": 318.5413000000119}. Delivery 8/8; all seven ElevenLabs routes played. Native and decoded contact frames inspected. No game/page/console errors.
