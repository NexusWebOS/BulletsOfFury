"""Publish current local review media without replacing historical release files."""
from pathlib import Path
import json,subprocess,hashlib
from PIL import Image
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/nightwing_shape_1028';F=R/json.loads((O/'video/latest.json').read_text())['folder'];proof=json.loads((F/'current-proof.json').read_text());probe=json.loads((O/'probe.json').read_text());reg=json.loads((R/'_shots/nightwing_wind_1028/checks.json').read_text())
assert all(proof['checks'].values())and all(c['passed']for c in probe['checks'])and all(c['passed']for c in reg['checks'])
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/manifest.json').read_text())
for bank,name in [('whole','current-bank'),('whole_hit','current-hit')]:
 a=M['banks'][bank];im=Image.open(R/a['path']);f=66;x=f%a['cols']*a['cw'];y=f//a['cols']*a['ch'];im.crop((x,y,x+a['cw'],y+a['ch'])).save(O/(name+'.png'))
rows=proof['film']['timeline'];turnStart=max(0,next(q['seconds']for q in rows if q.get('mode')=='go')-.7);drift=next(q['seconds']for q in rows if q.get('mode')=='drift');turnEnd=next(q['seconds']for q in rows if q['seconds']>drift and q.get('mode')=='fight')+1
windStart=max(0,next(q['seconds']for q in rows if q.get('nightwing')and(q['nightwing'].get('windState')or{}).get('kind')=='wind')-.4)
clips={'turn':dict(start=turnStart,seconds=turnEnd-turnStart),'wind':dict(start=windStart,seconds=5.8)};FF=imageio_ffmpeg.get_ffmpeg_exe()
for name,c in clips.items():
 c['path']=(F/(name+'-preview.mp4')).relative_to(R).as_posix();subprocess.run([FF,'-v','error','-y','-ss',str(c['start']),'-i',str(R/proof['video']),'-t',str(c['seconds']),'-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','160k','-pix_fmt','yuv420p','-movflags','+faststart',str(R/c['path'])],check=True)
gallery=R/'_shots/github_review_1028';manifest=gallery/'manifest.json';original=manifest.read_bytes();backup=gallery/'manifest.before-nightwing-current-1028.json'
if not backup.exists():backup.write_bytes(original)
entries=json.loads(original);carrier=R/json.loads((R/'_shots/carrier_turbulence_1028/video/latest.json').read_text())['folder'];carrierProof=json.loads((carrier/'report.json').read_text());src=F.relative_to(R).as_posix();changes=[]
updates={
 'stage6-carrier':dict(src='/'+carrierProof['video'],poster='/'+carrier.relative_to(R).as_posix()+'/full-red.png',seconds=carrierProof['seconds'],title='Harrier — current mounted lasers, whole-hull flash and turbulence',note='Current local native Furious Carrier fight: selected hull mounts, first/both fan loss turbulence, complete red hull pulses and original Nightwing handoff. GOD/input observer; original enemy HP and phases.'),
 'stage6-nightwing':dict(src='/'+proof['video'],poster='/'+src+'/cruise.png',seconds=proof['duration'],title='Nightwing — consistent aircraft through turns and hit flashes',note='Fresh current native Furious life through defeat. One canonical hull across normal, bank, roll, turn, depth and white-hit frames. Level5 laser/40-missile GOD/input setup; first35s withhold player fire. Enemy HP/attack phases stay native.'),
 'stage6-nightwing-shadow-turn':dict(src='/'+clips['turn']['path'],poster='/'+src+'/turn.png',seconds=clips['turn']['seconds'],title='Nightwing — current matching banked turn and shadow',note='Continuous normal-speed excerpt from the current native fight. Uses the same aircraft and matching white-hit/shadow pixels throughout.'),
 'stage6-nightwing-wind':dict(src='/'+clips['wind']['path'],poster='/'+src+'/wind.png',seconds=clips['wind']['seconds'],title='Nightwing — current aircraft and animated wind volley',note='Continuous normal-speed excerpt from the current native fight, with the corrected aircraft identity and current teal wind gusts.')}
