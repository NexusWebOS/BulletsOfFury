from pathlib import Path
import json,hashlib,subprocess,html
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/dredger_assault_1028';F=R/json.loads((O/'video/latest.json').read_text())['folder'];report=json.loads((F/'report.json').read_text());FF=imageio_ffmpeg.get_ffmpeg_exe()
assert all(report['checks'].values())
events=report['events'];rows=report['timeline']
def wall(t):
 q=min(rows,key=lambda q:abs(q['clock']-t));return max(0,q['seconds']+t-q['clock'])
def event(name,mode=None):return next(e for e in events if e['event']==name and(mode is None or e.get('mode')==mode))
chapters=[(0,'Arrival'),(wall(event('attack-start','dc40-circle')['t']),'Circular cannon warning'),(wall(event('attack-start','dc40-ram')['t']),'Fast ram & reverse'),(wall(event('mid-screen-opening')['t']),'Mid-screen opening'),(wall(event('attack-start','dc40-guns')['t']),'Twin toxic turrets')]
if any(e['event']=='core-exhausted-guns-live'for e in events):chapters.append((wall(event('core-exhausted-guns-live')['t']),'Surviving turrets'))
chapters.append((next(q['seconds']for q in rows if q['mode']=='dead')-.6,'Final defeat'))
stills=[('cannon-warning',wall(event('top-cannon-wave')['t'])-.2),('ram-opening',wall(event('mid-screen-opening')['t'])+.35),('twin-turrets',wall(event('twin-turret-burst')['t'])+.25)]
for name,t in stills:subprocess.run([FF,'-v','error','-y','-ss',str(t),'-i',str(F/'dredger-furious.mp4'),'-frames:v','1',str(F/(name+'.png'))],check=True)
(F/'chapters.json').write_text(json.dumps(chapters,indent=2))
folder=F.relative_to(R).as_posix();P=R/'docs/previews/dredger_assault_1028';P.mkdir(parents=True,exist_ok=True)
buttons=''.join(f'<button data-time="{t:.3f}">{html.escape(label)}</button>'for t,label in chapters)
pics=''.join(f'<figure><img src="../../../{folder}/{name}.png" alt="{label}"><figcaption>{label}</figcaption></figure>'for (name,_),label in zip(stills,['North-facing circular warning','Reverse to mid-screen, then a firing window','Two turrets with two toxic slug barrels each']))
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Dredger — ram, reverse & twin turrets</title><style>
*{box-sizing:border-box}body{margin:0;background:#0a100d;color:#e4ede6;font:16px/1.5 system-ui}main{max-width:1328px;margin:auto;padding:26px 24px 44px}h1{font-size:clamp(26px,4vw,40px);line-height:1.15;margin:0 0 10px}p{max-width:1040px;color:#b5c8b9}video{display:block;width:100%;background:#020503;aspect-ratio:16/10;border:1px solid #43603c;border-radius:4px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 24px}button{font:inherit;cursor:pointer;color:#eff7e8;background:#203221;border:1px solid #526c40;border-radius:4px;padding:9px 14px}button:hover,button:focus-visible{background:#354c2a;outline:2px solid #a3ef4a}.shots{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}figure{margin:0}img{width:100%;display:block;border:1px solid #3c513a}figcaption{padding-top:7px;font-size:14px;color:#b5c8b9}.note{font-size:14px;margin-top:22px}a{color:#b8ef69}@media(max-width:750px){main{padding:18px 12px}.shots{grid-template-columns:1fr}}
</style></head><body><main><h1>Dredger — fast ram, clean reverse, twin turrets</h1><p>A quick committed ram, a reverse to mid-screen, and a 1.65-second opening to hit him. Moving tracks, separated twin-barrel turrets with recoil and toxic slugs, plus a glowing top cannon with a green/yellow/red circular warning.</p>
<video id="v" controls preload="auto" poster="../../../FOLDER/cannon-warning.png" data-src="../../../FOLDER/dredger-furious.mp4"></video><nav aria-label="Fight chapters">BUTTONS</nav><div class="shots">PICS</div><p class="note">Complete Furious fight with an invulnerable input observer. Enemy HP, attacks and defeat run through the live game. The circular cannon leaves an opening to the south; the turrets remain separate targets after the core is spent.</p><p class="note" id="status" role="status">Loading full replay…</p></main><script>
let mediaURL;const status=document.querySelector('#status');fetch(v.dataset.src).then(r=>{if(!r.ok)throw Error('Replay load failed');return r.blob()}).then(blob=>{mediaURL=URL.createObjectURL(blob);v.src=mediaURL;v.load();status.textContent='Replay ready — select a chapter or press Play.'}).catch(e=>status.textContent=e.message);
document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{v.currentTime=+b.dataset.time;v.play().catch(()=>{});}));addEventListener('beforeunload',()=>{if(mediaURL)URL.revokeObjectURL(mediaURL)});
</script></body></html>'''.replace('FOLDER',folder).replace('BUTTONS',buttons).replace('PICS',pics)
(P/'index.html').write_text(page,encoding='utf8')
probe=json.loads((O/'probe/report.json').read_text());art=json.loads((O/'art-checks.json').read_text());warden=json.loads((R/'_shots/warden_lunge_1028/probe/report.json').read_text())
fps=report['sound']['frames']/rows[-1]['seconds']
files=['assets/dredger_assault_1028.js','assets/dredger_assault_art_1028.js','_BUILD_SOURCE/build_dredger_assault_1028.py']
qa=dict(request='Fast Dredger ram/reverse; moving treads; top 1015 glow and circular FOV; separated twin-barrel toxic MGs with recoil.',native=probe,art=art,wardenRegression=warden,film=dict(path=folder+'/dredger-furious.mp4',method=report['method'],duration=rows[-1]['seconds'],fps=fps,decodedPeakDb=report['decodedPeakDb'],checks=report['checks'],errors=report['errors'],soundCues=report['sound']['playing'],chapters=chapters),sourceHashes={f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in files},fullSuite=dict(exit=1,reachedFinalSummary=False,reason='Existing missing UNUSED_ASSETS/retired_art_1022/manifest.json',log='_shots/dredger-full-suite-1028.log'),syntax=dict(game=True,dredger=True),review='docs/previews/dredger_assault_1028/index.html')
Q=R/'docs/qa/dredger_assault_1028.json';Q.write_text(json.dumps(qa,indent=2),encoding='utf8')
notes=f'''# Dredger assault — October 28

