from pathlib import Path
R=Path(__file__).resolve().parents[1]
for src,dst in [('kit_dialogue_1114_probe.py','night_kit_probe_1116.py'),('kit_dialogue_1114_verify_final.py','night_kit_pixels_1116.py')]:
 s=(R/'_BUILD_SOURCE'/src).read_text(encoding='utf8')
 s=s.replace("R=Path(r'D:\\BOF-Downloads\\2026-11-14\\RevG-source')",'R=Path(__file__).resolve().parents[1]')
 s=s.replace("O=R/'_shots/kit_dialogue_1114';","O=R/'_shots/cinema_overnight_1116/kit';O.mkdir(parents=True,exist_ok=True);")
 s=s.replace('p.evaluate(shoot.TRAP_RAF)',"p.evaluate(shoot.TRAP_RAF);p.evaluate('()=>BOFOnline.submitScore=()=>{}')")
 (R/'_BUILD_SOURCE'/dst).write_text(s,encoding='utf8',newline='\n')
# Preserve the original failed fixture logs. Record what they actually tested.
p=R/'docs/CINEMA_OVERNIGHT_1116.md'
note='''
## Checkpoint — 4:20 AM EST

- Fresh native-startRun arrival sweep finished18/18: all nine Stage7 approaches, every other numbered arrival with Cole, and Decker+Cole co-op. All ten Stage7 visits played the actual once-only approach. Co-op end positions340/280 are separate. No stage7 player jumps, page/console/asset errors or STEP errors. Stage6's15 position changes belong to its scripted opening interception; no ordinary combat-teleport claim. Screenshots show all nine ships visible.
- Required-art delay guards5/5, native director139/139, corrected conference art9/9 (independent source decode + all4 actual native drawn crops). Friendly metal-dialogue dispatch4/4:36 crew and40 enemy cases; actual Decker ally-menu screenshot keeps the standard crew frame. Current `night_cinema_1116.js?v=4` and `night_hq_art_1116.js?v=1` are loaded last.
- Opening107.82s native crawl reaches all five backgrounds and its callback. All9 Stage1 comic traversals complete; actual full-text holds4.0–5.08s. Approved current cockpit screenshots retained. This is native-owner/checkpoint evidence, not nine human campaign runs. A real-time opening/map movie is recording separately.
- Current Stage8 possession/whole-shoulder probe26/26: intact HP and anchored pilot through entrance, both portals, visible UFO/bomb/code timing, full-white host reveal, mixer cue routing, protected core, actual arm damage/break effects and no browser errors.
- Earlier drone probe is obsolete: RD71/RD94 superseded its `RD29.last.gate` schema and `rd29CodeSkin` draw owner. Its original fail/KeyError is retained in drone.log. Old return-boundaries probe8/17 uses direct HP zero writes that no longer exhaust the actual copy ledger, so it does not establish a transfer bug; its raw9 failures remain. A continuous native-input GOD bot now fights Stage8 with no enemy HP, phase or timer writes to inspect current transitions. This will not certify human difficulty balance.
- Chronos death/return movie32.89s and HQ→Stage6 movie82.97s both have decoded video/audio, peaks0.784/0.750 and no browser errors. Contact boards reviewed: native death, Earth return, arrival/walk-in, welcome/radar, staggered launches, five-second quiet interval, enemy attack, Decker/Axel defense+escape and Stage6 opening. Chronos recorder's old expected `overhead/surface/aftermath/welcome/descent` tags are superseded by HQ19; its failed legacy assertion is retained. Actual native state correctly reached StageClear. The two clips omit intervening result/equipment menus and are prepared cinematic checkpoints, not a boss combat win.

No commit/push. Engine and main suite bytes remain unchanged overnight; final suite/syntax/hash receipts still pending.
'''
if '## Checkpoint — 4:20 AM EST'not in p.read_text(encoding='utf8'):
 with p.open('a',encoding='utf8',newline='\n')as f:f.write(note)
print('Prepared native assembly/pixel checks and saved current evidence limits')
