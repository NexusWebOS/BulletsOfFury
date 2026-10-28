# Chronos modular chaingun — October23

Canonical name changed to Chronos in both boss initializers, introductions,
announcements, last words and the post-orbit story. Legacy cronos function/asset
IDs remain stable. Two older regression expectations were updated for the new
spelling; their story/mercy/Earth and silent-arcade checks remain intact.

Mike's explicit modular exception keeps one whole body, one separate rotary
chaingun and foreground grip. Native chainHP/chainMax, independent Retina target,
damage/death and salvage/arsenal owners remain. Gun hit detection now samples
actual rendered module alpha; the Retina center overlaps real barrel pixels.
Actual muzzle is gun cell54,172, pivot54,46 at body socket0,48. Module unit104x208;
body384x512/pivot192,230. Normal/Chromium/red and opaque white-hit partners retain
dark outlines. Gun damage visibly flashes and expires; body/armor damage does not
consume gun HP. Breaking the gun removes its target, stops firing and leaves
Chronos alive with his existing other attacks. Pickup/throw/catch renders remain
authoritative and acquired gun stays equipped through armor activation.

Rotor uses8 actual axial poses, revs during native warning and coasts to rest.
The approved five-bore rotor is conserved using offline perspective-corrected
component rotation. PixelLab's changing muzzle topology and arm-drifting body
animation were rejected. Accepted shaft lighting remains inside the immutable
receiver/outer contour; accepted new two-hand grip is composited into the approved
body without changing his face/core/legs. Selection.json records all choices.
No runtime body/gun/round/FOV rotation, tint, glow, opacity animation or scaling;
existing native mixer/muzzle effects retain their owners.

Native gun passes alternate straight-down moving twin streams and a centered,
stationary fan. Fan uses5/7/9 ordinary mg rounds at Normal/Hard/Furious and5/6/7
volleys per pass, with slower bounded cadence/recovery. Down rakes retain the
native firing gaps and alternating sides. Native warning duration is0.85/0.75/0.65s.
Three preloaded authored FOV colors use fixed cone cells:0.18rad down/0.48rad fan.
All fan rays are downward and symmetric, from the measured muzzle; they are not
shootable missiles. Native eMG supplies one pressure/audio partner per volley,
with silent clones for the remaining rays; sustained hammerChaingun and warning
bossWeaponCharge cues retain the shared mixer/gates.18 native FX-derived direction
cells point along the actual round velocities.

Also fixed real dialogue contention exposed by gun destruction: the5.5s salvage
radio pauses and defers its drawing while a live cinematic owns the frame. Chronos
announcements use one portrait inside the dialogue; the legacy floating duplicate
is limited to its original named cronos scene. Radio resumes afterward.

PixelLab jobs:82cdddc4-d026-43b0-a12b-ff08d7bd1757 (barrel),
39117169-f35c-4fbe-b669-b19f24d64f37 (rejected body motion),
d9c920f4-e2aa-4059-a655-54b6fb335abb (accepted grip edit).
Balance4.59->4.44USD; no top-up.68 fixed exports/19 sheets; all even/no clipping,
binary alpha for actor/rounds and preserved authored alpha128 for warning fields.

Native32/32: name, alternating book, actual downward velocities/sockets,5/7/9
fan counts/angles, ordinary bullet policy, visible traveling bullet pixels,
natural warned releases/stationary fan/cooldown,8 visible spinning rotor phases,
all3 FOV colors, coast-down, separate body/gun/hand blits, actual separate gun
damage/alpha target and white flash expiry, body damage independence, gun break
continuation, matched rage art, portrait name and salvage contention, retained
gun through Chromium, pixel-identical receivers and distinct rotor faces.
Native handoff regression33/33 across Normal/Hard/Furious with/without armor.
No page/asset errors. Required full test_fl final BUILD OK/0errors/actual exit0.
Initial full run failed only the2 stale old-name expectations, now corrected.
Review fixtures prevent player damage and suppress their invulnerability clearing
field to show real bullet travel; this is a controlled animation/combat check,
not a human full campaign or balance playthrough. No commit/push.

Runtime:assets/chronos_modular_1023.js, registered art:chronos_modular_art_1023.js.
Sources/prompts/selection/hashes:_ART_SOURCES/chronos_modular_1023.
Builders/probe:_BUILD_SOURCE/{build,download,install,probe}_chronos_modular_1023.py.
