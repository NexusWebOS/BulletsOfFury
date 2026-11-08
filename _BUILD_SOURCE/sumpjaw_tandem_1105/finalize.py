from pathlib import Path
import json,shutil,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');V=W.parent/'BOF-Furious-Boss-Videos-1104';F=R/'_shots/boss_comparison_1102/sumpjaw-tandem-final-1105'
j=json.loads((F/'batch.json').read_text())['jobs']['stage7-mini'];probe=json.loads((W/'probe/report.json').read_text());art=json.loads((W/'art-checks/report.json').read_text());mouth=json.loads((W/'mouth-checks.json').read_text());compat=json.loads((W/'compat-report.json').read_text());perf=json.loads((W/'performance.json').read_text());pv=json.loads((V/'preview-checks.json').read_text());film=json.loads((F/'stage7-mini/report.json').read_text())
assert j['passed']and art['passed']and mouth['passed']and all(c['passed']for c in probe['checks']+compat['checks']+pv['checks'])and not perf['errors']
url='http://127.0.0.1:65123/?sumpjaw=tandem-final-1105#sumpjaw'
report=f'''# Sumpjaw — coordinated jumping pair and one shared health bar

November 5, 2026. SJ120 extends the existing approved SJ98/SS116 serpents.

The two floating health bars are replaced by one top-screen gauge. Each snake
permanently owns half: the left half is snake 01, the right half snake 02.
Killing either empties precisely its share while the other keeps its own
remaining health. No refill or transferred health occurs.

Base Furious HP is **14,000 total**, **7,000 each**, compared with **12,466 HP**
for the actual Hard Stage 7 boss in the matched native fixture: about 12.3%
more health. Each snake retains two 1,750 HP toxic gills and a protected
3,500 HP intake heart. Both gills must break before its heart takes damage.
NG+ still scales the complete pair to 17,500 HP, with equal 8,750 HP shares.
Hard's original Dredger and Warden encounters are unchanged.

The shared attack director performs six consecutive left/right leaps,
alternating high and low paths. The lower arc crosses the pilot's ground row
while airborne. Shadows stay on the floor; the visible head and its actual
gill sockets remain hittable in the air. Landing reticles mark committed
landing points. The snakes fire straight down from their real mouths while
passing overhead, with a point-blank shot guard.

They then align in a separated horizontal row, charge their mouth cores,
and strafe together while firing rapid dual large-orb bursts. Each mouth
fires every 0.14 seconds during 0.86-second bursts with brief gaps. They
split-hop apart, jump offscreen north, cross in opposite directions at
different heights, and return. The remaining snake uses faster solo jumps
and 0.105-second firing bursts instead of waiting for a dead partner.

All little acid/spread pellet emissions are removed from this encounter.
The only new rounds are the existing 72px toxic-orb artwork, travelling
straight down at speed 5.2. Their actual collision radius is 24px. They are
ordinary unshootable enemy ordnance from birth, have a 3-second maximum life,
and are capped at 44. Native pool breaks, death and retry clear owned rounds.
High overflight does not have body contact; low landings use native player
protection and hit/death rules. Floor shadows never absorb weapons.

The whole-body and tail green outer hot frames are no longer drawn when
charging or firing. Instead, authored emission pixels animate only inside
the original toxic mouth core, with four levels, an eight-cell source-timed
loop, both jaw positions and all 32 headings. The source's held frames are
preserved. No emission alpha extends onto armor or outside the mouth mask.
A small mouth-local ooze flash accompanies each launch. Native white hit
flashes still appear on the body and trail, then expire to normal material.

Toxic launch, heavy-gun pulse, charge, jump, landing, module break and death
sounds use the shared mixer and retrigger gates. The full recording contains
597 toxic-spit, 328 enemy-heavy-gun and 81 landing cue plays, with decoded
game audio and no audio tap errors. These counts include the complete fight,
not a synthetic sound montage.

## Artwork and ownership

No external image generation or generation credits were used. Existing
approved source pixels were re-authored offline into **2,066 frames in four
banks**, on six compact pages: 1,472,019 compressed bytes / 9.20 MiB decoded.
Mouth cells are fixed 176×176, local flashes 48×48, the shared frame 400×28
and its clipped half-fill 190×4. All dimensions are even with fixed pivots.
The complete rectangular UI border/fill intentionally have full-bleed edges;
creature effect cells have transparent padding. Runtime draws only selected
authored frames, with ordinary source-over blits and health-fill clipping.

Owners: `assets/sumpjaw_tandem_1105.js` and its art registry, loaded after
TC119. Editable Aseprite sources, strips, manifests, runtime snapshots and
rebuild/verification helpers are in `_BUILD_SOURCE/sumpjaw_tandem_1105/`.
The original native pool, damage/Retina and once-only defeat owners remain.
`assets/game.js` is unchanged. No commit or push was requested in this pass.

## Verification and limits

- **{len(probe['checks'])} focused native checks pass**: all attack families, real jumping
  paths/heights, aligned dual fire, only large downward orbs, no outer hot
  frames, actual mouth playback, visible-air targets, four gill gates,
  actual white hit pixels/expiry, one fixed 50/50 bar, solo behavior,
  unshootable bounded rounds, pause, retry, six pools and one native defeat.
- **{len(compat['checks'])} compatibility checks pass** for Hard Stage 7, both current
  Stage 6 alternates, NG+ health/pool scaling and browser errors.
- **2,066/2,066 frames** pass Aseprite roundtrip and compact-atlas visible
  RGBA/alpha comparisons. All 2,048 emission frames match the exact rotated
  original mouth mask; every emission level animates with distinct frames.
- Uncaptured high-quality native playback measured **{perf['observationFps']:.2f} FPS observing**
  and **{perf['firingFps']:.2f} FPS with sustained player fire**, without page errors.
- Full fresh real-RAF fight: **{j['nativeFps']:.2f} average engine FPS** over
  **{j['seconds']} seconds**, with 60 seconds hold-fire before an input-only
  Cole GOD bot attacks. No enemy health, phase or timer writes occur after
  spawn. All gills/hearts are destroyed with native player weapons and
  missiles; native rewards/progression finish. 960×1024 native canvas,
  30 FPS media, audio peak **{j['peakDb']} dB**. Source stability, full decoding,
  audible playback and browser/asset checks pass.
- **{len(pv['checks'])} preview checks pass** for actual video/audio, seeking,
  byte ranges, mobile fit and browser errors.
- Syntax and Windows-line-ending-aware whitespace checks pass. The required
  older `test_fl.js` suite still aborts before its final summary at the
  existing `difficultyHealthBaseline15 is not defined` dependency failure in
  `combat_polish_0927b.js:151`. Its fresh log is retained. This is not a
  full-suite pass.

The higher HP, faster cadence and paired choreography establish a stronger
encounter budget; they do not prove human difficulty. The GOD bot blocked
447 native hits during this recording. Human dodgeability/balance testing,
complete campaign testing and other machines remain unverified.

[Watch the revised full fight and attack chapters]({url})
'''
(W/'REPORT.md').write_text(report,encoding='utf8',newline='\n');(R/'docs/SUMPJAW_TANDEM_1105.md').write_text(report,encoding='utf8',newline='\n')
S=R/'_BUILD_SOURCE/sumpjaw_tandem_1105';S.mkdir(parents=True,exist_ok=True);A=W/'authored';M=json.loads((A/'manifest.json').read_text())
for p in W.glob('*.py'):shutil.copy2(p,S/p.name)
for n in ['SPEC.md','REPORT.md','sumpjaw_tandem_1105.js','sumpjaw_tandem_art_1105.js']:shutil.copy2(W/n,S/n)
for n in ['manifest.json','author.lua']:shutil.copy2(A/n,S/n)
(S/'strips').mkdir(exist_ok=True)
for n in M['banks']:
 shutil.copy2(A/(n+'.aseprite'),S/(n+'.aseprite'));shutil.copy2(A/'strips'/(n+'.png'),S/'strips'/(n+'.png'))
