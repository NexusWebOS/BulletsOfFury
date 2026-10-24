from pathlib import Path
import json,shutil,hashlib,subprocess,re
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
S=R/'_BUILD_SOURCE/encounter_revision_1023';Q=R/'_shots/encounter_revision_1023';S.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
contracts=json.loads((W/'native-contracts-extended.json').read_text());visual=json.loads((W/'visual-probe.json').read_text());playback=json.loads((W/'corrections-playback.json').read_text());clips=json.loads((W/'review/clips.json').read_text());art=json.loads((W/'art-integrity.json').read_text());audio=json.loads((W/'audio-final.json').read_text())
assert all(contracts['checks'].values()) and not contracts['errors']
assert visual['pass'] and playback['pass'] and audio['pass'] and art['pass']
assert len(clips)==12 and all(c['completed'] and not c['pageExceptions'] and not c['assetErrors'] for c in clips)
live=json.loads((W/'rebirth-live.json').read_text());assert not live['errors'];assert live['states'][-1]['arena']==live['states'][-1]['background']['phase']==2;assert live['states'][-1]['bolts']==24
assert 'BUILD OK, 0 ERRORS' in (W/'core-final.log').read_text(encoding='utf-8')

# One script owner per file. Re-running the installer is a stable operation.
index=R/'index.html';before=index.read_bytes();subprocess.run([r'C:/Users/Mike/AppData/Local/Programs/Python/Python312/python.exe',str(W/'install_latest.py')],check=True);assert index.read_bytes()==before
src=re.findall(r'<script[^>]*src="([^"]+)"',index.read_text(encoding='utf-8'));owners=[s.split('?')[0] for s in src];assert len(owners)==len(set(owners))

code=['encounter_revision_1023.js','dracodia_rebirth_1023.js','encounter_revision_art_1023.js','build_revision_art.py','build_turrets.py','install_latest.py','native_contracts.py','native_contracts_extended.py','visual_probe.py','rebirth_live_probe.py','record_final.py','build_review.py','serve_range.py','verify_corrections.py','finalize_pass.py']
meta=['art_meta.json','v18_meta.json','nb23_meta.json','d20_art.json','dr21_art.json','fv21_meta.json','art-manifest.json']
for name in code+meta:shutil.copy2(W/name,S/name)
for folder in ['charge_blue_retry','corrupt_charge','roll_fold','roll_smooth','symbiote_smooth','symbiote_fusion','stun_loop','symbiote_ref']:
 shutil.copytree(W/folder,S/folder,dirs_exist_ok=True)
for name in ['charge_blue.png','charge_corrupt.png','ball-reference.png','stun-reference.png']:
 if (W/name).exists():shutil.copy2(W/name,S/name)
for f in (W/'art').glob('*'):shutil.copy2(f,S/'art'/f.name) if (S/'art').exists() else None
# The existing runtime assets are installed. Seed manifests allow clean rebuilds:
# build_turrets.py, then build_revision_art.py, then install_latest.py.
p=S/'record_final.py';s=p.read_text();s=s.replace("B=W.parent/'BOF-Furious-Bot-1023'","B=(W.parent/'furious_bot_1023') if (W.parent/'furious_bot_1023').exists() else W.parent/'BOF-Furious-Bot-1023'");p.write_text(s)
report_files=['native-contracts-extended.json','visual-probe.json','rebirth-live.json','art-integrity.json','syntax-final.json','audio-final.json','corrections-playback.json','gallery-playback.json','core-final.log']
for name in report_files:shutil.copy2(W/name,Q/name)
shutil.copytree(W/'visual',Q/'visual',dirs_exist_ok=True)
for c in clips:shutil.copy2(Path(c['report']),Q/(c['id']+'.json'))

provenance={
 'creditsUsedUSD':.63,'bonusGenerationsUsed':3,'lastObservedBalanceUSD':3.47,
 'accepted':{
  'blue_charge':'7d4165af-ccc0-4738-904e-6a65c25d3ddb','corrupt_charge':'a1b6093d-08bb-4de9-9f8e-b738f95fbee8',
  'fold':'c45f6399-3d1b-4399-9ed8-7eeb791f479c','rolling_core_24':'1f4fcdb0-a803-44ca-b240-a72ad8b92c99',
  'symbiote_24':'63a1c6cd-9a7d-4202-97c3-22dfb202bc93','fusion':'51d40edf-8f45-4c56-8fee-c0a37553ed89','stun':'77ef4175-1978-4dd7-99bf-27c62c5d2ccb'},
 'rejectedOrSuperseded':{'7ac7f889-6463-4fc0-a3dd-147277ea3ab1':'hammer changed during charging','ae7dc7d7-1aa4-4875-bb08-85db1d15ed3f':'fold did not reach the intended ball silhouette','3ede2bef-973b-4334-937d-15daa3636728':'swayed instead of showing genuine changing views','4d930f7b-53e7-45d7-a183-f3ba7e434714':'superseded by 24-frame changing-view matter loop'},
 'existingArtReused':['canonical HF22 hammer designs','approved FV21 PixelLab shield wall','NB23 animated laser flow','D20 lightning/portal effects','PT11 Frost Cruiser turret plates'],
 'offlineVariants':['49 fixed-pivot turret angles per mount, with hit plates','chromium/red charge palettes','red eye and eye-charge plates','four laser directions','24 red spike-ball counter angles','black/white dither curtain tiles']}
