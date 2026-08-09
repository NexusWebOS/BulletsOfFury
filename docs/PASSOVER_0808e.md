# PASSOVER — drop 0808e   (THRUSTERS TO SPEC)

Build: `BulletsOfFury_0808e`
Harness: **2,246 assertions / 206 sections / 0 failing**, twice, reaching the banner.

---

## 1. MIKE'S SPEC, PILOT BY PILOT

    axel        1, centre        (was 2 on the sides)
    cole        2, twin          measured off the hull by nozzle brightness, +/-0.15
    decker      1, centre        already correct
    falva       1, centre        (was 2)
    freezer     1, centre        (was 4)
    juggernaut  3                a centre plus a measured pair
    lizzie      1, centre, FLIPPED and tucked under the tail
    maverick    1, centre        (was 2) — "maverick gets one, not double"
    yuri        1, centre        (was 2)

## 2. ⚠ WHERE THE OLD MOUNTS CAME FROM

The rig carried its own mount list that put FIVE pilots on twin plumes, at fractions I could not
trace to any measurement in the codebase. **Maverick's pair landed at +/-0.165 of hull width —
under his outboard wing roots, not his engine.** That is precisely what he saw as "doubling them
up on maverick", and it was never going to look right because the flames were not where the
exhausts are.

Measuring the hulls confirmed it: Maverick's real nozzle is a single cluster 0.244 of the hull
wide at dead centre; the things at +/-0.45 are fins.

## 3. TWO SIZING FAULTS FIXED WITH IT

**The plume was sized off SHIP HEIGHT** at 42%, so on a narrow airframe the flame came out wider
than the aircraft. It scales to a per-pilot fraction of HULL WIDTH now — the engine it comes out
of — carried in the same table.

**Lizzie's reel points the wrong way.** Hers is a warbird flame, not the four-pointed star burst
the other eight use, so a blanket draw had it firing into the fuselage. Flipped, and tucked under
the tail as asked.

The table lives in `assets/data/thruster_mounts.json` and is embedded as `THRUSTER_MOUNTS`.
Twenty-seven assertions pin it: the count per pilot, that every "centre" pilot is actually within
0.02 of the centreline, that Cole's twins straddle it, that Juggernaut's three are a centre plus a
pair, that Lizzie is flipped, and that every plume is scaled to its nozzle.

## 4. THE CALL HE ASKED ME TO MAKE

*"If your going to use this thruster system, then we delete and do not use all frames with
thrusters built in anymore. Your call as you say."*

**Yes — commit to this system.** One reel per pilot on measured mounts is the only version that
stays correct when art changes: a hull with flame baked in cannot be re-mounted, re-scaled,
flipped or switched off, and having both is why they have been fighting each other.

⚠ **I have NOT deleted the baked-in frames yet.** That needs identifying exactly which ship frames
carry flame before anything is removed, and I want that as its own verified pass rather than
folded into this one — deleting hull art on an assumption is how the roll frames got damaged.

## 5. STILL OPEN

    the baked-in thruster frames — identify, then delete
    mfx_ (252 cells) — the unconfirmed deletion
    the helix ball · stage 1 transition · menus backable by keyboard · fireorb icon on level 3
