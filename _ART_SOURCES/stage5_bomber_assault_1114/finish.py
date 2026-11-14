from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib,zipfile
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Stage5-bomber-assault';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=json.loads((O/'checks.json').read_text());G=json.loads((O/'weapon-gate/weapon-gate-checks.json').read_text());I=json.loads((W/'installation.json').read_text());A=json.loads((W/'editable-verification.json').read_text());V=json.loads((O/'recording-verification.json').read_text());Q=json.loads((O/'required-checks.json').read_text());M=json.loads((W/'manifest.json').read_text())
assert all(q['passed']for q in C['checks'])and not C['errors']and C['runtimeHash']==sha(R/'assets/stage5_bomber_assault_1114.js')
assert all(q['pass']for q in G['checks'])and not any(G[k]for k in ['pageErrors','consoleErrors','HTTPerrors'])
assert all(sha(R/n)==h for n,h in I['protected'].items())and all(sha(R/'assets'/n)==h for n,h in I['installed'].items())
assert all(sha(R/'assets/game/levels/stage_05/miniboss/assault_1114'/n)==h for n,h in I['textures'].items())
assert A['exactFrames']==1136 and A['banks']==46 and not A['errors']
assert all(q['returncode']==0 for q in Q[:3])and Q[3]['returncode']==1 and 'difficultyHealthBaseline15 is not defined'in Q[3]['tail']
assert V['complete']and V['nativeSourcesUnchanged']and not V['errors']and not V['stats']['tapErrors']and V['stats']['peak']>.001
assert all(sha(R/n)==h for n,h in V['sourceHashes'].items())and len(V['playbackSeeks'])==4
movie=O/'stage5-bomber-furious-final.mp4';assert sha(movie)==V['sha256']
old=(W/'index.before.html').read_bytes().decode('utf-8');nl='\r\n'if'\r\n'in old else'\n';added='<script src="assets/stage5_bomber_assault_art_1114.js?v=1"></script>'+nl+'<script src="assets/stage5_bomber_assault_1114.js?v=1"></script>'+nl
assert(R/'index.html').read_bytes().decode('utf-8')==old.replace('</body>',added+'</body>')
board=Image.new('RGB',(1280,838),'#08121c');d=ImageDraw.Draw(board)
for i,(label,name)in enumerate([('Committed cannon bursts','native-cannon-burst.png'),('Warned bombing overflight','native-bombing-overflight.png'),('Shadowed return','native-shadowed-return.png'),('Catch up to re-engage','native-catching-up.png')]):
 im=Image.open(O/name).convert('RGB').resize((640,400),Image.Resampling.NEAREST);x=i%2*640;y=i//2*419;board.paste(im,(x,y+19));d.text((x+10,y+3),label,fill='white')