(S/'provenance.json').write_text(json.dumps(provenance,indent=2))
summary={'nativeContracts':len(contracts['checks']),'visualChecks':len(visual['checks']),'artChecks':len(art['checks']),'videos':len(clips),'videoPlayback':playback['pass'],'oldVideoPlayback':json.loads((W/'gallery-playback.json').read_text())['pass'],'coreSuite':'0 errors','liveRebirth':'new arena visible; 24 lightning beats','scriptOwnersUnique':True,'installerIdempotent':True}
(W/'final-summary.json').write_text(json.dumps(summary,indent=2));shutil.copy2(W/'final-summary.json',Q/'final-summary.json')
lines=['# October 23–24 encounter correction pass','',
 'Implemented in the local BOF build. Review: http://127.0.0.1:62566/corrections/index.html','',
 '| Encounter | Correction |','|---|---|',
 '| Siege tanks | Sonic pressure waves are protected from offensive interception from their first frame; physical missiles remain interceptable. |',
 '| Stage 2 Inferno Reaver | Separate real HP budgets for every wing, gun and nose. Core damage is locked until all modules break. |',
 '| Frost Cruiser, Rime Wall, Olive Warden | Ordinary projectile corridors reach live rear racks. Frost guns/racks use stored fixed-pivot rotational frames and matching hit plates. |',
 '| Storm Sovereign | Generator/core hit regions and firing corridors are reachable. One half-health shield rebuild; final quarter-health cannon deployment retained. Latest Furious take: 81.19 seconds, versus the earlier 209.92-second take. Timing varies with the run. |',
 '| Siege Bomber | Engines and guns have priority over the core plate, with clear firing columns from below. Ordinary weapons reach all four modules. |',
 '| Chronos | Dialogue keeps combat, shots, movement and new action taps live. Animated charging shield sits in front of his body; hammer remains outside. Authored charge, red idle/energy palettes, fluid stun/death loop and red spike-ball counter frames. |',
 '| Chronos attacks | Normal: one down strike. Hard: second down strike. Furious: second down strike then both side sweeps, including the distance entry. Whirlwind exposes the canonical hammer. Throw uses glowing hammer, asterisk and “Dodge THIS!” without a route marker. Missiles reverse its orbit; timed recall remains independent. The corrupted copy retains its canonical hammer and gains the same timed reversal behavior. |',
 '| Siege Fortress | Exposed reactor alternates warned wind/lightning lanes and orb pincers, with the native charge/cannon audio. |',
 '| Caustic Dredger | Spacing-sensitive non-repeat attack choices, crossing volleys and double committed rushes on Furious. All 16 warning lanes match the emitted projectiles; surge owns one contact per seat/pass. |',
 '| Herald of Death | Talon pursuit, crossing swoops, feather lanes, wing/gun rakes, then disarmed head lances. Existing authored flight frames remain in use. |',
 '| Dracodia first body | Portal travel establishes the arena entrance. Arms own 33.3% HP each; protected body owns the remaining 33.4%. Red eye tracks the actual moving frame and charges/fires the red animated laser. Exposed core folds into a 24-frame rotating ball with varied paths, horizontal laser lanes and code grenades. |',
 '| Dracodia rebirth | Falling destruction with rising explosion trails; pilot reaction lines; rising, bobbing and turning symbiote matter; fusion; exactly 24 accelerating lightning beats; spiral and whiteout; final arena reveal and speech. Verified with both isolated animation coverage and a real-time render-loop probe. |','',
 '## Verification','',
 f"- {summary['nativeContracts']} native contract checks, {summary['visualChecks']} visual/state checks and {summary['artChecks']} authored-bank integrity checks passed.",
 '- Full `_BUILD_SOURCE/test_fl.js` suite finished with **0 errors**. JavaScript syntax checks passed.',
 '- Twelve selected Furious encounters reached native defeat. Each MP4 played from the start, decoded frames, sought near its end and contained audible AAC audio. All 30 older recordings also passed playback/seek checks.',
 '- Fresh Stage 4, Chronos, Dredger, Dracodia and alternate Rime Wall takes have no JavaScript exceptions or HTTP asset failures. Early parallel takes contained resource-connection console noise; retained reports distinguish that from JavaScript exceptions. The recorder now uses a larger request queue, checks required manifests, and separates exception/network logs.',
 '- The bot uses native inputs and delayed observations. Only player damage is ignored; it does not lower boss HP, manufacture upgrades, skip phases or force wins in the full fight recordings. Isolated fixtures deliberately select states/damage parts for coverage and are stored separately.',
 '- Invulnerable-bot completion establishes functioning encounters and capture coverage; human difficulty/fairness still needs player review.',
 '- PixelLab: **$0.63** plus **three bonus generations** used; **$3.47** last observed remaining. Weak generations are excluded from the installed banks.',
 '', '## Review files','',
 '- Gallery: `C:/Users/Mike/Documents/New project/BOF-Boss-Rework-1023/review/index.html`',
 '- Video media: the adjacent `media/` folder; raw engine recordings remain in the `native-*` folders.',
 '- Native reports and screenshots: `_shots/encounter_revision_1023/`.',
 '- Rebuild sources and provenance: `_BUILD_SOURCE/encounter_revision_1023/`.',
 '', 'No changes were made to the native death/reward ownership of the later Dracodia forms or the established final ending. The first-body transition replaces its intermediate ghost encounter, as requested, before entering the existing final form sequence.','']
