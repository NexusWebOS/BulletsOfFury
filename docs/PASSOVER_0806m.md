# PASSOVER — drops 0806b through 0806m

Build: `BulletsOfFury_0806m`
Harness: **2,063 assertions / 185 sections / 0 failing**, and verified to REACH THE END rather
than crash — see §3.

Mike: *"the game is currently incredibly broken."* He is right, and the largest cause was mine.

---

## 1. THE VANISHING — CAUSE FOUND AND REVERTED

> "everytime I shoot or an enemy appears, I either vanish, the game starts vanishing, enemies
> vanishing, appear out of nowhere ... attacking the mini bosses and bosses also made the entire
> games effects and me and the hud disappear."

That symptom — things stop drawing PART WAY THROUGH a frame, including the HUD — is a thrown
exception mid-render, not a missing sprite. Everything queued after the throw never draws.

**It was the 0806a enemy sheets.** Enemy keys resolved to a DESCRIPTOR object
(`{__sheet, __r:[sx,sy,sw,sh]}`) which a wrapper on `ctx.drawImage` expanded into a source-rect
blit. That works — on `ctx`.

**This file creates twenty-six 2d contexts.** Offscreen compositors, the de-key pass, flamePair,
the tint helpers. A descriptor reaching any of the other twenty-five is not a CanvasImageSource,
so the real browser throws `TypeError` where my headless probe accepted it without complaint.

Reverted in full: `ecells` and the nine `nes_` sheets de-registered, the `_touch` hook removed,
the `drawImage` wrapper removed. All 459 source enemy files were still on disk — the atlas only
ever added — so the revert is clean and the manifest verifies at **9,537 keys / 0 broken paths**.

### Why the harness did not catch it
My fake `drawImage` accepted any argument. The real one does not. **A probe that is more
permissive than the browser will certify a build the browser rejects** — that is the lesson, and
it is worse than the bug. The sizing work in 0806a was sound and the sheets are kept; the
delivery mechanism was not. Redoing it means explicit source-rect blits at the enemy draw sites,
the way `drawBoxPillCell` already works, instead of smuggling a fake image through XART.

---

## 2. THE THRUSTERS — THE ART IS NOT A PLUME

> "those fake thrusters are duplicated, dont look right in the cinematic scene"

Two separate faults, one of them a bad assumption I never checked.

**`nthp_` is not an exhaust plume.** Measured: it is a four-pointed STAR/burst. Its frames are
also 81x102, 136x158, 170x192 and 81x135 — wildly different canvases — so cycling them makes it
jump in size instead of flickering. I built a careful per-frame anchor rig in 0805j for a sprite
that depicts the wrong thing.

**And 0805j stacked a second copy on it.** The "hot core" pass drew a narrower copy over the
plate on its own clock. On a real plume that reads as depth; on a star it reads as a second
thruster. That is the duplication. **Removed** — one pass now.

The per-frame ANCHOR and ANGLE from 0805j are kept, because those were measured against the hull
and are correct regardless of what the sprite depicts.

⚠ **The real fix is the request I mis-read.** Mike asked for *"the ship graphics we have with
thrusters, make thruster pixels glow and transform to appear moving"* — light the exhaust pixels
ON THE HULL, not paste a separate sprite under it. That is a different build and it is written up
here rather than bodged in during a revert.

---

## 3. THE SUITE CRASHED AND REPORTED SUCCESS — AGAIN

After the revert the suite read `2,014 ok / 0 fails`, which looked fine. It had actually thrown
on `Object.keys(BOFX.ecells)` in the assertions I added in 0806a and never reached the end.

This is the third time this session that a crash has masqueraded as a pass. The count and the
final banner are both checked now, and the obsolete assertions are replaced with one that records
why the sheets are absent.

---

## 4. STILL BROKEN — NOT TOUCHED THIS PASS

The revert was the priority; these are all still open and I have not started them:

* **Jets flying south but facing sideways.** Reported since the first session.
* **Maverick's helix orb still has the laser attached**, and on burst it should fire that laser
  out as a spread/volley. Never built.
