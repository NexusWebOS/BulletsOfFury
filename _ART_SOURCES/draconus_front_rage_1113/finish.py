from pathlib import Path
import json, hashlib, shutil, subprocess, zipfile
import imageio_ffmpeg
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

W = Path(__file__).resolve().parent
R = Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
O = W.parents[1] / 'outputs/Draconus-frontal-and-rage'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = json.loads((O/'checks.json').read_text())
installation = json.loads((W/'installation.json').read_text())
recording = json.loads((O/'recording-verification.json').read_text())
broad = json.loads((W/'broad-checks.json').read_text())
assert len(checks['checks']) == 23 and all(c['passed'] for c in checks['checks']) and not checks['errors']
assert checks['runtimeHash'] == installation['runtime'] == sha(R/'assets/draconus_front_rage_1113.js')
assert checks['rageHash'] == installation['rageOwner'] == sha(R/'assets/rage_palm_1110.js')
assert all(sha(R/n) == h for n,h in installation['protected'].items())
assert recording['complete'] and recording['nativeSourcesUnchanged'] and not recording['errors']
assert recording['stats']['peak'] > .001 and not recording['stats']['tapErrors']
assert set(recording['phases']) == {'rage','kame_fire','foreground','background','beam'}
movie = O/'draconus-frontal-strikes-full-rage.mp4'
assert recording['sha256'] == sha(movie)
completion = [e for e in recording['stats']['events'] if e['type']=='rage-book-complete']
assert len(completion) == 1 and completion[0]['cycles'] == 3
assert all(x['exit']==0 for x in broad if x['name']!='full-suite')

# A shorter, continuous excerpt makes the previously missing rage easy to see.
ff = imageio_ffmpeg.get_ffmpeg_exe()
rage_start = next(c['at'] for c in recording['chapters'] if c['label']=='Rage transformation') - .5
rage_movie = O/'draconus-rage-transformation-and-attacks.mp4'
if not rage_movie.exists():
    subprocess.run([ff,'-v','error','-ss',str(rage_start),'-i',str(movie),
        '-map','0:v:0','-map','0:a:0','-c:v','libx264','-threads','2','-preset','fast',
        '-crf','19','-c:a','aac','-b:a','128k','-movflags','+faststart',str(rage_movie)],
        capture_output=True,check=True)
subprocess.run([ff,'-v','error','-threads','2','-i',str(rage_movie),'-f','null','-'],
    capture_output=True,check=True)
rage_media=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error',
    '-show_streams','-show_format','-of','json',str(rage_movie)]))
assert {s['codec_type'] for s in rage_media['streams']} >= {'video','audio'}

