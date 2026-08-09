# PASSOVER — drop 0807m   (STAGE CLEAR, REBUILT FROM SCRATCH)

Build: `BulletsOfFury_0807m`
Harness: **2,149 assertions / 197 sections / 0 failing**, twice, reaching the banner.

---

## 1. IT IS A DIFFERENT SCREEN, NOT A REPAIR

Mike: *"re-do it from scratch with the same concepts. Portrait of pilot, stat bars, fills, score,
rank, stage password. Lets make this a very sega genesis like stats screen with that bullets of
fury advanced features and touch and style."*

The old one drew seven left-aligned rows with a flat bar under each, positioned against the raw
viewport — which is why they collided with the frame at any other size, and why Mike reported the
misalignment four times. Everything here is positioned against the FITTED PANEL, so the content
tracks the frame at any window size. Asserted.

## 2. WHAT MAKES IT READ AS GENESIS

**A hard, sequenced beat — nothing arrives at once.** Panel, portrait, then rows one at a time,
then score, then rank, then password. Measured end to end:

    0.0s   panel lands
    0.5s   portrait pops in
    1.0s   rows begin, one every ~0.4s, filling segment by segment
    3.5s   score starts counting
    4.0s   RANK STAMPS — slams in at 3.4x, overshoots, settles, shakes the screen
    4.5s   password types in
    ~5s    complete, and skippable at any point with fire

The stat tick pitches up as a bar fills, so you hear how good a row is before you finish reading
it — the same idiom as the pilot card, deliberately reused.

## 3. THE BULLETS-OF-FURY TOUCH

**The portrait reacts to the rank.** This game ships seven emotion portraits per pilot and
nothing was using them here. S and A pull the victory pose, B laughs, C is idle, D is sad, F is
the crash portrait. Verified: an A rank on stage 1 selected `port_cole_victory`. The pilot's face
tells you how you did before the letter arrives.

**Every row fills with the art that MATCHES its meaning**, from the eight typed `nui_fill` sets —
kills fill with firepower, accuracy with speed, damage taken with armor, survival with health.
Rows below 34% stay dim; rows at 92%+ turn gold.

Six rows now, not seven: KILLS, ACCURACY, DAMAGE DEALT, DAMAGE TAKEN, SURVIVAL, CLEAR TIME.
ACCURACY is new — `shots` and `hits` were being tracked and never shown. DAMAGE TAKEN and CLEAR
TIME are INVERTED, so a low number fills a long bar.

## 4. ⚠ THREE THINGS I GOT WRONG FIRST

**I dropped three exit branches.** My first cut replaced the whole block and kept only the arcade
outbound — losing victory, the rival encounter and the campaign path. An assertion caught the
victory gate, which would have rolled the credits at the wrong stage or never. All four restored,
and the campaign now records THIS screen's rank instead of the placeholder derived from lives.

**I misused the fill art.** `nui_bframe_large`, `nui_bseg_large` and every `nui_fill_*_large`
frame all measure 512x64 — they are the WHOLE bar in eight animation frames, not segments. Drawing
one per segment stamped the entire bar twenty-four times across itself. It draws one image
clipped to the filled width now, stepped so it still advances visibly.

**And I reintroduced the exact bug I was fixing.** At `rowsW=0.655` the right-aligned values
landed on the panel's right bevel — the same collision, put back by me in the rebuild. Caught by
rendering it. Pulled in to 0.610 so the widest value clears the moulding.

## 5. STILL OPEN FROM THE PLAYTHROUGH

Seven: dialogue box art · liftoff music · L2 miniboss routing into lava · the tank on the
mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