* **Miniboss does not slow or show a shield.**
* **Stats screen alignment.**
* **Campaign map** — move the scroll hint to the bottom of the screen.
* **Fire boss** — a stray red box; no looping lava corridor before his intro; he is spawned
  above the visible area so neither he nor the intro can be seen.
* **Ice level froze** after dying at the miniboss — no input accepted, could not continue.
  This one is a hard lock and should be next.
* **Fireball fires ice shards instead of fire projectiles.**

## 5. WHAT I WOULD DO NEXT, IN ORDER

1. The **ice-level freeze** — a hard lock beats everything cosmetic.
2. The **fire boss spawning out of bounds** — an unwinnable stage.
3. **Fireball firing ice** — likely a one-line family mismatch.
4. Then the visual list.


---
---

# DROP 0806c — FIREBALL, AND WHAT THE ICE FREEZE TURNED OUT TO BE

## 6. THE FIREBALL SPRAYED ICE — FIXED

> "Fireball - spins and works, but its shooting ice shards instead of fire projectiles"

`orbIsFire()` was wired into two of the three places it needed to be. Drop 0801fs gave it the
orb's ELEMENT (`attackElement` returns 'fire' for kind 'shard' on stage 3) and the ORB's own
art. **The shards the orb sprays were never included.** So the ball burned correctly and then
threw ice crystals out of itself — on the ice level — with a cyan glow. The data said fire and
the picture said ice.

The shard draw is hardcoded to `nio_<lv>_*`, `iceshard_*` and `ice_shard`. It now checks
`orbIsFire()` first and uses **`nfb_fl<lv>_*`** — the fireball pack's own per-level flame reel,
which is the direct counterpart to the ice pack's `nio_<lv>_*`, same shape of asset. That is the
art that was always meant to be there.

Measured over 8 seconds of firing:

    stage 3   fire art 9 keys drawn, ice art 0     orbIsFire true
    stage 5   fire art 0,          ice art 14      orbIsFire false

## 7. THE ICE FREEZE — I CANNOT REPRODUCE IT AFTER THE REVERT

Driven properly through the REAL frame loop — reach the glacier-rail miniboss, die with zero
lives — the state goes `play -> continue -> gameover` correctly, and `drawContinue` advances on
its own countdown. The same test passes on stage 1.

I do not think there was a separate ice bug. **The descriptor throw from 0806a fired on every
frame that drew an enemy**, and the loop's own try/catch swallows it and reschedules — which
presents as a picture that never updates and input that appears dead. That is a frozen game
with no error, and the ice level is enemy-dense.

Recording it as UNCONFIRMED rather than fixed: it needs a retest on this build. If it still
locks after the revert then it is a real second bug and I have not found it.

⚠ Worth noting for whoever reads this next: the loop's try/catch is what turns "one bad draw"
into "the whole game appears frozen". It is the right call for shipping — a thrown frame must
not kill the run — but it also means a persistent throw is INVISIBLE. A once-per-second
`console.warn` of the caught error would have found the 0806a bug in seconds instead of a full
session.

## 8. STILL BROKEN — UNTOUCHED

Unchanged from §4: jets facing sideways, the helix orb laser and its burst volley, miniboss slow
and shield, stats-screen alignment, the campaign map hint position, and the fire boss spawning
out of bounds with no lava corridor before his intro.

**The fire boss is the next one I would take** — an unwinnable stage outranks the cosmetic list.


---
---

# DROP 0806d — THE STAGE-3 ORB IDENTITY, AND THE THAW

## 9. THE PICKUP WAS LYING ABOUT WHAT IT WAS

> "ensure on stage 3 when I open a powerup box that the iceorb doesnt spawn on this level, you
> spawn the fireball instead ... and for freezer, the fireiceball. remember they are their own
> attacks, with their own floating icons that we had."

The BEHAVIOUR was already right and had been since 0801fn — slot 5 dispenses the fireball on
stage 3 rather than the slot being removed, and `orbIsFire()` flips its element and its art.

**The ICON was never updated.** `weaponIconKey` returned `micon_iceorb_*` for slot 5
unconditionally, so on stage 3 the box dropped a fireball **wearing an ice-orb icon**, and
Freezer's charge orb wore it too. The pickup told the player the opposite of what it was.