page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Draconus: frontal strikes and full rage</title><style>body{max-width:1280px;margin:24px auto;padding:0 18px;background:#101820;color:#edf5ff;font:17px/1.5 system-ui}h1{font-size:28px}h2{font-size:22px}video{width:100%;background:#05090e}article{margin:24px 0;padding:18px;background:#192432;border:1px solid #3d4b5d}button{font:inherit;margin:6px;padding:9px;background:#d9edff;color:#102131;border:0;border-radius:3px;cursor:pointer}button:focus-visible{outline:3px solid #ffe16c}a{color:#91d9ff}small{display:block;margin-top:12px}</style><h1>Draconus: frontal strikes and full rage</h1><p>Center, left and right hammer smashes keep his face and chest toward you in normal and Chromium armor. His low-health rage now enters before the form-return timer and completes the opening wave, foreground palms, background palms and repeat wave.</p><p>Recorded directly from the updated game on Furious, with native animation and sound. These are prepared animation checkpoints with an invulnerable observer, not a full-stage or unassisted fight clear.</p><article><h2>Full preview</h2><video id="full" controls preload="metadata" src="draconus-frontal-strikes-full-rage.mp4"></video><div id="chapters"></div><small>The hammer portion includes the complete four-contact attack and the alternating diagonal pair in both armor forms. The rage portion runs continuously through its native completion.</small></article><article><h2>Jump straight to rage</h2><video id="rage" controls preload="metadata" src="draconus-rage-transformation-and-attacks.mp4"></video><small>Continuous excerpt from the full preview; same gameplay and sound.</small></article><p><a href="README.md">Changes and checks</a> · <a href="BOF-Draconus-frontal-rage-sources.zip">Recovery sources</a></p><script>const chapters=CHAPTERS;const full=document.querySelector('#full');for(const c of chapters){const b=document.createElement('button');b.textContent=c.label;b.onclick=()=>{full.currentTime=c.at;full.play()};document.querySelector('#chapters').append(b)}for(const v of document.querySelectorAll('video'))v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()}));</script></html>'''.replace('CHAPTERS',json.dumps(recording['chapters']))
(O/'playback.html').write_text(page,encoding='utf-8')
errors=[];seeks=[]
with sync_playwright() as pw:
    br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
    p=br.new_page(viewport={'width':1400,'height':1000})
    p.on('pageerror',lambda e:errors.append(str(e)))
    p.goto((O/'playback.html').as_uri())
    for name,points in [('full',[.03,.35,.68,.91,.975]),('rage',[.15,.7,.93])]:
        p.wait_for_function('id=>{const v=document.getElementById(id);return v.readyState>=1&&Number.isFinite(v.duration)}',arg=name,timeout=30000)
        for point in points:
            q=p.evaluate('''async({id,point})=>{const v=document.getElementById(id);v.currentTime=v.duration*point;await new Promise((ok,no)=>{v.addEventListener('seeked',ok,{once:true});setTimeout(()=>no(Error('Video seek timeout')),15000)});await v.play();await new Promise(ok=>setTimeout(ok,180));v.pause();if(v.error)throw Error(v.error.message);return{id,seconds:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight}}''',dict(id=name,point=point))
            assert q['width']==1280 and q['height']==844
            seeks.append(q)
    assert p.locator('#chapters button').count()==len(recording['chapters'])
    p.locator('#chapters button').filter(has_text='Rage transformation').click()
    p.wait_for_timeout(250)
    q=p.evaluate('()=>{const v=document.querySelector("#full");return{at:v.currentTime,paused:v.paused}}')
    assert not q['paused'] and abs(q['at']-(rage_start+.5))<2
    p.evaluate('()=>document.querySelector("#full").pause()')
    p.screenshot(path=str(O/'playback-preview.png'),full_page=True)
    br.close()
assert not errors
(O/'playback-verification.json').write_text(json.dumps(dict(seeks=seeks,chapterButton=q,errors=errors),indent=2))

# Record the existing authored banks, rather than making replacement art.
def literal(file,mark):
    text=(R/'assets'/file).read_text()
    return json.JSONDecoder().raw_decode(text[text.index(mark)+len(mark):].lstrip())[0]
art=literal('overhead_slam_art_1111.js','Object.assign(BA119_ART,')
rage=literal('rage_palm_art_1110.js','const RF1110_ART=')
sources=[]
for name in ['corrupt-overhead','corrupt-overhead-left','corrupt-overhead-right']:
    a=art[name]
    for mat in ['regular','chrome','red','hit','red_hit']:
        source=R/f'assets/game/shared/combat/{a["folder"]}/{name}_{mat}.webp'
        if source.exists():
            sources.append(dict(bank=name,material=mat,path=source.relative_to(R).as_posix(),
                cell=a['cell'],count=a['count'],pivot=a['pivot'],sha256=sha(source)))
for name,a in rage['banks'].items():
    if not name.startswith('drac'): continue
    for source in (R/'assets/game/shared/combat/rage_palm_1110').glob(name+'_*.webp'):
        sources.append(dict(bank=name,path=source.relative_to(R).as_posix(),
            cell=[a['cw'],a['ch']],count=a['count'],pivot=a['pivot'],sha256=sha(source)))

archive=R/'_ART_SOURCES/draconus_front_rage_1113'
archive.mkdir(exist_ok=True)
for name in ['draconus_front_rage_1113.js','rage_palm_1110.before.js','install.py','verify.py','setup.js','record.py','capture.js','capture-audio.js','checks.py','finish.py','installation.json','broad-checks.json']:
    shutil.copy2(W/name,archive/name)
shutil.copy2(R/'assets/rage_palm_1110.js',archive/'rage_palm_1110.after.js')
(archive/'authored-source-hashes.json').write_text(json.dumps(sources,indent=2))
patch=dict(runtime='assets/draconus_front_rage_1113.js',scriptInclude='<script src="assets/draconus_front_rage_1113.js?v=1"></script>',
    scriptPosition='After the current late owners, immediately before </body>.',rageOwner='assets/rage_palm_1110.js',
    before='if(b._r30.v18.donorAge>52){Q.rf1110=null;Q.action=null;Q.cool=.8;}',
    after='if(b._r30.v18.donorAge>52&&R.cycle>=3){Q.rf1110=null;Q.action=null;Q.cool=.8;}',
    protected=installation['protected'])
(archive/'patch.json').write_text(json.dumps(patch,indent=2))

readme=f'''# Draconus frontal strikes and full rage — November13,2026

Mike reported that Draconus turned away during strikes and that his rage form/attacks were missing. This correction is installed in the actual game. The late DFR13 owner selects the existing approved complete frontal center/left/right overhead drawings for Draconus, normal and Chromium. It replaces the copied boss's profile selectors only, including Furious contacts3/4 and the standalone two-strike side action. His face/chest remain toward the player through lift, contact and recovery. The metal hammer remains part of each complete authored character drawing. No new artwork, body assembly, interpolated sprite or runtime raster rotation is introduced. Chronos's recovered profile side sweeps and intentional whirlwind turns keep their owners.

The native hit clocks, four-contact Furious count, physical head landmarks, planted origin, native sounds and FOV/impact reticles remain. For the standalone diagonal pair, lift/recovery are harmless and the actual measured cap is the native impact location at0.35/1.05 seconds after tell. Native per-strike hit sets remain.

Two actual rage timing bugs are corrected. First, at low health the native copied-form return could win during the idle cooldown after an action. DFR13 commits the existing native rage at that action boundary when Chromium/opening/HP requirements are met. It does not heal the boss or reset the copied-form clock. Second, rage_palm_1110 previously allowed the52-second copied-form limit to end the rage book after the first foreground volley. Its Draconus-only exit now waits until cycle3: opening charged wave, all foreground palm groups, all background palm groups, then the repeat charged wave. It still returns finitely through the original owner with unchanged native HP and defeated gun/hammer pools. This uses Draconus's existing red full-body rage drawings and existing audio. Stage5 Chronos's critical original C45/C46/C47/CF48/CF49/CF50 transformation and Kamehameha/audio remain byte-identical.

{len(checks['checks'])} focused checks pass in actual Chromium, with no page/update/draw errors. They cover both materials and all directions throughout the complete four-contact action; frontal diagonal pair windup/contact/recovery; measured real impact locations; actual native damage and visible white flash/expiry; low-health rage commitment after the copied-form clock is overdue; formation/opening wave, complete foreground/background palm groups and repeat wave; finite cycle3 return without HP restoration; permanent defeated weapon pools; retained live independent modular gun; and protected source hashes. The fast probe snapshots are not the recording. The actual continuous recording uses the complete native animation/update path, with normal flash expiry, and its inspected frames visibly show the red rage body.

Open playback.html for chapter buttons. The {float(recording['media']['format']['duration']):.1f}-second full preview shows prepared normal/Chromium hammer checkpoints followed by one continuous native low-health rage sequence. The {float(rage_media['format']['duration']):.1f}-second rage-only movie is an excerpt of that same recording. Both contain decoded H264/AAC sound; {len(seeks)} player seeks and the actual rage chapter button pass. All five required rage phase markers were observed. Native palm rounds, cues, source hashes and continuous timeline are recorded in recording-verification.json. The observer is invulnerable and the low-health checkpoint is explicitly prepared; this is not a full-stage or unassisted balance clear. Earlier Stage5–8 stress films and the November12 Draconus side-only preview predate this correction.

Required syntax checks pass. The full test_fl.js suite still exits1 before its final summary on the existing missing difficultyHealthBaseline15 helper at assets/combat_polish_0927b.js:151. Exact output is preserved in full-suite.log. This does not certify release readiness.

Production changes are assets/draconus_front_rage_1113.js, its final index.html include, and the one Draconus exit guard in assets/rage_palm_1110.js. Game.js, restored Stage5 owners, recovered side assets, all overhead art, ships and independently rotating modular guns retain their original bytes. No commit, push, installer or publication. Source/patch history is in _ART_SOURCES/draconus_front_rage_1113; patch.json describes the exact integration and authored-source-hashes.json locates the reused original art. This is a recovery patch for the existing game, not a standalone game build. Canonical copied-boss names remain Dracodia/Chronos in game code.
'''
for file in [O/'README.md',archive/'README.md',R/'docs/DRACONUS_FRONT_RAGE_1113.md']:
    file.write_text(readme,encoding='utf-8')
summary=dict(checks=len(checks['checks']),errors=checks['errors'],broad=broad,
    runtime=checks['runtimeHash'],rageOwner=checks['rageHash'],protected=installation['protected'],
    playbackSeeks=len(seeks),chapterButtonPassed=True,phases=recording['phases'],rageCompletion=completion,
    fullVideo=dict(seconds=recording['media']['format']['duration'],sha256=recording['sha256']),
    rageExcerpt=dict(seconds=rage_media['format']['duration'],sha256=sha(rage_movie),sourceStart=rage_start),
    assistance='Prepared native checkpoints and invulnerable observer; not a full-stage clear.')
(O/'verification.json').write_text(json.dumps(summary,indent=2))
qa=R/'docs/qa/draconus_front_rage_1113'
qa.mkdir(parents=True,exist_ok=True)
for file in [O/'checks.json',O/'verification.json',O/'playback-verification.json',W/'broad-checks.json',W/'full-suite.log']:
    shutil.copy2(file,qa/file.name)
for file in [O/'checks.json',O/'verification.json']:
    shutil.copy2(file,archive/file.name)

note='''## November13,2026 — Draconus frontal strikes and complete native rage

Mike requires Draconus's face/chest to remain toward the player during hammer
strikes. DFR13 selects existing whole frontal center/left/right banks in both
normal/Chromium, including Furious contacts3/4 and the alternating diagonal pair.
This supersedes November12's Draconus profile-side selector only. Chronos's
recovered side sweeps, original Stage5 transformation/Kamehameha, ships, gun
exceptions, whirlwind and whole-held-hammer rules remain protected.
Low-health Chromium rage now commits at the native action boundary before the
copied-form return can win. The Draconus-only RF1110 exit requires cycle3, so the
opening wave, foreground palms, background palms and repeat wave all finish.
No healing, copied-form clock reset or defeated-weapon restoration. Native HP,
warnings, round owners, sounds and white hit feedback remain.
23 native checks pass; actual continuous audible preview visibly shows both
frontal armor forms and red rage/full attack book.8 player seeks and chapter
button pass. Prepared native checkpoints/invulnerable observer, not full clears.
Full suite retains existing difficultyHealthBaseline15 abort; no release claim.
Docs: docs/DRACONUS_FRONT_RAGE_1113.md; _ART_SOURCES/draconus_front_rage_1113.
No game.js edit, commit, push, installer or publication.

'''
file=R/'HANDOFF_CODEX.md'
old=file.read_bytes();heading=note.splitlines()[0].encode('utf-8')
if heading not in old:
    assert file.read_bytes()==old
    file.write_bytes(note.encode('utf-8')+old)
rule='''

## November13 — Draconus must remain frontal; complete native rage

Mike explicitly requires Draconus to keep his face and chest toward the player
during center, left and right hammer smashes, normal and Chromium. DFR13 selects
the existing complete frontal overhead banks throughout the four-contact Furious
attack and alternating diagonal pair. This supersedes November12's Draconus
profile-side selector only; Chronos's recovered side sweeps remain. Intentional
whirlwind turns retain their owner. Do not assemble held hammers or rotate plates.
Preserve the native low-health rage commitment at the action boundary, before
the copied-form return, and at least its full opening wave/foreground palms/
background palms/repeat-wave book before finite cycle3 exit. Do not heal, reset
the copied-form clock or restore defeated gun/hammer HP to make rage appear.
Keep Draconus's red authored form, native audio/white hit flash, ships/modular guns
and critical original Stage5 C45/C46/C47/CF48/CF49/CF50 formation/wave untouched.
Evidence/recovery: docs/DRACONUS_FRONT_RAGE_1113.md.
'''
file=R/'AGENTS.md';old=file.read_bytes()
if rule.splitlines()[2].encode('utf-8') not in old:
    assert file.read_bytes()==old
    file.write_bytes(old+rule.encode('utf-8'))
with zipfile.ZipFile(O/'BOF-Draconus-frontal-rage-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
    for file in archive.rglob('*'):
        if file.is_file(): z.write(file,file.relative_to(archive))
assert all(sha(R/n)==h for n,h in installation['protected'].items())
assert sha(R/'assets/draconus_front_rage_1113.js')==installation['runtime']
assert sha(R/'assets/rage_palm_1110.js')==installation['rageOwner']
print('Finished:23 native checks,8 video seeks, working rage chapter, full native recording and recovery handoff.',flush=True)
