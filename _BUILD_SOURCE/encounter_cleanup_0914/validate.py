"""Collect measured full-suite, native pixels, audio and complete movie evidence."""
import hashlib,json,re,subprocess
from pathlib import Path
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
OUT=ROOT/'_shots/encounter_cleanup_0914';VIDEO=OUT/'video'
log=(OUT/'tests.log').read_text(encoding='utf-8')
assert '============================================' in log and 'FAILED' in log,'suite did not reach its final summary'
fails=[l.strip() for l in log.splitlines() if 'ASSERT FAIL:' in l]
baseline=json.loads((ROOT/'docs/qa/stage_1_5_0914.json').read_text())['suite']['failureNames']
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s)
new=[f for f in fails if norm(f) not in {norm(b) for b in baseline}]
missing=[f for f in baseline if norm(f) not in {norm(b) for b in fails}]
passed=len(re.findall(r'^  ok  ',log,re.M))
assert passed==3734 and len(fails)==60 and not new and missing==['ASSERT FAIL: stage 1: the sand tanks spawn (scroll never)'],(passed,len(fails),new,missing)
section=log[log.index('=== 300.'):log.index('============================================',log.index('=== 300.'))]
assert len(re.findall(r'^  ok  ',section,re.M))==9,section
browser=json.loads((OUT/'results.json').read_text())
assert len(browser['checks'])==47 and all(c['pass'] for c in browser['checks']) and not browser['errors']
assert not browser['details']['error']
video=json.loads((VIDEO/'report.json').read_text())
assert len(video['takes'])==4 and sum(t['seconds'] for t in video['takes'])==37 and not video['errors']
assert all(not t['audio']['errs'] and 0<t['audio']['rms'] and t['audio']['peak']<1 for t in video['takes'])
movie=VIDEO/'BulletsOfFury_Readable_Attacks_0914.mp4';crc=VIDEO/'final.framecrc'
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-y','-v','error','-i',str(movie),'-map','0:v:0','-f','framecrc',str(crc)],check=True)
frames=sum(1 for l in crc.read_text().splitlines() if l and not l.startswith('#'))
assert frames==1110,frames
subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True)
info=subprocess.run([ff,'-hide_banner','-i',str(movie)],capture_output=True,text=True).stderr
assert '960x1024' in info and '30 fps' in info and 'Audio: aac' in info and '48000 Hz, stereo' in info
runtime=(ROOT/'assets/game.js').read_bytes();tests=(ROOT/'_BUILD_SOURCE/test_fl.js').read_bytes()
assert b'\r\n' not in runtime and runtime==(OUT/'game.expected.js').read_bytes()
assert b'\r\n' in tests and tests.count(b'\n')==tests.count(b'\r\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inspection=json.loads((OUT/'inspection.json').read_text())
assert not inspection['errors']
report={'date':'2026-09-14','suite':{'passed':passed,'failed':len(fails),'exitCode':1,'finalSummaryReached':True,'newSection300Passed':9,'baseline':'docs/qa/stage_1_5_0914.json','comparison':'Assertion names compared with dynamic numeric observations normalized.','newFailureNames':new,'missingBaselineFailureNames':missing,'failureNames':fails},'browser':browser,'runtime':{'sha256':sha(ROOT/'assets/game.js'),'beforeSha256':sha(OUT/'game.before.js'),'testSha256':sha(ROOT/'_BUILD_SOURCE/test_fl.js'),'readableSourcesReproduceRuntime':True,'LF':True,'testsCRLF':True},'art':inspection,'storedBoats':json.loads((ROOT/'docs/STAGE3_STORED_BOATS_0914.json').read_text()),'video':{'file':str(movie),'frames':frames,'fps':30,'seconds':37,'bytes':movie.stat().st_size,'sha256':sha(movie),'videoCodec':'h264','audioCodec':'aac','audioHz':48000,'audioChannels':2,'decodeExitCode':0,'errors':video['errors'],'protectedDemoPilot':True,'nativeDebugEncounters':True,'fixtures':'Native debug encounters, straight jet waves and selected Stage-3 cannon/Stage-2 head attack windows. Player damage disabled for recording. Regent runs its native encounter for 18 seconds.','audioScope':'Accepted native sound samples, loops and game-module cues, aligned to captured frames. Music is not included. Sound-pool voice reuse is reproduced; audio is not normalized for export.','takes':video['takes']},'audio':{t['name']:t['audio'] for t in video['takes']},'settings':{'warningSeconds':3,'headWarningSeconds':1.65,'headAimLockSeconds':.70,'playerFlameScale':.75,'furnaceFlameWidthMultiplier':1.25,'spaceImpactDecorationCap':6},'sources':{p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.suffix in ['.py','.js']}}
(ROOT/'docs/qa/encounter_cleanup_0914.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(VIDEO/'audit.json').write_text(json.dumps(report['video'],indent=2),encoding='utf-8')
(HERE/'runtime-sha256.txt').write_text(report['runtime']['sha256'])
print('%d passed / %d failures, suite exit 1; no new failing assertion names; one prior random spawn assertion passed this run. Section 300: 9/0. Chromium: 47/0. Movie: %d decoded frames.'%(passed,len(fails),frames))
print('Native sound-mixer peaks '+str({n:round(v['peak'],4) for n,v in report['audio'].items()}))