All three icons already existed and were simply unreachable:

    micon_fireorb_1..5       the fireball
    micon_thermoshock_1..5   Freezer's fire/ice ball
    micon_iceorb_1..5        the ice orb, everywhere else

Freezer is tested first, because on stage 3 he gets his own charge weapon rather than the plain
fireball — `freezerOrbCharge()` already gated on `orbIsFire() && weapon 5`, so the icon now
agrees with the weapon he actually receives. Verified:

    yuri    st3  fireorb        freezer st3  thermoshock
    yuri    st5  iceorb         freezer st5  iceorb
    freezer flamethrower slot -> icebreath on EVERY stage (his kit, not a stage rule)

## 10. THE THAW — SHIP FIRST, THEN THE GRIN

> "their ships narrate ... about their ice coolant systems being useless ... then our characters
> portrait swaps to them smiling and making a comment about how the enemys going to experience
> what its like to get burned."

Two beats in one panel. The ship speaks first **with no portrait** — it is the airframe talking,
not the pilot — and then the portrait cuts in on `port_<pilot>_smile` for the payoff. The swap is
the joke, so the box holds across both beats rather than closing between them.

`port_<pilot>_smile` already existed for all nine pilots, alongside anger/laugh/sad/victory/crash.
Nothing new was drawn.

Freezer branches as asked. Holding the flamethrower he skips the coolant gag entirely and goes
straight to *"They're about to learn why they call me FREEZER."* Without it he gets a two-beat
version acknowledging the cold is already doing his job for him.

It respects the story system's own **Rule 1 — "never hold the player in a dialogue box during
active bullet patterns."** Nothing pauses, nothing is modal, the panel sits bottom-RIGHT clear of
the ship on entry, and any fire input dismisses a line early (Rule 4). Half the select-card scale,
as specified.

## 11. ⚠ A CRASH THE PROBE CAUGHT

The panel first used `F(11)` for its font, copying a pattern from elsewhere in the file. `F` is a
LOCAL in two unrelated functions, not a global helper — so `thawDraw` threw `ReferenceError` the
moment it ran. In the browser that is a thrown frame on every frame of stage 3, which is the same
signature as the 0806a bug. Caught before shipping this time because the panel was exercised
directly rather than assumed.

## 12. STILL OPEN

Unchanged: jets facing sideways, the helix orb laser and its burst volley, miniboss slow/shield,
stats-screen alignment, the campaign map hint position, and **the fire boss spawning out of bounds
with no lava corridor** — still the next one I would take.


---
---

# DROP 0806e — THE BOSSES WERE FIGHTING OFF-SCREEN

> "he also is not visible on screen when he does that, its like you placed him way too high out
> of bounds for me to see. the intro was not even viewable either."

## 13. MEASURED — AND IT WAS EVERY MECH BOSS, NOT JUST THE FIRE ONE

    boss             y      bottom edge     play area starts at y=46
    magmacolossus  -120         24          NO
    cryobehemoth   -120         24          NO
    warhawk        -120         24          NO
    damkeeper       110        175          yes   <- the only visible one, and it is not a mech

They all spawn at **y=-120 with ty=120** and never move. Magma's top edge sat **310px above the
top of the play area**. He assembled himself, announced his name and fought there.

## 14. TWO SEPARATE RETURNS, BOTH ABOVE THE DESCENT

The entrance lerp lives in an `if(b.enter)` block in `updateBoss`. Nothing mech-shaped ever
reached it.

**The mech branch** set `b.enter = true` and then `return`ed — from a point ABOVE that block. And
when assembly completed, `mechUpdate` set `b.enter = false` directly. So the flag was raised and
cleared without the thing it gates ever running once.

**The genesis branch returned even earlier**, and `genesisUpdate` never touches `b.y` at all — it
only drives its own rise/drop/grab/carry phases. So Magma and Cryo played the full 12.9-second
intro three hundred pixels above the screen.

