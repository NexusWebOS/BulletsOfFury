"""Real short native fight with deliberately unavailable upload endpoint.
Verify that the retained MediaRecorder data reaches a local browser download.
This fixture is not included in the user's encounter coverage.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);c=b.new_context(viewport={'width':1280,'height':720},accept_downloads=True);p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.route('**/__capture/**',lambda r:r.fulfill(status=503,body='test unavailable endpoint'))
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>5');p.add_script_tag(content=(W/'furious_bot.js').read_text())
  with p.expect_download(timeout=90000)as d:
   p.evaluate('(q)=>FURYBOT.start(q)',dict(id='qa_buffer_save',stage=2,role='elite',kind='caldera',name='BUFFER TEST',limit=30))
  file=W/'qa_buffer_save.webm';d.value.save_as(file);q=p.evaluate('()=>FURYBOT.report()')
  report={'nativeDefeat':q['completed'],'bytes':file.stat().st_size,'uploadFailureObserved':bool(q.get('writeError')),'downloadFilename':d.value.suggested_filename,'pageErrors':errors};report['pass']=report['nativeDefeat']and report['bytes']>100000 and report['uploadFailureObserved']and not errors
  (W/'buffer-probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
