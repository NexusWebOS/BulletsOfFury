# First easy-to-hard queue batch — September 14, 2026

Mike asked to list the full checklist in chat and work from easiest to hardest.
The queue ranks implementation plus visual/behavior verification difficulty,
with prerequisite systems before dependent encounters. Asset-access and naming
requirements are recorded separately; an unavailable generator does not stall
independent code work.

## Completed

- **SPACE-15:** Replace the assembly/reveal's Gravity Mode text with the supplied
  Space Fighter models: Yuri Yamado, Maverick Moonraker, Lizzie Lavender, Falva
  Foxtrout, Cole Collisto, Juggernaut Janis, Axel Aristotle and Freezer Falcon.
  Decker displays his pilot name until Mike supplies the ninth model (SPACE-16).
  The new ship art is a separate pending item; this change uses the current ship.
- **MODE-06:** Both random Life Up opportunities receive the requested 25% boost
  on Hard/Furious in Campaign and Arcade. Midpoint chance rises from 2% to 2.5%;
  ordinary death life chance rises from 1% to 1.25%. Ammo remains 6.2% and shields
  2.8%, so the extra life probability does not replace those outcomes. Forced
  life grants remain single pickups. The midpoint spawn now uses the current
  camera's horizontal bounds, fixing offscreen drops on wider stages.

## Verification

`node --check assets/game.js` passes. Full suite: **3,818 passed / 61 failed,
exit 1**, final summary reached; all 15 new section-307 behavior assertions pass.
No new failing assertion names against the recorded 61-name baseline. The
variable sand-tank assertion failed this run after passing in the previous one.
Runtime LF and suite CRLF remain intact.

Real Chromium via `shoot.py` and the existing capture library: **25 passed / 0
failed**, zero page, console or controlled-loop errors. Inspected all nine native
model-name screenshots and the Life Up spawn/collection HUD. The text is drawn
by the actual launch renderer and fits the screen. Its existing white reveal
wash is unchanged. Native pickup collision awards exactly one life.

The probability probes deliberately inject boundary RNG values; they verify
that the actual update/drop routes use the requested probabilities in both modes,
not that a short random playthrough happens to produce a particular count.
Existing authored Life Up art remains until its separate SpriteCook replacement.

Proof: [qa/easy_queue_0914.json](qa/easy_queue_0914.json). Sources:
`_BUILD_SOURCE/easy_queue_0914/`; screenshots/logs `_shots/easy_queue_0914/`.
No commits, pushes, atlas edits or deletion of user data.