Mike requested a fast ram followed by a reverse to mid-screen; visible track motion; 1015 top-cannon light and a north-facing circular warning; separated twin turrets, each with two barrels, recoil and toxic slugs.

## Current owner and art

`assets/dredger_assault_1028.js` loads after the sewer/Warden owners and is scoped to Stage7's tank. The actual native 176×192 body, 76×68 top and ER28 gun source were exported with `_BUILD_SOURCE/export_dredger_1028.py`. `_BUILD_SOURCE/build_dredger_assault_1028.py` owns the new registry, manifest and source-derived banks under `assets/game/levels/stage_07/miniboss/dredger_assault_1028/`.

- Eight authored tread phases move only the measured link bands. Native chassis distance advances them; reversing reverses them; braced fire stops them. Hull/caps/rails remain unchanged.
- Two fixed trunnions at ±43,+66; 64 baked headings ×4 shot-linked recoil phases; two actual source barrels per housing. One proportional 0.94 source scale, fixed112×112 canvas/pivot56,56. Constrained inward aim prevents overlap. Four measured per-frame sockets drive native toxic muzzle flashes and slugs. Native player beams actually hit the exposed barrel alpha from the south; Retina targets use those visible apertures.
- The actual top has a source-aligned 1015 glow companion. Three native-palette192×192 FOV cells reproject the authored broad FOV into a north-facing300-degree circle, leaving a60-degree south opening. The committed finite three-wave slug barrage uses the same angular bounds.
- The whole native hull and top retain their existing dimensions/pixels; all hit companions preserve exact source alpha. Broken turrets use this same baked twin-gun bank while the native D27 debris flight, explosion cadence and terminal blast remain in charge.

