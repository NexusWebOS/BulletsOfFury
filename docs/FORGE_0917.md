# THE FORGE — the screen between the debrief and the next stage (0917)

Mike, 0917: *"I wanted to see the in between stage screen of weapons being unlocked, weapons being
combined, etc. how this system and set works before your next level. You should be allowed 2
combinations in between each level, and this upgrade permanently takes over your weapon style until
you reset it via re-spec, which unlocks the next level as you get 2 re-specs per level completion.
Additionally, as you unlock more weapon types or are about to go to level 2, we should limit the
amount of weapon types that can spawn to 6 per level, and make the player select their "loadout"
including their new upgraded weapon type replacing the weapon type it was I.E machine gun now
becomes incendary slugs/machine gun or something fitting of name."*

Reel: `_shots/forge_0917/BulletsOfFury_Forge_0917.mp4` (the `_compact` beside it is the sent one).
Probe: `probe_forge_0917.py` **32/0**, real key taps, 0 errors. Suite section **370**.

## Where it sits

```
STAGE CLEAR (debrief)  →  NEW WEAPONS UNLOCKED (if the stage has a row)  →  THE FORGE  →  next stage
```

The exact order the 0916 concept note wrote down. Each page runs the next from its own CONTINUE and
the stage exit is still the one function (`scLeaveStage`). The Forge opens only when there is
something to do on it — an element discovered, a weapon forged, or more weapons unlocked than the
loadout holds — otherwise it skips itself the way the unlock page does. An empty page teaches mashing.

## The rules, as built

| rule | value | where |
|---|---|---|
| combines per stage clear | **2** | `FORGE_COMBOS_PER_STAGE` |
| re-specs per stage clear | **2** | `FORGE_RESPECS_PER_STAGE` |
| weapon types that may drop per stage | **6** | `FORGE_LOADOUT_MAX`, applied in `crateWeaponPool()` |
| what can be forged | MG, spread, missiles, laser, orb, chaingun | `FORGE_WEAPONS` — the slots whose rounds are infusion carriers |
| what cannot | flamethrower, laser mist, lightning orb | their rounds are not carriers; the box says CANNOT TAKE AN ELEMENT |
| which elements are offered | the ones you have **collected in play** | `run.forgeElems`, written by the real `infuse` pickup path |

**A combine** puts an element on a weapon permanently (`run.forge[slot] = {elem, lv}`). The same
element again levels it — L1 → L2 → L3, and L3 is the named combination (FIREBURST, GODS WRATH…).
A different element *replaces* it at L1: that is "takes over". **A re-spec** removes it. The weapon's
name changes with it, everywhere the bare name went: the HUD, the pickup banner, the debrief's
WEAPON OF CHOICE.

**Permanent** means: it is asserted every time that weapon is equipped, at every stage start, and
after a death — the death reset still clears the in-play element and the forge puts its own straight
back. In-play pickups still work on top of it for the stage (a boost, a fusion), the forge is the
floor.

