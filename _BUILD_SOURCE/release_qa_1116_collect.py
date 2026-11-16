from pathlib import Path
import json,hashlib,shutil,re
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116';D=R/'docs/qa';D.mkdir(parents=True,exist_ok=True);S=R/'_ART_SOURCES/release_qa_1116'
def read(p):
 f=O/p
 return json.loads(f.read_text(encoding='utf8'))if f.exists()else{}
def stats(p):
 q=read(p);cs=q.get('checks',[]);return {'passed':sum(bool(c.get('ok',c.get('passed',False)))for c in cs),'failed':sum(not bool(c.get('ok',c.get('passed',False)))for c in cs),'errors':q.get('errors',[]),'evidence':(O/p).relative_to(R).as_posix()}
enc=read('encounters/report.json');weap=read('weapons/report.json');static=read('static-report.json')
report={'date':'2026-11-16','workspace':str(R),'releaseVerdict':'HOLD - broad smoke coverage is not exhaustive release certification','core':static,'coverage':{k:stats(v)for k,v in {'forge':'forge/report.json','online':'online/report.json','controls_modes':'controls-modes/report.json','ending':'cinema/report.json','followup':'followup/report.json'}.items()},'groundWeaponPreviews':{'cases':len(weap.get('rows',[])),'bad':sum(bool(x.get('error'))or not x.get('isolated')or not x.get('peak')for x in weap.get('rows',[])),'errors':weap.get('errors',[]),'scope':weap.get('scope')},'encounters':{'cases':len(enc.get('rows',[])),'errors':enc.get('errors',[]),'originalFlagged':[{'id':q['id'],'checks':q.get('checks')}for q in enc.get('rows',[])if not all(q.get('checks',{}).values())],'followup':'Stage6 entry now passes all four Hard/Furious preview cases. Stationary Stage8 death traced to actual whole-arm swipe after intro replaces temporary invulnerability, not stale space charge. Stage5 stationary death not consistently reproduced; not declared fixed.'},'fixed':['Local co-op controller2 retains its seat when controller1 disconnects/reconnects; solo first-present mapping retained.','Online guest full current multi-canvas HUD, native mixer audio, safe room reopening, focus-loss key release and saved controller bindings.','Standalone Stage6 boss/miniboss preview warning no longer trapped in ordinary prologue/crew conversation.','Ending conversation automatic reading holds for all nine pilot routes.','Current approved orange-vest Juggernaut guitar insert, six preserved whole512x512 poses and exact layered-source round-trip.'],'remaining':['No full unassisted Campaign/Arcade wins across all difficulties/pilots/routes.30-second protected encounter samples do not certify complete multi-form attack books or balance.','No physical8BitDo controller attached. Raw-API boot/remap/disconnect tests do not certify wireless/driver modes.','Online tested on two independent same-machine browser contexts. STUN only; restrictive-NAT/WAN/TURN/reconnect and long-session validation remain.','All enemy types, both co-op pilots in every live weapon/form combination, all ending/workshop artwork, all attack sounds and sustained performance are not exhaustively certified.','Legacy native probes have stale fixtures/assertions: normalized Forge tiers, removed automatic opening specials, old HUD/typewriter owners and removed health test switches. Original failed logs retained; current replacements cover stated scopes only.','Stage6 four-wave natural-input and full space/signature passes remain in progress; do not claim them passed from an aborted legacy probe.'],'noCommitPush':True,'sources':{p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in ['assets/game.js','assets/online.js','assets/release_cinema_1116.js','assets/release_entry_1116.js','_BUILD_SOURCE/test_fl.js','index.html']}}
(D/'release_readiness_1116.json').write_text(json.dumps(report,indent=2),encoding='utf8')
space=read('space/report.json');report['spaceWeaponPreviews']={'cases':len(space.get('rows',[])),'bad':len(space.get('bad',[])),'errors':space.get('errors',[]),'scope':space.get('scope')};report['coverage']['carrier_waves']=stats('carriers/campaign-checks.json')
report['coverage']['special_pickups']=stats('signatures/report.json')
ui=read('ui/report.json');report['menuSurvey']={'cases':len(ui.get('rows',[])),'bad':[r for r in ui.get('rows',[])if not r.get('aspectPreserved')],'errors':ui.get('errors',[]),'scope':ui.get('scope')}
report['legacyProbeResults']={}
for key,path in {'restored_coop':'legacy/overnight_combat_1019/restored-coop/native-report.json','signature_specials':'legacy/signature_specials_1011/report.json'}.items():
 report['legacyProbeResults'][key]=stats(path)
