# Stage 4 — bombing spirals and the final pursuit

October 18, 2026. Mike's approved follow-up to the Warden wing and Sovereign chase.

`assets/stage4_panic_1017.js` owns the new behavior after the existing combat
owners. The authored Warden/Sovereign plates, modular damage, score, boss death,
jet heading bank, bombs, lightning reels and normal FOV renderer remain in use.
No new art or atlas changes.

## Warden wing

- Easy/Normal keep their one/two-jet counts and now return to an orbit. Hard
  remains four; Furious/Insanity remain six, with the existing edge assignments.
- After the initial orbit, every surviving entered jet takes part in the same
  outward spiral. Real movement selects the authored heading frames. Each jet
  drops bombs at committed, distributed landing sites with the native ground
  reticle, falling bomb art, explosion and sound. The markers never chase a dodge.
- The same living actors return from their assigned edges with their original HP.
  Their entire enlarged entry remains above the combat plane and harmless.
  Normal gun bursts resume in orbit. Offscreen return warnings use the normal FOV.
- Destroyed jets are excluded. The existing five-second replacement timer still
  spawns a new actor; it never resurrects the destroyed actor. A Warden ram and
  his independent guns/missiles continue while the wing bombs or returns.
- The small `game.js` movement-loop guard prevents a second generic mover,
  edge pin or offscreen cull from fighting the owned flight. It retains flash
  expiry and the native zero-HP/death path; actors stay in the combat/Retina lists.

## Sovereign

- The native 25% HP handoff starts a warned panic ram. Aim tracking ends during
  the tell; moving after the lock clears the committed ram path. Native engine
  rev, charge sound, shake and rumble remain. Detached objectives do not ram.
- A small 4% HP floor makes the ram commit even under burst damage. The south
  exit is followed by an enlarged, north-facing overhead return; the entire
  scaled return is harmless. The floor ends on reaching the combat plane.
- The final phase then stays north-facing until death. It moves north while the
  existing road scroll sells the pursuit. There is no 10.5-second reset to the
  forward-facing attack book, shield rearm, new HP pool or heal.
- Exposed HP damage is multiplied by 2.0/2.1/2.2/2.3 on Easy/Normal/Hard/Furious.
  Only real HP loss builds retaliation. Extra lightning has its own committed
  target and full FOV tell; anger is capped at two stored charges, pending anger
  attacks are capped at two, and releases have an independent cooldown. Every
  hit still goes through native part/owner flash and normal death routing.
- Both directions now use a complete electric row, including straight down the
  middle. There is no rotating two-lane gap. Shared geometry supplies the warning
  and shot origins/angles. Electric balls remain unshootable through SG17's
  protected flags. Stage 3 keeps its authored moving ice gap.
- The older regular overflight also writes its rear-volley warnings into the
  live hull renderer. Its prior preview-only SG17 fan was insufficient because
  the Sovereign draws through `sa14Draw`. Its normal recovery remains above the
  final-quarter phase; the new final pursuit never recovers or turns around.

## Review and verification

Open `docs/previews/stage4_panic_1017/index.html` through the local server. It
offers the Warden, panic sequence, northbound pursuit and full electric row,
using the actual game, regular playfield and side HUD. Saves are isolated;
review flight is explicitly invulnerable. Actual keyboard firing is verified.

Recorded verification is in `docs/qa/stage4_panic_1017.json` and ignored output
under `_shots/stage4_panic_1017/`. Native fixtures verify every roster, bombs
from every surviving jet, stable HP/actor identity, authored turning frames,
death/replacement, ongoing Warden attacks, actual depth-contact safety, matching
FOV lanes, the native quarter-HP transition, visible damage pixels and expiry,
warned retaliation, a pursuit exceeding thirty seconds and normal boss defeat.
Screenshots use the full native game and were visually inspected. These are
controlled encounter checks, not a human campaign balance certification.

No commit or push. All prior local work is preserved. `test_fl.js` keeps its
starting bytes/CRLF; `game.js` keeps LF and differs from this pass's starting
bytes only by the documented owned-flight guard. The older gameplay owners
are unchanged from the starting hashes.
