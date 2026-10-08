from pathlib import Path
import json,math,hashlib,re,csv,html
R=Path(__file__).resolve().parents[1];O=R/'_shots/projectiles_1007'
main=json.loads((O/'after/audit.json').read_text(encoding='utf-8'))
pilots=json.loads((O/'pilots/audit.json').read_text(encoding='utf-8'))
final=json.loads((O/'final/audit.json').read_text(encoding='utf-8'))
primary=json.loads((O/'primary/audit.json').read_text(encoding='utf-8'))
valid_weapons=[r for r in pilots['weapons'] if r['case']['weapon']<8]
valid_orbs=[r for r in primary['cases'] if r['case']['weapon']==8]
checks={}
def check(name,value):checks[name]=bool(value)
check('144 projectile kinds on all four difficulties',len(main['catalog'])==4 and all(len(c['rows'])==144 for c in main['catalog'].values()))
check('all catalog frames draw visible pixels',all(f['n']>0 for c in main['catalog'].values() for r in c['rows'] for f in r.get('frames',[])))
check('no catalog exceptions or invalid crops',all(not c['geometry'] and all('error' not in r for r in c['rows']) for c in main['catalog'].values()))
check('all 164 encounter and stage observations completed',len(main['encounters'])==164 and all(r['frames']==(2160 if r['case'].get('slice') else 1440) for r in main['encounters']))
check('864 legal shared-weapon loadouts completed',len(valid_weapons)==864)
def primary_fired(r):
 c=r['case'];expected={0:['mg'],1:['spread'],2:['missile'],3:['mavlaser'] if c['pilot']=='maverick' else ['beam'],4:['flame'],5:['orb'],6:['lasermist'],7:['mg']}[c['weapon']]
 # Maverick's homing lance intentionally has fixed Level I combat stats;
 # acquired run.wlevels[3] still controls its color (game.js maverickLaserVolley).
 effective_level=1 if c['pilot']=='maverick' and c['weapon']==3 else c['level']
 return all(r['shots'].get(k,0)>0 for k in expected) and r['effective']=={'weapon':c['weapon'],'level':effective_level}
check('every shared primary actually fired at its intended effective tier',all(primary_fired(r) for r in valid_weapons))
check('12 unlocked Yuri Lightning Orb loadouts fired the orb and bolts',len(valid_orbs)==12 and all(r['case']['pilot']=='yuri' and r['shots'].get('yuriLightningOrb',0)>0 and r['shots'].get('yuriLightningBolt',0)>0 for r in valid_orbs))
check('108 corrected chaingun primary loadouts fired actual cal50 rounds',len(primary['cases'])==120 and all(r['cal50']>0 for r in primary['cases'] if r['case']['weapon']==7))
check('corrected primary loadouts have no invalid draw geometry',all(not r['geometry'] for r in primary['cases']))
check('all chaingun palettes retain constant bounds and pixel occupancy with animated light',all(len({tuple(f['bounds'] or []) for f in r['frames']})==1 and min(f['n'] for f in r['frames'])>0 and len({f['n'] for f in r['frames']})==1 and len({f['hash'] for f in r['frames']})>1 for c in primary['tracers'] for r in c['rows']))
check('no player projectile geometry errors',all(not r['geometry'] for r in pilots['weapons']))
check('all focused final rechecks passed',len(final['cases'])==20 and all(not r['geometry'] for r in final['cases']))
check('dedicated boss projectile routes draw all sampled frames',all(f['n']>0 for c in final['specialized'] for r in c['rows'] for f in r['frames']))
check('dedicated boss projectile routes have no invalid crops',all(not c['geometry'] for c in final['specialized']))
check('30/60/120 Hz keep player and enemy visual clocks at one second',len(pilots['clocks'])==12 and all(abs(r['player']-1)<1e-8 and abs(r['enemy']-1)<1e-8 and r['pFrame']==4 and r['eFrame']==4 for r in pilots['clocks']))
check('death animation sequences have no invalid draw geometry',len(pilots['deaths'])==8 and all(not r['geometry'] for r in pilots['deaths']))
for label,val in main['checks'].items():check(label,val)
for label,val in final['checks'].items():check(label,val)
unchanged=[]
for r in main['stableSheets']:
 # These three route to separate authored orb/laser reels, deliberately retained.
 if r['kind'] in ['s7acid','s7shard','s7laser']:continue
 fs=r['frames'];check(r['kind']+' stable silhouette and moving light',len({tuple(f['bounds']) for f in fs})==1 and len({f['n'] for f in fs})==1 and len({f['hash'] for f in fs})>1);unchanged.append(r['kind'])