**The loadout** is the six weapon types the crates may drop. While six or fewer are unlocked it is
simply all of them; once more are unlocked (the chaingun, laser mist, Yuri's orb) UP/DOWN on a box
swaps it for an unlocked weapon that is not in the loadout. The crate bag is rebuilt at stage start so
the new loadout takes effect at once.

All of it rides the campaign save (`forge`, `forgeElems`, `loadout` — optional fields, `CAMP_SAVE_VER`
untouched) and a new run starts bare.

## The names

`FORGE_NAMES[element][slot]`. Mike's own example is the first row.

|  | MACHINE GUN | SPREAD | MISSILES | LASER | ORB | CHAINGUN |
|---|---|---|---|---|---|---|
| fire | INCENDIARY SLUGS | NAPALM FAN | HELLFIRE RACK | INFERNO BEAM | MAGMA ORB | INFERNO GATLING |
| ice | CRYO SLUGS | SHARD FAN | FROSTBITE RACK | CRYO BEAM | GLACIER ORB | HAIL GATLING |
| lightning | VOLT SLUGS | ARC FAN | STORM RACK | TESLA BEAM | THUNDER ORB | STORM GATLING |
| prism | PRISM SLUGS | SPECTRUM FAN | PRISM RACK | LUMINAIRE BEAM | PRISM ORB | PRISM GATLING |
| toxic | VENOM SLUGS | ACID FAN | BLIGHT RACK | DECAY BEAM | PLAGUE ORB | VENOM GATLING |
| kinetic | SONIC SLUGS | SHOCK FAN | IMPACT RACK | GIANT BEAM | KINETIC ORB | HAMMER GATLING |
| chrome | MIRROR SLUGS | CHROME FAN | MIRROR RACK | CHROME BEAM | MIRROR ORB | CHROME GATLING |
| water | TIDAL SLUGS | GEYSER FAN | TORRENT RACK | HYDRO BEAM | WATER ORB | TORRENT GATLING |
| dark | VOID SLUGS | VOID FAN | VOID RACK | VOID BEAM | VOID ORB | VOID GATLING |

No apostrophes — this face has no usable one at UI size (0912b).

## The screen

Built on the debrief plate in the debrief's language: the six loadout boxes are the plate's own RANK
bay cut and repeated (the construction Mike approved for the unlock page), the element row sits on the
plate's word strip, every string goes through the stage face. Layout is data (`FORGE_ROWS`) so a
bespoke plate later is a constant change. `docs/marketing_0916/forge_concept_a.png` remains the
concept plate.

Controls (0917, second cut): LEFT/RIGHT walk the boxes · FIRE / UP / DOWN on a box open the WEAPON
LIST for that slot (UP/DOWN scroll it with a ding per row, FIRE picks the highlighted weapon into the
slot and goes on to the element row when it can take one and a combine is left, BACK keeps what was
there) · on the element row LEFT/RIGHT pick, FIRE combines, BACK cancels · CHARGE re-spec · START
continue. A click acts as FIRE on the current selection. The MISSILES slot never opens the list.

## Three things this build settled, none of them by reading

- **Nothing is invented for the round.** A forged weapon runs through the existing infusion system —
  `forgeApply` writes `run.infusion`, and the stamp, the palette, the on-hit effect, the EQUIPPED badge
  and the level-3 names are the 0917 machinery unchanged. The Forge is a surface and a rule set.
- **`chaingunUnlock()` EQUIPS the chaingun** (it is the stage-5 reward path). The probe called it to
  widen the pool and the held weapon became slot 7 for the whole run, so the MG's element had no gun in
  hand to apply to — five assertions failed on a build that was right. Take the unlock, put the hand
  back on the machine gun.
- **A blind second press left the Forge before a frame of it was filmed.** After 5.5 s the debrief is
  fully revealed, so ONE press exits it and opens the Forge; the capture's unconditional second press
  was the Forge's own CONTINUE. `forgeVisible()` was true the whole time (measured at the debrief). Tap
  until the state changes, never a fixed count.
- The element strip has to be at least as tall as the paint it stands on: the plate's bottom stat pair
  and the rank bay's foot peeked out around a strip sized only to the badges. Same trap the unlock page
  hit.

## Open, for Mike

- Mouse: a click acts as FIRE on the current selection; there is no pointer hit-test on the boxes yet.
- Whether an in-play pickup of a *different* element should be allowed to displace a forged one for the
  rest of the stage (it does today, as a temporary fusion), or whether the forge should be exclusive.
- The concept plate (`forge_concept_a.png`) as a bespoke background instead of the debrief plate.

## Second cut (0917, later the same day): the picker, the forged badges, the deadly boom

Mike: *"the forge, when I select a weapon slot, should become like a scrollable list I can select
and ding's with each icon. Missiles is a slot that remains Missiles and will never not be missiles. I
wanted weapon icons of each type after being upgraded with our element type, generate those. I also
need Cole's Sonic Wave/Boom to be upgraded and feel/sound and work like a deadly sonic sound attack."*

**The picker** (`forgePickerDraw` / `forgePick`, `F.row===2`). Selecting a box opens a scrollable
list of every unlocked weapon - icon, name, and where it sits (`IN THIS SLOT` / `IN SLOT n`) - four
rows in view (`FORGE_PICK_VIEW`), drawn scroll arrows (the face has no triangle glyph; a lettered arrow
is an invisible affordance). A pick into a slot that already holds another weapon SWAPS the two, so the
loadout can never carry a duplicate. `FORGE_FIXED={2:1}`: missiles are in every loadout and their box
refuses the list (`MISSILES STAY MISSILES`), going straight to the element row when an element can
be combined. A weapon that could take an element but has no combine left says `NO COMBINES LEFT THIS
STAGE` rather than the list silently closing - a silent return reads as a button that did nothing.

**The forged badges** are 54 generated plates, `assets/game/ui/forge_0917/micon_forge_<elem>_<slot>.png`
(9 elements x slots 0/1/2/3/5/7), one 3x3 sheet per weapon generated against the authored badge strip
(`docs/proofs/forge_icons_0917/ref_*.png`, uploaded as the reference asset) with a STRICT prompt - every
cell the same frame, the same emblem, the same `I` tag, only the element changing. `weaponIconKey`
answers `micon_forge_<elem>_<w>` for a forged slot on every surface - the Forge boxes, the picker, the
HUD, the EQUIPPED box, the falling crate - and only when the plate is registered, so a missing sheet
keeps the tier icon instead of drawing a hole.
- ⚠ **The RAW render is what gets cut** (`forge_icons_slice_0917.py`): the pixel_url is a 200px downscale
  of nine badges. The raw is on WHITE, so cells come from the sheet's own gutters, the white is punched
  by a flood from each cell's BORDER (a global sweep pinholes the chrome and ice badges), and the
  surviving rim fringe is converted to a dark edge, never deleted.
- ⚠ **Two of the first three MG sheets lost the gun** - the emblem drifted into a generic crystal or the
  tag vanished on half the cells. "Every cell contains the SAME ... emblem, never omit it" in the prompt
  is what held; read every cell before slicing.
- ⚠ **The reference strip's frame colour leaks**: the orb's first sheet came back with the reference
  badge's GREEN frame on every cell (it is a tier-3 badge, and tier 3 is green). The second variation
  keyed the frame to the element; pick by frame, not just by emblem.
- ⚠ **The chaingun is the EIGHTH weapon and `forgeLoadoutSync` fills six in pool order**, so a probe
  that forges slot 7 and expects a box for it measures 0 blits on a build that draws it perfectly. Put
  it in the loadout first.

**Cole's boom** (`probe_sonic_0917.py` 12/0, suite section 371): the dedicated release cue used to be
built into a local and NEVER CALLED; a full charge now asks for `coleSonicFull` and a partial for
`coleSonicHalf` (two new gated cues, `_BUILD_SOURCE/sfx/sonic.json`, TAME rows with retrigger gates).
The wavefront is the Razorback's authored pressure arc `rzb_sonic_wave` rotated to lead upward, a
release ring (`rzb_sonic_ring`) grows off the hull, `SONIC_DMG` 7 -> 11 (a full charge is 26), the
camera kicks with the charge, and the wave SHOVES ordinary hulls back up the screen as it pierces
(`e.y -= 6 + 14 x charge`). Set-pieces and tanks are not shoved.
- ⚠ A prompt whose subject is inherently low-frequency comes back as pure bass and the generator's
  impact gate refuses it; naming the bright transient first is what passed both cues (0912j's lesson,
  reproduced).

Probes: `probe_forge_0917.py` 40/0, `probe_forge_icons_0917.py` 16/0, `probe_sonic_0917.py` 12/0.
Reel: `_shots/forge_0917/BulletsOfFury_Forge_0917.mp4` (`capture_forge_0917.py`, the picker grammar).