for e in entries:
 if e['id']not in updates:continue
 old=dict(e);e.setdefault('archiveSrc',e['src']);e.update(updates[e['id']]);e['currentLocal']=True;changes.append(dict(id=e['id'],previous=old,current=e))
manifest.write_text(json.dumps(entries,indent=2,ensure_ascii=False),encoding='utf8')
p=gallery/'index.html';s=p.read_text(encoding='utf8');b=gallery/'index.before-nightwing-current-1028.html'
if not b.exists():b.write_bytes(p.read_bytes())
s=s.replace('<a id="download">Open / download this video</a>','<a id="download">Open / download this video</a><a id="archive" hidden>Earlier release recording</a>')if'id="archive"'not in s else s
s=s.replace("player.src=local?'_media/'+c.id+'.mp4':c.src;","player.src=c.currentLocal?c.src:local?'_media/'+c.id+'.mp4':c.src;")
s=s.replace("$('#download').href=c.src;$('#status').textContent='';","$('#download').href=c.src;$('#archive').hidden=!c.archiveSrc;$('#archive').href=c.archiveSrc||'';$('#status').textContent=c.currentLocal?'Current local recording — corrected aircraft frames.':'';")
s=s.replace("fetch('manifest.json')","fetch('manifest.json?v=nightwing-current-1028')")
s=s.replace('Current game update, the new Nightwing wind/shadow/turn footage, full Stage6 fights, Stage7 and9 minibosses/bosses, plus separate Stage8 phases and alternate forms.','Current local Carrier and Nightwing revisions: consistent flight/hit silhouettes, whole-hull red flashing and fan-loss turbulence. Other cards retain their recorded versions.')
s=s.replace('Updated game checks pass for the Nightwing changes. The full regression suite still reports the same five previously recorded failures; details and source are included in the repository’s October28 review report.','Current Nightwing identity/render and combat checks pass. The full suite remains blocked by the existing missing retired-art archive manifest.')
start=s.find('let currentMediaURL=');start=s.index('function show(')if start<0 else start;end=s.index('player.addEventListener',start)
s=s[:start]+'''let currentMediaURL=null,currentMediaController=null,currentMediaRevision=0;
function show(c,play=false){
 const revision=++currentMediaRevision;player.pause();player.removeAttribute('src');player.load();
 if(currentMediaController)currentMediaController.abort();if(currentMediaURL){URL.revokeObjectURL(currentMediaURL);currentMediaURL=null;}
 const source=c.currentLocal?c.src:local?'_media/'+c.id+'.mp4':c.src;player.dataset.source=source;player.poster=c.poster;
 $('#title').textContent='Stage '+c.stage+' — '+c.title;$('#note').textContent=c.note||'';$('#download').href=c.src;$('#archive').hidden=!c.archiveSrc;$('#archive').href=c.archiveSrc||'';
 $('#status').textContent=c.currentLocal?'Loading current recording…':'';document.querySelectorAll('.card').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.id===c.id)));history.replaceState(null,'','#clip='+c.id);
 const apply=url=>{if(revision!==currentMediaRevision)return;player.src=url;player.load();if(play)player.play().catch(()=>{});};
 if(c.currentLocal){currentMediaController=new AbortController();fetch(source,{signal:currentMediaController.signal}).then(r=>{if(!r.ok)throw Error('Current recording could not load.');return r.blob()}).then(blob=>{if(revision!==currentMediaRevision)return;currentMediaURL=URL.createObjectURL(blob);apply(currentMediaURL);$('#status').textContent='Current local recording — corrected aircraft frames.';}).catch(e=>{if(e.name!=='AbortError'&&revision===currentMediaRevision)$('#status').textContent=e.message;});}
 else apply(source);
}
addEventListener('beforeunload',()=>{if(currentMediaController)currentMediaController.abort();if(currentMediaURL)URL.revokeObjectURL(currentMediaURL);});
'''+s[end:]
p.write_text(s,encoding='utf8')
chapters=[(0,'Native arrival'),(turnStart,'Banked flyover and turn'),(windStart,'Wind charge and volley'),(35,'Normal and white-hit combat')];buttons=''.join(f'<button data-time="{t:.3f}">{label}</button>'for t,label in chapters)
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Nightwing — consistent aircraft frames</title><style>*{box-sizing:border-box}body{margin:0;background:#0b131e;color:#eaf4fa;font:16px/1.5 system-ui}main{max-width:1328px;margin:auto;padding:24px}h1{font-size:clamp(26px,4vw,38px);margin:0 0 8px}p{color:#bfd2dd}video{display:block;width:100%;aspect-ratio:16/10;background:#000;border:1px solid #32706d}nav{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}button{font:inherit;color:#ecffff;background:#123a3b;border:1px solid #458b89;padding:10px 13px;cursor:pointer}button:focus-visible{outline:2px solid #ffe3a5}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:700px;margin:24px auto}figure{margin:0}img{width:100%;display:block;background:#10202a;image-rendering:pixelated}figcaption{padding-top:7px}.note{font-size:14px}@media(max-width:700px){main{padding:14px}}</style></head><body><main><h1>Nightwing — one aircraft through every frame</h1><p>The banked frame and its white hit frame share the same silhouette. The review player now uses current footage; the older Carrier release film contained the retired jet with extra fins.</p><div class="pair"><figure><img src="../../../_shots/nightwing_shape_1028/current-bank.png" alt="Current teal banked aircraft"><figcaption>Current banked frame</figcaption></figure><figure><img src="../../../_shots/nightwing_shape_1028/current-hit.png" alt="Matching white hit frame with the identical silhouette"><figcaption>Its matching white hit frame</figcaption></figure></div><video id="v" controls playsinline preload="auto" poster="../../../FOLDER/cruise.png" data-src="../../../MOVIE"></video><nav>BUTTONS</nav><p><a href="../../../_shots/github_review_1028/index.html?revision=nightwing-current-1028#clip=stage6-carrier">Open the updated Carrier review player</a></p><p class="note">Complete current native Furious Nightwing life through defeat. GOD/input bot with level5 laser and40 missiles; normal allies remain. The bot withholds player fire for35s for a clear flight view. Enemy health, phases and timers remain native after ace-spawn setup.</p><p id="status" class="note">Loading replay…</p></main><script>let mediaURL;fetch(v.dataset.src).then(r=>{if(!r.ok)throw Error('Replay load failed');return r.blob()}).then(b=>{mediaURL=URL.createObjectURL(b);v.src=mediaURL;v.load();document.querySelector('#status').textContent='Replay ready — press Play or choose a chapter.'}).catch(e=>document.querySelector('#status').textContent=e.message);document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{v.currentTime=+b.dataset.time;v.play().catch(()=>{})});addEventListener('beforeunload',()=>{if(mediaURL)URL.revokeObjectURL(mediaURL)});</script></body></html>'''.replace('FOLDER',src).replace('MOVIE',proof['video']).replace('BUTTONS',buttons)
P=R/'docs/previews/nightwing_current_1028';P.mkdir(parents=True,exist_ok=True);(P/'index.html').write_text(page,encoding='utf8')
qa=dict(request='Nightwing plane identity inconsistent between the supplied normal/banked and white-hit frames.',finding='Retired Part2 banked planform in the older stage6-carrier release film. Current source-locked banks already contain the corrected identity.',native=probe,combatRegression=reg,film=proof,galleryUpdates=changes,chapters=chapters,clips=clips,gameplayOrRasterChanges=False,fullSuite=dict(exit=int((O/'full-suite-exit.txt').read_text().strip()),reachedFinalSummary=False,reason='Existing missing UNUSED_ASSETS/retired_art_1022/manifest.json'))
(R/'docs/qa/nightwing_current_1028.json').write_text(json.dumps(qa,indent=2));fps=proof['film']['audio']['frames']/proof['duration']
note=f'''# Nightwing current aircraft and review routing — October28

Mike supplied two frames from the stage6-carrier review movie. The teal banked aircraft matches the retained legacy whole.png bank66, which has the retired Part2 extra stabilizers; the regular white-hit aircraft uses the original planform. The installed identity_1028b / flight_1028c banks already use one canonical sky_repair aircraft. No additional hull redesign, generation, raster or gameplay changes were needed.

{len(probe['checks'])} focused source/native checks and{len(reg['checks'])} existing wind-combat regressions pass. Every live white-hit bank has exact source alpha/pivots for its normal partner. Actual native normal/hit coverage matches across10 idle/bank/roll/somersault/inverted/heading/flyover/drift/return configurations, using two backgrounds to recover coverage on the opaque game canvas. Real native damage/white pixels/expiry and removed-fin collision are verified. No game/draw/console/HTTP errors.

Fresh complete current Nightwing life: {proof['duration']:.2f}s, {fps:.2f}fps, decoded peak{proof['decodedPeakDb']:.1f}dB, all9 film checks pass. Native ace-spawn setup skips the Carrier; Furious GOD/input bot, level5 laser/40 missiles, first35s without player fire, ordinary allies. No enemy HP/phase/timer writes after setup. Browser audio retrigger/close cancellations remain recorded separately ({len(proof['expectedRequestCancellations'])} ERR_ABORTED requests); no non-cancellation network failures. Source hashes remain stable. Native defeat, wind, multiple full turn/return cycles and real white hit frames are recorded.

The existing local GitHub review player now routes its Carrier, Nightwing full fight, turn and wind cards to these current local recordings; the Carrier uses the latest108.76s native turbulence recording. Original MP4s are preserved, with earlier-release links and pre-update page/manifest snapshots. The currentLocal flag also respects updated recordings when the player uses its local query mode. No GitHub release files, commits or pushes are changed.

Review `docs/previews/nightwing_current_1028/index.html` and the existing `_shots/github_review_1028/index.html#clip=stage6-carrier`. Evidence `docs/qa/nightwing_current_1028.json`; portable probe/recorder/finalizer use nightwing_current_1028 names. Syntax passes. Full suite exits1 before summary on the existing missing archive manifest.
'''
(R/'docs/NIGHTWING_CURRENT_REVIEW_1028.md').write_text(note,encoding='utf8')
h=R/'HANDOFF_CODEX.md';raw=h.read_bytes();title='## 2026-10-28 — Current Nightwing frames in the Carrier review player'
if title.encode()not in raw:
 header=f'''{title}

Mike's normal/banked versus white-hit mismatch came from the older stage6-carrier release film's retired Part2 bank. Installed source-locked identity/flight banks are correct. {len(probe['checks'])} new source/native-render checks +{len(reg['checks'])} combat regressions verify matching hit silhouettes, real damage/expiry and removed-fin collision. No hull art or gameplay edits.

Fresh complete{proof['duration']:.2f}s native Furious GOD/input Nightwing life at{fps:.2f}fps, audible unclipped sound and9 film checks pass. Existing local GitHub gallery Carrier/Nightwing/turn/wind cards now use current local films; earlier media and release links are preserved. Review docs/previews/nightwing_current_1028/index.html; docs/NIGHTWING_CURRENT_REVIEW_1028.md and docs/qa/nightwing_current_1028.json. Full suite exits1 before summary on missing archive manifest. No game.js/test_fl.js edits, commit or push.

''';h.write_bytes(header.replace('\n','\r\n').encode()+raw)
print(json.dumps(dict(video=proof['video'],checks=len(probe['checks']),regression=len(reg['checks']),fps=fps,gallery=[c['id']for c in changes],clips=clips)))
