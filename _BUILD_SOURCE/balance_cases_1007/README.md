# Balance measurement fixtures — October 7, 2026

These fixtures drive the real local game in native Chromium. They do not change gameplay or submit online scores. Results are test-controller observations, not human win rates. Read `docs/BALANCE_PASS_1007.md` before interpreting them.

Requirements: Python 3, Playwright and its Chromium browser, plus the existing `_BUILD_SOURCE/shoot.py` helper. Run from the repository root. If necessary, install Playwright in your chosen Python environment with `python -m pip install playwright` and `python -m playwright install chromium`.

Run the strongest Stage 5 pacing confirmation with a separate browser context for every case:

```powershell
python _BUILD_SOURCE/balance_pass_1007.py --cases _BUILD_SOURCE/balance_cases_1007/balance_fresh_entry_1007.json --out balance_1007/fresh_entry --fresh-case
```

Keep new A/B outputs in a distinct folder so the original evidence stays available:

```powershell
python _BUILD_SOURCE/balance_pass_1007.py --cases _BUILD_SOURCE/balance_cases_1007/balance_followups_1007.json --out balance_candidate/followups --fresh-case
```

The runner advances at 60 simulation steps/second and draws every six steps. Attack controls can specify 30 simulation steps/second. This is accelerated testing, not a hardware frame-rate benchmark. All external network requests are blocked in the test context.

| Vector | Cases | Purpose |
|---|---:|---|
| balance_matrix_1007.json | 72 | Eighteen encounters/forms across four difficulties |
| balance_attack_cases_1007.json | 108 | Rift, hook and cross; position/reaction/difficulty matrix |
| balance_attack_controls_1007.json | 24 | Stationary damage controls and 30-Hz movement checks |
| balance_followups_1007.json | 415 | Equipment, pilots, co-op HP, recovery, pools, finale attempts and repeat controls |
| balance_confirmations_1007.json | 124 | Native entrance, supported/range-aware weapons, and active/mixed/missing co-op partner |
| balance_selected_mg_1007.json | 9 | Use actual primary-selection API to retain MG on all pilots |
| balance_fresh_entry_1007.json | 50 | Forty-eight fresh-context entry cases plus two exact repeats |
| balance_native_entry_1007.json | 48 | Original entrance subset, also included in confirmations |

Use the corresponding filename and a distinct `--out` folder for any vector. `--resume` skips completed case IDs; combine it with `--fresh-case` for independently initialized comparisons. Original exploratory runs used shared contexts and are preserved with that limitation. The Stage 6 default primary upgrade is intentional, including Cole: a requested weapon 0 often becomes effective weapon 7. Explicit MG fixtures use the real Forge selection. Nine invalid Orb cases in the original screening vector remain in the audit history and are excluded from conclusions; `owned-yuri-8` is the supported follow-up.

Stage slices use a separate legacy controller with rolls, somersaults and bombs:

```powershell
python _BUILD_SOURCE/balance_stage_slices_1007.py
```

That command measures 120 simulated seconds of each stage/mode, not a campaign clear. An optional list of stage numbers restricts it, for example `python _BUILD_SOURCE/balance_stage_slices_1007.py 4 6 8`.

After all eight report groups exist under `_shots/balance_1007`, regenerate the portable summary:

```powershell
python _BUILD_SOURCE/summarize_balance_1007.py
```

The summary validates case counts, damage controls, finite-motion flags, explicit MG identity and the final fresh-browser repeat. It preserves the failed shared-context reproducibility diagnostic instead of silently turning it into a pass. Raw traces and captures remain local under `_shots`; portable JSON/CSV and the human-session sheet live under `docs/qa`.

For future A/B balancing, use fresh contexts, keep pilot/equipment/seed/reaction delay constant, compare multiple seeds, and review actual pixels. Do not combine the two controllers into a single claimed skill level. Full human campaign/finale clears, pickup routing, specials/bombs, all Forge variants, deliberate cheese and exhaustive attack overlaps remain separate work.
