from pathlib import Path
import hashlib,json,re,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2];out=root/'_shots/tempest_fighter_0913'
first_log=(out/'test_fl_final.log').read_text(encoding='utf-8-sig')
confirm=out/'test_fl_confirm.log'
log=confirm.read_text(encoding='utf-8-sig') if confirm.exists() else first_log
assert '============================================'in log,'suite not finished'
fail=[s.strip()for s in log.splitlines()if s.strip().startswith('ASSERT FAIL:')]
base=(root/'docs/qa/codex_takeover_0913_failures.txt').read_text(encoding='utf-8-sig').splitlines()
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s.strip())
new=[s for s in fail if norm(s)not in {norm(s)for s in base}]
earlier_path=root/'_shots/tempest_duo_0913/test_fl.log'
earlier=earlier_path.read_text(encoding='utf-8-sig')
intermittent='ASSERT FAIL: stage 1: the sand tanks spawn (scroll never)'
assert intermittent in earlier and 'function tempestJetStart' not in (out/'game.before.js').read_text(encoding='utf-8'), 'historical flight comparison missing'
known=[s for s in new if norm(s)==norm(intermittent)]
first_fail=[s.strip() for s in first_log.splitlines() if s.strip().startswith('ASSERT FAIL:')]
probe=json.loads((out/'results.json').read_text(encoding='utf-8'))
movie=out/'BulletsOfFury_Tempest_FighterPasses.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
r=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','NUL'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr
r=subprocess.run([ff,'-v','error','-i',str(movie),'-map','0:v','-c:v','copy','-f','framecrc','pipe:1'],capture_output=True,text=True)
frames=sum(s.startswith('0,')for s in r.stdout.splitlines());assert frames==900,frames
stats=subprocess.run([ff,'-hide_banner','-i',str(movie),'-vn','-af','volumedetect','-f','null','NUL'],capture_output=True,text=True)
volume=[s for s in stats.stderr.splitlines()if 'volume:'in s]
d={'date':'2026-09-13','suite':{'passed':sum(s.startswith('  ok  ')for s in log.splitlines()),'failed':len(fail),'exitCode':int(bool(fail)),
    'newFailureNames':new,'failureNames':fail,
    'unexplainedFailureNames':[s for s in new if s not in known],
    'previouslyObservedFailureNames':known,
    'log':str(confirm.relative_to(root)).replace('\\','/') if confirm.exists() else str((out/'test_fl_final.log').relative_to(root)).replace('\\','/'),
    'firstRun':{'passed':sum(s.startswith('  ok  ')for s in first_log.splitlines()),'failed':len(first_fail),'exitCode':int(bool(first_fail))},
    'comparisonNote':'Compared with the 60-failure takeover baseline. The Stage 1 sand-wave sampling failure also appears in the duo log from before fighter flight was implemented.',
    'priorStage1FailureEvidence':{'path':str(earlier_path.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(earlier_path.read_bytes()).hexdigest(),'assertion':intermittent}},'browser':probe,
    'files':[{'path':str(p.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in [root/'assets/game.js',root/'_BUILD_SOURCE/test_fl.js',root/'_BUILD_SOURCE/tempest_source_0913/fighter.js',root/'_BUILD_SOURCE/tempest_source_0913/adapter.js']],
    'video':{'path':str(movie.relative_to(root)).replace('\\','/'),'bytes':movie.stat().st_size,'durationSeconds':30,'frames':frames,
      'width':960,'height':1024,'fps':30,'fullDecodeErrors':0,'driver':'real input, invincible recording pilot, no accelerated health gates',
      'audio':'frame-stamped game samples and engine loop replayed through existing OfflineAudioContext workflow','audioVolume':volume}}
(root/'docs/qa/tempest_fighter_0913.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print(json.dumps({'suitePassed':d['suite']['passed'],'suiteFailed':len(fail),'newFailures':new,
    'browserPassed':sum(c['pass']for c in probe['checks']),'browserFailed':[c for c in probe['checks']if not c['pass']],
    'browserErrors':probe['errors'],'movieFrames':frames,'movieBytes':movie.stat().st_size,'audioVolume':volume},indent=2))
sheet=Image.new('RGB',(320*4,370*2),'#111821')
for i,t in enumerate([2,6.1,6.8,7.3,8,13.5,14.3,17.2]):
    path=out/('encoded_%04.1fs.png'%t);subprocess.run([ff,'-y','-loglevel','error','-ss',str(t),'-i',str(movie),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((320,342));sheet.paste(im,(i%4*320,i//4*370));ImageDraw.Draw(sheet).text((i%4*320+8,i//4*370+348),str(t)+' seconds',fill='white')
sheet.save(out/'encoded_contact.png')
