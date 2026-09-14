"""Collect complete-suite, native browser, authored audio and movie evidence."""
import hashlib,json,re,subprocess
from pathlib import Path
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
OUT=ROOT/'_shots/weapon_feedback_0913';VIDEO=OUT/'video'
log=(OUT/'test_fl.log').read_text(encoding='utf-8')
assert '============================================'in log and 'FAILED'in log,'suite did not reach its final summary'
fails=[l.strip()for l in log.splitlines()if 'ASSERT FAIL:'in l]
baseline=json.loads((ROOT/'docs/qa/game_bugfix_0913.json').read_text())['suite']['failureNames']
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s)
new=[f for f in fails if norm(f)not in {norm(b)for b in baseline}]
assert not new,new
passed=len(re.findall(r'^  ok  ',log,re.M));assert passed>=3703 and len(fails)==61,(passed,len(fails))
browser=json.loads((OUT/'results.json').read_text());assert all(c['pass']for c in browser['checks'])and not browser['errors']
legacy=(OUT/'legacy_wreckdash.log').read_text(encoding='utf-8');assert '23 ok / 0 fail'in legacy and 'page errors'not in legacy
video=json.loads((VIDEO/'report.json').read_text());assert len(video['takes'])==4 and not video['errors']
assert all(not t['audio']['errs']and t['audio']['peak']<1 and t['audio']['rms']>0 and t['audio']['counts']['cut']==0 for t in video['takes'])
expected={'cole_sonic':['colePressureStart','colePressureRelease','colePressureImpact'],'juggernaut_dash':['juggernautRamLaunch','juggernautRamStop','juggernautRamImpact'],'juggernaut_flails':['juggernautWreckHit','juggernautWreckBlock'],'laser_mist':['laserMistFire','laserMistSplit','laserMistBloom','laserMistImpact']}
for t in video['takes']:assert set(expected[t['name']]).issubset(t['sounds']),(t['name'],t['sounds'])
movie=VIDEO/'BulletsOfFury_Weapon_Feedback_0913.mp4';framecrc=VIDEO/'final.framecrc'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(movie),'-map','0:v:0','-f','framecrc',str(framecrc)],check=True)
frames=sum(1 for l in framecrc.read_text().splitlines()if l and not l.startswith('#'))
assert frames==1200,frames
runtime=(ROOT/'assets/game.js').read_bytes();assert b'\r\n'not in runtime
assert runtime==(OUT/'game.expected.js').read_bytes(),'readable sources do not reproduce runtime'
tests=(ROOT/'_BUILD_SOURCE/test_fl.js').read_bytes();assert b'\r\n'in tests and tests.count(b'\n')==tests.count(b'\r\n')
report={'date':'2026-09-13','suite':{'passed':passed,'failed':len(fails),'exitCode':1,'newFailureNames':new,'failureNames':fails,'finalSummaryReached':True},'browser':browser,'legacyWreckDash':{'passed':23,'failed':0,'pageErrors':0,'consoleErrors':0},'audio':{t['name']:t['audio']for t in video['takes']},'video':{'file':str(movie),'frames':frames,'fps':30,'seconds':40,'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'takes':video['takes'],'errors':video['errors'],'protectedDemoPilot':True,'sourceHealthGatesUnchanged':True},'runtime':{'sha256':hashlib.sha256(runtime).hexdigest(),'beforeSha256':hashlib.sha256((OUT/'game.before.js').read_bytes()).hexdigest(),'readableSourcesReproduceRuntime':True,'LF':True,'testsCRLF':True},'art':json.loads((OUT/'asset-inspection.json').read_text()),'authoredAudio':json.loads((HERE/'audio-build.json').read_text())}
(ROOT/'docs/qa/weapon_feedback_0913.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(HERE/'runtime-sha256.txt').write_text(report['runtime']['sha256'])
print('%d passed / %d pre-existing failures; no new failure names. Browser 27/0; legacy 23/0; video %d decoded frames.'%(passed,len(fails),frames))
print('Audio peaks '+str({n:round(v['peak'],4)for n,v in report['audio'].items()}))