text='\n'.join(lines);(W/'REPORT.md').write_text(text,encoding='utf-8');(R/'docs/ENCOUNTER_REVIEW_1023.md').write_text(text,encoding='utf-8')
(S/'README.md').write_text('''# Encounter correction sources

Read `docs/ENCOUNTER_REVIEW_1023.md` in the repository for the player-requested behavior and verification limits.

The approved raw frames, identity references, generated manifests and PixelLab job provenance are stored here. No original personal photographs or upload credentials are included.

Rebuild order: `build_turrets.py`, `build_revision_art.py`, `install_latest.py`. Runtime outputs are copied to `assets/game/shared/combat/encounter_revision_1023/`; the installer is idempotent and keeps one correctly ordered script tag per owner. Set `BOF_GAME_ROOT` to use another checkout.

`record_final.py` uses the existing `_BUILD_SOURCE/furious_bot_1023/` controller and job list. Set `BOF_CAPTURE_DIR` to an ignored `_shots/` folder before recording. Full real-time takes are separate from the deterministic component/animation fixtures. Video source files remain in the local review workspace to avoid adding large movies to the repository.
''',encoding='utf-8')
note='\n\n## October 24 — encounter review corrections\n\nSee `docs/ENCOUNTER_REVIEW_1023.md` for the current player-requested modular HP, reachable rear weapons, Chronos live-dialogue/hammer rules, Dredger/Herald attacks and Dracodia teleport/rebirth sequence. Runtime owners are `encounter_revision_1023.js` and `dracodia_rebirth_1023.js`, loaded after their art manifest and prior encounter owners. Sources/provenance: `_BUILD_SOURCE/encounter_revision_1023/`. Full core suite: zero errors; native contract, authored-bank, live-render and twelve-film playback checks passed. Never restore Chronos dialogue pauses or make sonic pressure waves interceptable. Preserve the canonical Stage 5 / corrupted hammer designs.\n'
for name in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/name;s=p.read_bytes().decode('utf-8')
 if '## October 24 — encounter review corrections'not in s:p.write_bytes((s+note.replace('\n','\r\n' if '\r\n' in s else '\n')).encode('utf-8'))
p=R/'AGENTS.md';s=p.read_bytes().decode('utf-8');tag='\n\n## October 24 encounter rules\n\n- Chronos speech is a live combat overlay: preserve movement, projectiles, new input taps and vulnerability. His non-missile spike-ball response is the explicit authored **red** hit-feedback exception.\n- Siege-tank sonic waves are never offensive interception targets. Dracodia first-body arms each own 33.3% HP; the 33.4% core stays protected until both arms are destroyed.\n- Read `docs/ENCOUNTER_REVIEW_1023.md` before rebuilding these encounters. Preserve the portal entrance and symbiote rebirth into the final arena.\n'
if '## October 24 encounter rules'not in s:p.write_bytes((s+tag.replace('\n','\r\n' if '\r\n'in s else '\n')).encode('utf-8'))
print(json.dumps(summary,indent=2))