errors=main['errors']+pilots['errors']+final['errors']+primary['errors'];check('zero recorded native browser errors',not errors)
log=(O/'build-tests-complete.log').read_text(encoding='utf-8');suite_ok='==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====' in log and 'ASSERT FAIL:' not in log
check('full repository regression suite reached final success banner',suite_ok)
suite_count=len(re.findall(r'^  ok\s',log,re.M))
initial=[{'case':r['case'],'geometry':r['geometry']} for r in main['encounters'] if r['geometry']]
def same(a,b):return all(a.get(k)==b.get(k) for k in ['diff','stage','kind','mini','ace','slice'])
check('every initial invalid-render fixture has a clean final replay',all(any(same(r['case'],f['case']) and not f['geometry'] for f in final['cases']) for r in initial))
def clean(v):
 if isinstance(v,float) and not math.isfinite(v):return None
 if isinstance(v,dict):return {k:clean(q) for k,q in v.items()}
 if isinstance(v,list):return [clean(q) for q in v]
 return v
runtime=['assets/game.js','assets/combat_director_0927.js','assets/combat_polish_0927b.js','assets/pilot_feedback_0927.js','assets/repair_0930.js']
summary={'checks':checks,'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'suiteAssertions':suite_count,'browserErrors':errors,'catalogTypes':144,'catalogFrames':sum(len(r['frames']) for c in main['catalog'].values() for r in c['rows']),'dedicatedVariants':len(final['specialized'][0]['rows']),'dedicatedFrames':sum(len(r['frames']) for c in final['specialized'] for r in c['rows']),'encounterStageCases':len(main['encounters']),'weaponCases':len(pilots['weapons']),'stableFamilies':unchanged,'finalRechecks':final['cases'],'clockChecks':pilots['clocks'],'initialFailures':initial,'runtimeSHA256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in runtime},'scope':'Protected bounded encounters and isolated native renders; not human campaign clears or every possible forge/co-op/status combination.'}
Q=R/'docs/qa';Q.mkdir(exist_ok=True)
summary['attemptedWeaponCases']=len(pilots['weapons']);summary['weaponCases']=len(valid_weapons)+len(valid_orbs);summary['latePrimaryRechecks']=len(primary['cases']);summary['primaryResults']=primary
(Q/'PROJECTILE_ANIMATION_1007.json').write_text(json.dumps(clean(summary),indent=2,allow_nan=False)+'\n',encoding='utf-8')
with (Q/'PROJECTILE_ANIMATION_1007.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['group','difficulty','stage','pilot','weapon','level','case','frames','invalid_draws','shots'])
 for r in main['encounters']:
  c=r['case'];w.writerow(['stage' if c.get('slice') else 'encounter',c['diff'],c['stage'],c.get('pilot'),'',c.get('level'),c['id'],r['frames'],len(r['geometry']),sum(r['shots'].values())])
 for r in valid_weapons:
  c=r['case'];w.writerow(['weapon',c['diff'],c['stage'],c['pilot'],c['weapon'],c['level'],c['id'],r['frames'],len(r['geometry']),sum(r['shots'].values())])
 for r in primary['cases']:
  c=r['case'];w.writerow(['primary-final',c['diff'],c['stage'],c['pilot'],c['weapon'],c['level'],c['id'],180,len(r['geometry']),sum(r['shots'].values())])
 for r in final['cases']:
  c=r['case'];w.writerow(['final-recheck',c['diff'],c['stage'],c['pilot'],'',c['level'],c['id'],r['frames'],len(r['geometry']),sum(r['shots'].values())])
doc=f'''# Projectile and animation pass — October 7, 2026

Fixed confirmed visual defects, with no new art files, atlas repacks, hitbox changes, damage changes or difficulty tuning.

## What changed

- **Herald / Stage 8:** the live `s8pair` route was cycling four small-to-large charge examples as flight frames. Stage 7 had the same sheet contract mismatch. These shared charge sheets now use one complete flight pose with smooth internal luminance pulses and a travelling pixel highlight. Source outlines, palettes and transparent gutters are preserved. The crescent blade turns around its bright core; the toxic missile uses its hull pivot instead of its exhaust.
- **All projectile directions:** a zero vertical velocity was being replaced with `1` in several renderers, tilting exactly horizontal rounds. Zero components now remain zero while the original source-facing conventions remain intact.
- **Player projectiles:** flight visuals have a simulation-owned clock separate from damage/fuse clocks. Flame, shard, laser and spread fallback animations no longer jump with wall-clock time. Negative direction offsets can no longer request nonexistent negative frame indices. Reflected rounds retain a running visual clock.
- **Chaingun:** screenshot review exposed a second size-changing reel in the active `repair30` tracer renderer. Its complete first casing now remains fixed while an internal highlight moves through it, including every infused palette. All 108 shared chaingun loadouts were replayed after this correction.
- **Stage 4 lightning machine gun:** its eighth source cell is completely transparent. The flight loop now plays the seven real lightning frames, preventing an intermittent invisible round. All 32 final samples on each difficulty remain visible; the original failing samples are retained with the raw audit.
- **Pilot animation:** engine light follows simulation time; thrust animation advances continuously as acceleration changes, instead of repeatedly recalculating phase from a changing playback rate. Paused/zero-step rendering does not advance those clocks.
- **Destruction:** authored aircraft hull fragments used pixels-per-second launch speeds in a per-frame particle updater, immediately throwing them far offscreen. Their new seconds-based integration gives identical travel at 30/60/120 Hz and preserves their lifetime. They use their own authored fragment draw only; the duplicate generic spark path no longer receives records without a spark radius.
- **Supporting effects:** Stage 3/6 tinted cloud canvases now expose valid dimensions. The blue Ace launch starts with a defined vertical offset, so its launch burst has a finite position even when entered directly.

## Native evidence

| Coverage | Result |
|---|---:|
| Registered projectile kinds × four difficulties | 144 × 4; {summary['catalogFrames']:,} visible frame samples |
| Dedicated boss projectile variants × four difficulties | {summary['dedicatedVariants']} × 4; {summary['dedicatedFrames']:,} frame samples |
| Live encounter/stage observations | 164 |
| Valid shared-weapon loadouts | 9 pilots × 8 weapons × 3 levels × 4 difficulties = 864 |
| Yuri-only Lightning Orb, correctly unlocked | 3 levels × 4 difficulties = 12 |
| Final actual-primary rechecks | 108 chaingun + 12 Lightning Orb |
| Final replay of affected scenes | 20 clean runs |
| Clock tests | 30/60/120 Hz on all four difficulties |
| Plane/spacecraft death observations | 8 |
| Fixed-pose source families with identical bounds/pixel occupancy | {len(unchanged)}; internal RGB still animates |
| Repository suite | {suite_count:,} assertions; final success banner: {suite_ok} |
| Final verification checks | {sum(checks.values())}/{len(checks)} |
| Recorded browser errors | {len(errors)} |

The 164 observations comprise every regular boss and miniboss on stages 1–9, Rebels, the blue Ace, final host/ghost/home plus all nine copied forms (including Hammer), and all nine stage-opening slices on each difficulty. Boss observations run 24 simulated seconds; stage slices run 36. They use the real update and native Canvas draw paths with a protected pilot. The space miniboss uses live cross-beam draws rather than spawning discrete bullet objects; those beams were traced too.

The original sweep recorded {len(initial)} fixtures with non-finite scene draws. Their causes were traced to cloud dimensions, Ace launch initialization and duplicate debris rendering. The raw discovery evidence is retained; each affected configuration has a clean final replay. A source-text regression initially expected the old `||` expression; it now requires the corrected `??` expression while retaining the original `-PI/2` facing contract.

The first player matrix attempted 972 selections, including the Yuri-only weapon on other pilots and without its unlock. Auxiliary missiles initially obscured that fixture mistake. Those 108 original Orb selections are excluded from primary-weapon proof; 12 valid unlocked Yuri cases replace them. The retained 864 shared-weapon cases each contain their expected primary family. The reusable harness now respects the pilot/unlock requirements.

Maverick's homing lance intentionally retains Level I combat stats while the acquired laser level controls its color (`updatePlay` and `maverickLaserVolley` in `assets/game.js`). The coverage check initially expected the selected tier in `run.wlevel` for every weapon; it now verifies this existing lance contract explicitly. No gameplay behavior was changed to satisfy that check.

Inspected authored Stage 3/4 reel contacts: bodies remain fixed while exhaust/sparks change, so these genuine motion reels were retained. Stage 7's separate eight-frame orb and three-frame beam routes were also retained. The earlier 541-frame source audit identified tight-cropped cells; an opaque edge alone was not treated as clipping or permission to remove pixels.

## Review and reproduction

- Animated before/after and live Herald capture: `_shots/projectiles_1007/review.html`.
- Read-only source audit: `_BUILD_SOURCE/audit_projectiles_1007.py`.
- Full native matrix: `_BUILD_SOURCE/probe_projectiles_1007.py`.
- Player matrix: `_BUILD_SOURCE/probe_pilot_animations_1007.py`.
- Final targeted checks/comparisons: `_BUILD_SOURCE/probe_animation_fixes_1007.py`.
- Actual primary/chaingun checks: `_BUILD_SOURCE/probe_primary_animation_1007.py`.
- Stage 4 transparent-cell replay: `_BUILD_SOURCE/probe_lightning_animation_1007.py`.
- Portable results: [JSON](qa/PROJECTILE_ANIMATION_1007.json), [CSV](qa/PROJECTILE_ANIMATION_1007.csv).
- Required suite: `node --check assets/game.js` and `node _BUILD_SOURCE/test_fl.js`.

These are bounded visual/engine checks, not human clears, sustained hardware frame-rate benchmarks, or an exhaustive test of every co-op/forge/status-effect combination. The pass is local and has not been committed or pushed. Existing balance findings and unrelated work are preserved.
'''
(R/'docs/PROJECTILE_ANIMATION_PASS_1007.md').write_text(doc,encoding='utf-8')
cards=''.join(f'<article><h2>{label}</h2><div class="compare"><figure><img src="final/{kind}-before.webp"><figcaption>Before — charge columns loop</figcaption></figure><figure><img src="final/{kind}-after.webp"><figcaption>After — steady body, internal light</figcaption></figure></div></article>' for kind,label in [('s8pair','Herald twin-core projectile'),('s8blade','Symbiote crescent'),('s8rift','Symbiote rift'),('s7bio','Toxic missile')])
page=f'''<!doctype html><meta charset="utf-8"><title>BOF · Projectile animation pass</title><style>
body{{background:#08131f;color:#d5e2ef;font:16px/1.5 system-ui;max-width:1150px;margin:36px auto;padding:0 20px}}h1{{font-size:36px;margin-bottom:4px}}p{{max-width:900px;color:#a9bfd3}}.stats{{display:flex;gap:16px;flex-wrap:wrap}}.stat,article{{background:#112436;border:1px solid #27465f;border-radius:12px;padding:18px}}.stat b{{display:block;font-size:28px;color:#74e9c0}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:24px}}h2{{font-size:19px;margin:0}}.compare{{display:flex;justify-content:center}}figure{{margin:12px 5px;text-align:center;font-size:13px}}.compare img{{width:180px;height:180px;image-rendering:pixelated}}.live{{width:480px;max-width:100%;image-rendering:pixelated}}a{{color:#77caff}}@media(max-width:750px){{.grid{{grid-template-columns:1fr}}.compare img{{width:140px;height:140px}}}}</style>
<h1>Projectiles that hold their shape</h1><p>Actual native renders, using the same authored assets before and after. Internal light moves; charge-size examples no longer masquerade as flight animation.</p>
<div class="stats"><div class="stat"><b>144 × 4</b>projectile kind/difficulty checks</div><div class="stat"><b>876</b>valid pilot weapon loadouts</div><div class="stat"><b>164 + 20</b>live scenes and final rechecks</div><div class="stat"><b>{suite_count:,}</b>regression assertions</div></div><div class="grid">{cards}</div>
<h2 style="margin-top:32px">Herald in the actual arena</h2><p>30 native frames at 30 fps. Protected QA pilot; this is visual verification, not a balance clear.</p><img class="live" src="final/herald-live.webp">
<p>Also corrected: shrinking chaingun casings, an invisible frame in Stage 4 lightning rounds, zero-axis projectile headings, pause/negative-index animation faults, acceleration-phase jumps, tinted cloud dimensions and death debris that travelled at per-frame speed. 108 chaingun cases were replayed after the casing fix.</p>
<p><a href="../../docs/PROJECTILE_ANIMATION_PASS_1007.md">Full findings and coverage</a> · <a href="../../docs/qa/PROJECTILE_ANIMATION_1007.json">Portable checks</a></p>'''
page=page.replace('</style>','.compare figure{flex:1;min-width:0}.compare img{max-width:100%;height:auto;aspect-ratio:1}article{min-width:0}</style>')
(O/'review.html').write_text(page,encoding='utf-8')
print(json.dumps({'checks':len(checks),'passed':sum(checks.values()),'failed':summary['failed'],'suite':suite_count,'initialFailures':len(initial)},indent=2))
if summary['failed']:raise SystemExit(1)
