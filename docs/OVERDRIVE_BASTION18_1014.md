# Overdrive M30 and eight-room Bastion rebuild — October 14, 2026

Build: overdrive1013-bastion18-r1. Existing standalone Ground Operations entry.
Local preview: http://127.0.0.1:8781/expansion/topdown/index.html?fullscreen=0&build=overdrive1013-bastion18-r1
Level7 Yuri/Normal/Hotwire password remains OD-237F-5JXR and is pinned.

## Controller settings

Options → Controller Preset selects M30 2.4G, Genesis6 or Standard. M30 and
Genesis show X/Y/Z above A/B/C, a D-pad and Start/Mode. Only M30 has L/R.
An identified M30 keeps its real six-button diagram even with standard actions.
Genesis learning has12 inputs; M30 learning has14. The shoulderless Genesis
preset uses Mode for tank cruise/free aim. M30 preserves its printed receiver
mapping A/B/C/X/Y/Z=2/1/5/3/0/4. Standardized browser reports stay separate.

The settings capture now runs outside menu navigation/rendering. Keyboard events
capture directly, including fast taps. Pad capture waits for a release and consumes
the newly assigned press so it cannot also confirm/cancel the row. The wizard
accepts mirrored button reports and prefers the requested physical control.
Keycaps show physical letters and D-pad directions. Apply persists and Cancel
restores the complete snapshot, including the chosen preset. User custom bindings
still survive reconnect/reload.

Owners: js/core.js; _research/original_options_adapter_1011.js and
build_original_options_1011.py generate js/original_options_1011.js.

## Eight rooms and the corridor

Rooms1–7 each have troops, a compulsory animated door core and two mounted corner
turrets. Room8 has the Master Prism Core and corner turrets. The simple corridor
shell contains only side walls, floor and ceiling. A separate giant steel back
wall supplies matching door/core/turret sockets. Grimy explosive barrels and
ordinary/armored crates use new authored Doom-inspired damage/explosion states.

An ordinary clear requires troops, the door core and corners to be destroyed,
and the final elite capsule to be collected. Transition phases are blast1.0s,
hop0.75s, walk1.65s, black0.5s and emerge0.7s. Yuri jumps while cover stays fixed.
Forward perspective then enlarges cover until it passes the camera; the wall
never sinks to let him through. Floor/ceiling/side walls approach the camera,
then the entire scene including HUD reaches black before the next room fades in.
Combat scale stays1. Dead rear fixtures vanish with the wall; whole connected
source rows prevent a previous-row rubble strip from appearing over the breach.

## Bosses

Master Prism Core:8 rotating contained-face states,4 glass-fracture states and
4 glass-shatter/energy-release states. Three authored animated laser rays rotate
and sweep the player's lanes, with dim warnings and bright active phases. Cover
absorbs a sweep while crouched. Destroying containment cracks and bursts glass,
then expands to a full-screen white-out. Inputs/damage pause during transformation.
The light fades to reveal Helios and its orange-then-fire-red filling gauge.

Helios has64 new authored frames in eight8-frame walk/run/idle/throw/lightning/
jump/hit/death banks. Travel distance drives locomotion; returning uses walking
and the lateral assault uses running. Prism volleys, lightning and geyser slams
remain. Death in room7 restores room7; death after transformation restores Helios.

Gosfer has64 new authored frames:8 walk phases for each cardinal orientation,
front/side rifle-fire, lateral dash and backward fall. Firing stays attached to
the animated rifle and actual measured nozzle. His bar now shares the top HUD
instead of covering his head, and the fight movement keeps the full figure visible.
Arena health/attack/reflex systems remain, with modest vertical positioning for
the larger figure. Protected native rifle shots defeat the updated boss.

## Art and QA

art/bastion18 holds191 unique exported PNGs /193 registered keys /28 banks,
plus16 original/edited source sheets, exact prompts, and references. All final
cells have even dimensions, shared bank geometry, common proportional scales,
registered pivots and binary alpha. build_bastion18.py owns its manifest.
The older16/17 packs remain for infantry/player effects and provenance.

Evidence: [combined QA](qa/overdrive_bastion18_1014.json).
Focused38/38, recovery/muzzle/damage5/5, M30 mapping20/20; zero browser errors.
Full Normal mouse route132.083s:33kills,1damage,0deaths. D-pad route142.750s:
33kills,2damage,0deaths. Both complete all8cores, seven full passages, six elite
drops and both boss forms using input only. Native galleries show every new key.
Required base suite completed BUILD OK /0ERRORS/exit0. Changed JS syntax passes.
M30 reports are simulated; automated aiming is not human difficulty feedback.

## Reference provenance

- [8BitDo M30 product reference](https://www.8bitdo.com/m30-2-4g/) and [manual](https://download.8bitdo.com/Manual/Controller/M30-2.4g/M30_2.4g.pdf).
- [Classic Doom object sprite reference, rip credited Falcon Delta](https://i.pinimg.com/474x/30/93/83/309383ed1c95a115f65f97bc5b96f802.jpg).
- [Tron MCP visual reference](https://i.pinimg.com/originals/f7/f4/14/f7f41438a2be70883f1115149b680211.jpg).

These are retained under source/references for visual provenance. The runtime
uses the new generated BOF assets. No commit or push.