report['fixed'].append('Authored wide Forge/comic canvases preserve their backing-store aspect through legacy fullscreen CSS; native mouse registration and combat HUD restoration verified.')
report['fixed'][4]='Current approved orange-vest Juggernaut guitar insert: six preserved whole512x512 poses, direct270x270 comic exports, both native art registries corrected and actual drawn pixels independently verified.'
report['remaining'].append('Wide menus are proportionate on narrow windows but their labels become too small. A separate responsive layout/readability pass is required before claiming phone support.')
report['remaining'][5]='Stage6 native four-wave retry passes4/4; earlier aborted probe and its renderer exception remain archived. Fresh Edge boot and stepwise fixture isolation pass. Cold-load/performance soak remains a release gate. Fresh native special pickups pass for both tiers/all nine pilots, but all five Rough Rider personal signatures are not freshly certified.'
pace=read('pacing/report.json');report['framePacing']={'scope':pace.get('scope'),'rows':pace.get('rows',[]),'errors':pace.get('errors',[]),'resourceTimingCaveat':'Default browser timing buffer capped the recorded resource list at250; those counters are not the complete request inventory. The749-script count comes from actual shipping HTML.','profile':'_shots/release_qa_1116/profile/hot-stacks.json','notes':'Stage6 median33.3ms/p9983.3ms in this headless sample; sampled drawImage costs point mainly to authored Thunderhead weather tiles. Hardware/GPU/QA-load dependent, not a target-machine benchmark. Stage8 stationary player died after intro protection changes; not a successful encounter clear.'}
(D/'release_readiness_1116.json').write_text(json.dumps(report,indent=2),encoding='utf8')
table='\n'.join('| '+k.replace('_',' ')+' | '+str(v['passed'])+' passed / '+str(v['failed'])+' failed | '+v['evidence']+' |'for k,v in report['coverage'].items())
doc=f'''# Release-readiness QA — November16,2026

**Release verdict: HOLD.** The build is materially improved, but a green core suite and protected encounter fixtures are insufficient to certify a finished game. This pass uses original BOF on D:, not BOFII. No commit, push, deployment or public release occurred.

## Confirmed fixes

'''+ '\n'.join('- '+s for s in report['fixed'])+f'''

## Current evidence

- Baseline and final core suite:8,969 passes /0 errors; no new failing assertion names. Active shipping scripts: {static.get('activeScripts','pending')} parse checks. Engine LF and core test CRLF preserved.
- {report['groundWeaponPreviews']['cases']} eligible native ground pilot/weapon/element previews: no emitter/render exceptions, empty emissions or live-state leaks. Selected native pixels inspected. Preview coverage does not prove combat balance or every projectile collision.
- {report['spaceWeaponPreviews']['cases']} native space previews cover all9 pilots, all5 Laser/Fusion/auto-volley tiers, with no empty emissions, exceptions or state leaks.
- {report['menuSurvey']['cases']} desktop/narrow native menu geometry, pointer-registration and combat-restoration checks pass. The wide Forge is no longer squeezed, but small-window text is still too small for a supported mobile release.
- {report['encounters']['cases']} developer encounter starts sampled on Normal1–5 and Hard/Furious1–9, with original warnings/native AI and held primary input. Full screenshots and page/console/HTTP inspection retained. These are stationary protected smoke fixtures, not human wins. Original failed rows remain visible; separate follow-up resolves all four Stage6 preview-entry cases.
- The two protected-fixture deaths are not hidden: Stage8 traces show a real whole-arm swipe after the intro changes the temporary protection. Stage5 is not consistently reproduced; no invented fix is claimed.
- Two independent online clients use real Supabase anonymous auth/private rooms, WebRTC, native seat2 input, decoded video and decoded mixer audio (positive remote audio peak). Test rooms close through the native owner. This is not WAN/NAT certification.

| Area | Latest checks | Detailed receipt |
|---|---|---|
{table}

## Strict release gates still open

'''+ '\n'.join('- '+s for s in report['remaining'])+'''

The shipping page currently references749 separate JavaScript files. Cold-start/request/decode costs and sustained frame pacing need measured budgets on target hardware. Remaining old runtime graphics paths and baked paired-character scenes also need a deliberate art audit; this pass does not label them all consistent.

Four fresh native-RAF first-form samples (Stages 5, 6, 8, 9; 20 wall-clock seconds each) retained browser errors and frame times. No page/console/HTTP errors occurred. Stage 6 was materially slower here: median 33.3 ms, p95 66.6 ms, p99 83.3 ms. CPU sampling points mainly to `th114Weather` authored tile blits, then native reactor rendering. These software/headless measurements do not certify target-GPU performance. The stationary Stage 8 player death is not a successful fight. Default browser resource-timing buffers cap the separate recorded resource list at 250; that is not the full 749-script inventory. Full logs: `_shots/release_qa_1116/pacing/report.json` and `profile/hot-stacks.json`.

## Test hygiene and reproduction

Temporary evidence is under `_shots/release_qa_1116/`; the review page links raw receipts and actual screenshots. Core before/after hash receipts and original files are under `_ART_SOURCES/release_qa_1116/`. Applied patch recipes are historical; do not run them again against already-patched files. Current probes use the local native HTTP server at127.0.0.1:8765. Legacy probe failures are retained rather than erased or counted as shipping fixes. Detailed current machine receipt: `docs/qa/release_readiness_1116.json`.

No test-generated leaderboard scores or announcements are submitted. Profiles are isolated browser contexts. Current native game/save/reward/damage/health owners remain intact.
'''
doc=doc.replace('November16,2026','November 16, 2026').replace('controller2','controller 2').replace('controller1','controller 1').replace('Stage6','Stage 6').replace('Stage8','Stage 8').replace('Stage5','Stage 5').replace('Normal1','Normal 1').replace('Furious1','Furious 1').replace('whole512x512','whole 512×512').replace('direct270x270','direct 270×270').replace('suite:8,969 passes /0','suite: 8,969 passes / 0').replace('all9','all 9').replace('all5','all 5').replace('routes.30-second','routes. 30-second').replace('physical8BitDo','physical 8BitDo').replace('passes4/4','passes 4/4').replace('references749','references 749').replace('at127.0.0.1','at 127.0.0.1').replace('median33.3ms,p95866? see raw exact receipt','median 33.3 ms; see raw exact receipt')
doc+='''

## Strict beta criticism and next sign-off gates

| Priority | Finding | Required evidence before sign-off |
|---|---|---|
| P1 | Whole-mode wins, alternate routes and complete boss phase books are not certified by short checkpoint samples. | Unassisted complete Campaign/Arcade runs, Boss Rush/Time Attack outcomes, achievement/reward/save verification and both-player failures/revivals. Include Easy/Insanity where earned and available. |
| P1 | Online co-op uses STUN without TURN and was tested on one machine. | Two actual machines on separate networks, restrictive NAT, latency/loss, disconnect/rejoin and long sessions. |
| P1 | One carrier probe hit an initialization exception; subsequent boot/isolation/retry checks passed. The page loads 749 script files. | Repeated cold boots and a sustained target-hardware soak with browser logs, frame-time budgets and memory/request/decode measurements. No production fix is claimed for the unreproduced exception. |
| P1 for competitive release | Public leaderboard results are submitted by the client. | Define trusted submission/anti-cheat requirements and verify authoritative validation before advertising competitive integrity. No forged QA scores were submitted. |
| P2 | Wide layouts preserve proportions but are too small in narrow windows. | A dedicated readable layout and full interaction check before claiming phone support. |
| P2 | The complete art/effect/audio inventory has not received a final visual/auditory audit. | All paired workshop scenes, character identities, attack warnings, hit reactions and attack sounds reviewed in actual play. |

These are observed limitations or missing certification evidence, not a claim that every listed system is broken. The known original legacy-probe failures remain in the machine receipt with their replacement coverage described separately.
'''
(R/'docs/RELEASE_READINESS_1116.md').write_text(doc,encoding='utf8',newline='\n')
# Preserve reproducible native QA recipes beside the project's existing tools.
C=Path(r'C:\Users\Mdogg\Desktop\BOF-CODE\BulletsOfFury\_shots')
files={'release_encounters_1116.py':'release_qa_1116_encounters.py','release_weapons_1116.py':'release_qa_1116_weapons.py','release_forge_flow_1116.py':'release_qa_1116_forge.py','release_online_1116.py':'release_qa_1116_online.py','release_controls_modes_1116.py':'release_qa_1116_controls_modes.py','release_followup_1116.py':'release_qa_1116_followup.py','release_cinema_1116_probe.py':'release_qa_1116_cinema.py','release_cinema_1116_build.py':'release_qa_1116_cinema_build.py','release_fatal_1116.py':'release_qa_1116_fatal.py','release_static_1116.py':'release_qa_1116_static.py','release_checks_1116_run.py':'release_qa_1116_existing_probes.py','release_collect_1116.py':'release_qa_1116_collect.py'}
files.update({'release_space_1116.py':'release_qa_1116_space.py','release_carriers_1116.py':'release_qa_1116_carriers.py','release_edge_isolate_1116.py':'release_qa_1116_edge.py','release_ui_1116.py':'release_qa_1116_ui.py','release_signatures_1116.py':'release_qa_1116_signatures.py','release_pacing_1116.py':'release_qa_1116_pacing.py','release_review_1116.py':'release_qa_1116_review.py'})
files.update({'release_profile_1116.py':'release_qa_1116_profile.py','release_profile_read_1116.py':'release_qa_1116_profile_read.py','release_review_check_1116.py':'release_qa_1116_review_check.py','release_handoff_1116.py':'release_qa_1116_handoff.py'})
for src,dst in files.items():
 if not(C/src).exists():continue
 code=(C/src).read_text(encoding='utf8');code=re.sub(r"R=Path\(r'D:[^']+'\)","R=Path(__file__).resolve().parents[1]",code)
 (R/'_BUILD_SOURCE'/dst).write_text(code,encoding='utf8',newline='\n')
for f in C.glob('patch_*1116.py'):shutil.copyfile(f,S/f.name)
tax=R/'assets/data/ART_TAXONOMY.json';d=json.loads(tax.read_text(encoding='utf8'))
d={'release16_':{'role':'approved_cast_Juggernaut_ending_guitar_identity_correction','owner':'_BUILD_SOURCE/release_qa_1116_cinema_build.py','manifest':'_ART_SOURCES/release_qa_1116/juggernaut-guitar.json','note':'Six preserved512x512 whole poses with orange vest/approved rowB reference. Lossless generated master, editable layered source and exact source round-trip. Native ending timing/readability owner preserved.'},**d}
tax.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({'docs':'docs/RELEASE_READINESS_1116.md','previews':report['groundWeaponPreviews'],'coverage':report['coverage'],'encounters':report['encounters']['cases']}))