Q=R/'docs/qa/sumpjaw_tandem_1105';Q.mkdir(parents=True,exist_ok=True)
for src,name in [(W/'probe/report.json','native-checks.json'),(W/'baseline.json','before-change-native-baseline.json'),(W/'art-checks/report.json','art-checks.json'),(W/'mouth-checks.json','mouth-checks.json'),(W/'compat-report.json','compatibility.json'),(W/'performance.json','performance.json'),(W/'full-suite.log','existing-suite-failure.log'),(V/'preview-checks.json','preview-checks.json'),(F/'batch.json','batch.json'),(F/'stage7-mini/report.json','recording-report.json')]:shutil.copy2(src,Q/name)
for p in (W/'probe').glob('*.png'):shutil.copy2(p,Q/p.name)
shutil.copy2(W/'film-inspection/fight-contact.png',Q/'fight-contact.png')
for n in ['index.html','manifest.json','report.json','prepare.py','server.py','check_preview.py']:shutil.copy2(V/n,Q/('preview-'+n))
shutil.copytree(V/'posters',Q/'posters',dirs_exist_ok=True)
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest()for n in ['assets/game.js','assets/sumpjaw_tandem_1105.js','assets/sumpjaw_tandem_art_1105.js']};assert hashes['assets/game.js']=='4424749aa097782c033ecebad5246aff4f91f9f0c877e1720c1a416cb68e0e86';assert film['sourceHashes']['assets/sumpjaw_tandem_1105.js']==hashes['assets/sumpjaw_tandem_1105.js'];(Q/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
entry={'role':'furious_stage7_sumpjaw_coordinated_leaping_tandem_large_orb_fire_inner_mouth_animation_one_fixed_half_health_gauge','owner':'_BUILD_SOURCE/sumpjaw_tandem_1105/build_art.py','manifest':'assets/game/levels/stage_07/miniboss/sumpjaw_tandem_1105/manifest.json','note':'Re-authored approved SJ98/SS116 pixels without generation charge. 2066 fixed even-cell frames in four banks, six compact pages. Exact inner-mouth mask emission, mouth-local flash and one authored 50/50 gauge. No green outer hot frames or small acid spread. Six jumps, paired strafing large-orb bursts, split/north/over-under return, faster solo. 14000 total base Furious HP (7000 each), native two-gill heart gates, hit feedback and rewards. Source/Aseprite/QA: docs/SUMPJAW_TANDEM_1105.md.'}
p=R/'assets/data/ART_TAXONOMY.json';raw=p.read_bytes();data=json.loads(raw)
if 'sj120_'not in data:
 nl=b'\r\n'if b'\r\n'in raw else b'\n';pos=raw.rfind(nl+b'}');addition=json.dumps({'sj120_':entry},indent=2,ensure_ascii=False).encode('utf8')[2:-2];p.write_bytes(raw[:pos].rstrip()+b','+nl+addition+nl+b'}'+nl);assert json.loads(p.read_bytes())['sj120_']==entry
header=f'''## November 5, 2026 - Sumpjaw coordinated tandem and shared health (SJ120)

Mike's latest Sumpjaw pass is installed: no little spread pellets or whole-body
green charge rim; animate only the inside toxic mouth cores and local muzzle.
Six left/right airborne jumps over the pilot, downward large mouth orbs,
aligned dual firing row with joint strafing, split-hop/north exit and real
over/under crossing return. Faster solo survivor retains its native gates.
One top-screen bar with fixed 50/50 shares. Base Furious 14000 HP total,
7000 each; actual Hard Stage7 boss baseline12466. Native NG+17500 total.
Visible airborne heads remain hittable at their actual sockets; shadows do not
block weapons. Native gill gates, white hit expiry and single defeat preserved.
{len(probe['checks'])} native + {len(compat['checks'])} compatibility +2066 art-frame checks pass;
exact inner-mouth masks and14 preview checks pass. Full native GOD/input-bot
film: {j['nativeFps']:.2f} average engine FPS over {j['seconds']}s, 60s hold-fire.
Known older test_fl.js missing-helper failure remains; game.js unchanged.
Owner: assets/sumpjaw_tandem_1105.js. Rebuild: _BUILD_SOURCE/sumpjaw_tandem_1105/.
Evidence/limits: docs/SUMPJAW_TANDEM_1105.md. No commit/push requested.
Review: {url}

'''
for n in ['HANDOFF_CODEX.md','CLAUDE.md']:
 p=R/n;raw=p.read_bytes()
 if b'Sumpjaw coordinated tandem and shared health (SJ120)'not in raw[:5000]:
  nl='\r\n'if raw.count(b'\r\n')>raw.count(b'\n')/2 else'\n';p.write_bytes(header.replace('\n',nl).encode('utf8')+raw)
(Q/'delivery.json').write_text(json.dumps(dict(nativeChecks=len(probe['checks']),compatibility=len(compat['checks']),frames=art['frames'],preview=len(pv['checks']),nativeFps=j['nativeFps'],seconds=j['seconds'],url=url,movie=j['path'],runtimeSha256=hashes['assets/sumpjaw_tandem_1105.js']),indent=2))
print('Saved Sumpjaw runtime/source, editable art, report, taxonomy, handoff and native-film evidence.')