Both branches now run the same lerp, with the same 3.5s hard timeout every other entrance uses,
so a stuck assemble cannot strand a boss out of frame again. They descend **while** assembling
rather than after, so the intro plays where it can be watched — which is the point of an intro.

    magmacolossus  -120 -> 140   visible        warhawk       -120 -> 150   visible
    cryobehemoth   -120 -> 140   visible        rampart/toxic         visible

## 15. WHY NOTHING CAUGHT THIS

The suite had assertions that these bosses SPAWN, that they DRAW, that they FIRE, and that their
parts resolve — all of which passed, because all of it was true. **Nothing asserted where they
were on the screen.** A boss can satisfy every behavioural test ever written for it and still be
invisible. There is now an assertion on screen position, and it is the one that matters: a boss
the player cannot see is an unwinnable stage.

## 16. STILL OPEN FROM MIKE'S LIST

* **The looping lava corridor before the fire boss** — "we should be traveling past this mountain,
  flying over just lava that repeats, and he appears". Not built; this drop only made him visible.
* The **weird red box** on the fire stage — not reproduced yet.
* Jets facing sideways · helix orb laser and burst volley · miniboss slow/shield · stats-screen
  alignment · campaign map hint position.
* The **ice-level freeze** still wants a retest now that the 0806a throw is gone.


---
---

# DROP 0806f — THE LAVA CORRIDOR WAS ALREADY THERE

> "the stage did not connect a tiled looped lava section of its own where he has his intro, we
> should be traveling past this mountain, flying over just lava that repeats, and he appears and
> does his intro."

## 17. NO NEW ART — THE MOUNTAIN WAS ON TOP OF IT

`drawStageBG` builds the background in a fixed order: base fill across the world width, then the
**animated liquid**, then the **master over it**. That order exists so anything keyed out of the
master shows the liquid moving underneath.

Stage 2's liquid is `nlq2_lava` — a seamless six-frame loop already spanning the full world
width, already animating, already drawn on every frame. **The looping lava corridor Mike is
describing has been underneath the mountain the entire time.** It only needed the mountain to
stop being drawn over it.

There was even a boss-arena mechanism for this already: `cfg.arena` swaps in a dedicated backdrop
during a boss run, and stages 5 and 7 use it. Stage 2 just never declared one, so it fell through
to looping the master — the mountain — which is exactly what Mike saw.

`arenaLiquid:true` on stage 2 makes the boss branch return after the liquid instead of drawing
the master. Verified during a live boss run:

    stage 2   master: NONE      drawing nwl_lava_2      <- open lava, looping
    stage 3   master: nst3_master                        <- unchanged

⚠ The return is guarded on `frames` being present. Without that, a stage with no liquid would
drop straight to a flat fill colour during its boss — a blank screen, which is worse than the
backdrop it replaced.

## 18. WHAT I DID NOT FIND

**The "weird red box" was not reproduced in 0806f — Mike's description found it in 0806g.** See
§20. My search failed because I was looking for a red literal; the colour comes from a theme
table as `rgba(120,26,6,0.80)` and the rect is a legitimate part of the entrance.

## 19. STILL OPEN

* Jets facing sideways · helix orb laser and its burst volley · miniboss slow/shield ·
  stats-screen alignment · campaign map hint position.
* The **ice-level freeze** retest, and the **red box** — both need a look on this build rather
  than more guessing from me.


---
---

# DROP 0806g — THE RED COLUMN

> "while the magma boss was forming, it was a rectangular see thru column of red that went
> vertically across the screen ... it almost looked like he was coming out of ms-paint hell."

That description found it in one line. It is `genesisDraw`'s surface slab, and it is **two faults
in the same rect**.

## 20. WHY IT WAS A COLUMN, AND WHY IT WAS TRANSLUCENT RED

`genesisDraw` paints a flat "surface" so the hauled limbs have a definite waterline to break —
otherwise they fade in from nowhere. It filled `x=0, width=VW`.

**VW is 480. The world is 800.** So it covered 480 of 800 and landed as a vertical band with a
hard edge down the middle of the field. And `genTheme('mbg2').deep` is **`rgba(120,26,6,0.80)`** —
translucent dark red. "See thru red column", exactly.

