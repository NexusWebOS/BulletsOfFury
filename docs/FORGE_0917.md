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

Controls: LEFT/RIGHT walk the boxes · UP/DOWN swap the slot's weapon · FIRE combine (opens the
element row; FIRE again picks, BACK cancels) · CHARGE re-spec · START continue. A click acts as FIRE
on the current selection.

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
