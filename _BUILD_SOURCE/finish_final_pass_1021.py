from pathlib import Path
import json,shutil,re,hashlib
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';O=R/'_shots/final_version_1021';T=Path(__file__).parent
air=json.loads((S/'air-production-manifest.json').read_text());fx=json.loads((S/'export-audit.json').read_text());assert len(air['models'])==40 and not air['pending'] and len(air['audit'])==2280;assert all(not q['clipped'] for q in fx)
reports={
 'edge_contracts':O/'contracts/msedge-report.json',
 'edge_air_actions':O/'air-actions/msedge.json',
 'chrome_air_actions':O/'air-actions/chrome.json',
 'firefox_air_actions':O/'air-actions/firefox.json',
 'hammer_and_shields':O/'native/report.json',
 'contacts_and_audio':O/'contacts/report.json',
 'environment':O/'environment/report.json'}
verification={}
for name,p in reports.items():
 d=json.loads(p.read_text());assert not d['errors'],(name,d['errors']);assert all(c.get('ok',c.get('passed')) for c in d['checks']),name;verification[name]={'checks':len(d['checks']),'passed':True,'report':str(p.relative_to(R))}
log=R/'_shots/final-version-regression-1021-complete.log';text=log.read_text(encoding='utf-8');assert text.rstrip().endswith('==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====');count=len(re.findall(r'^  ok ',text,re.M));assert count==8943,count
review=json.loads((O/'review-qa.json').read_text());assert not review['errors'] and all(not r['overflow'] and r['models']==40 for r in review['rows'])
allies=json.loads((O/'ally-defense.json').read_text());assert not allies['errors'] and len(allies['rows'])==4 and all(r['targeted'] and r['alliedShots']>0 and r['intercepted'] for r in allies['rows']);verification['allied_missile_defense']={'difficulties':4,'passed':True,'report':'_shots/final_version_1021/ally-defense.json'}
assert b'\r\n' not in (R/'assets/game.js').read_bytes();test=(R/'_BUILD_SOURCE/test_fl.js').read_bytes();assert test.count(b'\n')==test.count(b'\r\n')
for name in ['collect_final_assets_1021.py','build_final_effects_1021.py','build_air_refit_1021.py','build_coastal_city_1021.py','build_final_review_1021.py','probe_final_contracts_1021.py','probe_final_contacts_1021.py','probe_final_environment_1021.py','probe_final_art_1021.py','profile_final_runtime_1021.py','probe_final_air_actions_1021.py','probe_final_review_1021.py','probe_final_ally_defense_1021.py','inspect_final_banks_1021.py','register_final_art_1021.py']:
 shutil.copyfile(T/name,R/'_BUILD_SOURCE'/name)
for p in T.glob('final21_*.json'):shutil.copyfile(p,S/p.name)
summary={'complete':True,'regression':{'assertions':count,'errors':0,'exit':0,'log':str(log.relative_to(R))},'native':verification,'review':review,'art':{'aircraft':40,'designIDsIncludingFamilies':53,'motionPosesPlusIdle':2280,'effectFrames':sum(q['frames'] for q in fx),'clippedFrames':0,'airRuntimeBytes':sum((R/a['path']).stat().st_size for a in air['sheets'].values())},'credits':{'startingDisplayedUSD':10.58,'closingDisplayedUSD':2.91,'accountPurchasePerformed':False},'reviewURL':'http://127.0.0.1:8794/_shots/final_version_1021/review.html'}
(S/'verification-final.json').write_text(json.dumps(summary,indent=2));state=json.loads((S/'work-scope.json').read_text())
for q in state['tasks']:q['status']='complete; verified in verification-final.json and docs/FINAL_VERSION_1021.md'
state['final_checkpoint']='Completed all requested art/combat integration and native validation.160 motion jobs plus one targeted axial-roll correction finished; no generation jobs remain pending. Cinematic concepts ready for user selection. Existing unrelated work preserved; no GitHub push.'
state['final_validation']=summary;(S/'work-scope.json').write_text(json.dumps(state,indent=2))
p=R/'docs/FINAL_VERSION_1021.md';s=p.read_text(encoding='utf-8').split('\n## Final verification record\n')[0];s+='''
## Final verification record

The finished build has155/155 native Edge contract checks,176/176 native aircraft-action checks in each of Edge/Chrome/Firefox,68/68 Hammer/shield checks,21/21 actual-contact/audio checks and8/8 carrier/city checks. Review works at1440px and390px without overflow. Runtime aircraft atlases total under2.6MB for all40 designs;558 new effect/actor poses and2,280 aircraft poses have no clipped frame edges. One weak silver-fighter roll bank was replaced by an approved true axial roll; unwanted generated purple coloration was corrected offline against each approved master palette. Native source aliases remove retired flight-texture readiness dependencies while retaining destruction reels. Nested renderers now honor the selected somersault bank.

Actual allied guns deliberately acquire and destroy incoming Rebel missiles on all four difficulties; this supplements the verified player interception path. Existing supply and dodge priorities remain.

PixelLab displayed balance:10.58USD at the verified start,2.91USD after generation. No account purchase was performed. Receipts and rejected experiments are retained outside runtime assets. No jobs remain pending. The cinematic concepts are ready for Mike's selection.
''';p.write_text(s,encoding='utf-8',newline='\n');print(json.dumps(summary['art']));print('All final verification gates passed. Production notes, source tools and task ledger are complete.')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('v=final-version-1021-2','v=final-version-1021-3');p.write_text(s,encoding='utf-8',newline='\n')
