# 0917 — NEW GAME +: the sixth mode, hidden until the final clear

Mike, overnight brief: *"Dark Matter which can be combined and used to make Void like weaponry and
effects. This can be only be used in New Game +, a new button you will create and unlock/make
visible after we beat the campaign on any difficulty."*

---

## 1. What it is

NEW GAME + is the **campaign structure with one flag**. `_modeGo` sets `run.mode='campaign'` and
`run.ngplus=true` and routes to the campaign hub exactly as CAMPAIGN does. The flag is read by
`infusionGateOpen('dark')` and by nothing else — so the mode changes what can **drop** (DARK MATTER
infusions, level 3 VOID) and never what the stages are. It is assigned on **every** branch of the
confirm, the way `coopOn` is and for the same reason: a stale `true` is a Dark Matter drop in a
plain run.

The unlock is the signal BOSS RUSH and TIME ATTACK already use (`bonusModesUnlockFromCampaign`,
`bof_bonus_modes_v1`) — a real final campaign clear on any difficulty. Unlike those two it is
**playable** (`BONUS_MODE_PLAYABLE.ngplus=true`), so confirming it enters the hub instead of the
"development in progress" refusal.

## 2. Hidden, not locked

Mike said *make visible*, so the row is **absent** before the clear rather than greyed under the
Nexus lock: an invisible button cannot be a spoiler. `modeList()` is the one list the cursor, the
draw loop and the mouse hit test all read, so a hidden row is gone from all three at once — the
INSANITY lesson (*"you cannot select it" is three claims; make it one fact*). Measured: five rows
walk and wrap before the clear, the draw never asks for the plate; six after.

## 3. Six rows do not fit at the five-row pitch

The 0915 layout was `y0=92, gap=82` for five plates. The family's aspects run **3.37 to 5.23**
(CO-OP is the tallest at 270px wide, NEW GAME + the shortest), so a sixth row at any literal pitch
either overlaps the tall plates or spills under the hint bar — the first cut measured the last
plate's bottom at **518** on a 512 field. `modeRows()` lays the rows out from the plates' **own**
heights; when the stack cannot fit, the plate **width** gives (270 → ~252), never the gaps, so it
is six whole plates a little smaller rather than five plates and an overlap. Five rows keep the
0915 literal layout untouched. The mouse hit test reads the same rows.

⚠ **The plate is registered under a NEW key** (`mode_ngplus_0917`, loose file
`assets/game/ui/modes_0917/new_game_plus.png`) — cells beat the loose-file cache.

## 4. The plate

SpriteCook, one job, the Boss Rush plate uploaded as `reference_asset_id` (24 credits): riveted
gunmetal frame, corner lamps, a black-hole emblem on the left, fighters diving into a void nebula
on the right, gold NEW GAME + lettering. Both variations lettered correctly; the one with the
tighter frame shipped. Cropped to its frame by difference from its own background colour — a
brightness threshold cut the dark top and bottom rails off (rows 32..128 both ways, which is the
frame, but the first pass could not tell that from the rails).

Its aspect (5.23) is wider than the family; at a shared width it reads shorter than its
neighbours. Flagged, not fixed — a taller generation is one job if Mike wants it.

## 5. Verified

`probe_ngplus_0917.py` — **15 ok / 0 fail**, 0 page or console errors, real key taps on the live
screen: five rows walk and wrap before the clear (the plate is never asked for); the clear unlocks
it; six rows laid out with 6px gaps and the last bottom at exactly 470; UP from CAMPAIGN wraps onto
it; CONFIRM lands on the hub with `run.ngplus` true; CAMPAIGN afterwards clears it; the drop pool
carries `dark` only with the flag; a campaign save carries it both ways; a password start is arcade
and drops it.

⚠ **107 `draw error in state modesel` on a green-looking run.** The first layout cut left the mouse
hit test reading `gap`, a constant the draw no longer declared — a ReferenceError swallowed by the
state draw's try/catch, invisible to every assertion above it. The probe's error count is what
caught it (the 0902a rule: read the console, not just the state).

Suite section 368. Proofs: `docs/proofs/ngplus_0917/01_locked_five_rows.png`,
`02_unlocked_six_rows.png`, `03_camphub_ngplus.png`.
