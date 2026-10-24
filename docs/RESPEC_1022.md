# Re-spec on the Forge, the Loadout and Decker's Upgrade Center (2026-10-22)

Mike: *"now we need the option to actually re-spec during between stages in the loadout/forge, and in this new menu during the map"*

## What was wrong
- `forgeRespec` only took the equipped form OFF a weapon. The form stayed earned, and the upgrade (combine) spent on it stayed spent. A loadout swap could already do that for free, so the re-spec changed nothing.
- It lived only on the CHARGE button, with no label. The Forge showed a lone `X0` on its bottom bar.
- The budget (2 upgrades / 2 re-specs) was refilled by `forgeStart`. The map could only offer whatever a Forge visit had left behind. That was nothing on a stage whose Forge never opened (stages 4 and 9, or nothing to do), and nothing after loading a save, because the budget was not saved.

## What a re-spec is now (`assets/respec_1022.js`, `window.RS22_OFF=1` disables)
- **The combination is undone.** Every element forged onto that weapon this run comes off. The weapon goes back to its base form, and each removed combination gives its upgrade back, so the weapon can be forged with a different element straight away. One re-spec per weapon; two per level completion.
- **Confirm step:** the first press arms it and says what will be removed and refunded. A second press on the same weapon within 3 s does it, because it deletes a combination.
- **The Forge:** the bottom bar is now a `X RE-SPEC <weapon>  N LEFT` button. Press CHARGE or click it.
- **The Loadout:** the same button sits above the hint row (`RS22_LOADOUT_BAR`). Press CHARGE or click it.
- **Decker's Upgrade Center:** a new row, `RE-SPEC A WEAPON` (rows are now FORGE / LOADOUT / RE-SPEC / LEAVE). It lists every loadout weapon plus any weapon carrying a forged upgrade. LEFT/RIGHT picks, FIRE arms and then confirms, B returns to Decker's rows.
- **Budget:** granted when a stage is cleared (entering `GS.STAGECLEAR`). `forgeStart` no longer refills it, and the campaign save carries `forgeCombos`, `forgeRespecs` and `rs22Serial`.
- New Game+ purchased recipes (profile `forge_<elem>_<w>_C`) are permanent purchases. They are not removed and not refunded.
- While the chaingun stands in for the MG, re-spec acts on the MG's forms (the same rule as `forgeEntry`).

## Verified
`_BUILD_SOURCE/probe_respec_1022.py` passes 20/0 in real Chromium with real keys, including a busted arm, and logs 0 page/console errors. Proof frames are in `docs/proofs/respec_1022/`. `probe_upgrade_center_1022.py` passes 20/0 (updated for four rows) and `probe_start_menu_1022.py` passes 33/0. The full suite reports 8,956 ok / 0 errors with BUILD OK.