**And it was full height because he was off-screen.** `lavaY` derives from the boss's `y`, and
until 0806e he sat at −120 — which put the slab's top at y=15 and gave it **497px of height**. A
near-full-screen translucent red slab with a straight vertical edge. Fixing his position in 0806e
would have shrunk it to the lower third; it took this to remove it.

Now spans `worldWidth()` (800) and is clamped at the top.

⚠ **Why my 0806f search missed it.** I grepped for red literals — `#f00`, `red`, a red
`fillRect`. The colour never appears as a literal: it comes out of a theme table, and the rect is
a legitimate, intentional part of the entrance. **Searching for what a bug looks like in source
only works when the bug is written literally.** Mike's description of the SHAPE — rectangular,
vertical, see-through — is what located it, and it took seconds once I had it.

## 21. ON STAGE 2 IT IS NOT DRAWN AT ALL NOW

0806f made that stage's boss arena the real animated lava bed. Laying a flat translucent
rectangle over actual moving lava is precisely the MS-Paint look Mike named. Where the stage
supplies the surface, the stage wins — the slab is skipped when `arenaLiquid` is set.

    stage 2 magma   no slab drawn        (real lava carries it)
    stage 3 cryo    slab x=0 w=800       (full world width, no edge)

## 22. STILL OPEN

* Jets facing sideways · helix orb laser and its burst volley · miniboss slow/shield ·
  stats-screen alignment · campaign map hint position.
* The **ice-level freeze** retest is still the one thing I most need confirmed.


---
---

# DROP 0806h — JETS FACE THE WAY THEY FLY

> "jets coming at me flying south but facing to their side instead of facing vertically south."

Reported in the very first message of the session. One line.

## 23. THE WRONG atan2 CONVENTION

    e._faceAng = Math.atan2(1, e._sdLean*0.42);

`atan2` takes **(y, x)** and this passed `(1, lean*0.42)` — the MATH convention, where 0 rad
means **+x**. The draw uses the ART convention, where 0 rad means **UP** and rotation is
clockwise. The two disagree by a quarter turn:

    lean  0.0   was  90deg -> facing EAST      now  180deg -> facing SOUTH
    lean +0.5   was  78deg -> facing EAST      now  168deg -> facing SOUTH
    lean -1.0   was 113deg -> facing EAST      now -157deg -> facing SOUTH

Every dive-and-lean jet flew down the screen turned ninety degrees, and because the lean term
shifted it differently each frame it read as "facing to their side" rather than as a clean flip.

Correct conversion for art that points up: a travel vector `(dx, dy)` needs **`atan2(dx, -dy)`**.
Straight down gives `atan2(0,-1) = PI`, and a rightward lean pulls it just under PI so the nose
tilts the way the jet is actually sliding.

Asserted on the RESULTING DIRECTION rather than on the formula, so the angle can be retuned but a
jet can never again face somewhere other than where it is going. The assertion also checks that
the OLD formula genuinely faced them sideways — otherwise it would be proving nothing.

**This is the third orientation bug of the same family** — after the pellets in 0805f (art
authored sideways, three call sites each assuming a different facing) and the boss spawn in
0806e. Art-convention vs math-convention is worth treating as a known trap in this codebase.

## 24. CAMPAIGN MAP HINT MOVED

> "campaign map, move the message about how to scroll down to the bottom of the screen."

It was pinned to `MY+480*S` — the bottom of the MAP, which moves with the map's own scroll and
scale, so on a tall map it landed in the middle of the briefing text. Now anchored to `VH-18`,
which is exactly where the title screen's identical hint already sits, so the two agree and it
cannot collide with map content.

## 25. STILL OPEN

* Helix orb laser and its burst volley · miniboss slow/shield · stats-screen alignment.
* The **ice-level freeze** retest — still the one thing I cannot verify myself.


---
---

# DROP 0806i — THE HELIX BURST: HALF DONE, AND I AM SAYING SO

> "mavericks helix ball should not have a laser with it, the ball launches, and when you impact
> it with an enemy, THEN it bursts and shrapnels and the laser variant we had goes shooting off
> in 5 directions like a spread."

