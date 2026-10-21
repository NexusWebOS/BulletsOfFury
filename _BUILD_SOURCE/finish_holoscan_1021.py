from pathlib import Path
import json,re,shutil
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;Q=R/'_shots/holoscan_1021';A=R/'_ART_SOURCES/holoscan_1021'
checks={}
for name in ['msedge','chrome','firefox']:
 d=json.loads((Q/(name+'-checks.json')).read_text());assert not d['errors'] and all(c['ok'] for c in d['checks']),name;checks[name]=dict(passed=len(d['checks']),errors=[])
combat=json.loads((R/'_shots/instructor_bob_1020/report.json').read_text());assert combat['passed']==combat['total'] and not combat['errors'];checks['tutorial_combat']=dict(passed=combat['total'],errors=[])
shutil.copy2(R/'_shots/instructor_bob_1020/report.json',Q/'tutorial-combat-checks.json')
d=json.loads((Q/'review-checks.json').read_text());assert not d['errors'] and all(c['ok'] for c in d['checks']);checks['interactive_review']=dict(passed=len(d['checks']),errors=[])
log=(Q/'full-suite.log').read_text(encoding='utf-8');assert 'BUILD OK, 0 ERRORS' in log;count=len(re.findall(r'^  ok  ',log,re.M));checks['full_suite']=dict(assertions=count,errors=0,exit=0)
assets=json.loads((A/'asset-manifest.json').read_text());summary=dict(selectedConcept=2,implemented=True,checks=checks,asset_bytes=assets['runtimeBytes'],new_pixel_lab_generations=0,cole_likeness_approved=False,published_to_github=False)
(A/'verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(Q/'verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
doc='''# B.O.B. Holoscan dossier — October21, 2026

Mike selected concept02 (Holoscan / Exploded View). The tutorial now uses that direction as its live dossier. The copied Overdrive window is no longer rendered or included in tutorial readiness/decode dependencies. Its source record remains for reproducibility.

## Live design

A newly generated empty cyan/black BOF scan frame supplies preserved corners, dark grid and holographic floor; the accepted concept supplies the floor dais. All delivered crops are even-sized. The frame uses corner-preserving nine-slice edges, not a stretched portrait plate. The new frame assets total1,183,916bytes. No new robot or animation generation was purchased: the four accepted PixelLab32-pose turntables are reused.

The full-unit view separates the actual missile pod, ice reactor and cannon. Four selectors include the complete assembled unit and each independent module. Dragging, native left/right or the turn buttons change the authored yaw frames. No flat-image spinning is used. Native up/down and Back retain their existing meanings. Live text uses the corrected BOF Iron Signal font; names and values remain text, rather than baked concept lettering.

Desktop uses the large exploded view, four thumbnails and three bottom intelligence panels. Compact screens use a horizontal part selector and one focused detail panel. Very short displays scroll inside the bounded window and keep Deploy available, preserving readable text instead of shrinking the whole page. Native screenshots cover1920×1080,1366×768,768×1024,390×844,320×568 and844×390. All text fits its regions; dimensions are even.

## Actual combat data

`BOB20_SPEC` in `assets/instructor_bob_1020.js` is shared by the exam spawn and dossier: missile90HP, cannon110HP, reactor240HP, total440HP. Both pods gate the ice reactor. Native fire damage is×1.5, ice×0.5; exposed-core missiles are×2. The concept's invented dimensions, cryogenic cannon description and blanket armor claims are not presented as game rules. The live cannon remains a steel FOV cannon; the launcher owns ground strikes.

The pointer Deploy button queues the native card confirm; the original3.8s scan gate and lesson completion own progression. The card continues to freeze combat/ammo/stage scheduling. Start opens the actual pause/skip menu and temporarily hides the modal. Resume preserves selection and auto-rotation preference. Reduced-motion settings stop automatic rotation while keeping manual turns. A closed/exited dossier releases its canvas buffers. The existing tutorial render tick drives the UI; no additional animation loop or per-frame pixel readback was added.

## Ownership and reproduction

- Runtime: `assets/holoscan_dossier_1021.js` and its scoped CSS, loaded after the native instructor and latest combat owners.
- Art: `assets/game/shared/ui/holoscan_1021/`.
- Sources and prompt provenance: `_ART_SOURCES/holoscan_1021/`.
- Builders: `_BUILD_SOURCE/build_holoscan_1021.py` and `build_holoscan_review_1021.py`.
- Native probes: `probe_holoscan_1021.py`, `probe_instructor_bob_1020.py`, `check_holoscan_review_1021.py`.
- Review: `_shots/holoscan_1021/review.html`; its interactive iframe uses the existing save-isolated preview bootstrap. Native selection, deploy and restart were checked against unchanged persistent storage.

The legacy turntable probe observed `ctx.drawImage` on the gameplay canvas. Its observer now watches the actual selected DOM thumbnail canvas. The four-bank/four-yaw distinct-source-rectangle assertion is retained, and the initial old-observer26/27 report is preserved beside the final27/27 result. Native damaged-pixel, weakness, missile, audio, module removal and handoff assertions remain.

## Verification

'''
doc+='- Full required regression:'+str(count)+' assertions; final BUILD OK / zero errors; exit0.\n'
for k,d in checks.items():
 if k!='full_suite':doc+='- '+k.replace('_',' ')+':'+str(d['passed'])+' passing checks; zero browser/page/resource errors.\n'
doc+='\nCore `game.js`, the regression harness and existing pilot art remain unchanged. The instructor owner now reads shared stats and accepts the pointer confirm queue; its combat numbers are preserved. Native audio remains owned by the shared mixer. Cole\u2019s likeness is still unapproved, and the other eight pilots\u2019 new cinematic banks remain on hold. No GitHub publish was requested or performed.\n'
(R/'docs/HOLOSCAN_1021.md').write_text(doc,encoding='utf-8')
# Preserve the selected decision in old review links instead of leaving an active
# instruction to choose again.
p=R/'_shots/menu_heart_1021/review.html';s=p.read_text(encoding='utf-8');s=s.replace('The preview concepts are choices for your review, not installed replacements.','Concept02, Holoscan / Exploded View, is selected and implemented. <a href="/_shots/holoscan_1021/review.html">Open the live Holoscan review.</a> Other concepts remain available for future expansions.');p.write_text(s,encoding='utf-8')
for file,marker,note in [
 ('HANDOFF_CODEX.md','## October21 — selected Holoscan dossier','Mike selected concept02. The new native tutorial dossier is live: generated cyan frame, actual exploded modular turntables, shared BOB20_SPEC, DOM text/compact layout, native scan/deploy/pause/skip and buffer retirement.104 UI checks across Edge/Chrome/Firefox (including every turntable pose at thumbnail/detail edges),27 combat/lesson checks,8 interactive-review checks; full8943/0/exit0. See docs/HOLOSCAN_1021.md and _shots/holoscan_1021/review.html. Cole still needs review; other8 cinematic banks stay on hold. No push requested.'),
 ('docs/MENU_HEART_1021.md','## Selected dossier — October21','Mike selected Holoscan / Exploded View (02), now implemented. The five-concept selection is resolved. See HOLOSCAN_1021.md and ../_shots/holoscan_1021/review.html. The remaining concepts stay archived for future expansions.'),
 ('docs/INSTRUCTOR_BOB_1020.md','## Superseded dossier — October21','The copied Overdrive card and its former layout are replaced by the approved Holoscan owner. The four actual turntables, module anatomy, HP, native targeting, audio and training rules remain. See HOLOSCAN_1021.md for current layout and verification.')]:
  p=R/file;s=p.read_text(encoding='utf-8')
  if marker not in s:p.write_text(s+'\n\n'+marker+'\n\n'+note+'\n',encoding='utf-8')
  else:
   start=s.index(marker);end=s.find('\n## ',start+len(marker));tail=s[end:] if end>=0 else '';p.write_text(s[:start]+marker+'\n\n'+note+'\n'+tail,encoding='utf-8')
for name in ['build_holoscan_1021.py','probe_holoscan_1021.py','build_holoscan_review_1021.py','review_holoscan_1021.js','check_holoscan_review_1021.py','finish_holoscan_1021.py']:
 source=W/name
 if source.resolve()!=(R/'_BUILD_SOURCE'/name).resolve():shutil.copy2(source,R/'_BUILD_SOURCE'/name)
print(json.dumps(summary,indent=2))