board.save(O/'visual-proof.png')
total=len(C['checks'])+len(G['checks']);seconds=float(V['media']['format']['duration'])
readme=f'''# Stage5 Eclipse Siege Bomber assault — November14,2026

Mike requested a more challenging and engaging Stage5 miniboss: thrust away, turn and charge toward the player while bombing, pass overhead with shadows, then let the player catch up. He also requested exclusive enemy targeting retinas with Stage4-style alert behavior, repeated laser-cannon bursts, cooling and reacquisition.

The actual Stage5 miniboss is the Earth-skinned Eclipse Siege Bomber. The existing pursuit_1027 controller is Stage6-only, so S5B14 supplies a scoped Stage5 controller without moving Stage6 onto a different owner. It adds assets/stage5_bomber_assault_art_1114.js and assets/stage5_bomber_assault_1114.js as the final two includes in index.html, plus textures in assets/game/levels/stage_05/miniboss/assault_1114. The rest of index.html is byte-preserved. Native game.js and the protected combat, four-module gate, roster, difficulty, Chronus rage and current Draconus source owners are unchanged.

The cycle is native entry → stalk/bombs → tracking optic → committed aim → cannon bursts → reacquire/burst → visible cooling → a second burst/cooling cluster → spool/thrust away → distant turnaround → accelerating head-on bombing charge → large foreground overflight → offscreen turn → shadowed return → catch-up → stalk. Moving forward shortens catch-up; a finite fallback always returns him to the damage plane. Surviving engines supply the visible thrusters. Breaking an engine slows the retreat/return; it never restores parts or health.

Each live cannon tracks a live pilot through its tell, commits .38 seconds before release and fires along that locked aim. The hull holds its committed position; the new scope bypasses only this bomber's additive space bob once his authored flight owner starts. The actual visible rear-facing barrel and muzzle/round origin agree. Easy/Normal/Hard/Furious use3/4/5/6 rounds per cannon in each group. Shared15% firing/targeting-rate rules remain; warning, flight, projectile travel and cooldown readability are separately authored. After two groups the cannon cycles through its existing mechanical cooling/retraction art, waits, reacquires and repeats. These enemy optics never enter the player's Retina/input target system. Their clear center does not cover the ship. Ordinary red laser rounds are non-interceptable immediately at spawn and carry the real live-cannon owner.

The bombing charge releases fixed warned placements across the playfield, with a reserved corridor around the committed safe column. Easy drops one bomb per row; the other difficulties drop two. Impact uses native green/yellow/red ground targeting, native hit timing/sound and the actual approved falling bomb art. The overflight is on the upper plane: the hull cannot ram the player, absorb player rounds or remain a stale Retina target. A silhouette shadow leads the pass instead of hiding underneath the giant hull. The large aircraft draws above the player; native impact warnings stay visible above that foreground hull without duplicate reticles. Released hazards remain native ground targets. Bombs cap at24 and owned cannon rounds at128. Destruction, leaving the fight and restarting clear owned attacks; cannon destruction cancels that cannon's pending and released fire. If both cannons are destroyed, the remaining core uses a finite bomb-pressure opening instead of resurrecting guns.

The four real module pools still protect the core until all four have broken. Native point, solid, beam, actual space-pulse, Retina and stale-lock paths are preserved. Modules visibly flash white on actual damage and expire normally. Core/module HP, native breakup, score, reward and once-only defeat remain. No health inflation, healing, recreated modules or forced flight-phase skips were added.

Aircraft pixels come directly from the existing approved hull, engines and sixteen-frame cannon master. The correction also turns the cannon pixels to face the real firing direction. Sixteen aircraft headings, thirty-two prepared distance sizes, registered white-hit partners, native plume phases, laser/muzzle headings and actual hull silhouette shadows are exported offline. The exclusive sixteen-frame amber/red enemy optic is newly generated with the built-in image tool; its empty center and clean binary-alpha ring are audited. No PixelLab credits were used. No runtime raster rotation, tinting, generated shapes or per-frame canvases are added. All46 editable Aseprite banks roundtrip exactly across1,136 frames, including materials, sizes, headings and effects. This is not a claim of1,136 newly drawn aircraft poses.

Verification: {len(C['checks'])} focused native behavior/damage/contact/death checks plus{len(G['checks'])} actual weapon/core-gate checks ({total} total) pass across all four difficulties. Two complete cycles per difficulty preserve the original full HP budgets. The native player-contact test proves an overhead hull is safe and a same-plane hull still contacts; breaking a real engine slows the retreat; breaking a real cannon cancels it. Committed target and live barrel origins match. Pause, all-pilots-dead stop, finite catch-up, native core opening, actual white sprite feedback, reward/death cleanup and Stage6 isolation pass. No page/update/draw/HTTP errors occur in these checks. Detailed results and full native traces are preserved.

The final{seconds:.1f}-second actual Furious preview contains native entry and two complete attack/flight cycles, real sound, original full HP, native keyboard movement and no attack-phase skips. It has an explicitly labeled invulnerable review pilot. It is a behavior/graphics preview, not a survival clear, a full-stage recording or a balance/release verdict. H264/AAC decoding, non-silent mixer output, source hashes and four playback seeks pass. Open playback.html or stage5-bomber-furious-final.mp4. The earlier stage5-bomber-furious-preview.mp4 is the preliminary shadow placement and is superseded by the final movie.

Required syntax checks pass. The full _BUILD_SOURCE/test_fl.js suite still exits1 before its summary on the existing missing difficultyHealthBaseline15 helper at assets/combat_polish_0927b.js:151. Its exact output is in full-suite.log. Mike's home playtest is still needed for the unassisted balance and complete game experience.

Recovery: generated/ contains the unmodified new optic master, references/ preserves native input masters/metadata, exports/ contains editable Aseprite and lossless runtime sheets, and source-hashes.json identifies the package. Rebuild in the existing project using build.py → author.py → manage.py --install → --verify / --gate / --checks → --record → --finish. Paths are local to Mike's project; Python/Pillow/numpy/scipy/Playwright, ffmpeg/ffprobe, Aseprite and the existing native review helpers are dependencies. The package is a patch for the existing game, not a standalone build. Runtime action timings are in the controller; .06-second Aseprite preview durations do not override those timings.

Source-only integration. No commit, push, installer or publication. The critical original Stage5 Chronus formation/Kamehameha and current Draconus normal/Chromium/rage/ship/modular-gun work remain protected.
'''
source=R/'_ART_SOURCES/stage5_bomber_assault_1114';source.mkdir(exist_ok=True);shutil.copytree(W/'generated',source/'generated',dirs_exist_ok=True);ref=source/'references';ref.mkdir(exist_ok=True)
native=['assets/game/shared/combat/polish_0927b/bomber.png','assets/game/levels/stage_05/miniboss/performance_1020/bomber_cannon.webp','assets/game/shared/combat/combat_1003i/laser_beams.png','assets/game/shared/combat/combat_1003i/laser_muzzles.png','assets/game/shared/effects/director_0927/specialist.png','assets/performance_finish_art_1020.js','assets/combat_art_1003i.js','assets/director_art_0927.js']
for n in native:shutil.copy2(R/n,ref/Path(n).name)
(ref/'native-inputs.json').write_text(json.dumps({n:sha(R/n)for n in native},indent=2))
for p in W.iterdir():
 if p.is_file()and p.suffix in ['.py','.js','.lua','.json','.log','.md','.html']:shutil.copy2(p,source/p.name)