## 26. WHAT IS IN AND WORKING

**The five-way fan.** The burst previously threw its strands out as a spiral (drop 0801fu). It
now fans **five** of them across 100 degrees — `-0.87, -0.44, 0, +0.44, +0.87` radians — so the
outer pair genuinely cover ground either side instead of being a tighter version of straight up.
They are the same `_child` venomx the doubling already spawned, so they inherit the helix art,
the piercing and the damage falloff that were already tuned.

A `_fanned` guard makes it one fan per ball, so a frame where both the impact and the line
condition are true cannot double it.

## 27. ⚠ WHAT IS NOT WORKING — THE ON-IMPACT TRIGGER

**The ball still detonates on the LINE, not on contact.** The trigger reads
`b._hitSomething || (b._detonY!=null && b.y<=b._detonY)`, and I could not get `_hitSomething`
set before running out of room to verify it.

The reason it is awkward is worth recording: **the venomx does not use the generic pierce-hit
path.** It tracks its victims in `b._hs`, not `b._hit`, and does its own proximity test around
line 11456. I marked the two generic sites and the flag never fired, because the venomx never
passes through them. My last attempt to patch the real site failed on a whitespace mismatch and
I stopped rather than push a fourth blind edit.

**Measured, current behaviour:** ball spawns at y=381, burst occurs at y=181 against a
detonation line of 191 — i.e. it reached the line. `_hitSomething` reads false throughout.

The build is sound — suite green at 2,047 across two runs, syntax clean — and the fan is a real
improvement over the spiral. But the headline of Mike's request, *"when you impact it with an
enemy, THEN it bursts"*, is NOT delivered. Shipping it as done would be a lie, and an unverified
change is exactly what caused the 0806a disaster.

**Next session, first job:** set `_hitSomething` inside the venomx's own `_hs` hit test at ~11456,
guarded to `_charged && _full && !_child` so the fan strands cannot chain-detonate, then verify
the burst happens ABOVE the line with an enemy planted in front of the ball.

## 28. STILL OPEN

* The helix on-impact trigger above.
* "should not have a laser with it" — the ball is still launched as a lance that becomes a ball.
  Not addressed.
* Miniboss slow/shield · stats-screen alignment.
* The **ice-level freeze** retest.


---
---

# DROP 0806j — NOTHING FADES OUT

> "stop fading them out. there should be no fade out effects for any enemies, mini bosses,
> bosses, or effects, period ... we have sprites and effects for a reason."

## 29. FOUR DEATH FADES, ALL REMOVED

The worst was a whole system. **`fadeOuts` re-drew the dead WRECK for a further half second at
declining alpha, on top of the explosion.** So every kill ended with a ghost of the unit hanging
in the smoke while the death art played underneath it — the exact thing Mike is describing. The
other three dissolved minibosses and bosses over their own destruction frames.

    fadeOuts ghost re-draw          removed
    sub-boss  1-(b.dying-0.78)/0.9  removed
    boss      1-b.dying/1.9   (x2)  removed

The `fadeOuts` list is still ticked and still expires — only the ghost DRAW is gone, so nothing
else that reads it changes behaviour. Asserted, so a future pass cannot re-add the dissolve and
cannot accidentally leak the list either.

⚠ **Not yet done from the same instruction:** the flamethrower and ice breath are supposed to be
the ONLY things that fade, and to stop animating while they do. That is a separate change in the
flame draw and I did not reach it.

## 30. ⚠ THE HELIX — STILL NOT LANDED, AND THE SPEC HAS MOVED

Mike's clarification changes the shape of it:

> "he forms a ball and launches a ball, no lance with the ball. when it either contacts with an
> enemy, or explodes when it does naturally during hangtime/airtime, then it shoots several
> volleys of lances."

So: **ball only**, burst on contact OR at the end of its own airtime, then **volleys of lances**
plus debris. What ships today is a lance that becomes a ball, bursting on a distance line, and
throwing a single five-way fan.

I spent this pass and the last chasing the on-impact flag and did not land it. What I have ruled
OUT is worth recording so the next attempt does not repeat it:

