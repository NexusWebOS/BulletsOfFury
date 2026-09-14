import json,threading,http.server,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path.cwd();sys.path.insert(0,str(R/'_BUILD_SOURCE/shared_laser_warnings_0914'));import record
class Q(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(R),**k)
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),Q);threading.Thread(target=s.serve_forever,daemon=True).start()
e=json.loads((record.OUT/'pause_flow_events.json').read_text())
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);g=b.new_page();g.goto('http://127.0.0.1:%d/index.html'%s.server_port,wait_until='load')
 print('COUNTS', {n:sum(v[1]==n for v in e['snd'])for n in set(v[1]for v in e['snd'])},flush=True)
 for n in set(v[1]for v in e['snd']):
  x=dict(e);x['snd']=[v for v in e['snd']if v[1]==n];x['syn']=[];x['warp']=[];x['loops']={}
  r=g.evaluate(record.render_audio.RENDER,{'ev':x,'iife':record.render_audio.audio_module_source(),'tail':0,'exclude':['@synth']});print(n,r['peak'],r['errs'],flush=True)
 b.close()
s.shutdown()