ex=source/'exports';ex.mkdir(exist_ok=True)
for p in(W/'exports').iterdir():
 if p.is_file()and p.suffix in ['.aseprite','.webp']:shutil.copy2(p,ex/p.name)
for p in [O/'README.md',source/'README.md',R/'docs/STAGE5_BOMBER_ASSAULT_1114.md']:p.write_text(readme,encoding='utf-8')
sources={str(p.relative_to(source)).replace('\\','/'):sha(p)for p in source.rglob('*')if p.is_file()and p.name!='source-hashes.json'};(source/'source-hashes.json').write_text(json.dumps(sources,indent=2))
summary=dict(nativeChecks=len(C['checks']),weaponChecks=len(G['checks']),totalChecks=total,editable=A,seconds=seconds,phases=V['phases'],audioPeak=V['stats']['peak'],sourceHashes=V['sourceHashes'],protected=I['protected'],movieSha256=V['sha256'],errors=[],requiredChecks=Q,playbackSeeks=V['playbackSeeks'])
(O/'verification.json').write_text(json.dumps(summary,indent=2));qa=R/'docs/qa/stage5_bomber_assault_1114';qa.mkdir(parents=True,exist_ok=True)
for p in[O/'verification.json',O/'checks.json',O/'required-checks.json',O/'full-suite.log',O/'native-traces.json',O/'weapon-gate/weapon-gate-checks.json',W/'editable-verification.json',W/'art-audit.json']:shutil.copy2(p,qa/p.name)
note=f'''## November14,2026 — Stage5 bomber hunting optics and overhead bombing pursuit

Mike requested a more active Stage5 miniboss. S5B14 now owns the actual Stage5
Eclipse Siege Bomber: committed enemy optic/cannon bursts, visible cooling and
repeat bursts, thrust away/turnaround, accelerating bombing charge, shadow-led
overhead pass, return and finite forward-responsive catch-up. The original four
modules/core gate/HP/white flashes/native defeat remain. Engine breaks slow flight;
cannon breaks cancel their fire. Upper-plane hulls cannot ram or absorb rounds.
No player Retina/input takeover or new runtime raster transforms. Original hull,
module/FX pixels plus a new exclusive clear-center16-frame enemy optic.16 headings,
32 prepared depths;1,136 exact editable exports in46 banks (includes variants).
{total} native behavior/weapon checks pass across all four difficulties; final audible
Furious preview completes native entry and two cycles with full original HP.
Invulnerable review pilot; not a survival or release claim. Syntax passes; full
suite retains the existing missing difficultyHealthBaseline15 abort. Protected
Chronus/Draconus and Stage6 owners unchanged. Source only; no push/installer.
Docs: docs/STAGE5_BOMBER_ASSAULT_1114.md; _ART_SOURCES/stage5_bomber_assault_1114.

'''
p=R/'HANDOFF_CODEX.md';old=p.read_bytes()
if note.splitlines()[0].encode()not in old:assert p.read_bytes()==old;p.write_bytes(note.encode()+old)
rule='''\n\n## November14 — Stage5 miniboss active bomber pursuit and enemy optics

Mike requests Stage5 Eclipse's thrust-away/head-on bombing/overhead shadow/finite
catch-up cycle and its own Stage4-like target/committed cannon burst/cool/repeat
behavior. Preserve S5B14's real native four-module/core gate, original pools,
visible white damage feedback and native breakup/reward. Never restore broken
engines/cannons or heal at flight transitions. Engine loss slows flight; cannon
loss cancels queued/released fire. Upper-plane hulls must not ram, absorb weapons
or remain offensive Retina targets. Only this controlled bomber skips additive
space bob after entry; other space actors keep their owner. Native bomb impact
warnings remain readable over the big foreground hull and preserve a dodge gap.
Its enemy-owned clear-center optic must not take over player Retina controls.
Keep authored sprite banks, fixed pivots and offline headings/depths, with no
runtime raster transforms. Keep Stage6 pursuit and critical original Chronus
formation/wave/current Draconus work untouched. Evidence and recovery source:
docs/STAGE5_BOMBER_ASSAULT_1114.md. Furious film is an invulnerable attack review.
'''
p=R/'AGENTS.md';old=p.read_bytes()
if rule.splitlines()[2].encode()not in old:assert p.read_bytes()==old;p.write_bytes(old+rule.encode())
with zipfile.ZipFile(O/'BOF-Stage5-bomber-assault-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3)as z:
 for p in source.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(source))
assert all(sha(R/n)==h for n,h in I['protected'].items())
print('Complete:',total,'native checks,1136 exact editable frames, final Furious preview and recovery handoff.',flush=True)
