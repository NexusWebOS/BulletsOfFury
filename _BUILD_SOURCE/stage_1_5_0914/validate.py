"""Collect measured full-suite, native pixels, audio and complete movie evidence."""
import hashlib,json,re,subprocess
from pathlib import Path
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
OUT=ROOT/'_shots/stage_1_5_0914';VIDEO=OUT/'video'
log=(OUT/'test-final-current.log').read_text(encoding='utf-8')
assert '============================================' in log and 'FAILED' in log,'suite did not reach its final summary'
fails=[l.strip() for l in log.splitlines() if 'ASSERT FAIL:' in l]
baseline=json.loads((ROOT/'docs/qa/weapon_feedback_0913.json').read_text())['suite']['failureNames']
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s)
new=[f for f in fails if norm(f) not in {norm(b) for b in baseline}]
missing=[f for f in baseline if norm(f) not in {norm(b) for b in fails}]
passed=len(re.findall(r'^  ok  ',log,re.M))
assert passed==3724 and len(fails)==61 and not new and not missing,(passed,len(fails),new,missing)
section=log[log.index('=== 299.'):log.index('============================================',log.index('=== 299.'))]
assert len(re.findall(r'^  ok  ',section,re.M))==21,section
browser=json.loads((OUT/'results.json').read_text())
assert len(browser['checks'])==42 and all(c['pass'] for c in browser['checks']) and not browser['errors']
assert not browser['details']['error']
video=json.loads((VIDEO/'report.json').read_text())
assert len(video['takes'])==10 and sum(t['seconds'] for t in video['takes'])==76 and not video['errors']
assert all(not t['audio']['errs'] and 0<t['audio']['rms'] and t['audio']['peak']<1 for t in video['takes'])
movie=VIDEO/'BulletsOfFury_Stages_1_to_5_0914.mp4';crc=VIDEO/'final.framecrc'
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-y','-v','error','-i',str(movie),'-map','0:v:0','-f','framecrc',str(crc)],check=True)
frames=sum(1 for l in crc.read_text().splitlines() if l and not l.startswith('#'))
assert frames==2280,frames
subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
info=subprocess.run([ff,'-hide_banner','-i',str(movie)],capture_output=True,text=True).stderr
assert '960x1024' in info and '30 fps' in info and 'Audio: aac' in info and '48000 Hz, stereo' in info
runtime=(ROOT/'assets/game.js').read_bytes();tests=(ROOT/'_BUILD_SOURCE/test_fl.js').read_bytes()
assert b'\r\n' not in runtime and runtime==(OUT/'game.expected.js').read_bytes()
assert b'\r\n' in tests and tests.count(b'\n')==tests.count(b'\r\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inspection=json.loads((OUT/'inspection.json').read_text())
assert not inspection['errors']
report={'date':'2026-09-14','suite':{'passed':passed,'failed':len(fails),'exitCode':1,'finalSummaryReached':True,'newSection299Passed':21,'baseline':'docs/qa/weapon_feedback_0913.json','comparison':'Assertion names compared with dynamic numeric observations normalized.','newFailureNames':new,'missingBaselineFailureNames':missing,'failureNames':fails},'browser':browser,'runtime':{'sha256':sha(ROOT/'assets/game.js'),'beforeSha256':sha(OUT/'game.before.js'),'testSha256':sha(ROOT/'_BUILD_SOURCE/test_fl.js'),'readableSourcesReproduceRuntime':True,'LF':True,'testsCRLF':True},'art':inspection,'storedBoats':json.loads((ROOT/'docs/STAGE3_STORED_BOATS_0914.json').read_text()),'video':{'file':str(movie),'frames':frames,'fps':30,'seconds':76,'bytes':movie.stat().st_size,'sha256':sha(movie),'videoCodec':'h264','audioCodec':'aac','audioHz':48000,'audioChannels':2,'decodeExitCode':0,'errors':video['errors'],'protectedDemoPilot':True,'nativeDebugEncounters':True,'fixtures':'Native debug encounters and selected attack windows. Stage-4 demo starts after the 75/50-percent health gates with 1-HP nodes, then uses actual held laser input. Player damage disabled for recording.','audioScope':'Accepted native sound samples, loops and game-module cues, aligned to captured frames. Music is not included. Sound-pool voice reuse is reproduced; audio is not normalized for export.','takes':video['takes']},'audio':{t['name']:t['audio'] for t in video['takes']},'settings':{'laserCannonGain':.30,'regentCombatEffectsGain':.40,'shadowOrbDamageMultiplier':1.35,'stage5SkyLeadSeconds':5,'encounterSoundRoutes':24},'sources':{p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.suffix in ['.py','.js']}}
(ROOT/'docs/qa/stage_1_5_0914.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(VIDEO/'audit.json').write_text(json.dumps(report['video'],indent=2),encoding='utf-8')
(HERE/'runtime-sha256.txt').write_text(report['runtime']['sha256'])
print('%d passed / %d failures, suite exit 1; all failure names match the prior baseline. Section 299: 21/0. Chromium: 42/0. Movie: %d decoded frames.'%(passed,len(fails),frames))
print('Native sound-mixer peaks '+str({n:round(v['peak'],4) for n,v in report['audio'].items()}))
