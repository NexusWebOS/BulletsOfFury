# Native enemy catalogue — 13 October 2026

The guide catalogue is `assets/data/enemy_atlas_1013.json`. Its 393 stable entries
cover 361 main-game identities and 32 Overdrive identities. The inventory keeps
old constructor names visible and labels them instead of silently dropping them.

| Status | Entries | Meaning |
| --- | ---: | --- |
| Current | 185 | Current main-game stage, form, route or password selection |
| Expansion | 31 | Current Overdrive unit, boss, form or crew member |
| Legacy spawnable | 100 | Retained main-game constructors not traced in current campaign plans |
| Replaced | 19 | Old names whose live constructors redirect to a newer identity |
| Culled | 1 | Stage-six buoy deliberately suppressed by current code |
| Legacy unverified | 57 | Archived boss constructors, plus the previous Overdrive Fortress |

There are 228 ordinary-enemy, 39 ground, 6 hazard, 4 naval, 29 miniboss, 51 boss,
15 password-boss, 13 form and 8 rebel entries across all statuses. Those are
catalogue rows, not a claim that 393 different opponents appear in a campaign.
The main-game final boss includes its three encounters and all nine copied forms.

Each current main-game row has a described attack list and a primary authored
art key. Source references identify files, symbols and lines. The data retains
native projectile identifiers, controller names, animation-bank metadata, stage
membership evidence and the exact spawn options consumed by the guide adapters.
Source digests make the catalogue's extraction state auditable.

The native guide remains the authority for moving sprites and projectiles. It
invokes the actual game controllers and rendering; the catalogue does not recreate
their combat. Continuous beams, contact attacks, ground impacts and private boss
shot arrays are labelled separately from the general projectile catalogue.

## Important current-route corrections

- Stage-seven Rifle Locust uses machine-gun fire; its pressure turn does not turn
  the gun into a charged laser. Stage-nine Beacon uses native warp-crystal shards.
- HARR6 now selects the six-turret Warhive Siege Carrier. XHARR retains the earlier
  active carrier-and-ace route because it sets the Stage X route flag.
- Warp Sentinels alternate warp crowns and needle fans. Their fusion reveals the
  Tidal Sovereign, which is a current second form with five tidal attack patterns.
- Overdrive's current mission-three boss is Gosfer. Its former Fortress remains
  an explicitly labelled legacy encounter. Mission six is a convoy pursuit and
  has no separate boss. Convoy preview uses `TD.Convoy.spawn` for native movement.

## Rebuilding

The owning scripts live in `tools/enemy_atlas_1013`. Run from the checkout root:

```powershell
python tools/enemy_atlas_1013/export_enemy_atlas_runtime.py --root .
python tools/enemy_atlas_1013/enrich_enemy_atlas_runtime.py --root .
python tools/enemy_atlas_1013/build_enemy_atlas_1013.py --root . --output assets/data/enemy_atlas_1013.json
```

The first two commands require Python Playwright and the game's existing
`_BUILD_SOURCE/shoot.py` dependencies. They open a temporary local server and
native headless browser, then save snapshots under ignored `_shots/enemy_atlas_1013`.
Use `--workdir PATH` to retain or reuse a different snapshot directory. The last
command requires only Python and those snapshots. The small source-reviewed
Overdrive supplement is kept beside the scripts. Re-run extraction after changing
stage plans, aliases, attack books or asset mappings; then review the per-type notes.

## Coverage and limits

The source census starts with 234 constructor candidates, all nine stage plans,
all four difficulty encounter launches, native roster/attack registries, password
catalogues and Overdrive factories. It expands modular emplacement weapon variants
and elite aliases. Current paths resolve both ordinary atlas cells and the later
stage-runtime atlas overrides; raw pre-repack source paths are not used as thumbnails.

The static attack index describes registered and source-reviewed phases. It does
not claim to enumerate every conditional frame, damage-state branch, random volley
or reinforcement route. Native previews demonstrate those behaviors. A legacy
constructor can require archived art or a campaign-only setup; its retained row is
not proof that every historical encounter is still independently playable. The
catalogue itself is not a human balance study or a frame-rate guarantee.