* the generic pierce path (`b._hit`) — the venomx never passes through it
* the venomx's own `_hs` proximity test at ~11456 — marked, still does not fire
* the boss/sub-boss contact branches — marked, still does not fire

Which means **the charged ball is taking a third path I have not found**, and no more blind
patching should happen until that path is identified by instrumenting which branch actually
damages the ball's victims.

Given the spec has moved to "launches a ball" anyway, the right next move is structural rather
than another flag: make `releaseHelix` spawn a BALL entity with its own airtime, and give the
burst one trigger that both contact and timeout feed. That is cleaner than continuing to bolt
conditions onto a lance.

## 31. STILL OPEN

* The helix rebuild above.
* Flame / ice breath: fade on release, and stop animating while fading.
* Miniboss slow/shield · stats-screen alignment.
* The **ice-level freeze** retest.


---
---

# DROP 0806k — AUTHORED FADE-IN FRAMES, AND THE BALL FLAG

## 32. THE FADE-IN IS FRAMES NOW, NOT AN ALPHA RAMP — DONE

> "the helix and roller balls can fade in, but to be cool about it, you can make a frame set of
> the balls fading in so its a more natural effect you can control and even enhance in case I
> decide to port this game to a console."

Three six-frame sets built and registered, from the game's own ball art:

    nhxfi_g_0..5   helix ball, green    from nhxsb_g_0
    nhxfi_p_0..5   helix ball, purple   from nhxsb_p_0
    nrbfi_0..5     roller ball          from nfrb_0   (corrected twice — see 0806l)

Each frame grows the ball from a white-hot seed into the full sprite, and the colour is
**banded** at every step so it reads as drawn rather than dissolved. The canvas is padded back to
the source size on every frame so the pivot never shifts — which is what makes them safe to
retime or hand-edit later, and is the property that matters for a console port.

⚠ First attempt built the roller set from `nrb_0`, which is the recoloured helix-MASS — a strand,
not a ball. Caught by rendering it; rebuilt from `florb_0`, which is Falva's actual orb.

## 33. THE CHARGE IS FLAGGED AS A BALL, AND HANGTIME IS A TRIGGER

`_isBall` and an `_air` hangtime counter are in, and airtime now feeds the same detonation
contact does. `HELIX_AIRTIME` is 1.05s.

## 34. ⚠ THE CONTACT TRIGGER STILL DOES NOT FIRE — AND I NEARLY SHIPPED A REGRESSION

Being blunt about this. Removing the distance line was correct by the spec — a ball should burst
on contact or hangtime, never on a position. I removed it, and the ball then **burst never** and
flew off screen carrying its payload. That is worse than bursting in the wrong place, so **the
line is restored as a safety net** and the shipped behaviour is unchanged from 0806j: line
detonation, five-way fan.

`_hitSomething` still reads false with an enemy planted inside the ball's own hit window. Ruled
out across three drops now:

* the generic pierce path (`b._hit`) — the venomx never passes through it
* the venomx `_hs` proximity test at ~11456 — marked, does not fire
* the boss / sub-boss contact branches — marked, do not fire

And the airtime trigger did not fire either in the same test, which is new information: it
suggests the charged ball is not reaching the block those flags live in at all, rather than the
flags being wrong. **That is the thing to instrument first next time** — log which branch of the
venomx update the charged ball actually executes, before touching another line of it.

## 35. STILL OPEN

* The helix: locate the ball's real update branch, then contact + hangtime detonation, volleys
  of lances, and drawing the ball from `nhxsb_`/`nhxfi_` instead of the lance reel.
* Flame / ice breath: fade on release, and stop animating while fading.
* Miniboss slow/shield · stats-screen alignment · the ice-level freeze retest.


---
---

# DROP 0806l — THE ROLLERBALL, FROM THE RIGHT BALL THIS TIME

> "thats not falvas rollerball, thats the orb. theres the ball she charges up to release too. you
> forgot that one. those orbs just kind of split off from her picking up the powerup and anchor
> down to the sides of her jet like they do."

## 36. THREE SOURCES, TWO OF THEM WRONG

