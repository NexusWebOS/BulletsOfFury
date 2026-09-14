# Bullets of Fury — Codex project guide

Read `HANDOFF_CODEX.md`, then the opening rules and latest relevant drop notes in
`CLAUDE.md`. Read `docs/CODEX_TAKEOVER_0913.md` for the measured takeover baseline.
Older README branch names, passovers, and test counts are historical; verify the
current Git state and runtime before relying on them.

## Working on this build

- Mike owns creative and design decisions. Continue his requested work using the
  existing authored assets and encounter specifications.
- Preserve existing staged, unstaged, and untracked work. Commit or push only when
  Mike asks. Inspect incoming GitHub changes before integrating them.
- Have one writer at a time for `assets/game.js`. Preserve its LF line endings and
  the CRLF line endings in `_BUILD_SOURCE/test_fl.js`.
- Available disk space is limited. Avoid full repository copies and worktrees.
  Keep temporary verification output under the ignored `_shots/` directory.
- Do not delete user data or trailer scratch files without explicit authorization.
  Do not expose secrets or SpriteCook signed URLs.

## Creative constraints

- Use authored art; do not add placeholder or procedural sprites. Render candidate
  art before trusting its name. Consult `assets/data/ART_TAXONOMY.json`.
- Preserve authored stage biomes. Palette changes must retain luminance, outlines,
  and the authored colors of ordnance.
- Bosses remain whole authored plates. The approved Furnace Tyrant head phase is
  a named exception. Approved miniboss aperture mechanics and the two independent
  Tempest ships are separate encounter designs.
- Player death remains hit, anchored burning spin through 540–900 degrees, crash,
  then shock ring and explosions. Space deaths use the spaceship.
- Read `docs/ATLAS_REPACK_0903.md` before editing an atlas. Register sheet and cell
  changes together; generated manifests require their owning build workflow.

## Verification

For gameplay edits, run `node --check assets/game.js` and
`node _BUILD_SOURCE/test_fl.js`. Confirm the suite reaches its final summary and
compare failing assertion names with the recorded baseline; a nonzero suite exit
must be reported even when failures predate the change.

Verify visible behavior in real Chromium using `_BUILD_SOURCE/shoot.py` and the
relevant existing probe. Inspect screenshots and both page and console errors.
State assertions alone do not verify pixels. Check local art through `XART.get`
keys and the game context's own `drawImage`; cached canvases have no reliable
`.src` or object identity. Poll lazy asset readiness and yield between frame batches.
