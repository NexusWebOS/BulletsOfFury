# Missile supplies — September 14, 2026

Missile crates previously followed the stage clock and stopped restocking during
boss encounters. Every live boss, miniboss and arsenal miniboss now gets an
encounter supply clock: first supply after seven seconds, then every eighteen
seconds. One live missile box/pickup is shared across overlapping encounters.
Entrance/death states and a dead player do not advance restocking. Hard/Furious
restock frequency increases 25 percent.

Stage 1–7 rolls x5/x10/x20 (50/30/20 percent); stage 8 rolls x50/x100 equally.
Stage 9 quantities are unspecified: retain small x5/x10 supplies for now.
Old x2 pickups migrate to x5. The authored x5 graphic now grants five rounds
instead of three. Retired x35 art/collect support and cinematic grants are kept
for legacy data, without ordinary x35 RNG.

Real fodder kills have a ten-percent chance of scattering one missile, or two
on a quarter of successful drops. Hard/Furious increase this chance 25 percent.
Their own pilot-colored projectile art spins while the pair separates.
Collection grants one actual manual-ammo round. Repeated death handling cannot
repeat the roll. Bosses, minibosses and destructible props are excluded.

Super/Ultra/Uber upgrades, their authored icons/boxes, wave gates and tier ammo
caps remain pending. This batch does not alter passive homing missile upgrades.

Syntax passes. Full suite **3,745 passed / 61 failed, exit 1**, final summary
reached, all names match docs/qa/stage_1_5_0914.json. The sand-tank random assertion
failed again after passing the preceding run. Twelve section-301 checks pass.
Native Chromium **11 / 0**, zero errors; actual hull destruction, spreading,
rotated drawImage pixels, boss/miniboss restocking and ammo collection verified.
Art inspected through XART/game context, with LF runtime/CRLF tests preserved.

Proof: docs/qa/missile_supplies_0914.json.
Sources: _BUILD_SOURCE/missile_supplies_0914/.
Screenshots: _shots/missile_supplies_0914/.
No atlas changes, commit, push or deletion of user data.
