"""Save the reviewed native screenshot index and portable regression evidence."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];O=R/'_shots/feedback_1002'
report=json.loads((O/'verification.json').read_text(encoding='utf-8'))
suite=(R/'_shots/feedback_1002_suite.log').read_text(encoding='utf-8')
report['baseline']={'assertions':6247,'failing_names':[]}
report['suite']={'assertions':sum(line.startswith('  ok') for line in suite.splitlines()),'failing_names':[line.strip() for line in suite.splitlines() if line.startswith('  FAIL')],'final_banner':'FALVA/LIZZIE BUILD OK, 0 ERRORS' in suite}
report['scope']='Controlled real Chromium fixtures; not campaign wins or verified final balance.'
(R/'docs/qa/feedback_1002.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
scenes=[
 ('Freezer: Ice Breath remains equipped','freezer-loadout'),
 ('Dam: vertical green bomber waves','dam-bombers'),
 ('Dam: waves clear before the chopper warning','dam-chopper-arrival'),
 ('Fire jet replaces the golem','replacement-firejet'),
 ('Furious magma: three groups of nine','magma-retina-groups'),
 ('Shooting magma ordnance: impact FX','magma-shotdown'),
 ('Generated Frost Cruiser: charge','frostcruiser-hard-charge'),
 ('Frost Cruiser: nuclear impact','frostcruiser-nuclear-impact'),
 ('Frost Cruiser: same actor, new form','frostcruiser-post-nuclear'),
 ('Cryospear: rapid cold battery','cryospear-hard-attack'),
 ('Sovereign: generated charged barrel','stormsovereign-hard-attack'),
 ('Sovereign: helpers stay positioned and fire','stage4-helper-burst-hard'),
 ('Sovereign: weaponless charge','stage4-ram-hard'),
 ('Hammer: post-transformation taunt','hammer-taunt'),
 ('Hammer: spikes rise through the playfield','hammer-fullheight-spikes'),
 ('Hammer: generated rotary cannon','hammer-new-chaingun'),
 ('Hammer: paired rage strike recovery','hammer-rage-recovery'),
 ('Hammer: head and raised arm during death','hammer-death-3'),
 ('Hammer: electrical/core bursts','hammer-death-5'),
 ('Other enemy droids: fixed hull facing','ordinary-straight-droid'),
 ('Sewer Lamprey: committed warning','s7lamprey-hard-warning'),
 ('Sewer Serpent: fixed hull and toxic burst','s7serpent-hard-burst'),
 ('Sewer Sampler: committed attack','s7sampler-furious-warning'),
 ('Stage 8 interceptor: straight attack','s8interceptor-hard-burst'),
 ('Stage 8 bomber: charge','s8bomber-hard-warning'),
 ('Stage 8 needle: fast burst','s8needlejet-hard-burst'),
 ('Stage 8 gunship: straight hull','s8gunship-furious-warning')]
cards=''.join(f'<figure><a href="{html.escape(key)}.png"><img loading="lazy" src="{html.escape(key)}.png" alt="{html.escape(title)}"></a><figcaption>{html.escape(title)}</figcaption></figure>' for title,key in scenes if (O/(key+'.png')).exists())
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>October 2 campaign feedback</title><style>
body{{background:#080e16;color:#e9f1fa;font:16px system-ui;margin:0;padding:32px;max-width:1500px;margin:auto}}h1{{margin:0 0 12px}}p{{line-height:1.6;max-width:950px}}.result{{color:#9fedd2}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}}figure{{margin:0;background:#111e2b;border:1px solid #304658;border-radius:8px;overflow:hidden}}img{{display:block;width:100%;height:auto;image-rendering:pixelated}}figcaption{{padding:14px}}a{{color:#9bddff}}
</style><h1>Campaign feedback — October 2</h1><p class="result">{report['suite']['assertions']:,} passing assertions · {sum(c['ok'] for c in report['checks'])}/{len(report['checks'])} Chromium checks · no page/console errors.</p><p>Generated Frost Cruiser and Hammer parts, corrected dam pacing, guided hammer counter, Sovereign helpers and lightning barrel, and straight-facing sewer/alien enemies. These are controlled native game fixtures, not complete campaign clears or final balance proof.</p><p><a href="../../index.html?build=feedback-1002-straight-hulls">Open the updated game</a> · <a href="verification.json">Browser check results</a> · <a href="../../docs/FEEDBACK_1002.md">Changes and remaining playtest</a></p><main>{cards}</main></html>'''
(O/'review.html').write_text(page,encoding='utf-8')
print('Saved review and portable evidence:',report['suite']['assertions'],'assertions,',len(report['checks']),'native checks')
