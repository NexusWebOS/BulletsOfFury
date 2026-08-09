# PASSOVER — drop 0808q   (STAGE 1 NAVAL: SIGNED OFF)

Build: `BulletsOfFury_0808q`
Harness: **2,279 assertions / 208 sections / 0 failing**, twice, reaching the banner.

---

## 1. WHAT LANDED

The first two units of the new stage 1 roster, built from Mike's spec and corrected across four
passes until he signed off.

    s1boatgun     5-8 round bursts at 0.40s spacing (half the player's 0.20s),
                  then EXACTLY 2.0s of silence, looping. Muzzle flash nmz_2 on the barrel.
    s1boatpatrol  moves, idles 1.5s, launches a non-homing rocket, recoils with screen shake.
                  Muzzle flash nmz_4 at 1.6x.

Both hold their bows vertical, fire straight down, and steer laterally rather than pirouetting.
Projectiles are the real in-game art on the real schedule: `mfx_mg_2_*` alternating every 70ms,
`mfx_emr_0_*` for the rocket.

## 2. THE FOUR CORRECTIONS, AND WHAT EACH ONE TAUGHT

**"burst is 5-8 pellets at a time"** — I had it as 3 SECONDS of firing. At 0.40s spacing that is
seven or eight rounds by accident, and a different number every time the boat clipped in or out
of its lane mid-volley. A burst is a COUNT of rounds.

**"burst fires with 2 second delays ... Back to the loop"** — the gap was `rnd(2.4,3.6)`, so the
rhythm was never twice the same. A burst weapon reads as one because the SILENCE is as fixed as
the volley: the player learns the window and moves in it. A random gap never becomes a window.

**"the boat should be facing vertical generally and only fire vertically"** — they were choosing
freely from eight compass headings and firing along the hull's yaw, so a boat could sit broadside
shooting across the screen. "In their six" also had to be rewritten: a compass arc means nothing
on a hull that no longer rotates, so it is now "player is below me and in my lane".

**"Only use single muzzle flashes"** — I was walking all nine `nmz_` reels so consecutive shots
would not repeat, which made one turret look like nine different weapons. One flash per weapon.

## 3. ⚠ THE BUG THAT HID INSIDE THE FLASH WORK

Frame 4 of every `nmz_` reel is a near-invisible tail-off. My draw mapped elapsed time linearly
across five frames, so a 0.13s flash spent most of its life on the frame with almost nothing on
it. **That is why the flash "wasn't there" — it was drawing, on the wrong frame.** Deleted from
all nine reels and the timing front-weighted with `pow(k,0.62)`.

And a real crash found on the way: renaming `NAVAL_BURST_LEN` left the patrol boat referencing
it, throwing a ReferenceError on every launch. That is why the rocket never fired in ANY capture,
and I had been reading it as "the player was never in its arc".

## 4. LOCKED

Eighteen new assertions pin all of it: the round count, the fixed gap, the spacing, both flash
families, the front-weighting, vertical fire, that the tail frame is gone from all nine reels and
the other four survive — and a played check that every volley fired is 5-8 rounds and only the
assigned flash families appear.

## 5. NEXT

The jets. Mike: "jets travel at medium speed towards the player from vertical or sides of the
screen."

Still open on the boats: they drift downscreen instead of holding station — the scroll
cancellation has its sign inverted. One line, deliberately left until the firing was signed off.
