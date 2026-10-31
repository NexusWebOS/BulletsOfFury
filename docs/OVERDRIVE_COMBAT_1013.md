# Overdrive combat overhaul — October 13, 2026

Build: `overdrive1013-bastion18-r1` in the existing standalone Ground Operations entry point.

## Playable campaign

| Level | Stage | Pinned password (Yuri / Normal / Hotwire) |
|---|---|---|
| 2 | Iron Infiltration | `OD-237A-5JXL` |
| 3 | Fortress / Dead Signal | `OD-237B-5JXM` |
| 4 | Machinists | `OD-237C-5JXN` |
| 5 | Desert Breaker | `OD-237D-5JXP` |
| 6 | Night Run | `OD-237E-5JXQ` |
| 7 | Prism Bastion | `OD-237F-5JXR` |

Museum is removed from the active campaign; its source art remains archived in the checkout. Old level-5 passwords open Desert Breaker. All six entries are permanently listed in Passwords, while manual entry and pilot selection still work. Completion/unlock logic includes Level 7.

## Controls

The M30 2.4g Genesis receiver has a dedicated physical-button mapping. Its printed A now fires in Prism Bastion and Y throws grenades. Old untouched generic mappings upgrade automatically; custom assignments survive. Night Run uses D-pad steering without redirecting the turret; hold L plus the D-pad for free aim. Face-direction firing, mouse and Retina remain independent.

| Action | Keyboard / mouse | Six-button pad | Standard pad |
|---|---|---|---|
| Prone / crawl in the fortress | F toggle, then WASD | Mode + X, then D-pad | Mode + X, then D-pad |
| Attach to cover | C / Shift near cover | Hold Mode | Hold L |
| Pop out and shoot | J / left mouse at cover | Directional fire buttons at cover | A at cover |
| Protected blindfire | Hold I + J at cover | Mode + Z | L + R + A |
| Truck steering | WASD | D-pad | D-pad |
| Truck free aim | Hold F + WASD, or mouse | Hold L + D-pad | Hold L + D-pad, or right stick |
| Base-stage sidestep | A / D | D-pad left / right | D-pad left / right |
| Base-stage duck | Down / Shift, or F toggle | C / Mode, or X toggle | Down / L, or Mode + X |
| Base-stage free aim | Hold I + WASD, or mouse | Hold Z + D-pad | Hold R + D-pad |
| Base-stage fire | J / left mouse | A | A |
| Base-stage quick side fire | K + A / D | B + left / right | B + left / right |
| Base-stage grenade | U | Y | Y |
| Base-stage blindfire | Hold cover + fire | Hold C / Mode + A | Hold L + A |

The base has no jump shot. Free aim fixes Yuri's position and twists his torso/rifle through five authored directions; the 16-pixel reticle now moves at 480 px/s horizontally and 420 px/s vertically (previously 260/230). B plus left/right immediately selects a new full-profile side-firing pose and shoots; B alone chooses the nearest attacker on Yuri's side. Switching sides fires on the next simulation tick, and releasing B restores the prior Retina cursor. Keyboard bindings can be changed in Options; Help reads the actual saved bindings. Hold cover plus fire to blindfire while crouched. Holding cover during Retina keeps him low. Move sideways while crouching to shuffle along intact wall sections. Cover wears down under bullets, lasers and rockets; broken sections stop protecting Yuri. Shoot incoming rockets and background barrels. Vaulted enemies bypass the wall and must be shot to the sides.

## Movement and cover

The old display-cadence rounding could produce extra simulation ticks under uneven frame delivery. The replacement retains fractional time, caps catch-up, and interpolates rendering at 120/144/240 Hz without changing exact collision state. Deterministic test hooks still render exact current state. Normal boss camera scale stays 1:1.

Vehicle families steer continuously, accelerate/brake, keep modular artwork registered and commit to warned rams. Larger mounted crews, hulls and projected swept hit tests improve visibility and aim reliability. Night Run uses north-edge arrivals, a visible-entry firing delay, and brief hull hit recovery.

Fortress pathfinding now normalizes route vectors before applying speed, removing the large position jumps. Yuri gets authored sidestep, rise/pop-out, back-to-wall blindfire and rear knockback frames. Cover no longer teleports the collision body during peeks. Barrels use authored sprite sockets, and blindfire waits for the raised-rifle pose. New straight concrete bunkers are indestructible. Troops arrive from above the camera, and Gosfer gets a visible filling boss bar.

## Prism Bastion

The latest [eight-room/controller/boss rebuild](OVERDRIVE_BASTION18_1014.md)
supersedes the earlier six-line corridor implementation. Every room has a door
core and mounted corners; Yuri hops the fixed cover, the corridor scrolls forward
and a full black passage leads into the next room. The Master Prism Core now has
spinning lasers, glass damage/shatter and a white-out release of the new64-frame
Helios. Gosfer also has64 new movement/fire/dash/death frames and nozzle sockets.
The M30/Genesis preset and binding capture corrections are in the same guide.

## Verification

Latest [combined evidence](qa/overdrive_bastion18_1014.json):38 focused,5 recovery/
damage and20 M30 checks pass. Full input-only mouse/D-pad Normal runs complete all
eight rooms and both boss forms without a death. All191 new PNGs render natively;
required base suite reaches BUILD OK /0ERRORS/exit0. Controller reports are synthetic.
Prior16/17 reports remain as historical evidence. Local changes; no commit/push.
