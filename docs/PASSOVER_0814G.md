# DROP 0814G — THE STALE SWEEP: THREE OF FOUR SMALL ITEMS WERE ALREADY FIXED, AND THE FOURTH WAS
# HIDING A REAL BUG

Continuation of 0814f's finding. Every remaining "quick" open-list item was re-measured before any
work. Three were stale; the one live item turned out to be two bugs, one of them unreported.

## 1. STALE: THE FONT 404

`assets/fonts/BlackOpsOne.ttf` — fixed in 0811z. index.html's @font-face points at
`assets/game/BlackOpsOne.ttf` and the file is on disk (166,532 bytes, measured). The entry
outlived the fix by three weeks.

## 2. STALE: THE validate_antipatterns HOOK

"Errors on every write — its script path does not exist." No settings file anywhere on this
machine references it any more — user-level `~/.claude/settings*.json` and the project's own
`.claude/`, all checked. The broken hook was removed at some point; nothing can error.

## 3. STALE: THE 0810a PARTICLE LEAK

`HANDOFF_BRIAN_0814` reported it back ("the expiry test sat below two branches that draw and
`continue`"). Read on main @ cbffa29: the expiry test sits at the TOP of the loop, above the
`_tsFx` / `_fbDecal` / `_iceChip` continue branches, with a "re-fixed drop 0814a" note and a
tombstone comment at the old position warning against moving it back. Found and fixed within the
same drop series that reported it.

## 4. LIVE: THE ui_layout.json 404 — AND THE EDITOR SAVING TO THE WRONG PATH

The 404 itself is real but cosmetic: `game.js` fetches `assets/data/ui_layout.json` (guarded,
`file://`-gated, catch-swallowed), and the file did not exist, so every http boot logged one 404.

⚠ **THE 404 WAS HIDING THE ACTUAL BUG.** `tools/bof_ui_editor.html` — the editor built so Mike can
reposition UI and "write layout changes straight back into" the game — loaded AND saved
**`assets/ui_layout.json`**, one directory up from the `assets/data/` path the game reads. Every
layout saved from the editor went to a file the game never fetches: the editor said saved, the
game showed defaults, and the boot 404 persisted because the file the game DOES ask for was never
written. The two halves of the feature had never actually been connected.

**Fix, both halves:**
- The editor's load and save now go through `assets/data/` (matching ART_TAXONOMY.json and every
  other data JSON), `{create:true}` on the dir so a fresh folder works.
- The game now SHIPS `assets/data/ui_layout.json` containing literal `null` — a valid JSON
  document. Over http the fetch gets 200; `r.json()` is `null`; the game's `if(d)` guard no-ops;
  the editor's loader treats it exactly like "no file yet" (guarded `if(json)`).

**Measured end to end** (`probe_uilayout_0814g.html`): file readable · parses as JSON · value
`null` · `guardWouldSet:false` · `UI_LAYOUT_OVERRIDE` unset · `uiRect` returns its fallback
untouched. Six for six.

⚠ **A `null` FILE IS THE ZERO-BEHAVIOUR DEFAULT, AND `{}` IS NOT.** An empty object is truthy: it
would pass the game's `if(d)`, set `UI_LAYOUT_OVERRIDE={}`, and silently change the code path every
`uiRect` call takes. The literal `null` document is the only content that makes the fetch succeed
while provably changing nothing.

## THE SWEEP'S SCORECARD

Six open-list entries re-measured across 0814f/0814g: **five stale, one live.** The live one had a
second, unreported bug underneath it. The lesson from 0814f stands and sharpens: the open list
records when a thing broke, not whether it still is — and an entry that IS still live may not be
describing the bug that matters.

**Next: the stage-8 boss forms** — the four authored forms in `CF_BOFFinalArtLock-Vol.2`
(symbiote_carrier → winged_predator → razorhalo → nullheart, with named component anchors and
damage states per form) against the standing "stage 8 boss: 4 forms, same pattern, very tanky".
That is real integration work, not a sweep item.
