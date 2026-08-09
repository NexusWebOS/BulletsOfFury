# PASSOVER — drop 0807o   (NINE STATS, OUR FONT, SCORE BAR, FLASHING PASSWORD)

Build: `BulletsOfFury_0807o`
Harness: **2,175 assertions / 200 sections / 0 failing**, twice, reaching the banner.

---

## 1. FOUR OF THE NEW ROWS WERE NEW MEASUREMENTS, NOT NEW LABELS

Mike's order, implemented exactly:

    KILLS · ACCURACY · MISSILES FIRED · MISSILE HITS · DAMAGE DEALT ·
    LIVES LOST · SPECIAL DAMAGE · SPECIAL HITS · CLEAR TIME

Only `missiles` (fired) was ever tracked. **Missile hits, special damage, special shots and
special hits did not exist** and had to be attributed before they could be shown.

Attribution is a source flag set ONCE per bullet at the top of the player-bullet loop, not
threaded through the forty-odd `hitEnemy` call sites inside it. Tagging each individually is how
one gets missed; one flag covers every path, and it is cleared after the loop so nothing outside
is ever mis-attributed.

⚠ **And I missed the reset.** I extended the `stageStats` declaration and forgot that
`beginStage` re-creates the object from scratch — so all four fields were undefined the moment a
stage began and the new rows would have read 0 forever. Caught because the assertion checks the
fields exist AT RUNTIME rather than in the source.

## 2. ⚠ THE RANK WAS PUNISHING PLAYERS FOR RESTRAINT

Driving a clean run through it exposed something the row list alone did not: **rank fell from A
to C** because MISSILE HITS and SPECIAL HITS read 0% when nothing had been fired, and dragged the
average down by two ninths.

MISSILES FIRED is a worse case — it is a COUNT, not a quality. Ranking on it puts a careful run
that saved its missiles BELOW a wasteful one.

All nine rows still display, because you should see that you used none. Three are excluded from
the rank average: the two accuracy rows when their denominator is zero, and MISSILES FIRED
always. Same clean run now ranks B, and A once the missiles land.

## 3. THE REST OF THE ASKS

    our fonts          every label, value, header and the rank go through stageText now
    scaled down        labels 0.024, values 0.026, header 0.050 of panel height
    portrait centred   in the left column, between the header and the bar block
    score + password   bold, outlined
    password flashes   alternates green/gold on a 7Hz beat with a blip every 0.45s,
                       and ticks once per letter as it types
    score              ticks as it counts, locks gold with a chime
    score bar          its own, at 0.95 of a row height — larger than a stat bar
    bars not thin      0.46 -> 0.50 of the row, and the panel grew 0.815 -> 0.925 of
                       the screen so nine rows fit without thinning anything

## 4. TWO THINGS MY OWN RENDER GOT WRONG

My proof render dropped `%` and `:` and I nearly reported them as broken. **The game resolves
both** — `%` through the gamefont fallback `ncm_font_c037`, `:` through `sfont1_p58` — my render
only checked one of the two lookup tables. The render was wrong, not the screen.

And the labels were sitting ON their own bars at the tighter nine-row pitch. Visible only by
rendering it; the numbers all looked fine.

## 5. STILL OPEN FROM THE PLAYTHROUGH

Seven: dialogue box art · liftoff music · L2 miniboss routing into lava · the tank on the
mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
