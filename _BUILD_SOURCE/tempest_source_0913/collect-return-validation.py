"""Record the complete suite comparison and inspect the encoded return-pass movie."""
from pathlib import Path
import hashlib,json,re,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[2]
out=root/'_shots/tempest_return_0913'
log=(out/'test_fl.log').read_text(encoding='utf-8-sig')
assert '=== 296.'in log and '============================================'in log,'suite not finished'
fail=[s.strip()for s in log.splitlines()if s.strip().startswith('ASSERT FAIL:')]
baseline_path=root/'docs/qa/tempest_fighter_0913.json'
baseline=json.loads(baseline_path.read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\d+(?:\.\d+)?','#',s.strip())
new=[s for s in fail if norm(s)not in {norm(s)for s in baseline['suite']['failureNames']}]
probe=json.loads((out/'results.json').read_text(encoding='utf-8'))
movie=out/'BulletsOfFury_Tempest_ExitAndReturn.mp4'
ff=imageio_ffmpeg.get_ffmpeg_exe()
decoded=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','NUL'],capture_output=True,text=True)
assert decoded.returncode==0 and not decoded.stderr,decoded.stderr
packets=subprocess.run([ff,'-v','error','-i',str(movie),'-map','0:v','-c:v','copy','-f','framecrc','pipe:1'],capture_output=True,text=True)
frames=sum(s.startswith('0,')for s in packets.stdout.splitlines())
assert frames==900,frames
stats=subprocess.run([ff,'-hide_banner','-i',str(movie),'-vn','-af','volumedetect','-f','null','NUL'],capture_output=True,text=True)
volume=[s for s in stats.stderr.splitlines()if 'volume:'in s]
assert '960x1024'in stats.stderr and 'Duration: 00:00:30.00'in stats.stderr,stats.stderr[-2000:]
report={
  'date':'2026-09-13',
  'suite':{'passed':sum(s.startswith('  ok  ')for s in log.splitlines()),'failed':len(fail),
    'exitCode':int(bool(fail)),'newFailureNames':new,'failureNames':fail,
    'baseline':{'path':str(baseline_path.relative_to(root)).replace('\\','/'),
      'sha256':hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
      'passed':baseline['suite']['passed'],'failed':baseline['suite']['failed']},
    'log':'_shots/tempest_return_0913/test_fl.log'},
  'browser':probe,
  'files':[{'path':str(p.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in [root/'assets/game.js',root/'_BUILD_SOURCE/test_fl.js',root/'_BUILD_SOURCE/tempest_source_0913/fighter.js',root/'_BUILD_SOURCE/probe_tempest_fighter_0913.py']],
  'video':{'path':str(movie.relative_to(root)).replace('\\','/'),'bytes':movie.stat().st_size,
    'durationSeconds':30,'frames':frames,'width':960,'height':1024,'fps':30,'fullDecodeErrors':0,
    'driver':'real movement input; invincible demo pilot; no accelerated health gates',
    'audio':'frame-stamped game samples and held engine-loop replay; stereo AAC','audioVolume':volume}
}
(root/'docs/qa/tempest_return_0913.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'suitePassed':report['suite']['passed'],'suiteFailed':len(fail),'newFailureNames':new,
  'browserPassed':sum(c['pass']for c in probe['checks']),'browserFailed':[c for c in probe['checks']if not c['pass']],
  'browserErrors':probe['errors'],'exits':probe['motion']['exits'],'returns':probe['motion']['returns'],
  'noseMismatch':probe['motion']['noseMismatch'],'frames':frames,'videoBytes':movie.stat().st_size,'audioVolume':volume},indent=2))
sheet=Image.new('RGB',(320*4,370*3),'#111821')
for i,t in enumerate([2.7,5.5,6.2,6.5,7,8,8.5,9,13.8,15,16,18]):
    path=out/('encoded_%04.1fs.png'%t)
    subprocess.run([ff,'-y','-loglevel','error','-ss',str(t),'-i',str(movie),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((320,342))
    sheet.paste(im,(i%4*320,i//4*370))
    ImageDraw.Draw(sheet).text((i%4*320+8,i//4*370+348),str(t)+' seconds',fill='white')
sheet.save(out/'encoded_contact.png')