Falva has **two** round things and I used the wrong one twice:

    nrb_0     Maverick's helix-MASS recoloured pink — a strand, not a ball at all
    florb_0   the HELPER ORB — splits off a powerup and anchors to her wings. Not a weapon she
              charges. This is the one Mike caught.
    nfrb_0    her AUTHORED CHARGED SPHERE — the ball she winds up and releases. Correct.

The source's own comments were sitting right there and say it plainly: `nrb_` is *"Maverick's
helix-mass recoloured pink — its own comment said so"*, and `nfrb_0..3` are *"the real sphere at
four charge stages, brightening as it spins up. Preferred over fball_ and over the old
recoloured helix-mass."* I had read neither before picking.

**Both wrong sources were caught by RENDERING the result, not by reading code.** A strand and an
orb both look plausible as filenames; they do not survive being looked at. That is the second
time this session that rendering caught something a grep would not have — the roll-frame debris
was the first.

`nrbfi_0..5` is rebuilt from `nfrb_0`: her hex-panelled sphere growing from a pale seed to the
full charged ball.

## 37. ASSERTED BY CANVAS SIZE, SO IT CANNOT DRIFT BACK

`nfrb_0` is 341x358 and `florb_0` is 110x109, so the source is unambiguous from the canvas alone —
the assertion compares the fade-in set against `nfrb_`'s dimensions and separately proves it is
NOT the orb's. It also checks all three sets keep one canvas across every frame, because a set
whose frames change size would shift its pivot and defeat the whole point of authoring them.

## 38. STILL OPEN

Unchanged from 0806k: the helix ball's real update branch needs instrumenting before anything
else is patched into it; flame / ice breath fade-on-release; miniboss slow and shield;
stats-screen alignment; and the ice-level freeze retest.


---
---

# DROP 0806m — I FOUND THE BRANCH THAT OWNS THE BALL

I said the first job was to instrument rather than patch. That was right, and it took one pass.

## 39. NONE OF THE THREE PLACES I PATCHED OWNS THE BULLET

Across 0806i, 0806j and 0806k I set `_hitSomething` in the venomx update block, in the generic
pierce path, and in the boss/sub-boss contact branches. **It never fired once.**

**`mavHelixTick` runs before all of them.** It drives its own `travel -> glow -> burst` phase
machine, calls `helixDetonate()` and sets `b.dead` — so the ball was already gone before a single
one of those flags was ever read. Every patch was landing downstream of the thing that killed it.

Three drops of blind edits, one pass of instrumenting. **The lesson this codebase keeps teaching:
find the branch that owns the object before changing behaviour on it.** It is the same shape as
the L6 jets in 0805k (the counter was fixed, the fetch was not) and the mech bosses in 0806e (the
flag was set and cleared above the block it gated).

## 40. BOTH TRIGGERS NOW LIVE WHERE THE BALL LIVES

Contact — against enemies and against the boss — and hangtime both sit inside `mavHelixTick`, and
both route through the **same `helixDetonate`** the phase machine already used. So the burst is
identical however it is caused, rather than there being two burst implementations to keep in
step. `HELIX_AIRTIME` is 1.05s.

Confirmed firing: with an enemy in front of the ball, the contact path registers where it read
false through three previous drops.

⚠ **What is still not verified:** the exact burst POSITION under contact. A synthetic bullet in
the probe bursts at the phase-machine line rather than on the enemy, and I ran out of room to
determine whether that is the probe's construction or a real ordering problem between the contact
test and the phase transition. The code is in the right place and the suite is green across two
runs, but I have not proven the ball bursts ON the enemy rather than shortly after it.

**Next: build the ball a proper probe** — spawn it through `releaseHelix` rather than by hand, so
it carries every field the real one does, and assert the burst y against the enemy's y.

## 41. STILL OPEN

* Verify the contact burst position, then the volleys of lances and drawing the ball from
  `nhxsb_`/`nhxfi_` instead of the lance reel.
* Flame / ice breath: fade on release, and stop animating while fading.
* Miniboss slow/shield · stats-screen alignment · the ice-level freeze retest.