## Live behavior and ownership

The ram keeps a committed warning, accelerates over0.20–0.42s, reverses over0.66s to46% screen height, then stays vulnerable and silent for1.65s before advancing the native book. Shared mixer cues remain `bossWeaponCharge`, `enemyMachineGunHeavy`, `combatToxic0927`, `jetDash` and native module-break cues, with retrigger gates. Ordinary slugs reject interception before their first update; physical missiles and defensive clears retain their owners. Gun break removes its target and cancels its rounds; death cancels the new launcher.

The first complete recording exposed a native composite-budget defect: core exhaustion entered death with surviving gun HP still displayed. The tank-only handoff now defers death until core and both gun pools are exhausted. An empty core drops its Retina target; surviving guns keep their attacks and HP. No pools are reset or fabricated, and the final native defeat/reward runs once. Warden ownership is unchanged.

## Verification

{len(probe['checks'])} native controller/render checks pass, including real turret hit pixels/expiry, exposed beam contact, source-matched sockets, non-overlap through extreme aim, moving/reversing tracks, committed ram contact, finite opening, three FOV phases, ordinary interception, break art and complete HP exhaustion. Ten export/rebuild checks pass; all outputs rebuild exactly. The existing16-check Warden rear-lunge/portal regression passes.

Final continuous native Furious fight: **{rows[-1]['seconds']:.2f}s**, **{fps:.2f}fps**, decoded peak **{report['decodedPeakDb']:.1f}dB**,12 film checks pass, no page/console/asset errors. It uses native debug entry and a labelled invulnerable input observer; no enemy HP, phase or timer writes. The complete gun/core budget is exhausted before the native defeat. File: `{folder}/dredger-furious.mp4`. Decoded stills and chapters accompany it. Review: `docs/previews/dredger_assault_1028/index.html`.

`node --check assets/game.js` and the new runtime pass. Required `node _BUILD_SOURCE/test_fl.js` exits1 before its summary on the pre-existing missing `UNUSED_ASSETS/retired_art_1022/manifest.json`. No assertion failures can be compared because the loader stops before assertions. Evidence: `docs/qa/dredger_assault_1028.json`. No game.js/test_fl.js edits, commit or push.
'''
(R/'docs/DREDGER_ASSAULT_1028.md').write_text(notes,encoding='utf8')
handoff=R/'HANDOFF_CODEX.md';raw=handoff.read_bytes();title='## 2026-10-28 — Dredger ram, reverse and twin toxic turrets'
if title.encode()not in raw:
 text=f'''{title}

Mike's Dredger revision is owned by assets/dredger_assault_1028.js: fast committed ram, reverse to mid-screen and1.65s exposed opening; actual distance-driven tread banks; fixed non-overlapping two-barrel turrets,64 authored headings/shot recoil, four measured native toxic-slug sockets; own-pixel1015 top light and native G/Y/R north-facing circular barrage FOV. Correct exposed beam targets and native source-matched turret break flight retained. Tank-only composite handoff fixes premature core death while guns have HP; all original pools/native final defeat and rewards remain.

{len(probe['checks'])} focused native +10 art/rebuild +16 Warden regression checks pass. Final {rows[-1]['seconds']:.2f}s complete native Furious film: {fps:.2f}fps, {report['decodedPeakDb']:.1f}dB, all12 film checks, no game errors or enemy HP/phase/timer writes. Review docs/previews/dredger_assault_1028/index.html; details docs/DREDGER_ASSAULT_1028.md; QA docs/qa/dredger_assault_1028.json. Full suite still exits1 before summary on missing retired-art manifest. No game.js/test_fl.js edits, commit or push.

'''
 handoff.write_bytes(text.replace('\n','\r\n').encode('utf8')+raw)
print(json.dumps(dict(review=str(P/'index.html'),video=folder+'/dredger-furious.mp4',fps=round(fps,2),duration=round(rows[-1]['seconds'],2),chapters=chapters),indent=2))
