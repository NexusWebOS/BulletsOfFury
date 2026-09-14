# Codex takeover — 2026-09-13

## Starting point

Workspace: `C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury`

GitHub: `https://github.com/NexusWebOS/BulletsOfFury`

Read `HANDOFF_CODEX.md` and `CLAUDE.md` for the original handoff, creative
constraints, local drops, and open design decisions. The current branch is `main`
at `694e84ae`; the README's Codex Edition branch description is historical.

Existing staged, unstaged, and untracked work was retained. This takeover adds
Codex guidance, verification records, and a small trailer source archive. It does
not change gameplay, commit, push, merge, or delete existing work.

## Verified baseline

| Check | Result |
|---|---|
| `node --check assets/game.js` | Passed |
| `_BUILD_SOURCE/test_fl.js` | Completed: 3,627 passing assertions, 60 failures; exit 1 |
| Real Chromium title capture | Passed; screenshot inspected |
| `_BUILD_SOURCE/probe_tempest_0913b.py` | 30 passed, 0 failed; no page or console errors; contact sheet inspected |
| `_BUILD_SOURCE/verify_atlas_0806z.js` | Completed with 3 failures; exit 1 |
| `_BUILD_SOURCE/probe_spaceship_0913a.py` | 31 passed, 0 failed in 231 seconds; no page errors, console errors, or loop throws; transformation contact sheet inspected |

The original handoff records 3,626 passing assertions and 61 existing failures.
The measured run differs by one assertion. No gameplay change was made and no
test repair is claimed. Compare failure names, masking changing numerical values,
before assigning a future failure to a regression.

Full suite failure names: `docs/qa/codex_takeover_0913_failures.txt`.
Atlas verifier failure names: `docs/qa/codex_takeover_0913_atlas_failures.txt`.

The atlas verifier reported:

1. Its VICTORY fixture drew nothing.
2. Its Stage 2 simulation lacks the mocked canvas method `ctx.setLineDash`.
3. Its sheet-majority threshold rejected 7,045 sheet keys versus 3,311 loose keys.

These are baseline verifier findings, not established new gameplay regressions.
The real Chromium Tempest encounter works with the current authored loose art.

Logs and screenshots are in the ignored `_shots/codex_takeover/` folder. A local
HTTP preview was started at `http://127.0.0.1:8000/` and requested in the Codex
browser panel. The server must be restarted if that process ends.

## Incoming GitHub work

The cached `origin/main` is two commits ahead of the checkout. A read of live
GitHub found the newer main commit `f936f106d85d935aaf518fbac5ab34756bc26724`,
dated 2026-09-13 05:15:40 UTC. That commit stores the Herald of Death as
`ALTBOSS[8]`, leaves Stage 8 without a miniboss, and stages a shared Stage 6
encounter for both Tempest brothers.

The local build already ports the black Tempest alone as `SUBBOSS[6]` and retains
Blacksteel as `ALTBOSS[6]`. It still has the Herald assigned to Stage 8. Resolve
this difference using the latest request before implementing the next encounter
or integrating GitHub changes. The remote staged passover's earlier Stage 8 plan
for the gray brother was superseded by its Stage 6 duo section.

The latest remote handoff was saved for inspection at
`_shots/codex_takeover/github_tempest_passover.md`. No Git refs were updated during
the takeover. Fetch and review incoming changes before any requested commit.

## Trailer continuity

Trailer v7 exists on the Desktop as `BulletsOfFury_Trailer.mp4`, 588,151,594 bytes.
The original handoff says Mike has seen it.

Fourteen source and JSON files were copied byte-for-byte from Claude's trailer
scratch folder into `_BUILD_SOURCE/trailer_v7/`, totaling 312,956 bytes before
archive metadata. SHA-256 comparisons matched all 14 originals. The archive's
README explains dependencies and original paths; it is not a complete footage
archive or a ready-to-run render workspace.

The C: drive reported 4.23 GiB free during the takeover. No full repo copies or
worktrees were created. Preserve original trailer media and scratch files.
