# 0821c — DECKER'S SHOTGUN GETS ITS ART AND ITS THREE SOUNDS

Mike supplied `CF_DeckerShotgunGenerations-Vol.1` and labelled the two plates himself: the HEX
BADGE is the icon, the SQUARE ARMOURED CRATE is the box.

| item | state |
|---|---|
| the proper pickup icon | **INSTALLED** — `nsw_icon_decker` |
| the pickup box | **INSTALLED** — `nsw_box_decker` |
| shells eject each side of the plane | **ALREADY CORRECT — verified** |
| buckshot sound on fire | **NEW** — `dkBuck` |
| eject sounds for the shells | **NEW** — `dkShell` |
| reload sound | **NEW** — `dkReload` |

---

## WHAT WAS ACTUALLY THERE

0811m built the whole fallback chain and left a note that it was waiting on art: *"it tries
nsw_icon_decker first so a real icon drops straight in the moment Mike supplies one."* That held —
installing the key was the entire wiring job for the pickup, no code change at all.

⚠ **BUT THE OTHER TWO SLOTS WERE WORSE THAN PLAIN, AND ONLY RENDERING THEM SHOWED IT.**

    spicon_decker    resolves to NO ART AT ALL — comes back missing
    special_decker   a blue crate with a GENERIC JET BLUEPRINT on it, nothing to do with a shotgun

Both are covered now by the same rename-map Cole's special uses, so the old plates stay on disk
and it is one line to reverse.

## ⚠ THE PACK RECOMMENDS Vol.3 AND THAT IS ONLY HALF RIGHT

The README says *"Vol.3 is the recommended implementation version"*. Rendered against the two
siblings, the generations split:

    Vol1   RED hex badge          — wrong family; cole and lizzie are green and yellow
    Vol2   YELLOW hex badge       — matches nsw_icon_lizzie exactly
    Vol3   SQUARE armoured crate  — box only; its ICON is byte-identical to Vol2's

**Vol2 and Vol3's icons have the same md5.** The icon never changed after Vol2; only the box did.
So "use Vol.3" is right for the box and irrelevant for the icon, and there was no choice to make.

Sizes landed on the siblings without scaling: icon 160x160 like `nsw_icon_cole`/`_lizzie`, box
400x400 like `nsw_box_cole`/`_lizzie`.

⚠ **THE BOX IS SQUARE WHERE THE SIBLINGS ARE HEX.** That is Mike's call — Vol.3 is the "final
square armored yellow pickup box" and he attached that one as the box. The ICON stays hex, which
is what keeps the on-field pickup in family beside the other two.

⚠ **NO KEYING NEEDED.** The magenta in Mike's screenshots is the preview backdrop, not a chroma
key — measured, every plate already carries real alpha (41-44% clear on the hex plates, matching
the siblings' 40.8/43.0).

---

## THE SHELLS WERE ALREADY RIGHT

`dkFire` has carried `for(const side of [-1,1])` since Mike first asked. Verified rather than
assumed: 7 pellets, 2 casings, at **x-13 and x+13** — one out of each side — and they draw.
Nothing to change.

## THE SOUNDS WERE THE REAL GAP

The whole weapon had **one** sound: `spread()`, a single 660Hz sawtooth shared with every other
scatter gun in the game. Nothing marked the casings, and nothing marked the pump — so a 0.62s
reload the player cannot hear is just an unexplained dead trigger.

Synthesised from `tone`/`noise` like every other entry rather than added as assets — the route
`blocked()` took in 0807b. They land as a rhythm you can learn, which is the point of `DK_RELOAD`
existing at all:

    BOOM .......... tink-tink .......... chk-CHK
    0ms            +70 / +125ms         +620ms (trigger live again)

- `dkBuck` sits between `expSmall` and `expBig` on purpose — a shotgun is a small explosion, not
  a laser.
- `dkShell` is deliberately THIN and high so a pair of casings reads over the blast's tail
  instead of fighting it. One call emits both tinks, so the call site stays one line.
- `dkReload` fires on the **transition** of `_dkCd` to zero, so it goes exactly once per reload
  and lands on the frame the weapon is ready. That turns the dead trigger into something the
  player can time instead of something that happens to them.

Verified in the browser by wrapping all three: `dkBuck` and `dkShell` at fire, `dkReload` once
when the cd reaches 0, in that order.

---

## HOW TO VERIFY

    node --check assets/game.js
    node --max-old-space-size=3072 _BUILD_SOURCE/test_fl.js     2,701 ok / 3 fail

The 3 failures are environmental: the preload key count (now 9805 — the two new keys) and the two
`_superseded/` ledger checks, which live on the primary machine.

---

## STILL OPEN FROM THIS PACK

The pack ships six more effect families that nothing references yet — **muzzle blast, buckshot,
7-way spread, impact fire, scorch decals, and Vol.3's projectile trails + pre-angled travel
shots**. Decker already has `ndk_muz_*`, `ndk_shot_*`, `ndk_ang_*`, `ndk_imp_*`, `ndk_scorch_*`
and `ndk_trail_*` wired to older art, so swapping them is a re-skin of a working weapon rather
than new plumbing — a drop of its own, and worth doing with Mike watching since it changes how
the gun reads in play.

⚠ Vol.3's map declares the trail art is for **non-hitscan pellets** with a stated collision rule
("use only the leading metal pellet; exclude the flame trail from the hitbox") and a speed band of
360-480 px/s. Current `DK_SPD` is 11.0 px/frame = 660 px/s, so adopting that art properly is a
BALANCE change too, not just an art swap. Do not take it as a drop-in.
