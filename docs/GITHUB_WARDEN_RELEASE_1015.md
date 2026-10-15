# Warden repair publication — October 15, 2026

Mike requested updating GitHub with the completed Stage 4 miniboss repair.
The release restores native hit feedback on the Warden, modules, helpers and
formation aircraft, records that engine rule, gives the Warden longer committed
warnings and finite attack bursts, and separates helper turns from its attacks.
Helpers are 50% larger in combat, use regular-family health, and have their own
entry and firing warnings. The fight uses enemy-specific gun audio and the
approved missile chip launch cue. Existing authored graphics and sound banks
are retained.

The source SHA-256 matches docs/qa/warden_readability_1014.json. Validation:
55 focused native checks across all four difficulties, 60 existing Stage 3–4
gameplay checks, 13 visual checks, and the full 8,700-check regression suite;
zero errors, final BUILD OK and exit 0. Source syntax and scoped whitespace
checks pass. Native pixels and nonzero decoded attack audio were inspected.
The steering samples are controlled fixtures, not human campaign-clear proof.

Before publication, origin/main was fetched and its two FURYBOT/trailer commits
were reviewed. They change tools/documentation without touching the gameplay
runtime. They were fast-forwarded at 58f32167b before this commit. No force push
is used. Separate pending Overdrive gameplay, art, audio, options and QA remain
local, as does the old Contra prototype scratch. Only the Warden section and
this release summary are staged from the shared project handoff.

Tuning and reproduction: docs/WARDEN_READABILITY_1014.md.
Evidence: docs/qa/warden_readability_1014.json.
